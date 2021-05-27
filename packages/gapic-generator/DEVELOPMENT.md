# Development

- Install dependencies with `pip install .`
- See all nox sessions with `nox -l`
- Execute unit tests by running one of the sessions prefixed with `unit-`
  - Example: `nox -s unit-3.8`
- Lint sources by running `autopep8`.

## Integration Tests
- Running tests: `bazel test tests/integration:asset`. See the full list of targets in `tests/integration/BUILD.bazel`.
- Updating golden files: `bazel run tests/integration:asset_update`
