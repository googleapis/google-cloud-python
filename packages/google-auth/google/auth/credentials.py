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


"""Interfaces for credentials."""

import abc
from enum import Enum
import logging
import os
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING: # pragma: NO COVER
    import google.auth.transport
from urllib.parse import urlparse

from google.auth import _helpers, environment_vars
from google.auth import _regional_access_boundary_utils
from google.auth import exceptions
from google.auth import metrics
from google.auth._credentials_base import _BaseCredentials
from google.auth._refresh_worker import RefreshThreadManager

DEFAULT_UNIVERSE_DOMAIN = "googleapis.com"

# These constants are deprecated and no longer used.
# They are kept solely for backward compatibility with older implementations.
NO_OP_TRUST_BOUNDARY_LOCATIONS: List[str] = []
NO_OP_TRUST_BOUNDARY_ENCODED_LOCATIONS = "0x0"

_LOGGER = logging.getLogger("google.auth._default")


class Credentials(_BaseCredentials):
    """Base class for all credentials.

    All credentials have a :attr:`token` that is used for authentication and
    may also optionally set an :attr:`expiry` to indicate when the token will
    no longer be valid.

    Most credentials will be :attr:`invalid` until :meth:`refresh` is called.
    Credentials can do this automatically before the first HTTP request in
    :meth:`before_request`.

    Although the token and expiration will change as the credentials are
    :meth:`refreshed <refresh>` and used, credentials should be considered
    immutable. Various credentials will accept configuration such as private
    keys, scopes, and other options. These options are not changeable after
    construction. Some classes will provide mechanisms to copy the credentials
    with modifications such as :meth:`ScopedCredentials.with_scopes`.
    """

    def __init__(self):
        super(Credentials, self).__init__()

        self.expiry = None
        """Optional[datetime]: When the token expires and is no longer valid.
        If this is None, the token is assumed to never expire."""
        self._quota_project_id = None
        """Optional[str]: Project to use for quota and billing purposes."""
        self._trust_boundary = None
        """Optional[dict]: Cache of a trust boundary response which has a list
        of allowed regions and an encoded string representation of credentials
        trust boundary."""
        self._universe_domain = DEFAULT_UNIVERSE_DOMAIN
        """Optional[str]: The universe domain value, default is googleapis.com
        """

        self._use_non_blocking_refresh = False
        self._refresh_worker = RefreshThreadManager()

    @property
    def expired(self):
        """Checks if the credentials are expired.

        Note that credentials can be invalid but not expired because
        Credentials with :attr:`expiry` set to None is considered to never
        expire.

        .. deprecated:: v2.24.0
          Prefer checking :attr:`token_state` instead.
        """
        if not self.expiry:
            return False
        # Remove some threshold from expiry to err on the side of reporting
        # expiration early so that we avoid the 401-refresh-retry loop.
        skewed_expiry = self.expiry - _helpers.REFRESH_THRESHOLD
        return _helpers.utcnow() >= skewed_expiry

    @property
    def valid(self):
        """Checks the validity of the credentials.

        This is True if the credentials have a :attr:`token` and the token
        is not :attr:`expired`.

        .. deprecated:: v2.24.0
          Prefer checking :attr:`token_state` instead.
        """
        return self.token is not None and not self.expired

    @property
    def token_state(self):
        """
        See `:obj:`TokenState`
        """
        if self.token is None:
            return TokenState.INVALID

        # Credentials that can't expire are always treated as fresh.
        if self.expiry is None:
            return TokenState.FRESH

        expired = _helpers.utcnow() >= self.expiry
        if expired:
            return TokenState.INVALID

        is_stale = _helpers.utcnow() >= (self.expiry - _helpers.REFRESH_THRESHOLD)
        if is_stale:
            return TokenState.STALE

        return TokenState.FRESH

    @property
    def quota_project_id(self):
        """Project to use for quota and billing purposes."""
        return self._quota_project_id

    @property
    def universe_domain(self):
        """The universe domain value."""
        return self._universe_domain

    def get_cred_info(self):
        """The credential information JSON.

        The credential information will be added to auth related error messages
        by client library.

        Returns:
            Mapping[str, str]: The credential information JSON.
        """
        return None

    @abc.abstractmethod
    def refresh(self, request):
        """Refreshes the access token.

        Args:
            request (google.auth.transport.Request): The object used to make
                HTTP requests.

        Raises:
            google.auth.exceptions.RefreshError: If the credentials could
                not be refreshed.
        """
        # pylint: disable=missing-raises-doc
        # (pylint doesn't recognize that this is abstract)
        raise NotImplementedError("Refresh must be implemented")

    def _metric_header_for_usage(self):
        """The x-goog-api-client header for token usage metric.

        This header will be added to the API service requests in before_request
        method. For example, "cred-type/sa-jwt" means service account self
        signed jwt access token is used in the API service request
        authorization header. Children credentials classes need to override
        this method to provide the header value, if the token usage metric is
        needed.

        Returns:
            str: The x-goog-api-client header value.
        """
        return None

    def apply(self, headers, token=None):
        """Apply the token to the authentication header.

        Args:
            headers (Mapping): The HTTP request headers.
            token (Optional[str]): If specified, overrides the current access
                token.
        """
        self._apply(headers, token)
        if self.quota_project_id:
            headers["x-goog-user-project"] = self.quota_project_id

    def _blocking_refresh(self, request):
        if not self.valid:
            self.refresh(request)

    def _non_blocking_refresh(self, request):
        use_blocking_refresh_fallback = False

        if self.token_state == TokenState.STALE:
            use_blocking_refresh_fallback = not self._refresh_worker.start_refresh(
                self, request
            )

        if self.token_state == TokenState.INVALID or use_blocking_refresh_fallback:
            self.refresh(request)
            # If the blocking refresh succeeds then we can clear the error info
            # on the background refresh worker, and perform refreshes in a
            # background thread.
            self._refresh_worker.clear_error()

    def before_request(self, request, method, url, headers):
        """Performs credential-specific before request logic.

        Refreshes the credentials if necessary, then calls :meth:`apply` to
        apply the token to the authentication header.

        Args:
            request (google.auth.transport.Request): The object used to make
                HTTP requests.
            method (str): The request's HTTP method or the RPC method being
                invoked.
            url (str): The request's URI or the RPC service's URI.
            headers (Mapping): The request's headers.
        """
        # pylint: disable=unused-argument
        # (Subclasses may use these arguments to ascertain information about
        # the http request.)
        if self._use_non_blocking_refresh:
            self._non_blocking_refresh(request)
        else:
            self._blocking_refresh(request)

        metrics.add_metric_header(headers, self._metric_header_for_usage())
        self.apply(headers)

    def with_non_blocking_refresh(self):
        self._use_non_blocking_refresh = True


