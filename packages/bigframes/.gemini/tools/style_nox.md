## Code Style with nox

- We use the automatic code formatter `black`. You can run it using
  the nox session `format`. This will eliminate many lint errors. Run via:

  ```bash
  nox -r -s format
  ```

- PEP8 compliance is required, with exceptions defined in the linter configuration.
  If you have ``nox`` installed, you can test that you have not introduced
  any non-compliant code via:

  ```
  nox -r -s lint
  ```

- When writing tests, use the idiomatic "pytest" style.
