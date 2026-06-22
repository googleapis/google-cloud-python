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

import { jest } from '@jest/globals';

describe('TableWidgetAngular', () => {
  let render;

  beforeEach(async () => {
    jest.resetModules();
    const tableWidgetAngular = (
      await import('../../bigframes/display/table_widget_angular.js')
    ).default;
    render = tableWidgetAngular.render;
  });

  it('should have a render function', () => {
    expect(render).toBeDefined();
  });

  it(
    'should bootstrap multiple widgets independently ' +
      'on their respective elements',
    async () => {
      const el1 = document.createElement('div');
      document.body.appendChild(el1);

      const model1 = {
        get: jest.fn((prop) => {
          if (prop === 'table_html') {
            return '<table><tr><td>Widget 1 Content</td></tr></table>';
          }
          if (prop === 'page_size') return 10;
          if (prop === 'page') return 0;
          if (prop === 'row_count') return 100;
          if (prop === 'max_columns') return 20;
          return null;
        }),
        set: jest.fn(),
        save_changes: jest.fn(),
        on: jest.fn(),
      };

      const el2 = document.createElement('div');
      document.body.appendChild(el2);

      const model2 = {
        get: jest.fn((prop) => {
          if (prop === 'table_html') {
            return '<table><tr><td>Widget 2 Content</td></tr></table>';
          }
          if (prop === 'page_size') return 25;
          if (prop === 'page') return 0;
          if (prop === 'row_count') return 200;
          if (prop === 'max_columns') return 20;
          return null;
        }),
        set: jest.fn(),
        save_changes: jest.fn(),
        on: jest.fn(),
      };

      render({ model: model1, el: el1 });
      render({ model: model2, el: el2 });

      // Wait for async angular bootstrap to complete
      await new Promise((resolve) => setTimeout(resolve, 200));

      const appRoot1 = el1.querySelector('.bigframes-widget');
      expect(appRoot1).not.toBeNull();
      expect(el1.textContent).toContain('Widget 1 Content');
      expect(el1.textContent).toContain('100 total rows');
      expect(el1.textContent).toContain('Page 1 of 10');

      const appRoot2 = el2.querySelector('.bigframes-widget');
      expect(appRoot2).not.toBeNull();
      expect(el2.textContent).toContain('Widget 2 Content');
      expect(el2.textContent).toContain('200 total rows');
      expect(el2.textContent).toContain('Page 1 of 8');

      document.body.removeChild(el1);
      document.body.removeChild(el2);
    });

  it(
    'should render deferred card and trigger execution on click',
    async () => {
      // Arrange
      const el = document.createElement('div');
      document.body.appendChild(el);

      const state = {
        is_deferred_mode: true,
        dry_run_info: 'Estimated cost: $0.05',
        start_execution: false,
        table_html: '',
        page_size: 10,
        page: 0,
        row_count: 0,
        max_columns: 20,
      };

      const listeners = {};
      const model = {
        get: jest.fn((prop) => state[prop]),
        set: jest.fn((prop, val) => {
          state[prop] = val;
        }),
        save_changes: jest.fn(),
        on: jest.fn((event, callback) => {
          listeners[event] = callback;
        }),
      };

      // Act
      render({ model, el });
      await new Promise((resolve) => setTimeout(resolve, 200));

      // Assert (Initial state)
      const estimate = el.querySelector('.deferred-estimate');
      expect(estimate).not.toBeNull();
      expect(estimate.textContent).toContain('Estimated cost: $0.05');

      const runButton = el.querySelector('.run-query-button');
      expect(runButton).not.toBeNull();
      expect(runButton.textContent).toContain('Run Query');
      expect(el.querySelector('.table-container')).toBeNull();

      // Act (Click Run Query)
      runButton.click();
      await new Promise((resolve) => setTimeout(resolve, 50));

      // Assert (Execution requested)
      expect(model.set).toHaveBeenCalledWith('start_execution', true);
      expect(model.save_changes).toHaveBeenCalled();
      expect(runButton.disabled).toBe(true);
      expect(el.querySelector('.spinner')).not.toBeNull();

      // Act (Simulate Python load completion)
      state.is_deferred_mode = false;
      state.table_html = '<table><tr><td>Data Loaded</td></tr></table>';
      state.row_count = 50;

      if (listeners['change:is_deferred_mode']) {
        listeners['change:is_deferred_mode']();
      }
      if (listeners['change:table_html']) {
        listeners['change:table_html']();
      }
      if (listeners['change:row_count']) {
        listeners['change:row_count']();
      }
      await new Promise((resolve) => setTimeout(resolve, 200));

      // Assert (Transition to loaded state)
      expect(el.querySelector('.deferred-container')).toBeNull();
      const tableContainer = el.querySelector('.table-container');
      expect(tableContainer).not.toBeNull();
      expect(el.textContent).toContain('Data Loaded');
      expect(el.textContent).toContain('50 total rows');

      // Clean up
      document.body.removeChild(el);
    });
});