class CredentialsWithQuotaProject(Credentials):
    """Abstract base for credentials supporting ``with_quota_project`` factory"""

    def with_quota_project(self, quota_project_id):
        """Returns a copy of these credentials with a modified quota project.

        Args:
            quota_project_id (str): The project to use for quota and
                billing purposes

        Returns:
            google.auth.credentials.Credentials: A new credentials instance.
        """
        raise NotImplementedError("This credential does not support quota project.")

    def with_quota_project_from_environment(self):
        quota_from_env = os.environ.get(environment_vars.GOOGLE_CLOUD_QUOTA_PROJECT)
        if quota_from_env:
            return self.with_quota_project(quota_from_env)
        return self


class CredentialsWithTokenUri(Credentials):
    """Abstract base for credentials supporting ``with_token_uri`` factory"""

    def with_token_uri(self, token_uri):
        """Returns a copy of these credentials with a modified token uri.

        Args:
            token_uri (str): The uri to use for fetching/exchanging tokens

        Returns:
            google.auth.credentials.Credentials: A new credentials instance.
        """
        raise NotImplementedError("This credential does not use token uri.")


class CredentialsWithUniverseDomain(Credentials):
    """Abstract base for credentials supporting ``with_universe_domain`` factory"""

    def with_universe_domain(self, universe_domain):
        """Returns a copy of these credentials with a modified universe domain.

        Args:
            universe_domain (str): The universe domain to use

        Returns:
            google.auth.credentials.Credentials: A new credentials instance.
        """
        raise NotImplementedError(
            "This credential does not support with_universe_domain."
        )


