# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock

import pytest  # type: ignore

from google.auth import transport

try:
    import grpc  # type: ignore

    from google.auth.transport import mtls_interceptor

    HAS_GRPC = True
except ImportError:  # pragma: NO COVER
    HAS_GRPC = False

pytestmark = pytest.mark.skipif(not HAS_GRPC, reason="gRPC is unavailable.")

CHECK_PARAMS = (
    "google.auth.transport._mtls_helper.check_parameters_for_unauthorized_response"
)
SHOULD_RETRY = (
    "google.auth.transport.mtls_interceptor.CertRotationInterceptor._should_retry"
)


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


class FakeRpcError(grpc.RpcError, grpc.Call, grpc.Future):
    """An RpcError that, like grpc's _InactiveRpcError, is also a finished call."""

    def __init__(self, code, details="error"):
        super().__init__()
        self._code = code
        self._details = details

    def code(self):
        return self._code

    def details(self):
        return self._details

    def initial_metadata(self):
        return None

    def trailing_metadata(self):
        return None

    def is_active(self):
        return False

    def time_remaining(self):
        return None

    def add_callback(self, callback):
        return False

    def cancel(self):
        return False

    def cancelled(self):
        return False

    def running(self):
        return False

    def done(self):
        return True

    def result(self, timeout=None):
        raise self

    def exception(self, timeout=None):
        return self

    def traceback(self, timeout=None):
        return None

    def add_done_callback(self, fn):
        fn(self)


class CompletedFuture(object):
    """An inner unary future that is already finished.

    This mirrors what grpc's blocking ``__call__`` / ``with_call`` path hands to
    an interceptor: ``add_done_callback`` runs the callback synchronously.
    """

    def __init__(self, result=None, exception=None, cancelled=False):
        self._result = result
        self._exception = exception
        self._cancelled = cancelled

    def add_done_callback(self, fn):
        fn(self)

    def cancelled(self):
        return self._cancelled

    def exception(self, timeout=None):
        return self._exception

    def result(self, timeout=None):
        if self._exception is not None:
            raise self._exception
        return self._result

    def code(self):
        if self._exception is not None and hasattr(self._exception, "code"):
            return self._exception.code()
        return grpc.StatusCode.OK

    def details(self):
        return "details"

    def initial_metadata(self):
        return ("initial", "md")

    def trailing_metadata(self):
        return ("trailing", "md")

    def traceback(self, timeout=None):
        return None


class FakeStreamCall(object):
    """An inner response-streaming call backed by a list of items/exceptions."""

    def __init__(self, items, code=grpc.StatusCode.OK):
        self._items = list(items)
        self._code = code
        self.done_callbacks = []

    def __iter__(self):
        return self

    def __next__(self):
        if not self._items:
            raise StopIteration()
        item = self._items.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item

    def add_done_callback(self, fn):
        self.done_callbacks.append(fn)

    def fire_done(self):
        for fn in self.done_callbacks:
            fn(self)

    def code(self):
        return self._code


def make_interceptor(cached_cert=b"old-cert"):
    wrapper = mock.Mock(spec=["_cached_cert", "refresh_logic"])
    wrapper._cached_cert = cached_cert
    return mtls_interceptor.CertRotationInterceptor(wrapper=wrapper), wrapper


def call_details(timeout=None):
    return mtls_interceptor._ClientCallDetails(
        method="/svc/Method",
        timeout=timeout,
        metadata=None,
        credentials=None,
        wait_for_ready=None,
    )


def unauthenticated():
    return FakeRpcError(grpc.StatusCode.UNAUTHENTICATED, "cert mismatch")


# ---------------------------------------------------------------------------
# CertRotationInterceptor
# ---------------------------------------------------------------------------


