# Copyright 2024 Google LLC
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

import asyncio
import collections.abc
from contextlib import asynccontextmanager
import functools
import http.client as http_client
import inspect
import logging
import time
from typing import Mapping, Optional, Tuple, TYPE_CHECKING, Union
import urllib.parse
import warnings

from google.auth import _exponential_backoff, exceptions
from google.auth.aio import transport
from google.auth.aio.credentials import Credentials
from google.auth.aio.transport import mtls
from google.auth.exceptions import TimeoutError
import google.auth.transport._mtls_helper

if TYPE_CHECKING:  # pragma: NO COVER
    import aiohttp
    from aiohttp import ClientTimeout  # type: ignore

else:
    try:
        import aiohttp
        from aiohttp import ClientTimeout
    except (ImportError, AttributeError):
        ClientTimeout = None

_LOGGER = logging.getLogger(__name__)
_MTLS_URL_PREFIXES = [
    "mtls.googleapis.com",
    "mtls.sandbox.googleapis.com",
    "p.googleapis.com",
]

# Tracks the internal aiohttp installation and usage
try:
    from google.auth.aio.transport.aiohttp import Request as AiohttpRequest

    AIOHTTP_INSTALLED = True
except ImportError:  # pragma: NO COVER
    AIOHTTP_INSTALLED = False


def _retrieve_task_exception(task: "asyncio.Task") -> None:
    """Mark a finished task's exception as retrieved.

    Used as a done-callback so that a background mTLS initialization failure
    that nobody ends up awaiting (for example, because the only caller timed
    out) does not later surface as an unraisable
    "Task exception was never retrieved" warning during garbage collection.
    Callers that *do* await the task still observe the exception normally.
    """
    if not task.cancelled():
        task.exception()


@asynccontextmanager
async def timeout_guard(timeout):
    """
    timeout_guard is an asynchronous context manager to apply a timeout to an asynchronous block of code.

    Args:
        timeout (float): The time in seconds before the context manager times out.

    Raises:
        google.auth.exceptions.TimeoutError: If the code within the context exceeds the provided timeout.

    Usage:
        async with timeout_guard(10) as with_timeout:
            await with_timeout(async_function())
    """
    start = time.monotonic()
    total_timeout = timeout

    def _remaining_time():
        if total_timeout is None:
            return None
        elapsed = time.monotonic() - start
        remaining = total_timeout - elapsed
        if remaining <= 0:
            raise TimeoutError(
                f"Context manager exceeded the configured timeout of {total_timeout}s."
            )
        return remaining

    async def with_timeout(coro):
        try:
            remaining = _remaining_time()
            response = await asyncio.wait_for(coro, remaining)
            return response
        except (asyncio.TimeoutError, TimeoutError) as e:
            raise TimeoutError(
                f"The operation {coro} exceeded the configured timeout of {total_timeout}s."
            ) from e

    try:
        yield with_timeout

    finally:
        _remaining_time()


