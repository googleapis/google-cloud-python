Changelog
=========

0.3.0 / 2017-??-??
------------------

- Use the `google-cloud-bigquery <https://googlecloudplatform.github.io/google-cloud-python/latest/bigquery/usage.html>`__ library for API calls. The ``google-cloud-bigquery`` package is a new dependency, and dependencies on ``google-api-python-client`` and ``httplib2`` are removed. See the `installation guide <https://pandas-gbq.readthedocs.io/en/latest/install.html#dependencies>`__ for more details.  (:issue:`93`)
- :func:`to_gbq` now uses a load job instead of the streaming API. Remove ``StreamingInsertError`` class, as it is no longer used by :func:`to_gbq`. (:issue:`7`, :issue:`75`)

0.2.1 / 2017-11-27
------------------

- :func:`read_gbq` now raises ``QueryTimeout`` if the request exceeds the ``query.timeoutMs`` value specified in the BigQuery configuration. (:issue:`76`)
- Environment variable ``PANDAS_GBQ_CREDENTIALS_FILE`` can now be used to override the default location where the BigQuery user account credentials are stored. (:issue:`86`)
- BigQuery user account credentials are now stored in an application-specific hidden user folder on the operating system. (:issue:`41`)

0.2.0 / 2017-07-24
------------------

- Drop support for Python 3.4 (:issue:`40`)
- The dataframe passed to ```.to_gbq(...., if_exists='append')``` needs to contain only a subset of the fields in the BigQuery schema. (:issue:`24`)
- Use the `google-auth <https://google-auth.readthedocs.io/en/latest/>`__ library for authentication because ``oauth2client`` is deprecated. (:issue:`39`)
- :func:`read_gbq` now has a ``auth_local_webserver`` boolean argument for controlling whether to use web server or console flow when getting user credentials. Replaces `--noauth_local_webserver` command line argument. (:issue:`35`)
- :func:`read_gbq` now displays the BigQuery Job ID and standard price in verbose output. (:issue:`70` and :issue:`71`)

0.1.6 / 2017-05-03
------------------

- All gbq errors will simply be subclasses of ``ValueError`` and no longer inherit from the deprecated ``PandasError``.

0.1.4 / 2017-03-17
------------------

- ``InvalidIndexColumn`` will be raised instead of ``InvalidColumnOrder`` in :func:`read_gbq` when the index column specified does not exist in the BigQuery schema. (:issue:`6`)

0.1.3 / 2017-03-04
------------------

- Bug with appending to a BigQuery table where fields have modes (NULLABLE,REQUIRED,REPEATED) specified. These modes were compared versus the remote schema and writing a table via :func:`to_gbq` would previously raise. (:issue:`13`)

0.1.2 / 2017-02-23
------------------

Initial release of transfered code from `pandas <https://github.com/pandas-dev/pandas>`__

Includes patches since the 0.19.2 release on pandas with the following:

- :func:`read_gbq` now allows query configuration preferences `pandas-GH#14742 <https://github.com/pandas-dev/pandas/pull/14742>`__
- :func:`read_gbq` now stores ``INTEGER`` columns as ``dtype=object`` if they contain ``NULL`` values. Otherwise they are stored as ``int64``. This prevents precision lost for integers greather than 2**53. Furthermore ``FLOAT`` columns with values above 10**4 are no longer casted to ``int64`` which also caused precision loss `pandas-GH#14064 <https://github.com/pandas-dev/pandas/pull/14064>`__, and `pandas-GH#14305 <https://github.com/pandas-dev/pandas/pull/14305>`__
