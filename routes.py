import json

import numpy as np
from flask import Blueprint, render_template, stream_with_context, Response, jsonify

from ai_interaction import callOpenAI, PROMPT_PUBMED, GENE_INFO_DESC_PROMPT
from donor_plot import get_age_comparison_plot
from gene_requests import request_pubmed_references
from volcano_plot import generate_volcano_plot

from data_interaction import *

# Main Flask blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
	script, div = generate_volcano_plot(dataframes.df_values, dataframes.df_limma)

	return render_template('home.html', script=script, div=div)

@main_bp.route('/gene/<gene_id>')
def get_gene_info(gene_id):
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
	# Get components of the donor box plot
	script, div = get_age_comparison_plot(dataframes.df_values, gene_id)

	# TODO: compute extra info about donors + normal distribution test

	# TODO: summarize information through OpenAI call

	return jsonify({
		"script": script,
		"div": div
	})

@main_bp.route('/gene/<gene_id>/ref')
def get_gene_references(gene_id):
	# Get gene PUBMED references
	gene_references = str(request_pubmed_references(gene_id))

	#TODO: select most relevant articles to display

	#TODO: add option for viewing the full reference list
