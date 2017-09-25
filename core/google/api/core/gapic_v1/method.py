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

"""Helpers for wrapping low-level gRPC methods with common functionality.

This is used by gapic clients to provide common error mapping, retry, timeout,
pagination, and long-running operations to gRPC methods.
"""

import platform

import pkg_resources

from google.api.core import retry
from google.api.core import timeout
from google.api.core.helpers import grpc_helpers

_PY_VERSION = platform.python_version()
_GRPC_VERSION = pkg_resources.get_distribution('grpcio').version
_API_CORE_VERSION = pkg_resources.get_distribution('google-cloud-core').version
METRICS_METADATA_KEY = 'x-goog-api-client'


def _is_not_none_or_false(value):
    return value is not None and value is not False


def _apply_decorators(func, decorators):
    """Apply a list of decorators to a given function.

    ``decorators`` may contain items that are ``None`` or ``False`` which will
    be ignored.
    """
    decorators = list(filter(_is_not_none_or_false, decorators))

    for decorator in reversed(decorators):
        func = decorator(func)

    return func


def _prepare_metadata(metadata):
    """Transforms metadata to gRPC format and adds global metrics.

    Args:
        metadata (Optional[Mapping[str, str]]): Any current metadata.

    Returns:
        Sequence[Tuple(str, str)]: The gRPC-friendly metadata keys and values.
    """
    if metadata is None:
        metadata = {}

    client_metadata = 'api-core/{} gl-python/{} grpc/{}'.format(
        _API_CORE_VERSION, _PY_VERSION, _API_CORE_VERSION)

    # Merge this with any existing metric metadata.
    client_metadata = ' '.join(filter(None, [
        client_metadata, metadata.get(METRICS_METADATA_KEY, None)]))

    metadata[METRICS_METADATA_KEY] = client_metadata

    return list(metadata.items())


def wrap_method(func, default_retry=None, default_timeout=None, metadata=None):
    """Wrap an RPC method with common behavior.

    This applies common error wrapping, retry, and timeout behavior a function.
    The wrapped function will take optional ``retry`` and ``timeout``
    arguments.

    For example::

        import google.api.core.gapic_v1.method
        from google.api.core import retry
        from google.api.core import timeout

        # The original RPC method.
        def get_topic(name, timeout=None):
            request = publisher_v2.GetTopicRequest(name=name)
            return publisher_stub.GetTopic(request, timeout=timeout)

        default_retry = retry.Retry(deadline=60)
        default_timeout = timeout.Timeout(deadline=60)
        wrapped_get_topic = google.api.core.gapic_v1.method.wrap_method(
            get_topic, default_retry)

        # Execute get_topic with default retry and timeout:
        response = wrapped_get_topic()

        # Execute get_topic without doing any retying but with the default
        # timeout:
        response = wrapped_get_topic(retry=False)

        # Execute get_topic but only retry on 5xx errors:
        my_retry = retry.Retry(retry.if_exception_type(
            exceptions.InternalServerError))
        response = wrapped_get_topic(retry=my_retry)

    The way this works is by late-wrapping the given function with the retry
    and timeout decorators. Essentially, when ``wrapped_get_topic()`` is
    called:

    * ``get_topic()`` is first wrapped with the ``timeout`` into
      ``get_topic_with_timeout``.
    * ``get_topic_with_timeout`` is wrapped with the ``retry`` into
      ``get_topic_with_timeout_and_retry()``.
    * The final ``get_topic_with_timeout_and_retry`` is called passing through
      the ``args``  and ``kwargs``.

    The callstack is therefore::

        method.__call__() ->
            Retry.__call__() ->
                Timeout.__call__() ->
                    wrap_errors() ->
                        get_topic()

    Note that if ``timeout`` or ``retry`` is ``False``, then they are not
    applied to the function. For example,
    ``wrapped_get_topic(timeout=False, retry=False)`` is more or less
    equivalent to just calling ``get_topic`` but with error re-mapping.

    Args:
        func (Callable[Any]): The function to wrap. If timeout is specified,
            then this function should take an optional timeout parameter.
        default_retry (Optional[google.api.core.Retry]): The default retry
            strategy.
        default_timeout (Optional[google.api.core.Timeout]): The default
            timeout strategy. If an int or float is specified, the timeout will
            always be set to that value.
        metadata (Union(Mapping[str, str], False)): A dict of metadata keys and
            values. This will be augmented with common ``x-google-api-client``
            metadata. If False, metadata will not be passed to the function
            at all.

    Returns:
        TODO
    """
    func = grpc_helpers.wrap_errors(func)
    if metadata is not False:
        metadata = _prepare_metadata(metadata)

    def method(*args, **kwargs):
        """RPC method with retry and timeout."""
        # Note: Due to Python 2 lacking keyword-only arguments we use this
        # pattern to extract the retry and timeout params.
        retry_ = kwargs.pop('retry', None)
        if retry_ is None:
            retry_ = default_retry

        timeout_ = kwargs.pop('timeout', None)
        if timeout_ is None:
            timeout_ = default_timeout

        # If timeout is specified as a number instead of a Timeout instance,
        # convert it to a ConstantTimeout.
        if timeout_ is not False and isinstance(timeout_, (int, float)):
            timeout_ = timeout.ConstantTimeout(timeout_)

        # If timeout is the default and the default timeout is exponential and
        # a non-default retry is specified, make sure the timeout's deadline
        # matches the retry's. This handles the case where the user leaves
        # the timeout default but specifies a lower deadline via the retry.
        if (timeout_ is default_timeout
                and retry is not False
                and retry is not default_retry
                and isinstance(timeout_, timeout.ExponentialTimeout)):
            timeout_ = timeout_.with_deadline(retry_._deadline)

        # Apply all applicable decorators.
        wrapped_func = _apply_decorators(func, [retry_, timeout_])

        # Set the metadata for the call using the metadata calculated by
        # _prepare_metadata.
        if metadata is not False:
            kwargs['metadata'] = metadata

        return wrapped_func(*args, **kwargs)

    return method
