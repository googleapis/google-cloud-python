"""mTLS Interceptor and Channel Wrapper for certificate rotation."""

import collections
import threading
import time

import grpc
from google.auth import transport

_ClientCallDetails = collections.namedtuple(
    "_ClientCallDetails",
    ("method", "timeout", "metadata", "credentials", "wait_for_ready"),
)

class _DeadlineExceededError(grpc.RpcError, grpc.Call):
    def __init__(self, details):
        super().__init__()
        self._details = details

    def code(self):
        return grpc.StatusCode.DEADLINE_EXCEEDED

    def details(self):
        return self._details


class _BaseCallWrapper(grpc.Future, grpc.Call):
    """A generic wrapper that delegates standard grpc.Call and grpc.Future 
    methods to an underlying call object.
    """
    
    def cancel(self):
        return self._call.cancel()

    def cancelled(self):
        return self._call.cancelled()

    def running(self):
        return self._call.running()

    def done(self):
        return self._call.done()

    def result(self, timeout=None):
        return self._call.result(timeout=timeout)

    def exception(self, timeout=None):
        return self._call.exception(timeout=timeout)

    def traceback(self, timeout=None):
        return self._call.traceback(timeout=timeout)

    def add_done_callback(self, fn):
        self._call.add_done_callback(fn)

    def initial_metadata(self):
        return self._call.initial_metadata()

    def trailing_metadata(self):
        return self._call.trailing_metadata()

    def code(self):
        return self._call.code()

    def details(self):
        return self._call.details()


class _RetryableUnaryResponseFuture(_BaseCallWrapper):
    def __init__(self, continuation, client_call_details, request_or_iterator, interceptor):
        self._continuation = continuation
        self._client_call_details = client_call_details
        self._request_or_iterator = request_or_iterator
        self._interceptor = interceptor
        self._retry_count = 0
        self._call = None
        self._lock = threading.RLock()
        
        timeout = getattr(self._client_call_details, "timeout", None)
        if timeout:
            self._initial_timeout = timeout
            self._start_time = time.monotonic()
        else:
            self._initial_timeout = None
            self._start_time = None

        self._terminal_exception = None
        self._callbacks = []
        self._is_completed = False
        self._start_call()

    def _start_call(self):
        with self._lock:
            payload = self._request_or_iterator
            call_details = self._client_call_details
            if callable(payload) and hasattr(payload, "can_replay"):
                if not payload.can_replay():
                    call_details = _ClientCallDetails(
                        method=call_details.method,
                        timeout=call_details.timeout,
                        metadata=call_details.metadata,
                        credentials=call_details.credentials,
                        wait_for_ready=call_details.wait_for_ready,
                    )
            
            if self._initial_timeout:
                elapsed = time.monotonic() - self._start_time
                remaining = self._initial_timeout - elapsed
                if remaining <= 0:
                    raise _DeadlineExceededError(
                        "Deadline Exceeded during retry resolution."
                    )
                call_details = _ClientCallDetails(
                    method=call_details.method,
                    timeout=remaining,
                    metadata=call_details.metadata,
                    credentials=call_details.credentials,
                    wait_for_ready=call_details.wait_for_ready,
                )

            self._call = self._continuation(call_details, payload)
            self._call.add_done_callback(self._on_inner_future_done)

    def _on_inner_future_done(self, inner_future):
        with self._lock:
            if self._call is not inner_future:
                return
        if inner_future.cancelled():
            self._resolve_completion()
            return
            
        status_code = inner_future.code()
        
        if self._interceptor._wrapper:
            (
                chk_should_retry,
                chk_cert,
                chk_key,
                chk_pwd,
            ) = self._interceptor._should_retry(
                status_code, 0, self._interceptor._wrapper._cached_cert
            )
            
            if chk_should_retry:
                payload = self._request_or_iterator
                can_replay = True
                if callable(payload) and hasattr(payload, "can_replay"):
                    can_replay = payload.can_replay()

                if can_replay:
                    try:
                        self._interceptor._wrapper.refresh_logic(
                            1, chk_cert, chk_key, chk_pwd
                        )
                    except Exception as e:
                        with self._lock:
                            self._terminal_exception = e
                    if self._terminal_exception is None:
                        self._retry_count += 1
                        self._start_call()
                        return
                        
        self._resolve_completion()

    def _resolve_completion(self):
        callbacks = []
        with self._lock:
            self._is_completed = True
            callbacks = self._callbacks[:]
        for cb in callbacks:
            try:
                cb(self)
            except Exception:
                pass


class _RetryableStreamResponseIterator(_BaseCallWrapper):
    def __init__(self, continuation, client_call_details, request_or_iterator, interceptor):
        self._continuation = continuation
        self._client_call_details = client_call_details
        self._request_or_iterator = (
            _ReplayableIterator(request_or_iterator)
            if hasattr(request_or_iterator, "__iter__")
            else request_or_iterator
        )
        self._call = None
        self._retry_count = 0
        self._yielded_any_response = False
        self._lock = threading.RLock()
        self._interceptor = interceptor
        self._start_call()

    def _start_call(self):
        with self._lock:
            if isinstance(self._request_or_iterator, _ReplayableIterator):
                payload = self._request_or_iterator.reader()
            else:
                payload = self._request_or_iterator
            self._call = self._continuation(self._client_call_details, payload)

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            try:
                response = next(self._call)
                self._yielded_any_response = True
                return response
            except grpc.RpcError as rpc_error:
                status_code = rpc_error.code()
                can_replay_request = True
                if isinstance(self._request_or_iterator, _ReplayableIterator):
                    can_replay_request = self._request_or_iterator.can_replay()
                    
                if not self._yielded_any_response and can_replay_request:
                    if self._interceptor._wrapper:
                        (
                            chk_should_retry,
                            chk_cert,
                            chk_key,
                            chk_pwd,
                        ) = self._interceptor._should_retry(
                            status_code, 0, self._interceptor._wrapper._cached_cert
                        )
                        if chk_should_retry:
                            try:
                                self._interceptor._wrapper.refresh_logic(
                                    1, chk_cert, chk_key, chk_pwd
                                )
                            except Exception as e:
                                raise e
                            self._retry_count += 1
                            self._start_call()
                            continue
                raise rpc_error

    def next(self):
        return self.__next__()


