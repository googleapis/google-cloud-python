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
import os
import re
from typing import Optional
from google.auth.transport import mtls  # type: ignore
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
    if not api_endpoint:
        return api_endpoint

    mtls_endpoint_re = re.compile(
        r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
    )

    m = mtls_endpoint_re.match(api_endpoint)
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

def use_client_cert_effective() -> bool:
    """Returns whether client certificate should be used for mTLS if the
    google-auth version supports should_use_client_cert automatic mTLS enablement.

    Alternatively, read from the GOOGLE_API_USE_CLIENT_CERTIFICATE env var.

    Returns:
        bool: whether client certificate should be used for mTLS
    Raises:
        ValueError: (If using a version of google-auth without should_use_client_cert and
        GOOGLE_API_USE_CLIENT_CERTIFICATE is set to an unexpected value.)
    """
    # check if google-auth version supports should_use_client_cert for automatic mTLS enablement
    if hasattr(mtls, "should_use_client_cert"):  # pragma: NO COVER
        return mtls.should_use_client_cert()
    else:  # pragma: NO COVER
        # if unsupported, fallback to reading from env var
        use_client_cert_str = os.getenv(
            "GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"
        ).lower()
        if use_client_cert_str not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be"
                " either `true` or `false`"
            )
        return use_client_cert_str == "true"

def read_environment_variables():
    """Returns the environment variables used by the client.

    Returns:
        Tuple[bool, str, str]: returns the GOOGLE_API_USE_CLIENT_CERTIFICATE,
        GOOGLE_API_USE_MTLS_ENDPOINT, and GOOGLE_CLOUD_UNIVERSE_DOMAIN environment variables.

    Raises:
        ValueError: If GOOGLE_API_USE_CLIENT_CERTIFICATE is not
            any of ["true", "false"].
        google.auth.exceptions.MutualTLSChannelError: If GOOGLE_API_USE_MTLS_ENDPOINT
            is not any of ["auto", "never", "always"].
    """
    use_client_cert = use_client_cert_effective()
    use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
    universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
    if use_mtls_endpoint not in ("auto", "never", "always"):
        raise MutualTLSChannelError(
            "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )
    return use_client_cert, use_mtls_endpoint, universe_domain_env
