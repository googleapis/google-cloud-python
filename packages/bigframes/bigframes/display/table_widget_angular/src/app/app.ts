/*
 * Copyright 2026 Google LLC
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

import { Component, ElementRef, ViewChild, computed, effect, inject, signal } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { WidgetStateService } from './widget-state.service';

@Component({
  selector: '[app-root]',
  standalone: true,
  imports: [],
  providers: [WidgetStateService],
  template: `
    <div class="bigframes-widget" [class.bigframes-dark-mode]="isDarkMode()">
      @if (errorMessage()) {
        <div class="bigframes-error-message">{{ errorMessage() }}</div>
      }

      @if (isDeferredMode()) {
        <div class="deferred-container">
          <div class="deferred-card">
            <p class="deferred-estimate">{{ dryRunInfo() }}</p>
            <button class="run-query-button"
                    [disabled]="isLoading()"
                    (click)="handleRunQuery()">
              @if (isLoading()) {
                <span class="spinner"></span> Run Query
              } @else {
                Run Query
              }
            </button>
          </div>
        </div>
      } @else {
        <div #tableContainer
             class="table-container"
             [innerHTML]="sanitizedHtml()"
             (click)="handleTableClick($event)">
        </div>

        <footer class="footer">
          <span class="row-count">{{ rowCountText() }}</span>

          <div class="pagination">
            <button [disabled]="prevPageDisabled()" (click)="handlePageChange(-1)">&lt;</button>
            <span class="page-indicator">{{ pageIndicatorText() }}</span>
            <button [disabled]="nextPageDisabled()" (click)="handlePageChange(1)">&gt;</button>
          </div>

          <div class="settings">
            <div class="max-columns">
              <label for="max-cols-select">Max columns:</label>
              <select id="max-cols-select" [value]="maxColumns()" (change)="handleMaxColumnsChange($event)">
                @for (cols of maxColumnOptions; track cols) {
                  <option [value]="cols">{{ cols === 0 ? 'All' : cols }}</option>
                }
              </select>
            </div>

            <div class="page-size">
              <label for="page-size-select">Page size:</label>
              <select id="page-size-select" [value]="pageSize()" (change)="handlePageSizeChange($event)">
                @for (size of pageSizeOptions; track size) {
                  <option [value]="size">{{ size }}</option>
                }
              </select>
            </div>
          </div>
        </footer>
      }
    </div>
  `,
  styles: [`
    /* Increase specificity to override framework styles without !important */
    .bigframes-widget.bigframes-widget {
      /* Default Light Mode Variables */
      --bf-bg: white;
      --bf-border-color: #ccc;
      --bf-error-bg: #fbe;
      --bf-error-border: red;
      --bf-error-fg: black;
      --bf-fg: black;
      --bf-header-bg: #f5f5f5;
      --bf-null-fg: gray;
      --bf-row-even-bg: #f5f5f5;
      --bf-row-odd-bg: white;

      background-color: var(--bf-bg);
      box-sizing: border-box;
      color: var(--bf-fg);
      display: flex;
      flex-direction: column;
      font-family:
        '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', sans-serif;
      margin: 0;
      padding: 0;
      width: 100%;
    }

    .bigframes-widget * {
      box-sizing: border-box;
    }

    /* Dark Mode Overrides */
    @media (prefers-color-scheme: dark) {
      .bigframes-widget.bigframes-widget {
        --bf-bg: var(--vscode-editor-background, #202124);
        --bf-border-color: #444;
        --bf-error-bg: #511;
        --bf-error-border: #f88;
        --bf-error-fg: #fcc;
        --bf-fg: white;
        --bf-header-bg: var(--vscode-editor-background, black);
        --bf-null-fg: #aaa;
        --bf-row-even-bg: #202124;
        --bf-row-odd-bg: #383838;
      }
    }

    .bigframes-widget.bigframes-dark-mode.bigframes-dark-mode {
      --bf-bg: var(--vscode-editor-background, #202124);
      --bf-border-color: #444;
      --bf-error-bg: #511;
      --bf-error-border: #f88;
      --bf-error-fg: #fcc;
      --bf-fg: white;
      --bf-header-bg: var(--vscode-editor-background, black);
      --bf-null-fg: #aaa;
      --bf-row-even-bg: #202124;
      --bf-row-odd-bg: #383838;
    }

    .bigframes-widget .table-container {
      background-color: var(--bf-bg);
      margin: 0;
      overflow: auto;
      padding: 0;
    }

    .bigframes-widget .footer {
      align-items: center;
      background-color: var(--bf-bg);
      color: var(--bf-fg);
      display: flex;
      font-size: 0.8rem;
      justify-content: space-between;
      padding: 8px;
    }

    .bigframes-widget .footer > * {
      flex: 1;
    }

    .bigframes-widget .pagination {
      align-items: center;
      display: flex;
      flex-direction: row;
      gap: 4px;
      justify-content: center;
      padding: 4px;
    }

    .bigframes-widget .page-indicator {
      margin: 0 8px;
    }

    .bigframes-widget .row-count {
      margin: 0 8px;
    }

    .bigframes-widget .settings {
      align-items: center;
      display: flex;
      flex-direction: row;
      gap: 16px;
      justify-content: end;
    }

    .bigframes-widget .page-size,
    .bigframes-widget .max-columns {
      align-items: center;
      display: flex;
      flex-direction: row;
      gap: 4px;
    }

    .bigframes-widget .page-size label,
    .bigframes-widget .max-columns label {
      margin-right: 8px;
    }

    /* Dynamic internal elements styles */
    .bigframes-widget ::ng-deep table.bigframes-widget-table,
    .bigframes-widget ::ng-deep table.dataframe {
      background-color: var(--bf-bg);
      border: 1px solid var(--bf-border-color);
      border-collapse: collapse;
      border-spacing: 0;
      box-shadow: none;
      color: var(--bf-fg);
      margin: 0;
      outline: none;
      text-align: left;
      width: auto;
    }

    .bigframes-widget ::ng-deep tr {
      border: none;
    }

    .bigframes-widget ::ng-deep th {
      background-color: var(--bf-header-bg);
      border: 1px solid var(--bf-border-color);
      color: var(--bf-fg);
      padding: 0;
      position: sticky;
      text-align: left;
      top: 0;
      z-index: 1;
    }

    .bigframes-widget ::ng-deep td {
      border: 1px solid var(--bf-border-color);
      color: var(--bf-fg);
      padding: 0.5em;
    }

    .bigframes-widget ::ng-deep table tbody tr:nth-child(odd),
    .bigframes-widget ::ng-deep table tbody tr:nth-child(odd) td {
      background-color: var(--bf-row-odd-bg);
    }

    .bigframes-widget ::ng-deep table tbody tr:nth-child(even),
    .bigframes-widget ::ng-deep table tbody tr:nth-child(even) td {
      background-color: var(--bf-row-even-bg);
    }

    .bigframes-widget ::ng-deep .bf-header-content {
      box-sizing: border-box;
      height: 100%;
      overflow: auto;
      padding: 0.5em;
      resize: horizontal;
      width: 100%;
    }

    .bigframes-widget ::ng-deep th .sort-indicator {
      padding-left: 4px;
      visibility: hidden;
    }

    .bigframes-widget ::ng-deep th:hover .sort-indicator {
      visibility: visible;
    }

    .bigframes-widget button {
      background-color: transparent;
      border: 1px solid currentColor;
      border-radius: 4px;
      color: inherit;
      cursor: pointer;
      display: inline-block;
      padding: 2px 8px;
      text-align: center;
      text-decoration: none;
      user-select: none;
      vertical-align: middle;
    }

    .bigframes-widget button:disabled {
      opacity: 0.65;
      pointer-events: none;
    }

    .bigframes-widget .bigframes-error-message {
      background-color: var(--bf-error-bg);
      border: 1px solid var(--bf-error-border);
      border-radius: 4px;
      color: var(--bf-error-fg);
      font-size: 14px;
      margin-bottom: 8px;
      padding: 8px;
    }

    .bigframes-widget ::ng-deep .cell-align-right {
      text-align: right;
    }

    .bigframes-widget ::ng-deep .cell-align-left {
      text-align: left;
    }

    .bigframes-widget ::ng-deep .null-value {
      color: var(--bf-null-fg);
    }

    .bigframes-widget ::ng-deep .debug-info {
      border-top: 1px solid var(--bf-border-color);
    }

    .bigframes-widget .deferred-container {
      align-items: center;
      display: flex;
      justify-content: center;
      min-height: 220px;
      padding: 24px;
      width: 100%;
    }

    .bigframes-widget .deferred-card {
      background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.6),
        rgba(255, 255, 255, 0.3)
      );
      border: 1px solid rgba(255, 255, 255, 0.4);
      border-radius: 16px;
      box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
      display: flex;
      flex-direction: column;
      gap: 16px;
      max-width: 500px;
      padding: 32px;
      text-align: center;
      transition: all 0.3s ease-in-out;
    }

    .bigframes-widget.bigframes-dark-mode .deferred-card {
      background: linear-gradient(
        135deg,
        rgba(32, 33, 36, 0.6),
        rgba(32, 33, 36, 0.3)
      );
      border: 1px solid rgba(255, 255, 255, 0.1);
      box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    @media (prefers-color-scheme: dark) {
      .bigframes-widget .deferred-card {
        background: linear-gradient(
          135deg,
          rgba(32, 33, 36, 0.6),
          rgba(32, 33, 36, 0.3)
        );
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
      }
    }

    .bigframes-widget .deferred-title {
      font-size: 1.1rem;
      font-weight: 600;
      margin: 0;
    }

    .bigframes-widget .deferred-estimate {
      color: var(--bf-null-fg);
      font-size: 0.9rem;
      margin: 0;
    }

    .bigframes-widget .run-query-button {
      align-items: center;
      background-color: var(--bf-fg);
      border: 1px solid var(--bf-fg);
      border-radius: 8px;
      color: var(--bf-bg);
      cursor: pointer;
      display: inline-flex;
      font-size: 14px;
      font-weight: 600;
      gap: 8px;
      justify-content: center;
      padding: 10px 20px;
      transition: transform 0.20s ease, opacity 0.20s ease;
    }

    .bigframes-widget .run-query-button:hover {
      opacity: 0.90;
      transform: translateY(-1px);
    }

    .bigframes-widget .run-query-button:active {
      transform: translateY(0);
    }

    .bigframes-widget .run-query-button:disabled {
      cursor: not-allowed;
      opacity: 0.60;
    }

    .bigframes-widget .spinner {
      animation: spin 1s linear infinite;
      border: 2px solid currentColor;
      border-radius: 50%;
      border-top-color: transparent;
      display: inline-block;
      height: 12px;
      width: 12px;
    }

    @keyframes spin {
      to {
        transform: rotate(360deg);
      }
    }
  `]
})
export class App {
  protected readonly state = inject(WidgetStateService);
  private readonly sanitizer = inject(DomSanitizer);

  protected readonly maxColumnOptions = [5, 10, 15, 20, 0];
  protected readonly pageSizeOptions = [10, 25, 50, 100];

  // State signals
  protected readonly errorMessage = this.state.errorMessage;
  protected readonly maxColumns = this.state.maxColumns;
  protected readonly pageSize = this.state.pageSize;
  protected readonly page = this.state.page;
  protected readonly rowCount = this.state.rowCount;
  protected readonly isDeferredMode = this.state.isDeferredMode;
  protected readonly dryRunInfo = this.state.dryRunInfo;
  protected readonly isLoading = signal(false);

  // Computed properties for formatting and display states
  protected readonly sanitizedHtml = computed(() =>
    this.sanitizer.bypassSecurityTrustHtml(this.state.tableHtml())
  );

  protected readonly totalPages = computed(() => {
    const count = this.rowCount();
    const size = this.pageSize();
    return count !== null && size > 0 ? Math.ceil(count / size) : null;
  });

  protected readonly pageIndicatorText = computed(() => {
    const currentPage = this.page();
    const count = this.rowCount();
    const total = this.totalPages();
    const currentStr = (currentPage + 1).toLocaleString();
    const totalStr = (total ?? 1).toLocaleString();
    return `Page ${currentStr} of ${totalStr}`;
  });

  protected readonly rowCountText = computed(() => {
    const count = this.rowCount();
    if (count === null) {
      return 'Total rows unknown';
    }
    if (count === 0) {
      return '0 total rows';
    }
    return `${count.toLocaleString()} total rows`;
  });

  protected readonly prevPageDisabled = computed(() => this.page() === 0);

  protected readonly nextPageDisabled = computed(() => {
    const currentPage = this.page();
    const count = this.rowCount();
    const total = this.totalPages();
    if (count === null) {
      return false;
    }
    if (count === 0) {
      return true;
    }
    return total !== null && currentPage >= total - 1;
  });

  protected readonly isDarkMode = signal(false);
  private themeObserver: MutationObserver | null = null;

  @ViewChild('tableContainer')
  tableContainerRef!: ElementRef<HTMLDivElement>;

  private isHeightInitialized = false;

  constructor() {
    effect(() => {
      // Setup dependencies for reactive effect
      const _html = this.state.tableHtml();
      const _sort = this.state.sortContext();
      const _orderable = this.state.orderableColumns();
      const deferred = this.isDeferredMode();
      if (deferred) {
        this.isHeightInitialized = false;
      }

      // Schedule DOM post-processing once the innerHTML render completes
      setTimeout(() => {
        this.applySortIndicators();
        this.lockInitialHeight();
      }, 0);
    });

    effect(() => {
      if (!this.state.startExecution()) {
        this.isLoading.set(false);
      }
    });

    effect((onCleanup) => {
      const executing = this.state.startExecution();
      if (executing) {
        const intervalId = setInterval(() => {
          if (this.state.startExecution()) {
            const currentPing = this.state.ping();
            this.state.setPing(currentPing + 1);
          } else {
            clearInterval(intervalId);
          }
        }, 500);
        onCleanup(() => {
          clearInterval(intervalId);
        });
      }
    });
  }

  ngOnInit() {
    this.initThemeDetection();
  }

  ngOnDestroy() {
    this.themeObserver?.disconnect();
  }

  protected handleRunQuery() {
    this.isLoading.set(true);
    this.state.setStartExecution(true);
  }

  protected handlePageChange(direction: number) {
    const nextPage = this.page() + direction;
    this.state.setPage(nextPage);
  }

  protected handlePageSizeChange(event: Event) {
    const select = event.target as HTMLSelectElement;
    const newSize = Number(select.value);
    if (newSize) {
      this.state.setPageSize(newSize);
    }
  }

  protected handleMaxColumnsChange(event: Event) {
    const select = event.target as HTMLSelectElement;
    const maxCols = Number(select.value);
    this.state.setMaxColumns(maxCols);
  }

  protected handleTableClick(event: MouseEvent) {
    const target = event.target as HTMLElement;
    const header = target.closest('th');
    if (!header) return;

    const headerDiv = header.querySelector(
      'div.bf-header-content'
    ) as HTMLElement | null;
    if (!headerDiv) return;

    const columnName = this.getColumnName(headerDiv);
    const sortableColumns = this.state.orderableColumns();
    if (!columnName || !sortableColumns.includes(columnName)) return;

    const currentSortContext = [...this.state.sortContext()];
    const sortIndex = currentSortContext.findIndex(
      (item) => item.column === columnName
    );
    let newContext = [...currentSortContext];

    if (event.shiftKey) {
      if (sortIndex !== -1) {
        // Toggle: Asc -> Desc -> Unsorted
        if (newContext[sortIndex].ascending) {
          newContext[sortIndex] = {
            ...newContext[sortIndex],
            ascending: false
          };
        } else {
          newContext.splice(sortIndex, 1);
        }
      } else {
        newContext.push({ column: columnName, ascending: true });
      }
    } else {
      // Single column sort mode
      if (sortIndex !== -1 && newContext.length === 1) {
        // Toggle: Asc -> Desc -> Unsorted
        if (newContext[sortIndex].ascending) {
          newContext[sortIndex] = {
            ...newContext[sortIndex],
            ascending: false
          };
        } else {
          newContext = [];
        }
      } else {
        newContext = [{ column: columnName, ascending: true }];
      }
    }

    this.state.setSortContext(newContext);
  }

  private getColumnName(headerDiv: HTMLElement): string {
    const clone = headerDiv.cloneNode(true) as HTMLElement;
    clone.querySelector('.sort-indicator')?.remove();
    return clone.textContent?.trim() || '';
  }

  private applySortIndicators() {
    const container = this.tableContainerRef?.nativeElement;
    if (!container) return;

    const sortableColumns = this.state.orderableColumns();
    const currentSortContext = this.state.sortContext() || [];

    const getSortIndex = (colName: string) =>
      currentSortContext.findIndex((item) => item.column === colName);

    const headers = container.querySelectorAll('th');
    headers.forEach((header: HTMLElement) => {
      const headerDiv = header.querySelector(
        'div.bf-header-content'
      ) as HTMLElement | null;
      if (!headerDiv) return;

      const columnName = this.getColumnName(headerDiv);
      if (columnName && sortableColumns.includes(columnName)) {

        let indicatorSpan = headerDiv.querySelector(
          '.sort-indicator'
        ) as HTMLElement;
        if (!indicatorSpan) {
          indicatorSpan = document.createElement('span');
          indicatorSpan.classList.add('sort-indicator');
          indicatorSpan.style.paddingLeft = '5px';
          headerDiv.appendChild(indicatorSpan);
        }

        const sortIndex = getSortIndex(columnName);
        if (sortIndex !== -1) {
          const isAscending = currentSortContext[sortIndex].ascending;
          indicatorSpan.textContent = isAscending ? '▲' : '▼';
          indicatorSpan.style.visibility = 'visible';
        } else {
          indicatorSpan.textContent = '●';
          indicatorSpan.style.visibility = 'hidden';
        }
      }
    });
  }

  private lockInitialHeight() {
    if (this.isHeightInitialized) return;
    const container = this.tableContainerRef?.nativeElement;
    if (!container) return;

    const table = container.querySelector('table');
    if (table && (table as HTMLElement).offsetHeight > 0) {
      const currentHeight = container.offsetHeight;
      if (currentHeight > 0) {
        container.style.height = `${currentHeight}px`;
        this.isHeightInitialized = true;
      }
    }
  }

  private initThemeDetection() {
    this.updateTheme();
    const observer = new MutationObserver(() => this.updateTheme());
    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ['class', 'data-theme', 'data-vscode-theme-kind'],
    });
    this.themeObserver = observer;
  }

  private updateTheme() {
    const body = document.body;
    const isDark =
      body.classList.contains('vscode-dark') ||
      body.classList.contains('theme-dark') ||
      body.dataset['theme'] === 'dark' ||
      body.getAttribute('data-vscode-theme-kind') === 'vscode-dark';
    this.isDarkMode.set(isDark);
  }
}
