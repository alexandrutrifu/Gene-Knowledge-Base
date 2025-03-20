import numpy as np
from flask import Blueprint, render_template

from ai_interaction import callOpenAI, PROMPT_PUBMED
from gene_requests import get_pubmed_references
from volcano_plot import generate_volcano_plot

from data_interaction import get_dataframe, get_donor_data

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
	# Get dataframes from gene database
	s4a_df = get_dataframe("s4a_values")
	s4b_df = get_dataframe("s4b_limma")

	# Adjust the p-value to be negative log10
	s4b_df['adj.P.Val'] = -1 * s4b_df['adj.P.Val'].apply(np.log10)

	# Rename problematic column name
	s4b_df.rename(columns={'adj.P.Val': 'adj_P_Val'}, inplace=True)

	script, div = generate_volcano_plot(s4b_df)

	return render_template('home.html', script=script, div=div)

@main_bp.route('/gene/<gene_id>')
def get_gene_info(gene_id):
	gene_references = str(get_pubmed_references(gene_id))

	# Call OpenAI API to request information
	response = callOpenAI(dev_prompt=PROMPT_PUBMED, user_request=gene_references)