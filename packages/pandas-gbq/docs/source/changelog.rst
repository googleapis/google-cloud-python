Changelog
=========

.. _changelog-0.14.1:

0.14.1 / TBD
------------

Bug fixes
~~~~~~~~~

- Use ``object`` dtype for ``TIME`` columns. (:issue:`328`)
- Encode floating point values with greater precision. (:issue:`326`)
- Support ``INT64`` and other standard SQL aliases in
  :func:`~pandas_gbq.to_gbq` ``table_schema`` argument. (:issue:`322`)


.. _changelog-0.14.0:

0.14.0 / 2020-10-05
-------------------

- Add ``dtypes`` argument to ``read_gbq``. Use this argument to override the
  default ``dtype`` for a particular column in the query results. For
  example, this can be used to select nullable integer columns as the
  ``Int64`` nullable integer pandas extension type. (:issue:`242`,
  :issue:`332`)

.. code-block:: python

   df = gbq.read_gbq(
       "SELECT CAST(NULL AS INT64) AS null_integer",
       dtypes={"null_integer": "Int64"},
   )

Dependency updates
~~~~~~~~~~~~~~~~~~

- Support ``google-cloud-bigquery-storage`` 2.0 and higher. (:issue:`329`)
- Update the minimum version of ``pandas`` to 0.20.1.
  (:issue:`331`)

Internal changes
~~~~~~~~~~~~~~~~

- Update tests to run against Python 3.8. (:issue:`331`)


.. _changelog-0.13.3:

0.13.3 / 2020-09-30
-------------------

- Include needed "extras" from ``google-cloud-bigquery`` package as
  dependencies. Exclude incompatible 2.0 version. (:issue:`324`, :issue:`329`)

.. _changelog-0.13.2:

0.13.2 / 2020-05-14
-------------------

- Fix ``Provided Schema does not match Table`` error when the existing table
  contains required fields. (:issue:`315`)

.. _changelog-0.13.1:

0.13.1 / 2020-02-13
-------------------

- Fix ``AttributeError`` with BQ Storage API to download empty results.
  (:issue:`299`)

.. _changelog-0.13.0:

0.13.0 / 2019-12-12
-------------------

- Raise ``NotImplementedError`` when the deprecated ``private_key`` argument
  is used. (:issue:`301`)


.. _changelog-0.12.0:

0.12.0 / 2019-11-25
-------------------

- Add ``max_results`` argument to :func:`~pandas_gbq.read_gbq()`. Use this
  argument to limit the number of rows in the results DataFrame. Set
  ``max_results`` to 0 to ignore query outputs, such as for DML or DDL
  queries. (:issue:`102`)
- Add ``progress_bar_type`` argument to :func:`~pandas_gbq.read_gbq()`. Use
  this argument to display a progress bar when downloading data.
  (:issue:`182`)

Dependency updates
~~~~~~~~~~~~~~~~~~

- Update the minimum version of ``google-cloud-bigquery`` to 1.11.1.
  (:issue:`296`)

Documentation
~~~~~~~~~~~~~

- Add code samples to introduction and refactor howto guides. (:issue:`239`)


.. _changelog-0.11.0:

0.11.0 / 2019-07-29
-------------------

- **Breaking Change:** Python 2 support has been dropped. This is to align
  with the pandas package which dropped Python 2 support at the end of 2019.
  (:issue:`268`)

Enhancements
~~~~~~~~~~~~

- Ensure ``table_schema`` argument is not modified inplace. (:issue:`278`)

Implementation changes
~~~~~~~~~~~~~~~~~~~~~~

- Use object dtype for ``STRING``, ``ARRAY``, and ``STRUCT`` columns when
  there are zero rows. (:issue:`285`)

Internal changes
~~~~~~~~~~~~~~~~

- Populate ``user-agent`` with ``pandas`` version information. (:issue:`281`)
- Fix ``pytest.raises`` usage for latest pytest. Fix warnings in tests.
  (:issue:`282`)
- Update CI to install nightly packages in the conda tests. (:issue:`254`)

.. _changelog-0.10.0:

0.10.0 / 2019-04-05
-------------------