class TestCertRotationInterceptor(object):
    def test_init_defaults(self):
        interceptor = mtls_interceptor.CertRotationInterceptor()
        assert interceptor._wrapper is None
        assert interceptor._max_retries == transport.DEFAULT_MAX_REFRESH_ATTEMPTS

    def test_init_with_wrapper(self):
        wrapper = mock.Mock()
        interceptor = mtls_interceptor.CertRotationInterceptor(wrapper=wrapper)
        assert interceptor._wrapper is wrapper

    def test_should_retry_without_wrapper(self):
        interceptor = mtls_interceptor.CertRotationInterceptor()
        assert interceptor._should_retry(
            grpc.StatusCode.UNAUTHENTICATED, 0, b"cert"
        ) == (False, None, None)

    @pytest.mark.parametrize(
        "code", [None, grpc.StatusCode.OK, grpc.StatusCode.INTERNAL]
    )
    def test_should_retry_non_unauthenticated(self, code):
        interceptor, _ = make_interceptor()
        with mock.patch(CHECK_PARAMS) as check:
            assert interceptor._should_retry(code, 0, b"old-cert") == (
                False,
                None,
                None,
            )
        check.assert_not_called()

    def test_should_retry_max_retries_reached(self):
        interceptor, _ = make_interceptor()
        with mock.patch(CHECK_PARAMS) as check:
            assert interceptor._should_retry(
                grpc.StatusCode.UNAUTHENTICATED,
                transport.DEFAULT_MAX_REFRESH_ATTEMPTS,
                b"old-cert",
            ) == (False, None, None)
        check.assert_not_called()

    def test_should_retry_channel_already_refreshed_by_other_thread(self):
        interceptor, _ = make_interceptor(cached_cert=b"new-cert")
        with mock.patch(CHECK_PARAMS) as check:
            assert interceptor._should_retry(
                grpc.StatusCode.UNAUTHENTICATED, 0, b"old-cert"
            ) == (True, None, None)
        check.assert_not_called()

    def test_should_retry_cert_rotated_returns_new_material(self):
        interceptor, _ = make_interceptor()
        with mock.patch(CHECK_PARAMS) as check:
            check.return_value = (b"new-cert", b"new-key", "fp1", "fp2")
            assert interceptor._should_retry(
                grpc.StatusCode.UNAUTHENTICATED, 0, b"old-cert"
            ) == (True, b"new-cert", b"new-key")
        check.assert_called_once_with(b"old-cert")

    def test_should_retry_cert_not_rotated(self):
        interceptor, _ = make_interceptor()
        with mock.patch(CHECK_PARAMS) as check:
            check.return_value = (b"old-cert", b"key", "fp1", "fp1")
            should_retry, *_ = interceptor._should_retry(
                grpc.StatusCode.UNAUTHENTICATED, 0, b"old-cert"
            )
        assert should_retry is False

    def test_intercept_methods_return_wrappers(self):
        interceptor = mtls_interceptor.CertRotationInterceptor()

        def unary_continuation(details, request):
            return CompletedFuture(result="ok")

        def stream_continuation(details, request):
            return FakeStreamCall([])

        assert isinstance(
            interceptor.intercept_unary_unary(unary_continuation, call_details(), "r"),
            mtls_interceptor._RetryableUnaryResponseFuture,
        )
        assert isinstance(
            interceptor.intercept_stream_unary(
                unary_continuation, call_details(), iter(["r"])
            ),
            mtls_interceptor._RetryableUnaryResponseFuture,
        )
        assert isinstance(
            interceptor.intercept_unary_stream(
                stream_continuation, call_details(), "r"
            ),
            mtls_interceptor._RetryableStreamResponseIterator,
        )
        assert isinstance(
            interceptor.intercept_stream_stream(
                stream_continuation, call_details(), iter(["r"])
            ),
            mtls_interceptor._RetryableStreamResponseIterator,
        )


# ---------------------------------------------------------------------------
# MTLSRefreshingChannel
# ---------------------------------------------------------------------------


