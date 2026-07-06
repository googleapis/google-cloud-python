# -*- coding: utf-8 -*-
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

"""Helpers for GAPIC client initialization."""

import os
import re
import uuid
from typing import Any, Optional, Tuple

from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore

_MTLS_ENDPOINT_RE = re.compile(
    r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?"
    r"(?P<googledomain>\.googleapis\.com)?"
)


def _get_default_mtls_endpoint(api_endpoint: Optional[str]) -> Optional[str]:
    """Converts api endpoint to mTLS endpoint.

    Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
    "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
    Args:
        api_endpoint (Optional[str]): the api endpoint to convert.
    Returns:
        Optional[str]: converted mTLS api endpoint.
    """
    if not api_endpoint:
        return api_endpoint

    m = _MTLS_ENDPOINT_RE.match(api_endpoint)
    if m is None:
        # Could not parse api_endpoint; return as-is.
        return api_endpoint

    name, mtls_group, sandbox, googledomain = m.groups()
    if mtls_group or not googledomain:
        return api_endpoint

    if sandbox:
        return api_endpoint.replace(
            "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
        )

    return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")


def _use_client_cert_effective() -> bool:
    """Returns whether client certificate should be used for mTLS if the
    google-auth version supports should_use_client_cert automatic mTLS
    enablement.

    Alternatively, read from the GOOGLE_API_USE_CLIENT_CERTIFICATE env var.

    Returns:
        bool: whether client certificate should be used for mTLS
    Raises:
        ValueError: (If using a version of google-auth without
        should_use_client_cert and GOOGLE_API_USE_CLIENT_CERTIFICATE is
        set to an unexpected value.)
    """
    # check if google-auth version supports should_use_client_cert for
    # automatic mTLS enablement
    if hasattr(mtls, "should_use_client_cert"):  # pragma: NO COVER
        return mtls.should_use_client_cert()
    else:  # pragma: NO COVER
        # if unsupported, fallback to reading from env var
        use_client_cert_str = os.getenv(
            "GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"
        ).lower()
        if use_client_cert_str not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` "
                "must be either `true` or `false`"
            )
        return use_client_cert_str == "true"


def _get_api_endpoint(
    api_override: Optional[str],
    client_cert_source: Optional[Any],
    universe_domain: str,
    use_mtls_endpoint: str,
    default_universe: str,
    default_mtls_endpoint: Optional[str],
    default_endpoint_template: str,
) -> Optional[str]:
    """Return the API endpoint used by the client.

    Args:
        api_override (Optional[str]): The API endpoint override.
        client_cert_source (Optional[Any]): The client certificate source.
        universe_domain (str): The universe domain.
        use_mtls_endpoint (str): How to use the mTLS endpoint.
        default_universe (str): The default universe.
        default_mtls_endpoint (Optional[str]): The default mTLS endpoint.
        default_endpoint_template (str): The default endpoint template.

    Returns:
        Optional[str]: The API endpoint to be used by the client.
    """
    if api_override is not None:
        return api_override
    elif use_mtls_endpoint == "always" or (
        use_mtls_endpoint == "auto" and client_cert_source
    ):
        if universe_domain != default_universe:
            raise MutualTLSChannelError(
                f"mTLS is not supported in any universe other than "
                f"{default_universe}."
            )
        return default_mtls_endpoint
    else:
        return default_endpoint_template.format(
            UNIVERSE_DOMAIN=universe_domain
        )


def _read_environment_variables() -> Tuple[bool, str, Optional[str]]:
    """Returns the environment variables used by the client.

    Returns:
        Tuple[bool, str, Optional[str]]: returns the
        GOOGLE_API_USE_CLIENT_CERTIFICATE, GOOGLE_API_USE_MTLS_ENDPOINT,
        and GOOGLE_CLOUD_UNIVERSE_DOMAIN environment variables.

    Raises:
        ValueError: If GOOGLE_API_USE_CLIENT_CERTIFICATE is not
            any of ["true", "false"].
        google.auth.exceptions.MutualTLSChannelError: If
            GOOGLE_API_USE_MTLS_ENDPOINT is not any of
            ["auto", "never", "always"].
    """
    use_client_cert = _use_client_cert_effective()
    use_mtls_endpoint = os.getenv(
        "GOOGLE_API_USE_MTLS_ENDPOINT", "auto"
    ).lower()
    universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
    if use_mtls_endpoint not in ("auto", "never", "always"):
        raise MutualTLSChannelError(
            "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` "
            "must be `never`, `auto` or `always`"
        )
    return use_client_cert, use_mtls_endpoint, universe_domain_env


def _get_client_cert_source(
    provided_cert_source: Optional[Any], use_cert_flag: bool
) -> Optional[Any]:
    """Return the client cert source to be used by the client.

    Args:
        provided_cert_source (bytes): The client certificate source provided.
        use_cert_flag (bool): A flag indicating whether to use the
            client certificate.

    Returns:
        bytes or None: The client cert source to be used by the client.
    """
    client_cert_source = None
    if use_cert_flag:
        if provided_cert_source:
            client_cert_source = provided_cert_source
        elif (
            hasattr(mtls, "has_default_client_cert_source")
            and mtls.has_default_client_cert_source()
        ):
            client_cert_source = mtls.default_client_cert_source()
    return client_cert_source


def _get_universe_domain(
    client_universe_domain: Optional[str],
    universe_domain_env: Optional[str],
    default_universe: str,
) -> str:
    """Return the universe domain used by the client.

    Args:
        client_universe_domain (Optional[str]): The universe domain
            configured via the client options.
        universe_domain_env (Optional[str]): The universe domain
            configured via the "GOOGLE_CLOUD_UNIVERSE_DOMAIN" env var.
        default_universe (str): The default universe domain.

    Returns:
        str: The universe domain to be used by the client.

    Raises:
        ValueError: If the universe domain is an empty string.
    """
    universe_domain = default_universe
    if client_universe_domain is not None:
        universe_domain = client_universe_domain
    elif universe_domain_env is not None:
        universe_domain = universe_domain_env
    if len(universe_domain.strip()) == 0:
        raise ValueError("Universe Domain cannot be an empty string.")
    return universe_domain


def _setup_request_id(
    request: Any, field_name: str, is_proto3_optional: bool
) -> None:
    """Populate a UUID4 field in the request if it is not already set.

    Args:
        request (Union[google.protobuf.message.Message, dict]): The
            request object.
        field_name (str): The name of the field to populate.
        is_proto3_optional (bool): Whether the field is proto3 optional.
    """
    if isinstance(request, dict):
        if is_proto3_optional:
            if field_name not in request:
                request[field_name] = str(uuid.uuid4())
        elif not request.get(field_name):
            request[field_name] = str(uuid.uuid4())
        return

    if is_proto3_optional:
        try:
            # Pure protobuf messages
            if not request.HasField(field_name):
                setattr(request, field_name, str(uuid.uuid4()))
        except (AttributeError, ValueError):
            # Proto-plus messages or other objects
            if field_name not in request:
                setattr(request, field_name, str(uuid.uuid4()))
    else:
        if not getattr(request, field_name):
            setattr(request, field_name, str(uuid.uuid4()))