- **Breaking Change:** Default SQL dialect is now ``standard``. Use
  :attr:`pandas_gbq.context.dialect` to override the default value.
  (:issue:`195`, :issue:`245`)

Documentation
~~~~~~~~~~~~~

- Document :ref:`BigQuery data type to pandas dtype conversion
  <reading-dtypes>` for ``read_gbq``. (:issue:`269`)

Dependency updates
~~~~~~~~~~~~~~~~~~

- Update the minimum version of ``google-cloud-bigquery`` to 1.9.0.
  (:issue:`247`)
- Update the minimum version of ``pandas`` to 0.19.0. (:issue:`262`)

Internal changes
~~~~~~~~~~~~~~~~

- Update the authentication credentials. **Note:** You may need to set
  ``reauth=True`` in order to update your credentials to the most recent
  version. This is required to use new functionality such as the BigQuery
  Storage API. (:issue:`267`)
- Use ``to_dataframe()`` from ``google-cloud-bigquery`` in the ``read_gbq()``
  function. (:issue:`247`)

Enhancements
~~~~~~~~~~~~

- Fix a bug where pandas-gbq could not upload an empty DataFrame. (:issue:`237`)
- Allow ``table_schema`` in :func:`to_gbq` to contain only a subset of columns,
  with the rest being populated using the DataFrame dtypes (:issue:`218`)
  (contributed by @johnpaton)
- Read ``project_id`` in :func:`to_gbq` from provided ``credentials`` if
  available (contributed by @daureg)
- ``read_gbq`` uses the timezone-aware ``DatetimeTZDtype(unit='ns',
  tz='UTC')`` dtype for BigQuery ``TIMESTAMP`` columns. (:issue:`269`)
- Add ``use_bqstorage_api`` to :func:`read_gbq`. The BigQuery Storage API can
  be used to download large query results (>125 MB) more quickly. If the BQ
  Storage API can't be used, the BigQuery API is used instead. (:issue:`133`,
  :issue:`270`)

.. _changelog-0.9.0:

0.9.0 / 2019-01-11
------------------

- Warn when deprecated ``private_key`` parameter is used (:issue:`240`)
- **New dependency** Use the ``pydata-google-auth`` package for
  authentication. (:issue:`241`)

.. _changelog-0.8.0:

0.8.0 / 2018-11-12
------------------

Breaking changes
~~~~~~~~~~~~~~~~

- **Deprecate** ``private_key`` parameter to :func:`pandas_gbq.read_gbq` and
  :func:`pandas_gbq.to_gbq` in favor of new ``credentials`` argument. Instead,
  create a credentials object using
  :func:`google.oauth2.service_account.Credentials.from_service_account_info`
  or
  :func:`google.oauth2.service_account.Credentials.from_service_account_file`.
  See the :doc:`authentication how-to guide <howto/authentication>` for
  examples. (:issue:`161`, :issue:`231`)

Enhancements
~~~~~~~~~~~~

- Allow newlines in data passed to ``to_gbq``. (:issue:`180`)
- Add :attr:`pandas_gbq.context.dialect` to allow overriding the default SQL
  syntax dialect. (:issue:`195`, :issue:`235`)
- Support Python 3.7. (:issue:`197`, :issue:`232`)

Internal changes
~~~~~~~~~~~~~~~~

- Migrate tests to CircleCI. (:issue:`228`, :issue:`232`)

.. _changelog-0.7.0:

0.7.0 / 2018-10-19
--------------------

- `int` columns which contain `NULL` are now cast to `float`, rather than
  `object` type. (:issue:`174`)
- `DATE`, `DATETIME` and `TIMESTAMP` columns are now parsed as pandas' `timestamp`
  objects (:issue:`224`)
- Add :class:`pandas_gbq.Context` to cache credentials in-memory, across
  calls to ``read_gbq`` and ``to_gbq``. (:issue:`198`, :issue:`208`)
- Fast queries now do not log above ``DEBUG`` level. (:issue:`204`)
  With BigQuery's release of `clustering <https://cloud.google.com/bigquery/docs/clustered-tables>`__
  querying smaller samples of data is now faster and cheaper.