class TestMTLSRefreshingChannel(object):
    def make_channel(self):
        old_channel = mock.Mock()
        new_channel = mock.Mock()
        create_channel_fn = mock.Mock(return_value=new_channel)
        channel = mtls_interceptor.MTLSRefreshingChannel(
            "example.com:443", create_channel_fn, old_channel, b"old-cert"
        )
        return channel, create_channel_fn, old_channel, new_channel

    @pytest.mark.parametrize("cert", [None, b"", b"old-cert"])
    def test_refresh_logic_noop_without_new_cert(self, cert):
        channel, create_channel_fn, old_channel, _ = self.make_channel()
        channel.refresh_logic(1, call_cert_bytes=cert, call_key_bytes=b"key")
        create_channel_fn.assert_not_called()
        assert channel._channel is old_channel
        assert channel._cached_cert == b"old-cert"

    @mock.patch("grpc.ssl_channel_credentials", autospec=True)
    def test_refresh_logic_rebuilds_channel(self, ssl_channel_credentials):
        channel, create_channel_fn, old_channel, new_channel = self.make_channel()
        subscriber = mock.Mock()
        channel.subscribe(subscriber)

        channel.refresh_logic(1, call_cert_bytes=b"new-cert", call_key_bytes=b"new-key")

        ssl_channel_credentials.assert_called_once_with(
            certificate_chain=b"new-cert", private_key=b"new-key"
        )
        create_channel_fn.assert_called_once_with(
            ssl_credentials=ssl_channel_credentials.return_value,
            client_cert_callback=None,
        )
        assert channel._channel is new_channel
        assert channel._cached_cert == b"new-cert"
        # Subscribers move to the new channel.
        old_channel.unsubscribe.assert_called_once_with(subscriber)
        new_channel.subscribe.assert_called_once_with(subscriber)
        # The old channel is not closed so in-flight RPCs on it can finish.
        old_channel.close.assert_not_called()

    @mock.patch("grpc.ssl_channel_credentials", autospec=True)
    def test_refresh_logic_ignores_unsubscribe_errors(self, ssl_channel_credentials):
        channel, _, old_channel, new_channel = self.make_channel()
        subscriber = mock.Mock()
        channel.subscribe(subscriber)
        old_channel.unsubscribe.side_effect = ValueError("already gone")

        channel.refresh_logic(1, call_cert_bytes=b"new-cert", call_key_bytes=b"k")

        new_channel.subscribe.assert_called_once_with(subscriber)

    @mock.patch("grpc.ssl_channel_credentials", autospec=True)
    def test_refresh_logic_failure_keeps_cached_cert(self, ssl_channel_credentials):
        channel, create_channel_fn, old_channel, _ = self.make_channel()
        create_channel_fn.side_effect = RuntimeError("cannot build channel")

        with pytest.raises(RuntimeError):
            channel.refresh_logic(1, call_cert_bytes=b"new-cert", call_key_bytes=b"k")

        # State is not half-updated, so a later 401 can still trigger a refresh.
        assert channel._cached_cert == b"old-cert"
        assert channel._channel is old_channel

    @pytest.mark.parametrize(
        "method", ["unary_unary", "unary_stream", "stream_unary", "stream_stream"]
    )
    def test_multicallables_use_current_channel(self, method):
        channel, _, old_channel, new_channel = self.make_channel()
        assert (
            getattr(channel, method)("/svc/M")
            is getattr(old_channel, method).return_value
        )

        channel._channel = new_channel
        assert (
            getattr(channel, method)("/svc/M", "extra", kw=1)
            is getattr(new_channel, method).return_value
        )
        getattr(new_channel, method).assert_called_once_with("/svc/M", "extra", kw=1)

    def test_subscribe_unsubscribe_close(self):
        channel, _, old_channel, _ = self.make_channel()
        callback = mock.Mock()

        channel.subscribe(callback, try_to_connect=True)
        assert callback in channel._subscribers
        old_channel.subscribe.assert_called_once_with(callback, try_to_connect=True)

        channel.unsubscribe(callback)
        assert callback not in channel._subscribers
        old_channel.unsubscribe.assert_called_once_with(callback)

        channel.close()
        old_channel.close.assert_called_once_with()


# ---------------------------------------------------------------------------
# _ReplayableIterator
# ---------------------------------------------------------------------------


class TestReplayableIterator(object):
    def test_accepts_plain_iterables(self):
        replayable = mtls_interceptor._ReplayableIterator([b"a", b"b"])
        assert list(iter(replayable)) == [b"a", b"b"]

    def test_replays_buffered_items_on_new_reader(self):
        replayable = mtls_interceptor._ReplayableIterator(x for x in [b"a", b"b"])
        first = iter(replayable)
        assert next(first) == b"a"

        second = iter(replayable)
        assert list(second) == [b"a", b"b"]
        assert replayable.can_replay()

    def test_stale_reader_stops(self):
        replayable = mtls_interceptor._ReplayableIterator([b"a", b"b"])
        first = iter(replayable)
        iter(replayable)  # A newer reader takes over.
        with pytest.raises(StopIteration):
            next(first)

    def test_disables_replay_after_max_items(self):
        replayable = mtls_interceptor._ReplayableIterator(range(5), max_items=2)
        assert list(iter(replayable)) == [0, 1, 2, 3, 4]
        assert replayable.can_replay() is False


