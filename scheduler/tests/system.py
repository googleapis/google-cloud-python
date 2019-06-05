# Copyright 2019 Google LLC
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

from google.cloud import scheduler_v1


class TestSystemScheduler(object):
    def test_create_job(self):
        client = scheduler_v1.CloudSchedulerClient()
        parent = client.location_path(os.environ.get("PROJECT_ID"), "us-central1")
        client.list_jobs(parent)
