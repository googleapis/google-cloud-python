# Copyright 2026 Google LLC
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
import requests
from google import showcase

@pytest.fixture
def run_pqc_test(use_mtls):
    if not use_mtls:
        pytest.skip("PQC integration test requires mTLS (--mtls flag) to be enabled.")

@pytest.mark.parametrize(
    "transport_fixture",
    ["intercepted_echo_grpc", "intercepted_echo_rest"]
)
def test_pqc_negotiated_group(run_pqc_test, request, transport_fixture):
    """Verifies that the generated client library negotiates PQC with the Showcase server."""
    client, interceptor = request.getfixturevalue(transport_fixture)
    
    # Make secure call using the standard client library fixture
    response = client.echo(request=showcase.EchoRequest(content="Verify PQC connection."))
    assert response.content == "Verify PQC connection."
    
    # Extract negotiated group and supported groups from response headers
    negotiated_group = None
    supported_groups = None
    for key, value in interceptor.response_metadata:
        if key.lower() == "x-showcase-tls-group":
            negotiated_group = value
        elif key.lower() == "x-showcase-tls-client-supported-groups":
            supported_groups = value
            
    assert negotiated_group is not None, "Failed: Showcase server did not return negotiated TLS group header."
    assert supported_groups is not None, "Failed: Showcase server did not return client advertised supported groups."
    
    print(f"\n[PQC Verification] ({transport_fixture}) Negotiated TLS Group: {negotiated_group}")
    print(f"[PQC Verification] ({transport_fixture}) Client Advertised Supported Groups: {supported_groups}")
    
    # Enforce PQC compliance (this will fail if not using MLKEM/Kyber)
    assert "MLKEM" in negotiated_group or "Kyber" in negotiated_group, \
        f"Failed: {transport_fixture} Connection is NOT PQC-compliant! Negotiated: {negotiated_group}"


def test_google_auth_transport_pqc(run_pqc_test):
    """Verifies that the google-auth HTTP transport adapter negotiates PQC with the Showcase server."""
    import google.auth.transport.requests
    from google.protobuf.json_format import MessageToJson
    from conftest import HostNameIgnoringAdapter

    # 1. Initialize a standard requests Session with mTLS certs
    session = requests.Session()
    cert_path = "/usr/local/google/home/omairn/git/googleapis/google-cloud-python-dev2/packages/gapic-generator/tests/cert/mtls.crt"
    key_path = "/usr/local/google/home/omairn/git/googleapis/google-cloud-python-dev2/packages/gapic-generator/tests/cert/mtls.key"

    session.verify = cert_path
    session.cert = (cert_path, key_path)
    
    # Bypass localhost hostname mismatch
    session.mount("https://", HostNameIgnoringAdapter())

    # 2. Wrap it in google-auth's Transport Request adapter
    auth_transport = google.auth.transport.requests.Request(session=session)

    # 3. Serialize the request body using the official protobuf JSON serializer
    req = showcase.EchoRequest(content="Verify google-auth transport PQC connection.")
    body = MessageToJson(req, including_default_value_fields=True).encode("utf-8")

    # 4. Make secure call using the google-auth transport adapter
    url = "https://localhost:7469/v1beta1/echo:echo"
    method = "POST"
    headers = {"Content-Type": "application/json"}

    # Execute the request through google-auth's transport layer
    response = auth_transport(url=url, method=method, body=body, headers=headers)
    assert response.status == 200

    # 5. Extract TLS group from response headers returned by Showcase
    negotiated_group = response.headers.get("x-showcase-tls-group")
    supported_groups = response.headers.get("x-showcase-tls-client-supported-groups")

    assert negotiated_group is not None, "Failed: Showcase server did not return negotiated TLS group header."
    print(f"\n[google-auth Transport PQC] Negotiated TLS Group: {negotiated_group}")
    print(f"[google-auth Transport PQC] Client Advertised Supported Groups: {supported_groups}")

    # Assert PQC compliance
    assert "MLKEM" in negotiated_group or "Kyber" in negotiated_group, \
        f"Failed: google-auth Transport is NOT PQC-compliant! Negotiated: {negotiated_group}"
