import { Component, Inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="angular-widget">
      <h3>Angular Hybrid Widget</h3>
      <p>Status: Infrastructure Loaded</p>
      <p>Message from Python: {{ message() }}</p>
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

  constructor(@Inject('ANYWIDGET_MODEL') public model: any) {
    if (model) {
      this.message.set(model.get('message') || 'Model loaded, no message.');
      // Listen for changes
      model.on('change:message', () => {
        this.message.set(model.get('message'));
      });
    }
  }
}
