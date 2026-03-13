import asyncio
import io
import uuid
import grpc
import requests

from google.api_core import exceptions
from google.auth import credentials as auth_credentials
from google.cloud import _storage_v2 as storage_v2

from google.cloud.storage._experimental.asyncio.async_multi_range_downloader import (
    AsyncMultiRangeDownloader,
)

# --- Configuration ---
PROJECT_NUMBER = "12345"  # A dummy project number is fine for the testbench.
GRPC_ENDPOINT = "localhost:8888"
HTTP_ENDPOINT = "http://localhost:9000"
CONTENT_LENGTH = 1024 * 10  # 10 KB


def _is_retriable(exc):
    """Predicate for identifying retriable errors."""
    return isinstance(
        exc,
        (
            exceptions.ServiceUnavailable,
            exceptions.Aborted,  # Required to retry on redirect
            exceptions.InternalServerError,
            exceptions.ResourceExhausted,
        ),
    )


async def run_test_scenario(
    gapic_client, http_client, bucket_name, object_name, scenario
):
    """Runs a single fault-injection test scenario."""
    print(f"\n--- RUNNING SCENARIO: {scenario['name']} ---")

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

        # 2. Set up downloader and metadata for fault injection.
        downloader = await AsyncMultiRangeDownloader.create_mrd(
            gapic_client, bucket_name, object_name
        )
        fault_injection_metadata = (("x-retry-test-id", retry_test_id),)

        buffer = io.BytesIO()

        # 3. Execute the download and assert the outcome.
        try:
            await downloader.download_ranges(
                [(0, 5 * 1024, buffer), (6 * 1024, 4 * 1024, buffer)],
                metadata=fault_injection_metadata,
            )
            # If an exception was expected, this line should not be reached.
            if scenario["expected_error"] is not None:
                raise AssertionError(
                    f"Expected exception {scenario['expected_error']} was not raised."
                )

            assert len(buffer.getvalue()) == 9 * 1024

        except scenario["expected_error"] as e:
            print(f"Caught expected exception for {scenario['name']}: {e}")

        await downloader.close()

    finally:
        # 4. Clean up the Retry Test resource.
        if retry_test_id:
            http_client.delete(f"{HTTP_ENDPOINT}/retry_test/{retry_test_id}")


