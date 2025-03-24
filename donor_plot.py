import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool

from data_interaction import get_donor_data


def get_age_comparison_plot(df, gene_id):
	""" Compares protein concentration values in different age groups through a box plot.

	:param df: Dataframe to get donor samples from.
	:param gene_name: Gene for which to inspect the samples.
	:return: Script/Div HTML elements for the box plot.
	"""

	# Get protein concentration values in young/old donor samples
	yd_values, od_values = get_donor_data(df, gene_id)

	# Age groups
	categories = ['Young Donors', 'Elderly Donors']

	# Create the box plot
	p = figure(title="Protein concentration in Young vs. Old Donor Samples",
			   x_axis_label='Age Groups', y_axis_label='Protein Concentration',
			   x_range=categories,
			   width=800, height=800)

	create_box_plot(p, yd_values, categories[0], "#F7717D")
	create_box_plot(p, od_values, categories[1], "#DE639A")

	script, div = components(p)

	return script, div

def create_box_plot(fig, sample_values, category, fill_color):
	""" Renders the box plot corresponding to the provided donor sample.

	:param fig: Bokeh figure to plot inside.
	:param sample_values: Donor sample values.
	:param category: Target age group.
	:param fill_color: Fill color for the box plot.
	:return:
	"""

	# Get series from value lists
	series = pd.to_numeric(pd.Series(sample_values))

	# Get box plot quartiles
	q_min, q1, q2, q3, q_max = series.quantile([0, 0.25, 0.5, 0.75, 1])

	# Interquartile range
	iqr = q3 - q1

	# Outer limits
	upper = q3 + 1.5 * iqr
	lower = q1 - 1.5 * iqr

	# Get list of outliers
	out = series[(series > upper) | (series < lower)]
	outliers = []

	if not out.empty:
		outliers = list(out.values)

	fig.yaxis[0].ticker.desired_num_ticks = 5

	# Stems
	fig.segment([category], upper, [category], q3, line_color="black")
	fig.segment([category], lower, [category], q1, line_color="black")

	# Boxes
	fig.vbar([category], 0.7, q2, q3, line_color="black", fill_color=fill_color)
	fig.vbar([category], 0.7, q1, q2, line_color="black", fill_color=fill_color)

	vbar_height = (q_max - q_min) / 500

	# Whiskers
	fig.rect([category], lower, 0.2, vbar_height, line_color="black")
	fig.rect([category], upper, 0.2, vbar_height, line_color="black")

	if outliers:
		source = ColumnDataSource(data={"x": [category] * len(outliers), "y": outliers})

		scatter = fig.scatter(x="x", y="y", size=10, source=source,
					fill_alpha=0.7, fill_color="#D33643", line_color="#D33643")

		# Add hover tool ONLY for outlier markers
		hover = HoverTool(renderers=[scatter])
		hover.tooltips = [
			("Concentration", "@y")
		]

		fig.add_tools(hover)