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

"""Transport adapter for urllib3."""

from __future__ import absolute_import

import http.client as http_client
import logging
import threading
import warnings

# Certifi is Mozilla's certificate bundle. Urllib3 needs a certificate bundle
# to verify HTTPS requests, and certifi is the recommended and most reliable
# way to get a root certificate bundle. See
# http://urllib3.readthedocs.io/en/latest/user-guide.html\
#   #certificate-verification
# For more details.
try:
    import certifi
except ImportError:  # pragma: NO COVER
    certifi = None  # type: ignore

try:
    import urllib3  # type: ignore
    import urllib3.exceptions  # type: ignore
    from packaging import version  # type: ignore
except ImportError as caught_exc:  # pragma: NO COVER
    raise ImportError(
        ""
        f"Error: {caught_exc}."
        " The 'google-auth' library requires the extras installed "
        "for urllib3 network transport."
        "\n"
        "Please install the necessary dependencies using pip:\n"
        "  pip install google-auth[urllib3]\n"
        "\n"
        "(Note: Using '[urllib3]' ensures the specific dependencies needed for this feature are installed. "
        "We recommend running this command in your virtual environment.)"
    ) from caught_exc


from google.auth import _helpers
from google.auth import exceptions
from google.auth import transport
from google.auth.transport import _mtls_helper
from google.oauth2 import service_account

if version.parse(urllib3.__version__) >= version.parse("2.0.0"):  # pragma: NO COVER
    RequestMethods = urllib3._request_methods.RequestMethods  # type: ignore
else:  # pragma: NO COVER
    RequestMethods = urllib3.request.RequestMethods  # type: ignore

_LOGGER = logging.getLogger(__name__)


class _Response(transport.Response):
    """urllib3 transport response adapter.

    Args:
        response (urllib3.response.HTTPResponse): The raw urllib3 response.
    """

    def __init__(self, response):
        self._response = response

    @property
    def status(self):
        return self._response.status

    @property
    def headers(self):
        return self._response.headers

    @property
    def data(self):
        return self._response.data


