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

from typing import Any, Optional

from google.auth.exceptions import MutualTLSChannelError  # type: ignore


def get_default_mtls_endpoint(api_endpoint: Optional[str]) -> Optional[str]:
    """Converts api endpoint to mTLS endpoint.

    Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
    "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.

    Args:
        api_endpoint (Optional[str]): the api endpoint to convert.

    Returns:
        Optional[str]: converted mTLS api endpoint.
    """
    if not api_endpoint or ".mtls." in api_endpoint:
        return api_endpoint

    if api_endpoint.endswith(".sandbox.googleapis.com"):
        # len(".sandbox.googleapis.com") == 23
        return api_endpoint[:-23] + ".mtls.sandbox.googleapis.com"

    if api_endpoint.endswith(".googleapis.com"):
        # len(".googleapis.com") == 15
        return api_endpoint[:-15] + ".mtls.googleapis.com"

    return api_endpoint


def get_api_endpoint(
    api_override: Optional[str],
    client_cert_source: Optional[Any],
    universe_domain: str,
    use_mtls_endpoint: str,
    default_universe: str,
    default_mtls_endpoint: Optional[str],
    default_endpoint_template: str,
) -> str:
    """Return the API endpoint used by the client.

    Args:
        api_override (Optional[str]): The API endpoint override. If specified,
            this is always returned.
        client_cert_source (Optional[Any]): The client certificate source used by the client.
        universe_domain (str): The universe domain used by the client.
        use_mtls_endpoint (str): How to use the mTLS endpoint. Possible values
            are "always", "auto", or "never".
        default_universe (str): The default universe domain.
        default_mtls_endpoint (Optional[str]): The default mTLS endpoint.
        default_endpoint_template (str): The default endpoint template containing
            a placeholder `{UNIVERSE_DOMAIN}`.

    Returns:
        str: The API endpoint to be used by the client.

    Raises:
        google.auth.exceptions.MutualTLSChannelError: If mTLS is requested but
            not supported in the configured universe domain.
        ValueError: If mTLS is requested but no mTLS endpoint is available.
    """
    if api_override is not None:
        return api_override
    elif use_mtls_endpoint == "always" or (
        use_mtls_endpoint == "auto" and client_cert_source
    ):
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
    client_universe_domain: Optional[str],
    universe_domain_env: Optional[str],
    default_universe: str,
) -> str:
    """Return the universe domain used by the client.

    Args:
        client_universe_domain (Optional[str]): The universe domain configured
            via client options.
        universe_domain_env (Optional[str]): The universe domain configured
            via environment variable.
        default_universe (str): The default universe domain.

    Returns:
        str: The universe domain to be used by the client.

    Raises:
        ValueError: If the resolved universe domain is an empty string.
    """
    if client_universe_domain is not None:
        universe_domain = client_universe_domain.strip()
    elif universe_domain_env is not None:
        universe_domain = universe_domain_env.strip()
    else:
        universe_domain = default_universe

    if not universe_domain:
        raise ValueError("Universe Domain cannot be an empty string.")
    return universe_domain
