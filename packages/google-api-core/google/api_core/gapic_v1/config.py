# Copyright 2017 Google LLC
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

"""Helpers for loading gapic configuration data.

The Google API generator creates supplementary configuration for each RPC
method to tell the client library how to deal with retries and timeouts.
"""

import collections
import os
from typing import Callable, Optional, Tuple

import grpc

from google.api_core import exceptions, retry, timeout
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore

_MILLIS_PER_SECOND = 1000.0


def _exception_class_for_grpc_status_name(name):
    """Returns the Google API exception class for a gRPC error code name.

    DEPRECATED: use ``exceptions.exception_class_for_grpc_status`` method
    directly instead.

    Args:
        name (str): The name of the gRPC status code, for example,
            ``UNAVAILABLE``.

    Returns:
        :func:`type`: The appropriate subclass of
            :class:`google.api_core.exceptions.GoogleAPICallError`.
    """
    return exceptions.exception_class_for_grpc_status(getattr(grpc.StatusCode, name))


def _retry_from_retry_config(retry_params, retry_codes, retry_impl=retry.Retry):
    """Creates a Retry object given a gapic retry configuration.

    DEPRECATED: instantiate retry and timeout classes directly instead.

    Args:
        retry_params (dict): The retry parameter values, for example::

            {
                "initial_retry_delay_millis": 1000,
                "retry_delay_multiplier": 2.5,
                "max_retry_delay_millis": 120000,
                "initial_rpc_timeout_millis": 120000,
                "rpc_timeout_multiplier": 1.0,
                "max_rpc_timeout_millis": 120000,
                "total_timeout_millis": 600000
            }

        retry_codes (sequence[str]): The list of retryable gRPC error code
            names.

    Returns:
        google.api_core.retry.Retry: The default retry object for the method.
    """
    exception_classes = [
        _exception_class_for_grpc_status_name(code) for code in retry_codes
    ]
    return retry_impl(
        retry.if_exception_type(*exception_classes),
        initial=(retry_params["initial_retry_delay_millis"] / _MILLIS_PER_SECOND),
        maximum=(retry_params["max_retry_delay_millis"] / _MILLIS_PER_SECOND),
        multiplier=retry_params["retry_delay_multiplier"],
        deadline=retry_params["total_timeout_millis"] / _MILLIS_PER_SECOND,
    )


def _timeout_from_retry_config(retry_params):
    """Creates a ExponentialTimeout object given a gapic retry configuration.

    DEPRECATED: instantiate retry and timeout classes directly instead.

    Args:
        retry_params (dict): The retry parameter values, for example::

            {
                "initial_retry_delay_millis": 1000,
                "retry_delay_multiplier": 2.5,
                "max_retry_delay_millis": 120000,
                "initial_rpc_timeout_millis": 120000,
                "rpc_timeout_multiplier": 1.0,
                "max_rpc_timeout_millis": 120000,
                "total_timeout_millis": 600000
            }

    Returns:
        google.api_core.retry.ExponentialTimeout: The default time object for
            the method.
    """
    return timeout.ExponentialTimeout(
        initial=(retry_params["initial_rpc_timeout_millis"] / _MILLIS_PER_SECOND),
        maximum=(retry_params["max_rpc_timeout_millis"] / _MILLIS_PER_SECOND),
        multiplier=retry_params["rpc_timeout_multiplier"],
        deadline=(retry_params["total_timeout_millis"] / _MILLIS_PER_SECOND),
    )


MethodConfig = collections.namedtuple("MethodConfig", ["retry", "timeout"])


def parse_method_configs(interface_config, retry_impl=retry.Retry):
    """Creates default retry and timeout objects for each method in a gapic
    interface config.

    DEPRECATED: instantiate retry and timeout classes directly instead.

    Args:
        interface_config (Mapping): The interface config section of the full
            gapic library config. For example, If the full configuration has
            an interface named ``google.example.v1.ExampleService`` you would
            pass in just that interface's configuration, for example
            ``gapic_config['interfaces']['google.example.v1.ExampleService']``.
        retry_impl (Callable): The constructor that creates a retry decorator
            that will be applied to the method based on method configs.

    Returns:
        Mapping[str, MethodConfig]: A mapping of RPC method names to their
            configuration.
    """
    # Grab all the retry codes
    retry_codes_map = {
        name: retry_codes
        for name, retry_codes in interface_config.get("retry_codes", {}).items()
    }

    # Grab all of the retry params
    retry_params_map = {
        name: retry_params
        for name, retry_params in interface_config.get("retry_params", {}).items()
    }

    # Iterate through all the API methods and create a flat MethodConfig
    # instance for each one.
    method_configs = {}

    for method_name, method_params in interface_config.get("methods", {}).items():
        retry_params_name = method_params.get("retry_params_name")

        if retry_params_name is not None:
            retry_params = retry_params_map[retry_params_name]
            retry_ = _retry_from_retry_config(
                retry_params,
                retry_codes_map[method_params["retry_codes_name"]],
                retry_impl,
            )
            timeout_ = _timeout_from_retry_config(retry_params)

        # No retry config, so this is a non-retryable method.
        else:
            retry_ = None
            timeout_ = timeout.ConstantTimeout(
                method_params["timeout_millis"] / _MILLIS_PER_SECOND
            )

        method_configs[method_name] = MethodConfig(retry=retry_, timeout=timeout_)

    return method_configs


def use_client_cert_effective() -> bool:
    """Returns whether client certificate should be used for mTLS."""
    if hasattr(mtls, "should_use_client_cert"):
        return mtls.should_use_client_cert()
    else:
        use_client_cert_str = os.getenv(
            "GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"
        ).lower()
        if use_client_cert_str not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be"
                " either `true` or `false`"
            )
        return use_client_cert_str == "true"


def get_client_cert_source(
    provided_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]],
    use_cert_flag: bool,
) -> Optional[Callable[[], Tuple[bytes, bytes]]]:
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
        else:
            raise ValueError(
                "Client certificate is required for mTLS, but no client certificate source was provided or found."
            )
    return client_cert_source


def read_environment_variables() -> Tuple[bool, str, Optional[str]]:
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
