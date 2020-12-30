# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import uuid

from google.cloud import spanner
from google.cloud.spanner_dbapi import connect
import mock
import pytest

import autocommit


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
    config_name = f"{spanner_client.project_name}/instanceConfigs/regional-us-central1"

    instance = spanner_client.instance(INSTANCE_ID, config_name)
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


def test_enable_autocommit_mode(capsys, database):
    connection = connect(INSTANCE_ID, DATABASE_ID)
    cursor = connection.cursor()

    with mock.patch(
        "google.cloud.spanner_dbapi.connection.Cursor", return_value=cursor,
    ):
        autocommit.enable_autocommit_mode(INSTANCE_ID, DATABASE_ID)
        out, _ = capsys.readouterr()
        assert "Autocommit mode is enabled." in out
        assert "SingerId: 13, AlbumId: Russell, AlbumTitle: Morales" in out
