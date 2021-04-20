import mock
import pytest
import sqlalchemy

import fauxdbi


@pytest.fixture()
def faux_conn():
    with mock.patch(
        "google.cloud.bigquery.dbapi.connection.Connection", fauxdbi.Connection
    ):
        engine = sqlalchemy.create_engine("bigquery://myproject/mydataset")
        conn = engine.connect()
        yield conn
        conn.close()
