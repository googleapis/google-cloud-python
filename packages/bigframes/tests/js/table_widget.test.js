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

import { jest } from "@jest/globals";
import { JSDOM } from "jsdom";

describe("TableWidget", () => {
	let model;
	let el;
	let render;

	beforeEach(async () => {
		jest.resetModules();
		document.body.innerHTML = "<div></div>";
		el = document.body.querySelector("div");

		const tableWidget = (
			await import("../../bigframes/display/table_widget.js")
		).default;
		render = tableWidget.render;

		model = {
			get: jest.fn(),
			set: jest.fn(),
			save_changes: jest.fn(),
			on: jest.fn(),
		};
	});

	it("should have a render function", () => {
		expect(render).toBeDefined();
	});

	describe("render", () => {
		it("should create the basic structure", () => {
			// Mock the initial state
			model.get.mockImplementation((property) => {
				if (property === "table_html") {
					return "";
				}
				if (property === "row_count") {
					return 100;
				}
				if (property === "error_message") {
					return null;
				}
				if (property === "page_size") {
					return 10;
				}
				if (property === "page") {
					return 0;
				}
				return null;
			});

			render({ model, el });

			expect(el.classList.contains("bigframes-widget")).toBe(true);
			expect(el.querySelector(".error-message")).not.toBeNull();
			expect(el.querySelector("div")).not.toBeNull();
			expect(el.querySelector("div:nth-child(3)")).not.toBeNull();
		});

		it("should sort when a sortable column is clicked", () => {
			// Mock the initial state
			model.get.mockImplementation((property) => {
				if (property === "table_html") {
					return "<table><thead><tr><th><div>col1</div></th></tr></thead></table>";
				}
				if (property === "orderable_columns") {
					return ["col1"];
				}
				if (property === "sort_column") {
					return "";
				}
				return null;
			});

			render({ model, el });

			// Manually trigger the table_html change handler
			const tableHtmlChangeHandler = model.on.mock.calls.find(
				(call) => call[0] === "change:table_html",
			)[1];
			tableHtmlChangeHandler();

			const header = el.querySelector("th");
			header.click();

			expect(model.set).toHaveBeenCalledWith("sort_column", "col1");
			expect(model.set).toHaveBeenCalledWith("sort_ascending", true);
			expect(model.save_changes).toHaveBeenCalled();
		});

		it("should reverse sort direction when a sorted column is clicked", () => {
			// Mock the initial state
			model.get.mockImplementation((property) => {
				if (property === "table_html") {
					return "<table><thead><tr><th><div>col1</div></th></tr></thead></table>";
				}
				if (property === "orderable_columns") {
					return ["col1"];
				}
				if (property === "sort_column") {
					return "col1";
				}
				if (property === "sort_ascending") {
					return true;
				}
				return null;
			});

			render({ model, el });

			// Manually trigger the table_html change handler
			const tableHtmlChangeHandler = model.on.mock.calls.find(
				(call) => call[0] === "change:table_html",
			)[1];
			tableHtmlChangeHandler();

			const header = el.querySelector("th");
			header.click();

			expect(model.set).toHaveBeenCalledWith("sort_ascending", false);
			expect(model.save_changes).toHaveBeenCalled();
		});

		it("should clear sort when a descending sorted column is clicked", () => {
			// Mock the initial state
			model.get.mockImplementation((property) => {
				if (property === "table_html") {
					return "<table><thead><tr><th><div>col1</div></th></tr></thead></table>";
				}
				if (property === "orderable_columns") {
					return ["col1"];
				}
				if (property === "sort_column") {
					return "col1";
				}
				if (property === "sort_ascending") {
					return false;
				}
				return null;
			});

			render({ model, el });

			// Manually trigger the table_html change handler
			const tableHtmlChangeHandler = model.on.mock.calls.find(
				(call) => call[0] === "change:table_html",
			)[1];
			tableHtmlChangeHandler();

			const header = el.querySelector("th");
			header.click();

			expect(model.set).toHaveBeenCalledWith("sort_column", "");
			expect(model.set).toHaveBeenCalledWith("sort_ascending", true);
			expect(model.save_changes).toHaveBeenCalled();
		});

		it("should display the correct sort indicator", () => {
			// Mock the initial state
			model.get.mockImplementation((property) => {
				if (property === "table_html") {
					return "<table><thead><tr><th><div>col1</div></th><th><div>col2</div></th></tr></thead></table>";
				}
				if (property === "orderable_columns") {
					return ["col1", "col2"];
				}
				if (property === "sort_column") {
					return "col1";
				}
				if (property === "sort_ascending") {
					return true;
				}
				return null;
			});

			render({ model, el });

			// Manually trigger the table_html change handler
			const tableHtmlChangeHandler = model.on.mock.calls.find(
				(call) => call[0] === "change:table_html",
			)[1];
			tableHtmlChangeHandler();

			const headers = el.querySelectorAll("th");
			const indicator1 = headers[0].querySelector(".sort-indicator");
			const indicator2 = headers[1].querySelector(".sort-indicator");

			expect(indicator1.textContent).toBe("▲");
			expect(indicator2.textContent).toBe("●");
		});
	});
});