class Request(transport.Request):
    """urllib3 request adapter.

    This class is used internally for making requests using various transports
    in a consistent way. If you use :class:`AuthorizedHttp` you do not need
    to construct or use this class directly.

    This class can be useful if you want to manually refresh a
    :class:`~google.auth.credentials.Credentials` instance::

        import google.auth.transport.urllib3
        import urllib3

        http = urllib3.PoolManager()
        request = google.auth.transport.urllib3.Request(http)

        credentials.refresh(request)

    Args:
        http (urllib3.PoolManager): An instance of a urllib3 class that implements
            the request interface (e.g. :class:`urllib3.PoolManager`).

    .. automethod:: __call__
    """

    def __init__(self, http):
        self.http = http
        # The PoolManager this Request created for mTLS endpoints. Stays None if
        # self.http was already configured for mTLS externally.
        self._mtls_http = None
        self._cached_cert = None
        self._mtls_lock = threading.RLock()

    def close(self):
        """Close the underlying mTLS PoolManager if one was created."""
        # Guard against partially initialized instances when called from __del__.
        if not hasattr(self, "_mtls_lock"):
            return

        # Detach the pool and reset state under the lock before clearing so
        # concurrent requests do not use a closing pool.
        with self._mtls_lock:
            old_mtls_http = self._mtls_http
            self._mtls_http = None
            self._cached_cert = None

        if old_mtls_http is not None:
            old_mtls_http.clear()

    def __del__(self):
        try:
            self.close()
        except Exception:
            # During interpreter shutdown, Python may clear module globals (like
            # queue.Empty inside urllib3) to None before __del__ runs, causing
            # pool cleanup to raise TypeError or AttributeError.
            pass

    def _get_http_for_url(
        self, url, force_reconfigure=False, client_cert_callback=None
    ):
        """Returns the appropriate urllib3 PoolManager for the target URL.

        For standard non-mTLS URLs or when client certificates are disabled, returns
        self.http. For .mtls. endpoints, lazily creates and caches a dedicated mutual TLS
        PoolManager (self._mtls_http) so standard traffic on self.http is unaffected.

        Args:
            url (str): The target request URL.
            force_reconfigure (bool): If True, rebuilds the mTLS pool even if already
                configured.
            client_cert_callback (Optional[Callable[[], Tuple[bytes, bytes]]]): Optional
                callback returning (cert_bytes, key_bytes) in PEM format.

        Returns:
            urllib3.PoolManager: The connection pool manager to use for the request.
        """
        # If self.http already has mTLS configured (e.g. via AuthorizedHttp),
        # leave it untouched and use self.http directly.
        if getattr(self.http, "_is_mtls", False):
            return self.http
        if not _mtls_helper.is_mtls_endpoint(url):
            return self.http
        if not _mtls_helper.check_use_client_cert():
            return self.http

        if not force_reconfigure and self._mtls_http is not None:
            return self._mtls_http

        with self._mtls_lock:
            # Re-check in case another thread created the mTLS pool while waiting on the lock.
            if not force_reconfigure and self._mtls_http is not None:
                return self._mtls_http

            has_cert, cert, key = _mtls_helper.get_client_cert_and_key(
                client_cert_callback
            )
            if not has_cert:
                return self.http

            # Copy necessary configuration from self.http so existing pool settings
            # carry over to the mTLS pool manager.
            kwargs = {}
            if hasattr(self.http, "connection_pool_kw"):
                for pool_key in ("retries", "maxsize", "block", "timeout"):
                    if pool_key in self.http.connection_pool_kw:
                        kwargs[pool_key] = self.http.connection_pool_kw[pool_key]
            if getattr(self.http, "headers", None):
                kwargs["headers"] = dict(self.http.headers)
            if hasattr(getattr(self.http, "pools", None), "_maxsize"):
                kwargs["num_pools"] = self.http.pools._maxsize
            old_mtls_http = self._mtls_http
            self._mtls_http = _make_mutual_tls_http(cert, key, **kwargs)
            self._cached_cert = cert
            if old_mtls_http is not None:
                # PoolManager.clear() drops cached HTTPConnectionPool references so idle
                # sockets are closed without interrupting in-flight or streaming requests.
                old_mtls_http.clear()

            return self._mtls_http

    def _handle_mtls_unauthorized_response(self, url, used_cert):
        """Handles a 401 Unauthorized response from an mTLS endpoint.

        Checks whether the client certificate on disk has rotated since
        ``used_cert`` was cached, and reconfigures the mTLS pool manager if so.

        Args:
            url (str): The target request URL that returned 401.
            used_cert (bytes): The client certificate bytes used for the
                failed request.

        Returns:
            bool: True if the mTLS pool manager was reconfigured (by this thread
                or a concurrent thread) and the request should be retried.
        """
        with self._mtls_lock:
            if self._cached_cert != used_cert:
                return True

            try:
                (
                    call_cert_bytes,
                    call_key_bytes,
                    cached_fp,
                    current_fp,
                ) = _mtls_helper.check_parameters_for_unauthorized_response(
                    self._cached_cert
                )
                if cached_fp == current_fp:
                    return False

                _LOGGER.info(
                    "Client certificate has changed, reconfiguring mTLS pool manager."
                )
                self._get_http_for_url(
                    url,
                    force_reconfigure=True,
                    client_cert_callback=lambda: (call_cert_bytes, call_key_bytes),
                )
            except Exception as exc:
                _LOGGER.debug(
                    "Failed to reconfigure mTLS pool manager on 401 response: %s",
                    exc,
                )
                return False

            return self._cached_cert != used_cert

    def _should_retry_closed_pool(self, used_cert):
        """Checks whether a ClosedPoolError should be retried on the new mTLS pool.

        Args:
            used_cert (Optional[bytes]): The client certificate bytes used for
                the failed request.

        Returns:
            bool: True if this request used an mTLS certificate and a concurrent
                thread reconfigured the mTLS pool with a new certificate while
                this request was in flight.
        """
        return used_cert is not None and self._cached_cert != used_cert

    def __call__(
        self, url, method="GET", body=None, headers=None, timeout=None, **kwargs
    ):
        """Make an HTTP request using urllib3.

        Args:
            url (str): The URI to be requested.
            method (str): The HTTP method to use for the request. Defaults
                to 'GET'.
            body (bytes): The payload / body in HTTP request.
            headers (Mapping[str, str]): Request headers.
            timeout (Optional[int]): The number of seconds to wait for a
                response from the server. If not specified or if None, the
                urllib3 default timeout will be used.
            kwargs: Additional arguments passed throught to the underlying
                urllib3 :meth:`urlopen` method.

        Returns:
            google.auth.transport.Response: The HTTP response.

        Raises:
            google.auth.exceptions.TransportError: If any exception occurred.
        """
        # urllib3 uses a sentinel default value for timeout, so only set it if
        # specified.
        if timeout is not None:
            kwargs["timeout"] = timeout

        try:
            http_client_pool = self._get_http_for_url(url)
            # Snapshot the active cert before the network call in case another
            # thread reconfigures mTLS mid-flight.
            used_cert = (
                self._cached_cert if http_client_pool is self._mtls_http else None
            )
            _helpers.request_log(_LOGGER, method, url, body, headers)
            try:
                response = http_client_pool.request(
                    method, url, body=body, headers=headers, **kwargs
                )
            except urllib3.exceptions.ClosedPoolError:
                if not self._should_retry_closed_pool(used_cert):
                    raise
                used_cert = self._cached_cert
                _helpers.request_log(_LOGGER, method, url, body, headers)
                response = self._mtls_http.request(
                    method, url, body=body, headers=headers, **kwargs
                )
            _helpers.response_log(_LOGGER, response)

            if (
                response.status == http_client.UNAUTHORIZED
                and used_cert is not None
                and _mtls_helper.is_mtls_endpoint(url)
                and self._handle_mtls_unauthorized_response(url, used_cert)
            ):
                _helpers.request_log(_LOGGER, method, url, body, headers)
                response = self._mtls_http.request(
                    method, url, body=body, headers=headers, **kwargs
                )
                _helpers.response_log(_LOGGER, response)

            return _Response(response)
        except urllib3.exceptions.HTTPError as caught_exc:
            new_exc = exceptions.TransportError(caught_exc)
            raise new_exc from caught_exc


