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

"""Helpers for routing and endpoint resolution."""

import re
from typing import Any, Optional

from google.auth.exceptions import MutualTLSChannelError  # type: ignore

_MTLS_ENDPOINT_RE = re.compile(
    r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?"
    r"(?P<googledomain>\.googleapis\.com)?"
)


def get_default_mtls_endpoint(api_endpoint: Optional[str]) -> Optional[str]:
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


def get_api_endpoint(
    api_override: Optional[str],
    client_cert_source: Optional[Any],
    universe_domain: str,
    use_mtls_endpoint: str,
    default_universe: str,
    default_mtls_endpoint: Optional[str],
    default_endpoint_template: str,
) -> Optional[str]:
    """Return the API endpoint used by the client."""
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
        )  # noqa: E501


def get_universe_domain(
    client_universe_domain: Optional[str],
    universe_domain_env: Optional[str],
    default_universe: str,
) -> str:
    """Return the universe domain used by the client."""
    universe_domain = default_universe
    if client_universe_domain is not None:
        universe_domain = client_universe_domain
    elif universe_domain_env is not None:
        universe_domain = universe_domain_env
    if len(universe_domain.strip()) == 0:
        raise ValueError("Universe Domain cannot be an empty string.")
    return universe_domain


# Backward compatibility aliases for private methods
# Previously, gapic-generator-python generated clients used these methods
_get_default_mtls_endpoint = get_default_mtls_endpoint
_get_universe_domain = get_universe_domain
