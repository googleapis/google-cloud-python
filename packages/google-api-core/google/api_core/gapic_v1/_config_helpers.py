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

"""Helpers for parsing environment variables."""

import os
from typing import Optional, Tuple

from google.api_core.gapic_v1._client_cert import use_client_cert_effective
from google.auth.exceptions import MutualTLSChannelError  # type: ignore


def read_environment_variables() -> Tuple[bool, str, Optional[str]]:
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
    use_client_cert = use_client_cert_effective()
    use_mtls_endpoint = os.getenv(
        "GOOGLE_API_USE_MTLS_ENDPOINT", "auto"
    ).lower()  # noqa: E501
    universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
    if use_mtls_endpoint not in ("auto", "never", "always"):
        raise MutualTLSChannelError(
            "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` "
            "must be `never`, `auto` or `always`"
        )
    return use_client_cert, use_mtls_endpoint, universe_domain_env


# Backward compatibility aliases for private methods
# Previously, gapic-generator-python generated clients used these methods
_read_environment_variables = read_environment_variables
