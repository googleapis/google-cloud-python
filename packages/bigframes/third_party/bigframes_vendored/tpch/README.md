polars-tpch
===========

This repo contains the code used for performance evaluation of polars. The benchmarks are TPC-standardised queries and data designed to test the performance of "real" workflows.

From the [TPC website](https://www.tpc.org/tpch/):
> TPC-H is a decision support benchmark. It consists of a suite of business-oriented ad hoc queries and concurrent data modifications. The queries and the data populating the database have been chosen to have broad industry-wide relevance. This benchmark illustrates decision support systems that examine large volumes of data, execute queries with a high degree of complexity, and give answers to critical business questions.

## Generating TPC-H Data

### Project setup

```shell
# clone this repository
git clone https://github.com/pola-rs/tpch.git
cd tpch/tpch-dbgen

# build tpch-dbgen
make
```

### Execute

```shell
# change directory to the root of the repository
cd ../
./run.sh
```

This will do the following,

- Create a new virtual environment with all required dependencies.
- Generate data for benchmarks.
- Run the benchmark suite.
