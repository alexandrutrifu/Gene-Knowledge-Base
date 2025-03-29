from threading import Thread

from flask import Blueprint, render_template, stream_with_context, Response, request, jsonify

from .ai_interaction import callOpenAIStream, GENE_INFO_DESC_PROMPT, DONOR_ANALYSIS_PROMPT
from .donor_plot import get_age_comparison_plot
from .volcano_plot import generate_volcano_plot
from .data_interaction import *

# Main Flask blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == 'POST':
		# POST method behaviour (file submission)
		file = request.files['file']

		# Switch current dataframe with new imported one
		file.save(file.filename)

		dataframes.df_limma = pd.read_csv(file.filename)

		clean_dataframe(dataframes.df_limma)
	else:
		# Use the original dataframe
		dataframes.df_limma = dataframes.original_df_limma.copy()

	script, div, resources = generate_volcano_plot(dataframes.df_values, dataframes.df_limma)

	return render_template('home.html', script=script, div=div, resources=resources)

@main_bp.route('/gene/<gene_id>')
def get_gene_info(gene_id):
	# Get JSON object containing information about the gene's activity level
	gene_parameters = json.dumps(get_gene_parameters(gene_id))

	# Call OpenAI API to request information
	response = Response(
		stream_with_context(
			callOpenAIStream(dev_prompt=GENE_INFO_DESC_PROMPT, user_request=gene_parameters)
		),
		content_type="text/plain"
	)

	# Prepare gene references in parallel so it doesn't slow down the text stream
	ref_thread = Thread(target=populate_gene_references, args=(gene_id,), daemon=True)

	ref_thread.start()

	return response

@main_bp.route('/gene/<gene_id>/donors/plot')
def get_donor_plot(gene_id):
	# Get components of the donor box plot
	script, div = get_age_comparison_plot(dataframes.df_values, gene_id)

	return jsonify({
		"script": script,
		"div": div
	})

@main_bp.route('/gene/<gene_id>/donors/stats')
def get_donor_stats(gene_id):
	# Get significance level from dataframe
	gene_name = get_complete_info(gene_id)["Target"]
	adjusted_p_value = dataframes.df_limma["adj_P_Val"][dataframes.df_limma["Target"] == gene_name].iloc[0]

	# Get donor samples
	yd_values, od_values = get_donor_data(dataframes.df_values, gene_id)

	donor_json = json.dumps({
		"gene_name": gene_name,
		"significance": adjusted_p_value,
		"donor_groups": {
			"young": yd_values,
			"old": od_values
		}
	})

	# Call OpenAI API to request information
	response = Response(
		stream_with_context(
			callOpenAIStream(dev_prompt=DONOR_ANALYSIS_PROMPT, user_request=donor_json)
		),
		content_type="text/plain"
	)

	return response

@main_bp.route('/gene/<gene_id>/ref')
def get_gene_references(gene_id):
	return jsonify(dataframes.current_gene_references)

@main_bp.route('/gene/<gene_id>/all')
def get_all_info(gene_id):
	return jsonify(get_complete_info(gene_id))