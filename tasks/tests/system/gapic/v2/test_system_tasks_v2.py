# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.cloud import tasks_v2


class TestSystemTasks(object):
    def test_recognize(self):
        client = tasks_v2.CloudTasksClient()

        # Setup Request
        parent = client.location_path(os.environ["PROJECT_ID"], "us-central1")

        paged_list_response = client.list_queues(parent)
        resources = list(paged_list_response)
        assert len(resources) == 0