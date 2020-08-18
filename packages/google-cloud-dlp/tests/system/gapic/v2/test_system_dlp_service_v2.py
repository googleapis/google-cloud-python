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

import json
import os

from google.cloud import dlp_v2


class TestSystemDlpService(object):
    def _get_project_id(self):
        env_var_name = "GOOGLE_APPLICATION_CREDENTIALS"
        path = os.environ[env_var_name]
        json_data = open(path).read()
        data = json.loads(json_data)
        return data["project_id"]

    def test_inspect_content(self):
        # get project id from json file
        project_id = self._get_project_id()

        client = dlp_v2.DlpServiceClient()
        min_likelihood = dlp_v2.Likelihood.POSSIBLE
        info_types = [{"name": "FIRST_NAME"}, {"name": "LAST_NAME"}]
        inspect_config = {"info_types": info_types, "min_likelihood": min_likelihood}
        item = {"value": "Robert Frost"}
        parent = f"projects/{project_id}"
        response = client.inspect_content(
            request={"parent": parent, "inspect_config": inspect_config, "item": item}
        )
