# Copyright 2021 Google LLC All Rights Reserved.
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

import unittest

import mock
import os


from google.cloud.logging_v2.handlers._monitored_resources import (
    _create_functions_resource,
)
from google.cloud.logging_v2.handlers._monitored_resources import (
    _create_app_engine_resource,
)
from google.cloud.logging_v2.handlers._monitored_resources import (
    _create_kubernetes_resource,
)
from google.cloud.logging_v2.handlers._monitored_resources import (
    _create_cloud_run_resource,
)
from google.cloud.logging_v2.handlers._monitored_resources import (
    _create_compute_resource,
)
from google.cloud.logging_v2.handlers._monitored_resources import (
    _create_global_resource,
)
from google.cloud.logging_v2.handlers._monitored_resources import detect_resource
from google.cloud.logging_v2.handlers import _monitored_resources
from google.cloud.logging_v2.resource import Resource


class Test_Create_Resources(unittest.TestCase):

    PROJECT = "test-project"
    LOCATION = "test-location"
    NAME = "test-name"
    CLUSTER = "test-cluster"
    VERSION = "1"
    CONFIG = "test-config"

    def _mock_metadata(self, endpoint):
        if (
            endpoint == _monitored_resources._ZONE_ID
            or endpoint == _monitored_resources._REGION_ID
        ):
            return self.LOCATION
        elif (
            endpoint == _monitored_resources._GKE_CLUSTER_NAME
            or endpoint == _monitored_resources._GCE_INSTANCE_ID
        ):
            return self.NAME
        else:
            return None

    def setUp(self):
        os.environ.clear()

    def test_create_legacy_functions_resource(self):
        patch = mock.patch(
            "google.cloud.logging_v2.handlers._monitored_resources.retrieve_metadata_server",
            wraps=self._mock_metadata,
        )

        os.environ[_monitored_resources._CLOUD_RUN_SERVICE_ID] = self.NAME
        with patch:
            legacy_func_resource = _create_functions_resource(self.PROJECT)

            self.assertIsInstance(legacy_func_resource, Resource)
            self.assertEqual(legacy_func_resource.type, "cloud_function")
            self.assertEqual(legacy_func_resource.labels["project_id"], self.PROJECT)
            self.assertEqual(legacy_func_resource.labels["function_name"], self.NAME)
            self.assertEqual(legacy_func_resource.labels["region"], self.LOCATION)

    def test_create_modern_functions_resource(self):
        patch = mock.patch(
            "google.cloud.logging_v2.handlers._monitored_resources.retrieve_metadata_server",
            wraps=self._mock_metadata,
        )
        os.environ[_monitored_resources._FUNCTION_NAME] = self.NAME
        with patch:
            func_resource = _create_functions_resource(self.PROJECT)

            self.assertIsInstance(func_resource, Resource)
            self.assertEqual(func_resource.type, "cloud_function")
            self.assertEqual(func_resource.labels["project_id"], self.PROJECT)
            self.assertEqual(func_resource.labels["function_name"], self.NAME)
            self.assertEqual(func_resource.labels["region"], self.LOCATION)

    def test_create_kubernetes_resource(self):

        patch = mock.patch(
            "google.cloud.logging_v2.handlers._monitored_resources.retrieve_metadata_server",
            wraps=self._mock_metadata,
        )
        with patch:
            resource = _create_kubernetes_resource(self.PROJECT)

            self.assertIsInstance(resource, Resource)
            self.assertEqual(resource.type, "k8s_container")
            self.assertEqual(resource.labels["project_id"], self.PROJECT)
            self.assertEqual(resource.labels["cluster_name"], self.NAME)
            self.assertEqual(resource.labels["location"], self.LOCATION)

    def test_compute_resource(self):
        patch = mock.patch(
            "google.cloud.logging_v2.handlers._monitored_resources.retrieve_metadata_server",
            wraps=self._mock_metadata,
        )

        with patch:
            resource = _create_compute_resource(self.PROJECT)
            self.assertIsInstance(resource, Resource)
            self.assertEqual(resource.type, "gce_instance")
            self.assertEqual(resource.labels["project_id"], self.PROJECT)
            self.assertEqual(resource.labels["instance_id"], self.NAME)
            self.assertEqual(resource.labels["zone"], self.LOCATION)

    def test_cloud_run_resource(self):
        patch = mock.patch(
            "google.cloud.logging_v2.handlers._monitored_resources.retrieve_metadata_server",
            wraps=self._mock_metadata,
        )
        os.environ[_monitored_resources._CLOUD_RUN_SERVICE_ID] = self.NAME
        os.environ[_monitored_resources._CLOUD_RUN_REVISION_ID] = self.VERSION
        os.environ[_monitored_resources._CLOUD_RUN_CONFIGURATION_ID] = self.CONFIG
        with patch:
            resource = _create_cloud_run_resource(self.PROJECT)
            self.assertIsInstance(resource, Resource)
            self.assertEqual(resource.type, "cloud_run_revision")
            self.assertEqual(resource.labels["project_id"], self.PROJECT)
            self.assertEqual(resource.labels["service_name"], self.NAME)
            self.assertEqual(resource.labels["revision_name"], self.VERSION)
            self.assertEqual(resource.labels["configuration_name"], self.CONFIG)
            self.assertEqual(resource.labels["location"], self.LOCATION)

    def test_app_engine_resource(self):
        patch = mock.patch(
            "google.cloud.logging_v2.handlers._monitored_resources.retrieve_metadata_server",
            wraps=self._mock_metadata,
        )
        os.environ[_monitored_resources._GAE_SERVICE_ENV] = self.NAME
        os.environ[_monitored_resources._GAE_VERSION_ENV] = self.VERSION
        with patch:
            resource = _create_app_engine_resource(self.PROJECT)
            self.assertIsInstance(resource, Resource)
            self.assertEqual(resource.type, "gae_app")
            self.assertEqual(resource.labels["project_id"], self.PROJECT)
            self.assertEqual(resource.labels["module_id"], self.NAME)
            self.assertEqual(resource.labels["version_id"], self.VERSION)
            self.assertEqual(resource.labels["zone"], self.LOCATION)

    def test_global_resource(self):
        resource = _create_global_resource(self.PROJECT)
        self.assertIsInstance(resource, Resource)
        self.assertEqual(resource.type, "global")
        self.assertEqual(resource.labels["project_id"], self.PROJECT)


