# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
#
import pytest
from unittest import mock
from google.cloud.config_v1 import ConfigClient, ConfigAsyncClient
from google.cloud.config_v1.services.config import transports
from google.auth import credentials as ga_credentials

def test_config_client_validates_grpc_asyncio_string():
    creds = ga_credentials.AnonymousCredentials()
    with pytest.raises(ValueError) as excinfo:
        ConfigClient(credentials=creds, transport="grpc_asyncio")
    assert "ConfigClient" in str(excinfo.value)
    assert "async transports" in str(excinfo.value)

def test_config_client_validates_grpc_asyncio_object():
    creds = ga_credentials.AnonymousCredentials()
    transport = transports.ConfigGrpcAsyncIOTransport(credentials=creds)
    with pytest.raises(ValueError) as excinfo:
        ConfigClient(transport=transport)
    assert "ConfigClient" in str(excinfo.value)
    assert "async transports" in str(excinfo.value)

def test_config_client_allows_custom_transport():
    creds = ga_credentials.AnonymousCredentials()
    class CustomTransport(transports.ConfigTransport):
        pass
    transport = CustomTransport(credentials=creds)
    # Should not raise
    ConfigClient(transport=transport)

def test_config_async_client_validates_grpc_string():
    creds = ga_credentials.AnonymousCredentials()
    with pytest.raises(ValueError) as excinfo:
        ConfigAsyncClient(credentials=creds, transport="grpc")
    assert "ConfigAsyncClient" in str(excinfo.value)
    assert "sync transports" in str(excinfo.value)

def test_config_async_client_validates_rest_string():
    creds = ga_credentials.AnonymousCredentials()
    with pytest.raises(ValueError) as excinfo:
        ConfigAsyncClient(credentials=creds, transport="rest")
    assert "ConfigAsyncClient" in str(excinfo.value)
    assert "sync transports" in str(excinfo.value)

def test_config_async_client_validates_grpc_object():
    creds = ga_credentials.AnonymousCredentials()
    transport = transports.ConfigGrpcTransport(credentials=creds)
    with pytest.raises(ValueError) as excinfo:
        ConfigAsyncClient(transport=transport)
    assert "ConfigAsyncClient" in str(excinfo.value)
    assert "sync transports" in str(excinfo.value)

def test_config_async_client_allows_custom_transport():
    creds = ga_credentials.AnonymousCredentials()
    class CustomTransport(transports.ConfigTransport):
        pass
    transport = CustomTransport(credentials=creds)
    # Should not raise
    ConfigAsyncClient(transport=transport)

def test_config_async_client_initialization_happy_path():
    creds = ga_credentials.AnonymousCredentials()
    # Should not raise
    client = ConfigAsyncClient(credentials=creds)
    assert isinstance(client._client, ConfigClient)