# ---------------------------------------------------------------------------
# _DeadlineExceededError
# ---------------------------------------------------------------------------


def test_deadline_exceeded_error_implements_call():
    error = mtls_interceptor._DeadlineExceededError("too late")
    assert isinstance(error, grpc.RpcError)
    assert isinstance(error, grpc.Call)
    assert error.code() == grpc.StatusCode.DEADLINE_EXCEEDED
    assert error.details() == "too late"


# ---------------------------------------------------------------------------
# _RetryableUnaryResponseFuture
# ---------------------------------------------------------------------------


class TestRetryableUnaryResponseFuture(object):
    def test_success_with_already_completed_call(self):
        # Regression: status_code was unbound on success, raising UnboundLocalError
        # out of intercept_unary_unary on grpc's blocking call path.
        interceptor, wrapper = make_interceptor()
        callback = mock.Mock()

        future = interceptor.intercept_unary_unary(
            lambda details, request: CompletedFuture(result="response"),
            call_details(),
            "request",
        )
        future.add_done_callback(callback)

        assert future.result(timeout=1) == "response"
        assert future.exception(timeout=1) is None
        assert future.code() == grpc.StatusCode.OK
        callback.assert_called_once_with(future)
        wrapper.refresh_logic.assert_not_called()

    def test_non_rpc_error_is_surfaced(self):
        interceptor, wrapper = make_interceptor()
        error = ValueError("boom")

        future = interceptor.intercept_unary_unary(
            lambda details, request: CompletedFuture(exception=error),
            call_details(),
            "request",
        )

        with pytest.raises(ValueError):
            future.result(timeout=1)
        assert future.exception(timeout=1) is error
        wrapper.refresh_logic.assert_not_called()

    def test_cancelled_call_completes_and_fires_callbacks(self):
        interceptor, _ = make_interceptor()
        inner = CompletedFuture(cancelled=True)
        calls = []
        future = mtls_interceptor._RetryableUnaryResponseFuture.__new__(
            mtls_interceptor._RetryableUnaryResponseFuture
        )
        # Build normally, but with a call whose callback we trigger manually.
        pending = mock.Mock()
        future = mtls_interceptor._RetryableUnaryResponseFuture(
            lambda details, request: pending, call_details(), "request", interceptor
        )
        future.add_done_callback(calls.append)
        future.add_done_callback(mock.Mock(side_effect=RuntimeError("ignored")))
        future._call = inner

        future._on_inner_future_done(inner)

        assert future._completion_event.is_set()
        assert calls == [future]

    def test_callback_for_stale_call_is_ignored(self):
        interceptor, _ = make_interceptor()
        pending = mock.Mock()
        future = mtls_interceptor._RetryableUnaryResponseFuture(
            lambda details, request: pending, call_details(), "request", interceptor
        )

        future._on_inner_future_done(CompletedFuture(result="stale"))

        assert not future._completion_event.is_set()

    def test_retries_after_cert_rotation(self):
        interceptor, wrapper = make_interceptor()
        continuation = mock.Mock(
            side_effect=[
                CompletedFuture(exception=unauthenticated()),
                CompletedFuture(result="response"),
            ]
        )

        with mock.patch(CHECK_PARAMS) as check:
            check.return_value = (b"new-cert", b"new-key", "fp1", "fp2")
            future = interceptor.intercept_unary_unary(
                continuation, call_details(), "request"
            )

        assert future.result(timeout=1) == "response"
        assert continuation.call_count == 2
        assert future._retry_count == 1
        # The cert material from the fingerprint check is reused, not re-fetched.
        wrapper.refresh_logic.assert_called_once_with(1, b"new-cert", b"new-key")
        check.assert_called_once()

    def test_no_retry_when_cert_unchanged(self):
        interceptor, wrapper = make_interceptor()
        error = unauthenticated()
        continuation = mock.Mock(return_value=CompletedFuture(exception=error))

        with mock.patch(CHECK_PARAMS) as check:
            check.return_value = (b"old-cert", b"key", "fp1", "fp1")
            future = interceptor.intercept_unary_unary(
                continuation, call_details(), "request"
            )

        with pytest.raises(FakeRpcError):
            future.result(timeout=1)
        assert future.code() == grpc.StatusCode.UNAUTHENTICATED
        assert continuation.call_count == 1
        wrapper.refresh_logic.assert_not_called()

    def test_stops_after_max_retries(self):
        interceptor, wrapper = make_interceptor()
        continuation = mock.Mock(
            side_effect=lambda details, request: CompletedFuture(
                exception=unauthenticated()
            )
        )

        with mock.patch(SHOULD_RETRY, autospec=True) as should_retry:
            should_retry.side_effect = lambda self, code, count, cert: (
                (count < 2, b"c", b"k")
            )
            future = interceptor.intercept_unary_unary(
                continuation, call_details(), "request"
            )

        with pytest.raises(FakeRpcError):
            future.result(timeout=1)
        assert continuation.call_count == 3

    def test_refresh_failure_becomes_terminal_exception(self):
        interceptor, wrapper = make_interceptor()
        wrapper.refresh_logic.side_effect = RuntimeError("refresh failed")

        with mock.patch(SHOULD_RETRY) as should_retry:
            should_retry.return_value = (True, b"c", b"k")
            future = interceptor.intercept_unary_unary(
                lambda details, request: CompletedFuture(exception=unauthenticated()),
                call_details(),
                "request",
            )

        assert future._completion_event.is_set()
        with pytest.raises(RuntimeError, match="refresh failed"):
            future.result(timeout=1)
        assert isinstance(future.exception(timeout=1), RuntimeError)
        assert future.initial_metadata() is None
        assert future.trailing_metadata() is None

    def test_deadline_exceeded_during_retry(self):
        interceptor, wrapper = make_interceptor()
        continuation = mock.Mock(
            return_value=CompletedFuture(exception=unauthenticated())
        )

        with (
            mock.patch(SHOULD_RETRY) as should_retry,
            mock.patch.object(
                mtls_interceptor.time, "monotonic", side_effect=[1000.0, 1000.0, 2000.0]
            ),
        ):
            should_retry.side_effect = [
                (True, b"c", b"k"),
                (False, None, None),
            ]
            future = interceptor.intercept_unary_unary(
                continuation, call_details(timeout=5.0), "request"
            )

        with pytest.raises(mtls_interceptor._DeadlineExceededError):
            future.result(timeout=1)
        assert future.code() == grpc.StatusCode.DEADLINE_EXCEEDED
        assert future.details() == "Deadline Exceeded during retry resolution."
        assert continuation.call_count == 1

    def test_retry_uses_remaining_timeout(self):
        interceptor, _ = make_interceptor()
        continuation = mock.Mock(
            side_effect=[
                CompletedFuture(exception=unauthenticated()),
                CompletedFuture(result="response"),
            ]
        )

        with (
            mock.patch(SHOULD_RETRY) as should_retry,
            mock.patch.object(
                mtls_interceptor.time, "monotonic", side_effect=[1000.0, 1000.0, 1002.0]
            ),
        ):
            should_retry.return_value = (True, b"c", b"k")
            future = interceptor.intercept_unary_unary(
                continuation, call_details(timeout=5.0), "request"
            )

        assert future.result(timeout=1) == "response"
        retry_details = continuation.call_args_list[1][0][0]
        assert retry_details.timeout == pytest.approx(3.0)

    def test_client_stream_is_replayed_on_retry(self):
        interceptor, _ = make_interceptor()
        seen = []

        def continuation(details, request_iterator):
            seen.append(list(request_iterator))
            if len(seen) == 1:
                return CompletedFuture(exception=unauthenticated())
            return CompletedFuture(result="response")

        with mock.patch(SHOULD_RETRY) as should_retry:
            should_retry.return_value = (True, b"c", b"k")
            future = interceptor.intercept_stream_unary(
                continuation, call_details(), iter([b"a", b"b"])
            )

        assert future.result(timeout=1) == "response"
        assert seen == [[b"a", b"b"], [b"a", b"b"]]

    def test_client_stream_not_retried_when_replay_disabled(self):
        interceptor, wrapper = make_interceptor()
        continuation = mock.Mock(
            return_value=CompletedFuture(exception=unauthenticated())
        )

        with (
            mock.patch.object(
                mtls_interceptor._ReplayableIterator, "can_replay", return_value=False
            ),
            mock.patch(SHOULD_RETRY) as should_retry,
        ):
            should_retry.return_value = (True, b"c", b"k")
            future = interceptor.intercept_stream_unary(
                continuation, call_details(), iter([b"a"])
            )

        with pytest.raises(FakeRpcError):
            future.result(timeout=1)
        assert continuation.call_count == 1

    def test_request_factory_is_called_per_attempt(self):
        interceptor, _ = make_interceptor()
        factory = mock.Mock(side_effect=lambda: iter([b"a"]))
        continuation = mock.Mock(
            side_effect=[
                CompletedFuture(exception=unauthenticated()),
                CompletedFuture(result="response"),
            ]
        )

        with mock.patch(SHOULD_RETRY) as should_retry:
            should_retry.return_value = (True, b"c", b"k")
            future = interceptor.intercept_stream_unary(
                continuation, call_details(), factory
            )

        assert future._uses_factory is True
        assert future.result(timeout=1) == "response"
        assert factory.call_count == 2

    def test_without_wrapper_does_not_retry(self):
        interceptor = mtls_interceptor.CertRotationInterceptor()
        future = interceptor.intercept_unary_unary(
            lambda details, request: CompletedFuture(exception=unauthenticated()),
            call_details(),
            "request",
        )

        assert future._attempt_cert is None
        with pytest.raises(FakeRpcError):
            future.result(timeout=1)

    def test_result_times_out_while_pending(self):
        interceptor, _ = make_interceptor()
        future = interceptor.intercept_unary_unary(
            lambda details, request: mock.Mock(), call_details(), "request"
        )
        with pytest.raises(grpc.FutureTimeoutError):
            future.result(timeout=0.01)
        with pytest.raises(grpc.FutureTimeoutError):
            future.exception(timeout=0.01)
        with pytest.raises(grpc.FutureTimeoutError):
            future.traceback(timeout=0.01)

    def test_add_done_callback_after_completion_fires_immediately(self):
        interceptor, _ = make_interceptor()
        future = interceptor.intercept_unary_unary(
            lambda details, request: CompletedFuture(result="response"),
            call_details(),
            "request",
        )
        callback = mock.Mock()
        future.add_done_callback(callback)
        callback.assert_called_once_with(future)
        # Errors raised by late callbacks are swallowed.
        future.add_done_callback(mock.Mock(side_effect=RuntimeError("ignored")))

    def test_call_methods_delegate_to_current_call(self):
        interceptor, _ = make_interceptor()
        future = interceptor.intercept_unary_unary(
            lambda details, request: CompletedFuture(result="response"),
            call_details(),
            "request",
        )
        assert future.initial_metadata() == ("initial", "md")
        assert future.trailing_metadata() == ("trailing", "md")
        assert future.details() == "details"
        assert future.traceback(timeout=1) is None


