import json
import sqlite3
import os
import pandas as pd
import numpy as np
import re

from . import dataframes
from .ai_interaction import callOpenAI, RELEVANT_REF_PROMPT
from .gene_requests import request_pubmed_references


def load_js_callback(filename):
	with open(filename, 'r') as file:
		return file.read()

def get_dataframe(table_name):
	base_dir = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(base_dir, '../database/gene-knowledge-db')
	con = sqlite3.connect(db_path)

	# Read the original database
	cursor = con.cursor()
	df = pd.read_sql_query(f"SELECT * FROM {table_name}", con)

	return df

def get_donor_data(df, gene_id):
	""" Returns protein concentration values across provided donor samples.

	:param df: Dataframe to get donor samples from.
	:param gene_id: Gene for which to inspect the samples.
	:return: Lists of concentration values for young/old donors.
	"""

	column_names = list(df)

	# Regular expressions for young/old donor column names
	young_re = re.compile("Set.*\\.YD.*")
	old_re = re.compile("Set.*\\.OD.*")

	# Get column names encoding young/old donor samples
	young_sample_keys = filter(lambda name: young_re.match(name) is not None, column_names)
	old_sample_keys = filter(lambda name: old_re.match(name) is not None, column_names)

	yd_values = []
	od_values = []

	row_index = np.where(df["EntrezGeneID"] == gene_id)[0][0]

	# Get YD concentration values
	for yd_sample in young_sample_keys:
		yd_values.append(df[yd_sample][row_index])

	# Get OD concentration values
	for od_sample in old_sample_keys:
		od_values.append(df[od_sample][row_index])

	return yd_values, od_values

def clean_dataframe(df):
	# Adjust the p-value to be negative log10
	df['adj.P.Val'] = -1 * df['adj.P.Val'].apply(np.log10)

	# Rename problematic column name
	df.rename(columns={'adj.P.Val': 'adj_P_Val'}, inplace=True)

def retrieve_dataframes():
	# Get dataframes from gene database
	df_values = get_dataframe("s4a_values")
	df_limma = get_dataframe("s4b_limma")

	clean_dataframe(df_limma)

	return df_values, df_limma

def get_gene_parameters(gene_id):
	df_values = dataframes.df_values
	df_limma = dataframes.df_limma

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

def get_complete_info(gene_id):
	gene_info = (dataframes.df_values[dataframes.df_values["EntrezGeneID"] == gene_id])

	return gene_info.to_dict(orient="records")[0]

def populate_gene_references(gene_id):
	# Get gene name
	gene_name = get_complete_info(gene_id)["Target"]

	# Get gene PUBMED references
	gene_references = request_pubmed_references(gene_id)

	request_params = json.dumps({
		"gene_name": gene_name,
		"references": gene_references
	})

	# Call OpenAI API to request relevant references
	reference_conclusions = callOpenAI(dev_prompt=RELEVANT_REF_PROMPT, user_request=request_params)

	# Clean JSON response if necessary
	if reference_conclusions.startswith("```json"):
		reference_conclusions = reference_conclusions.strip("```json").strip("```")

	reference_conclusions = json.loads(reference_conclusions)

	# Populate common resource
	dataframes.current_gene_references = reference_conclusions