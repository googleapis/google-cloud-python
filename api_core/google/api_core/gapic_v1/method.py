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

import functools
import platform

import pkg_resources
import six

from google.api_core import general_helpers
from google.api_core import grpc_helpers
from google.api_core import page_iterator
from google.api_core import timeout

_PY_VERSION = platform.python_version()
_GRPC_VERSION = pkg_resources.get_distribution('grpcio').version
_API_CORE_VERSION = pkg_resources.get_distribution('google-api-core').version
METRICS_METADATA_KEY = 'x-goog-api-client'
USE_DEFAULT_METADATA = object()
DEFAULT = object()
"""Sentinel value indicating that a retry or timeout argument was unspecified,
so the default should be used."""


def _is_not_none_or_false(value):
    return value is not None and value is not False


def _apply_decorators(func, decorators):
    """Apply a list of decorators to a given function.

    ``decorators`` may contain items that are ``None`` or ``False`` which will
    be ignored.
    """
    decorators = filter(_is_not_none_or_false, reversed(decorators))

    for decorator in decorators:
        func = decorator(func)

    return func


def _prepare_metadata(metadata):
    """Transforms metadata to gRPC format and adds global metrics.

    Args:
        metadata (Mapping[str, str]): Any current metadata.

    Returns:
        Sequence[Tuple(str, str)]: The gRPC-friendly metadata keys and values.
    """
    client_metadata = 'api-core/{} gl-python/{} grpc/{}'.format(
        _API_CORE_VERSION, _PY_VERSION, _GRPC_VERSION)

    # Merge this with any existing metric metadata.
    if METRICS_METADATA_KEY in metadata:
        client_metadata = '{} {}'.format(
            client_metadata, metadata[METRICS_METADATA_KEY])

    metadata[METRICS_METADATA_KEY] = client_metadata

    return list(metadata.items())


def _determine_timeout(default_timeout, specified_timeout, retry):
    """Determines how timeout should be applied to a wrapped method.

    Args:
        default_timeout (Optional[Timeout]): The default timeout specified
            at method creation time.
        specified_timeout (Optional[Timeout]): The timeout specified at
            invocation time. If :attr:`DEFAULT`, this will be set to
            the ``default_timeout``.
        retry (Optional[Retry]): The retry specified at invocation time.

    Returns:
        Optional[Timeout]: The timeout to apply to the method or ``None``.
    """
    if specified_timeout is DEFAULT:
        specified_timeout = default_timeout

    if specified_timeout is default_timeout:
        # If timeout is the default and the default timeout is exponential and
        # a non-default retry is specified, make sure the timeout's deadline
        # matches the retry's. This handles the case where the user leaves
        # the timeout default but specifies a lower deadline via the retry.
        if (retry and retry is not DEFAULT
                and isinstance(default_timeout, timeout.ExponentialTimeout)):
            return default_timeout.with_deadline(retry._deadline)
        else:
            return default_timeout

    # If timeout is specified as a number instead of a Timeout instance,
    # convert it to a ConstantTimeout.
    if isinstance(specified_timeout, (int, float)):
        return timeout.ConstantTimeout(specified_timeout)
    else:
        return specified_timeout


class _GapicCallable(object):
    """Callable that applies retry, timeout, and metadata logic.

    Args:
        target (Callable): The low-level RPC method.
        retry (google.api_core.retry.Retry): The default retry for the
            callable. If ``None``, this callable will not retry by default
        timeout (google.api_core.timeout.Timeout): The default timeout
            for the callable. If ``None``, this callable will not specify
            a timeout argument to the low-level RPC method by default.
        metadata (Optional[Sequence[Tuple[str, str]]]): gRPC call metadata
            that's passed to the low-level RPC method. If ``None``, no metadata
            will be passed to the low-level RPC method.
    """

    def __init__(self, target, retry, timeout, metadata):
        self._target = target
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __call__(self, *args, **kwargs):
        """Invoke the low-level RPC with retry, timeout, and metadata."""
        # Note: Due to Python 2 lacking keyword-only arguments we use kwargs to
        # extract the retry and timeout params.
        timeout_ = _determine_timeout(
            self._timeout,
            kwargs.pop('timeout', self._timeout),
            # Use only the invocation-specified retry only for this, as we only
            # want to adjust the timeout deadline if the *user* specified
            # a different retry.
            kwargs.get('retry', None))

        retry = kwargs.pop('retry', self._retry)

        if retry is DEFAULT:
            retry = self._retry

        # Apply all applicable decorators.
        wrapped_func = _apply_decorators(self._target, [retry, timeout_])

        # Set the metadata for the call using the metadata calculated by
        # _prepare_metadata.
        if self._metadata is not None:
            kwargs['metadata'] = self._metadata

        return wrapped_func(*args, **kwargs)