class AsyncAuthorizedSession:
    """This is an asynchronous implementation of :class:`google.auth.requests.AuthorizedSession` class.
    We utilize an instance of a class that implements :class:`google.auth.aio.transport.Request` configured
    by the caller or otherwise default to `google.auth.aio.transport.aiohttp.Request` if the external aiohttp
    package is installed.

    A Requests Session class with credentials.

    This class is used to perform asynchronous requests to API endpoints that require
    authorization::

        import aiohttp
        from google.auth.aio.transport import sessions

        async with sessions.AsyncAuthorizedSession(credentials) as authed_session:
            response = await authed_session.request(
                'GET', 'https://www.googleapis.com/storage/v1/b')

    The underlying :meth:`request` implementation handles adding the
    credentials' headers to the request and refreshing credentials as needed.

    Args:
        credentials (google.auth.aio.credentials.Credentials):
            The credentials to add to the request.
        auth_request (Optional[google.auth.aio.transport.Request]):
            An instance of a class that implements
            :class:`~google.auth.aio.transport.Request` used to make requests
            and refresh credentials. If not passed,
            an instance of :class:`~google.auth.aio.transport.aiohttp.Request`
            is created.

    Raises:
        - google.auth.exceptions.TransportError: If `auth_request` is `None`
            and the external package `aiohttp` is not installed.
        - google.auth.exceptions.InvalidType: If the provided credentials are
            not of type `google.auth.aio.credentials.Credentials`.
    """

    def __init__(
        self, credentials: Credentials, auth_request: Optional[transport.Request] = None
    ):
        if not isinstance(credentials, Credentials):
            raise exceptions.InvalidType(
                f"The configured credentials of type {type(credentials)} are invalid and must be of type `google.auth.aio.credentials.Credentials`"
            )
        self._credentials = credentials
        _auth_request = auth_request
        if not _auth_request and AIOHTTP_INSTALLED:
            _auth_request = AiohttpRequest()
        self._is_mtls = False
        self._mtls_init_task: Optional[asyncio.Task] = None
        self._cached_cert = None
        self._client_cert_callback = None
        self._old_auth_requests: list[transport.Request] = []
        if _auth_request is None:
            raise exceptions.TransportError(
                "`auth_request` must either be configured or the external package `aiohttp` must be installed to use the default value."
            )
        self._auth_request = _auth_request
        self._mtls_rotation_lock: Optional[asyncio.Lock] = None
        self._mtls_check_counter = 0
        # Incremented every time the mTLS channel is successfully reconfigured.
        # Unlike a coroutine-local flag, this lets a request that skipped the
        # rotation check (because a concurrent request already performed it)
        # still observe that the channel changed since its own 401.
        self._mtls_reconfig_counter = 0
        # Value of `_refresh_counter` at the moment of the most recent
        # reconfiguration. A credential refresh is only considered redundant
        # if it happened *after* the latest channel change, since a
        # certificate-bound token minted on the old channel is not valid on
        # the new one.
        self._refresh_counter_at_last_reconfig = 0
        # Serializes the decision to create a new mTLS initialization task so
        # that two concurrent callers cannot both spawn `_do_configure()`.
        self._mtls_init_lock: Optional[asyncio.Lock] = None
        self._refresh_lock: Optional[asyncio.Lock] = None
        self._refresh_counter = 0

    async def _trim_old_auth_requests(self) -> None:
        """Close retired transports, keeping at most the two most recent."""
        while len(self._old_auth_requests) > 2:
            oldest_auth_request = self._old_auth_requests.pop(0)
            try:
                if hasattr(oldest_auth_request, "close"):
                    res = oldest_auth_request.close()
                    if inspect.isawaitable(res):
                        await res
            except Exception:
                pass

    async def _reset_non_mtls_state(self) -> None:
        """Clear mTLS state, retiring a library-owned mTLS transport.

        If the session previously installed its own mTLS-enabled transport,
        that transport still presents the old client certificate. Simply
        clearing the flags would leave subsequent requests sending a stale
        cert, so the transport is retired and replaced with a fresh non-mTLS
        one. A caller-supplied custom transport is never replaced.
        """
        was_mtls = self._is_mtls
        self._is_mtls = False
        self._cached_cert = None
        if (
            was_mtls
            and AIOHTTP_INSTALLED
            and isinstance(self._auth_request, AiohttpRequest)
        ):
            self._old_auth_requests.append(self._auth_request)
            self._auth_request = AiohttpRequest()
            await self._trim_old_auth_requests()

    async def configure_mtls_channel(
        self,
        client_cert_callback=None,
        force: bool = False,
        _cert_key_override: Optional[Tuple[bytes, bytes]] = None,
    ):
        """Configure the client certificate and key for SSL connection.

        This method configures mTLS if client certificates are explicitly enabled
        (via GOOGLE_API_USE_CLIENT_CERTIFICATE=true) or auto-enabled (when the env
        variable is unset and workload certificates are discovered). In these cases,
        the underlying transport will be reconfigured to use mTLS.

        Note: This function does nothing if the `aiohttp` library is not
        installed.
        Important: Calling this method will close any ongoing API requests associated
        with the current session. To ensure a smooth transition, it is recommended
        to call this during session initialization.

        Args:
            client_cert_callback (Optional[Callable[[], (bytes, bytes)]]):
                The optional callback returns the client certificate and private
                key bytes both in PEM format.
                If the callback is None, application default SSL credentials
                will be used.
            force (bool):
                Whether to force reconfiguration even if the channel is already configured
                with the same callback.
            _cert_key_override (Optional[Tuple[bytes, bytes]]):
                Internal use only. An explicit (cert, key) pair to install,
                bypassing ``client_cert_callback`` resolution. Used by the
                certificate-rotation path so it does not have to temporarily
                mutate ``self._client_cert_callback``, which would otherwise
                be visible to (and clobber) concurrent callers. When set, the
                channel is always reconfigured and the user-supplied callback
                is left untouched.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
                creation failed for any reason.
        """
        if self._mtls_init_lock is None:
            self._mtls_init_lock = asyncio.Lock()
        init_lock = self._mtls_init_lock

        # Serialize the decide-and-create step so two concurrent callers cannot
        # both spawn `_do_configure()`. The lock is released before awaiting the
        # task itself, so a slow configuration does not block unrelated callers.
        async with init_lock:
            if _cert_key_override is not None:
                needs_reconfig = True
            else:
                is_explicit_reconfig = (
                    client_cert_callback != self._client_cert_callback
                )
                task_failed = (
                    self._mtls_init_task is not None
                    and self._mtls_init_task.done()
                    and (
                        self._mtls_init_task.cancelled()
                        or self._mtls_init_task.exception() is not None
                    )
                )
                needs_reconfig = (
                    self._mtls_init_task is None
                    or is_explicit_reconfig
                    or task_failed
                    or force
                )

            if not needs_reconfig:
                task = self._mtls_init_task
            else:
                old_task = self._mtls_init_task
                if old_task is not None and not old_task.done():
                    old_task.cancel()
                    # `asyncio.wait` does not re-raise the awaited task's
                    # exception, and does not convert that task's cancellation
                    # into ours -- while still letting a cancellation targeted
                    # at *this* coroutine propagate normally.
                    await asyncio.wait({old_task})
                if _cert_key_override is None:
                    # Only a user-driven call may change the stored callback.
                    # The internal rotation path leaves it untouched.
                    self._client_cert_callback = client_cert_callback

                async def _do_configure():
                    # Run the blocking check in an executor
                    use_client_cert = await mtls._run_in_executor(
                        google.auth.transport._mtls_helper.check_use_client_cert
                    )
                    if not use_client_cert:
                        return

                    try:
                        if _cert_key_override is not None:
                            is_mtls = True
                            cert, key = _cert_key_override
                        else:
                            (
                                is_mtls,
                                cert,
                                key,
                            ) = await mtls.get_client_cert_and_key(client_cert_callback)

                        if is_mtls:
                            # Re-create the auth request with the new SSL context
                            if AIOHTTP_INSTALLED and isinstance(
                                self._auth_request, AiohttpRequest
                            ):
                                ssl_context = await mtls._run_in_executor(
                                    mtls.make_client_cert_ssl_context, cert, key
                                )
                                connector = aiohttp.TCPConnector(ssl=ssl_context)
                                new_session = aiohttp.ClientSession(connector=connector)

                                old_auth_request = self._auth_request
                                self._auth_request = AiohttpRequest(session=new_session)
                                self._is_mtls = True
                                self._cached_cert = cert
                                self._old_auth_requests.append(old_auth_request)
                                await self._trim_old_auth_requests()

                            else:
                                await self._reset_non_mtls_state()
                                warnings.warn(
                                    "Attempted to establish mTLS, but a custom async transport was provided. "
                                    "google-auth cannot automatically configure custom transports for mTLS. "
                                    "Falling back to standard TLS. If your custom transport is not manually "
                                    "configured for mTLS, you may encounter 401 Unauthorized errors when "
                                    "using Certificate-Bound Tokens.",
                                    UserWarning,
                                )
                        else:
                            await self._reset_non_mtls_state()

                    except Exception as caught_exc:
                        new_exc = exceptions.MutualTLSChannelError(caught_exc)
                        raise new_exc from caught_exc

                task = asyncio.create_task(_do_configure())
                # If every awaiter goes away (e.g. the only caller timed out)
                # a failure would otherwise surface as an unraisable
                # "Task exception was never retrieved" warning at GC time.
                task.add_done_callback(_retrieve_task_exception)
                self._mtls_init_task = task

            if task is None:  # pragma: no cover - defensive
                raise exceptions.MutualTLSChannelError(
                    "mTLS initialization task was not created."
                )

        while True:
            try:
                return await asyncio.shield(task)
            except asyncio.CancelledError:
                if not task.cancelled():
                    # The cancellation targeted this caller rather than the
                    # initialization task, so it must propagate.
                    raise
                # The task we were waiting on was cancelled by a concurrent
                # reconfiguration. That coroutine holds `init_lock` across
                # both the cancel and the creation of the replacement, so
                # acquiring it here waits until the replacement is installed.
                async with init_lock:
                    current = self._mtls_init_task
                if current is None or current is task:
                    # Nobody installed a replacement (e.g. the session is
                    # closing); surface the cancellation.
                    raise
                # Follow the replacement rather than reporting a cancellation
                # this caller never requested.
                task = current

    async def request(
        self,
        method: str,
        url: str,
        data: Optional[bytes] = None,
        headers: Optional[Mapping[str, str]] = None,
        max_allowed_time: float = transport._DEFAULT_TIMEOUT_SECONDS,
        timeout: Union[float, ClientTimeout] = transport._DEFAULT_TIMEOUT_SECONDS,
        total_attempts: Optional[int] = transport.DEFAULT_MAX_RETRY_ATTEMPTS,
        **kwargs,
    ) -> transport.Response:
        """
        Args:
                method (str): The http method used to make the request.
                url (str): The URI to be requested.
                data (Optional[bytes]): The payload or body in HTTP request.
                headers (Optional[Mapping[str, str]]): Request headers.
                timeout (float, aiohttp.ClientTimeout):
                The amount of time in seconds to wait for the server response
                with each individual request.
                max_allowed_time (float):
                If the method runs longer than this, a ``Timeout`` exception is
                automatically raised. Unlike the ``timeout`` parameter, this
                value applies to the total method execution time, even if
                multiple requests are made under the hood.
                total_attempts (int):
                The total number of retry attempts.

                Mind that it is not guaranteed that the timeout error is raised
                at ``max_allowed_time``. It might take longer, for example, if
                an underlying request takes a lot of time, but the request
                itself does not timeout, e.g. if a large file is being
                transmitted. The timeout error will be raised after such
                request completes.

        Returns:
                google.auth.aio.transport.Response: The HTTP response.

        Raises:
                google.auth.exceptions.TimeoutError: If the method does not complete within
                the configured `max_allowed_time` or the request exceeds the configured
                `timeout`.
                google.auth.exceptions.MutualTLSChannelError: If mutual TLS
                channel reconfiguration fails for any reason during certificate rotation.
        """
        _auth_retry_count = kwargs.pop("_auth_retry_count", 0)
        # Wait for any in-flight mTLS initialization to settle. `asyncio.wait`
        # neither re-raises the task's exception (the request should fail
        # naturally elsewhere instead) nor turns that task's cancellation into
        # ours, while a cancellation aimed at *this* coroutine still
        # propagates. Looping re-reads the attribute in case a concurrent
        # `configure_mtls_channel()` swapped in a replacement task.
        while self._mtls_init_task is not None and not self._mtls_init_task.done():
            await asyncio.wait({self._mtls_init_task})
        retries = _exponential_backoff.AsyncExponentialBackoff(
            total_attempts=total_attempts,
        )
        request_headers = dict(headers) if headers is not None else {}
        start_time = time.monotonic()
        refresh_counter_at_error = self._refresh_counter
        check_counter_at_error = self._mtls_check_counter
        reconfig_counter_at_error = self._mtls_reconfig_counter
        async with timeout_guard(max_allowed_time) as with_timeout:
            await with_timeout(
                # Note: before_request will attempt to refresh credentials if expired.
                self._credentials.before_request(
                    self._auth_request, method, url, request_headers
                )
            )
            actual_timeout: float = 0.0
            if ClientTimeout is not None and isinstance(timeout, ClientTimeout):
                actual_timeout = timeout.total if timeout.total is not None else 0.0
            elif isinstance(timeout, (int, float)):
                actual_timeout = float(timeout)
            # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
            # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
            async for _ in retries:  # pragma: no branch
                response = await with_timeout(
                    self._auth_request(
                        url, method, data, request_headers, actual_timeout, **kwargs
                    )
                )

                if response.status_code not in transport.DEFAULT_RETRYABLE_STATUS_CODES:
                    break

        if response.status_code == http_client.UNAUTHORIZED:
            if _auth_retry_count < 2:
                try:
                    if max_allowed_time is not None:
                        elapsed = time.monotonic() - start_time
                        remaining_time = max(0.0, max_allowed_time - elapsed)
                        if remaining_time == 0.0:
                            raise google.auth.exceptions.TimeoutError(
                                "Timeout exceeded before credential refresh could begin"
                            )
                    else:
                        remaining_time = None
                    is_streaming = data is not None and (
                        isinstance(
                            data,
                            (collections.abc.Iterator, collections.abc.AsyncIterable),
                        )
                        or hasattr(data, "read")
                    )

                    async def _recover_auth_state():
                        is_mtls_endpoint = False
                        if self._is_mtls:
                            hostname = urllib.parse.urlsplit(url).hostname
                            if hostname:
                                is_mtls_endpoint = any(
                                    hostname == prefix
                                    or hostname.endswith("." + prefix)
                                    for prefix in _MTLS_URL_PREFIXES
                                )
                            # Snapshot the stale certificate state BEFORE acquiring the lock.
                            # This represents the cert that caused the 401 rejection.
                            if is_mtls_endpoint:
                                if self._mtls_rotation_lock is None:
                                    self._mtls_rotation_lock = asyncio.Lock()
                                async with self._mtls_rotation_lock:
                                    # Check if another coroutine already reconfigured mTLS or
                                    # ran the validation check.
                                    if (
                                        self._mtls_check_counter
                                        > check_counter_at_error
                                    ):
                                        pass
                                    else:
                                        try:
                                            (
                                                call_cert_bytes,
                                                call_key_bytes,
                                                cached_fingerprint,
                                                current_cert_fingerprint,
                                            ) = await mtls.check_parameters_for_unauthorized_response(
                                                self._cached_cert,
                                                self._client_cert_callback,
                                            )
                                        except (
                                            exceptions.ClientCertError,
                                            exceptions.MutualTLSChannelError,
                                            OSError,
                                            ValueError,
                                            TypeError,
                                            ImportError,
                                        ) as e:
                                            _LOGGER.warning(
                                                "Failed to check client certificate parameters: %s. "
                                                "Falling back to credential refresh and retry.",
                                                e,
                                            )
                                        else:
                                            if (
                                                current_cert_fingerprint is not None
                                                and cached_fingerprint
                                                != current_cert_fingerprint
                                            ):
                                                try:
                                                    _LOGGER.info(
                                                        "Client certificate has changed, reconfiguring mTLS "
                                                        "channel."
                                                    )
                                                    # Pass the rotated cert/key
                                                    # directly rather than
                                                    # temporarily swapping
                                                    # `self._client_cert_callback`,
                                                    # which is shared state and
                                                    # could be observed (or
                                                    # clobbered) by concurrent
                                                    # callers.
                                                    await self.configure_mtls_channel(
                                                        _cert_key_override=(
                                                            call_cert_bytes,
                                                            call_key_bytes,
                                                        )
                                                    )
                                                    self._refresh_counter_at_last_reconfig = (
                                                        self._refresh_counter
                                                    )
                                                    self._mtls_reconfig_counter += 1
                                                except Exception as e:
                                                    _LOGGER.error(
                                                        "Failed to reconfigure mTLS channel: %s",
                                                        e,
                                                    )
                                                    raise exceptions.MutualTLSChannelError(
                                                        "Failed to reconfigure mTLS channel"
                                                    ) from e
                                            else:
                                                if current_cert_fingerprint is None:
                                                    _LOGGER.info(
                                                        "Skipping reconfiguration of mTLS channel because the client"
                                                        " certificate does not exist."
                                                    )
                                                else:
                                                    _LOGGER.info(
                                                        "Skipping reconfiguration of mTLS channel because the client"
                                                        " certificate has not changed."
                                                    )
                                        # Always increment so waiting tasks skip the check block
                                        self._mtls_check_counter += 1
                        # Derived from session state rather than a local flag:
                        # a concurrent request may have performed the rotation
                        # on our behalf (we then skipped the check block), and
                        # that request still needs to retry on the new channel.
                        channel_reconfigured = (
                            self._mtls_reconfig_counter > reconfig_counter_at_error
                        )

                        if self._refresh_lock is None:
                            self._refresh_lock = asyncio.Lock()

                        async with self._refresh_lock:
                            # A refresh is redundant only if it happened after
                            # both this request's 401 and the most recent
                            # channel reconfiguration. Using the later of the
                            # two keeps concurrent requests de-duplicated while
                            # still guaranteeing at least one refresh against a
                            # freshly rotated channel.
                            refresh_baseline = max(
                                refresh_counter_at_error,
                                self._refresh_counter_at_last_reconfig,
                            )
                            if self._refresh_counter > refresh_baseline:
                                _LOGGER.debug(
                                    "Credentials were already refreshed by a concurrent task. Skipping duplicate refresh."
                                )
                            else:
                                try:
                                    await self._credentials.refresh(self._auth_request)
                                except NotImplementedError:
                                    _LOGGER.debug(
                                        "Credentials do not implement refresh()."
                                    )
                                    if not channel_reconfigured:
                                        return response
                                except exceptions.InvalidOperation as e:
                                    _LOGGER.debug(
                                        "Credentials cannot be refreshed: %s",
                                        e,
                                    )
                                    if not channel_reconfigured:
                                        return response
                                except exceptions.RefreshError as e:
                                    _LOGGER.debug(
                                        "Credential refresh failed, returning 401 response. Error: %s",
                                        e,
                                    )
                                    return response
                                else:
                                    self._refresh_counter += 1

                        if is_streaming:
                            return response
                        # Return None to explicitly signal successful recovery & trigger retry if needed
                        return None

                    async with timeout_guard(remaining_time) as auth_with_timeout:
                        early_return_response = await auth_with_timeout(
                            _recover_auth_state()
                        )
                except (Exception, asyncio.CancelledError):
                    if hasattr(response, "close"):
                        try:
                            res = response.close()
                            if inspect.isawaitable(res):
                                await res
                        except Exception:
                            pass
                    raise
                # If it returned a response (meaning streaming or error), bail out
                if early_return_response is not None:
                    return early_return_response
                if hasattr(response, "close"):
                    try:
                        res = response.close()
                        if inspect.isawaitable(res):
                            await res
                    except Exception:
                        pass
                if max_allowed_time is not None:
                    remaining_time = max(
                        0.0, max_allowed_time - (time.monotonic() - start_time)
                    )
                    if remaining_time == 0.0:
                        raise google.auth.exceptions.TimeoutError(
                            "Timeout exceeded before retrying the request"
                        )
                kwargs["_auth_retry_count"] = _auth_retry_count + 1
                return await self.request(
                    method,
                    url,
                    data=data,
                    headers=headers,
                    max_allowed_time=remaining_time,
                    timeout=timeout,
                    total_attempts=total_attempts,
                    **kwargs,
                )
        return response

    @functools.wraps(request)
    async def get(
        self,
        url: str,
        data: Optional[bytes] = None,
        headers: Optional[Mapping[str, str]] = None,
        max_allowed_time: float = transport._DEFAULT_TIMEOUT_SECONDS,
        timeout: Union[float, ClientTimeout] = transport._DEFAULT_TIMEOUT_SECONDS,
        total_attempts: Optional[int] = transport.DEFAULT_MAX_RETRY_ATTEMPTS,
        **kwargs,
    ) -> transport.Response:
        """
        Args:
                url (str): The URI to be requested.
                data (Optional[bytes]): The payload or body in HTTP request.
                headers (Optional[Mapping[str, str]]): Request headers.
                max_allowed_time (float):
                If the method runs longer than this, a ``Timeout`` exception is
                automatically raised. Unlike the ``timeout`` parameter, this
                value applies to the total method execution time, even if
                multiple requests are made under the hood.
                timeout (float, aiohttp.ClientTimeout):
                The amount of time in seconds to wait for the server response
                with each individual request.
                total_attempts (int):
                The total number of retry attempts.

                Mind that it is not guaranteed that the timeout error is raised
                at ``max_allowed_time``. It might take longer, for example, if
                an underlying request takes a lot of time, but the request
                itself does not timeout, e.g. if a large file is being
                transmitted. The timeout error will be raised after such
                request completes.

        Returns:
                google.auth.aio.transport.Response: The HTTP response.

        Raises:
                google.auth.exceptions.TimeoutError: If the method does not complete within
                the configured `max_allowed_time` or the request exceeds the configured
                `timeout`.
        """
        return await self.request(
            "GET",
            url,
            data,
            headers,
            max_allowed_time,
            timeout,
            total_attempts,
            **kwargs,
        )

    @functools.wraps(request)
    async def post(
        self,
        url: str,
        data: Optional[bytes] = None,
        headers: Optional[Mapping[str, str]] = None,
        max_allowed_time: float = transport._DEFAULT_TIMEOUT_SECONDS,
        timeout: Union[float, ClientTimeout] = transport._DEFAULT_TIMEOUT_SECONDS,
        total_attempts: Optional[int] = transport.DEFAULT_MAX_RETRY_ATTEMPTS,
        **kwargs,
    ) -> transport.Response:
        """
        Args:
                url (str): The URI to be requested.
                data (Optional[bytes]): The payload or body in HTTP request.
                headers (Optional[Mapping[str, str]]): Request headers.
                max_allowed_time (float):
                If the method runs longer than this, a ``Timeout`` exception is
                automatically raised. Unlike the ``timeout`` parameter, this
                value applies to the total method execution time, even if
                multiple requests are made under the hood.
                timeout (float, aiohttp.ClientTimeout):
                The amount of time in seconds to wait for the server response
                with each individual request.
                total_attempts (int):
                The total number of retry attempts.

                Mind that it is not guaranteed that the timeout error is raised
                at ``max_allowed_time``. It might take longer, for example, if
                an underlying request takes a lot of time, but the request
                itself does not timeout, e.g. if a large file is being
                transmitted. The timeout error will be raised after such
                request completes.

        Returns:
                google.auth.aio.transport.Response: The HTTP response.

        Raises:
                google.auth.exceptions.TimeoutError: If the method does not complete within
                the configured `max_allowed_time` or the request exceeds the configured
                `timeout`.
        """
        return await self.request(
            "POST",
            url,
            data,
            headers,
            max_allowed_time,
            timeout,
            total_attempts,
            **kwargs,
        )

    @functools.wraps(request)
    async def put(
        self,
        url: str,
        data: Optional[bytes] = None,
        headers: Optional[Mapping[str, str]] = None,
        max_allowed_time: float = transport._DEFAULT_TIMEOUT_SECONDS,
        timeout: Union[float, ClientTimeout] = transport._DEFAULT_TIMEOUT_SECONDS,
        total_attempts: Optional[int] = transport.DEFAULT_MAX_RETRY_ATTEMPTS,
        **kwargs,
    ) -> transport.Response:
        """
        Args:
                url (str): The URI to be requested.
                data (Optional[bytes]): The payload or body in HTTP request.
                headers (Optional[Mapping[str, str]]): Request headers.
                max_allowed_time (float):
                If the method runs longer than this, a ``Timeout`` exception is
                automatically raised. Unlike the ``timeout`` parameter, this
                value applies to the total method execution time, even if
                multiple requests are made under the hood.
                timeout (float, aiohttp.ClientTimeout):
                The amount of time in seconds to wait for the server response
                with each individual request.
                total_attempts (int):
                The total number of retry attempts.

                Mind that it is not guaranteed that the timeout error is raised
                at ``max_allowed_time``. It might take longer, for example, if
                an underlying request takes a lot of time, but the request
                itself does not timeout, e.g. if a large file is being
                transmitted. The timeout error will be raised after such
                request completes.

        Returns:
                google.auth.aio.transport.Response: The HTTP response.

        Raises:
                google.auth.exceptions.TimeoutError: If the method does not complete within
                the configured `max_allowed_time` or the request exceeds the configured
                `timeout`.
        """
        return await self.request(
            "PUT",
            url,
            data,
            headers,
            max_allowed_time,
            timeout,
            total_attempts,
            **kwargs,
        )

    @functools.wraps(request)
    async def patch(
        self,
        url: str,
        data: Optional[bytes] = None,
        headers: Optional[Mapping[str, str]] = None,
        max_allowed_time: float = transport._DEFAULT_TIMEOUT_SECONDS,
        timeout: Union[float, ClientTimeout] = transport._DEFAULT_TIMEOUT_SECONDS,
        total_attempts: Optional[int] = transport.DEFAULT_MAX_RETRY_ATTEMPTS,
        **kwargs,
    ) -> transport.Response:
        """
        Args:
                url (str): The URI to be requested.
                data (Optional[bytes]): The payload or body in HTTP request.
                headers (Optional[Mapping[str, str]]): Request headers.
                max_allowed_time (float):
                If the method runs longer than this, a ``Timeout`` exception is
                automatically raised. Unlike the ``timeout`` parameter, this
                value applies to the total method execution time, even if
                multiple requests are made under the hood.
                timeout (float, aiohttp.ClientTimeout):
                The amount of time in seconds to wait for the server response
                with each individual request.
                total_attempts (int):
                The total number of retry attempts.

                Mind that it is not guaranteed that the timeout error is raised
                at ``max_allowed_time``. It might take longer, for example, if
                an underlying request takes a lot of time, but the request
                itself does not timeout, e.g. if a large file is being
                transmitted. The timeout error will be raised after such
                request completes.

        Returns:
                google.auth.aio.transport.Response: The HTTP response.

        Raises:
                google.auth.exceptions.TimeoutError: If the method does not complete within
                the configured `max_allowed_time` or the request exceeds the configured
                `timeout`.
        """
        return await self.request(
            "PATCH",
            url,
            data,
            headers,
            max_allowed_time,
            timeout,
            total_attempts,
            **kwargs,
        )

    @functools.wraps(request)
    async def delete(
        self,
        url: str,
        data: Optional[bytes] = None,
        headers: Optional[Mapping[str, str]] = None,
        max_allowed_time: float = transport._DEFAULT_TIMEOUT_SECONDS,
        timeout: Union[float, ClientTimeout] = transport._DEFAULT_TIMEOUT_SECONDS,
        total_attempts: Optional[int] = transport.DEFAULT_MAX_RETRY_ATTEMPTS,
        **kwargs,
    ) -> transport.Response:
        """
        Args:
                url (str): The URI to be requested.
                data (Optional[bytes]): The payload or body in HTTP request.
                headers (Optional[Mapping[str, str]]): Request headers.
                max_allowed_time (float):
                If the method runs longer than this, a ``Timeout`` exception is
                automatically raised. Unlike the ``timeout`` parameter, this
                value applies to the total method execution time, even if
                multiple requests are made under the hood.
                timeout (float, aiohttp.ClientTimeout):
                The amount of time in seconds to wait for the server response
                with each individual request.
                total_attempts (int):
                The total number of retry attempts.

                Mind that it is not guaranteed that the timeout error is raised
                at ``max_allowed_time``. It might take longer, for example, if
                an underlying request takes a lot of time, but the request
                itself does not timeout, e.g. if a large file is being
                transmitted. The timeout error will be raised after such
                request completes.

        Returns:
                google.auth.aio.transport.Response: The HTTP response.

        Raises:
                google.auth.exceptions.TimeoutError: If the method does not complete within
                the configured `max_allowed_time` or the request exceeds the configured
                `timeout`.
        """
        return await self.request(
            "DELETE",
            url,
            data,
            headers,
            max_allowed_time,
            timeout,
            total_attempts,
            **kwargs,
        )

    @property
    def is_mtls(self):
        """Indicates if mutual TLS is enabled."""
        return self._is_mtls

    async def close(self) -> None:
        """
        Close the underlying auth request session.
        """
        try:
            if self._mtls_init_task and not self._mtls_init_task.done():
                self._mtls_init_task.cancel()
                # Same rationale as `configure_mtls_channel`: `asyncio.wait`
                # lets the cancelled initialization task unwind without
                # absorbing a cancellation aimed at this `close()` call.
                await asyncio.wait({self._mtls_init_task})
        finally:
            while self._old_auth_requests:
                old_request = self._old_auth_requests.pop(0)
                try:
                    if hasattr(old_request, "close"):
                        res = old_request.close()
                        if inspect.isawaitable(res):
                            await res
                except Exception:
                    pass
            try:
                if hasattr(self._auth_request, "close"):
                    res = self._auth_request.close()
                    if inspect.isawaitable(res):
                        await res
            except Exception:
                pass
