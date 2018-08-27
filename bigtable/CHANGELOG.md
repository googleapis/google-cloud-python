# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-bigtable/#history

## 0.30.0

## 0.30.0

### New Features

- Improved reads: Improving performance, and capabilities of reads.  `read_rows` now returns a generator; has automatic retries; and can read an arbitrary set of keys and ranges
-- Consolidated read_rows and yield_rows (#5840)
-- Implemented row set for yield_rows  (#5506)
-- Improved read rows validation performance (#5390)
-- Added retry for yield_rows (#4882)
-- Required TimestampRanges to be milliseconds granularity (#5002)
-- Provided better access to cell values  (#4908)
-- Added data app profile id  (#5369)

- Improved writes: Writes are usable in Beam
-- Creatd MutationBatcher for bigtable (#5651)
-- Allowed DirectRow to be created without a table (#5567)
-- Added data app profile id  (#5369)


- Improved table admin: Table creation now can also create families in a single RPC.  Added an `exist()` method.  Added `get_cluster_states` for information about replication
-- Added 'Table.get_cluster_states' method (#5790)
-- Optimized 'Table.exists' performance (#5749)
-- Added column creation in 'Table.create()'. (#5576)
-- Added 'Table.exists' method (#5545)
-- Added split keys on create table - v2 (#5513)
-- Avoid sharing table names across unrelated systests. (#5421)
-- Added truncate table and drop by prefix on top of GAPIC integration (#5360)

- Improved instance admin: Instance creation allows for the creation of multiple clusters.  Instance lable management is now enabled.  
-- Fixed failing systest: 'test_create_instance_w_two_clusters'. (#5836)
-- Created app_profile_object (#5782)
-- Added instance.exists(), system and unit tests (#5802)
-- Added 'Client.list_clusters()' (#5715)
-- Added labels {'python-system': ISO-timestamp} to systest instances (#5729)
-- Added 'Instance._state' property (#5736)
-- Converted 'instance.labels' to return as dictionary (#5728)
-- Shortenned cluster ID in system test (#5719)
-- Reshaped cluster.py, adding cluster() factory to instance.py (#5663)
-- Hardened 'test_list_instances' further. (#5696)
-- Converted 'Instance.update()' to use 'instance.partial_instance_update' API (#5643)
-- Refactored update_app_profile() to remove update_mask argument (#5684)
-- Added the ability to create an instance with multiple clusters (#5622)
-- Shortened instance / cluster name to fix CI breakage. (#5641)
-- Added 'instance_type', 'labels' to 'Instance' ctor (#5614)
-- Added optional app profile on instance.table() (#5605)
-- Cleaned up Instance creation. (#5542)
-- Improved testing of create instance (#5544)
-- Hardened 'test_list_instances' against simultaneous test runs. (#5476)
-- Made 'Client.list_instances' return actual instance objects, not protos. (#5420)
-- Pass through 'session.posargs' when running Bigtable system tests. (#5418)
-- Added admin app profile methods on Instance (#5315)

### Internal / Testing Changes
- Fixing the broken Bigtable system test. (#5607)
- Used client properties rather than private attrs (#5398)
- Fixed Py3 breakage in new system test. (#5474)
- Modified system test for new GAPIC code (#5302)
- Renamed releases to changelog and include from CHANGELOG.md (#5191)
- Integrated new generated low-level client (#5178)
- Fixed bad trove classifier
- Added Test runs for Python 3.7 and remove 3.4 (#5295)
- Disabled Bigtable system tests (#5381)
- Modified system tests to use prerelease versions of grpcio (#5304)
- Overrode gRPC max message lengths. (#5498)

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