def wrap_method(
        func, default_retry=None, default_timeout=None,
        metadata=USE_DEFAULT_METADATA):
    """Wrap an RPC method with common behavior.

    This applies common error wrapping, retry, and timeout behavior a function.
    The wrapped function will take optional ``retry`` and ``timeout``
    arguments.

    For example::

        import google.api_core.gapic_v1.method
        from google.api_core import retry
        from google.api_core import timeout

        # The original RPC method.
        def get_topic(name, timeout=None):
            request = publisher_v2.GetTopicRequest(name=name)
            return publisher_stub.GetTopic(request, timeout=timeout)

        default_retry = retry.Retry(deadline=60)
        default_timeout = timeout.Timeout(deadline=60)
        wrapped_get_topic = google.api_core.gapic_v1.method.wrap_method(
            get_topic, default_retry)

        # Execute get_topic with default retry and timeout:
        response = wrapped_get_topic()

        # Execute get_topic without doing any retying but with the default
        # timeout:
        response = wrapped_get_topic(retry=None)

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

    Note that if ``timeout`` or ``retry`` is ``None``, then they are not
    applied to the function. For example,
    ``wrapped_get_topic(timeout=None, retry=None)`` is more or less
    equivalent to just calling ``get_topic`` but with error re-mapping.

    Args:
        func (Callable[Any]): The function to wrap. It should accept an
            optional ``timeout`` argument. If ``metadata`` is not ``None``, it
            should accept a ``metadata`` argument.
        default_retry (Optional[google.api_core.Retry]): The default retry
            strategy. If ``None``, the method will not retry by default.
        default_timeout (Optional[google.api_core.Timeout]): The default
            timeout strategy. Can also be specified as an int or float. If
            ``None``, the method will not have timeout specified by default.
        metadata (Optional(Mapping[str, str])): A dict of metadata keys and
            values. This will be augmented with common ``x-google-api-client``
            metadata. If ``None``, metadata will not be passed to the function
            at all, if :attr:`USE_DEFAULT_METADATA` (the default) then only the
            common metadata will be provided.

    Returns:
        Callable: A new callable that takes optional ``retry`` and ``timeout``
            arguments and applies the common error mapping, retry, timeout,
            and metadata behavior to the low-level RPC method.
    """
    func = grpc_helpers.wrap_errors(func)

    if metadata is USE_DEFAULT_METADATA:
        metadata = {}

    if metadata is not None:
        metadata = _prepare_metadata(metadata)

    return general_helpers.wraps(func)(
        _GapicCallable(func, default_retry, default_timeout, metadata))


def wrap_with_paging(
        func, items_field, request_token_field, response_token_field):
    """Wrap an RPC method to return a page iterator.

    Args:
        func (Callable): The RPC method. This should already have been
            wrapped with common functionality using :func:`wrap_method`.
            request (protobuf.Message): The request message.
        items_field (str): The field in the response message that has the
            items for the page.
        request_token_field (str): The field in the request message used to
            specify the page token.
        response_token_field (str): The field in the response message that has
            the token for the next page.

    Returns:
        Callable: Returns a callable that when invoked will call the RPC
            method and return a
            :class:`google.api_core.page_iterator.Iterator`.
    """
    @six.wraps(func)
    def paged_method(request, **kwargs):
        """Wrapper that invokes a method and returns a page iterator."""
        iterator = page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(func, **kwargs),
            request=request,
            items_field=items_field,
            request_token_field=request_token_field,
            response_token_field=response_token_field)
        return iterator

    return paged_method