def _make_default_http():
    if certifi is not None:
        return urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    else:
        return urllib3.PoolManager()


def _make_mutual_tls_http(cert, key, **kwargs):
    """Create a mutual TLS HTTP connection with the given client cert and key.
    See https://github.com/urllib3/urllib3/issues/474#issuecomment-253168415

    Args:
        cert (bytes): client certificate in PEM format
        key (bytes): client private key in PEM format
        kwargs: Additional keyword arguments passed to the
            :class:`urllib3.PoolManager` constructor.

    Returns:
        urllib3.PoolManager: Mutual TLS HTTP connection.

    Raises:
        google.auth.exceptions.MutualTLSChannelError: If the cert or key is invalid.
    """
    import certifi
    import ssl

    ctx = urllib3.util.ssl_.create_urllib3_context()
    ctx.load_verify_locations(cafile=certifi.where())

    try:
        with _mtls_helper.secure_cert_key_paths(cert, key) as (
            cert_path,
            key_path,
            passphrase,
        ):
            password = passphrase
            ctx.load_cert_chain(
                certfile=cert_path,
                keyfile=key_path,
                password=password,
            )
    except (ssl.SSLError, OSError, IOError, ValueError, RuntimeError, TypeError) as exc:
        raise exceptions.MutualTLSChannelError(
            "Failed to configure client certificate and key for mTLS."
        ) from exc

    http = urllib3.PoolManager(ssl_context=ctx, **kwargs)
    http._is_mtls = True
    return http


