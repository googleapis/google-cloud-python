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
	TABLE_HTML: "table_html",
	ROW_COUNT: "row_count",
	PAGE_SIZE: "page_size",
	PAGE: "page",
};

const Event = {
	CHANGE_TABLE_HTML: `change:${ModelProperty.TABLE_HTML}`,
	CLICK: "click",
};

/**
 * Renders a paginated table and its controls into a given element.
 * @param {{
 * model: !Backbone.Model,
 * el: !HTMLElement
 * }} options
 */
function render({ model, el }) {
	const container = document.createElement("div");
	container.innerHTML = model.get(ModelProperty.TABLE_HTML);

	const buttonContainer = document.createElement("div");
	const prevPage = document.createElement("button");
	const label = document.createElement("span");
	const nextPage = document.createElement("button");

	prevPage.type = "button";
	nextPage.type = "button";
	prevPage.textContent = "Prev";
	nextPage.textContent = "Next";

	/** Updates the button states and page label based on the model. */
	function updateButtonStates() {
		const totalPages = Math.ceil(
			model.get(ModelProperty.ROW_COUNT) / model.get(ModelProperty.PAGE_SIZE),
		);
		const currentPage = model.get(ModelProperty.PAGE);

		label.textContent = `Page ${currentPage + 1} of ${totalPages}`;
		prevPage.disabled = currentPage === 0;
		nextPage.disabled = currentPage >= totalPages - 1;
	}

	/**
	 * Updates the page in the model.
	 * @param {number} direction -1 for previous, 1 for next.
	 */
	function handlePageChange(direction) {
		const currentPage = model.get(ModelProperty.PAGE);
		const newPage = Math.max(0, currentPage + direction);
		if (newPage !== currentPage) {
			model.set(ModelProperty.PAGE, newPage);
			model.save_changes();
		}
	}

	prevPage.addEventListener(Event.CLICK, () => handlePageChange(-1));
	nextPage.addEventListener(Event.CLICK, () => handlePageChange(1));

	model.on(Event.CHANGE_TABLE_HTML, () => {
		// Note: Using innerHTML can be a security risk if the content is
		// user-generated. Ensure 'table_html' is properly sanitized.
		container.innerHTML = model.get(ModelProperty.TABLE_HTML);
		updateButtonStates();
	});

	// Initial setup
	updateButtonStates();

	buttonContainer.appendChild(prevPage);
	buttonContainer.appendChild(label);
	buttonContainer.appendChild(nextPage);
	el.appendChild(container);
	el.appendChild(buttonContainer);
}

export default { render };
