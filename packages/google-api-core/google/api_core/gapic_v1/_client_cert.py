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

"""Helpers for client certificate handling and mTLS authentication."""

import os
from typing import Any, Optional

from google.auth.transport import mtls  # type: ignore


def use_client_cert_effective() -> bool:
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


def get_client_cert_source(
    provided_cert_source: Optional[Any], use_cert_flag: bool
) -> Optional[Any]:
    """Return the client cert source to be used by the client.

    Args:
        provided_cert_source (Callable[[], Tuple[bytes, bytes]]): The client certificate source provided.
        use_cert_flag (bool): A flag indicating whether to use the
            client certificate.

    Returns:
        Callable[[], Tuple[bytes, bytes]] or None: The client cert source to be used by the client.
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
