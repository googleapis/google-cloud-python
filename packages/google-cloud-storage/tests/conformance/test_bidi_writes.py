import asyncio
import uuid
import grpc
import requests

from google.api_core import exceptions
from google.auth import credentials as auth_credentials
from google.cloud import _storage_v2 as storage_v2

from google.api_core.retry_async import AsyncRetry
from google.cloud.storage._experimental.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)

# --- Configuration ---
PROJECT_NUMBER = "12345"  # A dummy project number is fine for the testbench.
GRPC_ENDPOINT = "localhost:8888"
HTTP_ENDPOINT = "http://localhost:9000"
CONTENT = b"A" * 1024 * 10  # 10 KB


def _is_retryable(exc):
    return isinstance(
        exc,
        (
            exceptions.InternalServerError,
            exceptions.ServiceUnavailable,
            exceptions.DeadlineExceeded,
            exceptions.TooManyRequests,
            exceptions.Aborted,  # For Redirects
        ),
    )


async def run_test_scenario(
    gapic_client,
    http_client,
    bucket_name,
    object_name,
    scenario,
):
    """Runs a single fault-injection test scenario."""
    print(f"\n--- RUNNING SCENARIO: {scenario['name']} ---")
    retry_count = 0

    def on_retry_error(exc):
        nonlocal retry_count
        retry_count += 1
        print(f"Retry attempt {retry_count} triggered by: {type(exc).__name__}")

    custom_retry = AsyncRetry(
        predicate=_is_retryable,
        on_error=on_retry_error,
        initial=0.1,  # Short backoff for fast tests
        multiplier=1.0,
    )

    use_default = scenario.get("use_default_policy", False)
    policy_to_pass = None if use_default else custom_retry

    retry_test_id = None
    try:
        # 1. Create a Retry Test resource on the testbench.
        retry_test_config = {
            "instructions": {scenario["method"]: [scenario["instruction"]]},
            "transport": "GRPC",
        }
        resp = http_client.post(f"{HTTP_ENDPOINT}/retry_test", json=retry_test_config)
        resp.raise_for_status()
        retry_test_id = resp.json()["id"]

        # 2. Set up writer and metadata for fault injection.
        writer = AsyncAppendableObjectWriter(
            gapic_client,
            bucket_name,
            object_name,
        )
        fault_injection_metadata = (("x-retry-test-id", retry_test_id),)

        # 3. Execute the write and assert the outcome.
        try:
            await writer.open(
                metadata=fault_injection_metadata, retry_policy=policy_to_pass
            )
            await writer.append(
                CONTENT, metadata=fault_injection_metadata, retry_policy=policy_to_pass
            )
            # await writer.finalize()
            await writer.close(finalize_on_close=True)

            # If an exception was expected, this line should not be reached.
            if scenario["expected_error"] is not None:
                raise AssertionError(
                    f"Expected exception {scenario['expected_error']} was not raised."
                )

            # 4. Verify the object content.
            read_request = storage_v2.ReadObjectRequest(
                bucket=f"projects/_/buckets/{bucket_name}",
                object=object_name,
            )
            read_stream = await gapic_client.read_object(request=read_request)
            data = b""
            async for chunk in read_stream:
                data += chunk.checksummed_data.content
            assert data == CONTENT
            if scenario["expected_error"] is None:
                # Scenarios like 503, 500, smarter resumption, and redirects
                # SHOULD trigger at least one retry attempt.
                if not use_default:
                    assert (
                        retry_count > 0
                    ), f"Test passed but no retry was actually triggered for {scenario['name']}!"
                else:
                    print("Successfully recovered using library's default policy.")
                print(f"Success: {scenario['name']}")

        except Exception as e:
            if scenario["expected_error"] is None or not isinstance(
                e, scenario["expected_error"]
            ):
                raise

            if not use_default:
                assert (
                    retry_count == 0
                ), f"Retry was incorrectly triggered for non-retriable error in {scenario['name']}!"
                print(f"Success: caught expected exception for {scenario['name']}: {e}")

    finally:
        # 5. Clean up the Retry Test resource.
        if retry_test_id:
            http_client.delete(f"{HTTP_ENDPOINT}/retry_test/{retry_test_id}")