# ---------------------------------------------------------------------------
# _RetryableStreamResponseIterator
# ---------------------------------------------------------------------------


class TestRetryableStreamResponseIterator(object):
    def test_yields_responses_and_fires_callbacks_once(self):
        interceptor, _ = make_interceptor()
        inner = FakeStreamCall([b"r1", b"r2"])
        stream = interceptor.intercept_unary_stream(
            lambda details, request: inner, call_details(), "request"
        )
        callback = mock.Mock()
        stream.add_done_callback(callback)

        assert list(stream) == [b"r1", b"r2"]
        inner.fire_done()

        callback.assert_called_once_with(stream)
        # Late callbacks fire immediately.
        late = mock.Mock()
        stream.add_done_callback(late)
        late.assert_called_once_with(stream)

    def test_retries_unauthenticated_before_first_response(self):
        interceptor, wrapper = make_interceptor()
        first = FakeStreamCall(
            [unauthenticated()], code=grpc.StatusCode.UNAUTHENTICATED
        )
        second = FakeStreamCall([b"r1"])
        continuation = mock.Mock(side_effect=[first, second])

        with mock.patch(CHECK_PARAMS) as check:
            check.return_value = (b"new-cert", b"new-key", "fp1", "fp2")
            stream = interceptor.intercept_unary_stream(
                continuation, call_details(), "request"
            )
            assert list(stream) == [b"r1"]

        assert continuation.call_count == 2
        wrapper.refresh_logic.assert_called_once_with(1, b"new-cert", b"new-key")

    def test_unauthenticated_done_callback_is_suppressed(self):
        # A 401 on the first attempt must not complete the outer stream while a
        # retry may still follow.
        interceptor, _ = make_interceptor()
        first = FakeStreamCall(
            [unauthenticated()], code=grpc.StatusCode.UNAUTHENTICATED
        )
        stream = interceptor.intercept_unary_stream(
            lambda details, request: first, call_details(), "request"
        )
        callback = mock.Mock()
        stream.add_done_callback(callback)

        first.fire_done()

        callback.assert_not_called()
        assert stream._is_completed is False

    def test_non_unauthenticated_done_callback_fires(self):
        interceptor, _ = make_interceptor()
        inner = FakeStreamCall([], code=grpc.StatusCode.INTERNAL)
        stream = interceptor.intercept_unary_stream(
            lambda details, request: inner, call_details(), "request"
        )
        callback = mock.Mock()
        stream.add_done_callback(callback)

        inner.fire_done()

        callback.assert_called_once_with(stream)

    def test_no_retry_after_a_response_was_yielded(self):
        interceptor, wrapper = make_interceptor()
        error = unauthenticated()
        inner = FakeStreamCall([b"r1", error])
        continuation = mock.Mock(return_value=inner)

        with mock.patch(SHOULD_RETRY) as should_retry:
            should_retry.return_value = (True, b"c", b"k")
            stream = interceptor.intercept_unary_stream(
                continuation, call_details(), "request"
            )
            assert next(stream) == b"r1"
            with pytest.raises(FakeRpcError):
                next(stream)

        assert continuation.call_count == 1

    def test_terminal_error_fires_callbacks_and_raises(self):
        interceptor, wrapper = make_interceptor()
        error = FakeRpcError(grpc.StatusCode.INTERNAL)
        stream = interceptor.intercept_unary_stream(
            lambda details, request: FakeStreamCall([error]),
            call_details(),
            "request",
        )
        callback = mock.Mock()
        stream.add_done_callback(callback)

        with pytest.raises(FakeRpcError):
            next(stream)

        callback.assert_called_once_with(stream)
        wrapper.refresh_logic.assert_not_called()

    def test_refresh_failure_is_raised(self):
        interceptor, wrapper = make_interceptor()
        wrapper.refresh_logic.side_effect = RuntimeError("refresh failed")

        with mock.patch(SHOULD_RETRY) as should_retry:
            should_retry.return_value = (True, b"c", b"k")
            stream = interceptor.intercept_unary_stream(
                lambda details, request: FakeStreamCall([unauthenticated()]),
                call_details(),
                "request",
            )
            callback = mock.Mock()
            stream.add_done_callback(callback)
            with pytest.raises(RuntimeError, match="refresh failed"):
                next(stream)

        callback.assert_called_once_with(stream)

    def test_deadline_exceeded_during_retry(self):
        interceptor, _ = make_interceptor()
        continuation = mock.Mock(return_value=FakeStreamCall([unauthenticated()]))

        with (
            mock.patch(SHOULD_RETRY) as should_retry,
            mock.patch.object(
                mtls_interceptor.time, "monotonic", side_effect=[1000.0, 1000.0, 2000.0]
            ),
        ):
            should_retry.return_value = (True, b"c", b"k")
            stream = interceptor.intercept_unary_stream(
                continuation, call_details(timeout=5.0), "request"
            )
            with pytest.raises(mtls_interceptor._DeadlineExceededError) as excinfo:
                next(stream)

        assert excinfo.value.code() == grpc.StatusCode.DEADLINE_EXCEEDED

    def test_bidi_stream_replays_requests(self):
        interceptor, _ = make_interceptor()
        seen = []

        def continuation(details, request_iterator):
            seen.append(list(request_iterator))
            if len(seen) == 1:
                return FakeStreamCall([unauthenticated()])
            return FakeStreamCall([b"r1"])

        with mock.patch(SHOULD_RETRY) as should_retry:
            should_retry.return_value = (True, b"c", b"k")
            stream = interceptor.intercept_stream_stream(
                continuation, call_details(), iter([b"a", b"b"])
            )
            assert list(stream) == [b"r1"]

        assert seen == [[b"a", b"b"], [b"a", b"b"]]

    def test_request_factory_is_called_per_attempt(self):
        interceptor, _ = make_interceptor()
        factory = mock.Mock(side_effect=lambda: iter([b"a"]))
        continuation = mock.Mock(
            side_effect=[FakeStreamCall([unauthenticated()]), FakeStreamCall([b"r1"])]
        )

        with mock.patch(SHOULD_RETRY) as should_retry:
            should_retry.return_value = (True, b"c", b"k")
            stream = interceptor.intercept_stream_stream(
                continuation, call_details(), factory
            )
            assert list(stream) == [b"r1"]

        assert stream._uses_factory is True
        assert factory.call_count == 2


