#!/usr/bin/env python

# Copyright 2018, Google LLC
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

"""Testable usage examples for Google Cloud Bigtable API wrapper

Each example function takes a ``client`` argument (which must be an instance
of :class:`google.cloud.bigtable.client.Client`) and uses it to perform a task
with the API.

To facilitate running the examples as system tests, each example is also passed
a ``to_delete`` list;  the function adds to the list any objects created which
need to be deleted during teardown.

.. note::
    This file is under progress and will be updated with more guidance from
    the team. Unit tests will be added with guidance from the team.

"""

import datetime
import pytest

from test_utils.system import unique_resource_id
from google.cloud._helpers import UTC
from google.cloud.bigtable import Client
from google.cloud.bigtable import enums


INSTANCE_ID = "snippet-" + unique_resource_id('-')
CLUSTER_ID = "clus-1-" + unique_resource_id('-')
LOCATION_ID = 'us-central1-f'
ALT_LOCATION_ID = 'us-central1-a'
PRODUCTION = enums.Instance.Type.PRODUCTION
SERVER_NODES = 3
STORAGE_TYPE = enums.StorageType.SSD
LABEL_KEY = u'python-snippet'
LABEL_STAMP = datetime.datetime.utcnow() \
                               .replace(microsecond=0, tzinfo=UTC,) \
                               .strftime("%Y-%m-%dt%H-%M-%S")
LABELS = {LABEL_KEY: str(LABEL_STAMP)}


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    INSTANCE = None


def setup_module():
    client = Client(admin=True)
    Config.INSTANCE = client.instance(INSTANCE_ID,
                                      instance_type=PRODUCTION,
                                      labels=LABELS)
    cluster = Config.INSTANCE.cluster(CLUSTER_ID,
                                      location_id=LOCATION_ID,
                                      serve_nodes=SERVER_NODES,
                                      default_storage_type=STORAGE_TYPE)
    operation = Config.INSTANCE.create(clusters=[cluster])
    # We want to make sure the operation completes.
    operation.result(timeout=100)


def teardown_module():
    Config.INSTANCE.delete()


def test_bigtable_create_additional_cluster():
    # [START bigtable_create_cluster]
    from google.cloud.bigtable import Client
    from google.cloud.bigtable import enums

    # Assuming that there is an existing instance with `INSTANCE_ID`
    # on the server already.
    # to create an instance see
    # 'https://cloud.google.com/bigtable/docs/creating-instance'

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)

    cluster_id = "clus-my-" + unique_resource_id('-')
    location_id = 'us-central1-a'
    serve_nodes = 3
    storage_type = enums.StorageType.SSD

    cluster = instance.cluster(cluster_id, location_id=location_id,
                               serve_nodes=serve_nodes,
                               default_storage_type=storage_type)
    operation = cluster.create()
    # We want to make sure the operation completes.
    operation.result(timeout=100)
    # [END bigtable_create_cluster]
    assert cluster.exists()

    cluster.delete()


def test_bigtable_cluster_exists():
    # [START bigtable_check_cluster_exists]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    cluster = instance.cluster(CLUSTER_ID)
    cluster_exists = cluster.exists()
    # [END bigtable_check_cluster_exists]
    assert cluster_exists


def test_bigtable_reload_cluster():
    # [START bigtable_reload_cluster]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    cluster = instance.cluster(CLUSTER_ID)
    cluster.reload()
    # [END bigtable_reload_cluster]
    assert cluster.serve_nodes is SERVER_NODES


def test_bigtable_update_cluster():
    # [START bigtable_update_cluster]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    cluster = instance.cluster(CLUSTER_ID)
    cluster.serve_nodes = 8
    cluster.update()
    # [END bigtable_update_cluster]
    assert cluster.serve_nodes is 8


def test_bigtable_delete_cluster():
    # [START bigtable_delete_cluster]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    instance = client.instance(INSTANCE_ID)
    cluster_id = "clus-my-" + unique_resource_id('-')
    # [END bigtable_delete_cluster]

    cluster = instance.cluster(cluster_id, location_id=ALT_LOCATION_ID,
                               serve_nodes=SERVER_NODES,
                               default_storage_type=STORAGE_TYPE)
    operation = cluster.create()
    # We want to make sure the operation completes.
    operation.result(timeout=1000)

    # [START bigtable_delete_cluster]
    cluster_to_delete = instance.cluster(cluster_id)
    cluster_to_delete.delete()
    # [END bigtable_delete_cluster]
    assert not cluster_to_delete.exists()


if __name__ == '__main__':
    pytest.main()
