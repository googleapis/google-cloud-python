# Copyright 2016 Google LLC
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

"""Authorization support for gRPC."""

from __future__ import absolute_import

import collections
import functools
import logging
import threading
import time
import warnings


from google.auth import exceptions
from google.auth import transport
from google.auth.transport import _mtls_helper
from google.auth.transport import mtls
from google.oauth2 import service_account

from typing import Optional


try:
    import grpc  # type: ignore
except ImportError as caught_exc:  # pragma: NO COVER
    raise ImportError(
        "gRPC is not installed from please install the grpcio package to use the gRPC transport."
    ) from caught_exc


_grpc_ver_str = getattr(grpc, "__version__", None)
if isinstance(_grpc_ver_str, str):
    _parts = []
    for _part in _grpc_ver_str.split("."):
        try:
            _parts.append(int(_part))
        except ValueError:
            break
    if _parts and tuple(_parts) < (1, 83, 0):
        warnings.warn(
            "grpcio < 1.83.0 does not support Post-Quantum Cryptography (PQC). "
            "Support for non-PQC environments is deprecated. In October 2026, "
            "google-auth will raise its minimum requirements "
            "to enforce grpcio >= 1.83.0. "
            "For more details on Google Cloud's post-quantum security migration, visit: "
            "https://cloud.google.com/security/resources/post-quantum-cryptography",
            FutureWarning,
        )

_LOGGER = logging.getLogger(__name__)


class AuthMetadataPlugin(grpc.AuthMetadataPlugin):
    """A `gRPC AuthMetadataPlugin`_ that inserts the credentials into each
    request.

    .. _gRPC AuthMetadataPlugin:
        http://www.grpc.io/grpc/python/grpc.html#grpc.AuthMetadataPlugin

    Args:
        credentials (google.auth.credentials.Credentials): The credentials to
            add to requests.
        request (google.auth.transport.Request): A HTTP transport request
            object used to refresh credentials as needed.
        default_host (Optional[str]): A host like "pubsub.googleapis.com".
            This is used when a self-signed JWT is created from service
            account credentials.
        suppress_metrics_header (bool): When enabled, ``x-goog-api-client``
            will be stripped from authorization headers.
    """

    def __init__(
        self, credentials, request, default_host=None, *, suppress_metrics_header=False
    ):
        # pylint: disable=no-value-for-parameter
        # pylint doesn't realize that the super method takes no arguments
        # because this class is the same name as the superclass.
        super(AuthMetadataPlugin, self).__init__()
        self._credentials = credentials
        self._request = request
        self._default_host = default_host
        self._suppress_metrics_header = suppress_metrics_header

    def _get_authorization_headers(self, context):
        """Gets the authorization headers for a request.

        Returns:
            Sequence[Tuple[str, str]]: A list of request headers (key, value)
                to add to the request.
        """
        headers = {}

        # https://google.aip.dev/auth/4111
        # Attempt to use self-signed JWTs when a service account is used.
        # A default host must be explicitly provided since it cannot always
        # be determined from the context.service_url.
        if isinstance(self._credentials, service_account.Credentials):
            self._credentials._create_self_signed_jwt(
                "https://{}/".format(self._default_host) if self._default_host else None
            )

        self._credentials.before_request(
            self._request, context.method_name, context.service_url, headers
        )

        if self._suppress_metrics_header and "x-goog-api-client" in headers:
            del headers["x-goog-api-client"]

        return list(headers.items())

    def __call__(self, context, callback):
        """Passes authorization metadata into the given callback.

        Args:
            context (grpc.AuthMetadataContext): The RPC context.
            callback (grpc.AuthMetadataPluginCallback): The callback that will
                be invoked to pass in the authorization metadata.
        """
        callback(self._get_authorization_headers(context), None)


