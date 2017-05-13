Changelog
=========

0.1.7 / 2017-??-??
------------------

- Resolve issue where the optional ``--noauth_local_webserver`` command line argument would not be propagated during the authentication process.

0.1.6 / 2017-05-03
------------------

- All gbq errors will simply be subclasses of ``ValueError`` and no longer inherit from the deprecated ``PandasError``.

0.1.4 / 2017-03-17
------------------

- ``InvalidIndexColumn`` will be raised instead of ``InvalidColumnOrder`` in ``read_gbq`` when the index column specified does not exist in the BigQuery schema. :issue:`6`

0.1.3 / 2017-03-04
------------------

- Bug with appending to a BigQuery table where fields have modes (NULLABLE,REQUIRED,REPEATED) specified. These modes were compared versus the remote schema and writing a table via ``to_gbq`` would previously raise. :issue:`13`

0.1.2 / 2017-02-23
------------------

Initial release of transfered code from `pandas <https://github.com/pandas-dev/pandas>`__

Includes patches since the 0.19.2 release on pandas with the following:

- ``read_gbq`` now allows query configuration preferences `pandas-GH#14742 <https://github.com/pandas-dev/pandas/pull/14742>`__
- ``read_gbq`` now stores ``INTEGER`` columns as ``dtype=object`` if they contain ``NULL`` values. Otherwise they are stored as ``int64``. This prevents precision lost for integers greather than 2**53. Furthermore ``FLOAT`` columns with values above 10**4 are no longer casted to ``int64`` which also caused precision loss `pandas-GH#14064 <https://github.com/pandas-dev/pandas/pull/14064>`__, and `pandas-GH#14305 <https://github.com/pandas-dev/pandas/pull/14305>`__