async def main():
    """Main function to set up resources and run all test scenarios."""
    channel = grpc.aio.insecure_channel(GRPC_ENDPOINT)
    creds = auth_credentials.AnonymousCredentials()
    transport = storage_v2.services.storage.transports.StorageGrpcAsyncIOTransport(
        channel=channel, credentials=creds
    )
    gapic_client = storage_v2.StorageAsyncClient(transport=transport)
    http_client = requests.Session()

    bucket_name = f"grpc-test-bucket-{uuid.uuid4().hex[:8]}"
    object_name = "retry-test-object"

    # Define all test scenarios
    test_scenarios = [
        {
            "name": "Retry on Service Unavailable (503)",
            "method": "storage.objects.get",
            "instruction": "return-503",
            "expected_error": None,
        },
        {
            "name": "Retry on 500",
            "method": "storage.objects.get",
            "instruction": "return-500",
            "expected_error": None,
        },
        {
            "name": "Retry on 504",
            "method": "storage.objects.get",
            "instruction": "return-504",
            "expected_error": None,
        },
        {
            "name": "Retry on 429",
            "method": "storage.objects.get",
            "instruction": "return-429",
            "expected_error": None,
        },
        {
            "name": "Smarter Resumption: Retry 503 after partial data",
            "method": "storage.objects.get",
            "instruction": "return-broken-stream-after-2K",
            "expected_error": None,
        },
        {
            "name": "Retry on BidiReadObjectRedirectedError",
            "method": "storage.objects.get",
            "instruction": "redirect-send-handle-and-token-tokenval",  # Testbench instruction for redirect
            "expected_error": None,
        },
    ]

    try:
        # Create a single bucket and object for all tests to use.
        content = b"A" * CONTENT_LENGTH
        bucket_resource = storage_v2.Bucket(project=f"projects/{PROJECT_NUMBER}")
        create_bucket_request = storage_v2.CreateBucketRequest(
            parent="projects/_", bucket_id=bucket_name, bucket=bucket_resource
        )
        await gapic_client.create_bucket(request=create_bucket_request)

        write_spec = storage_v2.WriteObjectSpec(
            resource=storage_v2.Object(
                bucket=f"projects/_/buckets/{bucket_name}", name=object_name
            )
        )

        async def write_req_gen():
            yield storage_v2.WriteObjectRequest(
                write_object_spec=write_spec,
                checksummed_data={"content": content},
                finish_write=True,
            )

        await gapic_client.write_object(requests=write_req_gen())

        # Run all defined test scenarios.
        for scenario in test_scenarios:
            await run_test_scenario(
                gapic_client, http_client, bucket_name, object_name, scenario
            )

        # Define and run test scenarios specifically for the open() method
        open_test_scenarios = [
            {
                "name": "Open: Retry on 503",
                "method": "storage.objects.get",
                "instruction": "return-503",
                "expected_error": None,
            },
            {
                "name": "Open: Retry on BidiReadObjectRedirectedError",
                "method": "storage.objects.get",
                "instruction": "redirect-send-handle-and-token-tokenval",
                "expected_error": None,
            },
            {
                "name": "Open: Fail Fast on 401",
                "method": "storage.objects.get",
                "instruction": "return-401",
                "expected_error": exceptions.Unauthorized,
            },
        ]
        for scenario in open_test_scenarios:
            await run_open_test_scenario(
                gapic_client, http_client, bucket_name, object_name, scenario
            )

    except Exception:
        import traceback

        traceback.print_exc()
    finally:
        # Clean up the test bucket.
        try:
            delete_object_req = storage_v2.DeleteObjectRequest(
                bucket="projects/_/buckets/" + bucket_name, object=object_name
            )
            await gapic_client.delete_object(request=delete_object_req)

            delete_bucket_req = storage_v2.DeleteBucketRequest(
                name=f"projects/_/buckets/{bucket_name}"
            )
            await gapic_client.delete_bucket(request=delete_bucket_req)
        except Exception as e:
            print(f"Warning: Cleanup failed: {e}")


async def run_open_test_scenario(
    gapic_client, http_client, bucket_name, object_name, scenario
):
    """Runs a fault-injection test scenario specifically for the open() method."""
    print(f"\n--- RUNNING SCENARIO: {scenario['name']} ---")

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
        print(f"Retry Test created with ID: {retry_test_id}")

        # 2. Set up metadata for fault injection.
        fault_injection_metadata = (("x-retry-test-id", retry_test_id),)

        # 3. Execute the open (via create_mrd) and assert the outcome.
        try:
            downloader = await AsyncMultiRangeDownloader.create_mrd(
                gapic_client,
                bucket_name,
                object_name,
                metadata=fault_injection_metadata,
            )

            # If open was successful, perform a simple download to ensure the stream is usable.
            buffer = io.BytesIO()
            await downloader.download_ranges([(0, 1024, buffer)])
            await downloader.close()
            assert len(buffer.getvalue()) == 1024

            # If an exception was expected, this line should not be reached.
            if scenario["expected_error"] is not None:
                raise AssertionError(
                    f"Expected exception {scenario['expected_error']} was not raised."
                )

        except scenario["expected_error"] as e:
            print(f"Caught expected exception for {scenario['name']}: {e}")

    finally:
        # 4. Clean up the Retry Test resource.
        if retry_test_id:
            http_client.delete(f"{HTTP_ENDPOINT}/retry_test/{retry_test_id}")


if __name__ == "__main__":
    asyncio.run(main())
