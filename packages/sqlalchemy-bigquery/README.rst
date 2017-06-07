DB-API interface and SQLAlchemy dialect for BigQuery. Inspired by `PyHive <https://github.com/dropbox/PyHive/>`_.


Usage
=====

DB-API
------
.. code-block:: python

    import bigquery
    cursor = bigquery.connect('project').cursor()
    cursor.execute('SELECT * FROM dataset.table LIMIT 10')
    print(cursor.fetchone())
    print(cursor.fetchall())

SQLAlchemy
----------
.. code-block:: python

    from sqlalchemy import *
    from sqlalchemy.engine import create_engine
    from sqlalchemy.schema import *
    engine = create_engine('bigquery://project')
    logs = Table('dataset.table', MetaData(bind=engine), autoload=True)
    print(select([func.count('*')], from_obj=logs).scalar())

Requirements
============

Install using

- ``pip install git+https://github.com/mxmzdlv/pybigquery.git@master#egg=pybigquery``

TODO
====

- Support for Record column type
- Add a test suite
