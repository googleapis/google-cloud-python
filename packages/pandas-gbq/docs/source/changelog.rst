Changelog
=========

.. _changelog-0.7.0:

0.7.0 / [unreleased]
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
