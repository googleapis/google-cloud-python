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
import os
import re
import traceback

import google.cloud.bigquery.dbapi.connection
import test_utils.prefixer
from sqlalchemy.testing import config
from sqlalchemy.testing.plugin.pytestplugin import *  # noqa
from sqlalchemy.testing.plugin.pytestplugin import (
    pytest_configure as _pytest_configure,
)
from sqlalchemy.testing.plugin.pytestplugin import (
    pytest_sessionfinish as _pytest_sessionfinish,
)
from sqlalchemy.testing.plugin.pytestplugin import (
    pytest_sessionstart as _pytest_sessionstart,
)

import sqlalchemy_bigquery.base
import sqlalchemy_bigquery.provision  # noqa: F401

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


def pytest_configure(config):
    if hasattr(config, "workerinput"):
        prefix = config.workerinput.get("compliance_run_prefix")
        if prefix:
            os.environ["COMPLIANCE_RUN_PREFIX"] = prefix
    else:
        if "COMPLIANCE_RUN_PREFIX" not in os.environ:
            os.environ["COMPLIANCE_RUN_PREFIX"] = prefixer.create_prefix()

    run_prefix = os.environ.get("COMPLIANCE_RUN_PREFIX")
    master_dataset_id = f"{run_prefix}_master"
    config.option.dburi = [f"bigquery:///{master_dataset_id}"]
    _pytest_configure(config)


def pytest_configure_node(node):
    node.workerinput["compliance_run_prefix"] = os.environ.get("COMPLIANCE_RUN_PREFIX")


def pytest_sessionstart(session):
    run_prefix = os.environ.get("COMPLIANCE_RUN_PREFIX")
    if not run_prefix:
        run_prefix = prefixer.create_prefix()
        os.environ["COMPLIANCE_RUN_PREFIX"] = run_prefix

    if hasattr(session.config, "workerinput"):
        # In a pytest-xdist worker process:
        # Each worker connects to its own partition ({run_prefix}_{follower_ident}).
        # Ensure the worker's dataset exists and bind dburi to worker partition.
        ident = session.config.workerinput.get("follower_ident")
        worker_dataset_id = f"{run_prefix}_{ident}" if ident else f"{run_prefix}_worker"
        session.config.option.dburi = [f"bigquery:///{worker_dataset_id}"]
        with contextlib.closing(google.cloud.bigquery.Client()) as client:
            dataset_ref = google.cloud.bigquery.DatasetReference(
                client.project, worker_dataset_id
            )
            dataset = google.cloud.bigquery.Dataset(dataset_ref)
            dataset.default_table_expiration_ms = 3600 * 1000
            client.create_dataset(dataset, exists_ok=True)
        _pytest_sessionstart(session)
        return

    # Master process (or single-process sequential run):
    master_dataset_id = f"{run_prefix}_master"
    session.config.option.dburi = [f"bigquery:///{master_dataset_id}"]
    with contextlib.closing(google.cloud.bigquery.Client()) as client:
        dataset_ref = google.cloud.bigquery.DatasetReference(
            client.project, master_dataset_id
        )
        dataset = google.cloud.bigquery.Dataset(dataset_ref)
        dataset.default_table_expiration_ms = 3600 * 1000
        client.create_dataset(dataset, exists_ok=True)
    _pytest_sessionstart(session)


def pytest_sessionfinish(session):
    if hasattr(session.config, "workerinput"):
        # Worker dataset teardown is handled by provision.drop_follower_db
        # on the controller node.
        _pytest_sessionfinish(session)
        return

    _pytest_sessionfinish(session)
    run_prefix = os.environ.get("COMPLIANCE_RUN_PREFIX")
    with contextlib.closing(google.cloud.bigquery.Client()) as client:
        if hasattr(config, "db") and config.db is not None:
            dataset_id = config.db.dialect.dataset_id
            client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)
        elif run_prefix:
            client.delete_dataset(
                f"{run_prefix}_master", delete_contents=True, not_found_ok=True
            )

        for dataset in client.list_datasets():
            if prefixer.should_cleanup(dataset.dataset_id):
                client.delete_dataset(dataset, delete_contents=True, not_found_ok=True)
