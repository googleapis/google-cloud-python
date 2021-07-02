# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import uuid

from google.cloud import spanner
import mock
import pytest

import quickstart
from snippets_test import cleanup_old_instances


def unique_instance_id():
    """Creates a unique id for the database."""
    return f"test-instance-{uuid.uuid4().hex[:10]}"


INSTANCE_ID = unique_instance_id()


def create_instance():
    spanner_client = spanner.Client()
    cleanup_old_instances(spanner_client)
    instance_config = "{}/instanceConfigs/{}".format(
        spanner_client.project_name, "regional-us-central1"
    )
    instance = spanner_client.instance(
        INSTANCE_ID,
        instance_config,
        labels={"cloud_spanner_samples": "true", "created": str(int(time.time()))},
    )
    op = instance.create()
    op.result(120)  # block until completion


@pytest.fixture
def patch_instance():
    original_instance = spanner.Client.instance

    spanner_client = spanner.Client()
    cleanup_old_instances(spanner_client)
    create_instance()

    def new_instance(self, unused_instance_name):
        return original_instance(self, INSTANCE_ID)

    instance_patch = mock.patch(
        "google.cloud.spanner_v1.Client.instance",
        side_effect=new_instance,
        autospec=True,
    )

    with instance_patch:
        yield


@pytest.fixture
def example_database():
    spanner_client = spanner.Client()
    instance = spanner_client.instance(INSTANCE_ID)
    database = instance.database("my-database-id")

    if not database.exists():
        database.create()

    yield


def drop_instance():
    spanner_client = spanner.Client()
    instance = spanner_client.instance(INSTANCE_ID)
    instance.delete()


def test_quickstart(capsys, patch_instance, example_database):
    quickstart.run_quickstart()
    out, _ = capsys.readouterr()

    # Drop created instance before verifying output.
    drop_instance()

    assert "[1]" in out
