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

import { Component, Inject, signal } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [],
  template: `
    <div class="angular-widget">
      <h3>Angular Hybrid Widget</h3>
      <p>Status: Infrastructure Loaded</p>
      <p>Message from Python: {{ message() }}</p>
      <div [innerHTML]="sanitizedHtml()"></div>
    </div>
  `,
  styles: [`
    .angular-widget {
      background-color: #f9f9f9;
      border: 1px solid #ccc;
      border-radius: 4px;
      padding: 10px;
    }
  `]
})
// Dummy comment to test pre-commit hook
export class App {
  protected readonly message = signal('Waiting for model...');
  protected readonly sanitizedHtml = signal<SafeHtml>('');

  constructor(
    @Inject('ANYWIDGET_MODEL') public model: any,
    private sanitizer: DomSanitizer
  ) {
    if (model) {
      this.message.set(model.get('message') || 'Model loaded, no message.');

      const rawHtml = model.get('table_html') || '<p>No table HTML yet.</p>';
      this.sanitizedHtml.set(this.sanitizer.bypassSecurityTrustHtml(rawHtml));

      // Listen for changes
      model.on('change:message', () => {
        this.message.set(model.get('message'));
      });
      model.on('change:table_html', () => {
        const html = model.get('table_html');
        this.sanitizedHtml.set(this.sanitizer.bypassSecurityTrustHtml(html));
      });
    }
  }
}
