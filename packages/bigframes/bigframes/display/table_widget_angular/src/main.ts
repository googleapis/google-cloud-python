import { bootstrapApplication } from '@angular/platform-browser';
import { App } from './app/app';
import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';

function render({ model, el }: { model: any, el: HTMLElement }) {
  // Create a container for the Angular app
  const appRoot = document.createElement('app-root');
  el.appendChild(appRoot);

  const appConfig: ApplicationConfig = {
    providers: [
      provideBrowserGlobalErrorListeners(),
      { provide: 'ANYWIDGET_MODEL', useValue: model }
    ]
  };

  bootstrapApplication(App, appConfig)
    .catch((err) => console.error(err));
}

export default { render };