# ---------------------------------------------------------------------------
# _BaseCallWrapper
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "method, args",
    [
        ("cancel", ()),
        ("cancelled", ()),
        ("running", ()),
        ("done", ()),
        ("initial_metadata", ()),
        ("trailing_metadata", ()),
        ("code", ()),
        ("details", ()),
        ("time_remaining", ()),
        ("add_callback", (mock.sentinel.callback,)),
        ("add_done_callback", (mock.sentinel.callback,)),
    ],
)
def test_base_call_wrapper_delegates(method, args):
    wrapper = mtls_interceptor._BaseCallWrapper()
    wrapper._call = mock.Mock()
    result = getattr(wrapper, method)(*args)
    getattr(wrapper._call, method).assert_called_once_with(*args)
    if method not in ("add_callback", "add_done_callback"):
        assert result is getattr(wrapper._call, method).return_value


@pytest.mark.parametrize("method", ["result", "exception", "traceback"])
def test_base_call_wrapper_delegates_with_timeout(method):
    wrapper = mtls_interceptor._BaseCallWrapper()
    wrapper._call = mock.Mock()
    assert (
        getattr(wrapper, method)(timeout=3)
        is getattr(wrapper._call, method).return_value
    )
    getattr(wrapper._call, method).assert_called_once_with(timeout=3)