class AuthorizedHttp(RequestMethods):  # type: ignore
    """A urllib3 HTTP class with credentials.

    This class is used to perform requests to API endpoints that require
    authorization::

        from google.auth.transport.urllib3 import AuthorizedHttp

        authed_http = AuthorizedHttp(credentials)

        response = authed_http.request(
            'GET', 'https://www.googleapis.com/storage/v1/b')

    This class implements the urllib3 request interface and can be
    used just like any other :class:`urllib3.PoolManager`.

    The underlying :meth:`urlopen` implementation handles adding the
    credentials' headers to the request and refreshing credentials as needed.

    This class also supports mutual TLS via :meth:`configure_mtls_channel`
    method. In order to use this method, the `GOOGLE_API_USE_CLIENT_CERTIFICATE`
    environment variable must be explicitly set to `true`, otherwise it does
    nothing. Assume the environment is set to `true`, the method behaves in the
    following manner:
    If client_cert_callback is provided, client certificate and private
    key are loaded using the callback; if client_cert_callback is None,
    application default SSL credentials will be used. Exceptions are raised if
    there are problems with the certificate, private key, or the loading process,
    so it should be called within a try/except block.

    First we set the environment variable to `true`, then create an :class:`AuthorizedHttp`
    instance and specify the endpoints::

        regular_endpoint = 'https://pubsub.googleapis.com/v1/projects/{my_project_id}/topics'
        mtls_endpoint = 'https://pubsub.mtls.googleapis.com/v1/projects/{my_project_id}/topics'

        authed_http = AuthorizedHttp(credentials)

    Now we can pass a callback to :meth:`configure_mtls_channel`::

        def my_cert_callback():
            # some code to load client cert bytes and private key bytes, both in
            # PEM format.
            some_code_to_load_client_cert_and_key()
            if loaded:
                return cert, key
            raise MyClientCertFailureException()

        # Always call configure_mtls_channel within a try/except block.
        try:
            is_mtls = authed_http.configure_mtls_channel(my_cert_callback)
        except:
            # handle exceptions.

        if is_mtls:
            response = authed_http.request('GET', mtls_endpoint)
        else:
            response = authed_http.request('GET', regular_endpoint)

    You can alternatively use application default SSL credentials like this::

        try:
            is_mtls = authed_http.configure_mtls_channel()
        except:
            # handle exceptions.

    Args:
        credentials (google.auth.credentials.Credentials): The credentials to
            add to the request.
        http (urllib3.PoolManager): The underlying HTTP object to
            use to make requests. If not specified, a
            :class:`urllib3.PoolManager` instance will be constructed with
            sane defaults.
        refresh_status_codes (Sequence[int]): Which HTTP status codes indicate
            that credentials should be refreshed and the request should be
            retried.
        max_refresh_attempts (int): The maximum number of times to attempt to
            refresh the credentials and retry the request.
        default_host (Optional[str]): A host like "pubsub.googleapis.com".
            This is used when a self-signed JWT is created from service
            account credentials.
    """

    def __init__(
        self,
        credentials,
        http=None,
        refresh_status_codes=transport.DEFAULT_REFRESH_STATUS_CODES,
        max_refresh_attempts=transport.DEFAULT_MAX_REFRESH_ATTEMPTS,
        default_host=None,
    ):
        if http is None:
            self.http = _make_default_http()
            self._has_user_provided_http = False
        else:
            self.http = http
            self._has_user_provided_http = True

        self.credentials = credentials
        self._refresh_status_codes = refresh_status_codes
        self._max_refresh_attempts = max_refresh_attempts
        self._default_host = default_host
        # Request instance used by internal methods (for example,
        # credentials.refresh).
        self._request = Request(self.http)
        self._is_mtls = False

        # https://google.aip.dev/auth/4111
        # Attempt to use self-signed JWTs when a service account is used.
        if isinstance(self.credentials, service_account.Credentials):
            self.credentials._create_self_signed_jwt(
                "https://{}/".format(self._default_host) if self._default_host else None
            )

        super(AuthorizedHttp, self).__init__()

    def configure_mtls_channel(self, client_cert_callback=None):
        """Configures mutual TLS channel using the given client_cert_callback or
        application default SSL credentials.

        The channel is configured if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true",
        or if it is unset and workload certificates are detected in the environment.
        If client_cert_callback is None, default SSL credentials (workload or SecureConnect)
        are loaded.

        Args:
            client_cert_callback (Optional[Callable[[], (bytes, bytes)]]):
                The optional callback returns the client certificate and private
                key bytes both in PEM format.
                If the callback is None, application default SSL credentials
                will be used.

        .. warning::
            Calling this method mutates the underlying `urllib3.PoolManager`.
            It is not thread-safe to call this explicitly while other
            threads are making requests.

        Returns:
            True if the channel is mutual TLS and False otherwise.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
                creation failed for any reason. The existing channel state (the
                HTTP client) remains unmodified if this error is raised.
        """
        use_client_cert = transport._mtls_helper.check_use_client_cert()
        if not use_client_cert:
            return False

        try:
            found_cert_key, cert, key = transport._mtls_helper.get_client_cert_and_key(
                client_cert_callback
            )

            if found_cert_key:
                new_http = _make_mutual_tls_http(cert, key)
                new_is_mtls = True
            else:
                new_http = _make_default_http()
                new_is_mtls = False
        except (
            exceptions.ClientCertError,
            ImportError,
            OSError,
            ValueError,
        ) as caught_exc:
            new_exc = exceptions.MutualTLSChannelError(caught_exc)
            raise new_exc from caught_exc

        old_http = self.http

        self.http = new_http
        self._is_mtls = new_is_mtls
        self._request.http = new_http

        if old_http is not None and old_http is not new_http:
            getattr(old_http, "clear", getattr(old_http, "close", lambda: None))()

        if new_is_mtls:
            self._cached_cert = cert
        else:
            if hasattr(self, "_cached_cert"):
                del self._cached_cert

        if self._has_user_provided_http:
            self._has_user_provided_http = False
            warnings.warn(
                "`http` provided in the constructor is overwritten", UserWarning
            )

        return found_cert_key

    def urlopen(self, method, url, body=None, headers=None, **kwargs):
        """Implementation of urllib3's urlopen."""
        # pylint: disable=arguments-differ
        # We use kwargs to collect additional args that we don't need to
        # introspect here. However, we do explicitly collect the two
        # positional arguments.

        # Use a kwarg for this instead of an attribute to maintain
        # thread-safety.
        _credential_refresh_attempt = kwargs.pop("_credential_refresh_attempt", 0)

        if headers is None:
            headers = self.headers

        # Make a copy of the headers. They will be modified by the credentials
        # and we want to pass the original headers if we recurse.
        request_headers = headers.copy()

        self.credentials.before_request(self._request, method, url, request_headers)

        response = self.http.urlopen(
            method, url, body=body, headers=request_headers, **kwargs
        )

        # If the response indicated that the credentials needed to be
        # refreshed, then refresh the credentials and re-attempt the
        # request.
        # A stored token may expire between the time it is retrieved and
        # the time the request is made, so we may need to try twice.
        # The reason urllib3's retries aren't used is because they
        # don't allow you to modify the request headers. :/
        if (
            response.status in self._refresh_status_codes
            and _credential_refresh_attempt < self._max_refresh_attempts
        ):
            if response.status == http_client.UNAUTHORIZED:
                use_mtls = self._is_mtls and _mtls_helper.is_mtls_endpoint(url)
                if use_mtls:
                    (
                        call_cert_bytes,
                        call_key_bytes,
                        cached_fingerprint,
                        current_cert_fingerprint,
                    ) = _mtls_helper.check_parameters_for_unauthorized_response(
                        self._cached_cert
                    )
                    if cached_fingerprint != current_cert_fingerprint:
                        try:
                            _LOGGER.info(
                                "Client certificate has changed, reconfiguring mTLS "
                                "channel."
                            )
                            self.configure_mtls_channel(
                                client_cert_callback=lambda: (
                                    call_cert_bytes,
                                    call_key_bytes,
                                )
                            )
                        except Exception as e:
                            _LOGGER.error("Failed to reconfigure mTLS channel: %s", e)
                            raise exceptions.MutualTLSChannelError(
                                "Failed to reconfigure mTLS channel"
                            ) from e

                    else:
                        _LOGGER.info(
                            "Skipping reconfiguration of mTLS channel because the "
                            "client certificate has not changed."
                        )

            _LOGGER.info(
                "Refreshing credentials due to a %s response. Attempt %s/%s.",
                response.status,
                _credential_refresh_attempt + 1,
                self._max_refresh_attempts,
            )

            self.credentials.refresh(self._request)

            # Recurse. Pass in the original headers, not our modified set.
            return self.urlopen(
                method,
                url,
                body=body,
                headers=headers,
                _credential_refresh_attempt=_credential_refresh_attempt + 1,
                **kwargs,
            )

        return response

    # Proxy methods for compliance with the urllib3.PoolManager interface

    def __enter__(self):
        """Proxy to ``self.http``."""
        return self.http.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Proxy to ``self.http``."""
        return self.http.__exit__(exc_type, exc_val, exc_tb)

    def __del__(self):
        if hasattr(self, "http") and self.http is not None:
            getattr(self.http, "clear", getattr(self.http, "close", lambda: None))()

    @property
    def headers(self):
        """Proxy to ``self.http``."""
        return self.http.headers

    @headers.setter
    def headers(self, value):
        """Proxy to ``self.http``."""
        self.http.headers = value
