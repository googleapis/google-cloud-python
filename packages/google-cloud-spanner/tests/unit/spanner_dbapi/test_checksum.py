# Copyright 2020 Google LLC
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
from unittest import mock

import grpc
from google.api_core.exceptions import (
    Aborted,
    AlreadyExists,
    DeadlineExceeded,
    GoogleAPICallError,
    InternalServerError,
    InvalidArgument,
    OutOfRange,
    Unknown,
    from_grpc_error,
)

from google.cloud.spanner_dbapi.checksum import (
    RETRY_ABORTED_ERROR,
    ChecksumIterator,
    ResultsChecksum,
    _compare_checksums,
    _errors_equal_for_retry,
)
from google.cloud.spanner_dbapi.exceptions import (
    IntegrityError,
    InterfaceError,
    OperationalError,
    RetryAborted,
)
from google.cloud.spanner_v1.exceptions import wrap_with_request_id


class Test_compare_checksums(unittest.TestCase):
    def test_equal(self):
        original = ResultsChecksum()
        original.consume_result(5)

        retried = ResultsChecksum()
        retried.consume_result(5)

        self.assertIsNone(_compare_checksums(original, retried))

    def test_less_results(self):
        original = ResultsChecksum()
        original.consume_result(5)

        retried = ResultsChecksum()

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            _compare_checksums(original, retried)

    def test_more_results(self):
        original = ResultsChecksum()
        original.consume_result(5)

        retried = ResultsChecksum()
        retried.consume_result(5)
        retried.consume_result(2)

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            _compare_checksums(original, retried)

    def test_mismatch(self):
        original = ResultsChecksum()
        original.consume_result(5)

        retried = ResultsChecksum()
        retried.consume_result(2)

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            _compare_checksums(original, retried)