def secure_authorized_channel(
    credentials,
    request,
    target,
    ssl_credentials=None,
    client_cert_callback=None,
    **kwargs
):
    """Creates a secure authorized gRPC channel.

    This creates a channel with SSL and :class:`AuthMetadataPlugin`. This
    channel can be used to create a stub that can make authorized requests.
    Users can configure client certificate or rely on device certificates to
    establish a mutual TLS channel, if the `GOOGLE_API_USE_CLIENT_CERTIFICATE`
    variable is explicitly set to `true`.

    Example::

        import google.auth
        import google.auth.transport.grpc
        import google.auth.transport.requests
        from google.cloud.speech.v1 import cloud_speech_pb2

        # Get credentials.
        credentials, _ = google.auth.default()

        # Get an HTTP request function to refresh credentials.
        request = google.auth.transport.requests.Request()

        # Create a channel.
        channel = google.auth.transport.grpc.secure_authorized_channel(
            credentials, regular_endpoint, request,
            ssl_credentials=grpc.ssl_channel_credentials())

        # Use the channel to create a stub.
        cloud_speech.create_Speech_stub(channel)

    Usage:

    There are actually a couple of options to create a channel, depending on if
    you want to create a regular or mutual TLS channel.

    First let's list the endpoints (regular vs mutual TLS) to choose from::

        regular_endpoint = 'speech.googleapis.com:443'
        mtls_endpoint = 'speech.mtls.googleapis.com:443'

    Option 1: create a regular (non-mutual) TLS channel by explicitly setting
    the ssl_credentials::

        regular_ssl_credentials = grpc.ssl_channel_credentials()

        channel = google.auth.transport.grpc.secure_authorized_channel(
            credentials, request, regular_endpoint,
            ssl_credentials=regular_ssl_credentials)

    Option 2: create a mutual TLS channel by calling a callback which returns
    the client side certificate and the key (Note that
    `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable must be explicitly
    set to `true`)::

        def my_client_cert_callback():
            code_to_load_client_cert_and_key()
            if loaded:
                return (pem_cert_bytes, pem_key_bytes)
            raise MyClientCertFailureException()

        try:
            channel = google.auth.transport.grpc.secure_authorized_channel(
                credentials, request, mtls_endpoint,
                client_cert_callback=my_client_cert_callback)
        except MyClientCertFailureException:
            # handle the exception

    Option 3: use application default SSL credentials. It searches and uses
    the command in a context aware metadata file, which is available on devices
    with endpoint verification support (Note that
    `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable must be explicitly
    set to `true`).
    See https://cloud.google.com/endpoint-verification/docs/overview::

        try:
            default_ssl_credentials = SslCredentials()
        except:
            # Exception can be raised if the context aware metadata is malformed.
            # See :class:`SslCredentials` for the possible exceptions.

        # Choose the endpoint based on the SSL credentials type.
        if default_ssl_credentials.is_mtls:
            endpoint_to_use = mtls_endpoint
        else:
            endpoint_to_use = regular_endpoint
        channel = google.auth.transport.grpc.secure_authorized_channel(
            credentials, request, endpoint_to_use,
            ssl_credentials=default_ssl_credentials)

    Option 4: not setting ssl_credentials and client_cert_callback. For devices
    without endpoint verification support or `GOOGLE_API_USE_CLIENT_CERTIFICATE`
    environment variable is not `true`, a regular TLS channel is created;
    otherwise, a mutual TLS channel is created, however, the call should be
    wrapped in a try/except block in case of malformed context aware metadata.

    The following code uses regular_endpoint, it works the same no matter the
    created channle is regular or mutual TLS. Regular endpoint ignores client
    certificate and key::

        channel = google.auth.transport.grpc.secure_authorized_channel(
            credentials, request, regular_endpoint)

    The following code uses mtls_endpoint, if the created channle is regular,
    and API mtls_endpoint is confgured to require client SSL credentials, API
    calls using this channel will be rejected::

        channel = google.auth.transport.grpc.secure_authorized_channel(
            credentials, request, mtls_endpoint)

    Args:
        credentials (google.auth.credentials.Credentials): The credentials to
            add to requests.
        request (google.auth.transport.Request): A HTTP transport request
            object used to refresh credentials as needed. Even though gRPC
            is a separate transport, there's no way to refresh the credentials
            without using a standard http transport.
        target (str): The host and port of the service.
        ssl_credentials (grpc.ChannelCredentials): Optional SSL channel
            credentials. This can be used to specify different certificates.
            This argument is mutually exclusive with client_cert_callback;
            providing both will raise an exception.
            If ssl_credentials and client_cert_callback are None, application
            default SSL credentials are used if `GOOGLE_API_USE_CLIENT_CERTIFICATE`
            environment variable is explicitly set to `true`, otherwise one way TLS
            SSL credentials are used.
        client_cert_callback (Callable[[], (bytes, bytes)]): Optional
            callback function to obtain client certicate and key for mutual TLS
            connection. This argument is mutually exclusive with
            ssl_credentials; providing both will raise an exception.
            This argument does nothing unless `GOOGLE_API_USE_CLIENT_CERTIFICATE`
            environment variable is explicitly set to `true`.
        kwargs: Additional arguments to pass to :func:`grpc.secure_channel`.

    Returns:
        grpc.Channel: The created gRPC channel.

    Raises:
        google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
            creation failed for any reason.
    """
    # Create the metadata plugin for inserting the authorization header.
    metadata_plugin = AuthMetadataPlugin(credentials, request)

    # Create a set of grpc.CallCredentials using the metadata plugin.
    google_auth_credentials = grpc.metadata_call_credentials(metadata_plugin)

    if ssl_credentials and client_cert_callback:
        raise exceptions.MalformedError(
            "Received both ssl_credentials and client_cert_callback; "
            "these are mutually exclusive."
        )

    # If SSL credentials are not explicitly set, try client_cert_callback and ADC.
    cached_cert: Optional[bytes] = None
    if not ssl_credentials:
        use_client_cert = _mtls_helper.check_use_client_cert()
        if use_client_cert and client_cert_callback:
            # Use the callback if provided.
            cert, key = client_cert_callback()
            ssl_credentials = grpc.ssl_channel_credentials(
                certificate_chain=cert, private_key=key
            )
            cached_cert = cert
        elif use_client_cert:
            # Use application default SSL credentials.
            adc_ssl_credentials = SslCredentials()
            ssl_credentials = adc_ssl_credentials.ssl_credentials
            cached_cert = adc_ssl_credentials._cached_cert
        else:
            ssl_credentials = grpc.ssl_channel_credentials()

    # Combine the ssl credentials and the authorization credentials.
    composite_credentials = grpc.composite_channel_credentials(
        ssl_credentials, google_auth_credentials
    )
    is_recreation = kwargs.pop("_is_recreation", False)
    channel = grpc.secure_channel(target, composite_credentials, **kwargs)
    # Avoid wrapping if mTLS is disabled or if this is a channel recreation call
    if cached_cert and not is_recreation:
        # Package arguments so the channel can be recreated later
        create_channel_fn = functools.partial(
            secure_authorized_channel,
            credentials=credentials,
            request=request,
            target=target,
            _is_recreation=True, # Hidden flag to stop recursion
            **kwargs
        )
        wrapper = MTLSRefreshingChannel(target, create_channel_fn, channel, cached_cert)
        interceptor = CertRotationInterceptor(wrapper=wrapper)
        return grpc.intercept_channel(wrapper, interceptor)
    return channel


