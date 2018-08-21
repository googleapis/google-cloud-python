# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-bigtable/#history

## 0.30.0

- Bigtable: app_profile_object (#5782)
- added instance.exists(), system and unit tests (#5802)
- Bigtable: add 'Client.list_clusters()' (#5715)
- Bigtable: optimize 'Table.exists' performance (#5749)
- Bigtable: add labels {'python-system': ISO-timestamp} to systest instances (#5729)
- Bigtable : Add 'Instance._state' property (#5736)
- BigTable: Create MutationBatcher for bigtable (#5651)
- BIgtable: return 'instance.labels' as dictionary (#5728)
- shortenning cluster ID in system test (#5719)
- Bigtable: Reshaping cluster.py, adding cluster() factory to instance.py (#5663)
- Harden 'test_list_instances' further. (#5696)
- Bigtable: 'Instance.update()' now uses 'instance.partial_instance_update' API (#5643)
- Bigtable: refactor update_app_profile() to remove update_mask argument (#5684)
- Bigtable: Ability to create an instance with multiple clusters (#5622)
- Shorten instance / cluster name to fix CI breakage. (#5641)
- Bigtable:  Add 'instance_type', 'labels' to 'Instance' ctor (#5614)
- Adding optional app profile on instance.table() (#5605)
- Fixing the broken Bigtable system test. (#5607)
- Bigtable : Implement row set for yield_rows  (#5506)
- Bigtable: Allow 'Table.create()' to create column families. (#5576)
- Bigtable: DirectRow without a table (#5567)
- BigTable: Add split keys on create table - v2 (#5513)
- Add 'Table.exists' method (#5545)
- Bigtable: Instance creation cleanup. (#5542)
- Bigtable: Improve testing of create instance (#5544)
- Override gRPC max message lengths. (#5498)
- Harden 'test_list_instances' against simultaneous test runs. (#5476)
- Fix Py3 breakage in new system test. (#5474)
- BigTable: Add truncate table and drop by prefix on top of GAPIC integration (#5360)
- Make 'Client.list_instances' return actual instance objects, not protos. (#5420)
- Avoid sharing table names across unrelated systests. (#5421)
- BigTable: use client properties rather than private attrs (#5398)
- Pass through 'session.posargs' when running Bigtable system tests. (#5418)
- BigTable: Add admin app profile methods on Instance (#5315)
- BigTable: improve read rows validation performance (#5390)
- BigTable: Add data app profile id  (#5369)
- disable bigtable system tests (#5381)
- Avoid overwriting '__module__' of messages from shared modules. (#5364)
- BigTable: Modify system test for new GAPIC code (#5302)
- Modify system tests to use prerelease versions of grpcio (#5304)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Integrate new generated low-level client (#5178)
- Rename releases to changelog and include from CHANGELOG.md (#5191)
- Add retry for yield_rows (#4882)
- Bigtable: TimestampRanges must be milliseconds granularity (#5002)
- Fix bad trove classifier
- BigTable: provide better access to cell values  (#4908)

### Implementation Changes

### New Features

### Dependencies

### Documentation

### Internal / Testing Changes

## 0.29.0

### New features

- Use `api_core.retry` for `mutate_row` (#4665, #4341)
- Added a row generator on a table. (#4679)

### Implementation changes

- Remove gax usage from BigTable (#4873)
- BigTable: Cell.from_pb() performance improvement (#4745)

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Documentation

- Minor typo (#4758)
- Row filter end points documentation error (#4667)
- Removing "rename" from bigtable table.py comments (#4526)
- Small docs/hygiene tweaks after #4256. (#4333)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Timestamp system test fix (#4765)

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
