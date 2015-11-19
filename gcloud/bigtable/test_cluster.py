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