class TestErrorsEqualForRetry(unittest.TestCase):
    def test_none_inputs(self):
        err = ValueError("boom")
        self.assertFalse(_errors_equal_for_retry(None, None))
        self.assertFalse(_errors_equal_for_retry(err, None))
        self.assertFalse(_errors_equal_for_retry(None, err))

    def test_same_instance(self):
        err = ValueError("boom")
        self.assertTrue(_errors_equal_for_retry(err, err))

    def test_same_grpc_status_code_matching_and_different_messages(self):
        self.assertTrue(
            _errors_equal_for_retry(
                InternalServerError("same"),
                InternalServerError("same"),
            )
        )
        self.assertTrue(
            _errors_equal_for_retry(
                DeadlineExceeded("timeout"),
                DeadlineExceeded("timeout"),
            )
        )
        self.assertFalse(
            _errors_equal_for_retry(
                InternalServerError("req-1"),
                InternalServerError("req-2"),
            )
        )
        self.assertFalse(
            _errors_equal_for_retry(
                InvalidArgument("bad 1"),
                InvalidArgument("bad 2"),
            )
        )
        self.assertFalse(
            _errors_equal_for_retry(
                DeadlineExceeded("timeout 1"),
                DeadlineExceeded("timeout 2"),
            )
        )

    def test_different_grpc_status_codes(self):
        self.assertFalse(
            _errors_equal_for_retry(
                InvalidArgument("same"),
                InternalServerError("same"),
            )
        )

    def test_wrapped_dbapi_cause_grpc_status_code(self):
        first_cause = InternalServerError("same cause message")
        first_error = OperationalError(["detail-1"])
        first_error.__cause__ = first_cause

        second_cause = InternalServerError("same cause message")
        second_error = OperationalError(["detail-2"])
        second_error.__cause__ = second_cause

        self.assertTrue(_errors_equal_for_retry(first_error, second_error))

        different_cause = InternalServerError("different cause message")
        different_error = OperationalError(["detail-1"])
        different_error.__cause__ = different_cause
        self.assertFalse(_errors_equal_for_retry(first_error, different_error))

        third_cause = AlreadyExists("dup")
        third_error = IntegrityError([])
        third_error.__cause__ = third_cause

        fourth_cause = OutOfRange("oob")
        fourth_error = IntegrityError([])
        fourth_error.__cause__ = fourth_cause

        self.assertFalse(_errors_equal_for_retry(third_error, fourth_error))

        error_without_cause = IntegrityError([])
        self.assertFalse(_errors_equal_for_retry(third_error, error_without_cause))
        self.assertFalse(_errors_equal_for_retry(error_without_cause, fourth_error))

    def test_unknown_ok_and_rpc_details_matching(self):
        self.assertFalse(
            _errors_equal_for_retry(
                Unknown("err-1"),
                Unknown("err-2"),
            )
        )
        self.assertTrue(
            _errors_equal_for_retry(
                Unknown("same"),
                Unknown("same"),
            )
        )

        class FakeRpcError(Exception):
            def __init__(self, message, status_code):
                super().__init__(message)
                self._status_code = status_code

            def code(self):
                return self._status_code

        class FakeRpcErrorWithDetails(FakeRpcError):
            def __init__(self, message, status_code, details_text):
                super().__init__(message, status_code)
                self._details_text = details_text

            def details(self):
                return self._details_text

        self.assertFalse(
            _errors_equal_for_retry(
                FakeRpcError("ok-1", grpc.StatusCode.OK),
                FakeRpcError("ok-2", grpc.StatusCode.OK),
            )
        )
        self.assertTrue(
            _errors_equal_for_retry(
                FakeRpcError("unavail", grpc.StatusCode.UNAVAILABLE),
                FakeRpcError("unavail", grpc.StatusCode.UNAVAILABLE),
            )
        )
        self.assertFalse(
            _errors_equal_for_retry(
                FakeRpcError("unavail-1", grpc.StatusCode.UNAVAILABLE),
                FakeRpcError("unavail-2", grpc.StatusCode.UNAVAILABLE),
            )
        )
        self.assertTrue(
            _errors_equal_for_retry(
                FakeRpcErrorWithDetails(
                    "wrapper-1", grpc.StatusCode.UNAVAILABLE, "same details"
                ),
                FakeRpcErrorWithDetails(
                    "wrapper-2", grpc.StatusCode.UNAVAILABLE, "same details"
                ),
            )
        )
        self.assertFalse(
            _errors_equal_for_retry(
                FakeRpcErrorWithDetails(
                    "same", grpc.StatusCode.UNAVAILABLE, "details-1"
                ),
                FakeRpcErrorWithDetails(
                    "same", grpc.StatusCode.UNAVAILABLE, "details-2"
                ),
            )
        )

    def test_non_grpc_exceptions_fallback_to_type_and_args(self):
        self.assertTrue(
            _errors_equal_for_retry(
                GoogleAPICallError("same"),
                GoogleAPICallError("same"),
            )
        )
        self.assertFalse(
            _errors_equal_for_retry(
                GoogleAPICallError("one"),
                GoogleAPICallError("two"),
            )
        )
        self.assertTrue(_errors_equal_for_retry(ValueError("a"), ValueError("a")))
        self.assertFalse(_errors_equal_for_retry(ValueError("a"), ValueError("b")))
        self.assertFalse(_errors_equal_for_retry(ValueError("a"), TypeError("a")))

    def test_google_api_call_error_response_code_and_non_status_code(self):
        class FakeResponse:
            def __init__(self, status_code):
                self._status_code = status_code

            def code(self):
                return self._status_code

        class NonStatusCodeError(Exception):
            def code(self):
                return 500

        self.assertTrue(
            _errors_equal_for_retry(
                GoogleAPICallError(
                    "msg", response=FakeResponse(grpc.StatusCode.UNAVAILABLE)
                ),
                GoogleAPICallError(
                    "msg", response=FakeResponse(grpc.StatusCode.UNAVAILABLE)
                ),
            )
        )
        self.assertFalse(
            _errors_equal_for_retry(
                GoogleAPICallError(
                    "msg-1", response=FakeResponse(grpc.StatusCode.UNAVAILABLE)
                ),
                GoogleAPICallError(
                    "msg-2", response=FakeResponse(grpc.StatusCode.UNAVAILABLE)
                ),
            )
        )
        self.assertFalse(
            _errors_equal_for_retry(
                GoogleAPICallError("msg-1", response=FakeResponse(503)),
                GoogleAPICallError("msg-2", response=FakeResponse(503)),
            )
        )
        self.assertFalse(
            _errors_equal_for_retry(
                NonStatusCodeError("err-1"),
                NonStatusCodeError("err-2"),
            )
        )

    def test_from_grpc_error_with_request_id_matches_raw_grpc_status(self):
        class StubRpcError(grpc.RpcError):
            def __init__(self, status_code, details_message):
                super().__init__()
                self._status_code = status_code
                self._details_message = details_message

            def code(self):
                return self._status_code

            def details(self):
                return self._details_message

            def trailing_metadata(self):
                return ()

        error_1 = wrap_with_request_id(
            from_grpc_error(
                StubRpcError(grpc.StatusCode.INVALID_ARGUMENT, "Division by zero")
            ),
            "1.1.1.1.1",
        )
        error_2 = wrap_with_request_id(
            from_grpc_error(
                StubRpcError(grpc.StatusCode.INVALID_ARGUMENT, "Division by zero")
            ),
            "1.1.1.1.2",
        )
        error_diff_msg = wrap_with_request_id(
            from_grpc_error(
                StubRpcError(grpc.StatusCode.INVALID_ARGUMENT, "Out of range")
            ),
            "1.1.1.1.3",
        )

        self.assertTrue(_errors_equal_for_retry(error_1, error_2))
        self.assertFalse(_errors_equal_for_retry(error_1, error_diff_msg))

        wrapped_1 = IntegrityError([])
        wrapped_1.__cause__ = error_1
        wrapped_2 = IntegrityError([])
        wrapped_2.__cause__ = error_2
        self.assertTrue(_errors_equal_for_retry(wrapped_1, wrapped_2))

    def test_grpc_error_none_details_falls_back_to_error_message(self):
        class NoneDetailsRpcError(grpc.RpcError):
            def __init__(self, status_code, details_message, string_repr):
                super().__init__()
                self._status_code = status_code
                self._details_message = details_message
                self._string_repr = string_repr

            def code(self):
                return self._status_code

            def details(self):
                return self._details_message

            def __str__(self):
                return self._string_repr

        first_api_error = InvalidArgument(
            "Division by zero",
            response=NoneDetailsRpcError(
                grpc.StatusCode.INVALID_ARGUMENT, None, "unused"
            ),
        )
        second_api_error = InvalidArgument(
            "Out of range",
            response=NoneDetailsRpcError(
                grpc.StatusCode.INVALID_ARGUMENT, None, "unused"
            ),
        )
        self.assertFalse(_errors_equal_for_retry(first_api_error, second_api_error))
        self.assertTrue(
            _errors_equal_for_retry(
                first_api_error,
                InvalidArgument(
                    "Division by zero",
                    response=NoneDetailsRpcError(
                        grpc.StatusCode.INVALID_ARGUMENT, None, "unused"
                    ),
                ),
            )
        )

        # Empty string details should still be used verbatim rather than replaced
        # with GoogleAPICallError.message.
        self.assertTrue(
            _errors_equal_for_retry(
                InvalidArgument(
                    "ignored-1",
                    response=NoneDetailsRpcError(
                        grpc.StatusCode.INVALID_ARGUMENT, "", "unused"
                    ),
                ),
                InvalidArgument(
                    "ignored-2",
                    response=NoneDetailsRpcError(
                        grpc.StatusCode.INVALID_ARGUMENT, "", "unused"
                    ),
                ),
            )
        )

        first_rpc_error = NoneDetailsRpcError(
            grpc.StatusCode.INVALID_ARGUMENT, None, "rpc detail A"
        )
        second_rpc_error = NoneDetailsRpcError(
            grpc.StatusCode.INVALID_ARGUMENT, None, "rpc detail B"
        )
        self.assertFalse(_errors_equal_for_retry(first_rpc_error, second_rpc_error))
        self.assertTrue(
            _errors_equal_for_retry(
                first_rpc_error,
                NoneDetailsRpcError(
                    grpc.StatusCode.INVALID_ARGUMENT, None, "rpc detail A"
                ),
            )
        )

    def test_cyclic_cause_chain_terminates_cleanly(self):
        first_error = OperationalError(["same"])
        second_error = OperationalError(["cause"])
        first_error.__cause__ = second_error
        second_error.__cause__ = first_error

        matching_first = OperationalError(["same"])
        matching_second = OperationalError(["cause"])
        matching_first.__cause__ = matching_second
        matching_second.__cause__ = matching_first

        different_error = OperationalError(["other"])
        different_error.__cause__ = different_error

        self.assertTrue(_errors_equal_for_retry(first_error, matching_first))
        self.assertFalse(_errors_equal_for_retry(first_error, different_error))


