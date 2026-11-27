# Copyright 2026 Google LLC All rights reserved.
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

import unittest
from types import SimpleNamespace
from unittest import mock

import grpc
from google.api_core import gapic_v1
from google.api_core.exceptions import (
    Aborted,
    DeadlineExceeded,
    InternalServerError,
    InvalidArgument,
    ResourceExhausted,
    RetryError,
    ServiceUnavailable,
)
from google.api_core.retry import Retry

from google.cloud.spanner_v1 import _retry as retry_module
from google.cloud.spanner_v1.services.spanner import SpannerClient
from google.cloud.spanner_v1.services.spanner.transports.grpc import (
    SpannerGrpcTransport,
)


def _create_mock_channel() -> mock.Mock:
    """Create a hermetic autospec gRPC channel with distinct stubs."""
    channel = mock.create_autospec(grpc.Channel, instance=True)
    channel.unary_unary.side_effect = lambda *args, **kwargs: mock.MagicMock()
    channel.unary_stream.side_effect = lambda *args, **kwargs: mock.MagicMock()
    return channel


class _RecordingDatabase:
    """Minimal database test double tracking request-ID augmentation calls."""

    def __init__(self, next_nth_request: int = 7) -> None:
        self._nth_request_value = next_nth_request
        self.augmentation_calls: list[tuple] = []
        self.augmented_errors: list[BaseException] = []

    @property
    def _next_nth_request(self) -> int:
        current = self._nth_request_value
        self._nth_request_value += 1
        return current

    def with_error_augmentation(
        self,
        nth_request: int,
        nth_attempt: int,
        prior_metadata: object = None,
        span: object = None,
    ) -> tuple:
        self.augmentation_calls.append((nth_request, nth_attempt, prior_metadata, span))
        base_metadata = list(prior_metadata) if prior_metadata else []
        base_metadata.append(
            ("x-goog-spanner-request-id", f"1.0.{nth_request}.{nth_attempt}")
        )

        class _ErrorAugmenter:
            def __init__(self, recorder: "_RecordingDatabase") -> None:
                self._recorder = recorder

            def __enter__(self) -> "_ErrorAugmenter":
                return self

            def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
                if exc_val is not None:
                    self._recorder.augmented_errors.append(exc_val)
                return False

        return base_metadata, _ErrorAugmenter(self)


