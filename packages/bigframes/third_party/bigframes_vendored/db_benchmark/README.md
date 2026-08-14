Repository for reproducible benchmarking of database-like operations in single-node environment.
Benchmark report is available at [h2oai.github.io/db-benchmark](https://h2oai.github.io/db-benchmark).
We focused mainly on portability and reproducibility. Benchmark is routinely re-run to present up-to-date timings. Most of solutions used are automatically upgraded to their stable or development versions.
This benchmark is meant to compare scalability both in data volume and data complexity.
Contribution and feedback are very welcome!

# Tasks

  - [x] groupby
  - [x] join
  - [x] groupby2014

# Solutions

  - [x] [dask](https://github.com/dask/dask)
  - [x] [data.table](https://github.com/Rdatatable/data.table)
  - [x] [dplyr](https://github.com/tidyverse/dplyr)
  - [x] [DataFrames.jl](https://github.com/JuliaData/DataFrames.jl)
  - [x] [pandas](https://github.com/pandas-dev/pandas)
  - [x] [(py)datatable](https://github.com/h2oai/datatable)
  - [x] [spark](https://github.com/apache/spark)
  - [x] [cuDF](https://github.com/rapidsai/cudf)
  - [x] [ClickHouse](https://github.com/yandex/ClickHouse)
  - [x] [Polars](https://github.com/ritchie46/polars)
  - [x] [Arrow](https://github.com/apache/arrow)
  - [x] [DuckDB](https://github.com/duckdb/duckdb)

More solutions has been proposed. Status of those can be tracked in issues tracker of our project repository by using [_new solution_](https://github.com/h2oai/db-benchmark/issues?q=is%3Aissue+is%3Aopen+label%3A%22new+solution%22) label.

# Reproduce

## Batch benchmark run

- edit `path.env` and set `julia` and `java` paths
- if solution uses python create new `virtualenv` as `$solution/py-$solution`, example for `pandas` use `virtualenv pandas/py-pandas --python=/usr/bin/python3.6`
- install every solution, follow `$solution/setup-$solution.sh` scripts
- edit `run.conf` to define solutions and tasks to benchmark
- generate data, for `groupby` use `Rscript _data/groupby-datagen.R 1e7 1e2 0 0` to create `G1_1e7_1e2_0_0.csv`, re-save to binary format where needed (see below), create `data` directory and keep all data files there
- edit `_control/data.csv` to define data sizes to benchmark using `active` flag
- ensure SWAP is disabled and ClickHouse server is not yet running
- start benchmark with `./run.sh`

## Single solution benchmark

- install solution software
  - for python we recommend to use `virtualenv` for better isolation
  - for R ensure that library is installed in a solution subdirectory, so that `library("dplyr", lib.loc="./dplyr/r-dplyr")` or `library("data.table", lib.loc="./datatable/r-datatable")` works
  - note that some solutions may require another to be installed to speed-up csv data load, for example, `dplyr` requires `data.table` and similarly `pandas` requires (py)`datatable`
- generate data using `_data/*-datagen.R` scripts, for example, `Rscript _data/groupby-datagen.R 1e7 1e2 0 0` creates `G1_1e7_1e2_0_0.csv`, put data files in `data` directory
- run benchmark for a single solution using `./_launcher/solution.R --solution=data.table --task=groupby --nrow=1e7`
- run other data cases by passing extra parameters `--k=1e2 --na=0 --sort=0`
- use `--quiet=true` to suppress script's output and print timings only, using `--print=question,run,time_sec` specify columns to be printed to console, to print all use `--print=*`
- use `--out=time.csv` to write timings to a file rather than console

## Running script interactively

- install software in expected location, details above
- ensure data name to be used in env var below is present in `./data` dir
- source python virtual environment if needed
- call `SRC_DATANAME=G1_1e7_1e2_0_0 R`, if desired replace `R` with `python` or `julia`
- proceed pasting code from benchmark script

## Extra care needed

- `cudf` uses `conda` instead of `virtualenv`

# Example environment

- setting up r3-8xlarge: 244GB RAM, 32 cores: [Amazon EC2 for beginners](https://github.com/Rdatatable/data.table/wiki/Amazon-EC2-for-beginners)
- (slightly outdated) full reproduce script on clean Ubuntu 16.04: [_utils/repro.sh](https://github.com/h2oai/db-benchmark/blob/master/_utils/repro.sh)

# Acknowledgment

Timings for some solutions might be missing for particular data sizes or questions. Some functions are not yet implemented in all solutions so we were unable to answer all questions in all solutions. Some solutions might also run out of memory when running benchmark script which results the process to be killed by OS. Lastly we also added timeout for single benchmark script to run, once timeout value is reached script is terminated.
Please check [_exceptions_](https://github.com/h2oai/db-benchmark/issues?q=is%3Aissue+is%3Aopen+label%3Aexceptions) label in our repository for a list of issues/defects in solutions, that makes us unable to provide all timings.
There is also [_no documentation_](https://github.com/h2oai/db-benchmark/labels/no%20documentation) label that lists issues that are blocked by missing documentation in solutions we are benchmarking.
