# Copyright (c) 2021 The sqlalchemy-bigquery Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import contextlib
import mock
import sqlite3

import pytest
import sqlalchemy

import fauxdbi

sqlalchemy_version_info = tuple(map(int, sqlalchemy.__version__.split(".")))
sqlalchemy_1_3_or_higher = pytest.mark.skipif(
    sqlalchemy_version_info < (1, 3), reason="requires sqlalchemy 1.3 or higher"
)
sqlalchemy_1_4_or_higher = pytest.mark.skipif(
    sqlalchemy_version_info < (1, 4), reason="requires sqlalchemy 1.4 or higher"
)
sqlalchemy_before_1_4 = pytest.mark.skipif(
    sqlalchemy_version_info >= (1, 4), reason="requires sqlalchemy 1.3 or lower"
)


@pytest.fixture()
def faux_conn():
    test_data = dict(execute=[])
    connection = sqlite3.connect(":memory:")

    def factory(*args, **kw):
        conn = fauxdbi.Connection(connection, test_data, *args, **kw)
        return conn

    with mock.patch("google.cloud.bigquery.dbapi.connection.Connection", factory):
        # We want to bypass client creation. We don't need it and it requires creds.
        with mock.patch(
            "sqlalchemy_bigquery._helpers.create_bigquery_client", fauxdbi.FauxClient
        ):
            with mock.patch("google.auth.default", return_value=("authdb", "authproj")):
                engine = sqlalchemy.create_engine("bigquery://myproject/mydataset")
                conn = engine.connect()
                conn.test_data = test_data

                def ex(sql, *args, **kw):
                    with contextlib.closing(
                        conn.connection.connection.connection.cursor()
                    ) as cursor:
                        cursor.execute(sql, *args, **kw)

                conn.ex = ex

                ex("create table comments" " (key string primary key, comment string)")

                yield conn
                conn.close()


@pytest.fixture()
def metadata():
    return sqlalchemy.MetaData()


def setup_table(connection, name, *columns, initial_data=(), **kw):
    metadata = sqlalchemy.MetaData()
    table = sqlalchemy.Table(name, metadata, *columns, **kw)
    metadata.create_all(connection.engine)
    if initial_data:
        connection.execute(table.insert(), initial_data)
    return table
