# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from google.api_core.exceptions import BadRequest
from pybigquery.api import ApiClient
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import Table, MetaData, Column
from sqlalchemy import types, func, case, inspect
from sqlalchemy.sql import expression, select, literal_column
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import sessionmaker
from pytz import timezone
import pytest
import sqlalchemy
import datetime


ONE_ROW_CONTENTS_EXPANDED = [
    588,
    datetime.datetime(2013, 10, 10, 11, 27, 16, tzinfo=timezone('UTC')),
    'W 52 St & 11 Ave',
    40.76727216,
    False,
    datetime.date(2013, 10, 10),
    datetime.datetime(2013, 10, 10, 11, 27, 16),
    datetime.time(11, 27, 16),
    b'\xef',
    {u'age': 100, u'name': u'John Doe'},
    'John Doe',
    100,
    {u'record': {u'age': 200, u'name': u'John Doe 2'}}, {u'age': 200, u'name': u'John Doe 2'},
    'John Doe 2',
    200,
    [1, 2, 3],
]

ONE_ROW_CONTENTS = [
    588,
    datetime.datetime(2013, 10, 10, 11, 27, 16, tzinfo=timezone('UTC')),
    'W 52 St & 11 Ave',
    40.76727216,
    False,
    datetime.date(2013, 10, 10),
    datetime.datetime(2013, 10, 10, 11, 27, 16),
    datetime.time(11, 27, 16),
    b'\xef',
    {
        'name': 'John Doe',
        'age': 100,
    },
    {
        'record': {
            'name': 'John Doe 2',
            'age': 200,
        }
    },
    [1, 2, 3],
]

ONE_ROW_CONTENTS_DML = [
    588,
    datetime.datetime(2013, 10, 10, 11, 27, 16, tzinfo=timezone('UTC')),
    'test',
    40.76727216,
    False,
    datetime.date(2013, 10, 10),
    datetime.datetime(2013, 10, 10, 11, 27, 16),
    datetime.time(11, 27, 16),
    'test_bytes'
]

SAMPLE_COLUMNS = [
    {'name': 'integer', 'type': types.Integer(), 'nullable': True, 'default': None},
    {'name': 'timestamp', 'type': types.TIMESTAMP(), 'nullable': True, 'default': None},
    {'name': 'string', 'type': types.String(), 'nullable': True, 'default': None},
    {'name': 'float', 'type': types.Float(), 'nullable': True, 'default': None},
    {'name': 'boolean', 'type': types.Boolean(), 'nullable': True, 'default': None},
    {'name': 'date', 'type': types.DATE(), 'nullable': True, 'default': None},
    {'name': 'datetime', 'type': types.DATETIME(), 'nullable': True, 'default': None},
    {'name': 'time', 'type': types.TIME(), 'nullable': True, 'default': None},
    {'name': 'bytes', 'type': types.BINARY(), 'nullable': True, 'default': None},
    {'name': 'record', 'type': types.JSON(), 'nullable': True, 'default': None},
    {'name': 'record.name', 'type': types.String(), 'nullable': True, 'default': None},
    {'name': 'record.age', 'type': types.Integer(), 'nullable': True, 'default': None},
    {'name': 'nested_record', 'type': types.JSON(), 'nullable': True, 'default': None},
    {'name': 'nested_record.record', 'type': types.JSON(), 'nullable': True, 'default': None},
    {'name': 'nested_record.record.name', 'type': types.String(), 'nullable': True, 'default': None},
    {'name': 'nested_record.record.age', 'type': types.Integer(), 'nullable': True, 'default': None},
    {'name': 'array', 'type': types.ARRAY(types.Integer()), 'nullable': True, 'default': None},
]


@pytest.fixture(scope='session')
def engine():
    engine = create_engine('bigquery://', echo=True)
    return engine


@pytest.fixture(scope='session')
def engine_using_test_dataset():
    engine = create_engine('bigquery:///test_pybigquery', echo=True)
    return engine


@pytest.fixture(scope='session')
def engine_with_location():
    engine = create_engine('bigquery://', echo=True, location="asia-northeast1")
    return engine


