import { animateArrow } from "./arrow-bounce.js";

document.addEventListener("DOMContentLoaded", function () {
	const plot_section = document.querySelector('.plot-section');
	const gene_info_container = plot_section.querySelector('#gene-info-box');

	// Keep track of arrow insertion
	let arrowInserted = false;

	const observer = new MutationObserver((mutations, observer) => {
		for (const mutation of mutations) {
			if (mutation.type === 'childList') {
				const ending_div = gene_info_container.querySelector('.ending-div');

				if (ending_div && !arrowInserted) {
					// Text generation has ended => insert the animated arrow
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

					// observer.disconnect();
					arrowInserted = true;

					gene_info_container.appendChild(scroll_down_container);

					// Animate arrow
					const arrow = scroll_down_container.querySelector(".down-arrow-container");

					animateArrow(arrow);
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