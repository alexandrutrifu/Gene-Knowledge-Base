import { observeDonorSentinel } from "./observe_donor_section.js"
import { insertScrollDownContainer } from "./scroll_down_containers.js";
import { createReferenceSection } from "./reference_section.js";


// Monitor active fetch requests through global variable
let active_fetch_controller = null

/** Fetches donor information & plot based on OpenAI backend calls
 *
 * @param gene_id EntrezGeneID
 * @param parent_section
 */
function fetchDonorInfo(gene_id, parent_section) {
	const donor_plot_container = parent_section.querySelector(".donor-plot-container");
	const donor_info_container = parent_section.querySelector(".donor-info-container");

	// Reset container content
	donor_plot_container.innerHTML = ``;

	return new Promise((resolve, reject) => {
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

		// Reset container content
		donor_info_box.innerHTML = ``;

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
 * @param parent_section
 */
function showDonorInfo(gene_info, parent_section) {
	// Update content based on selected gene
	const donor_info_container = parent_section.querySelector(".donor-info-container");
	const donor_header = donor_info_container.querySelector(".donor-header");

	const gene_header = donor_header.querySelector("h2");

	gene_header.innerHTML = `
		Age-group Analysis: <span style="color: #C93175">${gene_info["EntrezGeneSymbol"]}</span>
	`;

	// Remove leftover containers
	const scroll_down = parent_section.querySelector(".scroll-down-container");

	if (scroll_down) {
		scroll_down.remove();
	}

	fetchDonorInfo(gene_info["EntrezGeneID"], parent_section)
		.then(() => {
			// Insert scroll down container
			insertScrollDownContainer(donor_info_container);

			// Generate next section
			createReferenceSection(gene_info);
	});
}

export async function createDonorSection() {
	// Get donor section elements
	const donor_section = document.querySelector(".donor-section");
	const sentinel = donor_section.querySelector(".sentinel");

	// Reset height - opacity will be reset by observer
	donor_section.style.height = "auto";
	sentinel.style.display = "block";

	observeDonorSentinel();

	// Get gene ID from route
	const pathTokens = window.location.pathname.split("/");
	const gene_id = pathTokens[pathTokens.indexOf("gene") + 1];

	history.pushState({}, '', `/`);

	// Fetch donor information from Flask backend and populate containers
	const gene_info = await fetch(`/gene/${gene_id}/all`)
									.then(response => response.json());

	console.log(gene_info);

	showDonorInfo(gene_info, donor_section);
}