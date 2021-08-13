# Benchmarks

The performance test suite is located in [test/benchmark.py](https://github.com/cloudspannerecosystem/python-spanner-sqlalchemy/blob/main/test/benchmark.py) and intended to compare execution time difference between SQLAlchemy dialect for Spanner and pure Spanner client.

The test suite requirements:
- `scipy` Python package installed
- the original dialect requirements

Use `PROJECT`, `INSTANCE` and `DATABASE` module constants to set a project to execute tests on.

# 07-11-2021

|Test|mean, sec|error|std_dev|
|----|-------|-----|--------|
|SPANNER insert_one_row_with_fetch_after| 0.91|0.01|0.09|
|ALCHEMY insert_one_row_with_fetch_after|  1.07| 0.0|0.03|
|SPANNER read_one_row| 0.33| 0.0| 0.01|
|ALCHEMY read_one_row| 0.3| 0.0| 0.01|
|SPANNER insert_many_rows|  1.37| 0.02| 0.12|
|ALCHEMY insert_many_rows|  24.41| 0.07| 0.49|
|SPANNER select_many_rows| 0.31| 0.02| 0.08|
|ALCHEMY select_many_rows|   0.22| 0.03| 0.01|
|SPANNER insert_many_rows_with_mutations| 0.34| 0.0| 0.03|
|SQLALCHEMY insert_many_rows_with_mutations| 25.1| 0.03| 0.31|
