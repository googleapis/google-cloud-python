# Copyright 2023 Google LLC
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

import os
import pathlib
import tempfile
from typing import cast, Optional
import unittest.mock as mock

import google.auth.credentials
import google.cloud.bigquery
import google.cloud.bigquery_connection_v1
import google.cloud.bigquery_storage_v1
import google.cloud.functions_v2
import google.cloud.resourcemanager_v3
import requests.adapters

import bigframes.session.clients as clients
import bigframes.version


def create_clients_provider(application_name: Optional[str] = None, **kwargs):
    credentials = mock.create_autospec(google.auth.credentials.Credentials)
    return clients.ClientsProvider(
        project="test-project",
        location="test-region",
        use_regional_endpoints=False,
        credentials=credentials,
        application_name=application_name,
        bq_kms_key_name="projects/my-project/locations/us/keyRings/myKeyRing/cryptoKeys/myKey",
        **kwargs,
    )


def monkeypatch_client_constructors(monkeypatch):
    bqclient = mock.create_autospec(google.cloud.bigquery.Client)
    bqclient.return_value = bqclient
    # Assume we have a new client library in the unit tests.
    bqclient.default_job_creation_mode = None  # type: ignore
    monkeypatch.setattr(google.cloud.bigquery, "Client", bqclient)

    bqconnectionclient = mock.create_autospec(
        google.cloud.bigquery_connection_v1.ConnectionServiceClient
    )
    bqconnectionclient.return_value = bqconnectionclient
    monkeypatch.setattr(
        google.cloud.bigquery_connection_v1,
        "ConnectionServiceClient",
        bqconnectionclient,
    )

    bqstoragereadclient = mock.create_autospec(
        google.cloud.bigquery_storage_v1.BigQueryReadClient
    )
    bqstoragereadclient.return_value = bqstoragereadclient
    monkeypatch.setattr(
        google.cloud.bigquery_storage_v1, "BigQueryReadClient", bqstoragereadclient
    )

    cloudfunctionsclient = mock.create_autospec(
        google.cloud.functions_v2.FunctionServiceClient
    )
    cloudfunctionsclient.return_value = cloudfunctionsclient
    monkeypatch.setattr(
        google.cloud.functions_v2, "FunctionServiceClient", cloudfunctionsclient
    )

    resourcemanagerclient = mock.create_autospec(
        google.cloud.resourcemanager_v3.ProjectsClient
    )
    resourcemanagerclient.return_value = resourcemanagerclient
    monkeypatch.setattr(
        google.cloud.resourcemanager_v3, "ProjectsClient", resourcemanagerclient
    )


def assert_bqclient_sets_default_job_creation_mode(provider: clients.ClientsProvider):
    bqclient = provider.bqclient
    assert bqclient.default_job_creation_mode == "JOB_CREATION_OPTIONAL"


def assert_constructed_w_user_agent(mock_client: mock.Mock, expected_user_agent: str):
    assert (
        expected_user_agent
        in mock_client.call_args.kwargs["client_info"].to_user_agent()
    )


def assert_clients_w_user_agent(
    provider: clients.ClientsProvider, expected_user_agent: str
):
    assert_constructed_w_user_agent(provider.bqclient, expected_user_agent)
    assert_constructed_w_user_agent(provider.bqconnectionclient, expected_user_agent)
    assert_constructed_w_user_agent(provider.bqstoragereadclient, expected_user_agent)
    assert_constructed_w_user_agent(provider.cloudfunctionsclient, expected_user_agent)
    assert_constructed_w_user_agent(provider.resourcemanagerclient, expected_user_agent)


def assert_constructed_wo_user_agent(
    mock_client: mock.Mock, not_expected_user_agent: str
):
    assert (
        not_expected_user_agent
        not in mock_client.call_args.kwargs["client_info"].to_user_agent()
    )


def assert_clients_wo_user_agent(
    provider: clients.ClientsProvider, not_expected_user_agent: str
):
    assert_constructed_wo_user_agent(provider.bqclient, not_expected_user_agent)
    assert_constructed_wo_user_agent(
        provider.bqconnectionclient, not_expected_user_agent
    )
    assert_constructed_wo_user_agent(
        provider.bqstoragereadclient, not_expected_user_agent
    )
    assert_constructed_wo_user_agent(
        provider.cloudfunctionsclient, not_expected_user_agent
    )
    assert_constructed_wo_user_agent(
        provider.resourcemanagerclient, not_expected_user_agent
    )


def test_requests_transport_adapters_pool_maxsize(monkeypatch):
    monkeypatch_client_constructors(monkeypatch)
    requests_transport_adapters = (
        ("http://", requests.adapters.HTTPAdapter(pool_maxsize=123)),
        ("https://", requests.adapters.HTTPAdapter(pool_maxsize=123)),
    )  # doctest: +SKIP
    provider = create_clients_provider(
        requests_transport_adapters=requests_transport_adapters
    )

    _, kwargs = cast(mock.Mock, provider.bqclient).call_args
    requests_session = kwargs.get("_http")
    adapter: requests.adapters.HTTPAdapter = requests_session.get_adapter(
        "https://bigquery.googleapis.com/"
    )
    assert adapter._pool_maxsize == 123  # type: ignore


