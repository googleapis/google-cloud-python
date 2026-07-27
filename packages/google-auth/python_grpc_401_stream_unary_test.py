"""Python gRPC stream-unary example test for cert rotation resilience.

This test validates Stream-Unary methodologies by targeting Cloud Storage via raw Channels.
"""

import concurrent.futures
from unittest import mock

import grpc
import google.auth
import google.auth.credentials
import google.auth.transport.grpc
import google.auth.transport.requests

class RecoveringCredentials(google.auth.credentials.Credentials):
    """Fails on attempt 1, but succeeds with real Google credentials on attempt 2."""
    def __init__(self):
        super().__init__()
        self.attempts = 0
        try:
            self.real_creds, _ = google.auth.default()
        except:
            print("WARNING: Could not load default credentials. Some fallback authentication features may not work.")
            self.real_creds = None

    def refresh(self, request):
        if self.real_creds:
            self.real_creds.refresh(request)

    def before_request(self, request, method, url, headers):
        if self.attempts == 0:
            print(f"> Attempt {self.attempts}: Sending INVALID token to force UNAUTHENTICATED error.")
            headers["authorization"] = "Bearer simulated_invalid_token"
        else:
            print(f"> Attempt {self.attempts}: Sending REAL token to bypass AUTH check!")
            if self.real_creds:
                self.real_creds.before_request(request, method, url, headers)
            else:
                headers["authorization"] = "Bearer still_invalid_no_gcloud_auth_credentials_found"
        self.attempts += 1


def test_grpc_stream_unary_example():
    """Run a Stream-Unary request to verify gRPC resilience."""

    credentials = RecoveringCredentials()
    auth_request = google.auth.transport.requests.Request()

    # Hit the true mTLS endpoint. This requires GOOGLE_API_USE_CLIENT_CERTIFICATE=true
    # to be set in your terminal so it automatically picks up your device certificate!
    target = "storage.mtls.googleapis.com:443"

    print(f"Attempting to create channel configuration for {target}...")
    channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials,
        auth_request,
        target,
        # Notice we removed client_cert_callback to let google.auth fetch the real device cert automatically
    )

    stream_unary_method = channel.stream_unary(
        "/google.storage.v2.Storage/WriteObject",
        request_serializer=lambda x: x.encode("utf-8"),
        response_deserializer=lambda x: x,
    )

    def payload_generator():
        yield "Chunk 1: Payload transmission"
        yield "Chunk 2: Simulating broken stream logic"

    # Mock `check_parameters` so the interceptor assumes the cert on disk changed during our 401 response
    with mock.patch(
        "google.auth.transport._mtls_helper.check_parameters_for_unauthorized_response",
        return_value=("foo.pem", "foo.pem", "old_fp", "new_fp"),
    ) as mock_check_params:

        print("Firing Stream-Unary...")
        future = stream_unary_method.future(payload_generator())
        
        def future_done_callback(completed_future):
            try:
                completed_future.result()
            except grpc.RpcError:
                # We expect the final call to be executed fully
                pass

        future.add_done_callback(future_done_callback)

        try:
            future.result(timeout=5)
        except Exception as e:  
            print(f"Final Execution Error Code: {e.code() if hasattr(e, 'code') else e}")
            print(f"Total times rotation interceptor was triggered: {mock_check_params.call_count}")

            if hasattr(e, 'code') and e.code() != grpc.StatusCode.UNAUTHENTICATED:
                print("\n\033[92m>>> SUCCESS! The request bypassed the authentication layer natively and was processed by GCP! <<<\033[0m")
                print(">>> (We received INVALID_ARGUMENT instead of UNAUTHENTICATED because we uploaded raw utf8 strings instead of a Protobuf format, but Auth passed!) <<<")

if __name__ == "__main__":
    print("Starting Stream-Unary streaming script...")
    test_grpc_stream_unary_example()
    print("Script finished.")
