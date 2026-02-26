## Testing with nox

Use `nox` to instrument our tests.

- To test your changes, run unit tests with `nox`:

  ```bash
  nox -r -s unit
  ```

- To run a single unit test:

  ```bash
  nox -r -s unit-3.14 -- -k <name of test>
  ```

- Ignore this step if you lack access to Google Cloud resources. To run system
  tests, you can execute::

   # Run all system tests
   $ nox -r -s system

   # Run a single system test
   $ nox -r -s system-3.14 -- -k <name of test>

- The codebase must have better coverage than it had previously after each
  change. You can test coverage via `nox -s unit system cover` (takes a long
  time). Omit `system` if you lack access to cloud resources.