class SslCredentials:
    """Class for application default SSL credentials.

    Mutual TLS (mTLS) is enabled if either:

    1. The `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is explicitly
       set to `"true"`.
    2. The `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is unset or empty,
       but a valid workload certificate configuration is found (e.g., via the
       `GOOGLE_API_CERTIFICATE_CONFIG` environment variable or the default gcloud config path).

    See https://google.aip.dev/auth/4114 for client certificate discovery details.

    If client certificate usage is enabled, then for devices with endpoint
    verification support, a device certificate will be automatically loaded and
    mutual TLS will be established.
    See https://cloud.google.com/endpoint-verification/docs/overview.
    """

    def __init__(self):
        use_client_cert = _mtls_helper.check_use_client_cert()
        self._cached_cert = None
        if not use_client_cert:
            self._is_mtls = False
        else:
            self._is_mtls = mtls.has_default_client_cert_source()

    @property
    def ssl_credentials(self):
        """Get the created SSL channel credentials.

        For devices with endpoint verification support, if the device certificate
        loading has any problems, corresponding exceptions will be raised. For
        a device without endpoint verification support, no exceptions will be
        raised.

        Returns:
            grpc.ChannelCredentials: The created grpc channel credentials.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
                creation failed for any reason.
        """
        if self._is_mtls:
            try:
                has_cert, cert, key, _ = _mtls_helper.get_client_ssl_credentials()
                if has_cert:
                    self._ssl_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                    self._cached_cert = cert
                else:
                    self._ssl_credentials = grpc.ssl_channel_credentials()
                    self._is_mtls = False
            except (exceptions.ClientCertError, OSError) as caught_exc:
                new_exc = exceptions.MutualTLSChannelError(caught_exc)
                raise new_exc from caught_exc
        else:
            self._ssl_credentials = grpc.ssl_channel_credentials()

        return self._ssl_credentials

    @property
    def is_mtls(self):
        """Indicates if the created SSL channel credentials is mutual TLS."""
        return self._is_mtls


class CertRotationInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):
    """A gRPC client interceptor that provides automatic retry logic for mTLS certificate rotation.

    This interceptor wraps all gRPC client calls (unary and streaming) with retryable
    futures or iterators. Its primary role is to monitor responses for `UNAUTHENTICATED`
    errors. When an authentication failure occurs, it uses `_should_retry()` to check
    if a new mTLS certificate is available. If a new certificate is found, it signals
    its associated `MTLSRefreshingChannel` wrapper to refresh the underlying gRPC
    channel's credentials and automatically replays the failed RPC.
    """

    def __init__(self, wrapper=None):
        self._wrapper = wrapper
        self._max_retries = transport.DEFAULT_MAX_REFRESH_ATTEMPTS

    def _should_retry(self, code, retry_count, attempt_cert):
        """Determines if the RPC should be retried due to a certificate rotation.

        Returns a tuple: (should_retry, call_cert_bytes, call_key_bytes, passphrase).
        """
        if code != grpc.StatusCode.UNAUTHENTICATED or not self._wrapper:
            return False, None, None, None

        if retry_count >= self._max_retries:
            _LOGGER.debug(
                "Max retries reached (%d/%d) for channel recreation.",
                retry_count,
                self._max_retries,
            )
            return False, None, None, None

        # If another thread already refreshed the channel with an updated cert, retry immediately
        if attempt_cert != self._wrapper._cached_cert:
            return True, None, None, None

        # Check if the certificate on disk or callback has changed since this request was attempted
        (
            call_cert_bytes,
            call_key_bytes,
            passphrase,
            cached_fingerprint,
            current_cert_fingerprint,
        ) = _mtls_helper.check_parameters_for_unauthorized_response(attempt_cert)
        should_retry = cached_fingerprint != current_cert_fingerprint
        return should_retry, call_cert_bytes, call_key_bytes, passphrase

    def intercept_unary_unary(self, continuation, client_call_details, request):
        return _RetryableUnaryResponseFuture(
            continuation, client_call_details, request, self, is_client_stream=False
        )

    def intercept_stream_unary(
        self, continuation, client_call_details, request_iterator
    ):
        return _RetryableUnaryResponseFuture(
            continuation,
            client_call_details,
            request_iterator,
            self,
            is_client_stream=True,
        )

    def intercept_unary_stream(self, continuation, client_call_details, request):
        return _RetryableStreamResponseIterator(
            continuation, client_call_details, request, self, is_client_stream=False
        )

    def intercept_stream_stream(
        self, continuation, client_call_details, request_iterator
    ):
        return _RetryableStreamResponseIterator(
            continuation,
            client_call_details,
            request_iterator,
            self,
            is_client_stream=True,
        )