def test_user_agent_default(monkeypatch):
    monkeypatch_client_constructors(monkeypatch)
    provider = create_clients_provider(application_name=None)
    assert_clients_w_user_agent(provider, f"bigframes/{bigframes.version.__version__}")


def test_user_agent_custom(monkeypatch):
    monkeypatch_client_constructors(monkeypatch)
    provider = create_clients_provider(application_name="(gpn:testpartner;)")
    assert_clients_w_user_agent(provider, "(gpn:testpartner;)")

    # We still need to include attribution to bigframes, even if there's also a
    # partner using the package.
    assert_clients_w_user_agent(provider, f"bigframes/{bigframes.version.__version__}")


@mock.patch.dict(os.environ, {}, clear=True)
def test_user_agent_not_in_vscode(monkeypatch):
    monkeypatch_client_constructors(monkeypatch)
    provider = create_clients_provider()
    assert_clients_wo_user_agent(provider, "vscode")
    assert_clients_wo_user_agent(provider, "googlecloudtools.cloudcode")

    # We still need to include attribution to bigframes
    assert_clients_w_user_agent(provider, f"bigframes/{bigframes.version.__version__}")


@mock.patch.dict(os.environ, {"VSCODE_PID": "12345"}, clear=True)
def test_user_agent_in_vscode(monkeypatch):
    monkeypatch_client_constructors(monkeypatch)
    provider = create_clients_provider()
    assert_clients_w_user_agent(provider, "vscode")
    assert_clients_wo_user_agent(provider, "googlecloudtools.cloudcode")

    # We still need to include attribution to bigframes
    assert_clients_w_user_agent(provider, f"bigframes/{bigframes.version.__version__}")


@mock.patch.dict(os.environ, {"VSCODE_PID": "12345"}, clear=True)
def test_user_agent_in_vscode_w_extension(monkeypatch):
    monkeypatch_client_constructors(monkeypatch)

    with tempfile.TemporaryDirectory() as tmpdir:
        user_home = pathlib.Path(tmpdir)
        extension_dir = (
            user_home / ".vscode" / "extensions" / "googlecloudtools.cloudcode-0.12"
        )
        extension_config = extension_dir / "package.json"

        # originally extension config does not exist
        assert not extension_config.exists()

        # simulate extension installation by creating extension config on disk
        extension_dir.mkdir(parents=True)
        with open(extension_config, "w") as f:
            f.write("{}")

        with mock.patch("pathlib.Path.home", return_value=user_home):
            provider = create_clients_provider()
            assert_clients_w_user_agent(provider, "vscode")
            assert_clients_w_user_agent(provider, "googlecloudtools.cloudcode")

            # We still need to include attribution to bigframes
            assert_clients_w_user_agent(
                provider, f"bigframes/{bigframes.version.__version__}"
            )


@mock.patch.dict(os.environ, {}, clear=True)
def test_user_agent_not_in_jupyter(monkeypatch):
    monkeypatch_client_constructors(monkeypatch)
    provider = create_clients_provider()
    assert_clients_wo_user_agent(provider, "jupyter")
    assert_clients_wo_user_agent(provider, "bigquery_jupyter_plugin")

    # We still need to include attribution to bigframes
    assert_clients_w_user_agent(provider, f"bigframes/{bigframes.version.__version__}")


@mock.patch.dict(os.environ, {"JPY_PARENT_PID": "12345"}, clear=True)
def test_user_agent_in_jupyter(monkeypatch):
    monkeypatch_client_constructors(monkeypatch)
    provider = create_clients_provider()
    assert_clients_w_user_agent(provider, "jupyter")
    assert_clients_wo_user_agent(provider, "bigquery_jupyter_plugin")

    # We still need to include attribution to bigframes
    assert_clients_w_user_agent(provider, f"bigframes/{bigframes.version.__version__}")


@mock.patch.dict(os.environ, {"JPY_PARENT_PID": "12345"}, clear=True)
def test_user_agent_in_jupyter_with_plugin(monkeypatch):
    monkeypatch_client_constructors(monkeypatch)

    def custom_import_module_side_effect(name, package=None):
        if name == "bigquery_jupyter_plugin":
            return mock.MagicMock()
        else:
            import importlib

            return importlib.import_module(name, package)

    assert isinstance(
        custom_import_module_side_effect("bigquery_jupyter_plugin"), mock.MagicMock
    )
    assert custom_import_module_side_effect("bigframes") is bigframes

    with mock.patch(
        "importlib.import_module", side_effect=custom_import_module_side_effect
    ):
        provider = create_clients_provider()
        assert_clients_w_user_agent(provider, "jupyter")
        assert_clients_w_user_agent(provider, "bigquery_jupyter_plugin")

        # We still need to include attribution to bigframes
        assert_clients_w_user_agent(
            provider, f"bigframes/{bigframes.version.__version__}"
        )
