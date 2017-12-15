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

"""Helpers for :mod:`grpc`."""

import grpc
import six

from google.api_core import exceptions
from google.api_core import general_helpers
import google.auth
import google.auth.credentials
import google.auth.transport.grpc
import google.auth.transport.requests


# The list of gRPC Callable interfaces that return iterators.
_STREAM_WRAP_CLASSES = (
    grpc.UnaryStreamMultiCallable,
    grpc.StreamStreamMultiCallable,
)


def _patch_callable_name(callable_):
    """Fix-up gRPC callable attributes.

    gRPC callable lack the ``__name__`` attribute which causes
    :func:`functools.wraps` to error. This adds the attribute if needed.
    """
    if not hasattr(callable_, '__name__'):
        callable_.__name__ = callable_.__class__.__name__


def _wrap_unary_errors(callable_):
    """Map errors for Unary-Unary and Stream-Unary gRPC callables."""
    _patch_callable_name(callable_)

    @six.wraps(callable_)
    def error_remapped_callable(*args, **kwargs):
        try:
            return callable_(*args, **kwargs)
        except grpc.RpcError as exc:
            six.raise_from(exceptions.from_grpc_error(exc), exc)

    return error_remapped_callable


def _wrap_stream_errors(callable_):
    """Wrap errors for Unary-Stream and Stream-Stream gRPC callables.

    The callables that return iterators require a bit more logic to re-map
    errors when iterating. This wraps both the initial invocation and the
    iterator of the return value to re-map errors.
    """
    _patch_callable_name(callable_)

    @general_helpers.wraps(callable_)
    def error_remapped_callable(*args, **kwargs):
        try:
            result = callable_(*args, **kwargs)
            # Note: we are patching the private grpc._channel._Rendezvous._next
            # method as magic methods (__next__ in this case) can not be
            # patched on a per-instance basis (see
            # https://docs.python.org/3/reference/datamodel.html
            # #special-lookup).
            # In an ideal world, gRPC would return a *specific* interface
            # from *StreamMultiCallables, but they return a God class that's
            # a combination of basically every interface in gRPC making it
            # untenable for us to implement a wrapper object using the same
            # interface.
            result._next = _wrap_unary_errors(result._next)
            return result
        except grpc.RpcError as exc:
            six.raise_from(exceptions.from_grpc_error(exc), exc)

    return error_remapped_callable


def wrap_errors(callable_):
    """Wrap a gRPC callable and map :class:`grpc.RpcErrors` to friendly error
    classes.

    Errors raised by the gRPC callable are mapped to the appropriate
    :class:`google.api_core.exceptions.GoogleAPICallError` subclasses.
    The original `grpc.RpcError` (which is usually also a `grpc.Call`) is
    available from the ``response`` property on the mapped exception. This
    is useful for extracting metadata from the original error.

    Args:
        callable_ (Callable): A gRPC callable.

    Returns:
        Callable: The wrapped gRPC callable.
    """
    if isinstance(callable_, _STREAM_WRAP_CLASSES):
        return _wrap_stream_errors(callable_)
    else:
        return _wrap_unary_errors(callable_)


def create_channel(target, credentials=None, scopes=None, **kwargs):
    """Create a secure channel with credentials.

    Args:
        target (str): The target service address in the format 'hostname:port'.
        credentials (google.auth.credentials.Credentials): The credentials. If
            not specified, then this function will attempt to ascertain the
            credentials from the environment using :func:`google.auth.default`.
        scopes (Sequence[str]): A optional list of scopes needed for this
            service. These are only used when credentials are not specified and
            are passed to :func:`google.auth.default`.
        kwargs: Additional key-word args passed to
            :func:`google.auth.transport.grpc.secure_authorized_channel`.

    Returns:
        grpc.Channel: The created channel.
    """
    if credentials is None:
        credentials, _ = google.auth.default(scopes=scopes)
    else:
        credentials = google.auth.credentials.with_scopes_if_required(
            credentials, scopes)

    request = google.auth.transport.requests.Request()

    return google.auth.transport.grpc.secure_authorized_channel(
        credentials, request, target, **kwargs)
