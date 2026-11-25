# Copyright 2024 Google LLC
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

"""Helpers for universe domain."""

import os
import re
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, NamedTuple, Optional, Union
from urllib.parse import urlparse, urlsplit, urlunparse

from google.auth import compute_engine
from google.auth import credentials as auth_credentials
from google.auth.exceptions import MutualTLSChannelError  # type: ignore

from google.api_core import client_options as client_options_lib

if TYPE_CHECKING:  # pragma: NO COVER
    from google.auth.aio import credentials as aio_credentials

try:
    # google.auth.aio was added in google-auth 2.28.0; older supported versions
    # (down to 2.14.1) only provide synchronous AnonymousCredentials.
    from google.auth.aio import credentials as _aio_credentials

    _ANONYMOUS_CREDENTIAL_TYPES: tuple[type[Any], ...] = (
        auth_credentials.AnonymousCredentials,
        _aio_credentials.AnonymousCredentials,
    )
except ImportError:  # pragma: NO COVER
    _ANONYMOUS_CREDENTIAL_TYPES = (auth_credentials.AnonymousCredentials,)

DEFAULT_UNIVERSE = "googleapis.com"
UNIVERSE_DOMAIN_ENV = "GOOGLE_CLOUD_UNIVERSE_DOMAIN"
_GOOGLEAPIS_HOST_PATTERN = re.compile(
    rf"^(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)*{re.escape(DEFAULT_UNIVERSE)}$",
    re.IGNORECASE,
)


class _ParsedTarget(NamedTuple):
    """Normalized components of an HTTP(S) URL or gRPC target string."""

    scheme: str
    authority: str
    host: str
    query: str


class EmptyUniverseError(ValueError):
    def __init__(self):
        message = "Universe Domain cannot be an empty string."
        super().__init__(message)


class UniverseMismatchError(ValueError):
    def __init__(self, client_universe, credentials_universe):
        message = (
            f"The configured universe domain ({client_universe}) does not match the universe domain "
            f"found in the credentials ({credentials_universe}). "
            "If you haven't configured the universe domain explicitly, "
            f"`{DEFAULT_UNIVERSE}` is the default."
        )
        super().__init__(message)


def get_universe_domain(
    *potential_universes: Optional[str],
    default_universe: str,
) -> str:
    """Return the universe domain used by the client.

    Args:
        *potential_universes (Optional[str]): Potential universe domains in order of preference.
        default_universe (str): The default universe domain.

    Returns:
        str: The universe domain to be used by the client.

    Raises:
        EmptyUniverseError: If the resolved universe domain is an empty string.
    """
    resolved = next(
        (x.strip() for x in potential_universes if x is not None),
        default_universe,
    )

    if not resolved:
        raise EmptyUniverseError()
    return resolved


def determine_domain(
    client_universe_domain: Optional[str], universe_domain_env: Optional[str]
) -> str:
    """Return the universe domain used by the client.

    Args:
        client_universe_domain (Optional[str]): The universe domain configured via the client options.
        universe_domain_env (Optional[str]): The universe domain configured via the
        "GOOGLE_CLOUD_UNIVERSE_DOMAIN" environment variable.

    Returns:
        str: The universe domain to be used by the client.

    Raises:
        ValueError: If the universe domain is an empty string.
    """
    return get_universe_domain(
        client_universe_domain,
        universe_domain_env,
        default_universe=DEFAULT_UNIVERSE,
    )


def compare_domains(client_universe: str, credentials: Any) -> bool:
    """Returns True iff the universe domains used by the client and credentials match.

    Args:
        client_universe (str): The universe domain configured via the client options.
        credentials Any: The credentials being used in the client.

    Returns:
        bool: True iff client_universe matches the universe in credentials.

    Raises:
        ValueError: when client_universe does not match the universe in credentials.
    """
    credentials_universe = getattr(credentials, "universe_domain", DEFAULT_UNIVERSE)

    if client_universe != credentials_universe:
        raise UniverseMismatchError(client_universe, credentials_universe)
    return True


