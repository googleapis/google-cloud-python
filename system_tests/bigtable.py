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
    total_sleep = 0
    while not created_op.finished():
        if total_sleep > 5:
            raise RuntimeError('Cluster creation exceed 5 seconds.')
        time.sleep(1)
        total_sleep += 1


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
