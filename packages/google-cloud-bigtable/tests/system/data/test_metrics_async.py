# Copyright 2026 Google LLC
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
import asyncio
import os
import pytest
import uuid

from grpc import StatusCode

from google.api_core.exceptions import Aborted
from google.api_core.exceptions import GoogleAPICallError
from google.api_core.exceptions import PermissionDenied
from google.cloud.bigtable.data._metrics.handlers._base import MetricsHandler
from google.cloud.bigtable.data._metrics.data_model import (
    CompletedOperationMetric,
    CompletedAttemptMetric,
)
from google.cloud.bigtable_v2.types import ResponseParams
from google.cloud.environment_vars import BIGTABLE_EMULATOR

from google.cloud.bigtable.data._cross_sync import CrossSync

from . import TEST_FAMILY, SystemTestRunner

if CrossSync.is_async:
    from grpc.aio import UnaryUnaryClientInterceptor
    from grpc.aio import UnaryStreamClientInterceptor
    from grpc.aio import AioRpcError
    from grpc.aio import Metadata
else:
    from grpc import UnaryUnaryClientInterceptor
    from grpc import UnaryStreamClientInterceptor
    from grpc import RpcError
    from grpc import intercept_channel

__CROSS_SYNC_OUTPUT__ = "tests.system.data.test_metrics_autogen"


class _MetricsTestHandler(MetricsHandler):
    """
    Store completed metrics events in internal lists for testing
    """

    def __init__(self, **kwargs):
        self.completed_operations = []
        self.completed_attempts = []

    def on_operation_complete(self, op):
        self.completed_operations.append(op)

    def on_attempt_complete(self, attempt, _):
        self.completed_attempts.append(attempt)

    def clear(self):
        self.completed_operations.clear()
        self.completed_attempts.clear()

    def __repr__(self):
        return f"{self.__class__}(completed_operations={len(self.completed_operations)}, completed_attempts={len(self.completed_attempts)}"


@CrossSync.convert_class
class _ErrorInjectorInterceptor(
    UnaryUnaryClientInterceptor, UnaryStreamClientInterceptor
):
    """
    Gprc interceptor used to inject errors into rpc calls, to test failures
    """

    def __init__(self):
        self._exc_list = []
        self.fail_mid_stream = False

    def push(self, exc: Exception):
        self._exc_list.append(exc)

    def clear(self):
        self._exc_list.clear()
        self.fail_mid_stream = False

    @CrossSync.convert
    async def intercept_unary_unary(self, continuation, client_call_details, request):
        if self._exc_list:
            raise self._exc_list.pop(0)
        return await continuation(client_call_details, request)

    @CrossSync.convert
    async def intercept_unary_stream(self, continuation, client_call_details, request):
        if not self.fail_mid_stream and self._exc_list:
            raise self._exc_list.pop(0)

        response = await continuation(client_call_details, request)

        if self.fail_mid_stream and self._exc_list:
            exc = self._exc_list.pop(0)

            class CallWrapper:
                def __init__(self, call, exc_to_raise):
                    self._call = call
                    self._exc = exc_to_raise
                    self._raised = False

                @CrossSync.convert(sync_name="__iter__")
                def __aiter__(self):
                    return self

                @CrossSync.convert(
                    sync_name="__next__", replace_symbols={"__anext__": "__next__"}
                )
                async def __anext__(self):
                    if not self._raised:
                        self._raised = True
                        if self._exc:
                            raise self._exc
                    return await self._call.__anext__()

                def __getattr__(self, name):
                    return getattr(self._call, name)

            return CallWrapper(response, exc)

        return response