- Don't load credentials from disk if reauth is ``True``. (:issue:`212`)
  This fixes a bug where pandas-gbq could not refresh credentials if the
  cached credentials were invalid, revoked, or expired, even when
  ``reauth=True``.
- Catch RefreshError when trying credentials. (:issue:`226`)

Internal changes
~~~~~~~~~~~~~~~~

- Avoid listing datasets and tables in system tests. (:issue:`215`)
- Improved performance from eliminating some duplicative parsing steps
  (:issue:`224`)

.. _changelog-0.6.1:

0.6.1 / 2018-09-11
--------------------

- Improved ``read_gbq`` performance and memory consumption by delegating
  ``DataFrame`` construction to the Pandas library, radically reducing
  the number of loops that execute in python
  (:issue:`128`)
- Reduced verbosity of logging from ``read_gbq``, particularly for short
  queries. (:issue:`201`)
- Avoid ``SELECT 1`` query when running ``to_gbq``. (:issue:`202`)

.. _changelog-0.6.0:

0.6.0 / 2018-08-15
--------------------

- Warn when ``dialect`` is not passed in to ``read_gbq``. The default dialect
  will be changing from 'legacy' to 'standard' in a future version.
  (:issue:`195`)
- Use general float with 15 decimal digit precision when writing to local
  CSV buffer in ``to_gbq``. This prevents numerical overflow in certain
  edge cases. (:issue:`192`)

.. _changelog-0.5.0:

0.5.0 / 2018-06-15
------------------

- Project ID parameter is optional in ``read_gbq`` and ``to_gbq`` when it can
  inferred from the environment. Note: you must still pass in a project ID when
  using user-based authentication. (:issue:`103`)
- Progress bar added for ``to_gbq``, through an optional library `tqdm` as
  dependency. (:issue:`162`)
- Add location parameter to ``read_gbq`` and ``to_gbq`` so that pandas-gbq
  can work with datasets in the Tokyo region. (:issue:`177`)

Documentation
~~~~~~~~~~~~~

- Add :doc:`authentication how-to guide <howto/authentication>`. (:issue:`183`)
- Update :doc:`contributing` guide with new paths to tests. (:issue:`154`,
  :issue:`164`)

Internal changes
~~~~~~~~~~~~~~~~

- Tests now use `nox` to run in multiple Python environments. (:issue:`52`)
- Renamed internal modules. (:issue:`154`)
- Refactored auth to an internal auth module. (:issue:`176`)
- Add unit tests for ``get_credentials()``. (:issue:`184`)

.. _changelog-0.4.1:

0.4.1 / 2018-04-05
------------------

- Only show ``verbose`` deprecation warning if Pandas version does not
  populate it. (:issue:`157`)

.. _changelog-0.4.0:

0.4.0 / 2018-04-03
------------------

-   Fix bug in `read_gbq` when building a dataframe with integer columns
    on Windows. Explicitly use 64bit integers when converting from BQ types.
    (:issue:`119`)
-   Fix bug in `read_gbq` when querying for an array of floats (:issue:`123`)
-   Fix bug in `read_gbq` with configuration argument. Updates `read_gbq` to
    account for breaking change in the way ``google-cloud-python`` version
    0.32.0+ handles query configuration API representation. (:issue:`152`)
-   Fix bug in `to_gbq` where seconds were discarded in timestamp columns.
    (:issue:`148`)
-   Fix bug in `to_gbq` when supplying a user-defined schema (:issue:`150`)
-   **Deprecate** the ``verbose`` parameter in `read_gbq` and `to_gbq`.
    Messages use the logging module instead of printing progress directly to
    standard output. (:issue:`12`)

.. _changelog-0.3.1:

0.3.1 / 2018-02-13
------------------

- Fix an issue where Unicode couldn't be uploaded in Python 2 (:issue:`106`)
- Add support for a passed schema in :func:``to_gbq`` instead inferring the schema from the passed ``DataFrame`` with ``DataFrame.dtypes`` (:issue:`46`)
- Fix an issue where a dataframe containing both integer and floating point columns could not be uploaded with ``to_gbq`` (:issue:`116`)
- ``to_gbq`` now uses ``to_csv`` to avoid manually looping over rows in a dataframe (should result in faster table uploads) (:issue:`96`)

