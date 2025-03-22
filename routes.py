import json

import numpy as np
from flask import Blueprint, render_template, stream_with_context, Response

from ai_interaction import callOpenAI, PROMPT_PUBMED, GENE_INFO_DESC_PROMPT
from donor_plot import get_age_comparison_plot
from gene_requests import get_pubmed_references
from volcano_plot import generate_volcano_plot

from data_interaction import get_dataframe, get_donor_data

# Main Flask blueprint
main_bp = Blueprint('main', __name__)

# Dataframe variables
df_values = None
df_limma = None


def retrieve_dataframes():
	# Get dataframes from gene database
	df_values = get_dataframe("s4a_values")
	df_limma = get_dataframe("s4b_limma")

	# Adjust the p-value to be negative log10
	df_limma['adj.P.Val'] = -1 * df_limma['adj.P.Val'].apply(np.log10)

	# Rename problematic column name
	df_limma.rename(columns={'adj.P.Val': 'adj_P_Val'}, inplace=True)

	return df_values, df_limma

def get_gene_parameters(gene_id):
	global df_values, df_limma

	# Get gene index in Values-Dataframe
	gene_values_index = df_values.index[df_values["EntrezGeneID"] == gene_id][0]
	gene_target = df_values["Target"][gene_values_index]
	gene_limma_index = df_limma.index[df_limma["Target"] == gene_target][0]

	# Put dataframe gene parameters into JSON object
	gene_parameters = {
		"name": df_limma["Target"][gene_limma_index],
		"log_fold_change": df_limma["logFC"][gene_limma_index],
		"adjusted_p_value": df_limma["adj_P_Val"][gene_limma_index]
	}

	return gene_parameters

@main_bp.route('/')
def index():
	global df_values, df_limma

	df_values, df_limma = retrieve_dataframes()

	script, div = generate_volcano_plot(df_values, df_limma)

	return render_template('home.html', script=script, div=div)

@main_bp.route('/gene/<gene_id>')
def get_gene_info(gene_id):
	global df_values, df_limma

	# Get gene PUBMED references
	gene_references = str(get_pubmed_references(gene_id))

	# Get JSON object containing information about the gene's activity level
	gene_parameters = json.dumps(get_gene_parameters(gene_id))

	# Call OpenAI API to request information
	response = Response(
		stream_with_context(
			callOpenAI(dev_prompt=GENE_INFO_DESC_PROMPT, user_request=gene_parameters)
		),
		content_type="text/plain"
	)

	return response

@main_bp.route('/gene/<gene_id>/donors')
def get_gene_donors(gene_id):
	global df_values, df_limma

	# Get components of the donor box plot
	script, div = get_age_comparison_plot(df_values, gene_id)

	# TODO: compute extra info about donors + normal distribution test

	# TODO: summarize information through OpenAI call

	return script, div