class MTLSRefreshingChannel(grpc.Channel):
    def __init__(self, target, factory_args, initial_channel, initial_cert):
        self._target = target
        self._create_channel_fn = create_channel_fn
        self._channel = initial_channel
        self._cached_cert = initial_cert
        self._lock = threading.Lock()
        self._subscribers = set()

    def refresh_logic(
        self, count, call_cert_bytes=None, call_key_bytes=None, passphrase=None
    ):
        with self._lock:
            if not call_cert_bytes or self._cached_cert == call_cert_bytes:
                return

            _LOGGER.debug("Wrapper: Refreshing mTLS channel. Retry count: %d", count)
            old_channel = self._channel

            if passphrase is not None:
                call_key_bytes = _mtls_helper.decrypt_private_key(
                    call_key_bytes, passphrase
                )

            # Call the partial, overriding only the cert-related arguments
            new_ssl_credentials = grpc.ssl_channel_credentials(
                certificate_chain=call_cert_bytes,
                private_key=call_key_bytes,
            )

            self._channel = self._create_channel_fn(
                ssl_credentials=new_ssl_credentials,
                client_cert_callback=None
            )


            self._channel = secure_authorized_channel(**factory_args)
            self._cached_cert = call_cert_bytes
            for callback in self._subscribers:
                try:
                    old_channel.unsubscribe(callback)
                except Exception:
                    pass
                self._channel.subscribe(callback)

    def unary_unary(self, method, *args, **kwargs):
        # Always return a callable from the CURRENT channel
        return self._channel.unary_unary(method, *args, **kwargs)

    # Mandatory passthroughs
    def unary_stream(self, method, *args, **kwargs):
        return self._channel.unary_stream(method, *args, **kwargs)

    def stream_unary(self, method, *args, **kwargs):
        return self._channel.stream_unary(method, *args, **kwargs)

    def stream_stream(self, method, *args, **kwargs):
        return self._channel.stream_stream(method, *args, **kwargs)

    def subscribe(self, callback, try_to_connect=False):
        with self._lock:
            self._subscribers.add(callback)
            return self._channel.subscribe(callback, try_to_connect=try_to_connect)

    def unsubscribe(self, callback):
        with self._lock:
            self._subscribers.discard(callback)
            return self._channel.unsubscribe(callback)

    def close(self):
        self._channel.close()


class _ReplayableIterator(object):
    def __init__(self, target_iterator, max_items=1000):
        self._target_iterator = iter(target_iterator)
        self._max_items = max_items
        self._buffer = []
        self._exhausted = False
        self._can_replay = True

        self._lock = threading.Lock()
        self._consumer_lock = threading.Lock()
        self._active_reader = None

    def __iter__(self):
        reader = _ReplayableIteratorReader(self)
        with self._lock:
            self._active_reader = reader
        return reader

    def can_replay(self):
        with self._lock:
            return self._can_replay


class _ReplayableIteratorReader(object):
    def __init__(self, parent):
        self._parent = parent
        self._read_index = 0

    def __next__(self):
        while True:
            with self._parent._lock:
                if self._read_index < len(self._parent._buffer):
                    val = self._parent._buffer[self._read_index]
                    self._read_index += 1
                    return val

                if self._parent._exhausted:
                    raise StopIteration()

                if self._parent._active_reader is not self:
                    raise StopIteration()

            with self._parent._consumer_lock:
                with self._parent._lock:
                    if self._read_index < len(self._parent._buffer):
                        continue
                    if self._parent._active_reader is not self:
                        raise StopIteration()

                try:
                    val = next(self._parent._target_iterator)
                except StopIteration:
                    with self._parent._lock:
                        if self._parent._active_reader is self:
                            self._parent._exhausted = True
                    raise

            with self._parent._lock:
                if self._parent._active_reader is not self:
                    if self._parent._can_replay:
                        self._parent._buffer.append(val)
                    raise StopIteration()

                if self._parent._can_replay:
                    self._parent._buffer.append(val)
                    if len(self._parent._buffer) > self._parent._max_items:
                        self._parent._buffer.clear()
                        self._parent._can_replay = False

                self._read_index += 1
                return val


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


