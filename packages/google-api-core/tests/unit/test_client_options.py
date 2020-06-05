# Copyright 2019 Google LLC
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

import pytest

from google.api_core import client_options


def get_client_cert():
    return b"cert", b"key"


def get_client_encrypted_cert():
    return "cert_path", "key_path", b"passphrase"


def test_constructor():

    options = client_options.ClientOptions(
        api_endpoint="foo.googleapis.com",
        client_cert_source=get_client_cert,
        quota_project_id="quote-proj",
        credentials_file="path/to/credentials.json",
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/cloud-platform.read-only",
        ]
    )

    assert options.api_endpoint == "foo.googleapis.com"
    assert options.client_cert_source() == (b"cert", b"key")
    assert options.quota_project_id == "quote-proj"
    assert options.credentials_file == "path/to/credentials.json"
    assert options.scopes == [
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
    ]


def test_constructor_with_encrypted_cert_source():

    options = client_options.ClientOptions(
        api_endpoint="foo.googleapis.com",
        client_encrypted_cert_source=get_client_encrypted_cert,
    )

    assert options.api_endpoint == "foo.googleapis.com"
    assert options.client_encrypted_cert_source() == (
        "cert_path",
        "key_path",
        b"passphrase",
    )


def test_constructor_with_both_cert_sources():
    with pytest.raises(ValueError):
        client_options.ClientOptions(
            api_endpoint="foo.googleapis.com",
            client_cert_source=get_client_cert,
            client_encrypted_cert_source=get_client_encrypted_cert,
        )


def test_from_dict():
    options = client_options.from_dict(
        {
            "api_endpoint": "foo.googleapis.com",
            "client_cert_source": get_client_cert,
            "quota_project_id": "quote-proj",
            "credentials_file": "path/to/credentials.json",
            "scopes": [
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ]
        }
    )

    assert options.api_endpoint == "foo.googleapis.com"
    assert options.client_cert_source() == (b"cert", b"key")
    assert options.quota_project_id == "quote-proj"
    assert options.credentials_file == "path/to/credentials.json"
    assert options.scopes == [
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
    ]


def test_from_dict_bad_argument():
    with pytest.raises(ValueError):
        client_options.from_dict(
            {
                "api_endpoint": "foo.googleapis.com",
                "bad_arg": "1234",
                "client_cert_source": get_client_cert,
            }
        )


def test_repr():
    options = client_options.ClientOptions(api_endpoint="foo.googleapis.com")

    assert (
        repr(options)
        == "ClientOptions: {'api_endpoint': 'foo.googleapis.com', 'client_cert_source': None, 'client_encrypted_cert_source': None}"
        or "ClientOptions: {'client_encrypted_cert_source': None, 'client_cert_source': None, 'api_endpoint': 'foo.googleapis.com'}"
    )