@pytest.fixture(scope='session')
def table(engine):
    return Table('test_pybigquery.sample', MetaData(bind=engine), autoload=True)


@pytest.fixture(scope='session')
def table_using_test_dataset(engine_using_test_dataset):
    return Table('sample', MetaData(bind=engine_using_test_dataset), autoload=True)


@pytest.fixture(scope='session')
def table_one_row(engine):
    return Table('test_pybigquery.sample_one_row', MetaData(bind=engine), autoload=True)


@pytest.fixture(scope='session')
def table_dml(engine):
    return Table('test_pybigquery.sample_dml', MetaData(bind=engine), autoload=True)


@pytest.fixture(scope='session')
def session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


@pytest.fixture(scope='session')
def session_using_test_dataset(engine_using_test_dataset):
    Session = sessionmaker(bind=engine_using_test_dataset)
    session = Session()
    return session


@pytest.fixture(scope='session')
def inspector(engine):
    return inspect(engine)

@pytest.fixture(scope='session')
def inspector_using_test_dataset(engine_using_test_dataset):
    return inspect(engine_using_test_dataset)


@pytest.fixture(scope='session')
def query():
    def query(table):
        col1 = literal_column("TIMESTAMP_TRUNC(timestamp, DAY)").label("timestamp_label")
        col2 = func.sum(table.c.integer)
        query = (
            select([
                col1,
                col2,
            ])
            .where(col1 < '2017-01-01 00:00:00')
            .group_by(col1)
            .order_by(col2)
        )
        return query
    return query


@pytest.fixture(scope='session')
def api_client():
    return ApiClient()


def test_dry_run(engine, api_client):
    sql = 'SELECT * FROM test_pybigquery.sample_one_row'
    assert api_client.dry_run_query(sql).total_bytes_processed == 132

    sql = 'SELECT * FROM sample_one_row'
    with pytest.raises(BadRequest) as excinfo:
        api_client.dry_run_query(sql)

    assert 'Table name "sample_one_row" cannot be resolved: dataset name is missing.' in str(excinfo.value.message)


def test_engine_with_dataset(engine_using_test_dataset):
    rows = engine_using_test_dataset.execute('SELECT * FROM sample_one_row').fetchall()
    assert list(rows[0]) == ONE_ROW_CONTENTS

    table_one_row = Table('sample_one_row', MetaData(bind=engine_using_test_dataset), autoload=True)
    rows = table_one_row.select().execute().fetchall()
    assert list(rows[0]) == ONE_ROW_CONTENTS_EXPANDED

    # Table name shouldn't include dataset
    with pytest.raises(Exception):
        table_one_row = Table('test_pybigquery.sample_one_row', MetaData(bind=engine_using_test_dataset), autoload=True)


def test_dataset_location(engine_with_location):
    rows = engine_with_location.execute('SELECT * FROM test_pybigquery_location.sample_one_row').fetchall()
    assert list(rows[0]) == ONE_ROW_CONTENTS


def test_reflect_select(table, table_using_test_dataset):
    for table in [table, table_using_test_dataset]:
        assert len(table.c) == 17

        assert isinstance(table.c.integer, Column)
        assert isinstance(table.c.integer.type, types.Integer)
        assert isinstance(table.c.timestamp.type, types.TIMESTAMP)
        assert isinstance(table.c.string.type, types.String)
        assert isinstance(table.c.float.type, types.Float)
        assert isinstance(table.c.boolean.type, types.Boolean)
        assert isinstance(table.c.date.type, types.DATE)
        assert isinstance(table.c.datetime.type, types.DATETIME)
        assert isinstance(table.c.time.type, types.TIME)
        assert isinstance(table.c.bytes.type, types.BINARY)
        assert isinstance(table.c['record.age'].type, types.Integer)
        assert isinstance(table.c['record.name'].type, types.String)
        assert isinstance(table.c['nested_record.record.age'].type, types.Integer)
        assert isinstance(table.c['nested_record.record.name'].type, types.String)
        assert isinstance(table.c.array.type, types.ARRAY)

        rows = table.select().execute().fetchall()
        assert len(rows) == 1000