@CrossSync.convert_class(sync_name="TestMetrics")
class TestMetricsAsync(SystemTestRunner):
    def _make_client(self):
        project = os.getenv("GOOGLE_CLOUD_PROJECT") or None
        return CrossSync.DataClient(project=project)

    def _make_exception(self, status, cluster_id=None, zone_id=None):
        if cluster_id or zone_id:
            metadata = (
                "x-goog-ext-425905942-bin",
                ResponseParams.serialize(
                    ResponseParams(cluster_id=cluster_id, zone_id=zone_id)
                ),
            )
        else:
            metadata = None
        if CrossSync.is_async:
            metadata = Metadata(metadata) if metadata else Metadata()
            return AioRpcError(status, Metadata(), metadata)
        else:
            exc = RpcError(status)
            exc.trailing_metadata = lambda: [metadata] if metadata else []
            exc.initial_metadata = lambda: []
            exc.code = lambda: status
            exc.details = lambda: None

            def _result():
                raise exc

            exc.result = _result
            return exc

    @pytest.fixture(scope="session")
    def handler(self):
        return _MetricsTestHandler()

    @pytest.fixture(scope="session")
    def error_injector(self):
        return _ErrorInjectorInterceptor()

    @CrossSync.convert
    @CrossSync.pytest_fixture(scope="function", autouse=True)
    async def _clear_state(self, handler, error_injector):
        """Clear handler and interceptor between each test"""
        handler.clear()
        error_injector.clear()

    @CrossSync.convert
    @CrossSync.pytest_fixture(scope="session")
    async def client(self, error_injector):
        async with self._make_client() as client:
            if CrossSync.is_async:
                client.transport.grpc_channel._unary_unary_interceptors.append(
                    error_injector
                )
                client.transport.grpc_channel._unary_stream_interceptors.append(
                    error_injector
                )
            else:
                # inject interceptor after bigtable metrics interceptors
                metrics_channel = client.transport._grpc_channel._channel._channel
                client.transport._grpc_channel._channel._channel = intercept_channel(
                    metrics_channel, error_injector
                )
            yield client

    @CrossSync.convert
    @CrossSync.pytest_fixture(scope="function")
    async def temp_rows(self, table):
        builder = CrossSync.TempRowBuilder(table)
        yield builder
        await builder.delete_rows()

    @CrossSync.convert
    @CrossSync.pytest_fixture(scope="session")
    async def table(self, client, table_id, instance_id, handler):
        async with client.get_table(instance_id, table_id) as table:
            table._metrics.add_handler(handler)
            yield table

    @CrossSync.convert
    @CrossSync.pytest_fixture(scope="session")
    async def authorized_view(
        self, client, table_id, instance_id, authorized_view_id, handler
    ):
        async with client.get_authorized_view(
            instance_id, table_id, authorized_view_id
        ) as table:
            table._metrics.add_handler(handler)
            yield table

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)),
        reason="emulator doesn't suport cluster_config",
    )
    @CrossSync.pytest
    async def test_mutate_row(self, table, temp_rows, handler, cluster_config):
        row_key = b"mutate"
        new_value = uuid.uuid4().hex.encode()
        row_key, mutation = await temp_rows.create_row_and_mutation(
            table, new_value=new_value
        )
        handler.clear()
        await table.mutate_row(row_key, mutation)
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.value[0] == 0
        assert operation.is_streaming is False
        assert operation.op_type.value == "MutateRow"
        assert len(operation.completed_attempts) == 1
        assert operation.completed_attempts[0] == handler.completed_attempts[0]
        assert operation.cluster_id == next(iter(cluster_config.keys()))
        assert (
            operation.zone
            == cluster_config[operation.cluster_id].location.split("/")[-1]
        )
        assert operation.duration_ns > 0 and operation.duration_ns < 1e9
        assert (
            operation.first_response_latency_ns is None
        )  # populated for read_rows only
        assert operation.flow_throttling_time_ns == 0
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert isinstance(attempt, CompletedAttemptMetric)
        assert attempt.duration_ns > 0 and attempt.duration_ns < operation.duration_ns
        assert attempt.end_status.value[0] == 0
        assert attempt.backoff_before_attempt_ns == 0
        assert (
            attempt.gfe_latency_ns > 0 and attempt.gfe_latency_ns < attempt.duration_ns
        )
        assert attempt.application_blocking_time_ns == 0

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)),
        reason="emulator doesn't suport cluster_config",
    )
    @CrossSync.pytest
    async def test_mutate_row_failure_with_retries(
        self, table, handler, error_injector
    ):
        """
        Test failure in grpc layer by injecting errors into an interceptor
        with retryable errors, then a terminal one
        """
        from google.cloud.bigtable.data.mutations import SetCell

        row_key = b"row_key_1"
        mutation = SetCell(TEST_FAMILY, b"q", b"v")

        handler.clear()
        expected_zone = "my_zone"
        expected_cluster = "my_cluster"
        num_retryable = 2
        for i in range(num_retryable):
            error_injector.push(
                self._make_exception(StatusCode.ABORTED, cluster_id=expected_cluster)
            )
        error_injector.push(
            self._make_exception(StatusCode.PERMISSION_DENIED, zone_id=expected_zone)
        )
        with pytest.raises(PermissionDenied):
            await table.mutate_row(row_key, [mutation], retryable_errors=[Aborted])
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == num_retryable + 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "PERMISSION_DENIED"
        assert operation.op_type.value == "MutateRow"
        assert operation.is_streaming is False
        assert len(operation.completed_attempts) == num_retryable + 1
        assert operation.cluster_id == expected_cluster
        assert operation.zone == expected_zone
        # validate attempts
        for i in range(num_retryable):
            attempt = handler.completed_attempts[i]
            assert isinstance(attempt, CompletedAttemptMetric)
            assert attempt.end_status.name == "ABORTED"
            assert attempt.gfe_latency_ns is None
        final_attempt = handler.completed_attempts[num_retryable]
        assert isinstance(final_attempt, CompletedAttemptMetric)
        assert final_attempt.end_status.name == "PERMISSION_DENIED"
        assert final_attempt.gfe_latency_ns is None

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)), reason="not supported by emulator"
    )
    @CrossSync.pytest
    async def test_mutate_row_failure_timeout(self, table, temp_rows, handler):
        """
        Test failure in gapic layer by passing very low timeout

        No grpc headers expected
        """
        from google.cloud.bigtable.data.mutations import SetCell

        row_key = b"row_key_1"
        mutation = SetCell(TEST_FAMILY, b"q", b"v")

        with pytest.raises(GoogleAPICallError):
            await table.mutate_row(row_key, [mutation], operation_timeout=0.001)
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "DEADLINE_EXCEEDED"
        assert operation.op_type.value == "MutateRow"
        assert operation.is_streaming is False
        assert len(operation.completed_attempts) == 1
        assert operation.cluster_id == "<unspecified>"
        assert operation.zone == "global"
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert isinstance(attempt, CompletedAttemptMetric)
        assert attempt.end_status.name == "DEADLINE_EXCEEDED"
        assert attempt.gfe_latency_ns is None

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)),
        reason="emulator doesn't suport cluster_config",
    )
    @CrossSync.pytest
    async def test_mutate_row_failure_unauthorized(
        self, handler, authorized_view, cluster_config
    ):
        """
        Test failure in backend by accessing an unauthorized family
        """
        from google.cloud.bigtable.data.mutations import SetCell

        row_key = b"row_key_1"
        mutation = SetCell("unauthorized", b"q", b"v")

        with pytest.raises(GoogleAPICallError) as e:
            await authorized_view.mutate_row(row_key, [mutation])
        assert e.value.grpc_status_code.name == "PERMISSION_DENIED"
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "PERMISSION_DENIED"
        assert operation.op_type.value == "MutateRow"
        assert operation.is_streaming is False
        assert len(operation.completed_attempts) == 1
        assert operation.cluster_id == next(iter(cluster_config.keys()))
        assert (
            operation.zone
            == cluster_config[operation.cluster_id].location.split("/")[-1]
        )
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert isinstance(attempt, CompletedAttemptMetric)
        assert attempt.end_status.name == "PERMISSION_DENIED"
        assert (
            attempt.gfe_latency_ns >= 0
            and attempt.gfe_latency_ns < operation.duration_ns
        )

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)),
        reason="emulator doesn't suport cluster_config",
    )
    @CrossSync.pytest
    async def test_mutate_row_failure_unauthorized_with_retries(
        self, handler, authorized_view, cluster_config
    ):
        """
        retry unauthorized request multiple times before timing out
        """
        from google.cloud.bigtable.data.mutations import SetCell

        row_key = b"row_key_1"
        mutation = SetCell("unauthorized", b"q", b"v")

        with pytest.raises(GoogleAPICallError) as e:
            await authorized_view.mutate_row(
                row_key,
                [mutation],
                retryable_errors=[PermissionDenied],
                operation_timeout=0.5,
            )
        assert e.value.grpc_status_code.name == "DEADLINE_EXCEEDED"
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) > 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "DEADLINE_EXCEEDED"
        assert operation.op_type.value == "MutateRow"
        assert operation.is_streaming is False
        assert len(operation.completed_attempts) > 1
        assert operation.cluster_id == next(iter(cluster_config.keys()))
        assert (
            operation.zone
            == cluster_config[operation.cluster_id].location.split("/")[-1]
        )
        # validate attempts
        for attempt in handler.completed_attempts:
            assert attempt.end_status.name in ["PERMISSION_DENIED", "DEADLINE_EXCEEDED"]

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)),
        reason="emulator doesn't suport cluster_config",
    )
    @CrossSync.pytest
    async def test_sample_row_keys(self, table, temp_rows, handler, cluster_config):
        await table.sample_row_keys()
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.value[0] == 0
        assert operation.is_streaming is False
        assert operation.op_type.value == "SampleRowKeys"
        assert len(operation.completed_attempts) == 1
        assert operation.completed_attempts[0] == handler.completed_attempts[0]
        assert operation.cluster_id == next(iter(cluster_config.keys()))
        assert (
            operation.zone
            == cluster_config[operation.cluster_id].location.split("/")[-1]
        )
        assert operation.duration_ns > 0 and operation.duration_ns < 1e9
        assert (
            operation.first_response_latency_ns is None
        )  # populated for read_rows only
        assert operation.flow_throttling_time_ns == 0
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert isinstance(attempt, CompletedAttemptMetric)
        assert attempt.duration_ns > 0 and attempt.duration_ns < operation.duration_ns
        assert attempt.end_status.value[0] == 0
        assert attempt.backoff_before_attempt_ns == 0
        assert (
            attempt.gfe_latency_ns > 0 and attempt.gfe_latency_ns < attempt.duration_ns
        )
        assert attempt.application_blocking_time_ns == 0

    @CrossSync.drop
    @CrossSync.pytest
    async def test_sample_row_keys_failure_cancelled(
        self, table, temp_rows, handler, error_injector
    ):
        """
        Test failure in grpc layer by injecting errors into an interceptor
        test with retryable errors, then a terminal one

        No headers expected
        """
        num_retryable = 3
        for i in range(num_retryable):
            error_injector.push(self._make_exception(StatusCode.ABORTED))
        error_injector.push(asyncio.CancelledError)
        with pytest.raises(asyncio.CancelledError):
            await table.sample_row_keys(retryable_errors=[Aborted])
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == num_retryable + 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "UNKNOWN"
        assert operation.op_type.value == "SampleRowKeys"
        assert operation.is_streaming is False
        assert len(operation.completed_attempts) == num_retryable + 1
        assert operation.completed_attempts[0] == handler.completed_attempts[0]
        assert operation.cluster_id == "<unspecified>"
        assert operation.zone == "global"
        # validate attempts
        for i in range(num_retryable):
            attempt = handler.completed_attempts[i]
            assert isinstance(attempt, CompletedAttemptMetric)
            assert attempt.end_status.name == "ABORTED"
            assert attempt.gfe_latency_ns is None
        final_attempt = handler.completed_attempts[num_retryable]
        assert isinstance(final_attempt, CompletedAttemptMetric)
        assert final_attempt.end_status.name == "UNKNOWN"
        assert final_attempt.gfe_latency_ns is None

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)),
        reason="emulator doesn't suport cluster_config",
    )
    @CrossSync.pytest
    async def test_sample_row_keys_failure_with_retries(
        self, table, temp_rows, handler, error_injector, cluster_config
    ):
        """
        Test failure in grpc layer by injecting errors into an interceptor
        with retryable errors, then a success
        """
        num_retryable = 3
        for i in range(num_retryable):
            error_injector.push(self._make_exception(StatusCode.ABORTED))
        await table.sample_row_keys(retryable_errors=[Aborted])
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == num_retryable + 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "OK"
        assert operation.op_type.value == "SampleRowKeys"
        assert operation.is_streaming is False
        assert len(operation.completed_attempts) == num_retryable + 1
        assert operation.completed_attempts[0] == handler.completed_attempts[0]
        assert operation.cluster_id == next(iter(cluster_config.keys()))
        assert (
            operation.zone
            == cluster_config[operation.cluster_id].location.split("/")[-1]
        )
        # validate attempts
        for i in range(num_retryable):
            attempt = handler.completed_attempts[i]
            assert isinstance(attempt, CompletedAttemptMetric)
            assert attempt.end_status.name == "ABORTED"
            assert attempt.gfe_latency_ns is None
        final_attempt = handler.completed_attempts[num_retryable]
        assert isinstance(final_attempt, CompletedAttemptMetric)
        assert final_attempt.end_status.name == "OK"
        assert (
            final_attempt.gfe_latency_ns > 0
            and final_attempt.gfe_latency_ns < operation.duration_ns
        )

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)), reason="not supported by emulator"
    )
    @CrossSync.pytest
    async def test_sample_row_keys_failure_timeout(self, table, handler):
        """
        Test failure in gapic layer by passing very low timeout

        No grpc headers expected
        """
        with pytest.raises(GoogleAPICallError):
            await table.sample_row_keys(operation_timeout=0.001)
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "DEADLINE_EXCEEDED"
        assert operation.op_type.value == "SampleRowKeys"
        assert operation.is_streaming is False
        assert len(operation.completed_attempts) == 1
        assert operation.cluster_id == "<unspecified>"
        assert operation.zone == "global"
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert isinstance(attempt, CompletedAttemptMetric)
        assert attempt.end_status.name == "DEADLINE_EXCEEDED"
        assert attempt.gfe_latency_ns is None

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)),
        reason="emulator doesn't suport cluster_config",
    )
    @CrossSync.pytest
    async def test_sample_row_keys_failure_mid_stream(
        self, table, temp_rows, handler, error_injector
    ):
        """
        Test failure in grpc stream
        """
        error_injector.fail_mid_stream = True
        error_injector.push(self._make_exception(StatusCode.ABORTED))
        error_injector.push(self._make_exception(StatusCode.PERMISSION_DENIED))
        with pytest.raises(PermissionDenied):
            await table.sample_row_keys(retryable_errors=[Aborted])
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 2
        # validate operation
        operation = handler.completed_operations[0]
        assert operation.final_status.name == "PERMISSION_DENIED"
        assert operation.op_type.value == "SampleRowKeys"
        assert operation.is_streaming is False
        assert len(operation.completed_attempts) == 2
        # validate retried attempt
        attempt = handler.completed_attempts[0]
        assert attempt.end_status.name == "ABORTED"
        # validate final attempt
        final_attempt = handler.completed_attempts[-1]
        assert final_attempt.end_status.name == "PERMISSION_DENIED"

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)),
        reason="emulator doesn't suport cluster_config",
    )
    @CrossSync.pytest
    async def test_read_modify_write(self, table, temp_rows, handler, cluster_config):
        from google.cloud.bigtable.data.read_modify_write_rules import IncrementRule

        row_key = b"test-row-key"
        family = TEST_FAMILY
        qualifier = b"test-qualifier"
        await temp_rows.add_row(row_key, value=0, family=family, qualifier=qualifier)
        rule = IncrementRule(family, qualifier, 1)
        await table.read_modify_write_row(row_key, rule)
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.value[0] == 0
        assert operation.is_streaming is False
        assert operation.op_type.value == "ReadModifyWriteRow"
        assert len(operation.completed_attempts) == 1
        assert operation.completed_attempts[0] == handler.completed_attempts[0]
        assert operation.cluster_id == next(iter(cluster_config.keys()))
        assert (
            operation.zone
            == cluster_config[operation.cluster_id].location.split("/")[-1]
        )
        assert operation.duration_ns > 0 and operation.duration_ns < 1e9
        assert (
            operation.first_response_latency_ns is None
        )  # populated for read_rows only
        assert operation.flow_throttling_time_ns == 0
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert isinstance(attempt, CompletedAttemptMetric)
        assert attempt.duration_ns > 0 and attempt.duration_ns < operation.duration_ns
        assert attempt.end_status.value[0] == 0
        assert attempt.backoff_before_attempt_ns == 0
        assert (
            attempt.gfe_latency_ns > 0 and attempt.gfe_latency_ns < attempt.duration_ns
        )
        assert attempt.application_blocking_time_ns == 0

    @CrossSync.drop
    @CrossSync.pytest
    async def test_read_modify_write_failure_cancelled(
        self, table, temp_rows, handler, error_injector
    ):
        """
        Test failure in grpc layer by injecting an error into an interceptor

        No headers expected
        """
        from google.cloud.bigtable.data.read_modify_write_rules import IncrementRule

        row_key = b"test-row-key"
        family = TEST_FAMILY
        qualifier = b"test-qualifier"
        await temp_rows.add_row(row_key, value=0, family=family, qualifier=qualifier)
        rule = IncrementRule(family, qualifier, 1)

        # trigger an exception
        exc = asyncio.CancelledError("injected")
        error_injector.push(exc)
        with pytest.raises(asyncio.CancelledError):
            await table.read_modify_write_row(row_key, rule)

        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "UNKNOWN"
        assert operation.is_streaming is False
        assert operation.op_type.value == "ReadModifyWriteRow"
        assert len(operation.completed_attempts) == len(handler.completed_attempts)
        assert operation.completed_attempts == handler.completed_attempts
        assert operation.cluster_id == "<unspecified>"
        assert operation.zone == "global"
        assert operation.duration_ns > 0 and operation.duration_ns < 1e9
        assert (
            operation.first_response_latency_ns is None
        )  # populated for read_rows only
        assert operation.flow_throttling_time_ns == 0
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert isinstance(attempt, CompletedAttemptMetric)
        assert attempt.duration_ns > 0
        assert attempt.end_status.name == "UNKNOWN"
        assert attempt.backoff_before_attempt_ns == 0
        assert attempt.gfe_latency_ns is None
        assert attempt.application_blocking_time_ns == 0

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)), reason="not supported by emulator"
    )
    @CrossSync.pytest
    async def test_read_modify_write_failure_timeout(self, table, temp_rows, handler):
        """
        Test failure in gapic layer by passing very low timeout

        No grpc headers expected
        """
        from google.cloud.bigtable.data.read_modify_write_rules import IncrementRule

        row_key = b"test-row-key"
        family = TEST_FAMILY
        qualifier = b"test-qualifier"
        await temp_rows.add_row(row_key, value=0, family=family, qualifier=qualifier)
        rule = IncrementRule(family, qualifier, 1)
        with pytest.raises(GoogleAPICallError):
            await table.read_modify_write_row(row_key, rule, operation_timeout=0.001)
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "DEADLINE_EXCEEDED"
        assert operation.op_type.value == "ReadModifyWriteRow"
        assert operation.cluster_id == "<unspecified>"
        assert operation.zone == "global"
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert attempt.gfe_latency_ns is None

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)), reason="not supported by emulator"
    )
    @CrossSync.pytest
    async def test_read_modify_write_failure_unauthorized(
        self, handler, authorized_view, cluster_config
    ):
        """
        Test failure in backend by accessing an unauthorized family
        """
        from google.cloud.bigtable.data.read_modify_write_rules import IncrementRule

        row_key = b"test-row-key"
        qualifier = b"test-qualifier"
        rule = IncrementRule("unauthorized", qualifier, 1)
        with pytest.raises(GoogleAPICallError):
            await authorized_view.read_modify_write_row(row_key, rule)
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "PERMISSION_DENIED"
        assert operation.op_type.value == "ReadModifyWriteRow"
        assert operation.cluster_id == next(iter(cluster_config.keys()))
        assert (
            operation.zone
            == cluster_config[operation.cluster_id].location.split("/")[-1]
        )
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert (
            attempt.gfe_latency_ns >= 0
            and attempt.gfe_latency_ns < operation.duration_ns
        )

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)),
        reason="emulator doesn't suport cluster_config",
    )
    @CrossSync.pytest
    async def test_check_and_mutate_row(
        self, table, temp_rows, handler, cluster_config
    ):
        from google.cloud.bigtable.data.mutations import SetCell
        from google.cloud.bigtable.data.row_filters import ValueRangeFilter

        row_key = b"test-row-key"
        family = TEST_FAMILY
        qualifier = b"test-qualifier"
        await temp_rows.add_row(row_key, value=1, family=family, qualifier=qualifier)

        true_mutation_value = b"true-mutation-value"
        true_mutation = SetCell(
            family=TEST_FAMILY, qualifier=qualifier, new_value=true_mutation_value
        )
        predicate = ValueRangeFilter(0, 2)
        await table.check_and_mutate_row(
            row_key,
            predicate,
            true_case_mutations=true_mutation,
        )
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.value[0] == 0
        assert operation.is_streaming is False
        assert operation.op_type.value == "CheckAndMutateRow"
        assert len(operation.completed_attempts) == 1
        assert operation.completed_attempts[0] == handler.completed_attempts[0]
        assert operation.cluster_id == next(iter(cluster_config.keys()))
        assert (
            operation.zone
            == cluster_config[operation.cluster_id].location.split("/")[-1]
        )
        assert operation.duration_ns > 0 and operation.duration_ns < 1e9
        assert (
            operation.first_response_latency_ns is None
        )  # populated for read_rows only
        assert operation.flow_throttling_time_ns == 0
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert isinstance(attempt, CompletedAttemptMetric)
        assert attempt.duration_ns > 0 and attempt.duration_ns < operation.duration_ns
        assert attempt.end_status.value[0] == 0
        assert attempt.backoff_before_attempt_ns == 0
        assert (
            attempt.gfe_latency_ns > 0 and attempt.gfe_latency_ns < attempt.duration_ns
        )
        assert attempt.application_blocking_time_ns == 0

    @CrossSync.drop
    @CrossSync.pytest
    async def test_check_and_mutate_row_failure_cancelled(
        self, table, temp_rows, handler, error_injector
    ):
        """
        Test failure in grpc layer by injecting an error into an interceptor

        No headers expected
        """
        from google.cloud.bigtable.data.row_filters import ValueRangeFilter

        row_key = b"test-row-key"
        family = TEST_FAMILY
        qualifier = b"test-qualifier"
        await temp_rows.add_row(row_key, value=1, family=family, qualifier=qualifier)

        # trigger an exception
        exc = asyncio.CancelledError("injected")
        error_injector.push(exc)
        with pytest.raises(asyncio.CancelledError):
            await table.check_and_mutate_row(
                row_key,
                predicate=ValueRangeFilter(0, 2),
            )
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "UNKNOWN"
        assert operation.is_streaming is False
        assert operation.op_type.value == "CheckAndMutateRow"
        assert len(operation.completed_attempts) == len(handler.completed_attempts)
        assert operation.completed_attempts == handler.completed_attempts
        assert operation.cluster_id == "<unspecified>"
        assert operation.zone == "global"
        assert operation.duration_ns > 0 and operation.duration_ns < 1e9
        assert (
            operation.first_response_latency_ns is None
        )  # populated for read_rows only
        assert operation.flow_throttling_time_ns == 0
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert isinstance(attempt, CompletedAttemptMetric)
        assert attempt.duration_ns > 0
        assert attempt.end_status.name == "UNKNOWN"
        assert attempt.backoff_before_attempt_ns == 0
        assert attempt.gfe_latency_ns is None
        assert attempt.application_blocking_time_ns == 0

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)), reason="not supported by emulator"
    )
    @CrossSync.pytest
    async def test_check_and_mutate_row_failure_timeout(
        self, table, temp_rows, handler
    ):
        """
        Test failure in gapic layer by passing very low timeout

        No grpc headers expected
        """
        from google.cloud.bigtable.data.mutations import SetCell
        from google.cloud.bigtable.data.row_filters import ValueRangeFilter

        row_key = b"test-row-key"
        family = TEST_FAMILY
        qualifier = b"test-qualifier"
        await temp_rows.add_row(row_key, value=1, family=family, qualifier=qualifier)

        true_mutation_value = b"true-mutation-value"
        true_mutation = SetCell(
            family=TEST_FAMILY, qualifier=qualifier, new_value=true_mutation_value
        )
        with pytest.raises(GoogleAPICallError):
            await table.check_and_mutate_row(
                row_key,
                predicate=ValueRangeFilter(0, 2),
                true_case_mutations=true_mutation,
                operation_timeout=0.001,
            )
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "DEADLINE_EXCEEDED"
        assert operation.cluster_id == "<unspecified>"
        assert operation.zone == "global"
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert attempt.gfe_latency_ns is None

    @pytest.mark.skipif(
        bool(os.environ.get(BIGTABLE_EMULATOR)),
        reason="emulator doesn't suport cluster_config",
    )
    @CrossSync.pytest
    async def test_check_and_mutate_row_failure_unauthorized(
        self, handler, authorized_view, cluster_config
    ):
        """
        Test failure in backend by accessing an unauthorized family
        """
        from google.cloud.bigtable.data.mutations import SetCell
        from google.cloud.bigtable.data.row_filters import ValueRangeFilter

        row_key = b"test-row-key"
        qualifier = b"test-qualifier"
        mutation_value = b"true-mutation-value"
        mutation = SetCell(
            family="unauthorized", qualifier=qualifier, new_value=mutation_value
        )
        with pytest.raises(GoogleAPICallError):
            await authorized_view.check_and_mutate_row(
                row_key,
                predicate=ValueRangeFilter(0, 2),
                true_case_mutations=mutation,
                false_case_mutations=mutation,
            )
        # validate counts
        assert len(handler.completed_operations) == 1
        assert len(handler.completed_attempts) == 1
        # validate operation
        operation = handler.completed_operations[0]
        assert isinstance(operation, CompletedOperationMetric)
        assert operation.final_status.name == "PERMISSION_DENIED"
        assert operation.cluster_id == next(iter(cluster_config.keys()))
        assert (
            operation.zone
            == cluster_config[operation.cluster_id].location.split("/")[-1]
        )
        # validate attempt
        attempt = handler.completed_attempts[0]
        assert (
            attempt.gfe_latency_ns >= 0
            and attempt.gfe_latency_ns < operation.duration_ns
        )
