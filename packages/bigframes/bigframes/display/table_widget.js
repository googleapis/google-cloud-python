/**
 * Copyright 2025 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

const ModelProperty = {
	PAGE: "page",
	PAGE_SIZE: "page_size",
	ROW_COUNT: "row_count",
	TABLE_HTML: "table_html",
};

const Event = {
	CHANGE: "change",
	CHANGE_TABLE_HTML: `change:${ModelProperty.TABLE_HTML}`,
	CLICK: "click",
};

/**
 * Renders the interactive table widget.
 * @param {{
 * model: any,
 * el: HTMLElement
 * }} options
 */
function render({ model, el }) {
	// Main container with a unique class for CSS scoping
	el.classList.add("bigframes-widget");

	// Structure
	const tableContainer = document.createElement("div");
	const footer = document.createElement("div");

	// Footer: Total rows label
	const rowCountLabel = document.createElement("div");

	// Footer: Pagination controls
	const paginationContainer = document.createElement("div");
	const prevPage = document.createElement("button");
	const paginationLabel = document.createElement("span");
	const nextPage = document.createElement("button");

	// Footer: Page size controls
	const pageSizeContainer = document.createElement("div");
	const pageSizeLabel = document.createElement("label");
	const pageSizeSelect = document.createElement("select");

	// Add CSS classes
	tableContainer.classList.add("table-container");
	footer.classList.add("footer");
	paginationContainer.classList.add("pagination");
	pageSizeContainer.classList.add("page-size");

	// Configure pagination buttons
	prevPage.type = "button";
	nextPage.type = "button";
	prevPage.textContent = "Prev";
	nextPage.textContent = "Next";

	// Configure page size selector
	pageSizeLabel.textContent = "Page Size";
	for (const size of [10, 25, 50, 100]) {
		const option = document.createElement("option");
		option.value = size;
		option.textContent = size;
		if (size === model.get(ModelProperty.PAGE_SIZE)) {
			option.selected = true;
		}
		pageSizeSelect.appendChild(option);
	}

	/** Updates the footer states and page label based on the model. */
	function updateButtonStates() {
		const rowCount = model.get(ModelProperty.ROW_COUNT);
		const pageSize = model.get(ModelProperty.PAGE_SIZE);
		const currentPage = model.get(ModelProperty.PAGE);
		const totalPages = Math.ceil(rowCount / pageSize);

		rowCountLabel.textContent = `${rowCount.toLocaleString()} total rows`;
		paginationLabel.textContent = `Page ${(
			currentPage + 1
		).toLocaleString()} of ${(totalPages || 1).toLocaleString()}`;
		prevPage.disabled = currentPage === 0;
		nextPage.disabled = currentPage >= totalPages - 1;
		pageSizeSelect.value = pageSize;
	}

	/**
	 * Increments or decrements the page in the model.
	 * @param {number} direction - `1` for next, `-1` for previous.
	 */
	function handlePageChange(direction) {
		const current = model.get(ModelProperty.PAGE);
		const next = current + direction;
		model.set(ModelProperty.PAGE, next);
		model.save_changes();
	}

	/**
	 * Handles changes to the page size from the dropdown.
	 * @param {number} size - The new page size.
	 */
	function handlePageSizeChange(size) {
		const currentSize = model.get(ModelProperty.PAGE_SIZE);
		if (size !== currentSize) {
			model.set(ModelProperty.PAGE_SIZE, size);
			model.save_changes();
		}
	}

	/** Updates the HTML in the table container and refreshes button states. */
	function handleTableHTMLChange() {
		// Note: Using innerHTML is safe here because the content is generated
		// by a trusted backend (DataFrame.to_html).
		tableContainer.innerHTML = model.get(ModelProperty.TABLE_HTML);
		updateButtonStates();
	}

	// Add event listeners
	prevPage.addEventListener(Event.CLICK, () => handlePageChange(-1));
	nextPage.addEventListener(Event.CLICK, () => handlePageChange(1));
	pageSizeSelect.addEventListener(Event.CHANGE, (e) => {
		const newSize = Number(e.target.value);
		if (newSize) {
			handlePageSizeChange(newSize);
		}
	});
	model.on(Event.CHANGE_TABLE_HTML, handleTableHTMLChange);

	// Assemble the DOM
	paginationContainer.appendChild(prevPage);
	paginationContainer.appendChild(paginationLabel);
	paginationContainer.appendChild(nextPage);

	pageSizeContainer.appendChild(pageSizeLabel);
	pageSizeContainer.appendChild(pageSizeSelect);

	footer.appendChild(rowCountLabel);
	footer.appendChild(paginationContainer);
	footer.appendChild(pageSizeContainer);

	el.appendChild(tableContainer);
	el.appendChild(footer);

	// Initial render
	handleTableHTMLChange();
}

export default { render };
