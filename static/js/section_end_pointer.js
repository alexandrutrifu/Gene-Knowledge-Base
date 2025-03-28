import { createDonorSection } from "./donor_section.js"
import { insertScrollDownContainer } from "./scroll_down_containers.js"

document.addEventListener("DOMContentLoaded", function () {
	const plot_section = document.querySelector('.plot-section');
	const section_container = plot_section.querySelector('.section-container');
	const gene_info_container = section_container.querySelector('#gene-info-box');

	// Keep track of arrow insertion
	let arrowInserted = false;

	const observer = new MutationObserver((mutations, observer) => {
		for (const mutation of mutations) {
			if (mutation.type === 'childList') {
				const ending_div = gene_info_container.querySelector('.ending-div');

				if (ending_div && !arrowInserted) {
					// If the text generation has ended, insert scroll container & arrow
					insertScrollDownContainer(gene_info_container)

					arrowInserted = true;

					// Start generating the next section
					createDonorSection();
				} else if (!ending_div && arrowInserted) {
					arrowInserted = false;
				}
			}
		}
	});

	observer.observe(gene_info_container, {
		childList: true,
		subtree: true
	});
})