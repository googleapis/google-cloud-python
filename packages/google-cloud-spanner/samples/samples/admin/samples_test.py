#!/usr/bin/env python

# Copyright 2024 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to do basic operations using Cloud
Spanner.
For more information, see the README.rst under /spanner.
"""

import uuid

from google.api_core import exceptions
from google.cloud.spanner_admin_database_v1.types.common import DatabaseDialect
import pytest
from test_utils.retry import RetryErrors

import samples

CREATE_TABLE_SINGERS = """\
CREATE TABLE Singers (
    SingerId     INT64 NOT NULL,
    FirstName    STRING(1024),
    LastName     STRING(1024),
    SingerInfo   BYTES(MAX),
    FullName     STRING(2048) AS (
        ARRAY_TO_STRING([FirstName, LastName], " ")
    ) STORED
) PRIMARY KEY (SingerId)
"""

CREATE_TABLE_ALBUMS = """\
CREATE TABLE Albums (
    SingerId     INT64 NOT NULL,
    AlbumId      INT64 NOT NULL,
    AlbumTitle   STRING(MAX)
) PRIMARY KEY (SingerId, AlbumId),
INTERLEAVE IN PARENT Singers ON DELETE CASCADE
"""

retry_429 = RetryErrors(exceptions.ResourceExhausted, delay=15)


@pytest.fixture(scope="module")
def sample_name():
    return "snippets"


@pytest.fixture(scope="module")
def database_dialect():
    """Spanner dialect to be used for this sample.

    The dialect is used to initialize the dialect for the database.
    It can either be GoogleStandardSql or PostgreSql.
    """
    return DatabaseDialect.GOOGLE_STANDARD_SQL


@pytest.fixture(scope="module")
def create_instance_id():
    """Id for the low-cost instance."""
    return f"create-instance-{uuid.uuid4().hex[:10]}"


@pytest.fixture(scope="module")
def lci_instance_id():
    """Id for the low-cost instance."""
    return f"lci-instance-{uuid.uuid4().hex[:10]}"


@pytest.fixture(scope="module")
def database_id():
    return f"test-db-{uuid.uuid4().hex[:10]}"


@pytest.fixture(scope="module")
def create_database_id():
    return f"create-db-{uuid.uuid4().hex[:10]}"


@pytest.fixture(scope="module")
def cmek_database_id():
    return f"cmek-db-{uuid.uuid4().hex[:10]}"


@pytest.fixture(scope="module")
def default_leader_database_id():
    return f"leader_db_{uuid.uuid4().hex[:10]}"


@pytest.fixture(scope="module")
def database_ddl():
    """Sequence of DDL statements used to set up the database.

    Sample testcase modules can override as needed.
    """
    return [CREATE_TABLE_SINGERS, CREATE_TABLE_ALBUMS]


@pytest.fixture(scope="module")
def default_leader():
    """Default leader for multi-region instances."""
    return "us-east4"


@pytest.fixture(scope="module")
def base_instance_config_id(spanner_client):
    return "{}/instanceConfigs/{}".format(spanner_client.project_name, "nam7")


def test_create_instance_explicit(spanner_client, create_instance_id):
    # Rather than re-use 'sample_isntance', we create a new instance, to
    # ensure that the 'create_instance' snippet is tested.
    retry_429(samples.create_instance)(create_instance_id)
    instance = spanner_client.instance(create_instance_id)
    retry_429(instance.delete)()


def test_create_database_with_default_leader(
    capsys,
    multi_region_instance,
    multi_region_instance_id,
    default_leader_database_id,
    default_leader,
):
    retry_429 = RetryErrors(exceptions.ResourceExhausted, delay=15)
    retry_429(samples.create_database_with_default_leader)(
        multi_region_instance_id, default_leader_database_id, default_leader
    )
    out, _ = capsys.readouterr()
    assert default_leader_database_id in out
    assert default_leader in out
