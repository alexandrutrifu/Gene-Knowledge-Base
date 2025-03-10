import pandas as pd
import sqlite3
import numpy as np

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components


def generate_plot():
	con = sqlite3.connect('database/gene-knowledge-db')

	# Read the original database
	cursor = con.cursor()

	df = pd.read_sql_query("SELECT * FROM s4b_limma", con)
	print(df)

	p = figure(title="Volcano plot", x_axis_label='log2 fold change', y_axis_label='-log10 p-value')

	p.scatter(df['logFC'], -1 * df['adj.P.Val'].apply(np.log10), size=5, marker='circle', color='blue')
	p.background_fill_color = None
	p.border_fill_color = None

	script, div = components(p)

	return script, div