class CredentialsWithRegionalAccessBoundary(Credentials):
    """Abstract base for credentials supporting regional access boundary configuration."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rab_manager = (
            _regional_access_boundary_utils._RegionalAccessBoundaryManager()
        )

    @abc.abstractmethod
    def _perform_refresh_token(self, request):
        """Refreshes the access token.

        Args:
            request (google.auth.transport.Request): The object used to make
                HTTP requests.

        Raises:
            google.auth.exceptions.RefreshError: If the credentials could
                not be refreshed.
        """
        raise NotImplementedError("_perform_refresh_token must be implemented")

    def with_trust_boundary(self, trust_boundary):
        """Returns a copy of these credentials.

        .. deprecated::
            Manual Regional Access Boundary overrides are not supported.
            This method is maintained for backwards compatibility and
            returns a copy of the credentials without modifying the
            Regional Access Boundary state.

        Args:
            trust_boundary (Mapping[str, str]): Ignored.

        Returns:
            google.auth.credentials.Credentials: A new credentials instance.
        """
        import warnings

        warnings.warn(
            "with_trust_boundary is deprecated and has no effect.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._make_copy()

    def _copy_regional_access_boundary_manager(self, target):
        """Copies the regional access boundary manager to another instance."""
        target._rab_manager = self._rab_manager

    def _maybe_start_regional_access_boundary_refresh(self, request, url):
        """
        Starts a background thread to refresh the Regional Access Boundary if needed.

        This method checks if a refresh is necessary and if one is not already
        in progress or in a cooldown period. If so, it starts a background
        thread to perform the lookup.

        Args:
            request (google.auth.transport.Request): The object used to make
                HTTP requests.
            url (str): The URL of the request.
        """
        try:
            # Do not perform a lookup if the request is for a regional endpoint.
            hostname = urlparse(url).hostname
            if hostname and (
                hostname.endswith(".rep.googleapis.com")
                or hostname.endswith(".rep.sandbox.googleapis.com")
            ):
                return
        except (ValueError, TypeError):
            # If the URL is malformed, proceed with the default lookup behavior.
            pass

        # A refresh is only needed if the feature is enabled.
        if not self._is_regional_access_boundary_lookup_required():
            return

        # Start the background refresh if needed.
        self._rab_manager.maybe_start_refresh(self, request)

    def _is_regional_access_boundary_lookup_required(self):
        """Checks if a Regional Access Boundary lookup is required.

        A lookup is required if the feature is enabled via an environment
        variable and the universe domain is supported.

        Returns:
            bool: True if a Regional Access Boundary lookup is required, False otherwise.
        """
        # 1. Check if the feature is enabled.
        if not _regional_access_boundary_utils.is_regional_access_boundary_enabled():
            return False

        # 2. Skip for non-default universe domains.
        if self.universe_domain != DEFAULT_UNIVERSE_DOMAIN:
            return False

        return True

    def apply(self, headers, token=None):
        """Apply the token to the authentication header."""
        super().apply(headers, token)
        self._rab_manager.apply_headers(headers)

    def before_request(self, request, method, url, headers):
        """Refreshes the access token and triggers the Regional Access Boundary
        lookup if necessary.
        """
        super(CredentialsWithRegionalAccessBoundary, self).before_request(
            request, method, url, headers
        )
        self._maybe_start_regional_access_boundary_refresh(request, url)

    def refresh(self, request):
        """Refreshes the access token.

        This method calls the subclass's token refresh logic. The Regional
        Access Boundary is refreshed separately in a non-blocking way.
        """
        self._perform_refresh_token(request)

    def _lookup_regional_access_boundary(
        self, request: "google.auth.transport.Request"  # noqa: F821
    ) -> "Optional[Dict[str, str]]":
        """Calls the Regional Access Boundary lookup API to retrieve the Regional Access Boundary information.

        Args:
            request (google.auth.transport.Request): The object used to make
                HTTP requests.

        Returns:
            Optional[Dict[str, str]]: The Regional Access Boundary information returned by the lookup API, or None if the lookup failed.
        """
        from google.oauth2 import _client

        url = self._build_regional_access_boundary_lookup_url(request=request)
        if not url:
            _LOGGER.error("Failed to build Regional Access Boundary lookup URL.")
            return None

        headers: Dict[str, str] = {}
        self._apply(headers)
        self._rab_manager.apply_headers(headers)
        return _client._lookup_regional_access_boundary(request, url, headers=headers)

    @abc.abstractmethod
    def _build_regional_access_boundary_lookup_url(
        self, request: "Optional[google.auth.transport.Request]" = None  # noqa: F821
    ):
        """
        Builds and returns the URL for the Regional Access Boundary lookup API.

        This method should be implemented by subclasses to provide the
        specific URL based on the credential type and its properties.

        Args:
            request (Optional[google.auth.transport.Request]): The object used
                to make HTTP requests. In some subclasses, this may be used to
                make an initial network call to resolve required metadata for the
                URL.

        Returns:
            str: The URL for the Regional Access Boundary lookup endpoint, or None
                 if lookup should be skipped (e.g., for non-applicable universe domains).
        """
        raise NotImplementedError(
            "_build_regional_access_boundary_lookup_url must be implemented"
        )


class AnonymousCredentials(Credentials):
    """Credentials that do not provide any authentication information.

    These are useful in the case of services that support anonymous access or
    local service emulators that do not use credentials.
    """

    @property
    def expired(self):
        """Returns `False`, anonymous credentials never expire."""
        return False

    @property
    def valid(self):
        """Returns `True`, anonymous credentials are always valid."""
        return True

    def refresh(self, request):
        """Raises :class:``InvalidOperation``, anonymous credentials cannot be
        refreshed."""
        raise exceptions.InvalidOperation("Anonymous credentials cannot be refreshed.")

    def apply(self, headers, token=None):
        """Anonymous credentials do nothing to the request.

        The optional ``token`` argument is not supported.

        Raises:
            google.auth.exceptions.InvalidValue: If a token was specified.
        """
        if token is not None:
            raise exceptions.InvalidValue("Anonymous credentials don't support tokens.")

    def before_request(self, request, method, url, headers):
        """Anonymous credentials do nothing to the request."""


class ReadOnlyScoped(metaclass=abc.ABCMeta):
    """Interface for credentials whose scopes can be queried.

    OAuth 2.0-based credentials allow limiting access using scopes as described
    in `RFC6749 Section 3.3`_.
    If a credential class implements this interface then the credentials either
    use scopes in their implementation.

    Some credentials require scopes in order to obtain a token. You can check
    if scoping is necessary with :attr:`requires_scopes`::

        if credentials.requires_scopes:
            # Scoping is required.
            credentials = credentials.with_scopes(scopes=['one', 'two'])

    Credentials that require scopes must either be constructed with scopes::

        credentials = SomeScopedCredentials(scopes=['one', 'two'])

    Or must copy an existing instance using :meth:`with_scopes`::

        scoped_credentials = credentials.with_scopes(scopes=['one', 'two'])

    Some credentials have scopes but do not allow or require scopes to be set,
    these credentials can be used as-is.

    .. _RFC6749 Section 3.3: https://tools.ietf.org/html/rfc6749#section-3.3
    """

    def __init__(self):
        super(ReadOnlyScoped, self).__init__()
        self._scopes = None
        self._default_scopes = None

    @property
    def scopes(self):
        """Sequence[str]: the credentials' current set of scopes."""
        return self._scopes

    @property
    def default_scopes(self):
        """Sequence[str]: the credentials' current set of default scopes."""
        return self._default_scopes

    @abc.abstractproperty
    def requires_scopes(self):
        """True if these credentials require scopes to obtain an access token."""
        return False

    def has_scopes(self, scopes):
        """Checks if the credentials have the given scopes.

        .. warning: This method is not guaranteed to be accurate if the
            credentials are :attr:`~Credentials.invalid`.

        Args:
            scopes (Sequence[str]): The list of scopes to check.

        Returns:
            bool: True if the credentials have the given scopes.
        """
        credential_scopes = (
            self._scopes if self._scopes is not None else self._default_scopes
        )
        return set(scopes).issubset(set(credential_scopes or []))


