import { observeDonorSentinel } from "./observe_donor_section.js"


// Monitor active fetch requests through global variable
let active_fetch_controller = null

/** Fetches donor information & plot based on OpenAI backend calls
 *
 * @param gene_id EntrezGeneID
 * @param donor_plot_container
 */
function fetchDonorInfo(gene_id, donor_plot_container, donor_info_container) {
	return new Promise((resolve, reject) => {
		// Change URL
		history.pushState({}, '', `/gene/${gene_id}/donors`);

		// Fetched age comparison plot
		fetch(`/gene/${gene_id}/donors/plot`)
			.then(response => response.json())
			.then(({ script, div }) => {
				const temp = document.createElement("div");
				temp.innerHTML = div;

				// Add all parsed HTML nodes
				for (const node of temp.childNodes) {
					donor_plot_container.appendChild(node);
				}

				// Execute the returned script
				const scriptTag = document.createElement("script");
				scriptTag.textContent = script.replace(/<script.*?>|<\/script>/g, '');
				donor_plot_container.appendChild(scriptTag);

				resolve();
			})
			.catch(err => console.error("Error fetching donor info:", err));

		// Abort previously active fetch requests
		if (active_fetch_controller) {
			active_fetch_controller.abort();
		}

		active_fetch_controller = new AbortController();
		const signal = active_fetch_controller.signal;

		// Get gene information div element to append text in
		let donor_info_box = donor_info_container.querySelector(".donor-info");

		// Interpret donor samples & summarize through OpenAI call
		fetch(`/gene/${gene_id}/donors/stats`, {signal})
			.then(response => {
				const reader = response.body.getReader();
				const decoder = new TextDecoder();
				let generated_info = '';

				// Keep track of bold enclosures
				let openBold = false;

				function readStream() {
					reader.read().then(({done, value}) => {
						if (done) {
							resolve();
							return;
						}

						// Read the next streamed text chunk
						let chunk = decoder.decode(value, {stream: true});

						// Create a new span block to fade in the text
						let span = document.createElement("span");

						if (chunk.includes("**")) {
							openBold = !openBold;
							chunk = " ";
						}

						if (openBold) {
							span.style.fontWeight = "bold";
						}

						span.textContent = chunk;
						span.classList.add("fade-in");

						// Append new text span to textbox
						donor_info_box.appendChild(span);

						if (chunk.includes("\n")) {
							let spacer = document.createElement("div");

							spacer.style.height = "1em";

							donor_info_box.appendChild(spacer);
						}

						// Read next stream chunk
						readStream();
					})
				}

				readStream();
			})
			.catch(reject);
	})
}

/** Inserts donor information inside the corresponding DOM container
 *
 * @param gene_info Dictionary with complete gene records
 * @param donor_plot_container
 * @param donor_info_container
 */
function showDonorInfo(gene_info, donor_plot_container, donor_info_container) {
	if (donor_info_container) {
		// Update content based on selected gene
		donor_info_container.innerHTML = `
			<div class="donor-header">
				<div class="donor-icon-div">
					<img src="/static/images/donor-icon.svg"
						alt="Donor SVG" class="donor-icon">
				</div>
				
				<h2>Age-group Analysis: <span style="color: #C93175">${gene_info["EntrezGeneSymbol"]}</span></h2>
			</div>
			
			<div class="donor-info">
				<!--- Placeholder for text spans which will fade in --->
			</div>
		`;

		fetchDonorInfo(gene_info["EntrezGeneID"], donor_plot_container, donor_info_container)
			.then(() => {
				// Insert empty div to signal the end of the stream (event trigger)
				let endingDiv = document.createElement("div")

				endingDiv.style.height = "0px";
				endingDiv.className = "donor-ending-div";

				donor_info_container.appendChild(endingDiv);
				console.log("finalized")
		});
	}
}

export async function createDonorSection() {
	// Get donor section element
	const donor_section = document.querySelector(".donor-section");

	// Create main containers
	const donor_container = document.createElement("div");
	const donor_sentinel = document.createElement("div");
	const donor_plot_container = document.createElement("div");
	const donor_info_container = document.createElement("div");

	donor_container.className = "donor-container";
	donor_sentinel.className = "sentinel";
	donor_plot_container.className = "donor-plot-container";
	donor_info_container.className = "donor-info-container";

	// donor_section.classList.add("fade-in");

	// Append child containers
	donor_container.appendChild(donor_info_container);
	donor_container.appendChild(donor_plot_container);
	donor_section.appendChild(donor_container);
	donor_section.appendChild(donor_sentinel);

	observeDonorSentinel();

	// Get gene ID from route
	const pathTokens = window.location.pathname.split("/");
	const gene_id = pathTokens[pathTokens.indexOf("gene") + 1];

	// Fetch donor information from Flask backend and populate containers
	const gene_info = await fetch(`/gene/${gene_id}/all`)
									.then(response => response.json());

	console.log(gene_info);

	showDonorInfo(gene_info, donor_plot_container, donor_info_container);
}