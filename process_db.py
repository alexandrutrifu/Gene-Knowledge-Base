from fileinput import filename

import pandas as pd
import sqlite3
import numpy as np

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, TapTool, CustomJS, LogColorMapper, ColorBar
from bokeh.palettes import Blues9, linear_palette


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

	print(density)

	# Attach the density values to your DataFrame
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
	# Pass the plot's ranges to the callback as well
	callback = CustomJS(args=dict(src=source, x_range=p.x_range, y_range=p.y_range), code="""
	    var indices = src.selected.indices;
	    
	    // Shift the plot left when a point is selected
	    plotContainer = document.getElementById("volcano-plot");
	    if (plotContainer) {
	        plotContainer.classList.add("shift-left");
	    }

	    // If original ranges haven't been stored yet, save them.
	    if (x_range.orig_start === undefined) {
	        x_range.orig_start = x_range.start;
	        x_range.orig_end = x_range.end;
	        y_range.orig_start = y_range.start;
	        y_range.orig_end = y_range.end;
	    }

	    // When a marker is selected, zoom in on it.
	    if (indices.length > 0) {
	        var index = indices[0];
	        var data = src.data;
	        var x = data['logFC'][index];
	        var y = data['adjPVal'][index];

	        // Define zoom factor: fraction of the current range to display after zoom
	        var zoom_factor = 0.1;

	        // Compute target ranges based on the zoom factor
	        var current_x_range = x_range.end - x_range.start;
	        var current_y_range = y_range.end - y_range.start;
	        var final_x_range = current_x_range * zoom_factor;
	        var final_y_range = current_y_range * zoom_factor;
	        var final_x_start = x - final_x_range / 2;
	        var final_x_end = x + final_x_range / 2;
	        var final_y_start = y - final_y_range / 2;
	        var final_y_end = y + final_y_range / 2;

	        // Save current ranges as initial values for the animation
	        var init_x_start = x_range.start;
	        var init_x_end = x_range.end;
	        var init_y_start = y_range.start;
	        var init_y_end = y_range.end;

	        // Animation settings
	        var duration = 500; // total animation time in ms
	        var steps = 150;     // number of steps in the animation
	        var step_duration = duration / steps;
	        var current_step = 0;

	        function animateZoomIn() {
	            current_step++;
	            var t = current_step / steps;
	            // Linear interpolation of each boundary
	            x_range.start = init_x_start + t * (final_x_start - init_x_start);
	            x_range.end   = init_x_end   + t * (final_x_end   - init_x_end);
	            y_range.start = init_y_start + t * (final_y_start - init_y_start);
	            y_range.end   = init_y_end   + t * (final_y_end   - init_y_end);
	            if (current_step < steps) {
	                setTimeout(animateZoomIn, step_duration);
	            }
	        }
	        animateZoomIn();

	        // Optionally add a CSS class to slide the plot left
	        var plotContainer = document.getElementById("volcano-plot");
	        if (plotContainer) {
	            plotContainer.classList.add("shift-left");
	        }
	    } else {
	        // No marker selected: animate zooming back out to original ranges.
	        if (x_range.orig_start !== undefined) {
	            var final_x_start = x_range.orig_start;
	            var final_x_end = x_range.orig_end;
	            var final_y_start = y_range.orig_start;
	            var final_y_end = y_range.orig_end;

	            var init_x_start = x_range.start;
	            var init_x_end = x_range.end;
	            var init_y_start = y_range.start;
	            var init_y_end = y_range.end;

	            var duration = 600;
	            var steps = 150;
	            var step_duration = duration / steps;
	            var current_step = 0;

	            function animateZoomOut() {
	                current_step++;
	                var t = current_step / steps;
	                x_range.start = init_x_start + t * (final_x_start - init_x_start);
	                x_range.end = init_x_end + t * (final_x_end - init_x_end);
	                y_range.start = init_y_start + t * (final_y_start - init_y_start);
	                y_range.end = init_y_end + t * (final_y_end - init_y_end);
	                if (current_step < steps) {
	                    setTimeout(animateZoomOut, step_duration);
	                }
	            }
	            animateZoomOut();
	        }
	    }
	""")

	# Link selection event to callback
	source.selected.js_on_change("indices", callback)

	script, div = components(p)

	return script, div