async def main():
    """Main function to set up resources and run all test scenarios."""
    channel = grpc.aio.insecure_channel(GRPC_ENDPOINT)
    creds = auth_credentials.AnonymousCredentials()
    transport = storage_v2.services.storage.transports.StorageGrpcAsyncIOTransport(
        channel=channel,
        credentials=creds,
    )
    gapic_client = storage_v2.StorageAsyncClient(transport=transport)
    http_client = requests.Session()

    bucket_name = f"grpc-test-bucket-{uuid.uuid4().hex[:8]}"
    object_name_prefix = "retry-test-object-"

    # Define all test scenarios
    test_scenarios = [
        {
            "name": "Retry on Service Unavailable (503)",
            "method": "storage.objects.insert",
            "instruction": "return-503",
            "expected_error": None,
        },
        {
            "name": "Retry on 500",
            "method": "storage.objects.insert",
            "instruction": "return-500",
            "expected_error": None,
        },
        {
            "name": "Retry on 504",
            "method": "storage.objects.insert",
            "instruction": "return-504",
            "expected_error": None,
        },
        {
            "name": "Retry on 429",
            "method": "storage.objects.insert",
            "instruction": "return-429",
            "expected_error": None,
        },
        {
            "name": "Smarter Resumption: Retry 503 after partial data",
            "method": "storage.objects.insert",
            "instruction": "return-503-after-2K",
            "expected_error": None,
        },
        {
            "name": "Retry on BidiWriteObjectRedirectedError",
            "method": "storage.objects.insert",
            "instruction": "redirect-send-handle-and-token-tokenval",
            "expected_error": None,
        },
        {
            "name": "Fail on 401",
            "method": "storage.objects.insert",
            "instruction": "return-401",
            "expected_error": exceptions.Unauthorized,
        },
        {
            "name": "Default Policy: Retry on 503",
            "method": "storage.objects.insert",
            "instruction": "return-503",
            "expected_error": None,
            "use_default_policy": True,
        },
        {
            "name": "Default Policy: Retry on 503",
            "method": "storage.objects.insert",
            "instruction": "return-500",
            "expected_error": None,
            "use_default_policy": True,
        },
        {
            "name": "Default Policy: Retry on BidiWriteObjectRedirectedError",
            "method": "storage.objects.insert",
            "instruction": "redirect-send-handle-and-token-tokenval",
            "expected_error": None,
            "use_default_policy": True,
        },
        {
            "name": "Default Policy: Smarter Ressumption",
            "method": "storage.objects.insert",
            "instruction": "return-503-after-2K",
            "expected_error": None,
            "use_default_policy": True,
        },
    ]

    try:
        bucket_resource = storage_v2.Bucket(project=f"projects/{PROJECT_NUMBER}")
        create_bucket_request = storage_v2.CreateBucketRequest(
            parent="projects/_", bucket_id=bucket_name, bucket=bucket_resource
        )
        await gapic_client.create_bucket(request=create_bucket_request)

        for i, scenario in enumerate(test_scenarios):
            object_name = f"{object_name_prefix}{i}"
            await run_test_scenario(
                gapic_client,
                http_client,
                bucket_name,
                object_name,
                scenario,
            )

    except Exception:
        import traceback

        traceback.print_exc()
    finally:
        # Clean up the test bucket.
        try:
            list_objects_req = storage_v2.ListObjectsRequest(
                parent=f"projects/_/buckets/{bucket_name}",
            )
            list_objects_res = await gapic_client.list_objects(request=list_objects_req)
            async for obj in list_objects_res:
                delete_object_req = storage_v2.DeleteObjectRequest(
                    bucket=f"projects/_/buckets/{bucket_name}", object=obj.name
                )
                await gapic_client.delete_object(request=delete_object_req)

            delete_bucket_req = storage_v2.DeleteBucketRequest(
                name=f"projects/_/buckets/{bucket_name}"
            )
            await gapic_client.delete_bucket(request=delete_bucket_req)
        except Exception as e:
            print(f"Warning: Cleanup failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
