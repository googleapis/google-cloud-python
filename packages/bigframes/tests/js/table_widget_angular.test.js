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
    'should bootstrap multiple widgets independently on their respective elements',
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

      const appRoot1 = el1.querySelector('app-root');
      expect(appRoot1).not.toBeNull();
      expect(el1.textContent).toContain('Widget 1 Content');
      expect(el1.textContent).toContain('100 total rows');
      expect(el1.textContent).toContain('Page 1 of 10');

      const appRoot2 = el2.querySelector('app-root');
      expect(appRoot2).not.toBeNull();
      expect(el2.textContent).toContain('Widget 2 Content');
      expect(el2.textContent).toContain('200 total rows');
      expect(el2.textContent).toContain('Page 1 of 8');

      document.body.removeChild(el1);
      document.body.removeChild(el2);
    });
});