def test_content_from_raw_queries(engine):
    rows = engine.execute('SELECT * FROM test_pybigquery.sample_one_row').fetchall()
    assert list(rows[0]) == ONE_ROW_CONTENTS


def test_record_content_from_raw_queries(engine):
    rows = engine.execute('SELECT record.name FROM test_pybigquery.sample_one_row').fetchall()
    assert rows[0][0] == 'John Doe'


def test_content_from_reflect(engine, table_one_row):
    rows = table_one_row.select().execute().fetchall()
    assert list(rows[0]) == ONE_ROW_CONTENTS_EXPANDED


def test_unicode(engine, table_one_row):
    unicode_str = "白人看不懂"
    returned_str = sqlalchemy.select(
        [expression.bindparam("好", unicode_str)],
        from_obj=table_one_row,
    ).scalar()
    assert returned_str == unicode_str


def test_reflect_select_shared_table(engine):
    one_row = Table('bigquery-public-data.samples.natality', MetaData(bind=engine), autoload=True)
    row = one_row.select().limit(1).execute().first()
    assert len(row) >= 1


def test_reflect_table_does_not_exist(engine):
    with pytest.raises(NoSuchTableError):
        table = Table('test_pybigquery.table_does_not_exist', MetaData(bind=engine), autoload=True)

    assert Table('test_pybigquery.table_does_not_exist', MetaData(bind=engine)).exists() is False


def test_reflect_dataset_does_not_exist(engine):
    with pytest.raises(NoSuchTableError):
        Table('dataset_does_not_exist.table_does_not_exist', MetaData(bind=engine), autoload=True)


def test_tables_list(engine, engine_using_test_dataset):
    tables = engine.table_names()
    assert 'test_pybigquery.sample' in tables
    assert 'test_pybigquery.sample_one_row' in tables
    assert 'test_pybigquery.sample_dml' in tables

    tables = engine_using_test_dataset.table_names()
    assert 'sample' in tables
    assert 'sample_one_row' in tables
    assert 'sample_dml' in tables


def test_group_by(session, table, session_using_test_dataset, table_using_test_dataset):
    """labels in SELECT clause should be correclty formatted (dots are replaced with underscores)"""
    for session, table in [(session, table), (session_using_test_dataset, table_using_test_dataset)]:
        result = session.query(table.c.string, func.count(table.c.integer)).group_by(table.c.string).all()
    assert len(result) > 0


def test_session_query(session, table, session_using_test_dataset, table_using_test_dataset):
    for session, table in [(session, table), (session_using_test_dataset, table_using_test_dataset)]:
        col_concat = func.concat(table.c.string).label('concat')
        result = (
            session
            .query(
                table.c.string,
                col_concat,
                func.avg(table.c.integer),
                func.sum(case([(table.c.boolean == True, 1)], else_=0))
            )
            .group_by(table.c.string, col_concat)
            .having(func.avg(table.c.integer) > 10)

        ).all()
        assert len(result) > 0


def test_labels(session, table, session_using_test_dataset, table_using_test_dataset):
    for session, table in [(session, table), (session_using_test_dataset, table_using_test_dataset)]:
        result = (
            session
            .query(
                # Valid
                table.c.string.label('abc'),
                # Invalid, needs to start with underscore
                table.c.string.label('123'),
                # Valid
                table.c.string.label('_123abc'),
                # Invalid, contains illegal characters
                table.c.string.label('!@#$%^&*()~`'),
            )
        )
        result = result.all()
        assert len(result) > 0


def test_custom_expression(engine, engine_using_test_dataset, table, table_using_test_dataset, query):
    """GROUP BY clause should use labels instead of expressions"""
    q = query(table)
    result = engine.execute(q).fetchall()
    assert len(result) > 0

    q = query(table_using_test_dataset)
    result = engine_using_test_dataset.execute(q).fetchall()

    assert len(result) > 0


