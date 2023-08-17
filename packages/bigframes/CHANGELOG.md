# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/bigframes/#history

## 0.2.0 (2023-08-17)

### Features
* Add KMeans.cluster_centers_.
* Allow column labels to be any type handled by bq df, column labels can be integers now.
* Add dataframegroupby.agg().
* Add Series Property is_monotonic_increasing and is_monotonic_decreasing.
* Add match, fullmatch, get, pad str methods.
* Add series isin function.

### Bug Fixes
* Update ML package to use sessions for queries.
* Optimize `read_gbq` with `index_col` set to cluster by `index_col`.
* Raise ValueError if the location mismatched.
* `read_gbq` no longer uses 'time travel' with query inputs.

### Documentation
* Add docstring to _uniform_sampling to avoid user using it.

## 0.1.1 (2023-08-14)

### Documentation

* Correct link to code repository in `setup.py` and use correct terminology for
  `console.cloud.google.com` links.

## 0.1.0 (2023-08-11)

### Features

* Add `bigframes.pandas` package with an API compatible with
  [pandas](https://pandas.pydata.org/). Supported data sources include:
  BigQuery SQL queries, BigQuery tables, CSV (local and GCS), Parquet (local
  and Cloud Storage), and more.
* Add `bigframes.ml` package with an API inspired by
  [scikit-learn](https://scikit-learn.org/stable/). Train machine learning
  models and run batch predicition, powered by [BigQuery
  ML](https://cloud.google.com/bigquery/docs/bqml-introduction).

## [0.0.0](https://pypi.org/project/bigframes/0.0.0/) (2023-02-22)

* Empty package to reserve package name.
