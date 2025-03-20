import numpy as np
from flask import Blueprint, render_template, stream_with_context, Response

from ai_interaction import callOpenAI, PROMPT_PUBMED
from gene_requests import get_pubmed_references
from volcano_plot import generate_volcano_plot

from data_interaction import get_dataframe, get_donor_data

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
	# Get dataframes from gene database
	df_values = get_dataframe("s4a_values")
	df_limma = get_dataframe("s4b_limma")

	# Adjust the p-value to be negative log10
	df_limma['adj.P.Val'] = -1 * df_limma['adj.P.Val'].apply(np.log10)

	# Rename problematic column name
	df_limma.rename(columns={'adj.P.Val': 'adj_P_Val'}, inplace=True)

	script, div = generate_volcano_plot(df_values, df_limma)

	return render_template('home.html', script=script, div=div)

@main_bp.route('/gene/<gene_id>')
def get_gene_info(gene_id):
	gene_references = str(get_pubmed_references(gene_id))

	# Call OpenAI API to request information
	response = Response(
		stream_with_context(
			callOpenAI(dev_prompt=PROMPT_PUBMED, user_request=gene_references)
		),
		content_type="text/plain"
	)

	return response