class Scoped(ReadOnlyScoped):
    """Interface for credentials whose scopes can be replaced while copying.

    OAuth 2.0-based credentials allow limiting access using scopes as described
    in `RFC6749 Section 3.3`_.
    If a credential class implements this interface then the credentials either
    use scopes in their implementation.

    Some credentials require scopes in order to obtain a token. You can check
    if scoping is necessary with :attr:`requires_scopes`::

        if credentials.requires_scopes:
            # Scoping is required.
            credentials = credentials.create_scoped(['one', 'two'])

    Credentials that require scopes must either be constructed with scopes::

        credentials = SomeScopedCredentials(scopes=['one', 'two'])

    Or must copy an existing instance using :meth:`with_scopes`::

        scoped_credentials = credentials.with_scopes(scopes=['one', 'two'])

    Some credentials have scopes but do not allow or require scopes to be set,
    these credentials can be used as-is.

    .. _RFC6749 Section 3.3: https://tools.ietf.org/html/rfc6749#section-3.3
    """

    @abc.abstractmethod
    def with_scopes(self, scopes, default_scopes=None):
        """Create a copy of these credentials with the specified scopes.

        Args:
            scopes (Sequence[str]): The list of scopes to attach to the
                current credentials.

        Raises:
            NotImplementedError: If the credentials' scopes can not be changed.
                This can be avoided by checking :attr:`requires_scopes` before
                calling this method.
        """
        raise NotImplementedError("This class does not require scoping.")


