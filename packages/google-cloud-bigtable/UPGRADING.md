# 3.0.0 Migration Guide

The v3.0.0 release of `google-cloud-bigtable` deprecates the previous `google.cloud.bigtable.Client` class in favor of distinct clients for the two API surfaces, supporting both sync and async calls:
- Data API: 
  - `google.cloud.bigtable.data.BigtableDataClient`
  - `google.cloud.bigtable.data.BigtableDataClientAsync`
- Admin API: 
  - `google.cloud.bigtable.admin.BigtableInstanceAdminAsyncClient`
  - `google.cloud.bigtable.admin.BigtableInstanceAdminClient`
  - `google.cloud.bigtable.admin.BigtableTableAdminClient`
  - `google.cloud.bigtable.admin.BigtableTableAdminAsyncClient`

The deprecated client will remain available as an alternative API surface, which internally delegates calls to the respective new clients. For most users, existing code will continue to work as before. But there may be some breaking changes associated with this update, which are detailed in this document.

If you experience technical issues or have questions, please file an [issue](https://github.com/googleapis/python-bigtable/issues).

## Breaking Changes
- **[MutationBatcher](https://github.com/googleapis/python-bigtable/blob/main/google/cloud/bigtable/data/_sync_autogen/mutations_batcher.py#L151) and [MutationBatcherAsync](https://github.com/googleapis/python-bigtable/blob/main/google/cloud/bigtable/data/_async/mutations_batcher.py#L182)'s `table` argument was renamed to `target`**, since it also supports [Authorized View](https://github.com/googleapis/python-bigtable/pull/1034) instances. This matches the naming used in other classes (PR: https://github.com/googleapis/python-bigtable/pull/1153)
