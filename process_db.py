import pandas as pd
import sqlite3
import numpy as np

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, TapTool, CustomJS, LogColorMapper, ColorBar
from bokeh.palettes import Blues9, linear_palette


def load_js_callback(filename):
	with open(filename, 'r') as file:
		return file.read()

def generate_plot():
	data, df = get_sql_data()

	# Create density mapping for data concentration in the plot
	density = get_density_map(data, df)

	# Attach the density values to our dataframe
	# The density is adjusted by 2 to make the plot more readable
	data['density'] = density + 2

	source = ColumnDataSource(data)

	# Create a 256-color blue gradient from light (low) to dark (high)
	blue_palette = linear_palette(Blues9, 9)

	# Create a color mapper from density values
	color_mapper = LogColorMapper(
		palette=blue_palette,
		low=data["density"].min(),
		high=data["density"].max()
	)

	p = figure(title="Volcano plot", x_axis_label='log2 fold change', y_axis_label='-log10 p-value',
			   width=800, height=800)

	p.scatter(x='logFC', y='adjPVal', source=source, fill_alpha=0.8,
			  size=5, marker='circle', color={'field': 'density', 'transform': color_mapper})
	p.background_fill_color = None
	p.border_fill_color = None

	# Add a color bar on the right
	color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12, location=(0, 0))
	p.add_layout(color_bar, "right")

	# Add hover tool
	hover = HoverTool()
	hover.tooltips = [
		("Gene", "@Gene"),
		("logFC", "@logFC"),
		("adj.P.Val", "@adjPVal")
	]

	p.add_tools(hover)

	p.add_tools(TapTool())

	# JavaScript callback to update DOM when a point is clicked
	zoom_js_code = load_js_callback('static/js/zoom.js')
	callback = CustomJS(args=dict(src=source, x_range=p.x_range, y_range=p.y_range),
						code=zoom_js_code)

	# Link selection event to callback
	source.selected.js_on_change("indices", callback)

	script, div = components(p)

	return script, div


def get_density_map(data, df):
	# Create density histogram
	# Number of bins in each dimension (tune as needed)
	xbins = 200
	ybins = 200

	# Create a new plot
	counts, xedges, yedges = np.histogram2d(data['logFC'], data['adjPVal'], bins=(xbins, ybins))

	xidx = np.searchsorted(xedges, data['logFC'])
	yidx = np.searchsorted(yedges, data['adjPVal'])

	in_range = (
			(xidx >= 0) & (xidx < xbins) &
			(yidx >= 0) & (yidx < ybins)
	)

	# Create a density array (same length as df) to store the bin count for each point
	density = np.zeros(len(df), dtype=float)
	density[in_range] = counts[xidx[in_range], yidx[in_range]]

	return density


def get_sql_data():
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

	return data, df
