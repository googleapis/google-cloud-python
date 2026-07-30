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
"""A compatibility module for older versions of google-api-core."""

from typing import Optional
from urllib.parse import urlparse, urlunparse

from google.auth.exceptions import MutualTLSChannelError
from google.api_core.universe import EmptyUniverseError

import uuid
from typing import Union
import google.protobuf.message

DEFAULT_UNIVERSE = "googleapis.com"


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

def get_universe_domain(
    *potential_universes: Optional[str],
    default_universe: str = DEFAULT_UNIVERSE,
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


def setup_request_id(
    request: Union[google.protobuf.message.Message, dict, None],
    field_name: str,
    is_proto3_optional: bool,
) -> None:
    """Populate a UUID4 field in the request if it is not already set.

    This helper is used to ensure request idempotency by automatically
    generating a unique identifier (such as `request_id`) for requests
    that support it. If a request is retried, the same identifier can be
    sent on subsequent retries, allowing the server to recognize the retried
    request and prevent duplicate processing (e.g., creating duplicate
    resources).

    Args:
        request (Union[google.protobuf.message.Message, dict]): The
            request object.
        field_name (str): The name of the field to populate.
        is_proto3_optional (bool): Whether the field is proto3 optional.
    """
    if request is None:
        return

    if isinstance(request, dict):
        if is_proto3_optional:
            if field_name not in request or request[field_name] is None:
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
            if not getattr(request, field_name, None):
                setattr(request, field_name, str(uuid.uuid4()))
    else:
        if not getattr(request, field_name, None):
            setattr(request, field_name, str(uuid.uuid4()))
