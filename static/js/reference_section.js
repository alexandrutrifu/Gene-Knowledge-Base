function insertReferences(references, parent_section) {
	// First two references go on the first row
	const first_row_ref1 = parent_section.querySelector(".first-row-ref1");
	const first_row_ref2 = parent_section.querySelector(".first-row-ref2");

	console.log(references);
	console.log("references[1]:", references[1]);
	console.log("conclusion:", references[1]?.conclusion);

	first_row_ref1.innerHTML = `
		<h2>
			<a href="${references[1].ref_url}" target="_blank"
               style="text-decoration: none; color: inherit">${references[1].conclusion}</a>
        </h2>
	`;

	first_row_ref2.innerHTML = `
		<h2>
			<a href="${references[2].ref_url}" target="_blank"
               style="text-decoration: none; color: inherit">${references[2].conclusion}</a>
        </h2>
	`;

	// Next three references go on the second row
	const second_row_ref1 = parent_section.querySelector(".second-row-ref1");
	const second_row_ref2 = parent_section.querySelector(".second-row-ref2");
	const main_ref = parent_section.querySelector(".main-ref");

	second_row_ref1.innerHTML = `
		<h2>
			<a href="${references[3].ref_url}" target="_blank"
               style="text-decoration: none; color: inherit">${references[3].conclusion}</a>
        </h2>
	`;

	main_ref.innerHTML = `
		<h2>
			<a href="${references[0].ref_url}" target="_blank"
               style="text-decoration: none; color: inherit">${references[0].conclusion}</a>
        </h2>
	`;

	second_row_ref2.innerHTML = `
		<h2>
			<a href="${references[4].ref_url}" target="_blank"
               style="text-decoration: none; color: inherit">${references[4].conclusion}</a>
        </h2>
	`;

	// Final references go on the last row
	const last_row_ref1 = parent_section.querySelector(".last-row-ref1");
	const last_row_ref2 = parent_section.querySelector(".last-row-ref2");

	last_row_ref1.innerHTML = `
		<h2>
			<a href="${references[5].ref_url}" target="_blank"
               style="text-decoration: none; color: inherit">${references[5].conclusion}</a>
        </h2>
	`;

	last_row_ref2.innerHTML = `
		<h2>
			<a href="${references[6].ref_url}" target="_blank"
               style="text-decoration: none; color: inherit">${references[6].conclusion}</a>
        </h2>
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
}