class Test_Resource_Detection(unittest.TestCase):

    PROJECT = "test-project"

    def _mock_k8s_metadata(self, endpoint):
        if (
            endpoint == _monitored_resources._GKE_CLUSTER_NAME
            or endpoint == _monitored_resources._GCE_INSTANCE_ID
        ):
            return "TRUE"
        else:
            return None

    def _mock_gce_metadata(self, endpoint):
        if endpoint == _monitored_resources._GCE_INSTANCE_ID:
            return "TRUE"
        else:
            return None

    def setUp(self):
        os.environ.clear()

    def test_detect_appengine(self):
        for env in _monitored_resources._GAE_ENV_VARS:
            os.environ[env] = "TRUE"
        resource = detect_resource(self.PROJECT)
        self.assertIsInstance(resource, Resource)
        self.assertEqual(resource.type, "gae_app")

    def test_detect_kubernetes(self):
        patch = mock.patch(
            "google.cloud.logging_v2.handlers._monitored_resources.retrieve_metadata_server",
            wraps=self._mock_k8s_metadata,
        )
        with patch:
            resource = detect_resource(self.PROJECT)
            self.assertIsInstance(resource, Resource)
            self.assertEqual(resource.type, "k8s_container")

    def test_detect_functions(self):
        for env in _monitored_resources._FUNCTION_ENV_VARS:
            os.environ[env] = "TRUE"
        resource = detect_resource(self.PROJECT)
        self.assertIsInstance(resource, Resource)
        self.assertEqual(resource.type, "cloud_function")

    def test_detect_legacy_functions(self):
        for env in _monitored_resources._LEGACY_FUNCTION_ENV_VARS:
            os.environ[env] = "TRUE"
        resource = detect_resource(self.PROJECT)
        self.assertIsInstance(resource, Resource)
        self.assertEqual(resource.type, "cloud_function")

    def test_detect_cloud_run(self):
        for env in _monitored_resources._CLOUD_RUN_ENV_VARS:
            os.environ[env] = "TRUE"
        resource = detect_resource(self.PROJECT)
        self.assertIsInstance(resource, Resource)
        self.assertEqual(resource.type, "cloud_run_revision")

    def test_detect_compute_engine(self):
        patch = mock.patch(
            "google.cloud.logging_v2.handlers._monitored_resources.retrieve_metadata_server",
            wraps=self._mock_gce_metadata,
        )
        with patch:
            resource = detect_resource(self.PROJECT)
            self.assertIsInstance(resource, Resource)
            self.assertEqual(resource.type, "gce_instance")

    def test_detection_unknown(self):
        patch = mock.patch(
            "google.cloud.logging_v2.handlers._monitored_resources.retrieve_metadata_server",
            return_value=None,
        )
        with patch:
            resource = detect_resource(self.PROJECT)
            self.assertIsInstance(resource, Resource)
            self.assertEqual(resource.type, "global")
