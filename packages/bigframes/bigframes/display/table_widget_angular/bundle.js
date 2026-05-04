const esbuild = require('esbuild');
const path = require('path');

esbuild.build({
  entryPoints: [path.resolve(__dirname, 'dist/table-widget-angular/browser/main.js')],
  bundle: true,
  outfile: path.resolve(__dirname, '../table_widget_angular.js'),
  format: 'esm',
  logLevel: 'info',
}).catch(() => process.exit(1));
