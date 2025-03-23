import sqlite3
import pandas as pd
import numpy as np
import re
import dataframes

def load_js_callback(filename):
	with open(filename, 'r') as file:
		return file.read()

def get_dataframe(table_name):
	con = sqlite3.connect('database/gene-knowledge-db')

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