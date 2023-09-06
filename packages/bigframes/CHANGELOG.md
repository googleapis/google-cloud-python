# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/bigframes/#history

## [0.3.2](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.3.1...v0.3.2) (2023-09-06)


### Bug Fixes

* Make release.sh script for PyPI upload executable ([#20](https://github.com/googleapis/python-bigquery-dataframes/issues/20)) ([9951610](https://github.com/googleapis/python-bigquery-dataframes/commit/995161068b118a639903878acfde3202087c25f8))

## [0.3.1](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.3.0...v0.3.1) (2023-09-05)


### Bug Fixes

* **release:** Use correct directory name for release build config ([#17](https://github.com/googleapis/python-bigquery-dataframes/issues/17)) ([3dd25b3](https://github.com/googleapis/python-bigquery-dataframes/commit/3dd25b379ed832ea062e188f483d2789830de67b))

## [0.3.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.2.0...v0.3.0) (2023-09-02)


### Features

* Add `bigframes.get_global_session()` and `bigframes.reset_session()` aliases ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Add `bigframes.pandas.read_pickle` function ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Add `components_`, `explained_variance_`, and `explained_variance_ratio_` properties to `bigframes.ml.decomposition.PCA` ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Add `fit_transform` to `bigquery.ml` transformers ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Add `Series.dropna` and `DataFrame.fillna` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Add `Series.str` methods `isalpha`, `isdigit`, `isdecimal`, `isalnum`, `isspace`, `islower`, `isupper`, `zfill`, `center` ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Support `bigframes.pandas.merge()` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support `DataFrame.isin` with list and dict inputs ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support `DataFrame.pivot` ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Support `DataFrame.stack` ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Support `DataFrame`-`DataFrame` binary operations ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support `df[my_column] = [a python list]` ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Support `Index.is_monotonic` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support `np.arcsin`, `np.arccos`, `np.arctan`, `np.sinh`, `np.cosh`, `np.tanh`, `np.arcsinh`, `np.arccosh`, `np.arctanh`, `np.exp` with Series argument ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Support `np.sin`, `np.cos`, `np.tan`, `np.log`, `np.log10`, `np.sqrt`, `np.abs` with Series argument ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Support `pow()` and power operator in `DataFrame` and `Series` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support `read_json` with `engine=bigquery` for newline-delimited JSON files ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Support `Series.corr` ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Support `Series.map` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support for `np.add`, `np.subtract`, `np.multiply`, `np.divide`, `np.power` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support MultiIndex for DataFrame columns ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Use `pandas.Index` for column labels ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Use default session and connection in `ml.llm` and `ml.imported` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))


### Bug Fixes

* Add error message to `set_index` ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Align column names with pandas in `DataFrame.agg` results ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Allow (but still not recommended) `ORDER BY` in `read_gbq` input when an `index_col` is defined ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Check for IAM role on the BigQuery connection when initializing a `remote_function` ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Check that types are specified in `read_gbq_function` ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Don't use query cache for Session construction ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Include survey link in abstract `NotImplementedError` exception messages ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Label temp table creation jobs with `source=bigquery-dataframes-temp` label ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Make `X_train` argument names consistent across methods ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Raise AttributeError for unimplemented pandas methods ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Raise exception for invalid function in `read_gbq_function` ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Support spaces in column names in `DataFrame` initializater ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))


### Performance Improvements

* Add local cache for `__repr_*__` methods ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Lazily instantiate client library objects ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Use `row_number()` filter for `head` / `tail` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))


### Documentation

* Add ML section under Overview ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Add release status to table of contents ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Add samples and best practices to `read_gbq` docs ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Correct the return types of Dataframe and Series ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Create subfolders for notebooks ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Fix link to GitHub ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Highlight bigframes is open-source ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Sample ML Drug Name Generation notebook ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Set `options.bigquery.project` in sample code ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Transform remote function user guide into sample code ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Update remote function notebook with read_gbq_function usage ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))

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
