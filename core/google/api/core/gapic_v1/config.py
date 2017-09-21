# Copyright 2017 Google Inc.
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

import grpc
import six

from google.api.core import exceptions


_MILLIS_PER_SECOND = 1000.0


MethodConfig = collections.namedtuple('MethodConfig', [
    'timeout',
])

RetryableMethodConfig = collections.namedtuple('RetryableMethodConfig', [
    # Retry settings
    'retry_exceptions',
    'initial_delay',
    'delay_multiplier',
    'max_delay',
    'deadline',
    # Timeout settings
    'initial_timeout',
    'timeout_multiplier',
    'max_timeout',
])


def _exception_class_for_grpc_status_name(name):
    """Returns the Google API exception class for a gRPC error code name."""
    return exceptions.exception_class_for_grpc_status(
        getattr(grpc.StatusCode, name))


def _make_retryable_config(retry_params, retry_codes):
    """Creates a retryable method configuration.

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
        RetryableMethodConfig: Configuration for the method.
    """
    return RetryableMethodConfig(
        retry_exceptions=[
            _exception_class_for_grpc_status_name(code)
            for code in retry_codes],
        initial_delay=(
            retry_params['initial_retry_delay_millis'] / _MILLIS_PER_SECOND),
        delay_multiplier=retry_params['retry_delay_multiplier'],
        max_delay=(
            retry_params['max_retry_delay_millis'] / _MILLIS_PER_SECOND),
        deadline=(
            retry_params['total_timeout_millis'] / _MILLIS_PER_SECOND),
        initial_timeout=(
            retry_params['initial_rpc_timeout_millis'] / _MILLIS_PER_SECOND),
        timeout_multiplier=retry_params['rpc_timeout_multiplier'],
        max_timeout=(
            retry_params['max_rpc_timeout_millis'] / _MILLIS_PER_SECOND),
    )


def create_method_configs(interface_config):
    """Creates method configs for each method in a gapic interface config.

    Args:
        interface_config (Mapping): The interface config section of the full
            gapic library config. For example,
            ``gapic_config['interfaces']['google.example.v1.ExampleService']``.

    Returns:
        Mapping[str, Union[MethodConfig, RetryableMethodConfig]]: A mapping
            of RPC method names to their associated parsed configuration.
    """
    # Grab all the retry codes
    retry_codes_map = {
        name: retry_codes
        for name, retry_codes
        in six.iteritems(interface_config.get('retry_codes', {}))
    }

    # Grab all of the retry params
    retry_params_map = {
        name: retry_params
        for name, retry_params
        in six.iteritems(interface_config.get('retry_params', {}))
    }

    # Iterate through all the API methods and create a flat MethodConfig
    # instance for each one.
    method_configs = {}
    for method_name, method_params in six.iteritems(
            interface_config.get('methods', {})):
        retry_params_name = method_params.get('retry_params_name')
        if retry_params_name is not None:
            config = _make_retryable_config(
                retry_params_map[retry_params_name],
                retry_codes_map[method_params['retry_codes_name']])
        else:
            config = MethodConfig(
                timeout=method_params['timeout_millis'] / _MILLIS_PER_SECOND)

        method_configs[method_name] = config

    return method_configs