.. _changelog-0.3.0:

0.3.0 / 2018-01-03
------------------

- Use the `google-cloud-bigquery <https://googlecloudplatform.github.io/google-cloud-python/latest/bigquery/usage.html>`__ library for API calls. The ``google-cloud-bigquery`` package is a new dependency, and dependencies on ``google-api-python-client`` and ``httplib2`` are removed. See the `installation guide <https://pandas-gbq.readthedocs.io/en/latest/install.html#dependencies>`__ for more details.  (:issue:`93`)
- Structs and arrays are now named properly (:issue:`23`) and BigQuery functions like ``array_agg`` no longer run into errors during type conversion (:issue:`22`).
- :func:`to_gbq` now uses a load job instead of the streaming API. Remove ``StreamingInsertError`` class, as it is no longer used by :func:`to_gbq`. (:issue:`7`, :issue:`75`)

.. _changelog-0.2.1:

0.2.1 / 2017-11-27
------------------

- :func:`read_gbq` now raises ``QueryTimeout`` if the request exceeds the ``query.timeoutMs`` value specified in the BigQuery configuration. (:issue:`76`)
- Environment variable ``PANDAS_GBQ_CREDENTIALS_FILE`` can now be used to override the default location where the BigQuery user account credentials are stored. (:issue:`86`)
- BigQuery user account credentials are now stored in an application-specific hidden user folder on the operating system. (:issue:`41`)

.. _changelog-0.2.0:

0.2.0 / 2017-07-24
------------------

- Drop support for Python 3.4 (:issue:`40`)
- The dataframe passed to ```.to_gbq(...., if_exists='append')``` needs to contain only a subset of the fields in the BigQuery schema. (:issue:`24`)
- Use the `google-auth <https://google-auth.readthedocs.io/en/latest/>`__ library for authentication because ``oauth2client`` is deprecated. (:issue:`39`)
- :func:`read_gbq` now has a ``auth_local_webserver`` boolean argument for controlling whether to use web server or console flow when getting user credentials. Replaces `--noauth_local_webserver` command line argument. (:issue:`35`)
- :func:`read_gbq` now displays the BigQuery Job ID and standard price in verbose output. (:issue:`70` and :issue:`71`)

.. _changelog-0.1.6:

0.1.6 / 2017-05-03
------------------

- All gbq errors will simply be subclasses of ``ValueError`` and no longer inherit from the deprecated ``PandasError``.

.. _changelog-0.1.4:

0.1.4 / 2017-03-17
------------------

- ``InvalidIndexColumn`` will be raised instead of ``InvalidColumnOrder`` in :func:`read_gbq` when the index column specified does not exist in the BigQuery schema. (:issue:`6`)

.. _changelog-0.1.3:

0.1.3 / 2017-03-04
------------------

- Bug with appending to a BigQuery table where fields have modes (NULLABLE,REQUIRED,REPEATED) specified. These modes were compared versus the remote schema and writing a table via :func:`to_gbq` would previously raise. (:issue:`13`)

.. _changelog-0.1.2:

0.1.2 / 2017-02-23
------------------

Initial release of transfered code from `pandas <https://github.com/pandas-dev/pandas>`__

Includes patches since the 0.19.2 release on pandas with the following:

- :func:`read_gbq` now allows query configuration preferences `pandas-GH#14742 <https://github.com/pandas-dev/pandas/pull/14742>`__
- :func:`read_gbq` now stores ``INTEGER`` columns as ``dtype=object`` if they contain ``NULL`` values. Otherwise they are stored as ``int64``. This prevents precision lost for integers greather than 2**53. Furthermore ``FLOAT`` columns with values above 10**4 are no longer casted to ``int64`` which also caused precision loss `pandas-GH#14064 <https://github.com/pandas-dev/pandas/pull/14064>`__, and `pandas-GH#14305 <https://github.com/pandas-dev/pandas/pull/14305>`__