def get_default_mtls_endpoint(api_endpoint: Optional[str]) -> Optional[str]:
    """Converts api endpoint to mTLS endpoint.

    Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
    "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
    Other URLs (including those that do not match these domain suffixes or
    already contain '.mtls.') are passed through as-is.

    Args:
        api_endpoint (Optional[str]): the api endpoint to convert.

    Returns:
        Optional[str]: converted mTLS api endpoint.
    """
    if not api_endpoint or ".mtls." in api_endpoint.lower():
        return api_endpoint

    has_scheme = "://" in api_endpoint
    if not has_scheme:
        parsed = urlparse("//" + api_endpoint)
    else:
        parsed = urlparse(api_endpoint)

    host = parsed.hostname
    if not host:
        return api_endpoint

    port = f":{parsed.port}" if parsed.port else ""

    lowered_host = host.lower()
    suffix_sandbox = ".sandbox.googleapis.com"
    suffix_google = ".googleapis.com"
    if lowered_host.endswith(suffix_sandbox):
        new_host = host[: -len(suffix_sandbox)] + ".mtls.sandbox.googleapis.com"
    elif lowered_host.endswith(suffix_google):
        new_host = host[: -len(suffix_google)] + ".mtls.googleapis.com"
    else:
        return api_endpoint

    netloc = new_host + port
    new_parsed = parsed._replace(netloc=netloc)

    if not has_scheme:
        return urlunparse(new_parsed)[2:]
    else:
        return urlunparse(new_parsed)


def get_api_endpoint(
    api_override: Optional[str],
    universe_domain: str,
    default_universe: str,
    default_mtls_endpoint: Optional[str],
    default_endpoint_template: str,
    use_mtls: bool,
) -> str:
    """Return the API endpoint used by the client.

    Args:
        api_override (Optional[str]): The API endpoint override. If specified,
            this is always returned.
        universe_domain (str): The universe domain used by the client.
        default_universe (str): The default universe domain.
        default_mtls_endpoint (Optional[str]): The default mTLS endpoint.
        default_endpoint_template (str): The default endpoint template containing
            a placeholder `{UNIVERSE_DOMAIN}`.
        use_mtls (bool): Whether to use the mTLS endpoint.

    Returns:
        str: The API endpoint to be used by the client.

    Raises:
        google.auth.exceptions.MutualTLSChannelError: If mTLS is requested but
            not supported in the configured universe domain.
        ValueError: If mTLS is requested but no mTLS endpoint is available.
    """
    if api_override is not None:
        return api_override

    if use_mtls:
        if universe_domain.lower() != default_universe.lower():
            raise MutualTLSChannelError(
                f"mTLS is not supported in any universe other than {default_universe}."
            )
        if not default_mtls_endpoint:
            raise ValueError("mTLS endpoint is not available.")
        return default_mtls_endpoint
    else:
        return default_endpoint_template.format(UNIVERSE_DOMAIN=universe_domain)


def resolve_client_universe(
    client_options: client_options_lib.ClientOptions | Mapping[str, Any] | None = None,
) -> str:
    """Resolve a client's universe domain from ``client_options`` or the environment.

    Follows AIP-4113 precedence: ``client_options.universe_domain``, then
    ``GOOGLE_CLOUD_UNIVERSE_DOMAIN``, then ``"googleapis.com"``.

    Args:
        client_options (Optional[Union[google.api_core.client_options.ClientOptions, Mapping[str, Any]]]):
            Optional ``ClientOptions`` instance or mapping passed to
            ``Client.__init__``. If ``None``, falls back to
            ``GOOGLE_CLOUD_UNIVERSE_DOMAIN`` and then ``"googleapis.com"``.

    Returns:
        str: The resolved universe domain string.

    Raises:
        EmptyUniverseError: If the configured universe domain is an empty string.
        TypeError: If ``client_options`` is not a ``ClientOptions`` instance,
            ``Mapping``, or ``None``.
    """
    if client_options is None:
        options_universe = None
    elif isinstance(client_options, Mapping):
        options_universe = client_options.get("universe_domain")
    elif isinstance(client_options, client_options_lib.ClientOptions):
        options_universe = client_options.universe_domain
    else:
        raise TypeError(
            "client_options must be a ClientOptions instance, Mapping, or None; "
            f"got {type(client_options).__name__}"
        )
    return determine_domain(
        options_universe,
        os.getenv(UNIVERSE_DOMAIN_ENV),
    )


