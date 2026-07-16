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

import grpc
from packaging.version import Version
import pytest
from google import showcase


@pytest.fixture
def run_pqc_test(use_tls):
    if not use_tls:
        pytest.skip("PQC integration test requires TLS (--tls or --mtls flag) to be enabled.")


def _verify_pqc_negotiated_group(client, interceptor, transport_name):
    # Make secure call using standard GAPIC client library fixture
    response = client.echo(request=showcase.EchoRequest(content="Verify PQC connection."))
    assert response.content == "Verify PQC connection."

    # Extract negotiated group and supported groups from response headers
    response_metadata = getattr(interceptor, "response_metadata", []) or []
    headers = {key.lower(): value for key, value in response_metadata}
    negotiated_group = headers.get("x-showcase-tls-group")
    supported_groups = headers.get("x-showcase-tls-client-supported-groups")

    assert negotiated_group is not None, "Failed: Showcase server did not return negotiated TLS group header."
    assert supported_groups is not None, "Failed: Showcase server did not return client advertised supported groups."

    print(f"\n[PQC Verification] ({transport_name}) Negotiated TLS Group: {negotiated_group}")
    print(f"[PQC Verification] ({transport_name}) Client Advertised Supported Groups: {supported_groups}")

    # Enforce PQC compliance (X25519MLKEM768 or Kyber)
    assert "MLKEM" in negotiated_group or "Kyber" in negotiated_group, \
        f"Failed: {transport_name} Connection is NOT PQC-compliant! Negotiated: {negotiated_group}"


def test_pqc_grpc(run_pqc_test, intercepted_echo_grpc):
    """Verifies that the gRPC client library negotiates PQC (X25519MLKEM768) with Showcase server."""
    # TODO(Phase 3): Remove this check once grpcio >= 1.83.0 is enforced across all client libraries.
    if Version(grpc.__version__) < Version("1.83.0rc0"):
        pytest.skip(f"gRPC PQC negotiation requires grpcio >= 1.83.0 (current: {grpc.__version__})")

    client, interceptor = intercepted_echo_grpc
    _verify_pqc_negotiated_group(client, interceptor, "grpc")


def test_pqc_rest(run_pqc_test, intercepted_echo_rest):
    """Verifies that the REST client library negotiates PQC (X25519MLKEM768) with Showcase server."""
    client, interceptor = intercepted_echo_rest
    _verify_pqc_negotiated_group(client, interceptor, "rest")


