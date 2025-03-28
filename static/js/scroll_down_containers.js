import { animateArrow } from "./arrow_bounce.js";

export function insertScrollDownContainer(gene_info_container) {
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