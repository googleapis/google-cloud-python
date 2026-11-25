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

import pickle

import pytest
import sqlalchemy

from .conftest import sqlalchemy_2_0_or_higher, sqlalchemy_before_2_0


def test_engine_dataset_but_no_project(faux_conn):
    engine = sqlalchemy.create_engine("bigquery:///foo")
    conn = engine.connect()
    assert conn.connection._client.project == "authproj"


def test_engine_dataset_with_billing_project(faux_conn):
    engine = sqlalchemy.create_engine("bigquery://foo", billing_project_id="bar")
    conn = engine.connect()
    assert conn.connection._client.project == "bar"


def test_engine_no_dataset_no_project(faux_conn):
    engine = sqlalchemy.create_engine("bigquery://")
    conn = engine.connect()
    assert conn.connection._client.project == "authproj"


@pytest.mark.parametrize("arraysize", [0, None])
def test_set_arraysize_not_set_if_false(faux_conn, metadata, arraysize):
    engine = sqlalchemy.create_engine("bigquery://", arraysize=arraysize)
    sqlalchemy.Table("t", metadata, sqlalchemy.Column("c", sqlalchemy.Integer))
    conn = engine.connect()
    metadata.create_all(engine)

    # Because we gave a false array size, the array size wasn't set on the cursor:
    assert "arraysize" not in conn.connection.test_data


def test_set_arraysize(faux_conn, metadata):
    engine = sqlalchemy.create_engine("bigquery://", arraysize=42)
    sqlalchemy.Table("t", metadata, sqlalchemy.Column("c", sqlalchemy.Integer))
    conn = engine.connect()
    metadata.create_all(engine)

    # Because we gave a false array size, the array size wasn't set on the cursor:
    assert conn.connection.test_data["arraysize"] == 42


def test_arraysize_querystring_takes_precedence_over_default(faux_conn, metadata):
    arraysize = 42
    engine = sqlalchemy.create_engine(
        f"bigquery://myproject/mydataset?arraysize={arraysize}"
    )
    sqlalchemy.Table("t", metadata, sqlalchemy.Column("c", sqlalchemy.Integer))
    conn = engine.connect()
    metadata.create_all(engine)

    assert conn.connection.test_data["arraysize"] == arraysize


def test_dbapi_deprecated():
    from sqlalchemy_bigquery.base import BigQueryDialect

    assert BigQueryDialect.dbapi() is BigQueryDialect.import_dbapi()


# The faux client never decodes the credentials, so any value works.
FAKE_CREDENTIALS_BASE64 = "c2VjcmV0LWtleQ"
URL_WITH_CREDENTIALS = (
    "bigquery://user:pa55word@myproject/mydataset"
    f"?credentials_base64={FAKE_CREDENTIALS_BASE64}&location=US"
)


def test_engine_repr_hides_credentials_base64(faux_conn):
    engine = sqlalchemy.create_engine(URL_WITH_CREDENTIALS)

    assert repr(engine) == (
        "Engine(bigquery://user:***@myproject/mydataset"
        "?credentials_base64=%2A%2A%2A&location=US)"
    )


@pytest.mark.parametrize(
    ("render", "shows_secrets"),
    [
        pytest.param(str, True, marks=sqlalchemy_before_2_0, id="str-sqlalchemy-1.4"),
        pytest.param(str, False, marks=sqlalchemy_2_0_or_higher, id="str"),
        pytest.param(
            lambda url: url.render_as_string(hide_password=False),
            True,
            id="render_as_string-hide_password_false",
        ),
    ],
)
def test_engine_url_hides_credentials_base64_like_password(
    faux_conn, render, shows_secrets
):
    engine = sqlalchemy.create_engine(URL_WITH_CREDENTIALS)

    rendered = render(engine.url)

    assert ("pa55word" in rendered) is shows_secrets
    assert (FAKE_CREDENTIALS_BASE64 in rendered) is shows_secrets


@pytest.mark.parametrize(
    "derive",
    [
        pytest.param(
            lambda url: url.difference_update_query(["location"]),
            id="difference_update_query",
        ),
        pytest.param(lambda url: pickle.loads(pickle.dumps(url)), id="pickle"),
    ],
)
def test_engine_url_derived_urls_hide_credentials_base64(faux_conn, derive):
    engine = sqlalchemy.create_engine(URL_WITH_CREDENTIALS)

    url = derive(engine.url)

    assert url.query["credentials_base64"] == FAKE_CREDENTIALS_BASE64
    assert FAKE_CREDENTIALS_BASE64 not in repr(url)


def test_engine_url_without_credentials_base64_renders_as_usual(faux_conn):
    engine = sqlalchemy.create_engine(URL_WITH_CREDENTIALS)

    url = engine.url.difference_update_query(["credentials_base64"])

    assert repr(url) == "bigquery://user:***@myproject/mydataset?location=US"


def test_engine_url_keeps_credentials_base64(faux_conn):
    engine = sqlalchemy.create_engine(URL_WITH_CREDENTIALS)
    plain_url = sqlalchemy.engine.make_url(URL_WITH_CREDENTIALS)

    assert engine.url.query["credentials_base64"] == FAKE_CREDENTIALS_BASE64
    assert engine.url == plain_url
    assert hash(engine.url) == hash(plain_url)
    clone = sqlalchemy.create_engine(engine.url)
    assert clone.dialect.credentials_base64 == FAKE_CREDENTIALS_BASE64
    assert FAKE_CREDENTIALS_BASE64 not in repr(clone)


def test_engine_url_without_credentials_base64_is_unchanged(faux_conn):
    engine = sqlalchemy.create_engine("bigquery://myproject/mydataset?location=US")

    assert type(engine.url) is sqlalchemy.engine.URL
