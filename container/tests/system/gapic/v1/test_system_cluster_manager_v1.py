# Copyright 2017, Google LLC All rights reserved.
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

import os
import time

from google.cloud import container_v1
from google.cloud.container_v1.proto import cluster_service_pb2


class TestSystemClusterManager(object):
    def test_list_clusters(self):
        project_id = os.environ["PROJECT_ID"]

        client = container_v1.ClusterManagerClient()
        project_id_2 = project_id
        zone = "us-central1-a"
        response = client.list_clusters(project_id_2, zone)
