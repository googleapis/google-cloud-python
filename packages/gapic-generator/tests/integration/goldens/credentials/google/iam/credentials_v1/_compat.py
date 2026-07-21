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
from typing import Optional, Callable, Tuple, Union
from google.auth.exceptions import MutualTLSChannelError

try:
    from google.api_core.gapic_v1.client_utils import (
        use_client_cert_effective,
        get_client_cert_source,
        read_environment_variables,
    )
except ImportError:  # pragma: NO COVER
    from google.auth.transport import mtls  # type: ignore

    # TODO: Remove these fallbacks when google-api-core >= 2.18.0 is the minimum required version.

    def use_client_cert_effective() -> bool:  # pragma: NO COVER
        """Returns whether client certificate should be used for mTLS."""
        if hasattr(mtls, "should_use_client_cert"):
            return mtls.should_use_client_cert()
        else:
            use_client_cert_str = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false").lower()
            if use_client_cert_str not in ("true", "false"):
                raise ValueError(
                    "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be"
                    " either `true` or `false`"
                )
            return use_client_cert_str == "true"

    def get_client_cert_source(
        provided_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]],
        use_cert_flag: bool,
    ) -> Optional[Callable[[], Tuple[bytes, bytes]]]:  # pragma: NO COVER
        """Return the client cert source to be used by the client."""
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

    def read_environment_variables() -> Tuple[bool, str, Optional[str]]:  # pragma: NO COVER
        """Returns the environment variables used by the client."""
        use_client_cert = use_client_cert_effective()
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
        universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` "
                "must be `never`, `auto` or `always`"
            )
        return use_client_cert, use_mtls_endpoint, universe_domain_env
