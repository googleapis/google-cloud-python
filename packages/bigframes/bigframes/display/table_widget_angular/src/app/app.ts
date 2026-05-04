import { Component, Inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
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
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
      background-color: #f9f9f9;
    }
  `]
})
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