class _ReplayableIterator(object):
    def __init__(self, target_iterator, max_items=1000):
        self._target_iterator = iter(target_iterator)
        self._max_items = max_items
        self._buffer = []
        self._exhausted = False
        self._can_replay = True
        self._lock = threading.Lock()

    def _get_item(self, index):
        with self._lock:
            if not self._can_replay:
                raise RuntimeError("Iterator replay capability lost")

            while index >= len(self._buffer) and not self._exhausted:
                try:
                    item = next(self._target_iterator)
                    if len(self._buffer) >= self._max_items:
                        self._can_replay = False
                        self._buffer = None
                        raise RuntimeError(
                            f"More than {self._max_items} items in replay buffer."
                        )
                    self._buffer.append(item)
                except StopIteration:
                    self._exhausted = True

            if index < len(self._buffer):
                return self._buffer[index]
            raise StopIteration()

    def reader(self):
        return _ReplayableIteratorReader(self)

    def can_replay(self):
        with self._lock:
            return self._can_replay


class _ReplayableIteratorReader(object):
    def __init__(self, parent):
        self._parent = parent
        self._read_index = 0

    def __next__(self):
        item = self._parent._get_item(self._read_index)
        self._read_index += 1
        return item

    def next(self):
        return self.__next__()


class CertRotationInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):
    """A gRPC client interceptor that provides automatic retry logic for mTLS certificate rotation."""
    
    def __init__(self, wrapper=None):
        self._wrapper = wrapper
        self._max_retries = transport.DEFAULT_MAX_REFRESH_ATTEMPTS

    def _should_retry(self, code, retry_count, attempt_cert):
        do_refresh = False
        new_cert, new_key, passphrase = None, None, None

        if retry_count < self._max_retries and code == grpc.StatusCode.UNAUTHENTICATED:
            (
                new_cert,
                new_key,
                passphrase,
            ) = self._wrapper.get_cert()
            
            if new_cert and new_cert != attempt_cert:
                do_refresh = True

        return do_refresh, new_cert, new_key, passphrase

    def intercept_unary_unary(self, continuation, client_call_details, request):
        return _RetryableUnaryResponseFuture(
            continuation, client_call_details, request, self
        )

    def intercept_unary_stream(self, continuation, client_call_details, request):
        return _RetryableStreamResponseIterator(
            continuation, client_call_details, request, self
        )

    def intercept_stream_unary(self, continuation, client_call_details, request_iterator):
        return _RetryableUnaryResponseFuture(
            continuation, client_call_details, request_iterator, self
        )

    def intercept_stream_stream(self, continuation, client_call_details, request_iterator):
        return _RetryableStreamResponseIterator(
            continuation, client_call_details, request_iterator, self
        )


class MTLSRefreshingChannel(grpc.Channel):
    def __init__(self, target, create_channel_fn, initial_channel, initial_cert):
        self._target = target
        self._create_channel_fn = create_channel_fn
        self._channel = initial_channel
        self._cached_cert = initial_cert
        self._lock = threading.Lock()
        self._subscribers = []
        self._cert_factory = transport.grpc._get_client_ssl_credentials_auto_enablement

    def get_cert(self):
        creds = self._cert_factory()
        return creds.certificate_chain, creds.private_key, None

    def refresh_logic(self, expected_retry_count, call_cert_bytes, call_key_bytes, passphrase):
        with self._lock:
            # Another thread may have already completed the refresh
            if self._cached_cert != call_cert_bytes:
                return

            new_ssl_credentials = grpc.ssl_channel_credentials(
                certificate_chain=call_cert_bytes,
                private_key=call_key_bytes,
            )

            self._channel = self._create_channel_fn(
                ssl_credentials=new_ssl_credentials,
                client_cert_callback=None
            )

            self._cached_cert = call_cert_bytes
            for callback in self._subscribers:
                callback(grpc.ChannelConnectivity.IDLE)
            
    def subscribe(self, callback, try_to_connect=False):
        with self._lock:
            self._subscribers.append(callback)
            return self._channel.subscribe(callback, try_to_connect=try_to_connect)

    def unsubscribe(self, callback):
        with self._lock:
            if callback in self._subscribers:
                self._subscribers.remove(callback)
            return self._channel.unsubscribe(callback)

    def unary_unary(self, method, *args, **kwargs):
        return lambda request, **req_kwargs: self._channel.unary_unary(
            method, *args, **kwargs
        )(request, **req_kwargs)

    def unary_stream(self, method, *args, **kwargs):
        return lambda request, **req_kwargs: self._channel.unary_stream(
            method, *args, **kwargs
        )(request, **req_kwargs)

    def stream_unary(self, method, *args, **kwargs):
        return lambda request_iterator, **req_kwargs: self._channel.stream_unary(
            method, *args, **kwargs
        )(request_iterator, **req_kwargs)

    def stream_stream(self, method, *args, **kwargs):
        return lambda request_iterator, **req_kwargs: self._channel.stream_stream(
            method, *args, **kwargs
        )(request_iterator, **req_kwargs)

    def close(self):
        self._channel.close()
