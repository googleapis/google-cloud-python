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

# flake8: noqa

from google.api_core import exceptions
from google.cloud import asset_v1
from google.cloud.asset_v1 import enums

from test_utils.vpcsc_config import vpcsc_config


class TestVPCServiceControl(object):
    @staticmethod
    def _is_rejected(call):
        try:
            responses = call()
        except exceptions.PermissionDenied as e:
            return e.message == "Request is prohibited by organization's policy"
        except:
            pass  # XXX raise?
        return False

    def _do_test(self, delayed_inside, delayed_outside):
        if vpcsc_config.inside_vpcsc:
            assert self._is_rejected(delayed_outside)
            assert not self._is_rejected(delayed_inside)
        else:
            assert not self._is_rejected(delayed_outside)
            assert self._is_rejected(delayed_inside)

    @vpcsc_config.skip_if_no_inside_project
    @vpcsc_config.skip_if_no_outside_project
    def test_export_assets(self):
        client = asset_v1.AssetServiceClient()
        output_config = {}
        parent_inside = "projects/" + vpcsc_config.project_inside
        delayed_inside = lambda: client.export_assets(parent_inside, output_config)
        parent_outside = "projects/" + vpcsc_config.project_outside
        delayed_outside = lambda: client.export_assets(parent_outside, output_config)
        self._do_test(delayed_inside, delayed_outside)

    @vpcsc_config.skip_if_no_inside_project
    @vpcsc_config.skip_if_no_outside_project
    def test_batch_get_assets_history(self):
        client = asset_v1.AssetServiceClient()
        content_type = enums.ContentType.CONTENT_TYPE_UNSPECIFIED
        read_time_window = {}
        parent_inside = "projects/" + vpcsc_config.project_inside
        delayed_inside = lambda: client.batch_get_assets_history(
            parent_inside, content_type, read_time_window
        )
        parent_outside = "projects/" + vpcsc_config.project_outside
        delayed_outside = lambda: client.batch_get_assets_history(
            parent_outside, content_type, read_time_window
        )
        self._do_test(delayed_inside, delayed_outside)
