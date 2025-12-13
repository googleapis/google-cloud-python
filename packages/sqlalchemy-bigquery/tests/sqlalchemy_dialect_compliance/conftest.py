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
import re
import traceback

from sqlalchemy.testing import config
from sqlalchemy.testing.plugin.pytestplugin import *  # noqa
from sqlalchemy.testing.plugin.pytestplugin import (
    pytest_sessionstart as _pytest_sessionstart,
    pytest_sessionfinish as _pytest_sessionfinish,
)

import google.cloud.bigquery.dbapi.connection
import test_utils.prefixer

import sqlalchemy_bigquery.base

sqlalchemy_bigquery.BigQueryDialect.preexecute_autoincrement_sequences = True


prefixer = test_utils.prefixer.Prefixer(
    "python-bigquery-sqlalchemy", "tests/compliance"
)

google.cloud.bigquery.dbapi.connection.Connection.rollback = lambda self: None

_where = re.compile(r"\s+WHERE\s+", re.IGNORECASE).search

# BigQuery requires delete statements to have where clauses. Other
# databases don't and sqlalchemy doesn't include where clauses when
# cleaning up test data.  So we add one when we see a delete without a
# where clause when tearing down tests.  We only do this during tear
# down, by inspecting the stack, because we don't want to hide bugs
# outside of test house-keeping.


def visit_delete(self, delete_stmt, *args, **kw):
    text = super(sqlalchemy_bigquery.base.BigQueryCompiler, self).visit_delete(
        delete_stmt, *args, **kw
    )

    if not _where(text) and any(
        "teardown" in f.name.lower() for f in traceback.extract_stack()
    ):
        text += " WHERE true"

    return text


sqlalchemy_bigquery.base.BigQueryCompiler.visit_delete = visit_delete


def pytest_sessionstart(session):
    dataset_id = prefixer.create_prefix()
    session.config.option.dburi = [f"bigquery:///{dataset_id}"]
    with contextlib.closing(google.cloud.bigquery.Client()) as client:
        client.create_dataset(dataset_id)
    _pytest_sessionstart(session)


def pytest_sessionfinish(session):
    dataset_id = config.db.dialect.dataset_id
    _pytest_sessionfinish(session)
    with contextlib.closing(google.cloud.bigquery.Client()) as client:
        client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)
        for dataset in client.list_datasets():
            if prefixer.should_cleanup(dataset.dataset_id):
                client.delete_dataset(dataset, delete_contents=True, not_found_ok=True)
