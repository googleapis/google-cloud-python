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


def test_bigtable_create_instance():
    from test_utils.system import unique_resource_id
    # [START bigtable_create_prod_instance]
    from google.cloud.bigtable import Client
    from google.cloud.bigtable import enums

    my_instance_id = "inst-my-" + unique_resource_id('-')
    my_cluster_id = "clus-my-" + unique_resource_id('-')
    location_id = 'us-central1-f'
    serve_nodes = 3
    storage_type = enums.StorageType.SSD
    production = enums.Instance.Type.PRODUCTION
    labels = {'prod-label': 'prod-label'}

    client = Client(admin=True)
    instance = client.instance(my_instance_id, instance_type=production,
                               labels=labels)
    cluster = instance.cluster(my_cluster_id, location_id=location_id,
                               serve_nodes=serve_nodes,
                               default_storage_type=storage_type)
    operation = instance.create(clusters=[cluster])
    # We want to make sure the operation completes.
    operation.result(timeout=100)
    # [END bigtable_create_prod_instance]
    assert instance.exists()
    instance.delete()


def test_bigtable_list_instances():
    # [START bigtable_list_instances]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    (instances_list, failed_locations_list) = client.list_instances()
    # [END bigtable_list_instances]
    assert len(instances_list) is not 0


def test_bigtable_list_clusters_in_project():
    # [START bigtable_list_clusters_in_project]
    from google.cloud.bigtable import Client

    client = Client(admin=True)
    (clusters_list, failed_locations_list) = client.list_clusters()
    # [END bigtable_list_clusters_in_project]
    assert len(clusters_list) is not 0


if __name__ == '__main__':
    pytest.main()
