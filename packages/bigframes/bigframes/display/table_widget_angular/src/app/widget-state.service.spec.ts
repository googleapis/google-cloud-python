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

import { TestBed } from '@angular/core/testing';
import { vi } from 'vitest';
import { WidgetStateService } from './widget-state.service';

describe('WidgetStateService', () => {
  let service: WidgetStateService;
  let mockModel: any;
  let mockListeners: { [key: string]: Function };

  beforeEach(() => {
    mockListeners = {};
    mockModel = {
      get: vi.fn().mockImplementation((prop: string) => {
        if (prop === 'page') return 2;
        if (prop === 'page_size') return 25;
        if (prop === 'max_columns') return 10;
        if (prop === 'row_count') return 150;
        if (prop === 'table_html') return '<table></table>';
        if (prop === 'sort_context') {
          return [{ column: 'col1', ascending: true }];
        }
        if (prop === 'orderable_columns') {
          return ['col1', 'col2'];
        }
        if (prop === 'error_message') return 'initial error';
        return null;
      }),
      set: vi.fn(),
      save_changes: vi.fn(),
      on: vi.fn().mockImplementation(
        (event: string, callback: Function) => {
          mockListeners[event] = callback;
        }
      )
    };

    TestBed.configureTestingModule({
      providers: [
        WidgetStateService,
        { provide: 'ANYWIDGET_MODEL', useValue: mockModel }
      ]
    });
    service = TestBed.inject(WidgetStateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should initialize signals from model values', () => {
    expect(service.page()).toBe(2);
    expect(service.pageSize()).toBe(25);
    expect(service.maxColumns()).toBe(10);
    expect(service.rowCount()).toBe(150);
    expect(service.tableHtml()).toBe('<table></table>');
    expect(service.sortContext()).toEqual([
      { column: 'col1', ascending: true }
    ]);
    expect(service.orderableColumns()).toEqual(['col1', 'col2']);
    expect(service.errorMessage()).toBe('initial error');
  });

  it('should update signals when model triggers change events', () => {
    mockModel.get.mockImplementation((prop: string) => {
      if (prop === 'page') return 5;
      if (prop === 'page_size') return 50;
      return null;
    });

    mockListeners['change:page']();
    mockListeners['change:page_size']();

    expect(service.page()).toBe(5);
    expect(service.pageSize()).toBe(50);
  });

  it('should support dual-listen pattern for error messages', () => {
    // 1. Check error_message change
    mockModel.get.mockImplementation((prop: string) => {
      if (prop === 'error_message') return 'new error';
      return null;
    });
    mockListeners['change:error_message']();
    expect(service.errorMessage()).toBe('new error');

    // 2. Check _error_message change
    mockModel.get.mockImplementation((prop: string) => {
      if (prop === '_error_message') return 'new private error';
      return null;
    });
    mockListeners['change:_error_message']();
    expect(service.errorMessage()).toBe('new private error');
  });

  it('should write updates back to model on setter methods', () => {
    service.setPage(4);
    expect(mockModel.set).toHaveBeenCalledWith('page', 4);
    expect(mockModel.save_changes).toHaveBeenCalled();

    service.setPageSize(100);
    expect(mockModel.set).toHaveBeenCalledWith('page_size', 100);
    expect(mockModel.set).toHaveBeenCalledWith('page', 0);

    service.setMaxColumns(15);
    expect(mockModel.set).toHaveBeenCalledWith('max_columns', 15);

    service.setSortContext([{ column: 'col2', ascending: false }]);
    expect(mockModel.set).toHaveBeenCalledWith(
      'sort_context',
      [{ column: 'col2', ascending: false }]
    );
  });
});