def test_compiled_query_literal_binds(engine, engine_using_test_dataset, table, table_using_test_dataset, query):
    q = query(table)
    compiled = q.compile(engine, compile_kwargs={"literal_binds": True})
    result = engine.execute(compiled).fetchall()
    assert len(result) > 0

    q = query(table_using_test_dataset)
    compiled = q.compile(engine_using_test_dataset, compile_kwargs={"literal_binds": True})
    result = engine_using_test_dataset.execute(compiled).fetchall()
    assert len(result) > 0


def test_joins(session, table, table_one_row):
    result = (session.query(table.c.string, func.count(table_one_row.c.integer))
                     .join(table_one_row, table_one_row.c.string == table.c.string)
                     .group_by(table.c.string).all())

    assert len(result) > 0


def test_querying_wildcard_tables(engine):
    table = Table('bigquery-public-data.noaa_gsod.gsod*', MetaData(bind=engine), autoload=True)
    rows = table.select().limit(1).execute().first()
    assert len(rows) > 0


def test_dml(engine, session, table_dml):
    # test insert
    engine.execute(table_dml.insert(ONE_ROW_CONTENTS_DML))
    result = table_dml.select().execute().fetchall()
    assert len(result) == 1

    # test update
    session.query(table_dml)\
        .filter(table_dml.c.string == 'test')\
        .update({'string': 'updated_row'}, synchronize_session=False)
    updated_result = table_dml.select().execute().fetchone()
    assert updated_result['test_pybigquery.sample_dml_string'] == 'updated_row'

    # test delete
    session.query(table_dml).filter(table_dml.c.string == 'updated_row').delete(synchronize_session=False)
    result = table_dml.select().execute().fetchall()
    assert len(result) == 0


def test_schemas_names(inspector, inspector_using_test_dataset):
    datasets = inspector.get_schema_names()
    assert 'test_pybigquery' in datasets

    datasets = inspector_using_test_dataset.get_schema_names()
    assert 'test_pybigquery' in datasets


def test_table_names_in_schema(inspector, inspector_using_test_dataset):
    tables = inspector.get_table_names('test_pybigquery')
    assert 'test_pybigquery.sample' in tables
    assert 'test_pybigquery.sample_one_row' in tables
    assert 'test_pybigquery.sample_dml' in tables
    assert len(tables) == 3

    tables = inspector_using_test_dataset.get_table_names()
    assert 'sample' in tables
    assert 'sample_one_row' in tables
    assert 'sample_dml' in tables
    assert len(tables) == 3


def test_get_columns(inspector, inspector_using_test_dataset):
    columns_without_schema = inspector.get_columns('test_pybigquery.sample')
    columns_schema = inspector.get_columns('sample', 'test_pybigquery')
    columns_queries = [columns_without_schema, columns_schema]
    for columns in columns_queries:
        for i, col in enumerate(columns):
            sample_col = SAMPLE_COLUMNS[i]
            assert col['name'] == sample_col['name']
            assert col['nullable'] == sample_col['nullable']
            assert col['default'] == sample_col['default']
            assert col['type'].__class__.__name__ == sample_col['type'].__class__.__name__

    columns_without_schema = inspector_using_test_dataset.get_columns('sample')
    columns_schema = inspector_using_test_dataset.get_columns('sample', 'test_pybigquery')
    columns_queries = [columns_without_schema, columns_schema]
    for columns in columns_queries:
        for i, col in enumerate(columns):
            sample_col = SAMPLE_COLUMNS[i]
            assert col['name'] == sample_col['name']
            assert col['nullable'] == sample_col['nullable']
            assert col['default'] == sample_col['default']
            assert col['type'].__class__.__name__ == sample_col['type'].__class__.__name__


def test_has_table(engine, engine_using_test_dataset):
    assert engine.has_table('sample', 'test_pybigquery') is True
    assert engine.has_table('test_pybigquery.sample') is True

    assert engine_using_test_dataset.has_table('sample') is True
    with pytest.raises(Exception):
        assert engine_using_test_dataset.has_table('test_pybigquery.sample') is True
