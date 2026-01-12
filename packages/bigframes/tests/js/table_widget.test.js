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

import { jest } from '@jest/globals';

describe('TableWidget', () => {
  let model;
  let el;
  let render;

  beforeEach(async () => {
    jest.resetModules();
    document.body.innerHTML = '<div></div>';
    el = document.body.querySelector('div');

    const tableWidget = (
      await import('../../bigframes/display/table_widget.js')
    ).default;
    render = tableWidget.render;

    model = {
      get: jest.fn(),
      set: jest.fn(),
      save_changes: jest.fn(),
      on: jest.fn(),
    };
  });

  it('should have a render function', () => {
    expect(render).toBeDefined();
  });

  describe('render', () => {
    it('should create the basic structure', () => {
      // Mock the initial state
      model.get.mockImplementation((property) => {
        if (property === 'table_html') {
          return '';
        }
        if (property === 'row_count') {
          return 100;
        }
        if (property === 'error_message') {
          return null;
        }
        if (property === 'page_size') {
          return 10;
        }
        if (property === 'page') {
          return 0;
        }
        return null;
      });

      render({ model, el });

      expect(el.classList.contains('bigframes-widget')).toBe(true);
      expect(el.querySelector('.error-message')).not.toBeNull();
      expect(el.querySelector('div')).not.toBeNull();
      expect(el.querySelector('div:nth-child(3)')).not.toBeNull();
    });

    it('should sort when a sortable column is clicked', () => {
      // Mock the initial state
      model.get.mockImplementation((property) => {
        if (property === 'table_html') {
          return '<table><thead><tr><th><div>col1</div></th></tr></thead></table>';
        }
        if (property === 'orderable_columns') {
          return ['col1'];
        }
        if (property === 'sort_context') {
          return [];
        }
        return null;
      });

      render({ model, el });

      // Manually trigger the table_html change handler
      const tableHtmlChangeHandler = model.on.mock.calls.find(
        (call) => call[0] === 'change:table_html',
      )[1];
      tableHtmlChangeHandler();

      const header = el.querySelector('th');
      header.click();

      expect(model.set).toHaveBeenCalledWith('sort_context', [
        { column: 'col1', ascending: true },
      ]);
      expect(model.save_changes).toHaveBeenCalled();
    });

    it('should reverse sort direction when a sorted column is clicked', () => {
      // Mock the initial state
      model.get.mockImplementation((property) => {
        if (property === 'table_html') {
          return '<table><thead><tr><th><div>col1</div></th></tr></thead></table>';
        }
        if (property === 'orderable_columns') {
          return ['col1'];
        }
        if (property === 'sort_context') {
          return [{ column: 'col1', ascending: true }];
        }
        return null;
      });

      render({ model, el });

      // Manually trigger the table_html change handler
      const tableHtmlChangeHandler = model.on.mock.calls.find(
        (call) => call[0] === 'change:table_html',
      )[1];
      tableHtmlChangeHandler();

      const header = el.querySelector('th');
      header.click();

      expect(model.set).toHaveBeenCalledWith('sort_context', [
        { column: 'col1', ascending: false },
      ]);
      expect(model.save_changes).toHaveBeenCalled();
    });

    it('should clear sort when a descending sorted column is clicked', () => {
      // Mock the initial state
      model.get.mockImplementation((property) => {
        if (property === 'table_html') {
          return '<table><thead><tr><th><div>col1</div></th></tr></thead></table>';
        }
        if (property === 'orderable_columns') {
          return ['col1'];
        }
        if (property === 'sort_context') {
          return [{ column: 'col1', ascending: false }];
        }
        return null;
      });

      render({ model, el });

      // Manually trigger the table_html change handler
      const tableHtmlChangeHandler = model.on.mock.calls.find(
        (call) => call[0] === 'change:table_html',
      )[1];
      tableHtmlChangeHandler();

      const header = el.querySelector('th');
      header.click();

      expect(model.set).toHaveBeenCalledWith('sort_context', []);
      expect(model.save_changes).toHaveBeenCalled();
    });

    it('should display the correct sort indicator', () => {
      // Mock the initial state
      model.get.mockImplementation((property) => {
        if (property === 'table_html') {
          return '<table><thead><tr><th><div>col1</div></th><th><div>col2</div></th></tr></thead></table>';
        }
        if (property === 'orderable_columns') {
          return ['col1', 'col2'];
        }
        if (property === 'sort_context') {
          return [{ column: 'col1', ascending: true }];
        }
        return null;
      });

      render({ model, el });

      // Manually trigger the table_html change handler
      const tableHtmlChangeHandler = model.on.mock.calls.find(
        (call) => call[0] === 'change:table_html',
      )[1];
      tableHtmlChangeHandler();

      const headers = el.querySelectorAll('th');
      const indicator1 = headers[0].querySelector('.sort-indicator');
      const indicator2 = headers[1].querySelector('.sort-indicator');

      expect(indicator1.textContent).toBe('▲');
      expect(indicator2.textContent).toBe('●');
    });

    it('should add a column to sort when Shift+Click is used', () => {
      // Mock the initial state: already sorted by col1 asc
      model.get.mockImplementation((property) => {
        if (property === 'table_html') {
          return '<table><thead><tr><th><div>col1</div></th><th><div>col2</div></th></tr></thead></table>';
        }
        if (property === 'orderable_columns') {
          return ['col1', 'col2'];
        }
        if (property === 'sort_context') {
          return [{ column: 'col1', ascending: true }];
        }
        return null;
      });

      render({ model, el });

      // Manually trigger the table_html change handler
      const tableHtmlChangeHandler = model.on.mock.calls.find(
        (call) => call[0] === 'change:table_html',
      )[1];
      tableHtmlChangeHandler();

      const headers = el.querySelectorAll('th');
      const header2 = headers[1]; // col2

      // Simulate Shift+Click
      const clickEvent = new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        shiftKey: true,
      });
      header2.dispatchEvent(clickEvent);

      expect(model.set).toHaveBeenCalledWith('sort_context', [
        { column: 'col1', ascending: true },
        { column: 'col2', ascending: true },
      ]);
      expect(model.save_changes).toHaveBeenCalled();
    });
  });

  describe('Theme detection', () => {
    beforeEach(() => {
      jest.useFakeTimers();
      // Mock the initial state for theme detection tests
      model.get.mockImplementation((property) => {
        if (property === 'table_html') {
          return '';
        }
        if (property === 'row_count') {
          return 100;
        }
        if (property === 'error_message') {
          return null;
        }
        if (property === 'page_size') {
          return 10;
        }
        if (property === 'page') {
          return 0;
        }
        return null;
      });
    });

    afterEach(() => {
      jest.useRealTimers();
      document.body.classList.remove('vscode-dark');
    });

    it('should add bigframes-dark-mode class in dark mode', () => {
      document.body.classList.add('vscode-dark');
      render({ model, el });
      jest.runAllTimers();
      expect(el.classList.contains('bigframes-dark-mode')).toBe(true);
    });

    it('should not add bigframes-dark-mode class in light mode', () => {
      render({ model, el });
      jest.runAllTimers();
      expect(el.classList.contains('bigframes-dark-mode')).toBe(false);
    });
  });

  it('should render the series as a table with an index and one value column', () => {
    // Mock the initial state
    model.get.mockImplementation((property) => {
      if (property === 'table_html') {
        return `
      <div class="paginated-table-container">
      <div id="table-c" class="table-container">
        <table class="bigframes-styles">
        <thead>
          <tr>
          <th class="col-header-name"><div></div></th>
          <th class="col-header-name"><div>value</div></th>
          </tr>
        </thead>
        <tbody>
          <tr>
          <td class="cell-align-right">0</td>
          <td class="cell-align-left">a</td>
          </tr>
          <tr>
          <td class="cell-align-right">1</td>
          <td class="cell-align-left">b</td>
          </tr>
        </tbody>
        </table>
      </div>
      </div>`;
      }
      if (property === 'orderable_columns') {
        return [];
      }
      return null;
    });

    render({ model, el });

    // Manually trigger the table_html change handler
    const tableHtmlChangeHandler = model.on.mock.calls.find(
      (call) => call[0] === 'change:table_html',
    )[1];
    tableHtmlChangeHandler();

    // Check that the table has two columns
    const headers = el.querySelectorAll(
      '.paginated-table-container .col-header-name',
    );
    expect(headers).toHaveLength(2);

    // Check that the headers are an empty string (for the index) and "value"
    expect(headers[0].textContent).toBe('');
    expect(headers[1].textContent).toBe('value');
  });

  /*
   * Tests that the widget correctly renders HTML with truncated columns (ellipsis)
   * and ensures that the ellipsis column is not treated as a sortable column.
   */
  it('should render truncated columns with ellipsis and not make ellipsis sortable', () => {
    // Mock HTML with truncated columns
    // Use the structure produced by the python backend
    const mockHtml = `
      <table>
        <thead>
          <tr>
            <th><div class="bf-header-content">col1</div></th>
            <th><div class="bf-header-content" style="cursor: default;">...</div></th>
            <th><div class="bf-header-content">col10</div></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="cell-align-right">1</td>
            <td class="cell-align-left">...</td>
            <td class="cell-align-right">10</td>
          </tr>
        </tbody>
      </table>
    `;

    model.get.mockImplementation((property) => {
      if (property === 'table_html') {
        return mockHtml;
      }
      if (property === 'orderable_columns') {
        // Only actual columns are orderable
        return ['col1', 'col10'];
      }
      if (property === 'sort_context') {
        return [];
      }
      return null;
    });

    render({ model, el });

    // Manually trigger the table_html change handler
    const tableHtmlChangeHandler = model.on.mock.calls.find(
      (call) => call[0] === 'change:table_html',
    )[1];
    tableHtmlChangeHandler();

    const headers = el.querySelectorAll('th');
    expect(headers).toHaveLength(3);

    // Check col1 (sortable)
    const col1Header = headers[0];
    const col1Indicator = col1Header.querySelector('.sort-indicator');
    expect(col1Indicator).not.toBeNull(); // Should exist (hidden by default)

    // Check ellipsis (not sortable)
    const ellipsisHeader = headers[1];
    const ellipsisIndicator = ellipsisHeader.querySelector('.sort-indicator');
    // The render function adds sort indicators only if the column name matches an entry in orderable_columns.
    // The ellipsis header content is "..." which is not in ['col1', 'col10'].
    expect(ellipsisIndicator).toBeNull();

    // Check col10 (sortable)
    const col10Header = headers[2];
    const col10Indicator = col10Header.querySelector('.sort-indicator');
    expect(col10Indicator).not.toBeNull();
  });

  describe('Max columns', () => {
    /*
     * Tests for the max columns dropdown functionality.
     */

    it('should render the max columns dropdown', () => {
      // Mock basic state
      model.get.mockImplementation((property) => {
        if (property === 'max_columns') {
          return 20;
        }
        return null;
      });

      render({ model, el });

      const maxColumnsContainer = el.querySelector('.max-columns');
      expect(maxColumnsContainer).not.toBeNull();
      const label = maxColumnsContainer.querySelector('label');
      expect(label.textContent).toBe('Max columns:');
      const select = maxColumnsContainer.querySelector('select');
      expect(select).not.toBeNull();
    });

    it('should select the correct initial value', () => {
      const initialMaxColumns = 20;
      model.get.mockImplementation((property) => {
        if (property === 'max_columns') {
          return initialMaxColumns;
        }
        return null;
      });

      render({ model, el });

      const select = el.querySelector('.max-columns select');
      expect(Number(select.value)).toBe(initialMaxColumns);
    });

    it('should handle None/null initial value as 0 (All)', () => {
      model.get.mockImplementation((property) => {
        if (property === 'max_columns') {
          return null; // Python None is null in JS
        }
        return null;
      });

      render({ model, el });

      const select = el.querySelector('.max-columns select');
      expect(Number(select.value)).toBe(0);
      expect(select.options[select.selectedIndex].textContent).toBe('All');
    });

    it('should update model when value changes', () => {
      model.get.mockImplementation((property) => {
        if (property === 'max_columns') {
          return 20;
        }
        return null;
      });

      render({ model, el });

      const select = el.querySelector('.max-columns select');

      // Change to 10
      select.value = '10';
      const event = new Event('change');
      select.dispatchEvent(event);

      expect(model.set).toHaveBeenCalledWith('max_columns', 10);
      expect(model.save_changes).toHaveBeenCalled();
    });
  });
});
