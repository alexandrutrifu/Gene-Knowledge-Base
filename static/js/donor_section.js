/** Fetches donor information & plot based on OpenAI backend calls
 *
 * @param gene_id EntrezGeneID
 * @param donor_plot_container
 */
function fetchDonorInfo(gene_id, donor_plot_container) {
	return new Promise((resolve, reject) => {
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

				resolve();
			})
			.catch(err => console.error("Error fetching donor info:", err));
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
		// Opacity -> 1
		donor_info_container.classList.add("active");

		// Update content based on selected gene
		donor_info_container.innerHTML = `
			<div class="donor-header fade-in">
				<div class="donor-icon-div">
					<img src="/static/images/donor-icon.svg"
						alt="Donor SVG" class="donor-icon">
				</div>
				
				<h2>Age-group Analysis: </h2>
				<br>
				<h2 style="color: #C93175">${gene_info["EntrezGeneSymbol"]}</h2>
			</div>
			
			<div class="donor-info">
				<!--- Placeholder for text spans which will fade in --->
			</div>
		`;

		// Get gene information div element to append text in
		let donor_info_box = donor_info_container.querySelector(".donor-info");

		fetchDonorInfo(gene_info["EntrezGeneID"], donor_plot_container)
			.then(() => {
				// Insert empty div to signal the end of the stream (event trigger)
				let endingDiv = document.createElement("div")

				endingDiv.style.height = "0px";
				endingDiv.className = "donor-ending-div";

				donor_info_box.appendChild(endingDiv);
				console.log("finalized")
		});
	}
}

export async function createDonorSection() {
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
	donor_container.appendChild(donor_info_container);
	donor_container.appendChild(donor_plot_container);
	donor_section.appendChild(donor_container);

	// Get gene ID from route
	const pathTokens = window.location.pathname.split("/");
	const gene_id = pathTokens[pathTokens.indexOf("gene") + 1];

	// Fetch donor information from Flask backend and populate containers
	const gene_info = await fetch(`/gene/${gene_id}/all`)
									.then(response => response.json());

	console.log(gene_info);

	showDonorInfo(gene_info, donor_plot_container, donor_info_container);
}