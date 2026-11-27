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
from unittest import mock

import pytest
from google.api_core import universe
from google.api_core.client_options import ClientOptions
from google.auth import compute_engine, credentials
from google.cloud.datastore import _http

from google.cloud import environment_vars
from google.cloud.ndb import _eventloop
from google.cloud.ndb import client as client_module
from google.cloud.ndb import context as context_module


@contextlib.contextmanager
def patch_credentials(project):
    creds = mock.Mock(spec=credentials.Credentials)
    patch = mock.patch("google.auth.default", return_value=(creds, project))
    with patch:
        yield creds


class TestClient:
    @staticmethod
    def test_constructor_no_args():
        patch_environ = mock.patch.dict(
            "google.cloud.ndb.client.os.environ", {}, clear=True
        )
        with patch_environ:
            with patch_credentials("testing"):
                client = client_module.Client()
        assert client.SCOPE == ("https://www.googleapis.com/auth/datastore",)
        assert client.host == _http.DATASTORE_API_HOST
        assert client.project == "testing"
        assert client.database is None
        assert client.namespace is None
        assert client.secure is True

    @staticmethod
    def test_constructor_no_args_emulator():
        patch_environ = mock.patch.dict(
            "google.cloud.ndb.client.os.environ",
            {"DATASTORE_EMULATOR_HOST": "foo"},
            clear=True,
        )
        with patch_environ:
            with patch_credentials("testing"):
                client = client_module.Client()
        assert client.SCOPE == ("https://www.googleapis.com/auth/datastore",)
        assert client.host == "foo"
        assert client.project == "testing"
        assert client.database is None
        assert client.namespace is None
        assert client.secure is False

    @staticmethod
    def test_constructor_get_project_from_environ(environ):
        patch_environ = mock.patch.dict(
            "google.cloud.ndb.client.os.environ",
            {environment_vars.GCD_DATASET: "gcd-project"},
            clear=True,
        )
        with patch_environ:
            with patch_credentials(None):
                client = client_module.Client()
        assert client.project == "gcd-project"

    @staticmethod
    def test_constructor_all_args():
        with patch_credentials("testing") as creds:
            client = client_module.Client(
                project="test-project",
                database="test-database",
                namespace="test-namespace",
                credentials=creds,
                client_options=ClientOptions(
                    api_endpoint="alternate-endpoint.example.com"
                ),
            )
        assert client.project == "test-project"
        assert client.database == "test-database"
        assert client.namespace == "test-namespace"
        assert client.host == "alternate-endpoint.example.com"
        assert client.secure is True

    @staticmethod
    def test_constructor_client_options_as_dict():
        with patch_credentials("testing") as creds:
            client = client_module.Client(
                project="test-project",
                database="test-database",
                namespace="test-namespace",
                credentials=creds,
                client_options={"api_endpoint": "alternate-endpoint.example.com"},
            )
        assert client.project == "test-project"
        assert client.database == "test-database"
        assert client.namespace == "test-namespace"
        assert client.host == "alternate-endpoint.example.com"
        assert client.secure is True

    @staticmethod
    def test_constructor_client_options_no_api_endpoint():
        with patch_credentials("testing") as creds:
            client = client_module.Client(
                project="test-project",
                database="test-database",
                namespace="test-namespace",
                credentials=creds,
                client_options={"scopes": ["my_scope"]},
            )
        assert client.project == "test-project"
        assert client.database == "test-database"
        assert client.namespace == "test-namespace"
        assert client.host == _http.DATASTORE_API_HOST
        assert client.secure is True

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

    @staticmethod
    def test_context():
        with patch_credentials("testing"):
            client = client_module.Client()

        with client.context():
            context = context_module.get_context()
            assert context.client is client

    @staticmethod
    def test_context_double_jeopardy():
        with patch_credentials("testing"):
            client = client_module.Client()

        with client.context():
            with pytest.raises(RuntimeError):
                client.context().__enter__()

    @staticmethod
    def test_context_unfinished_business():
        """Regression test for #213.

        Make sure the eventloop is exhausted inside the context.

        https://github.com/googleapis/python-ndb/issues/213
        """
        with patch_credentials("testing"):
            client = client_module.Client()

        def finish_up():
            context = context_module.get_context()
            assert context.client is client

        with client.context():
            _eventloop.call_soon(finish_up)

    @staticmethod
    def test_client_info():
        with patch_credentials("testing"):
            client = client_module.Client()
        agent = client.client_info.to_user_agent()
        assert "google-cloud-ndb" in agent
        version = agent.split("/")[1]
        assert version[0].isdigit()
        assert "." in version

    @staticmethod
    @pytest.mark.parametrize(
        "client_options",
        [
            ClientOptions(universe_domain="my-universe.com"),
            {"universe_domain": "my-universe.com"},
        ],
    )
    def test_constructor_universe_domain_from_client_options(client_options):
        creds = mock.Mock(spec=credentials.Credentials)
        creds.universe_domain = "my-universe.com"
        with mock.patch(
            "google.cloud.ndb.client._helpers.make_secure_channel"
        ) as make_channel:
            client = client_module.Client(
                project="testing",
                credentials=creds,
                client_options=client_options,
            )
        assert client.universe_domain == "my-universe.com"
        assert client.host == "datastore.my-universe.com"
        assert client.secure is True
        make_channel.assert_called_once_with(
            creds, client.client_info.to_user_agent(), "datastore.my-universe.com"
        )

    @staticmethod
    def test_constructor_universe_domain_from_env():
        creds = mock.Mock(spec=credentials.Credentials)
        creds.universe_domain = "env-universe.com"
        patch_environ = mock.patch.dict(
            "google.cloud.ndb.client.os.environ",
            {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "env-universe.com"},
            clear=True,
        )
        with patch_environ:
            client = client_module.Client(project="testing", credentials=creds)
        assert client.universe_domain == "env-universe.com"
        assert client.host == "datastore.env-universe.com"

    @staticmethod
    def test_constructor_universe_domain_precedence():
        creds = mock.Mock(spec=credentials.Credentials)
        creds.universe_domain = "opts-universe.com"
        patch_environ = mock.patch.dict(
            "google.cloud.ndb.client.os.environ",
            {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "env-universe.com"},
            clear=True,
        )
        with patch_environ:
            client = client_module.Client(
                project="testing",
                credentials=creds,
                client_options=ClientOptions(universe_domain="opts-universe.com"),
            )
        assert client.universe_domain == "opts-universe.com"
        assert client.host == "datastore.opts-universe.com"

    @staticmethod
    def test_constructor_api_endpoint_overrides_universe_template():
        creds = mock.Mock(spec=credentials.Credentials)
        creds.universe_domain = "my-universe.com"
        client = client_module.Client(
            project="testing",
            credentials=creds,
            client_options=ClientOptions(
                universe_domain="my-universe.com",
                api_endpoint="custom.endpoint.test:443",
            ),
        )
        assert client.universe_domain == "my-universe.com"
        assert client.host == "custom.endpoint.test:443"

    @staticmethod
    @pytest.mark.parametrize(
        "client_options,env_universe",
        [
            (ClientOptions(universe_domain=""), None),
            ({"universe_domain": "   "}, None),
            (None, ""),
            (None, "   "),
        ],
    )
    def test_constructor_empty_universe_domain_raises(client_options, env_universe):
        env = (
            {}
            if env_universe is None
            else {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": env_universe}
        )
        patch_environ = mock.patch.dict(
            "google.cloud.ndb.client.os.environ", env, clear=True
        )
        with patch_environ:
            with patch_credentials("testing"):
                with pytest.raises(universe.EmptyUniverseError):
                    client_module.Client(client_options=client_options)

    @staticmethod
    @pytest.mark.parametrize(
        "client_options,env_universe,cred_universe",
        [
            (None, None, "tpc.test"),
            (ClientOptions(universe_domain="tpc.test"), None, "googleapis.com"),
            (None, "tpc.test", "googleapis.com"),
        ],
    )
    def test_constructor_universe_mismatch_raises_before_channel(
        client_options, env_universe, cred_universe
    ):
        creds = mock.Mock(spec=credentials.Credentials)
        creds.universe_domain = cred_universe
        env = (
            {}
            if env_universe is None
            else {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": env_universe}
        )
        patch_environ = mock.patch.dict(
            "google.cloud.ndb.client.os.environ", env, clear=True
        )
        with (
            patch_environ,
            mock.patch("google.auth.default", return_value=(creds, "testing")),
            mock.patch(
                "google.cloud.ndb.client._helpers.make_secure_channel"
            ) as make_channel,
        ):
            with pytest.raises(universe.UniverseMismatchError):
                client_module.Client(client_options=client_options)
        make_channel.assert_not_called()

    @staticmethod
    def test_constructor_emulator_exempt_from_universe_mismatch():
        creds = mock.Mock(spec=credentials.Credentials)
        creds.universe_domain = "tpc.test"
        patch_environ = mock.patch.dict(
            "google.cloud.ndb.client.os.environ",
            {"DATASTORE_EMULATOR_HOST": "localhost:8081"},
            clear=True,
        )
        with patch_environ:
            client = client_module.Client(project="testing", credentials=creds)
        assert client.host == "localhost:8081"
        assert client.secure is False

    @staticmethod
    def test_constructor_anonymous_credentials_exempt_from_universe_mismatch():
        creds = credentials.AnonymousCredentials()
        client = client_module.Client(
            project="testing",
            credentials=creds,
            client_options=ClientOptions(universe_domain="tpc.test"),
        )
        assert client.universe_domain == "tpc.test"
        assert client.host == "datastore.tpc.test"

    @staticmethod
    def test_constructor_uncached_compute_engine_credentials_exempt():
        creds = compute_engine.Credentials()
        assert not getattr(creds, "_universe_domain_cached", False)
        client = client_module.Client(
            project="testing",
            credentials=creds,
            client_options=ClientOptions(universe_domain="tpc.test"),
        )
        assert client.universe_domain == "tpc.test"
        assert client.host == "datastore.tpc.test"

    @staticmethod
    def test_constructor_cached_compute_engine_credentials_mismatch_raises():
        creds = compute_engine.Credentials()
        creds._universe_domain = "googleapis.com"
        creds._universe_domain_cached = True
        with pytest.raises(universe.UniverseMismatchError):
            client_module.Client(
                project="testing",
                credentials=creds,
                client_options=ClientOptions(universe_domain="tpc.test"),
            )
