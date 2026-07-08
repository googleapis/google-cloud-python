# TableWidgetAngular

This project is the Angular-based interactive Table Widget frontend for BigQuery DataFrames (``bigframes``). It is integrated into the Python backend using ``anywidget``.

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 21.2.9.

## Getting Started

Ensure you have [Node.js](https://nodejs.org/) installed.

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the local development server:
   ```bash
   npm run start
   ```
   Navigate to `http://localhost:4200/`. The application will automatically reload when you modify the source files under `src/`.

## Development & Code Scaffolding

To generate a new component, directive, or service:
```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:
```bash
ng generate --help
```

## Running Tests

To execute unit tests:
```bash
npm run test
```

## Packaging for Python

Before testing the widget inside a Jupyter notebook or committing changes, compile the Angular app and bundle it so that the Python backend can load it:
```bash
npm run build:widget
```

This command compiles the project in production mode and then triggers `bundle.js` (via `esbuild`) to bundle the browser artifacts into a single unified ES module file at `../table_widget_angular.js`.
