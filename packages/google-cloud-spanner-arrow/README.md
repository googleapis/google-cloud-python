# Google Cloud Spanner Apache Arrow Accelerator

[![PyPI version](https://badge.fury.io/py/google-cloud-spanner-arrow.svg)](https://badge.fury.io/py/google-cloud-spanner-arrow)

High-performance native C extension and Apache Arrow accelerator for the Google Cloud Spanner Python client library (`google-cloud-spanner`).

## Overview

`google-cloud-spanner-arrow` accelerates ingestion of Cloud Spanner `PartialResultSet` protobuf streams into Apache Arrow `RecordBatch` / `Table` / `DataFrame` structures.

### Highlights
- **Native C Data Ingestion**: Zero-copy parsing of Spanner primitive types (INT64, FLOAT64, BOOL, STRING, BYTES, DATE, TIMESTAMP, NUMERIC) into Arrow memory buffers using `nanoarrow` and the Arrow C Data Interface (`RecordBatch._import_from_c`).
- **GIL Release for Multi-Threaded Partitioned Queries**: Releases CPython's Global Interpreter Lock (GIL) during parsing for linear scaling across multi-core CPU architectures.
- **Seamless Drop-in Integration**: Automatically discovered by `google-cloud-spanner`'s `StreamedResultSet.to_arrow_batches()`, `to_arrow()`, and `to_dataframe()`, with pure-Python fallback if not installed.

## Quick Start

### Installation

```bash
pip install google-cloud-spanner-arrow
```

### Usage with `google-cloud-spanner`

When `google-cloud-spanner-arrow` is installed in your Python environment, `google-cloud-spanner` automatically uses the native C accelerator:

```python
from google.cloud import spanner

client = spanner.Client()
instance = client.instance("my-instance")
database = instance.database("my-database")

with database.snapshot() as snapshot:
    results = snapshot.execute_sql("SELECT * FROM large_table")
    # Native C-accelerated Arrow batch iterator
    for batch in results.to_arrow_batches(max_chunk_size=65536):
        print(f"Batch rows: {batch.num_rows}")

    # Or directly as a PyArrow Table or Pandas DataFrame
    table = results.to_arrow()
    df = results.to_dataframe()
```

## Pure-Python Fallback Mode

To explicitly disable the C extension and force pure-Python fallback, set the environment variable:

```bash
export SPANNER_ARROW_PURE_PYTHON=1
```
