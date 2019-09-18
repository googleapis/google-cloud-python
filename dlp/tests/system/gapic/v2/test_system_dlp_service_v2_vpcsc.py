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
import json
import pytest

from google.cloud import dlp_v2
from google.cloud.dlp_v2 import enums
from google.cloud.dlp_v2.proto import dlp_pb2
from google.api_core import exceptions


PROJECT_INSIDE = os.environ.get("PROJECT_ID", None)
PROJECT_OUTSIDE = os.environ.get(
    "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT", None
)
IS_INSIDE_VPCSC = os.environ.get("GOOGLE_CLOUD_TESTS_IN_VPCSC", "true")


class TestSystemDlpService(object):
    @staticmethod
    def _is_rejected(call):
        try:
            responses = call()
        except exceptions.PermissionDenied as e:
            return e.message == "Request is prohibited by organization's policy"
        except:
            pass
        return False

    def _get_project_id(self):
        env_var_name = "GOOGLE_APPLICATION_CREDENTIALS"
        path = os.environ[env_var_name]
        json_data = open(path).read()
        data = json.loads(json_data)
        return data["project_id"]

    @staticmethod
    def _do_test(inspect_inside, inspect_outside):
        if IS_INSIDE_VPCSC.lower() == "true":
            assert TestSystemDlpService._is_rejected(inspect_outside)
            assert not (TestSystemDlpService._is_rejected(inspect_inside))
        else:
            assert not (TestSystemDlpService._is_rejected(inspect_outside))
            assert TestSystemDlpService._is_rejected(inspect_inside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_inspect_content_vpcsc(self):
        # get project id from json file
        project_id = self._get_project_id()

        client = dlp_v2.DlpServiceClient()
        min_likelihood = enums.Likelihood.POSSIBLE
        info_types = [{"name": "FIRST_NAME"}, {"name": "LAST_NAME"}]
        inspect_config = {"info_types": info_types, "min_likelihood": min_likelihood}
        item = {"value": "Robert Frost"}

        project_inside = client.project_path(PROJECT_INSIDE)
        project_outside = client.project_path(PROJECT_OUTSIDE)

        inspect_inside = lambda: client.inspect_content(
            project_inside, inspect_config, item
        )
        inspect_outside = lambda: client.inspect_content(
            project_outside, inspect_config, item
        )
        TestSystemDlpService._do_test(inspect_inside, inspect_outside)
