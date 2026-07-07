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
    """Verifies that the generated client library negotiates PQC (X25519MLKEM768) with Showcase server."""
    client, interceptor = request.getfixturevalue(transport_fixture)

    # Make secure call using standard GAPIC client library fixture
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

    # Enforce PQC compliance (X25519MLKEM768 or Kyber)
    assert "MLKEM" in negotiated_group or "Kyber" in negotiated_group, \
        f"Failed: {transport_fixture} Connection is NOT PQC-compliant! Negotiated: {negotiated_group}"


def test_google_auth_transport_pqc(run_pqc_test):
    """Verifies that google-auth transport adapter negotiates PQC (X25519MLKEM768) with Showcase server."""
    import google.auth.transport.requests
    from conftest import HostNameIgnoringAdapter

    # 1. Initialize requests Session with mTLS certs
    session = requests.Session()
    cert_path = "/usr/local/google/home/omairn/git/googleapis/google-cloud-python-dev2/packages/gapic-generator/tests/cert/mtls.crt"
    key_path = "/usr/local/google/home/omairn/git/googleapis/google-cloud-python-dev2/packages/gapic-generator/tests/cert/mtls.key"

    session.verify = cert_path
    session.cert = (cert_path, key_path)
    session.mount("https://", HostNameIgnoringAdapter())

    # 2. Wrap session in google-auth transport adapter
    auth_transport = google.auth.transport.requests.Request(session=session)

    # 3. Serialize request body
    req = showcase.EchoRequest(content="Verify google-auth transport PQC connection.")
    body = showcase.EchoRequest.to_json(req, including_default_value_fields=False).encode("utf-8")

    # 4. Execute request through google-auth's transport layer
    url = "https://localhost:7469/v1beta1/echo:echo"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-client": "gapic/1.0 rest/1.0",
    }

    response = auth_transport(url=url, method="POST", body=body, headers=headers)
    assert response.status == 200, f"Failed: status={response.status}, body={response.data}"

    # 5. Extract and verify negotiated TLS group returned by Showcase
    negotiated_group = response.headers.get("x-showcase-tls-group")
    supported_groups = response.headers.get("x-showcase-tls-client-supported-groups")

    assert negotiated_group is not None, "Failed: Showcase server did not return negotiated TLS group header."
    print(f"\n[google-auth Transport PQC] Negotiated TLS Group: {negotiated_group}")
    print(f"[google-auth Transport PQC] Client Advertised Supported Groups: {supported_groups}")

    assert "MLKEM" in negotiated_group or "Kyber" in negotiated_group, \
        f"Failed: google-auth Transport is NOT PQC-compliant! Negotiated: {negotiated_group}"
