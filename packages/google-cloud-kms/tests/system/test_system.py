# -*- coding: utf-8 -*-
#
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

from google.cloud import kms_v1


class TestKeyManagementServiceClient(object):
    def test_list_global_key_rings(self):
        project_id = os.environ["PROJECT_ID"]

        # List key rings from the global location.
        client = kms_v1.KeyManagementServiceClient()
        parent = f"projects/{project_id}/locations/global"
        client.list_key_rings(request={"parent": parent})
