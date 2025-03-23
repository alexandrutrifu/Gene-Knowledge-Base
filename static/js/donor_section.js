/** Fetches donor information & plot based on OpenAI backend calls
 *
 * @param gene_id EntrezGeneID
 * @param donor_plot_container
 */
function fetchDonorInfo(gene_id, donor_plot_container) {
	// Change URL
	history.pushState({}, '', `/gene/${gene_id}/donors`);

	fetch(`/gene/${gene_id}/donors`)
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
}

export function createDonorSection() {
	// Get donor section element
	const donor_section = document.querySelector(".donor-section");

	// Create main containers
	const donor_container = document.createElement("div");
	const donor_plot_container = document.createElement("div");
	const donor_info_container = document.createElement("div");

	donor_container.className = "donor-container";
	donor_plot_container.className = "donor-plot-container";
	donor_info_container.className = "donor-info-container";

	// Append child containers
	donor_container.appendChild(donor_plot_container);
	donor_container.appendChild(donor_info_container);
	donor_section.appendChild(donor_container);

	// Get gene ID from route
	const pathTokens = window.location.pathname.split("/");
	const gene_id = pathTokens[pathTokens.indexOf("gene") + 1];

	// Fetch donor information from Flask backend and populate containers
	fetchDonorInfo(gene_id, donor_plot_container);
}