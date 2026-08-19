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

import { Injectable, Inject, signal } from '@angular/core';

export interface SortItem {
  column: string;
  ascending: boolean;
}

@Injectable()
export class WidgetStateService {
  readonly page = signal<number>(0);
  readonly pageSize = signal<number>(10);
  readonly maxColumns = signal<number>(0);
  readonly rowCount = signal<number | null>(null);
  readonly tableHtml = signal<string>('');
  readonly sortContext = signal<SortItem[]>([]);
  readonly orderableColumns = signal<string[]>([]);
  readonly errorMessage = signal<string | null>(null);
  readonly startExecution = signal<boolean>(false);
  readonly isDeferredMode = signal<boolean>(false);
  readonly dryRunInfo = signal<string>('');
  readonly ping = signal<number>(0);

  constructor(@Inject('ANYWIDGET_MODEL') private model: any) {
    if (model) {
      // Initialize from the model
      this.page.set(model.get('page') ?? 0);
      this.pageSize.set(model.get('page_size') ?? 10);
      this.maxColumns.set(model.get('max_columns') ?? 0);
      this.rowCount.set(model.get('row_count') ?? null);
      this.tableHtml.set(model.get('table_html') ?? '');
      this.sortContext.set(model.get('sort_context') ?? []);
      this.orderableColumns.set(model.get('orderable_columns') ?? []);
      const initialError =
        model.get('error_message') ??
        model.get('_error_message') ??
        null;
      this.errorMessage.set(initialError);
      this.startExecution.set(model.get('start_execution') ?? false);
      this.isDeferredMode.set(model.get('is_deferred_mode') ?? false);
      this.dryRunInfo.set(model.get('dry_run_info') ?? '');
      this.ping.set(model.get('ping') ?? 0);

      // Register event listeners for anywidget updates
      model.on('change:page', () => {
        this.page.set(model.get('page'));
      });
      model.on('change:page_size', () => {
        this.pageSize.set(model.get('page_size'));
      });
      model.on('change:max_columns', () => {
        this.maxColumns.set(model.get('max_columns'));
      });
      model.on('change:row_count', () => {
        this.rowCount.set(model.get('row_count'));
      });
      model.on('change:table_html', () => {
        this.tableHtml.set(model.get('table_html'));
      });
      model.on('change:sort_context', () => {
        this.sortContext.set(model.get('sort_context'));
      });
      model.on('change:orderable_columns', () => {
        this.orderableColumns.set(model.get('orderable_columns'));
      });
      model.on('change:start_execution', () => {
        this.startExecution.set(model.get('start_execution') ?? false);
      });
      model.on('change:is_deferred_mode', () => {
        this.isDeferredMode.set(model.get('is_deferred_mode') ?? false);
      });
      model.on('change:dry_run_info', () => {
        this.dryRunInfo.set(model.get('dry_run_info') ?? '');
      });
      model.on('change:ping', () => {
        this.ping.set(model.get('ping') ?? 0);
      });

      // Robust dual-listen pattern for error messages (with/without underscore)
      const handleErrorChange = () => {
        const err =
          model.get('error_message') ??
          model.get('_error_message') ??
          null;
        this.errorMessage.set(err);
      };
      model.on('change:error_message', handleErrorChange);
      model.on('change:_error_message', handleErrorChange);
    }
  }

  setPage(page: number) {
    this.page.set(page);
    if (this.model) {
      this.model.set('page', page);
      this.model.save_changes();
    }
  }

  setPageSize(pageSize: number) {
    this.pageSize.set(pageSize);
    this.page.set(0);
    if (this.model) {
      this.model.set('page_size', pageSize);
      // Reset to page 0 on page size change
      this.model.set('page', 0);
      this.model.save_changes();
    }
  }

  setMaxColumns(maxColumns: number) {
    this.maxColumns.set(maxColumns);
    if (this.model) {
      this.model.set('max_columns', maxColumns);
      this.model.save_changes();
    }
  }

  setSortContext(context: SortItem[]) {
    this.sortContext.set(context);
    if (this.model) {
      this.model.set('sort_context', context);
      this.model.save_changes();
    }
  }

  setStartExecution(startExecution: boolean) {
    this.startExecution.set(startExecution);
    if (this.model) {
      this.model.set('start_execution', startExecution);
      this.model.save_changes();
    }
  }

  setPing(ping: number) {
    this.ping.set(ping);
    if (this.model) {
      this.model.set('ping', ping);
      this.model.save_changes();
    }
  }
}