class _RetryableUnaryResponseFuture(_BaseCallWrapper):
    def __init__(
        self,
        continuation,
        client_call_details,
        request_or_iterator,
        interceptor,
        is_client_stream=False,
    ):
        self._continuation = continuation
        self._client_call_details = client_call_details
        self._is_client_stream = is_client_stream
        self._source_request = request_or_iterator
        self._interceptor = interceptor

        self._uses_factory = is_client_stream and callable(request_or_iterator)
        self._payload = (
            None
            if self._uses_factory
            else (
                _ReplayableIterator(request_or_iterator)
                if is_client_stream
                else request_or_iterator
            )
        )

        self._retry_count = 0
        self._call = None
        self._lock = threading.RLock()

        timeout = getattr(self._client_call_details, "timeout", None)
        self._initial_timeout = timeout if isinstance(timeout, (int, float)) else None
        self._start_time = time.monotonic() if self._initial_timeout else None

        self._completion_event = threading.Event()
        self._done_callbacks = []
        self._terminal_exception = None

        self._start_call()

    def _start_call(self):
        self._attempt_cert = (
            self._interceptor._wrapper._cached_cert
            if self._interceptor._wrapper
            else None
        )

        with self._lock:
            if self._uses_factory:
                payload = self._source_request()
            else:
                payload = (
                    iter(self._payload) if self._is_client_stream else self._payload
                )

            call_details = self._client_call_details
            if self._start_time and self._initial_timeout:
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
            with self._lock:
                self._completion_event.set()
                callbacks_to_fire = list(self._done_callbacks)
            for fn in callbacks_to_fire:
                try:
                    fn(self)
                except Exception as e:
                    _LOGGER.warning("Callback failed: %s", e)
            return

        exc = inner_future.exception()
        if isinstance(exc, grpc.RpcError):
            status_code = exc.code()

            can_replay = (
                True
                if self._uses_factory
                else (self._payload.can_replay() if self._is_client_stream else True)
            )

            should_retry, call_cert, call_key, pwd = self._interceptor._should_retry(
                status_code, self._retry_count, getattr(self, "_attempt_cert", None)
            )
            if can_replay and should_retry:
                if getattr(self._interceptor, "_wrapper", None):
                    try:
                        self._interceptor._wrapper.refresh_logic(
                            1, call_cert, call_key, pwd
                        )
                    except Exception as e:
                        with self._lock:
                            self._terminal_exception = e
                        self._completion_event.set()
                        return
                with self._lock:
                    self._retry_count += 1
                try:
                    self._start_call()
                    return
                except Exception as e:
                    self._terminal_exception = e

            if self._interceptor._wrapper:
                (
                    chk_should_retry,
                    chk_cert,
                    chk_key,
                    chk_pwd,
                ) = self._interceptor._should_retry(status_code, 0, self._attempt_cert)
                if chk_should_retry:
                    try:
                        self._interceptor._wrapper.refresh_logic(
                            1, chk_cert, chk_key, chk_pwd
                        )
                    except Exception:
                        pass
        with self._lock:
            self._completion_event.set()
            callbacks_to_fire = list(self._done_callbacks)

        for fn in callbacks_to_fire:
            try:
                fn(self)
            except Exception as e:
                _LOGGER.warning("Callback failed: %s", e)

    def add_done_callback(self, fn):
        with self._lock:
            if self._completion_event.is_set():
                fire_now = True
            else:
                self._done_callbacks.append(fn)
                fire_now = False

        if fire_now:
            try:
                fn(self)
            except Exception:
                pass

    def result(self, timeout=None):
        if not self._completion_event.wait(timeout):
            raise grpc.FutureTimeoutError()
        with self._lock:
            if self._terminal_exception is not None:
                raise self._terminal_exception
            current_future = self._call
        return current_future.result()

    def exception(self, timeout=None):
        if not self._completion_event.wait(timeout):
            raise grpc.FutureTimeoutError()
        with self._lock:
            if self._terminal_exception is not None:
                return self._terminal_exception
            return self._call.exception()

    def traceback(self, timeout=None):
        if not self._completion_event.wait(timeout):
            raise grpc.FutureTimeoutError()
        with self._lock:
            if self._terminal_exception is not None:
                return self._terminal_exception.__traceback__
            return self._call.traceback()

    def initial_metadata(self):
        self._completion_event.wait()
        with self._lock:
            if self._terminal_exception is not None:
                return None
            return self._call.initial_metadata()

    def trailing_metadata(self):
        self._completion_event.wait()
        with self._lock:
            if self._terminal_exception is not None:
                return None
            return self._call.trailing_metadata()

    def code(self):
        self._completion_event.wait()
        with self._lock:
            if hasattr(self._terminal_exception, "code"):
                return self._terminal_exception.code()
            return self._call.code()

    def details(self):
        self._completion_event.wait()
        with self._lock:
            if hasattr(self._terminal_exception, "details"):
                return self._terminal_exception.details()
            return self._call.details()

