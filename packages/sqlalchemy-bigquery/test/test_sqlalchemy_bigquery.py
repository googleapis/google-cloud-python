from sqlalchemy.engine import create_engine
from sqlalchemy.schema import Table, MetaData, Column
from sqlalchemy import types, func, case
from sqlalchemy.sql import expression, select, literal_column
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import sessionmaker
import pytest
import sqlalchemy
import datetime


ONE_ROW_CONTENTS = [
    588,
    datetime.datetime(2013, 10, 10, 11, 27, 16, tzinfo=datetime.timezone.utc),
    'W 52 St & 11 Ave',
    40.76727216,
    False,
    datetime.date(2013, 10, 10),
    datetime.datetime(2013, 10, 10, 11, 27, 16),
    datetime.time(11, 27, 16),
    b'\xef'
]


@pytest.fixture(scope='session')
def engine():
    engine = create_engine('bigquery://', echo=True)
    return engine


@pytest.fixture(scope='session')
def table(engine):
    return Table('test_pybigquery.sample', MetaData(bind=engine), autoload=True)


@pytest.fixture(scope='session')
def table_one_row(engine):
    return Table('test_pybigquery.sample_one_row', MetaData(bind=engine), autoload=True)


@pytest.fixture(scope='session')
def session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def test_reflect_select(engine, table):
    assert len(table.c) == 9
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

    rows = table.select().execute().fetchall()
    assert len(rows) == 1000


def test_content_from_raw_queries(engine):
    rows = engine.execute('SELECT * FROM test_pybigquery.sample_one_row').fetchall()
    assert list(rows[0]) == ONE_ROW_CONTENTS


def test_content_from_reflect(engine, table_one_row):
    rows = table_one_row.select().execute().fetchall()
    assert list(rows[0]) == ONE_ROW_CONTENTS


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


def test_tables_list(engine):
    assert 'test_pybigquery.sample' in engine.table_names()
    assert 'test_pybigquery.sample_one_row' in engine.table_names()


def test_group_by(session, table):
    """labels in SELECT clause should be correclty formatted (dots are replaced with underscores)"""
    result = session.query(table.c.string, func.count(table.c.integer)).group_by(table.c.string).all()
    assert len(result) > 0


def test_session_query(session, table):
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


def test_custom_expression(engine, table):
    """GROUP BY clause should use labels instead of expressions"""

    col1 = literal_column("TIMESTAMP_TRUNC(timestamp, DAY)").label("timestamp_label")
    col2 = func.sum(table.c.integer)
    query = (
        select([
            col1,
            col2,
        ])
        .group_by(col1)
        .order_by(col2)
    )
    result = engine.execute(query).fetchone()
    assert len(result) > 0