def with_scopes_if_required(credentials, scopes, default_scopes=None):
    """Creates a copy of the credentials with scopes if scoping is required.

    This helper function is useful when you do not know (or care to know) the
    specific type of credentials you are using (such as when you use
    :func:`google.auth.default`). This function will call
    :meth:`Scoped.with_scopes` if the credentials are scoped credentials and if
    the credentials require scoping. Otherwise, it will return the credentials
    as-is.

    Args:
        credentials (google.auth.credentials.Credentials): The credentials to
            scope if necessary.
        scopes (Sequence[str]): The list of scopes to use.
        default_scopes (Sequence[str]): Default scopes passed by a
            Google client library. Use 'scopes' for user-defined scopes.

    Returns:
        google.auth.credentials.Credentials: Either a new set of scoped
            credentials, or the passed in credentials instance if no scoping
            was required.
    """
    if isinstance(credentials, Scoped) and credentials.requires_scopes:
        return credentials.with_scopes(scopes, default_scopes=default_scopes)
    else:
        return credentials


class Signing(metaclass=abc.ABCMeta):
    """Interface for credentials that can cryptographically sign messages."""

    @abc.abstractmethod
    def sign_bytes(self, message):
        """Signs the given message.

        Args:
            message (bytes): The message to sign.

        Returns:
            bytes: The message's cryptographic signature.
        """
        # pylint: disable=missing-raises-doc,redundant-returns-doc
        # (pylint doesn't recognize that this is abstract)
        raise NotImplementedError("Sign bytes must be implemented.")

    @abc.abstractproperty
    def signer_email(self):
        """Optional[str]: An email address that identifies the signer."""
        # pylint: disable=missing-raises-doc
        # (pylint doesn't recognize that this is abstract)
        raise NotImplementedError("Signer email must be implemented.")

    @abc.abstractproperty
    def signer(self):
        """google.auth.crypt.Signer: The signer used to sign bytes."""
        # pylint: disable=missing-raises-doc
        # (pylint doesn't recognize that this is abstract)
        raise NotImplementedError("Signer must be implemented.")


class TokenState(Enum):
    """
    Tracks the state of a token.
    FRESH: The token is valid. It is not expired or close to expired, or the token has no expiry.
    STALE: The token is close to expired, and should be refreshed. The token can be used normally.
    INVALID: The token is expired or invalid. The token cannot be used for a normal operation.
    """

    FRESH = 1
    STALE = 2
    INVALID = 3


# For backwards compatibility with the previous feature name.
# Use CredentialsWithRegionalAccessBoundary instead.
CredentialsWithTrustBoundary = CredentialsWithRegionalAccessBoundary
