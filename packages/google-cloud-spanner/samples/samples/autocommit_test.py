# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import time
import uuid

from google.api_core.exceptions import Aborted
from google.cloud import spanner
import pytest
from test_utils.retry import RetryErrors

import autocommit
from snippets_test import cleanup_old_instances


def unique_instance_id():
    """Creates a unique id for the database."""
    return f"test-instance-{uuid.uuid4().hex[:10]}"


def unique_database_id():
    """Creates a unique id for the database."""
    return f"test-db-{uuid.uuid4().hex[:10]}"


INSTANCE_ID = unique_instance_id()
DATABASE_ID = unique_database_id()


@pytest.fixture(scope="module")
def spanner_instance():
    spanner_client = spanner.Client()
    cleanup_old_instances(spanner_client)
    instance_config = "{}/instanceConfigs/{}".format(
        spanner_client.project_name, "regional-us-central1"
    )
    instance = spanner_client.instance(
        INSTANCE_ID,
        instance_config,
        labels={
            "cloud_spanner_samples": "true",
            "created": str(int(time.time()))
        }
    )
    op = instance.create()
    op.result(120)  # block until completion
    yield instance
    instance.delete()


@pytest.fixture(scope="module")
def database(spanner_instance):
    """Creates a temporary database that is removed after testing."""
    db = spanner_instance.database(DATABASE_ID)
    db.create()
    yield db
    db.drop()


@RetryErrors(exception=Aborted, max_tries=2)
def test_enable_autocommit_mode(capsys, database):
    # Delete table if it exists for retry attempts.
    table = database.table('Singers')
    if table.exists():
        op = database.update_ddl(["DROP TABLE Singers"])
        op.result()

    autocommit.enable_autocommit_mode(INSTANCE_ID, DATABASE_ID)
    out, _ = capsys.readouterr()
    assert "Autocommit mode is enabled." in out
    assert "SingerId: 13, AlbumId: Russell, AlbumTitle: Morales" in out