class TestRetryHelpers(unittest.TestCase):
    def test_is_retryable_internal_error_matching_messages(self) -> None:
        retryable_messages = (
            "RST_STREAM",
            "Received unexpected EOS on DATA frame from server",
            "HTTP/2 error code: INTERNAL_ERROR",
            "Connection closed with unknown cause",
            "Authentication backend internal server error. Please retry",
        )
        for message in retryable_messages:
            with self.subTest(message=message):
                exception = InternalServerError(f"prefix: {message} (details)")
                self.assertTrue(retry_module._is_retryable_internal_error(exception))

    def test_is_retryable_internal_error_non_retryable_messages(self) -> None:
        non_retryable = (
            InternalServerError("Unexpected server failure"),
            InternalServerError(""),
            InternalServerError("rst_stream lowercase"),
            ServiceUnavailable("RST_STREAM"),
            ValueError("RST_STREAM"),
        )
        for exception in non_retryable:
            with self.subTest(exception=exception):
                self.assertFalse(retry_module._is_retryable_internal_error(exception))

    def test_is_retryable_internal_error_fallback_to_str(self) -> None:
        class _CustomInternalError(InternalServerError):
            def __str__(self) -> str:
                return "500 RST_STREAM in str representation"

        exception_empty_message = _CustomInternalError("")
        self.assertTrue(
            retry_module._is_retryable_internal_error(exception_empty_message)
        )

        exception_none_message = _CustomInternalError(None)
        self.assertTrue(
            retry_module._is_retryable_internal_error(exception_none_message)
        )

        exception_deleted_message = _CustomInternalError("ignored")
        del exception_deleted_message.message
        self.assertTrue(
            retry_module._is_retryable_internal_error(exception_deleted_message)
        )

        mock_retryable = mock.Mock(spec=InternalServerError)
        mock_retryable.__str__ = mock.Mock(return_value="500 RST_STREAM")
        self.assertTrue(retry_module._is_retryable_internal_error(mock_retryable))

        mock_non_retryable = mock.Mock(spec=InternalServerError)
        mock_non_retryable.__str__ = mock.Mock(return_value="500 permanent error")
        self.assertFalse(retry_module._is_retryable_internal_error(mock_non_retryable))

    def test_is_retryable_unary_error(self) -> None:
        retryable = (
            ServiceUnavailable("unavailable"),
            ResourceExhausted("exhausted"),
            InternalServerError("Received unexpected EOS on DATA frame from server"),
        )
        for exception in retryable:
            with self.subTest(retryable=exception):
                self.assertTrue(retry_module._is_retryable_unary_error(exception))

        non_retryable = (
            InternalServerError("non-retryable internal bug"),
            Aborted("transaction aborted"),
            InvalidArgument("bad argument"),
            DeadlineExceeded("deadline exceeded"),
            RuntimeError("unexpected runtime error"),
        )
        for exception in non_retryable:
            with self.subTest(non_retryable=exception):
                self.assertFalse(retry_module._is_retryable_unary_error(exception))

    def test_resolve_unary_retry_none(self) -> None:
        api = mock.MagicMock()
        self.assertIsNone(retry_module.resolve_unary_retry(api, "commit", retry=None))

    def test_resolve_unary_retry_explicit_policy_preserved(self) -> None:
        api = mock.MagicMock()
        custom_retry = Retry(
            predicate=lambda exception: isinstance(exception, ServiceUnavailable),
            initial=1.0,
            maximum=5.0,
            multiplier=2.0,
            timeout=12.0,
        )
        resolved = retry_module.resolve_unary_retry(api, "commit", retry=custom_retry)
        self.assertIs(resolved, custom_retry)

    def test_resolve_unary_retry_from_real_client_transport(self) -> None:
        transport = SpannerGrpcTransport(channel=_create_mock_channel())
        client = SpannerClient(transport=transport)

        commit_retry = retry_module.resolve_unary_retry(
            client, "commit", retry=gapic_v1.method.DEFAULT
        )
        self.assertIsInstance(commit_retry, Retry)
        self.assertEqual(commit_retry.timeout, 3600.0)
        self.assertTrue(commit_retry._predicate(ServiceUnavailable("unavailable")))
        self.assertTrue(commit_retry._predicate(ResourceExhausted("exhausted")))
        self.assertTrue(commit_retry._predicate(InternalServerError("RST_STREAM")))
        self.assertFalse(commit_retry._predicate(Aborted("aborted")))
        self.assertFalse(commit_retry._predicate(DeadlineExceeded("deadline")))

        batch_create_retry = retry_module.resolve_unary_retry(
            client, "batch_create_sessions", retry=gapic_v1.method.DEFAULT
        )
        self.assertIsInstance(batch_create_retry, Retry)
        self.assertEqual(batch_create_retry.timeout, 60.0)
        self.assertTrue(
            batch_create_retry._predicate(InternalServerError("RST_STREAM"))
        )

        rollback_retry = retry_module.resolve_unary_retry(
            client, "rollback", retry=gapic_v1.method.DEFAULT
        )
        self.assertIsInstance(rollback_retry, Retry)
        self.assertEqual(rollback_retry.timeout, 30.0)
        self.assertTrue(rollback_retry._predicate(ServiceUnavailable("unavailable")))

        streaming_retry = retry_module.resolve_unary_retry(
            client, "streaming_read", retry=gapic_v1.method.DEFAULT
        )
        self.assertIsNone(streaming_retry)

    def test_resolve_unary_retry_preserves_existing_predicate(self) -> None:
        custom_gapic_retry = Retry(
            predicate=lambda exception: isinstance(exception, DeadlineExceeded),
            initial=1.0,
            maximum=10.0,
            multiplier=2.0,
            timeout=120.0,
        )
        method_key = object()
        api = SimpleNamespace(
            transport=SimpleNamespace(
                _wrapped_methods={
                    method_key: SimpleNamespace(_retry=custom_gapic_retry)
                },
                custom_rpc=method_key,
            )
        )

        resolved_retry = retry_module.resolve_unary_retry(
            api, "custom_rpc", retry=gapic_v1.method.DEFAULT
        )
        self.assertIsInstance(resolved_retry, Retry)
        self.assertEqual(resolved_retry.timeout, 120.0)
        self.assertEqual(resolved_retry._initial, 1.0)
        self.assertTrue(resolved_retry._predicate(DeadlineExceeded("timed out")))
        self.assertTrue(resolved_retry._predicate(ServiceUnavailable("unavailable")))
        self.assertTrue(resolved_retry._predicate(ResourceExhausted("exhausted")))
        self.assertTrue(resolved_retry._predicate(InternalServerError("RST_STREAM")))
        self.assertFalse(resolved_retry._predicate(InvalidArgument("bad request")))

        self.assertIs(
            retry_module._extend_retry_predicate(None),
            retry_module._is_retryable_unary_error,
        )
        self.assertIs(
            retry_module._extend_retry_predicate(
                retry_module._is_retryable_unary_error
            ),
            retry_module._is_retryable_unary_error,
        )

    def test_resolve_unary_retry_fallback_for_mock_api(self) -> None:
        none_api_retry = retry_module.resolve_unary_retry(
            None, "rollback", retry=gapic_v1.method.DEFAULT
        )
        self.assertIsInstance(none_api_retry, Retry)
        self.assertIs(none_api_retry._predicate, retry_module._is_retryable_unary_error)

        api = mock.MagicMock()
        default_retry = retry_module.resolve_unary_retry(
            api, "rollback", retry=gapic_v1.method.DEFAULT
        )
        self.assertIsInstance(default_retry, Retry)
        self.assertIs(default_retry._predicate, retry_module._is_retryable_unary_error)

        missing_method_api = SimpleNamespace(
            transport=SimpleNamespace(_wrapped_methods={})
        )
        missing_method_retry = retry_module.resolve_unary_retry(
            missing_method_api, "commit", retry=gapic_v1.method.DEFAULT
        )
        self.assertIsInstance(missing_method_retry, Retry)
        self.assertIs(
            missing_method_retry._predicate, retry_module._is_retryable_unary_error
        )

        method_key = object()
        missing_retry_attr_api = SimpleNamespace(
            transport=SimpleNamespace(
                _wrapped_methods={method_key: SimpleNamespace()},
                commit=method_key,
            )
        )
        missing_retry_attr_result = retry_module.resolve_unary_retry(
            missing_retry_attr_api, "commit", retry=gapic_v1.method.DEFAULT
        )
        self.assertIsInstance(missing_retry_attr_result, Retry)
        self.assertIs(
            missing_retry_attr_result._predicate, retry_module._is_retryable_unary_error
        )

        non_retry_attr_api = SimpleNamespace(
            transport=SimpleNamespace(
                _wrapped_methods={method_key: SimpleNamespace(_retry="not-a-retry")},
                commit=method_key,
            )
        )
        non_retry_attr_result = retry_module.resolve_unary_retry(
            non_retry_attr_api, "commit", retry=gapic_v1.method.DEFAULT
        )
        self.assertIsInstance(non_retry_attr_result, Retry)
        self.assertIs(
            non_retry_attr_result._predicate, retry_module._is_retryable_unary_error
        )

        unhashable_transport = SimpleNamespace(
            _wrapped_methods={},
            commit=["unhashable"],
        )
        unhashable_api = SimpleNamespace(transport=unhashable_transport)
        fallback_from_unhashable = retry_module.resolve_unary_retry(
            unhashable_api, "commit", retry=gapic_v1.method.DEFAULT
        )
        self.assertIsInstance(fallback_from_unhashable, Retry)
        self.assertIs(
            fallback_from_unhashable._predicate, retry_module._is_retryable_unary_error
        )

    def test_execute_unary_with_retry_disabled(self) -> None:
        database = _RecordingDatabase(next_nth_request=11)
        metadata = [("google-cloud-resource-prefix", "projects/p/instances/i")]
        metadata_snapshot = list(metadata)
        span = mock.MagicMock()
        retry_events: list[tuple[int, Exception]] = []
        rpc_call = mock.MagicMock(return_value="ok")

        result = retry_module.execute_unary_with_retry(
            database=database,
            rpc_call=rpc_call,
            metadata=metadata,
            span=span,
            retry_policy=None,
            on_retry=lambda attempt, exception: retry_events.append(
                (attempt, exception)
            ),
        )

        self.assertEqual(result, "ok")
        self.assertEqual(rpc_call.call_count, 1)
        self.assertEqual(metadata, metadata_snapshot)
        self.assertEqual(
            database.augmentation_calls,
            [(11, 1, metadata, span)],
        )
        self.assertEqual(database.augmented_errors, [])
        self.assertEqual(retry_events, [])

        class _MinimalDatabase:
            def __init__(self) -> None:
                self.calls: list[tuple[int, int]] = []

            def with_error_augmentation(
                self,
                nth_request: int,
                nth_attempt: int,
                prior_metadata: object = None,
                span: object = None,
            ) -> tuple:
                self.calls.append((nth_request, nth_attempt))

                class _NoOpContext:
                    def __enter__(self) -> "_NoOpContext":
                        return self

                    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
                        return False

                return [], _NoOpContext()

        minimal_database = _MinimalDatabase()
        minimal_rpc = mock.MagicMock(return_value="minimal-ok")
        self.assertEqual(
            retry_module.execute_unary_with_retry(
                database=minimal_database,
                rpc_call=minimal_rpc,
                retry_policy=None,
            ),
            "minimal-ok",
        )
        self.assertEqual(minimal_database.calls, [(0, 1)])

        failing_rpc = mock.MagicMock(
            side_effect=ServiceUnavailable("backend temporarily unavailable")
        )
        with self.assertRaisesRegex(
            ServiceUnavailable, "backend temporarily unavailable"
        ):
            retry_module.execute_unary_with_retry(
                database=database,
                rpc_call=failing_rpc,
                metadata=metadata,
                span=span,
                retry_policy=None,
                on_retry=lambda attempt, exception: retry_events.append(
                    (attempt, exception)
                ),
            )

        self.assertEqual(failing_rpc.call_count, 1)
        self.assertEqual(retry_events, [])
        self.assertEqual(len(database.augmented_errors), 1)
        self.assertEqual(
            database.augmentation_calls[-1],
            (12, 1, metadata, span),
        )

    def test_execute_unary_with_retry_succeeds_first_attempt(self) -> None:
        database = _RecordingDatabase(next_nth_request=3)
        metadata = [("x-custom", "value")]
        span = mock.MagicMock()
        retry_events: list[tuple[int, Exception]] = []
        rpc_call = mock.MagicMock(return_value="first-try")
        retry_policy = Retry(
            predicate=retry_module._is_retryable_unary_error,
            initial=0.25,
            maximum=1.0,
            multiplier=1.3,
            timeout=30.0,
        )

        with mock.patch("google.api_core.retry.retry_unary.time.sleep") as sleep_mock:
            result = retry_module.execute_unary_with_retry(
                database=database,
                rpc_call=rpc_call,
                metadata=metadata,
                span=span,
                retry_policy=retry_policy,
                on_retry=lambda attempt, exception: retry_events.append(
                    (attempt, exception)
                ),
            )

        self.assertEqual(result, "first-try")
        self.assertEqual(rpc_call.call_count, 1)
        sleep_mock.assert_not_called()
        self.assertEqual(retry_events, [])
        self.assertEqual(database.augmentation_calls, [(3, 1, metadata, span)])

    def test_execute_unary_with_retry_transient_then_success(self) -> None:
        database = _RecordingDatabase(next_nth_request=5)
        metadata = [("x-custom", "value")]
        metadata_snapshot = list(metadata)
        span = mock.MagicMock()
        retry_events: list[tuple[int, Exception]] = []
        observed_metadata: list[list[tuple[str, str]]] = []
        transient_errors = [
            ServiceUnavailable("unavailable"),
            ResourceExhausted("rate limited"),
            InternalServerError("RST_STREAM"),
        ]

        def rpc_call(call_metadata: list[tuple[str, str]]) -> str:
            observed_metadata.append(call_metadata)
            if len(observed_metadata) <= len(transient_errors):
                raise transient_errors[len(observed_metadata) - 1]
            return "recovered"

        retry_policy = Retry(
            predicate=retry_module._is_retryable_unary_error,
            initial=0.25,
            maximum=1.0,
            multiplier=1.3,
            timeout=30.0,
        )

        with (
            mock.patch("google.api_core.retry.retry_unary.time.sleep") as sleep_mock,
            mock.patch(
                "google.api_core.retry.retry_base.time.monotonic",
                side_effect=[0.0, 1.0, 2.0, 3.0],
            ),
        ):
            result = retry_module.execute_unary_with_retry(
                database=database,
                rpc_call=rpc_call,
                metadata=metadata,
                span=span,
                retry_policy=retry_policy,
                on_retry=lambda attempt, exception: retry_events.append(
                    (attempt, exception)
                ),
            )

        self.assertEqual(result, "recovered")
        self.assertEqual(metadata, metadata_snapshot)
        self.assertEqual(len(observed_metadata), 4)
        self.assertEqual(sleep_mock.call_count, 3)
        self.assertEqual(
            database.augmentation_calls,
            [
                (5, 1, metadata, span),
                (5, 2, metadata, span),
                (5, 3, metadata, span),
                (5, 4, metadata, span),
            ],
        )
        self.assertEqual(
            [item[-1] for item in observed_metadata],
            [
                ("x-goog-spanner-request-id", "1.0.5.1"),
                ("x-goog-spanner-request-id", "1.0.5.2"),
                ("x-goog-spanner-request-id", "1.0.5.3"),
                ("x-goog-spanner-request-id", "1.0.5.4"),
            ],
        )
        self.assertEqual(
            retry_events,
            [
                (1, transient_errors[0]),
                (2, transient_errors[1]),
                (3, transient_errors[2]),
            ],
        )
        self.assertEqual(database.augmented_errors, transient_errors)

    def test_execute_unary_with_retry_retryable_then_non_retryable(self) -> None:
        database = _RecordingDatabase(next_nth_request=18)
        retry_events: list[tuple[int, Exception]] = []
        first_error = ServiceUnavailable("temporary outage")
        second_error = InvalidArgument("bad request on retry")
        rpc_call = mock.MagicMock(side_effect=[first_error, second_error])
        retry_policy = Retry(
            predicate=retry_module._is_retryable_unary_error,
            initial=0.25,
            maximum=1.0,
            multiplier=1.3,
            timeout=30.0,
        )

        with (
            mock.patch("google.api_core.retry.retry_unary.time.sleep") as sleep_mock,
            mock.patch(
                "google.api_core.retry.retry_base.time.monotonic",
                side_effect=[0.0, 1.0],
            ),
            self.assertRaisesRegex(InvalidArgument, "bad request on retry"),
        ):
            retry_module.execute_unary_with_retry(
                database=database,
                rpc_call=rpc_call,
                retry_policy=retry_policy,
                on_retry=lambda attempt, exception: retry_events.append(
                    (attempt, exception)
                ),
            )

        self.assertEqual(rpc_call.call_count, 2)
        self.assertEqual(sleep_mock.call_count, 1)
        self.assertEqual(retry_events, [(1, first_error)])
        self.assertEqual(database.augmented_errors, [first_error, second_error])

    def test_execute_unary_with_retry_non_retryable_internal_error_no_retry(
        self,
    ) -> None:
        retry_policy = Retry(
            predicate=retry_module._is_retryable_unary_error,
            initial=0.25,
            maximum=1.0,
            multiplier=1.3,
            timeout=30.0,
        )
        non_retryable_errors = (
            InternalServerError("Non-retryable internal bug"),
            Aborted("Transaction aborted"),
            InvalidArgument("Invalid SQL"),
        )
        for error in non_retryable_errors:
            with self.subTest(error=error):
                database = _RecordingDatabase(next_nth_request=9)
                retry_events: list[tuple[int, Exception]] = []
                rpc_call = mock.MagicMock(side_effect=error)
                with (
                    mock.patch(
                        "google.api_core.retry.retry_unary.time.sleep"
                    ) as sleep_mock,
                    self.assertRaisesRegex(type(error), str(error.message)),
                ):
                    retry_module.execute_unary_with_retry(
                        database=database,
                        rpc_call=rpc_call,
                        retry_policy=retry_policy,
                        on_retry=lambda attempt, exception: retry_events.append(
                            (attempt, exception)
                        ),
                    )
                self.assertEqual(rpc_call.call_count, 1)
                sleep_mock.assert_not_called()
                self.assertEqual(retry_events, [])
                self.assertEqual(database.augmented_errors, [error])

    def test_execute_unary_with_retry_timeout_exceeded(self) -> None:
        database = _RecordingDatabase(next_nth_request=14)
        first_error = ServiceUnavailable("still unavailable 1")
        second_error = ServiceUnavailable("still unavailable 2")
        rpc_call = mock.MagicMock(side_effect=[first_error, second_error])
        retry_events: list[tuple[int, Exception]] = []
        retry_policy = Retry(
            predicate=retry_module._is_retryable_unary_error,
            initial=0.25,
            maximum=1.0,
            multiplier=1.3,
            timeout=5.0,
        )

        with (
            mock.patch("google.api_core.retry.retry_unary.time.sleep") as sleep_mock,
            mock.patch(
                "google.api_core.retry.retry_base.time.monotonic",
                side_effect=[0.0, 1.0, 10.0],
            ),
            self.assertRaisesRegex(
                RetryError,
                r"Timeout of 5\.0s exceeded, last exception: .*still unavailable 2",
            ) as context,
        ):
            retry_module.execute_unary_with_retry(
                database=database,
                rpc_call=rpc_call,
                retry_policy=retry_policy,
                on_retry=lambda attempt, exception: retry_events.append(
                    (attempt, exception)
                ),
            )

        self.assertIs(context.exception.__cause__, second_error)
        self.assertEqual(rpc_call.call_count, 2)
        self.assertEqual(sleep_mock.call_count, 1)
        self.assertEqual(retry_events, [(1, first_error), (2, second_error)])
        self.assertEqual(database.augmented_errors, [first_error, second_error])
        self.assertEqual(
            database.augmentation_calls,
            [(14, 1, None, None), (14, 2, None, None)],
        )

    def test_execute_unary_with_retry_preserves_existing_on_error(self) -> None:
        database = _RecordingDatabase(next_nth_request=21)
        callback_order: list[str] = []
        rpc_call = mock.MagicMock(
            side_effect=[ServiceUnavailable("retry once"), "done"]
        )

        def existing_on_error(exception: Exception) -> None:
            callback_order.append(f"user:{exception.message}")

        def on_retry(attempt: int, exception: Exception) -> None:
            callback_order.append(f"retry:{attempt}:{exception.message}")

        retry_policy = Retry(
            predicate=retry_module._is_retryable_unary_error,
            initial=0.25,
            maximum=1.0,
            multiplier=1.3,
            timeout=30.0,
            on_error=existing_on_error,
        )

        with (
            mock.patch("google.api_core.retry.retry_unary.time.sleep") as sleep_mock,
            mock.patch(
                "google.api_core.retry.retry_base.time.monotonic",
                side_effect=[0.0, 1.0],
            ),
        ):
            result = retry_module.execute_unary_with_retry(
                database=database,
                rpc_call=rpc_call,
                retry_policy=retry_policy,
                on_retry=on_retry,
            )

        self.assertEqual(result, "done")
        self.assertEqual(rpc_call.call_count, 2)
        self.assertEqual(sleep_mock.call_count, 1)
        self.assertEqual(
            callback_order,
            ["retry:1:retry once", "user:retry once"],
        )

        callback_order.clear()
        rpc_call_no_on_retry = mock.MagicMock(
            side_effect=[ServiceUnavailable("retry without hook"), "ok"]
        )
        with (
            mock.patch("google.api_core.retry.retry_unary.time.sleep") as sleep_mock,
            mock.patch(
                "google.api_core.retry.retry_base.time.monotonic",
                side_effect=[0.0, 1.0],
            ),
        ):
            result_no_hook = retry_module.execute_unary_with_retry(
                database=database,
                rpc_call=rpc_call_no_on_retry,
                retry_policy=retry_policy,
            )

        self.assertEqual(result_no_hook, "ok")
        self.assertEqual(rpc_call_no_on_retry.call_count, 2)
        self.assertEqual(sleep_mock.call_count, 1)
        self.assertEqual(callback_order, ["user:retry without hook"])

    def test_execute_unary_with_retry_on_retry_exception_propagates(self) -> None:
        database = _RecordingDatabase(next_nth_request=25)
        rpc_call = mock.MagicMock(side_effect=ServiceUnavailable("unavailable"))
        retry_policy = Retry(
            predicate=retry_module._is_retryable_unary_error,
            initial=0.25,
            maximum=1.0,
            multiplier=1.3,
            timeout=30.0,
        )

        def failing_on_retry(attempt: int, exception: Exception) -> None:
            raise RuntimeError("on_retry hook failed")

        with (
            mock.patch("google.api_core.retry.retry_unary.time.sleep") as sleep_mock,
            self.assertRaisesRegex(RuntimeError, "on_retry hook failed"),
        ):
            retry_module.execute_unary_with_retry(
                database=database,
                rpc_call=rpc_call,
                retry_policy=retry_policy,
                on_retry=failing_on_retry,
            )

        self.assertEqual(rpc_call.call_count, 1)
        sleep_mock.assert_not_called()

    def test_execute_unary_with_retry_without_timeout(self) -> None:
        database = _RecordingDatabase(next_nth_request=30)
        rpc_call = mock.MagicMock(
            side_effect=[ServiceUnavailable("retry unbounded"), "ok"]
        )
        retry_policy = Retry(
            predicate=retry_module._is_retryable_unary_error,
            initial=0.25,
            maximum=1.0,
            multiplier=1.3,
            timeout=None,
        )

        with mock.patch("google.api_core.retry.retry_unary.time.sleep") as sleep_mock:
            result = retry_module.execute_unary_with_retry(
                database=database,
                rpc_call=rpc_call,
                retry_policy=retry_policy,
            )

        self.assertEqual(result, "ok")
        self.assertEqual(rpc_call.call_count, 2)
        self.assertEqual(sleep_mock.call_count, 1)


if __name__ == "__main__":
    unittest.main()
