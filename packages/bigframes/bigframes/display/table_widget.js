/*
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
	ERROR_MESSAGE: "error_message",
	ORDERABLE_COLUMNS: "orderable_columns",
	PAGE: "page",
	PAGE_SIZE: "page_size",
	ROW_COUNT: "row_count",
	SORT_CONTEXT: "sort_context",
	TABLE_HTML: "table_html",
};

const Event = {
	CHANGE: "change",
	CHANGE_TABLE_HTML: "change:table_html",
	CLICK: "click",
};

/**
 * Renders the interactive table widget.
 * @param {{ model: any, el: !HTMLElement }} props - The widget properties.
 */
function render({ model, el }) {
	// Main container with a unique class for CSS scoping
	el.classList.add("bigframes-widget");

	// Add error message container at the top
	const errorContainer = document.createElement("div");
	errorContainer.classList.add("error-message");

	const tableContainer = document.createElement("div");
	tableContainer.classList.add("table-container");
	const footer = document.createElement("footer");
	footer.classList.add("footer");

	// Pagination controls
	const paginationContainer = document.createElement("div");
	paginationContainer.classList.add("pagination");
	const prevPage = document.createElement("button");
	const pageIndicator = document.createElement("span");
	pageIndicator.classList.add("page-indicator");
	const nextPage = document.createElement("button");
	const rowCountLabel = document.createElement("span");
	rowCountLabel.classList.add("row-count");

	// Page size controls
	const pageSizeContainer = document.createElement("div");
	pageSizeContainer.classList.add("page-size");
	const pageSizeLabel = document.createElement("label");
	const pageSizeInput = document.createElement("select");

	prevPage.textContent = "<";
	nextPage.textContent = ">";
	pageSizeLabel.textContent = "Page size:";

	// Page size options
	const pageSizes = [10, 25, 50, 100];
	for (const size of pageSizes) {
		const option = document.createElement("option");
		option.value = size;
		option.textContent = size;
		if (size === model.get(ModelProperty.PAGE_SIZE)) {
			option.selected = true;
		}
		pageSizeInput.appendChild(option);
	}

	/** Updates the footer states and page label based on the model. */
	function updateButtonStates() {
		const currentPage = model.get(ModelProperty.PAGE);
		const pageSize = model.get(ModelProperty.PAGE_SIZE);
		const rowCount = model.get(ModelProperty.ROW_COUNT);

		if (rowCount === null) {
			// Unknown total rows
			rowCountLabel.textContent = "Total rows unknown";
			pageIndicator.textContent = `Page ${(
				currentPage + 1
			).toLocaleString()} of many`;
			prevPage.disabled = currentPage === 0;
			nextPage.disabled = false; // Allow navigation until we hit the end
		} else if (rowCount === 0) {
			// Empty dataset
			rowCountLabel.textContent = "0 total rows";
			pageIndicator.textContent = "Page 1 of 1";
			prevPage.disabled = true;
			nextPage.disabled = true;
		} else {
			// Known total rows
			const totalPages = Math.ceil(rowCount / pageSize);
			rowCountLabel.textContent = `${rowCount.toLocaleString()} total rows`;
			pageIndicator.textContent = `Page ${(
				currentPage + 1
			).toLocaleString()} of ${totalPages.toLocaleString()}`;
			prevPage.disabled = currentPage === 0;
			nextPage.disabled = currentPage >= totalPages - 1;
		}
		pageSizeInput.value = pageSize;
	}

	/**
	 * Handles page navigation.
	 * @param {number} direction - The direction to navigate (-1 for previous, 1 for next).
	 */
	function handlePageChange(direction) {
		const currentPage = model.get(ModelProperty.PAGE);
		model.set(ModelProperty.PAGE, currentPage + direction);
		model.save_changes();
	}

	/**
	 * Handles page size changes.
	 * @param {number} newSize - The new page size.
	 */
	function handlePageSizeChange(newSize) {
		model.set(ModelProperty.PAGE_SIZE, newSize);
		model.set(ModelProperty.PAGE, 0); // Reset to first page
		model.save_changes();
	}

	/** Updates the HTML in the table container and refreshes button states. */
	function handleTableHTMLChange() {
		// Note: Using innerHTML is safe here because the content is generated
		// by a trusted backend (DataFrame.to_html).
		tableContainer.innerHTML = model.get(ModelProperty.TABLE_HTML);

		// Get sortable columns from backend
		const sortableColumns = model.get(ModelProperty.ORDERABLE_COLUMNS);
		const currentSortContext = model.get(ModelProperty.SORT_CONTEXT) || [];

		const getSortIndex = (colName) =>
			currentSortContext.findIndex((item) => item.column === colName);

		// Add click handlers to column headers for sorting
		const headers = tableContainer.querySelectorAll("th");
		headers.forEach((header) => {
			const headerDiv = header.querySelector("div");
			const columnName = headerDiv.textContent.trim();

			// Only add sorting UI for sortable columns
			if (columnName && sortableColumns.includes(columnName)) {
				header.style.cursor = "pointer";

				// Create a span for the indicator
				const indicatorSpan = document.createElement("span");
				indicatorSpan.classList.add("sort-indicator");
				indicatorSpan.style.paddingLeft = "5px";

				// Determine sort indicator and initial visibility
				let indicator = "●"; // Default: unsorted (dot)
				const sortIndex = getSortIndex(columnName);

				if (sortIndex !== -1) {
					const isAscending = currentSortContext[sortIndex].ascending;
					indicator = isAscending ? "▲" : "▼";
					indicatorSpan.style.visibility = "visible"; // Sorted arrows always visible
				} else {
					indicatorSpan.style.visibility = "hidden"; // Unsorted dot hidden by default
				}
				indicatorSpan.textContent = indicator;

				// Add indicator to the header, replacing the old one if it exists
				const existingIndicator = headerDiv.querySelector(".sort-indicator");
				if (existingIndicator) {
					headerDiv.removeChild(existingIndicator);
				}
				headerDiv.appendChild(indicatorSpan);

				// Add hover effects for unsorted columns only
				header.addEventListener("mouseover", () => {
					if (getSortIndex(columnName) === -1) {
						indicatorSpan.style.visibility = "visible";
					}
				});
				header.addEventListener("mouseout", () => {
					if (getSortIndex(columnName) === -1) {
						indicatorSpan.style.visibility = "hidden";
					}
				});

				// Add click handler for three-state toggle
				header.addEventListener(Event.CLICK, (event) => {
					const sortIndex = getSortIndex(columnName);
					let newContext = [...currentSortContext];

					if (event.shiftKey) {
						if (sortIndex !== -1) {
							// Already sorted. Toggle or Remove.
							if (newContext[sortIndex].ascending) {
								// Asc -> Desc
								// Clone object to avoid mutation issues
								newContext[sortIndex] = {
									...newContext[sortIndex],
									ascending: false,
								};
							} else {
								// Desc -> Remove
								newContext.splice(sortIndex, 1);
							}
						} else {
							// Not sorted -> Append Asc
							newContext.push({ column: columnName, ascending: true });
						}
					} else {
						// No shift key. Single column mode.
						if (sortIndex !== -1 && newContext.length === 1) {
							// Already only this column. Toggle or Remove.
							if (newContext[sortIndex].ascending) {
								newContext[sortIndex] = {
									...newContext[sortIndex],
									ascending: false,
								};
							} else {
								newContext = [];
							}
						} else {
							// Start fresh with this column
							newContext = [{ column: columnName, ascending: true }];
						}
					}

					model.set(ModelProperty.SORT_CONTEXT, newContext);
					model.save_changes();
				});
			}
		});

		const table = tableContainer.querySelector("table");
		if (table) {
			const tableBody = table.querySelector("tbody");

			/**
			 * Handles row hover events.
			 * @param {!Event} event - The mouse event.
			 * @param {boolean} isHovering - True to add hover class, false to remove.
			 */
			function handleRowHover(event, isHovering) {
				const cell = event.target.closest("td");
				if (cell) {
					const row = cell.closest("tr");
					const origRowId = row.dataset.origRow;
					if (origRowId) {
						const allCellsInGroup = tableBody.querySelectorAll(
							`tr[data-orig-row="${origRowId}"] td`,
						);
						allCellsInGroup.forEach((c) => {
							c.classList.toggle("row-hover", isHovering);
						});
					}
				}
			}

			if (tableBody) {
				tableBody.addEventListener("mouseover", (event) =>
					handleRowHover(event, true),
				);
				tableBody.addEventListener("mouseout", (event) =>
					handleRowHover(event, false),
				);
			}
		}

		updateButtonStates();
	}

	// Add error message handler
	function handleErrorMessageChange() {
		const errorMsg = model.get(ModelProperty.ERROR_MESSAGE);
		if (errorMsg) {
			errorContainer.textContent = errorMsg;
			errorContainer.style.display = "block";
		} else {
			errorContainer.style.display = "none";
		}
	}

	// Add event listeners
	prevPage.addEventListener(Event.CLICK, () => handlePageChange(-1));
	nextPage.addEventListener(Event.CLICK, () => handlePageChange(1));
	pageSizeInput.addEventListener(Event.CHANGE, (e) => {
		const newSize = Number(e.target.value);
		if (newSize) {
			handlePageSizeChange(newSize);
		}
	});
	model.on(Event.CHANGE_TABLE_HTML, handleTableHTMLChange);
	model.on(`change:${ModelProperty.ROW_COUNT}`, updateButtonStates);
	model.on(`change:${ModelProperty.ERROR_MESSAGE}`, handleErrorMessageChange);
	model.on(`change:_initial_load_complete`, (val) => {
		if (val) {
			updateButtonStates();
		}
	});
	model.on(`change:${ModelProperty.PAGE}`, updateButtonStates);

	// Assemble the DOM
	paginationContainer.appendChild(prevPage);
	paginationContainer.appendChild(pageIndicator);
	paginationContainer.appendChild(nextPage);

	pageSizeContainer.appendChild(pageSizeLabel);
	pageSizeContainer.appendChild(pageSizeInput);

	footer.appendChild(rowCountLabel);
	footer.appendChild(paginationContainer);
	footer.appendChild(pageSizeContainer);

	el.appendChild(errorContainer);
	el.appendChild(tableContainer);
	el.appendChild(footer);

	// Initial render
	handleTableHTMLChange();
	handleErrorMessageChange();
}

export default { render };
