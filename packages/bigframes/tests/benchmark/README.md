# BigFrames Benchmarking
## Overview
This directory contains scripts for performance benchmarking of various components of BigFrames.

## Why Separate Processes?
Each benchmark is executed in a separate process to mitigate the effects of any residual caching or settings that may persist in BigFrames, ensuring that each test is conducted in a clean state.

## Available Benchmarks
This section lists the benchmarks currently available, with descriptions and links to their sources:
- **DB Benchmark**: This benchmark is adapted from DuckDB Labs and is designed to assess database performance. More information can be found on the [official DB Benchmark GitHub page](https://github.com/duckdblabs/db-benchmark).
- **TPC-H Benchmark**: Based on the TPC-H standards, this benchmark evaluates transaction processing capabilities. It is adapted from code found in the Polars repository, specifically tailored to test and compare these capabilities. Details are available on the [Polars Benchmark GitHub repository](https://github.com/pola-rs/polars-benchmark).
- **Notebooks**: These Jupyter notebooks showcase BigFrames' key features and patterns, and also enable performance benchmarking. Explore them at the [BigFrames Notebooks repository](https://github.com/googleapis/python-bigquery-dataframes/tree/main/notebooks).

## Benchmark Configuration Using `config.jsonl` Files

For each benchmark, a corresponding `config.jsonl` file exists in the same folder or its parent folder. These configuration files allow users to control various benchmark parameters without modifying the code directly. By updating the relevant `config.jsonl` file in the specific benchmark's folder, you can easily configure settings such as:
- **benchmark_suffix**: A suffix appended to the benchmark name for identification purposes.
- **ordered**: Controls the mode for BigFrames, specifying whether to use ordered (`true`) or unordered mode (`false`).
- **project_id**: The Google Cloud project ID where the benchmark dataset or table is located.
- **dataset_id**: The dataset ID for querying during the benchmark.
- **table_id**: This is **required** for benchmarks like `dbbenchmark` that target a specific table, but is **not configurable** for benchmarks like `TPC-H`, which use multiple tables with fixed names.

### Example `config.jsonl` Files

#### `dbbenchmark` Example
```jsonl
{"benchmark_suffix": "50g_ordered", "project_id": "your-google-cloud-project", "dataset_id": "dbbenchmark", "table_id": "G1_1e9_1e2_5_0", "ordered": true}
{"benchmark_suffix": "50g_unordered", "project_id": "your-google-cloud-project", "dataset_id": "dbbenchmark", "table_id": "G1_1e9_1e2_5_0", "ordered": false}
```

#### `TPC-H` Example
```jsonl
{"benchmark_suffix": "10t_unordered", "project_id":  "your-google-cloud-project", "dataset_id": "tpch_0010t", "ordered": false}
```

## Usage Examples
Our benchmarking process runs internally on a daily basis to continuously monitor the performance of BigFrames. However, there are occasions when you might need to conduct benchmarking locally to test specific changes or new features.

Here's how you can run benchmarks locally:

- **Running Notebook Benchmarks**: To execute all notebook benchmarks, use the following command:
  ```bash
  nox -r -s notebook
  ```

  This command runs all the Jupyter notebooks in the repository as benchmarks.
- **Running Pure Benchmarks**: For executing more traditional benchmarks that do not involve notebooks, use:
  ```bash
  nox -r -s benchmark
  ```
  This will run all the non-notebook benchmarks specified in the repository.

- **Saving Results**: By default, when run locally, each benchmark concludes by printing a summary of the results, which are not saved automatically. To save the results to a CSV file, you can use the --output-csv or -o option followed by a specific path. If no path is specified, the results will be saved to a temporary location, and the path to this location will be printed at the end of the benchmark.
  ```bash
  nox -r -s benchmark -- --output-csv path/to/your/results.csv
  nox -r -s benchmark -- --output-csv
  ```

- **Running Multiple Iterations**: To run a benchmark multiple times and obtain an average result, use the -i or --iterations option followed by the number of iterations:
  ```bash
  nox -r -s benchmark -- --iterations 5
  ```

- **Filtering Benchmarks**: If you want to run only specific benchmarks, such as TPC-H, or specific queries within a benchmark, like tpch/q1, you can use the --benchmark-filter or -b option followed by the folder, file name, or both:
  ```bash
  # Runs all benchmarks in the 'tpch' directory
  nox -r -s benchmark -- --benchmark-filter tpch

  # Runs all benchmarks in 'db_benchmark' and specific queries q1 and q2 from TPC-H
  nox -r -s benchmark -- --benchmark-filter db_benchmark tpch/q1.py tpch/q2.py
  ```
- **Uploading Results to BigQuery**: To upload benchmark results to BigQuery, set the environment variable GCLOUD_BENCH_PUBLISH_PROJECT to the Google Cloud project where you want to store the results. This enables automatic uploading of the benchmark data to your specified project in BigQuery:
  ```bash
  export GCLOUD_BENCH_PUBLISH_PROJECT='your-google-cloud-project-id'

  # Run all non-notebook benchmarks and uploads the results to
  # your-google-cloud-project-id.benchmark_report.benchmark
  nox -r -s benchmark

  # Run all notebook benchmarks and uploads the results to
  # your-google-cloud-project-id.benchmark_report.notebook_benchmark
  nox -r -s notebook
  ```
