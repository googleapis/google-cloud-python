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