class _RetryableStreamResponseIterator(_BaseCallWrapper):
    def __init__(
        self,
        continuation,
        client_call_details,
        request_or_iterator,
        interceptor,
        is_client_stream=False,
    ):
        self._continuation = continuation
        self._client_call_details = client_call_details
        self._is_client_stream = is_client_stream
        self._source_request = request_or_iterator
        self._interceptor = interceptor

        self._uses_factory = is_client_stream and callable(request_or_iterator)
        self._payload = (
            None
            if self._uses_factory
            else (
                _ReplayableIterator(request_or_iterator)
                if is_client_stream
                else request_or_iterator
            )
        )
        self._call = None
        self._retry_count = 0
        self._yielded_any_response = False
        self._lock = threading.RLock()

        timeout = getattr(self._client_call_details, "timeout", None)
        self._initial_timeout = timeout if isinstance(timeout, (int, float)) else None
        self._start_time = time.monotonic() if self._initial_timeout else None

        self._is_completed = False
        self._done_callbacks = []

        self._start_call()

    def _start_call(self):
        self._attempt_cert = (
            self._interceptor._wrapper._cached_cert
            if getattr(self._interceptor, "_wrapper", None)
            else None
        )
        with self._lock:
            if self._uses_factory:
                payload = self._source_request()
            else:
                payload = (
                    iter(self._payload) if self._is_client_stream else self._payload
                )

            call_details = self._client_call_details
            if self._start_time and self._initial_timeout:
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
            self._call.add_done_callback(self._on_inner_call_done)

    def _trigger_callbacks(self):
        with self._lock:
            if self._is_completed:
                return
            self._is_completed = True
            callbacks = list(self._done_callbacks)

        for fn in callbacks:
            try:
                fn(self)
            except Exception:
                pass

    def _on_inner_call_done(self, inner_call):
        with self._lock:
            if self._call is not inner_call:
                return
            # Intercept and suppress premature callbacks for UNAUTHENTICATED.
            # __next__ inherently handles this error and manages triggering callbacks
            # later if retriies are exhausted.
            if (
                callable(getattr(inner_call, "code", None))
                and inner_call.code() == grpc.StatusCode.UNAUTHENTICATED
            ):
                return
        self._trigger_callbacks()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            with self._lock:
                current_call = self._call

            try:
                response = next(current_call)
                self._yielded_any_response = True
                return response
            except StopIteration:
                self._trigger_callbacks()
                raise
            except grpc.RpcError as e:
                status_code = getattr(e, "code", lambda: None)()
                with self._lock:
                    if self._call is not current_call:
                        continue

                can_replay = (
                    True
                    if self._uses_factory
                    else (
                        self._payload.can_replay() if self._is_client_stream else True
                    )
                )

                (
                    should_retry,
                    call_cert,
                    call_key,
                    pwd,
                ) = self._interceptor._should_retry(
                    status_code,
                    self._retry_count,
                    getattr(self, "_attempt_cert", None),
                )

                if not self._yielded_any_response and can_replay and should_retry:
                    try:
                        if getattr(self._interceptor, "_wrapper", None):
                            self._interceptor._wrapper.refresh_logic(
                                1, call_cert, call_key, pwd
                            )

                        with self._lock:
                            self._retry_count += 1
                            self._start_call()

                    except Exception as fallback_e:
                        self._trigger_callbacks()
                        raise fallback_e

                    continue
                else:
                    # Non-retryable error, check if another rotation happened while we were finishing
                    if getattr(self._interceptor, "_wrapper", None):
                        (
                            chk_should_retry,
                            chk_cert,
                            chk_key,
                            chk_pwd,
                        ) = self._interceptor._should_retry(
                            status_code, 0, getattr(self, "_attempt_cert", None)
                        )
                        if chk_should_retry:
                            try:
                                self._interceptor._wrapper.refresh_logic(
                                    1, chk_cert, chk_key, chk_pwd
                                )
                            except Exception:
                                pass  # Terminal anyway

                    self._trigger_callbacks()
                    raise e

    def add_done_callback(self, fn):
        with self._lock:
            if getattr(self, "_is_completed", False):
                fire_now = True
            else:
                self._done_callbacks.append(fn)
                fire_now = False

        if fire_now:
            try:
                fn(self)
            except Exception:
                pass

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

    def time_remaining(self):
        return self._call.time_remaining()

    def add_callback(self, callback):
        self._call.add_callback(callback)
