# Changelog

## 0.1.0 (2026-08-16)

- Initial release of `google-cloud-spanner-arrow`.
- Native C extension leveraging `nanoarrow` and the Arrow C Data Interface (`RecordBatch._import_from_c`).
- GIL-free parsing of Spanner rows and partial result set streams into Arrow RecordBatches.
- Dynamic integration with `google-cloud-spanner`'s `StreamedResultSet`.
