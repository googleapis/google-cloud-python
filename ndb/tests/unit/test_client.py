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

import contextlib
import pytest

from unittest import mock

from google.auth import credentials
from google.cloud import environment_vars
from google.cloud.ndb import client as client_module


@contextlib.contextmanager
def patch_credentials(project):
    creds = mock.Mock(spec=credentials.Credentials)
    patch = mock.patch("google.auth.default", return_value=(creds, project))
    with patch:
        yield creds


class TestClient:
    @staticmethod
    def test_constructor_no_args():
        with patch_credentials("testing"):
            client = client_module.Client()
        assert client.SCOPE == ("https://www.googleapis.com/auth/datastore",)
        assert client.namespace is None
        assert client.host == client_module._DATASTORE_HOST
        assert client.project == "testing"

    @staticmethod
    def test_constructor_get_project_from_environ(environ):
        environ[environment_vars.GCD_DATASET] = "gcd-project"
        with patch_credentials(None):
            client = client_module.Client()
        assert client.project == "gcd-project"

    @staticmethod
    def test_constructor_all_args():
        with patch_credentials("testing") as creds:
            client = client_module.Client(
                project="test-project",
                namespace="test-namespace",
                credentials=creds,
            )
        assert client.namespace == "test-namespace"
        assert client.project == "test-project"

    @staticmethod
    def test__determine_default():
        with patch_credentials("testing"):
            client = client_module.Client()
        assert client._determine_default("this") == "this"

    @staticmethod
    def test__http():
        with patch_credentials("testing"):
            client = client_module.Client()
        with pytest.raises(NotImplementedError):
            client._http