def _iter_with_error(rows, error):
    for row in rows:
        yield row
    raise error


class _CloseableIterator:
    def __init__(self, rows):
        self._iter = iter(rows)
        self.close_count = 0

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)

    def close(self):
        self.close_count += 1


class TestChecksumIterator(unittest.TestCase):
    def test_none_iterator_raises(self):
        with self.assertRaisesRegex(ValueError, "iterator must not be None"):
            ChecksumIterator(None)

    def test_iterate_all_rows_and_eof_sticky(self):
        rows = [(1, "a"), (2, "b")]
        checksum_iterator = ChecksumIterator(iter(rows))
        self.assertIs(iter(checksum_iterator), checksum_iterator)

        consumed = list(checksum_iterator)
        self.assertEqual(consumed, rows)
        self.assertEqual(checksum_iterator.next_count, 3)
        self.assertTrue(checksum_iterator.eof_reached)
        self.assertIsNone(checksum_iterator.error)
        self.assertIsNone(checksum_iterator.error_index)

        # Calling next() again after EOF must not advance next_count.
        with self.assertRaises(StopIteration):
            next(checksum_iterator)
        self.assertEqual(checksum_iterator.next_count, 3)

    def test_non_aborted_error_recorded_and_sticky(self):
        rows = [(1,), (2,)]
        original_error = InternalServerError("mid-stream boom")
        checksum_iterator = ChecksumIterator(_iter_with_error(rows, original_error))

        self.assertEqual(next(checksum_iterator), (1,))
        self.assertEqual(next(checksum_iterator), (2,))
        with self.assertRaisesRegex(InternalServerError, "mid-stream boom"):
            next(checksum_iterator)

        self.assertEqual(checksum_iterator.next_count, 3)
        self.assertIs(checksum_iterator.error, original_error)
        self.assertEqual(checksum_iterator.error_index, 2)
        self.assertFalse(checksum_iterator.eof_reached)
        self.assertEqual(len(checksum_iterator.checksum), 2)

        # Subsequent next() calls re-raise the same error without advancing next_count.
        with self.assertRaisesRegex(InternalServerError, "mid-stream boom"):
            next(checksum_iterator)
        self.assertEqual(checksum_iterator.next_count, 3)

    def test_aborted_without_callback_does_not_mutate_state(self):
        checksum_iterator = ChecksumIterator(_iter_with_error([(1,)], Aborted("abort")))

        self.assertEqual(next(checksum_iterator), (1,))
        with self.assertRaisesRegex(Aborted, "abort"):
            next(checksum_iterator)

        self.assertEqual(checksum_iterator.next_count, 1)
        self.assertIsNone(checksum_iterator.error)
        self.assertIsNone(checksum_iterator.error_index)
        self.assertFalse(checksum_iterator.eof_reached)

    def test_aborted_with_retry_callback_resumes(self):
        retry_callback = mock.Mock()

        def on_retry():
            checksum_iterator.retry(iter([(1,), (2,), (3,)]))

        retry_callback.side_effect = on_retry
        checksum_iterator = ChecksumIterator(
            _iter_with_error([(1,)], Aborted("abort")),
            retry_callback=retry_callback,
        )

        self.assertEqual(list(checksum_iterator), [(1,), (2,), (3,)])
        self.assertEqual(retry_callback.call_count, 1)
        self.assertEqual(checksum_iterator.next_count, 4)
        self.assertTrue(checksum_iterator.eof_reached)

    def test_aborted_with_failing_retry_callback_propagates_retry_aborted(self):
        retry_callback = mock.Mock(side_effect=RetryAborted(RETRY_ABORTED_ERROR))
        checksum_iterator = ChecksumIterator(
            _iter_with_error([(1,)], Aborted("abort")),
            retry_callback=retry_callback,
        )

        self.assertEqual(next(checksum_iterator), (1,))
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            next(checksum_iterator)

        self.assertEqual(retry_callback.call_count, 1)
        self.assertEqual(checksum_iterator.next_count, 1)
        self.assertIsNone(checksum_iterator.error)

    def test_retry_zero_consumed(self):
        old_iterator = iter([(1,), (2,)])
        new_iterator = iter([(1,), (2,), (3,)])
        checksum_iterator = ChecksumIterator(old_iterator)

        checksum_iterator.retry(new_iterator)

        self.assertIs(checksum_iterator.iterator, new_iterator)
        self.assertEqual(list(checksum_iterator), [(1,), (2,), (3,)])

    def test_retry_none_new_iterator_raises(self):
        checksum_iterator = ChecksumIterator(iter([(1,)]))
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(None)

    def test_retry_partial_consumption_success(self):
        old_gen = (row for row in [(1,), (2,), (3,)])
        new_gen = (row for row in [(1,), (2,), (3,), (4,)])
        checksum_iterator = ChecksumIterator(old_gen)

        self.assertEqual(next(checksum_iterator), (1,))
        self.assertEqual(next(checksum_iterator), (2,))

        checksum_iterator.retry(new_gen)

        self.assertIs(checksum_iterator.iterator, new_gen)
        # Old generator was closed upon swap.
        self.assertIsNone(old_gen.gi_frame)
        self.assertEqual(list(checksum_iterator), [(3,), (4,)])

    def test_retry_partial_consumption_checksum_mismatch_keeps_old_iterator(self):
        old_iterator = iter([(1,), (2,)])
        new_gen = (row for row in [(1,), (99,)])
        checksum_iterator = ChecksumIterator(old_iterator)

        self.assertEqual(next(checksum_iterator), (1,))
        self.assertEqual(next(checksum_iterator), (2,))

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(new_gen)

        self.assertIs(checksum_iterator.iterator, old_iterator)
        self.assertIsNone(new_gen.gi_frame)

    def test_retry_partial_consumption_unexpected_eof(self):
        checksum_iterator = ChecksumIterator(iter([(1,), (2,), (3,)]))
        self.assertEqual(next(checksum_iterator), (1,))
        self.assertEqual(next(checksum_iterator), (2,))

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(iter([(1,)]))

    def test_retry_partial_consumption_unexpected_error(self):
        checksum_iterator = ChecksumIterator(iter([(1,), (2,)]))
        self.assertEqual(next(checksum_iterator), (1,))
        self.assertEqual(next(checksum_iterator), (2,))

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(_iter_with_error([(1,)], ValueError("unexpected")))

    def test_retry_partial_consumption_aborted_propagates(self):
        old_iterator = iter([(1,), (2,)])
        checksum_iterator = ChecksumIterator(old_iterator)
        self.assertEqual(next(checksum_iterator), (1,))

        with self.assertRaisesRegex(Aborted, "retry aborted"):
            checksum_iterator.retry(_iter_with_error([], Aborted("retry aborted")))

        self.assertIs(checksum_iterator.iterator, old_iterator)

    def test_retry_eof_verification(self):
        checksum_iterator = ChecksumIterator(iter([(1,), (2,)]))
        self.assertEqual(list(checksum_iterator), [(1,), (2,)])

        # Exact match succeeds.
        new_iterator = iter([(1,), (2,)])
        checksum_iterator.retry(new_iterator)
        self.assertIs(checksum_iterator.iterator, new_iterator)

        # Concurrent insert past EOF fails.
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(iter([(1,), (2,), (3,)]))

        # Concurrent delete (earlier EOF) fails.
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(iter([(1,)]))

        # Concurrent modification with same row count fails.
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(iter([(1,), (99,)]))

    def test_retry_empty_result_set_eof_detects_concurrent_insert(self):
        checksum_iterator = ChecksumIterator(iter([]))
        self.assertEqual(list(checksum_iterator), [])
        self.assertTrue(checksum_iterator.eof_reached)
        self.assertEqual(checksum_iterator.next_count, 1)

        # Still empty succeeds.
        checksum_iterator.retry(iter([]))

        # Newly inserted row fails.
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(iter([(1,)]))

    def test_retry_mid_stream_error_matching(self):
        checksum_iterator = ChecksumIterator(
            _iter_with_error([(1,), (2,)], InternalServerError("mid-stream err"))
        )
        self.assertEqual(next(checksum_iterator), (1,))
        self.assertEqual(next(checksum_iterator), (2,))
        with self.assertRaisesRegex(InternalServerError, "mid-stream err"):
            next(checksum_iterator)

        # Same prefix and matching gRPC status code + message at error_index succeeds.
        new_iterator = _iter_with_error(
            [(1,), (2,)], InternalServerError("mid-stream err")
        )
        checksum_iterator.retry(new_iterator)
        self.assertIs(checksum_iterator.iterator, new_iterator)

        # Different prefix row fails.
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(
                _iter_with_error([(1,), (99,)], InternalServerError("mid-stream err"))
            )

        # Replay succeeds past error_index fails.
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(iter([(1,), (2,), (3,)]))

        # Replay reaches EOF at error_index fails.
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(iter([(1,), (2,)]))

        # Replay raises same status code with different message fails.
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(
                _iter_with_error([(1,), (2,)], InternalServerError("different msg"))
            )

        # Replay raises different error code at error_index fails.
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(
                _iter_with_error([(1,), (2,)], InvalidArgument("mid-stream err"))
            )

        # Replay raises same error at earlier index fails.
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(
                _iter_with_error([(1,)], InternalServerError("mid-stream err"))
            )

    def test_retry_error_on_first_row(self):
        checksum_iterator = ChecksumIterator(
            _iter_with_error([], InvalidArgument("bad arg"))
        )
        with self.assertRaisesRegex(InvalidArgument, "bad arg"):
            next(checksum_iterator)

        checksum_iterator.retry(_iter_with_error([], InvalidArgument("bad arg")))

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(_iter_with_error([], InvalidArgument("other arg")))

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(iter([(1,)]))

    def test_retry_terminal_state_aborted_propagates(self):
        eof_iterator = ChecksumIterator(iter([(1,)]))
        self.assertEqual(list(eof_iterator), [(1,)])

        with self.assertRaisesRegex(Aborted, "abort at eof"):
            eof_iterator.retry(_iter_with_error([(1,)], Aborted("abort at eof")))

        error_iterator = ChecksumIterator(
            _iter_with_error([(1,)], InternalServerError("req-1"))
        )
        self.assertEqual(next(error_iterator), (1,))
        with self.assertRaisesRegex(InternalServerError, "req-1"):
            next(error_iterator)

        with self.assertRaisesRegex(Aborted, "abort at err"):
            error_iterator.retry(_iter_with_error([(1,)], Aborted("abort at err")))

    def test_close_marks_closed_and_closes_closeable_iterator(self):
        underlying = _CloseableIterator([(1,), (2,)])
        checksum_iterator = ChecksumIterator(underlying)
        self.assertFalse(checksum_iterator.is_closed)
        self.assertEqual(next(checksum_iterator), (1,))

        checksum_iterator.close()
        checksum_iterator.close()  # Idempotent.

        self.assertTrue(checksum_iterator.is_closed)
        self.assertEqual(underlying.close_count, 1)
        with self.assertRaisesRegex(
            InterfaceError, "ChecksumIterator is already closed."
        ):
            next(checksum_iterator)

    def test_retry_when_closed_verifies_and_closes_new_iterator(self):
        original = _CloseableIterator([(1,), (2,)])
        checksum_iterator = ChecksumIterator(original)
        self.assertEqual(next(checksum_iterator), (1,))
        checksum_iterator.close()

        replacement = _CloseableIterator([(1,), (2,)])
        checksum_iterator.retry(replacement)

        self.assertTrue(checksum_iterator.is_closed)
        self.assertIs(checksum_iterator.iterator, original)
        self.assertEqual(replacement.close_count, 1)

        mismatched = _CloseableIterator([(99,), (2,)])
        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            checksum_iterator.retry(mismatched)
        self.assertEqual(mismatched.close_count, 1)

    def test_close_iterator_exception_logged_and_does_not_mask_retry_error(self):
        class FailingCloseIterator:
            def __init__(self, rows):
                self._iter = iter(rows)

            def __iter__(self):
                return self

            def __next__(self):
                return next(self._iter)

            def close(self):
                raise RuntimeError("close failure")

        checksum_iterator = ChecksumIterator(FailingCloseIterator([(1,)]))
        self.assertEqual(next(checksum_iterator), (1,))

        with self.assertLogs(
            "google.cloud.spanner_dbapi.checksum", level="WARNING"
        ) as captured_logs:
            with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
                checksum_iterator.retry(FailingCloseIterator([(99,)]))

        self.assertIn(
            "Failed to close iterator: close failure", captured_logs.output[0]
        )

        with self.assertLogs(
            "google.cloud.spanner_dbapi.checksum", level="WARNING"
        ) as close_logs:
            checksum_iterator.close()

        self.assertIn("Failed to close iterator: close failure", close_logs.output[0])

    def test_next_raises_if_closed_during_retry_callback(self):
        def close_during_retry():
            checksum_iterator.close()

        checksum_iterator = ChecksumIterator(
            _iter_with_error([(1,)], Aborted("abort")),
            retry_callback=close_during_retry,
        )

        self.assertEqual(next(checksum_iterator), (1,))
        with self.assertRaisesRegex(
            InterfaceError, "ChecksumIterator is already closed."
        ):
            next(checksum_iterator)

    def test_close_after_eof_and_after_error_raises_interface_error_on_next(self):
        eof_iterator = ChecksumIterator(iter([(1,)]))
        self.assertEqual(next(eof_iterator), (1,))
        with self.assertRaises(StopIteration):
            next(eof_iterator)
        eof_iterator.close()
        with self.assertRaisesRegex(
            InterfaceError, "ChecksumIterator is already closed."
        ):
            next(eof_iterator)

        error_iterator = ChecksumIterator(
            _iter_with_error([(1,)], InternalServerError("mid-stream boom"))
        )
        self.assertEqual(next(error_iterator), (1,))
        with self.assertRaisesRegex(InternalServerError, "mid-stream boom"):
            next(error_iterator)
        error_iterator.close()
        with self.assertRaisesRegex(
            InterfaceError, "ChecksumIterator is already closed."
        ):
            next(error_iterator)

    def test_next_multiple_aborted_retries_during_consumption(self):
        attempts = [0]

        def retry_callback():
            attempts[0] += 1
            if attempts[0] == 1:
                checksum_iterator.retry(
                    _iter_with_error([(1,), (2,), (3,)], Aborted("abort-2"))
                )
            else:
                checksum_iterator.retry(iter([(1,), (2,), (3,), (4,)]))

        checksum_iterator = ChecksumIterator(
            _iter_with_error([(1,)], Aborted("abort-1")),
            retry_callback=retry_callback,
        )

        self.assertEqual(list(checksum_iterator), [(1,), (2,), (3,), (4,)])
        self.assertEqual(attempts[0], 2)
