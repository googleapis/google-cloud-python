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

"""Unit tests for VPC-SC."""

import os
import pytest

from google.api_core import exceptions
from google.cloud import translate_v3beta1
from google.cloud.translate_v3beta1.proto import translation_service_pb2
from google.longrunning import operations_pb2

PROJECT_INSIDE = os.environ.get("PROJECT_ID", None)
PROJECT_OUTSIDE = os.environ.get(
    "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT", None
)
IS_INSIDE_VPCSC = os.environ.get("GOOGLE_CLOUD_TESTS_IN_VPCSC", "false")

class TestVPCServiceControl(object):
    @classmethod
    def setup(self):
        self._client = translate_v3beta1.TranslationServiceClient()
        self._parent_inside = self._client.location_path(PROJECT_INSIDE, 'us-central1')
        self._parent_outside = self._client.location_path(PROJECT_OUTSIDE, 'us-central1')

        def make_glossary_name(project_id):
          return 'projects/{0}/locations/us-central1/glossaries/fake_glossary'.format(project_id)
        self._glossary_name_inside = make_glossary_name(PROJECT_INSIDE)
        self._glossary_name_outside = make_glossary_name(PROJECT_OUTSIDE)

    @staticmethod
    def _is_rejected(call):
        try:
            responses = call()
            print("responses: ", responses)
        except exceptions.PermissionDenied as e:
            print("PermissionDenied Exception: ", e)
            return e.message == "Request is prohibited by organization's policy"
        except Exception as e:
            print("Other Exception: ", e)
            pass
        return False

    @staticmethod
    def _do_test(delayed_inside, delayed_outside):
        if IS_INSIDE_VPCSC.lower() == "true":
            assert TestVPCServiceControl._is_rejected(delayed_outside)
            assert not (TestVPCServiceControl._is_rejected(delayed_inside))
        else:
            assert not (TestVPCServiceControl._is_rejected(delayed_outside))
            assert TestVPCServiceControl._is_rejected(delayed_inside)

    @pytest.mark.skipif(
        IS_INSIDE_VPCSC.lower() != "true",
        reason="To run tests, GOOGLE_CLOUD_TESTS_IN_VPCSC environment variable needs to be set to True",
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_glossary(self):
      def make_glossary(project_id):
        return {'name': 'projects/{0}/locations/us-central1/glossaries/fake_glossary'.format(project_id),
                'language_codes_set': {'language_codes': ['en', 'ja']},
                'input_config': {'gcs_source': {'input_uri': 'gs://fake-bucket/fake_glossary.csv'}}}
      glossary_inside = make_glossary(PROJECT_INSIDE)
      delayed_inside = lambda: self._client.create_glossary(self._parent_inside, glossary_inside)

      glossary_outside = make_glossary(PROJECT_OUTSIDE)
      delayed_outside = lambda: self._client.create_glossary(self._parent_outside, glossary_outside)
      TestVPCServiceControl._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        IS_INSIDE_VPCSC.lower() != "true",
        reason="To run tests, GOOGLE_CLOUD_TESTS_IN_VPCSC environment variable needs to be set to True",
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_glossaries(self):
      # list_glossaries() returns an GRPCIterator instance, and we need to actually iterate through it
      # by calling _next_page() to get real response.
      delayed_inside = lambda: self._client.list_glossaries(self._parent_inside)._next_page()
      delayed_outside = lambda: self._client.list_glossaries(self._parent_outside)._next_page()
      TestVPCServiceControl._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        IS_INSIDE_VPCSC.lower() != "true",
        reason="To run tests, GOOGLE_CLOUD_TESTS_IN_VPCSC environment variable needs to be set to True",
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_glossary(self):
      delayed_inside = lambda: self._client.get_glossary(self._glossary_name_inside)
      delayed_outside = lambda: self._client.get_glossary(self._glossary_name_outside)
      TestVPCServiceControl._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        IS_INSIDE_VPCSC.lower() != "true",
        reason="To run tests, GOOGLE_CLOUD_TESTS_IN_VPCSC environment variable needs to be set to True",
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_delete_glossary(self):
      delayed_inside = lambda: self._client.delete_glossary(self._glossary_name_inside)
      delayed_outside = lambda: self._client.delete_glossary(self._glossary_name_outside)
      TestVPCServiceControl._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        IS_INSIDE_VPCSC.lower() != "true",
        reason="To run tests, GOOGLE_CLOUD_TESTS_IN_VPCSC environment variable needs to be set to True",
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_batch_translate_text(self):
      source_language_code = "en"
      target_language_codes = ["es"]
      input_configs = [{'gcs_source': {'input_uri': 'gs://fake-bucket/*'}}]
      output_config = {'gcs_destination': {'output_uri_prefix': 'gs://fake-bucket/output/'}}
      delayed_inside = lambda: self._client.batch_translate_text(source_language_code, target_language_codes, input_configs, output_config, parent=self._parent_inside)
      delayed_outside = lambda: self._client.batch_translate_text(source_language_code, target_language_codes, input_configs, output_config, parent=self._parent_outside)
      TestVPCServiceControl._do_test(delayed_inside, delayed_outside)
