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

import { createApplication } from '@angular/platform-browser';
import { App } from './app/app';
import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZonelessChangeDetection } from '@angular/core';

function render({ model, el }: { model: any, el: HTMLElement }) {
  // Create a container for the Angular app
  const appRoot = document.createElement('div');
  appRoot.setAttribute('app-root', '');
  el.appendChild(appRoot);

  const appConfig: ApplicationConfig = {
    providers: [
      provideBrowserGlobalErrorListeners(),
      provideZonelessChangeDetection(),
      { provide: 'ANYWIDGET_MODEL', useValue: model }
    ]
  };

  createApplication(appConfig)
    .then((appRef) => {
      appRef.bootstrap(App, appRoot);
      appRoot.removeAttribute('app-root');
    })
    .catch((err) => console.error(err));
}

export default { render };
