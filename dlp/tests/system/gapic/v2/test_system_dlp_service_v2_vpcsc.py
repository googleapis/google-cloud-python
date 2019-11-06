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
import pytest

from google.cloud import dlp_v2
from google.cloud.dlp_v2 import enums
from google.cloud.dlp_v2.proto import dlp_pb2
from google.api_core import exceptions

from test_utils.vpcsc_config import vpcsc_config


@vpcsc_config.skip_unless_inside_vpcsc
class TestSystemDlpService(object):
    @staticmethod
    def _is_rejected(call):
        try:
            responses = call()
        except exceptions.PermissionDenied as e:
            return e.message == "Request is prohibited by organization's policy"
        return False

    def _do_test(self, delayed_inside, delayed_outside):
        assert self._is_rejected(delayed_outside)
        assert not (self._is_rejected(delayed_inside))

    def test_inspect_content(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.inspect_content(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.inspect_content(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_redact_image(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.redact_image(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.redact_image(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_deidentify_content(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.deidentify_content(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.deidentify_content(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_reidentify_content(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.reidentify_content(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.reidentify_content(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_create_inspect_template(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.create_inspect_template(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.create_inspect_template(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_update_inspect_template(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.update_inspect_template(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.update_inspect_template(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_get_inspect_template(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.get_inspect_template(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.get_inspect_template(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skip(reason="List tests are currently not supported")
    def test_list_inspect_templates(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_inspect_templates(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_inspect_templates(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_delete_inspect_template(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.delete_inspect_template(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.delete_inspect_template(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_create_deidentify_template(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.create_deidentify_template(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.create_deidentify_template(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_update_deidentify_template(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.update_deidentify_template(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.update_deidentify_template(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_get_deidentify_template(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.get_deidentify_template(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.get_deidentify_template(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skip(reason="List tests are currently not supported")
    def test_list_deidentify_templates(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_deidentify_templates(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_deidentify_templates(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_delete_deidentify_template(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.delete_deidentify_template(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.delete_deidentify_template(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_create_dlp_job(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.create_dlp_job(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.create_dlp_job(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skip(reason="List tests are currently not supported")
    def test_list_dlp_jobs(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_dlp_jobs(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_dlp_jobs(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_get_dlp_job(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.get_dlp_job(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.get_dlp_job(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_delete_dlp_job(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.delete_dlp_job(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.delete_dlp_job(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_cancel_dlp_job(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.cancel_dlp_job(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.cancel_dlp_job(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skip(reason="List tests are currently not supported")
    def test_list_job_triggers(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_job_triggers(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_job_triggers(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_get_job_trigger(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.get_job_trigger(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.get_job_trigger(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_delete_job_trigger(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.delete_job_trigger(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.delete_job_trigger(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_update_job_trigger(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.update_job_trigger(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.update_job_trigger(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_create_job_trigger(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.create_job_trigger(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.create_job_trigger(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_create_stored_info_type(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.create_stored_info_type(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.create_stored_info_type(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_update_stored_info_type(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.update_stored_info_type(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.update_stored_info_type(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_get_stored_info_type(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.get_stored_info_type(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.get_stored_info_type(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skip(reason="List tests are currently not supported")
    def test_list_stored_info_types(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_stored_info_types(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_stored_info_types(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_delete_stored_info_type(self):
        client = dlp_v2.DlpServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.delete_stored_info_type(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.delete_stored_info_type(name_outside)
        self._do_test(delayed_inside, delayed_outside)
