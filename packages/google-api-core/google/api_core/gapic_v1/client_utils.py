# Copyright 2026 Google LLC
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
#

import warnings
from typing import Any, Callable, Optional, Sequence, Tuple, Union
from urllib.parse import urlparse, urlunparse

import google.auth  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore
from google.api_core import exceptions as core_exceptions


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
    if lowered_host.endswith(".sandbox.googleapis.com"):
        new_host = host[:-23] + ".mtls.sandbox.googleapis.com"
    elif lowered_host.endswith(".googleapis.com"):
        new_host = host[:-15] + ".mtls.googleapis.com"
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


def get_universe_domain(
    universe_domain: Optional[str],
    default_universe: str = "googleapis.com",
) -> str:
    """Return the universe domain used by the client.

    Args:
        universe_domain (Optional[str]): The configured universe domain.
        default_universe (str): The default universe domain.

    Returns:
        str: The universe domain to be used by the client.

    Raises:
        ValueError: If the resolved universe domain is an empty string.
    """
    resolved = (
        universe_domain.strip() if universe_domain is not None else default_universe
    )

    if not resolved:
        raise ValueError("Universe Domain cannot be an empty string.")
    return resolved


def resolve_credentials_and_host(
    host: str,
    credentials: Optional[Any] = None,
    credentials_file: Optional[str] = None,
    scopes: Optional[Sequence[str]] = None,
    quota_project_id: Optional[str] = None,
    always_use_jwt_access: Optional[bool] = False,
    api_audience: Optional[str] = None,
    auth_scopes: Optional[Sequence[str]] = None,
    ignore_credentials: bool = False,
) -> Tuple[Any, str]:
    """Resolves and loads authorization credentials and host for the client.

    Args:
        host (str): The host to connect to.
        credentials (Optional[google.auth.credentials.Credentials]): The
            credentials to attach to requests.
        credentials_file (Optional[str]): A file with credentials to load.
        scopes (Optional[Sequence[str]]): A list of scopes.
        quota_project_id (Optional[str]): An optional project to use for billing and quota.
        always_use_jwt_access (Optional[bool]): Whether self signed JWT should be used.
        api_audience (Optional[str]): The intended audience for the API calls.
        auth_scopes (Optional[Sequence[str]]): Default scopes to fall back to.
        ignore_credentials (bool): If True, skips credentials loading.

    Returns:
        Tuple[google.auth.credentials.Credentials, str]: Stated credentials and resolved host.
    """
    if credentials and credentials_file:
        raise core_exceptions.DuplicateCredentialArgs(
            "'credentials_file' and 'credentials' are mutually exclusive"
        )

    if credentials_file is not None:
        credentials, _ = google.auth.load_credentials_from_file(
            credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            default_scopes=auth_scopes,
        )
    elif credentials is None and not ignore_credentials:
        credentials, _ = google.auth.default(
            scopes=scopes,
            quota_project_id=quota_project_id,
            default_scopes=auth_scopes,
        )
        if hasattr(credentials, "with_gdch_audience"):
            credentials = credentials.with_gdch_audience(
                api_audience if api_audience else host
            )

    if (
        always_use_jwt_access
        and isinstance(credentials, service_account.Credentials)
        and hasattr(credentials, "with_always_use_jwt_access")
    ):
        credentials = credentials.with_always_use_jwt_access(True)

    if ":" not in host:
        host += ":443"

    return credentials, host


def resolve_grpc_channel(
    host: str,
    channel: Optional[Any] = None,
    api_mtls_endpoint: Optional[str] = None,
    client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
    ssl_channel_credentials: Optional[Any] = None,
    client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
) -> Tuple[Optional[Any], Optional[Any], bool, str]:
    """Resolves SSL credentials and channels for gRPC client initialization.

    Args:
        host (str): Host to connect to.
        channel (Optional[Union[grpc.Channel, grpc.aio.Channel]]): Configured channel to reuse.
        api_mtls_endpoint (Optional[str]): Deprecated mutual TLS endpoint.
        client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): Deprecated client certificate source.
        ssl_channel_credentials (Optional[grpc.ChannelCredentials]): Custom SSL credentials.
        client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]): Client certificate source.

    Returns:
        Tuple[Optional[grpc.Channel], Optional[grpc.ChannelCredentials], bool, str]:
            - Stated or resolved gRPC channel (None if not provided).
            - Resolved SSL channel credentials (None if none needed).
            - ignore_credentials boolean.
            - Resolved host.
    """
    import grpc

    if api_mtls_endpoint:
        warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
    if client_cert_source:
        warnings.warn("client_cert_source is deprecated", DeprecationWarning)

    is_channel = isinstance(channel, grpc.Channel)
    if not is_channel:
        try:
            from grpc import aio
            is_channel = isinstance(channel, aio.Channel)
        except ImportError:
            pass

    ignore_credentials = False
    grpc_channel = None

    if is_channel:
        ignore_credentials = True
        grpc_channel = channel
        ssl_channel_credentials = None
    else:
        if api_mtls_endpoint:
            host = api_mtls_endpoint
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_channel_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                from google.auth.transport.grpc import SslCredentials
                ssl_channel_credentials = SslCredentials().ssl_credentials
        else:
            if client_cert_source_for_mtls and not ssl_channel_credentials:
                cert, key = client_cert_source_for_mtls()
                ssl_channel_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )

    return grpc_channel, ssl_channel_credentials, ignore_credentials, host


def resolve_rest_session(
    credentials: Any,
    default_host: str,
    client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
) -> Any:
    """Resolves and configures an AuthorizedSession for REST transports.

    Args:
        credentials (google.auth.credentials.Credentials): The credentials to use.
        default_host (str): Default host for REST requests.
        client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]): Client cert callback for mTLS.

    Returns:
        google.auth.transport.requests.AuthorizedSession: Configured session object.
    """
    from google.auth.transport.requests import AuthorizedSession  # type: ignore

    session = AuthorizedSession(credentials, default_host=default_host)
    if client_cert_source_for_mtls:
        session.configure_mtls_channel(client_cert_source_for_mtls)
    return session
