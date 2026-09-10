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
from typing import Mapping, Optional, TYPE_CHECKING, Union
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


@asynccontextmanager
async def timeout_guard(timeout):
    """
    timeout_guard is an asynchronous context manager to apply a timeout to an asynchronous block of code.

    Args:
        timeout (Optional[float]): The time in seconds before the context manager times out.
            If None, no timeout is applied.

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

    A Requests Session class with credentials and mutual TLS (mTLS) support.

    This class is used to perform asynchronous requests to API endpoints that require
    authorization::

        import aiohttp
        from google.auth.aio.transport import sessions

        async with sessions.AsyncAuthorizedSession(credentials) as authed_session:
            response = await authed_session.request(
                'GET', 'https://www.googleapis.com/storage/v1/b')

    The underlying :meth:`request` implementation handles adding the
    credentials' headers to the request, refreshing credentials as needed,
    and automatically recovering from certificate rotation on mTLS endpoints
    when 401 Unauthorized responses occur.

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
        google.auth.exceptions.TransportError: If `auth_request` is `None`
            and the external package `aiohttp` is not installed.
        google.auth.exceptions.InvalidType: If the provided credentials are
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
        self._mtls_init_task = None
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
        self._refresh_lock: Optional[asyncio.Lock] = None
        self._refresh_counter = 0

    async def configure_mtls_channel(self, client_cert_callback=None):
        """Configure or reconfigure the client certificate and key for SSL connections.

        This method configures mTLS if client certificates are explicitly enabled
        (via GOOGLE_API_USE_CLIENT_CERTIFICATE=true) or auto-enabled (when the env
        variable is unset and workload certificates are discovered). In these cases,
        the underlying transport will be configured or rotated to use mTLS.

        Note: This function does nothing if the `aiohttp` library is not installed
        or if custom non-aiohttp transports are used.

        Args:
            client_cert_callback (Optional[Callable[[], Tuple[bytes, bytes]]]):
                The optional callback returning the client certificate and private
                key bytes in PEM format. If None, application default SSL credentials
                or workload certificates will be discovered and used.

        Returns:
            bool: True if mTLS channel configuration succeeded and is enabled,
                False otherwise.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
                creation or client certificate discovery fails for any reason.
        """
        if self._mtls_init_task is None or self._mtls_init_task.done():
            self._client_cert_callback = client_cert_callback

            async def _do_configure():
                try:
                    (
                        is_mtls,
                        cert_bytes,
                        key_bytes,
                    ) = await mtls.get_client_cert_and_key(
                        self._client_cert_callback
                    )
                except Exception as e:
                    self._is_mtls = False
                    self._cached_cert = None
                    raise exceptions.MutualTLSChannelError(
                        "Client certificate discovery failed"
                    ) from e

                if is_mtls:
                    if AIOHTTP_INSTALLED and isinstance(
                        self._auth_request, AiohttpRequest
                    ):
                        if cert_bytes and key_bytes:
                            ssl_context = (
                                mtls.make_client_cert_ssl_context(
                                    cert_bytes, key_bytes
                                )
                            )
                            new_connector = aiohttp.TCPConnector(
                                ssl=ssl_context
                            )
                            new_session = aiohttp.ClientSession(
                                connector=new_connector
                            )

                            old_auth_request = self._auth_request
                            self._auth_request = AiohttpRequest(session=new_session)
                            self._is_mtls = is_mtls
                            self._cached_cert = cert_bytes
                            self._old_auth_requests.append(old_auth_request)

                            while len(self._old_auth_requests) > 2:
                                oldest_auth_request = self._old_auth_requests.pop(0)
                                try:
                                    if hasattr(oldest_auth_request, "close"):
                                        res = oldest_auth_request.close()
                                        if inspect.isawaitable(res):
                                            await res
                                except Exception:
                                    pass
                        else:
                            is_mtls = False
                            self._is_mtls = False
                            self._cached_cert = None
                            warnings.warn(
                                "Attempted to establish mTLS, but client "
                                "certificate or private key was not found."
                            )
                    else:
                        is_mtls = False
                        self._is_mtls = False
                        self._cached_cert = None
                        warnings.warn(
                            "Attempted to establish mTLS, but custom "
                            "request transport cannot be configured "
                            "for mTLS."
                        )
                else:
                    self._is_mtls = False
                    self._cached_cert = None

                return is_mtls

            self._mtls_init_task = asyncio.create_task(_do_configure())

        try:
            return await asyncio.shield(self._mtls_init_task)
        except BaseException:
            if (
                self._mtls_init_task is not None
                and self._mtls_init_task.done()
                and (self._mtls_init_task.cancelled() or self._mtls_init_task.exception() is not None)
            ):
                self._mtls_init_task = None
            raise

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
        """Make an authenticated asynchronous HTTP request with automatic retry and mTLS rotation.

        Args:
            method (str): The HTTP method used to make the request (e.g. "GET", "POST").
            url (str): The URI to be requested.
            data (Optional[bytes]): The payload or body in the HTTP request.
            headers (Optional[Mapping[str, str]]): Request headers.
            max_allowed_time (float): If the method runs longer than this, a
                ``google.auth.exceptions.TimeoutError`` is raised. Applies to total execution time.
            timeout (Union[float, aiohttp.ClientTimeout]): The timeout in seconds for each
                individual HTTP request attempt.
            total_attempts (Optional[int]): The maximum number of retry attempts for retryable errors.
            **kwargs: Additional arguments passed to the underlying HTTP transport.

        Returns:
            google.auth.aio.transport.Response: The HTTP response.

        Raises:
            google.auth.exceptions.TimeoutError: If the operation exceeds `max_allowed_time`
                or an individual request attempt exceeds `timeout`.
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
                reconfiguration fails for any reason during certificate rotation.
        """
        _auth_retry_count = kwargs.pop("_auth_retry_count", 0)
        if self._mtls_init_task and not self._mtls_init_task.done():
            try:
                await asyncio.shield(self._mtls_init_task)
            except (Exception, asyncio.CancelledError):
                pass

        retries = _exponential_backoff.AsyncExponentialBackoff(
            total_attempts=total_attempts,
        )
        request_headers = dict(headers) if headers is not None else {}
        start_time = time.monotonic()
        refresh_counter_at_error = self._refresh_counter
        check_counter_at_error = self._mtls_check_counter
        response = None

        try:
            async with timeout_guard(max_allowed_time) as with_timeout:
                await with_timeout(
                    self._credentials.before_request(
                        self._auth_request, method, url, request_headers
                    )
                )
                actual_timeout: float = 0.0
                if ClientTimeout is not None and isinstance(timeout, ClientTimeout):
                    actual_timeout = timeout.total if timeout.total is not None else 0.0
                elif isinstance(timeout, (int, float)):
                    actual_timeout = float(timeout)
                elif max_allowed_time is not None:
                    actual_timeout = max_allowed_time

                async for _ in retries:  # pragma: no branch
                    response = await with_timeout(
                        self._auth_request(
                            url, method, data, request_headers, actual_timeout, **kwargs
                        )
                    )
                    if response.status_code not in transport.DEFAULT_RETRYABLE_STATUS_CODES:
                        break
        except BaseException:
            if response is not None and hasattr(response, "close"):
                try:
                    res = response.close()
                    if inspect.isawaitable(res):
                        await res
                except Exception:
                    pass
            raise

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
                        channel_reconfigured = False
                        if self._is_mtls:
                            hostname = urllib.parse.urlsplit(url).hostname
                            if hostname:
                                is_mtls_endpoint = any(
                                    hostname == prefix
                                    or hostname.endswith("." + prefix)
                                    for prefix in _MTLS_URL_PREFIXES
                                )
                            if is_mtls_endpoint:
                                if self._mtls_rotation_lock is None:
                                    self._mtls_rotation_lock = asyncio.Lock()
                                async with self._mtls_rotation_lock:
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
                                            ImportError,
                                        ) as e:
                                            _LOGGER.warning(
                                                "Failed to check client certificate parameters: %s. Proceeding with original response.",
                                                e,
                                            )
                                        else:
                                            self._mtls_check_counter += 1
                                            if (
                                                current_cert_fingerprint is not None
                                                and cached_fingerprint
                                                != current_cert_fingerprint
                                            ):
                                                saved_callback = (
                                                    self._client_cert_callback
                                                )
                                                try:
                                                    _LOGGER.info(
                                                        "Client certificate has changed, reconfiguring mTLS "
                                                        "channel."
                                                    )
                                                    await self.configure_mtls_channel(
                                                        lambda: (
                                                            call_cert_bytes,
                                                            call_key_bytes,
                                                        )
                                                    )
                                                    channel_reconfigured = True
                                                except Exception as e:
                                                    _LOGGER.error(
                                                        "Failed to reconfigure mTLS channel: %s",
                                                        e,
                                                    )
                                                    raise exceptions.MutualTLSChannelError(
                                                        "Failed to reconfigure mTLS channel"
                                                    ) from e
                                                finally:
                                                    self._client_cert_callback = (
                                                        saved_callback
                                                    )
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

                        if self._refresh_lock is None:
                            self._refresh_lock = asyncio.Lock()

                        async with self._refresh_lock:
                            if self._refresh_counter > refresh_counter_at_error:
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
                                    return response
                                except (
                                    exceptions.RefreshError,
                                    getattr(exceptions, "InvalidOperation", Exception),
                                ) as e:
                                    _LOGGER.debug(
                                        "Credential refresh failed, returning 401 response. Error: %s",
                                        e,
                                    )
                                    return response
                                else:
                                    self._refresh_counter += 1

                        if is_streaming:
                            return response
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
        """Make an authenticated asynchronous GET request.

        Args:
            url (str): The URI to be requested.
            data (Optional[bytes]): The payload or body in the HTTP request.
            headers (Optional[Mapping[str, str]]): Request headers.
            max_allowed_time (float): Total execution timeout in seconds.
            timeout (Union[float, aiohttp.ClientTimeout]): Individual request timeout in seconds.
            total_attempts (Optional[int]): Maximum number of retry attempts.
            **kwargs: Additional keyword arguments passed to the underlying request transport.

        Returns:
            google.auth.aio.transport.Response: The HTTP response.

        Raises:
            google.auth.exceptions.TimeoutError: If the operation exceeds `max_allowed_time`
                or an individual request attempt exceeds `timeout`.
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
                reconfiguration fails for any reason during certificate rotation.
        """
        return await self.request(
            "GET",
            url,
            data=data,
            headers=headers,
            max_allowed_time=max_allowed_time,
            timeout=timeout,
            total_attempts=total_attempts,
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
        """Make an authenticated asynchronous POST request.

        Args:
            url (str): The URI to be requested.
            data (Optional[bytes]): The payload or body in the HTTP request.
            headers (Optional[Mapping[str, str]]): Request headers.
            max_allowed_time (float): Total execution timeout in seconds.
            timeout (Union[float, aiohttp.ClientTimeout]): Individual request timeout in seconds.
            total_attempts (Optional[int]): Maximum number of retry attempts.
            **kwargs: Additional keyword arguments passed to the underlying request transport.

        Returns:
            google.auth.aio.transport.Response: The HTTP response.

        Raises:
            google.auth.exceptions.TimeoutError: If the operation exceeds `max_allowed_time`
                or an individual request attempt exceeds `timeout`.
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
                reconfiguration fails for any reason during certificate rotation.
        """
        return await self.request(
            "POST",
            url,
            data=data,
            headers=headers,
            max_allowed_time=max_allowed_time,
            timeout=timeout,
            total_attempts=total_attempts,
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
        """Make an authenticated asynchronous PUT request.

        Args:
            url (str): The URI to be requested.
            data (Optional[bytes]): The payload or body in the HTTP request.
            headers (Optional[Mapping[str, str]]): Request headers.
            max_allowed_time (float): Total execution timeout in seconds.
            timeout (Union[float, aiohttp.ClientTimeout]): Individual request timeout in seconds.
            total_attempts (Optional[int]): Maximum number of retry attempts.
            **kwargs: Additional keyword arguments passed to the underlying request transport.

        Returns:
            google.auth.aio.transport.Response: The HTTP response.

        Raises:
            google.auth.exceptions.TimeoutError: If the operation exceeds `max_allowed_time`
                or an individual request attempt exceeds `timeout`.
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
                reconfiguration fails for any reason during certificate rotation.
        """
        return await self.request(
            "PUT",
            url,
            data=data,
            headers=headers,
            max_allowed_time=max_allowed_time,
            timeout=timeout,
            total_attempts=total_attempts,
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
        """Make an authenticated asynchronous PATCH request.

        Args:
            url (str): The URI to be requested.
            data (Optional[bytes]): The payload or body in the HTTP request.
            headers (Optional[Mapping[str, str]]): Request headers.
            max_allowed_time (float): Total execution timeout in seconds.
            timeout (Union[float, aiohttp.ClientTimeout]): Individual request timeout in seconds.
            total_attempts (Optional[int]): Maximum number of retry attempts.
            **kwargs: Additional keyword arguments passed to the underlying request transport.

        Returns:
            google.auth.aio.transport.Response: The HTTP response.

        Raises:
            google.auth.exceptions.TimeoutError: If the operation exceeds `max_allowed_time`
                or an individual request attempt exceeds `timeout`.
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
                reconfiguration fails for any reason during certificate rotation.
        """
        return await self.request(
            "PATCH",
            url,
            data=data,
            headers=headers,
            max_allowed_time=max_allowed_time,
            timeout=timeout,
            total_attempts=total_attempts,
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
        """Make an authenticated asynchronous DELETE request.

        Args:
            url (str): The URI to be requested.
            data (Optional[bytes]): The payload or body in the HTTP request.
            headers (Optional[Mapping[str, str]]): Request headers.
            max_allowed_time (float): Total execution timeout in seconds.
            timeout (Union[float, aiohttp.ClientTimeout]): Individual request timeout in seconds.
            total_attempts (Optional[int]): Maximum number of retry attempts.
            **kwargs: Additional keyword arguments passed to the underlying request transport.

        Returns:
            google.auth.aio.transport.Response: The HTTP response.

        Raises:
            google.auth.exceptions.TimeoutError: If the operation exceeds `max_allowed_time`
                or an individual request attempt exceeds `timeout`.
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
                reconfiguration fails for any reason during certificate rotation.
        """
        return await self.request(
            "DELETE",
            url,
            data=data,
            headers=headers,
            max_allowed_time=max_allowed_time,
            timeout=timeout,
            total_attempts=total_attempts,
            **kwargs,
        )

    @property
    def is_mtls(self):
        """Indicates if mutual TLS is enabled."""
        return self._is_mtls

    async def close(self) -> None:
        """Close the underlying auth request session and drain any retained mTLS transports."""
        try:
            if self._mtls_init_task and not self._mtls_init_task.done():
                self._mtls_init_task.cancel()
                try:
                    await self._mtls_init_task
                except (Exception, asyncio.CancelledError):
                    pass
            if hasattr(self._auth_request, "close"):
                res = self._auth_request.close()
                if inspect.isawaitable(res):
                    await res
        finally:
            for old_request in self._old_auth_requests:
                try:
                    if hasattr(old_request, "close"):
                        res = old_request.close()
                        if inspect.isawaitable(res):
                            await res
                except Exception:
                    pass
            self._old_auth_requests.clear()
