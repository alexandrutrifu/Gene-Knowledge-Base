// import {observeReferenceSentinel } from "./observe_reference_section.js";

function insertReferences(references, parent_section) {
	// First two references go on the first row
	const first_row_ref1 = parent_section.querySelector(".first-row-ref1");
	const first_row_ref2 = parent_section.querySelector(".first-row-ref2");

	console.log(references);
	console.log("references[1]:", references[1]);
	console.log("conclusion:", references[1]?.conclusion);

	first_row_ref1.innerHTML = `
		<h2>${references[0].conclusion}</h2>
	`;

	first_row_ref2.innerHTML = `
		<h2>${references[1].conclusion}</h2>
	`;

	// Next three references go on the second row

	// Final references go on the last row
	const last_row_ref1 = parent_section.querySelector(".last-row-ref1");
	const last_row_ref2 = parent_section.querySelector(".last-row-ref2");

	last_row_ref1.innerHTML = `
		<h2>${references[5].conclusion}</h2>
	`;

	last_row_ref2.innerHTML = `
		<h2>${references[6].conclusion}</h2>
	`;
}

export async function createReferenceSection(gene_info) {
	// Get reference section elements
	const reference_section = document.querySelector(".reference-section");
	const reference_container = reference_section.querySelector(".reference-container");

	// Reset visibility attributes
	reference_section.classList.add("active");
	reference_section.style.height = "auto";
	reference_container.style.height = "auto";

	// Get gene ID
	const gene_id = gene_info["EntrezGeneID"];

	// Fetch data from Flask backend
	fetch(`/gene/${gene_id}/ref`)
		.then(response => response.json())
		.then((references) => {
			insertReferences(references, reference_section);
		})

	// observeReferenceSentinel();
	//
	// // Get gene ID from route
	// const pathTokens = window.location.pathname.split("/");
	// const gene_id = pathTokens[pathTokens.indexOf("gene") + 1];
	//
	// // Fetch donor information from Flask backend and populate containers
	// const gene_info = await fetch(`/gene/${gene_id}/all`)
	// 								.then(response => response.json());
	//
	// console.log(gene_info);
	//
	// showReferenceInfo(gene_info, );
}