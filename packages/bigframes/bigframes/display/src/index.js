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

import React, { useState, useEffect, useRef } from "../react.js";
import ReactDOM from "../react-dom.js";

const e = React.createElement;

function TableWidget({ model }) {
  const [page, setPage] = useState(model.get("page"));
  const [pageSize, setPageSize] = useState(model.get("page_size"));
  const [maxColumns, setMaxColumns] = useState(model.get("max_columns"));
  const [tableHtml, setTableHtml] = useState(model.get("table_html"));
  const [rowCount, setRowCount] = useState(model.get("row_count"));
  const [errorMessage, setErrorMessage] = useState(model.get("error_message"));
  const [sortContext, setSortContext] = useState(model.get("sort_context") || []);
  const [orderableColumns, setOrderableColumns] = useState(model.get("orderable_columns") || []);
  const [deferredMode, setDeferredMode] = useState(model.get("deferred_mode"));
  const [executionState, setExecutionState] = useState(model.get("execution_state") || "idle");

  const tableContainerRef = useRef(null);

  useEffect(() => {
    const handleChange = () => {
      setPage(model.get("page"));
      setPageSize(model.get("page_size"));
      setMaxColumns(model.get("max_columns"));
      setTableHtml(model.get("table_html"));
      setRowCount(model.get("row_count"));
      setErrorMessage(model.get("error_message"));
      setSortContext(model.get("sort_context") || []);
      setOrderableColumns(model.get("orderable_columns") || []);
      setDeferredMode(model.get("deferred_mode"));
      setExecutionState(model.get("execution_state") || "idle");
    };

    model.on("change", handleChange);
    return () => model.off("change", handleChange);
  }, [model]);

  // Post-processing the HTML table to attach sort handlers (Hybrid Approach)
  useEffect(() => {
    const tableContainer = tableContainerRef.current;
    if (!tableContainer) return;

    const headers = tableContainer.querySelectorAll("th");
    headers.forEach((header) => {
      const headerDiv = header.querySelector("div");
      if (!headerDiv) return;

      const columnName = headerDiv.textContent.trim();

      if (columnName && orderableColumns.includes(columnName)) {
        header.style.cursor = "pointer";

        const indicatorSpan = document.createElement("span");
        indicatorSpan.classList.add("sort-indicator");
        indicatorSpan.style.paddingLeft = "5px";

        const sortIndex = sortContext.findIndex((item) => item.column === columnName);
        let indicator = "●";

        if (sortIndex !== -1) {
          const isAscending = sortContext[sortIndex].ascending;
          indicator = isAscending ? "▲" : "▼";
          indicatorSpan.style.visibility = "visible";
        } else {
          indicatorSpan.style.visibility = "hidden";
        }
        indicatorSpan.textContent = indicator;

        const existingIndicator = headerDiv.querySelector(".sort-indicator");
        if (existingIndicator) {
          headerDiv.removeChild(existingIndicator);
        }
        headerDiv.appendChild(indicatorSpan);

        header.addEventListener("mouseover", () => {
          if (sortContext.findIndex((item) => item.column === columnName) === -1) {
            indicatorSpan.style.visibility = "visible";
          }
        });
        header.addEventListener("mouseout", () => {
          if (sortContext.findIndex((item) => item.column === columnName) === -1) {
            indicatorSpan.style.visibility = "hidden";
          }
        });

        header.addEventListener("click", (event) => {
          const currentSortIndex = sortContext.findIndex((item) => item.column === columnName);
          let newContext = [...sortContext];

          if (event.shiftKey) {
            if (currentSortIndex !== -1) {
              if (newContext[currentSortIndex].ascending) {
                newContext[currentSortIndex] = { ...newContext[currentSortIndex], ascending: false };
              } else {
                newContext.splice(currentSortIndex, 1);
              }
            } else {
              newContext.push({ column: columnName, ascending: true });
            }
          } else {
            if (currentSortIndex !== -1 && newContext.length === 1) {
              if (newContext[currentSortIndex].ascending) {
                newContext[currentSortIndex] = { ...newContext[currentSortIndex], ascending: false };
              } else {
                newContext = [];
              }
            } else {
              newContext = [{ column: columnName, ascending: true }];
            }
          }

          model.set("sort_context", newContext);
          model.save_changes();
        });
      }
    });
  }, [tableHtml, sortContext, orderableColumns, model]);

  const handlePageChange = (direction) => {
    model.set("page", page + direction);
    model.save_changes();
  };

  const handlePageSizeChange = (e) => {
    const newSize = Number(e.target.value);
    model.set("page_size", newSize);
    model.set("page", 0);
    model.save_changes();
  };

  const handleMaxColumnsChange = (e) => {
    const newVal = Number(e.target.value);
    model.set("max_columns", newVal);
    model.save_changes();
  };

  const pageSizes = [10, 25, 50, 100];
  const maxColumnOptions = [5, 10, 15, 20, 0];

  const totalPages = rowCount ? Math.ceil(rowCount / pageSize) : 1;

  if (deferredMode && executionState === "idle") {
    return e("div", { className: "bigframes-widget" },
      e("div", { className: "deferred-container", style: { padding: "20px", textAlign: "center" } },
        e("button", {
          className: "execute-button",
          onClick: () => {
            model.set("execution_state", "executing");
            model.save_changes();
          }
        }, "Execute Query")
      )
    );
  }

  if (deferredMode && executionState === "executing") {
    return e("div", { className: "bigframes-widget" },
      e("div", { className: "loading-container", style: { padding: "20px", textAlign: "center" } }, "Executing query...")
    );
  }

  return e("div", { className: "bigframes-widget" },
    errorMessage && e("div", { className: "bigframes-error-message" }, errorMessage),
    e("div", {
      className: "table-container",
      ref: tableContainerRef,
      dangerouslySetInnerHTML: { __html: tableHtml }
    }),
    e("footer", { className: "footer" },
      e("span", { className: "row-count" },
        rowCount === null ? "Total rows unknown" : `${rowCount.toLocaleString()} total rows`
      ),
      e("div", { className: "pagination" },
        e("button", { onClick: () => handlePageChange(-1), disabled: page === 0 }, "<"),
        e("span", { className: "page-indicator" },
          rowCount === null ? `Page ${(page + 1).toLocaleString()} of many` : `Page ${(page + 1).toLocaleString()} of ${totalPages.toLocaleString()}`
        ),
        e("button", { onClick: () => handlePageChange(1), disabled: rowCount !== null && page >= totalPages - 1 }, ">")
      ),
      e("div", { className: "settings" },
        e("div", { className: "max-columns" },
          e("label", null, "Max columns:"),
          e("select", { value: maxColumns || 0, onChange: handleMaxColumnsChange },
            maxColumnOptions.map((cols) =>
              e("option", { key: cols, value: cols }, cols === 0 ? "All" : cols)
            )
          )
        ),
        e("div", { className: "page-size" },
          e("label", null, "Page size:"),
          e("select", { value: pageSize, onChange: handlePageSizeChange },
            pageSizes.map((size) =>
              e("option", { key: size, value: size }, size)
            )
          )
        )
      )
    )
  );
}

export default {
  render({ model, el }) {
    const root = ReactDOM.createRoot(el);
    root.render(e(TableWidget, { model: model }));
  }
};
