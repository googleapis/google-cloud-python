# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-bigtable/#history

## 0.29.0

- Update dependency range for api-core to include v1.0.0 releases (#4944)
- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Remove gax usage from BigTable (#4873)
- Use `api_core.retry` for `mutate_row` (#4665)
- BigTable: Adding a row generator on a table. (#4679)
- BigTable: Timestamp system test fix (#4765)
- BigTable: Cell.from_pb() performance improvement (#4745)
- BigTable: minor typo (#4758)
- Bigtable: Row filter end points documentation error (#4667)
- Add `google.cloud.container` API. (#4577)
- Removing "rename" from bigtable table.py comments (#4526)
- Revert "Add RPC retries to Bigtable (#3811)" (#4524)
- Add RPC retries to Bigtable (#3811)
- Handle retry=None for mutate_rows, and some refactoring in test (#4341)
- BigQuery: moves Row class out of helpers and updates docstrings (#4291)
- BigTable: Small docs/hygiene tweaks after #4256. (#4333)
- Marking Bigtable as "dev" after release. (#4332)

## 0.28.1

### Implementation Changes

- Bugfix: Distinguish between an unset column qualifier and an empty string
  column qualifier while parsing a `ReadRows` response (#4252)

### Features added

- Add a ``retry`` strategy that will be used for retry-able errors
  in ``Table.mutate_rows``. This will be used for gRPC errors of type
  ``ABORTED``, ``DEADLINE_EXCEEDED`` and ``SERVICE_UNAVAILABLE``. (#4256)

PyPI: https://pypi.org/project/google-cloud-bigtable/0.28.1/

## 0.28.0

### Documentation

- Fixed referenced types in `Table.row` docstring (#3934, h/t to
  @MichaelTamm)
- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-bigtable/0.28.0/
