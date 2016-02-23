# Copyright 2016 Google Inc. All rights reserved.
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

import unittest2

from gcloud import _helpers
from gcloud.bigtable.client import Client
from gcloud.environment_vars import TESTS_PROJECT


_helpers.PROJECT = TESTS_PROJECT
CENTRAL_1C_ZONE = 'us-central1-c'
NOW_MILLIS = int(1000 * time.time())
CLUSTER_ID = 'gcloud-python-%d' % (NOW_MILLIS,)
EXISTING_CLUSTERS = []
EXPECTED_ZONES = (
    'asia-east1-b',
    'europe-west1-c',
    'us-central1-b',
    CENTRAL_1C_ZONE,
)


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None
    CLUSTER = None


def _operation_wait(operation, max_attempts=5):
    """Wait until an operation has completed.

    :type operation: :class:`gcloud.bigtable.cluster.Operation`
    :param operation: Operation that has not finished.

    :type max_attempts: int
    :param max_attempts: (Optional) The maximum number of times to check if
                         the operation has finished. Defaults to 5.
    """
    total_sleep = 0
    while not operation.finished():
        if total_sleep > max_attempts:
            return False
        time.sleep(1)
        total_sleep += 1

    return True


def setUpModule():
    Config.CLIENT = Client(admin=True)
    Config.CLUSTER = Config.CLIENT.cluster(CENTRAL_1C_ZONE, CLUSTER_ID,
                                           display_name=CLUSTER_ID)
    Config.CLIENT.start()
    clusters, failed_zones = Config.CLIENT.list_clusters()

    if len(failed_zones) != 0:
        raise ValueError('List clusters failed in module set up.')

    EXISTING_CLUSTERS[:] = clusters

    # After listing, create the test cluster.
    created_op = Config.CLUSTER.create()
    if not _operation_wait(created_op):
        raise RuntimeError('Cluster creation exceed 5 seconds.')


def tearDownModule():
    Config.CLUSTER.delete()
    Config.CLIENT.stop()


class TestClusterAdminAPI(unittest2.TestCase):

    def setUp(self):
        self.clusters_to_delete = []

    def tearDown(self):
        for cluster in self.clusters_to_delete:
            cluster.delete()

    def test_list_zones(self):
        zones = Config.CLIENT.list_zones()
        self.assertEqual(sorted(zones), sorted(EXPECTED_ZONES))

    def test_list_clusters(self):
        clusters, failed_zones = Config.CLIENT.list_clusters()
        self.assertEqual(failed_zones, [])
        # We have added one new cluster in `setUpModule`.
        self.assertEqual(len(clusters), len(EXISTING_CLUSTERS) + 1)
        for cluster in clusters:
            cluster_existence = (cluster in EXISTING_CLUSTERS or
                                 cluster == Config.CLUSTER)
            self.assertTrue(cluster_existence)

    def test_reload(self):
        # Use same arguments as Config.CLUSTER (created in `setUpModule`)
        # so we can use reload() on a fresh instance.
        cluster = Config.CLIENT.cluster(CENTRAL_1C_ZONE, CLUSTER_ID)
        # Make sure metadata unset before reloading.
        cluster.display_name = None
        cluster.serve_nodes = None

        cluster.reload()
        self.assertEqual(cluster.display_name, Config.CLUSTER.display_name)
        self.assertEqual(cluster.serve_nodes, Config.CLUSTER.serve_nodes)

    def test_create_cluster(self):
        cluster_id = '%s-a' % (CLUSTER_ID,)
        cluster = Config.CLIENT.cluster(CENTRAL_1C_ZONE, cluster_id)
        operation = cluster.create()
        # Make sure this cluster gets deleted after the test case.
        self.clusters_to_delete.append(cluster)

        # We want to make sure the operation completes.
        self.assertTrue(_operation_wait(operation))

        # Create a new cluster instance and make sure it is the same.
        cluster_alt = Config.CLIENT.cluster(CENTRAL_1C_ZONE, cluster_id)
        cluster_alt.reload()

        self.assertEqual(cluster, cluster_alt)
        self.assertEqual(cluster.display_name, cluster_alt.display_name)
        self.assertEqual(cluster.serve_nodes, cluster_alt.serve_nodes)

    def test_update(self):
        curr_display_name = Config.CLUSTER.display_name
        Config.CLUSTER.display_name = 'Foo Bar Baz'
        operation = Config.CLUSTER.update()

        # We want to make sure the operation completes.
        self.assertTrue(_operation_wait(operation))

        # Create a new cluster instance and make sure it is the same.
        cluster_alt = Config.CLIENT.cluster(CENTRAL_1C_ZONE, CLUSTER_ID)
        self.assertNotEqual(cluster_alt.display_name,
                            Config.CLUSTER.display_name)
        cluster_alt.reload()
        self.assertEqual(cluster_alt.display_name,
                         Config.CLUSTER.display_name)

        # Make sure to put the cluster back the way it was for the
        # other test cases.
        Config.CLUSTER.display_name = curr_display_name
        operation = Config.CLUSTER.update()

        # We want to make sure the operation completes.
        self.assertTrue(_operation_wait(operation))
