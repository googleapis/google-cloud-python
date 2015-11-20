# Copyright 2015 Google Inc. All rights reserved.
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


import unittest2


class TestCluster(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.cluster import Cluster
        return Cluster

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor_defaults(self):
        zone = 'zone'
        cluster_id = 'cluster-id'
        client = object()

        cluster = self._makeOne(zone, cluster_id, client)
        self.assertEqual(cluster.zone, zone)
        self.assertEqual(cluster.cluster_id, cluster_id)
        self.assertEqual(cluster.display_name, cluster_id)
        self.assertEqual(cluster.serve_nodes, 3)
        self.assertTrue(cluster._client is client)

    def test_constructor_non_default(self):
        zone = 'zone'
        cluster_id = 'cluster-id'
        display_name = 'display_name'
        serve_nodes = 8
        client = object()

        cluster = self._makeOne(zone, cluster_id, client,
                                display_name=display_name,
                                serve_nodes=serve_nodes)
        self.assertEqual(cluster.zone, zone)
        self.assertEqual(cluster.cluster_id, cluster_id)
        self.assertEqual(cluster.display_name, display_name)
        self.assertEqual(cluster.serve_nodes, serve_nodes)
        self.assertTrue(cluster._client is client)

    def test_table_factory(self):
        from gcloud.bigtable.table import Table

        zone = 'zone'
        cluster_id = 'cluster-id'
        cluster = self._makeOne(zone, cluster_id, None)

        table_id = 'table_id'
        table = cluster.table(table_id)
        self.assertTrue(isinstance(table, Table))
        self.assertEqual(table.table_id, table_id)
        self.assertEqual(table._cluster, cluster)

    def test_from_pb_success(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        client = _Client(project=project)

        cluster_name = ('projects/' + project + '/zones/' + zone +
                        '/clusters/' + cluster_id)
        cluster_pb = data_pb2.Cluster(
            name=cluster_name,
            display_name=cluster_id,
            serve_nodes=3,
        )

        klass = self._getTargetClass()
        cluster = klass.from_pb(cluster_pb, client)
        self.assertTrue(isinstance(cluster, klass))
        self.assertEqual(cluster._client, client)
        self.assertEqual(cluster.zone, zone)
        self.assertEqual(cluster.cluster_id, cluster_id)

    def test_from_pb_bad_cluster_name(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)

        cluster_name = 'INCORRECT_FORMAT'
        cluster_pb = data_pb2.Cluster(name=cluster_name)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, None)

    def test_from_pb_project_mistmatch(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        alt_project = 'ALT_PROJECT'
        client = _Client(project=alt_project)

        self.assertNotEqual(project, alt_project)

        cluster_name = ('projects/' + project + '/zones/' + zone +
                        '/clusters/' + cluster_id)
        cluster_pb = data_pb2.Cluster(name=cluster_name)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, client)


class Test__get_pb_property_value(unittest2.TestCase):

    def _callFUT(self, message_pb, property_name):
        from gcloud.bigtable.cluster import _get_pb_property_value
        return _get_pb_property_value(message_pb, property_name)

    def test_it(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        serve_nodes = 119
        cluster_pb = data_pb2.Cluster(serve_nodes=serve_nodes)
        result = self._callFUT(cluster_pb, 'serve_nodes')
        self.assertEqual(result, serve_nodes)

    def test_with_value_unset_on_pb(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        cluster_pb = data_pb2.Cluster()
        with self.assertRaises(ValueError):
            self._callFUT(cluster_pb, 'serve_nodes')


class _Client(object):

    def __init__(self, project):
        self.project = project
