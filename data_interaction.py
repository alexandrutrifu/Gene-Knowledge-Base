import sqlite3
import pandas as pd
import numpy as np

def load_js_callback(filename):
	with open(filename, 'r') as file:
		return file.read()

def get_dataframe(table_name):
	con = sqlite3.connect('database/gene-knowledge-db')

	# Read the original database
	cursor = con.cursor()
	df = pd.read_sql_query(f"SELECT * FROM {table_name}", con)

	# Adjust the p-value to be negative log10
	df['adj.P.Val'] = -1 * df['adj.P.Val'].apply(np.log10)

	# Rename problematic column name
	df.rename(columns={'adj.P.Val': 'adj_P_Val'}, inplace=True)

	return df

def get_donor_data(gene_name):
	pass