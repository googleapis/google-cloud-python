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

import pytest

from google.cloud import bigtable

INSTANCE_ID = "instance-snippet"
CLUSTER_ID = "cluster-snippet"
CLUSTER_ID1 = "ssd-cluster-1"


@pytest.fixture(scope='module')
def client():
    return bigtable.Client(project='grass-clump-479', admin=True)


@pytest.fixture
def to_delete():
    doomed = []
    yield doomed
    for item in doomed:
        item.delete()


@pytest.mark.order1
def test_bigtable_create_instance(client, to_delete):
    # [START bigtable_create_prod_instance]
    from google.cloud.bigtable import enums

    location_id = 'us-central1-f'
    serve_nodes = 3
    storage_type = enums.StorageType.SSD
    production = enums.Instance.Type.PRODUCTION
    labels = {'prod-label': 'prod-label'}

    instance = client.instance(INSTANCE_ID, instance_type=production,
                               labels=labels)
    cluster = instance.cluster(CLUSTER_ID1, location_id=location_id,
                               serve_nodes=serve_nodes,
                               default_storage_type=storage_type)
    instance.create(clusters=[cluster])
    # [END bigtable_create_prod_instance]

    assert instance is not None
    to_delete.append(instance)


@pytest.mark.order2
def test_bigtable_create_cluster(client):
    # [START bigtable_create_cluster]
    from google.cloud.bigtable import enums

    instance = client.instance(INSTANCE_ID)
    location_id = 'us-central1-a'
    serve_nodes = 3
    storage_type = enums.StorageType.SSD

    cluster = instance.cluster(CLUSTER_ID, location_id=location_id,
                               serve_nodes=serve_nodes,
                               default_storage_type=storage_type)
    cluster.create()
    # [END bigtable_create_cluster]
    assert cluster is not None


@pytest.mark.order3
def test_bigtable_list_instances(client):
    # [START bigtable_list_instances]
    (instances_list, failed_locations_list) = client.list_instances()
    # [END bigtable_list_instances]

    assert instances_list.__len__() is not 0


@pytest.mark.order4
def test_bigtable_list_clusters(client):
    # [START bigtable_list_clusters]
    instance = client.instance(INSTANCE_ID)
    (clusters_list, failed_locations_list) = instance.list_clusters()
    # [END bigtable_list_clusters]

    assert clusters_list.__len__() is not 0


@pytest.mark.order5
def test_bigtable_instance_exists(client):
    # [START bigtable_check_instance_exists]
    instance = client.instance(INSTANCE_ID)
    instance_exists = instance.exists()
    # [END bigtable_check_instance_exists]
    assert instance_exists


@pytest.mark.order6
def test_bigtable_cluster_exists(client):
    # [START bigtable_check_cluster_exists]
    instance = client.instance(INSTANCE_ID)
    cluster = instance.cluster(CLUSTER_ID1)
    cluster_exists = cluster.exists()
    # [END bigtable_check_cluster_exists]
    assert cluster_exists


@pytest.mark.order7
def test_bigtable_reload_cluster(client):
    # [START bigtable_reload_cluster]
    instance = client.instance(INSTANCE_ID)
    cluster = instance.cluster(CLUSTER_ID1)
    cluster.reload()
    # [END bigtable_reload_cluster]
    assert cluster is not None


@pytest.mark.order8
def test_bigtable_update_cluster(client):
    # [START bigtable_update_cluster]
    instance = client.instance(INSTANCE_ID)
    cluster = instance.cluster(CLUSTER_ID1)
    cluster.serve_nodes = 8
    cluster.update()
    # [END bigtable_update_cluster]
    assert cluster is not None


@pytest.mark.order9
def test_bigtable_create_table(client):
    # [START bigtable_create_table]
    from google.cloud.bigtable import column_family

    instance = client.instance(INSTANCE_ID)
    table = instance.table("table_my")
    # Define the GC policy to retain only the most recent 2 versions.
    max_versions_rule = column_family.MaxVersionsGCRule(2)
    column_families = {'cf1': max_versions_rule}
    table.create(column_families=column_families)
    # [END bigtable_create_table]
    assert table is not None


@pytest.mark.order10
def test_bigtable_list_tables(client):
    # [START bigtable_list_tables]
    instance = client.instance(INSTANCE_ID)
    tables_list = instance.list_tables()
    # [END bigtable_list_tables]
    assert tables_list.__len__() is not 0


@pytest.mark.order11
def test_bigtable_delete_cluster(client):
    # [START bigtable_delete_cluster]
    instance = client.instance(INSTANCE_ID)
    cluster = instance.cluster(CLUSTER_ID1)
    cluster.delete()
    # [END bigtable_delete_cluster]
    assert cluster is None


@pytest.mark.order12
def test_bigtable_delete_instance(client):
    # [START bigtable_delete_instance]
    instance = client.instance(INSTANCE_ID)
    instance.delete()
    # [END bigtable_delete_instance]
    assert instance is None


if __name__ == '__main__':
    pytest.main()
