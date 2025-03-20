import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, TapTool, CustomJS, LogColorMapper, ColorBar
from bokeh.palettes import Blues9, linear_palette

from data_interaction import load_js_callback


def generate_volcano_plot(df_values, df_limma):
	""" Renders a volcano plot for comparing protein activity levels.

	:param df_values:
	:param df_limma: Dataframe containing gene sample data.
	:return:
	"""

	# Create density mapping for data concentration in the plot
	density = get_density_map(df_limma)

	# Attach the density values to our dataframe
	# The density is adjusted by 2 to make the plot more readable
	df_limma['density'] = density + 2

	source = ColumnDataSource(df_limma)

	# Create a 256-color blue gradient from light (low) to dark (high)
	blue_palette = linear_palette(Blues9, 9)

	# Create a color mapper from density values
	color_mapper = LogColorMapper(
		palette=blue_palette,
		low=df_limma["density"].min(),
		high=df_limma["density"].max()
	)

	p = figure(title="Volcano plot", x_axis_label='log2 fold change', y_axis_label='-log10 p-value',
			   width=800, height=800)

	p.scatter(x='logFC', y='adj_P_Val', source=source, fill_alpha=0.8,
			  size=5, marker='circle', color={'field': 'density', 'transform': color_mapper})
	p.background_fill_color = None
	p.border_fill_color = None

	# Add a color bar on the right
	color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12, location=(0, 0))
	p.add_layout(color_bar, "right")

	# Add hover tool
	hover = HoverTool()
	hover.tooltips = [
		("Gene", "@EntrezGeneSymbol"),
		("logFC", "@logFC"),
		("adj.P.Val", "@adj_P_Val")
	]

	p.add_tools(hover)

	p.add_tools(TapTool())

	# Convert Values Dataframe to a normal dictionary, passed over to JS code
	df_values_dict = df_values.to_dict(orient="list")

	# JavaScript callback to update DOM when a point is clicked
	zoom_js_code = load_js_callback('static/js/marker_selection.js')
	callback = CustomJS(
		args=dict(
			src=source,
			x_range=p.x_range,
			y_range=p.y_range,
			df_values=df_values_dict
		),
		code=zoom_js_code)

	# Link selection event to callback
	source.selected.js_on_change("indices", callback)

	script, div = components(p)

	return script, div

def get_density_map(df):
	# Create density histogram
	xbins = 200
	ybins = 200

	counts, xedges, yedges = np.histogram2d(df['logFC'], df['adj_P_Val'], bins=(xbins, ybins))

	xidx = np.searchsorted(xedges, df['logFC'])
	yidx = np.searchsorted(yedges, df['adj_P_Val'])

	in_range = (
			(xidx >= 0) & (xidx < xbins) &
			(yidx >= 0) & (yidx < ybins)
	)

	# Create a density array (same length as df) to store the bin count for each point
	density = np.zeros(len(df), dtype=float)
	density[in_range] = counts[xidx[in_range], yidx[in_range]]

	return density
