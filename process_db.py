import pandas as pd
import sqlite3
import numpy as np

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool


def generate_plot():
	con = sqlite3.connect('database/gene-knowledge-db')

	# Read the original database
	cursor = con.cursor()

	df = pd.read_sql_query("SELECT * FROM s4b_limma", con)

	# Get plot data column
	data = {
		'Gene': df['EntrezGeneSymbol'],
		'logFC': df['logFC'],
		'adjPVal': -1 * df['adj.P.Val'].apply(np.log10)
	}

	source = ColumnDataSource(data)

	p = figure(title="Volcano plot", x_axis_label='log2 fold change', y_axis_label='-log10 p-value',
			   width=800, height=800)

	p.scatter(x='logFC', y='adjPVal', source=source,
			  size=5, marker='circle', color='blue')
	p.background_fill_color = None
	p.border_fill_color = None

	hover = HoverTool()
	hover.tooltips = [
		("Gene", "@Gene"),
		("logFC", "@logFC"),
		("adj.P.Val", "@adjPVal")
	]

	p.add_tools(hover)

	script, div = components(p)

	return script, div
