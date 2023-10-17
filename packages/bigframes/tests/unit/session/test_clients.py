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

from typing import Optional
import unittest.mock as mock

import google.api_core.client_info
import google.api_core.client_options
import google.api_core.exceptions
import google.api_core.gapic_v1.client_info
import google.auth.credentials
import google.cloud.bigquery
import google.cloud.bigquery_connection_v1
import google.cloud.bigquery_storage_v1
import google.cloud.functions_v2
import google.cloud.resourcemanager_v3

import bigframes.session.clients as clients
import bigframes.version


def create_clients_provider(application_name: Optional[str] = None):
    credentials = mock.create_autospec(google.auth.credentials.Credentials)
    return clients.ClientsProvider(
        project="test-project",
        location="test-region",
        use_regional_endpoints=False,
        credentials=credentials,
        application_name=application_name,
    )


def monkeypatch_client_constructors(monkeypatch):
    bqclient = mock.create_autospec(google.cloud.bigquery.Client)
    bqclient.return_value = bqclient
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
