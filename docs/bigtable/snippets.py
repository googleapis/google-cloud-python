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

from google.cloud import bigtable


def snippet(func):
    """Mark ``func`` as a snippet example function."""
    func._snippet = True
    return func


@snippet
def bigtable_create_instance(client, to_delete):
    # [START bigtable_create_prod_instance]
    from google.cloud.bigtable import enums

    location_id = 'us-central1-f'
    serve_nodes = 3
    storage_type = enums.StorageType.SSD
    production = enums.Instance.Type.PRODUCTION
    labels = {'prod-label': 'prod-label'}

    instance = client.instance("instance_my1", instance_type=production,
                               labels=labels)
    cluster = instance.cluster("ssd-cluster1", location_id=location_id,
                               serve_nodes=serve_nodes,
                               default_storage_type=storage_type)
    instance.create(clusters=[cluster])
    # [END bigtable_create_prod_instance]

    to_delete.append(instance)


@snippet
def bigtable_create_cluster(client):
    # [START bigtable_create_cluster]
    from google.cloud.bigtable import enums

    instance = client.instance("instance_my1")
    location_id = 'us-central1-a'
    serve_nodes = 3
    storage_type = enums.StorageType.SSD

    cluster = instance.cluster("cluster_my2", location_id=location_id,
                               serve_nodes=serve_nodes,
                               default_storage_type=storage_type)
    cluster.create()
    # [END bigtable_create_cluster]


@snippet
def bigtable_list_instances(client):
    # [START bigtable_list_instances]
    (instances_list, failed_locations_list) = client.list_instances()
    # [END bigtable_list_instances]


@snippet
def bigtable_list_clusters(client):
    # [START bigtable_list_clusters]
    instance = client.instance("instance_my1")
    (clusters_list, failed_locations_list) = instance.list_clusters()
    # [END bigtable_list_clusters]


@snippet
def bigtable_instance_exists(client):
    # [START bigtable_check_instance_exists]
    instance = client.instance("instance_my1")
    instance_exists =  instance.exists()
    # [END bigtable_check_instance_exists]


@snippet
def bigtable_cluster_exists(client):
    # [START bigtable_check_cluster_exists]
    instance = client.instance("instance_my1")
    cluster = instance.cluster("ssd-cluster1")
    cluster_exists = cluster.exists()
    # [END bigtable_check_cluster_exists]


@snippet
def bigtable_delete_instance(client):
    # [START bigtable_delete_instance]
    instance = client.instance("instance_my1")
    instance.delete()
    # [END bigtable_delete_instance]


@snippet
def bigtable_delete_cluster(client):
    # [START bigtable_delete_cluster]
    instance = client.instance("instance_my1")
    cluster = instance.cluster("ssd-cluster1")
    cluster.delete()
    # [END bigtable_delete_cluster]


def bigtable_reload_cluster(client):
    # [START bigtable_reload_cluster]
    instance = client.instance("instance_my1")
    cluster = instance.cluster("ssd-cluster1")
    cluster.reload()
    # [END bigtable_reload_cluster]

def bigtable_update_cluster(client):
    # [START bigtable_update_cluster]
    instance = client.instance("instance_my1")
    cluster = instance.cluster("ssd-cluster1")
    cluster.serve_nodes = 8
    cluster.update()
    # [END bigtable_update_cluster]


@snippet
def bigtable_create_table(client):
    # [START bigtable_create_table]
    from google.cloud.bigtable import column_family
    
    instance = client.instance("instance_my1")
    table = instance.table("table_my")
    # Define the GC policy to retain only the most recent 2 versions.
    max_versions_rule = column_family.MaxVersionsGCRule(2)
    column_families = {'cf1': max_versions_rule}
    table.create(column_families=column_families)
    # [END bigtable_create_table]


@snippet
def bigtable_list_tables(client):
    # [START bigtable_list_tables]
    instance = client.instance("instance_my1")
    tables_list = instance.list_tables()
    # [END bigtable_list_tables]


def _line_no(func):
    code = getattr(func, '__code__', None) or getattr(func, 'func_code')
    return code.co_firstlineno


def _find_examples():
    funcs = [obj for obj in globals().values()
             if getattr(obj, '_snippet', False)]
    for func in sorted(funcs, key=_line_no):
        yield func


def _name_and_doc(func):
    return func.__name__, func.__doc__


def main():
    client = bigtable.Client(project='my-project', admin=True)
    for example in _find_examples():
        to_delete = []
        print '%-25s: %s' % _name_and_doc(example)
        try:
            example(client, to_delete)
        except AssertionError as failure:
            print '   FAIL: %s' % (failure,)
        except Exception as error:  # pylint: disable=broad-except
            print '  ERROR: %r' % (error,)
        for item in to_delete:
            item.delete()


if __name__ == '__main__':
    main()