def validate_credentials_universe(
    client_universe: str,
    credentials: Union[
        auth_credentials.Credentials, "aio_credentials.Credentials", None
    ],
) -> None:
    """Validate that resolved client credentials match ``client_universe``.

    Call on ``self._credentials`` after ``super().__init__()`` or Application
    Default Credentials resolution rather than on the raw constructor
    ``credentials`` argument (which is ``None`` before ADC loads), and never
    inside ``Credentials.before_request()``. Exempts ``None``, synchronous and
    asynchronous ``AnonymousCredentials``, and ``compute_engine.Credentials``
    whose universe domain is not yet cached in memory (avoiding synchronous
    Metadata Server HTTP requests during client initialization).

    Args:
        client_universe (str): Resolved universe domain of the client.
        credentials (Optional[Union[google.auth.credentials.Credentials, google.auth.aio.credentials.Credentials]]):
            Resolved credentials bound to the client, or ``None`` (in which case
            validation is skipped).

    Raises:
        UniverseMismatchError: If ``credentials`` has an in-memory universe
            domain configured for a different universe than ``client_universe``.
    """
    if credentials is None or isinstance(credentials, _ANONYMOUS_CREDENTIAL_TYPES):
        return
    if isinstance(credentials, compute_engine.Credentials) and not getattr(
        credentials, "_universe_domain_cached", False
    ):
        return
    compare_domains(client_universe, credentials)


def _parse_target(url_or_target: str) -> _ParsedTarget | None:
    """Parse an HTTP(S) URL or gRPC target into normalized components.

    Uses :func:`urllib.parse.urlsplit` for case-insensitive RFC 3986 scheme and
    port validation while normalizing scheme-less ``host:port`` targets and gRPC
    path-style schemes (``dns:`` and ``google-c2p:///``). Rejects userinfo
    (``@`` in authority/netloc) while allowing ``@`` in HTTP(S) paths and
    queries (such as service account email endpoints). Returns ``None`` for
    empty, non-string, userinfo- or fragment-containing, unknown-scheme, or
    malformed inputs.
    """
    if not isinstance(url_or_target, str) or not url_or_target or "#" in url_or_target:
        return None

    try:
        raw = urlsplit(url_or_target)
        if raw.scheme in ("http", "https"):
            if (
                not url_or_target[len(raw.scheme) :].startswith("://")
                or "@" in raw.netloc
            ):
                return None
            _ = raw.port
            if not raw.hostname:
                return None
            return _ParsedTarget(raw.scheme, "", raw.hostname, raw.query)

        if raw.scheme == "google-c2p":
            if not url_or_target[len(raw.scheme) :].startswith(":///"):
                return None
            endpoint = raw.path.removeprefix("/")
            authority = ""
            query = raw.query
        elif raw.scheme == "dns":
            _ = raw.port
            endpoint = raw.path.removeprefix("/")
            authority = raw.netloc
            query = raw.query
        elif "://" in url_or_target:
            return None
        else:
            endpoint = url_or_target
            authority = ""
            query = ""

        inner = urlsplit(f"//{endpoint}")
        _ = inner.port
        if "@" in authority or "@" in inner.netloc or inner.path or not inner.hostname:
            return None
        return _ParsedTarget(
            raw.scheme if raw.scheme in ("google-c2p", "dns") else "",
            authority,
            inner.hostname,
            query or inner.query,
        )
    except ValueError:
        return None


def is_googleapis_host(url_or_target: str) -> bool:
    """Return True if an HTTP(S) URL or gRPC target resolves to ``googleapis.com``.

    Matches ``googleapis.com`` and ``*.googleapis.com`` across ``https://`` URLs,
    ``host:port`` gRPC targets, ``google-c2p:///`` DirectPath targets, and
    ``dns:///`` or ``dns://authority/`` targets while rejecting userinfo in the
    authority/netloc (``@``), fragments (``#``), unknown schemes, malformed
    ports, and spoofed suffixes. Intended for gating default-universe-only
    features (such as DirectPath, mTLS endpoint switching, or built-in Cloud
    Monitoring metrics); do not use to test equality against a single default
    service host because regional (``*.rep.googleapis.com``) and Private Service
    Connect (``*.p.googleapis.com``) endpoints also match ``*.googleapis.com``.

    Args:
        url_or_target (str): HTTP(S) URL or gRPC target string to inspect.

    Returns:
        bool: True if the target hostname is ``googleapis.com`` or a valid
            subdomain of ``googleapis.com``; False otherwise.
    """
    parsed = _parse_target(url_or_target)
    return bool(parsed and _GOOGLEAPIS_HOST_PATTERN.fullmatch(parsed.host))