# ---------------------------------------------------------------------------
# End to end through grpc.intercept_channel
# ---------------------------------------------------------------------------


class _FakeUnaryMultiCallable(object):
    def __init__(self, outcome):
        self._outcome = outcome
        self.calls = 0

    def with_call(self, request, **kwargs):
        self.calls += 1
        if isinstance(self._outcome, BaseException):
            raise self._outcome
        return self._outcome, CompletedFuture(result=self._outcome)


class _FakeChannel(object):
    def __init__(self, outcome):
        self.multicallable = _FakeUnaryMultiCallable(outcome)

    def unary_unary(self, method, *args, **kwargs):
        return self.multicallable


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
def test_blocking_call_recovers_from_cert_rotation(ssl_channel_credentials):
    old_channel = _FakeChannel(unauthenticated())
    new_channel = _FakeChannel("response")
    create_channel_fn = mock.Mock(return_value=new_channel)
    refreshing = mtls_interceptor.MTLSRefreshingChannel(
        "example.com:443", create_channel_fn, old_channel, b"old-cert"
    )
    channel = grpc.intercept_channel(
        refreshing, mtls_interceptor.CertRotationInterceptor(wrapper=refreshing)
    )

    with mock.patch(CHECK_PARAMS) as check:
        check.return_value = (b"new-cert", b"new-key", "fp1", "fp2")
        response = channel.unary_unary("/svc/Method")(b"request")

    assert response == "response"
    assert old_channel.multicallable.calls == 1
    assert new_channel.multicallable.calls == 1
    assert refreshing._cached_cert == b"new-cert"
    create_channel_fn.assert_called_once_with(
        ssl_credentials=ssl_channel_credentials.return_value,
        client_cert_callback=None,
    )


def test_blocking_call_success_without_rotation():
    old_channel = _FakeChannel("response")
    refreshing = mtls_interceptor.MTLSRefreshingChannel(
        "example.com:443", mock.Mock(), old_channel, b"old-cert"
    )
    channel = grpc.intercept_channel(
        refreshing, mtls_interceptor.CertRotationInterceptor(wrapper=refreshing)
    )

    with mock.patch(CHECK_PARAMS) as check:
        assert channel.unary_unary("/svc/Method")(b"request") == "response"

    check.assert_not_called()
