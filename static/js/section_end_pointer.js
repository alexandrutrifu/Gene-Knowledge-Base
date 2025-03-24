import { animateArrow } from "./arrow_bounce.js";
import { createDonorSection } from "./donor_section.js"

function insertScrollDownContainer(gene_info_container) {
	const scroll_down_container = document.createElement("div");

	scroll_down_container.className = "scroll-down-container";

	// Add fade-in & animation loop
	scroll_down_container.classList.add("fade-in");

	// Add arrow icon and text
	scroll_down_container.innerHTML = `
		<div class="scroll-down-hint-container">
			<p>Scroll for details</p>
		</div>
		<div class="down-arrow-container">
			<img src="/static/images/down-arrow-icon.svg"
			alt="Arrow SVG" class="down-arrow-icon">
		</div>
	`;

	gene_info_container.appendChild(scroll_down_container);

	// Animate arrow
	const arrow = scroll_down_container.querySelector(".down-arrow-container");

	animateArrow(arrow);
}

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

					// TODO: remove the following sections from DOM
				}
			}
		}
	});

	observer.observe(gene_info_container, {
		childList: true,
		subtree: true
	});
})