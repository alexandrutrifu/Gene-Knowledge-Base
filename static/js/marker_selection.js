const indices = src.selected.indices;

const plotSection = document.querySelector('.plot-section');

// Save original axis ranges
if (x_range.orig_start === undefined) {
	x_range.orig_start = x_range.start;
	x_range.orig_end = x_range.end;
	y_range.orig_start = y_range.start;
	y_range.orig_end = y_range.end;
}

// Zoom on selected marker
if (indices.length > 0) {
	var index = indices[0];
	console.log(index);

	var df_limma = src.data;
	var x = df_limma['logFC'][index];
	var y = df_limma['adj_P_Val'][index];

	// Get gene_id through common Target column
	var gene_target = df_limma['Target'][index];
	var gene_value_index = df_values['Target'].indexOf(gene_target);
	var gene_id = df_values['EntrezGeneID'][gene_value_index];

	// Zoom factor
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

	if (plotSection) {
		plotSection.classList.add("shift-left");
	}

	// Gene Info Box
	var geneInfoBox = document.getElementById("gene-info-box");

	if (geneInfoBox) {
		// Opacity -> 1
		geneInfoBox.classList.add("active");

		// Update content based on selected gene
		geneInfoBox.innerHTML = `
			<div class="gene-header">
				<div class="dna-icon-div">
					<img src="/static/images/dna-icon-gene-box.svg"
						alt="DNA SVG" class="dna-icon">
				</div>
				
				<h2>Gene: ${df_limma['EntrezGeneSymbol'][index]}</h2>
			</div>
			
			<div class="gene-info">
				<!--- Placeholder for text spans which will fade in --->
			</div>
		`;

		// Get gene information div element to append text in
		let geneInfoTextBox = geneInfoBox.querySelector(".gene-info");

		// Fetch gene information from Flask backend
		fetch('/gene/' + gene_id)
			.then(response => {
				const reader = response.body.getReader();
				const decoder = new TextDecoder();
				let generated_info = '';

				function readStream() {
					reader.read().then(({done, value}) => {
						if (done) {
							return;
						}

						// Read the next streamed text chunk
						let chunk = decoder.decode(value, {stream: true});

						// Create a new span block to fade in the text
						let span = document.createElement("span");
						span.textContent = chunk;
						span.classList.add("fade-in");

						// Append new text span to textbox
						geneInfoTextBox.appendChild(span);

						readStream();
					})
				}

				readStream();
			})
			.catch(error => console.error("Error: ", error));
	}

} else {
	// No marker selected = Zoom out
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

	// Gene Info Box
	var geneInfoBox = document.getElementById("gene-info-box");
	if (geneInfoBox) {
		geneInfoBox.classList.remove("active");
	}
}