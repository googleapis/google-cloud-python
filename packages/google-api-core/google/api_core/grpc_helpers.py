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

import collections
import functools
import os
import threading
import urllib.parse
import warnings
import weakref
from typing import (
    Any,
    Callable,
    Generic,
    Iterator,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    TypeAlias,
    TypeVar,
    cast,
    get_args,
)

import google.auth
import google.auth.credentials
import google.auth.transport.grpc
import google.auth.transport.requests
import google.protobuf
import grpc

from google.api_core import exceptions, general_helpers
from google.api_core._feature_gating_helpers import _strtobool

_DIRECT_PATH_INTERCONNECT_ENV = "GOOGLE_CLOUD_ENABLE_DIRECT_PATH_XDS_OVER_INTERCONNECT"


def _resolve_direct_path_interconnect(
    attempt_direct_path_xds_over_interconnect: Optional[bool] = None,
) -> bool:
    """Resolves whether DirectPath over Interconnect is enabled.

    Args:
        attempt_direct_path_xds_over_interconnect (Optional[bool]): Programmatic
            override. If specified, this value takes precedence over environment
            variables. If None, falls back to the environment variable.

    Returns:
        bool: True if DirectPath over Interconnect is enabled, False otherwise.

    Raises:
        ValueError: If the environment variable contains an invalid boolean value.
    """
    if attempt_direct_path_xds_over_interconnect is not None:
        return attempt_direct_path_xds_over_interconnect

    env_val = os.environ.get(_DIRECT_PATH_INTERCONNECT_ENV)
    if env_val is not None:
        try:
            val = _strtobool(env_val)
        except ValueError:
            val = None
        if val is None:
            raise ValueError(
                f"Invalid value for {_DIRECT_PATH_INTERCONNECT_ENV}: {env_val!r}"
            )
        return val

    return False


def _extract_target_host(target: str) -> str:
    """Extracts the host from a target URI or address."""
    stripped_target = target
    for prefix in ("google-c2p:///", "dns:///", "https://", "http://"):
        if target.startswith(prefix):
            stripped_target = target.removeprefix(prefix)
            break
    try:
        return urllib.parse.urlsplit(f"//{stripped_target}").hostname or target
    except ValueError:
        return target


def _extract_direct_path_authority(target: str) -> Optional[str]:
    """Extracts the canonical TLS/HTTP2 authority for a ``-direct.googleapis.com`` target."""
    clean_host = _extract_target_host(target)
    suffix = "-direct.googleapis.com"
    if clean_host.endswith(suffix):
        service_prefix = clean_host.removesuffix(suffix)
        if service_prefix:
            return f"{service_prefix}.googleapis.com"
    return None


# The list of gRPC Callable interfaces that return iterators.
_STREAM_WRAP_CLASSES = (grpc.UnaryStreamMultiCallable, grpc.StreamStreamMultiCallable)

# denotes the proto response type for grpc calls
P = TypeVar("P")

# Type alias representing any client-side gRPC interceptor
ClientInterceptor: TypeAlias = (
    grpc.UnaryUnaryClientInterceptor
    | grpc.UnaryStreamClientInterceptor
    | grpc.StreamUnaryClientInterceptor
    | grpc.StreamStreamClientInterceptor
)

# Runtime tuple of gRPC client interceptor base classes for isinstance checks
_CLIENT_INTERCEPTOR_CLASSES = get_args(ClientInterceptor)


def _patch_callable_name(callable_):
    """Fix-up gRPC callable attributes.

    gRPC callable lack the ``__name__`` attribute which causes
    :func:`functools.wraps` to error. This adds the attribute if needed.
    """
    if not hasattr(callable_, "__name__"):
        callable_.__name__ = callable_.__class__.__name__


def _wrap_unary_errors(callable_):
    """Map errors for Unary-Unary and Stream-Unary gRPC callables."""
    _patch_callable_name(callable_)

    @functools.wraps(callable_)
    def error_remapped_callable(*args, **kwargs):
        try:
            return callable_(*args, **kwargs)
        except grpc.RpcError as exc:
            raise exceptions.from_grpc_error(exc) from exc

    return error_remapped_callable


class _StreamingResponseIterator(Generic[P], grpc.Call):
    def __init__(self, wrapped, prefetch_first_result=True):
        self._wrapped = wrapped

        # This iterator is used in a retry context, and returned outside after init.
        # gRPC will not throw an exception until the stream is consumed, so we need
        # to retrieve the first result, in order to fail, in order to trigger a retry.
        try:
            if prefetch_first_result:
                self._stored_first_result = next(self._wrapped)
        except TypeError:
            # It is possible the wrapped method isn't an iterable (a grpc.Call
            # for instance). If this happens don't store the first result.
            pass
        except StopIteration:
            # ignore stop iteration at this time. This should be handled outside of retry.
            pass

    def __iter__(self) -> Iterator[P]:
        """This iterator is also an iterable that returns itself."""
        return self

    def __next__(self) -> P:
        """Get the next response from the stream.

        Returns:
            protobuf.Message: A single response from the stream.
        """
        try:
            if hasattr(self, "_stored_first_result"):
                result = self._stored_first_result
                del self._stored_first_result
                return result
            return next(self._wrapped)
        except grpc.RpcError as exc:
            # If the stream has already returned data, we cannot recover here.
            raise exceptions.from_grpc_error(exc) from exc

    # grpc.Call & grpc.RpcContext interface

    def add_callback(self, callback):
        return self._wrapped.add_callback(callback)

    def cancel(self):
        return self._wrapped.cancel()

    def code(self):
        return self._wrapped.code()

    def details(self):
        return self._wrapped.details()

    def initial_metadata(self):
        return self._wrapped.initial_metadata()

    def is_active(self):
        return self._wrapped.is_active()

    def time_remaining(self):
        return self._wrapped.time_remaining()

    def trailing_metadata(self):
        return self._wrapped.trailing_metadata()


# public type alias denoting the return type of streaming gapic calls
GrpcStream = _StreamingResponseIterator[P]


def _wrap_stream_errors(callable_):
    """Wrap errors for Unary-Stream and Stream-Stream gRPC callables.

    The callables that return iterators require a bit more logic to re-map
    errors when iterating. This wraps both the initial invocation and the
    iterator of the return value to re-map errors.
    """
    _patch_callable_name(callable_)

    @functools.wraps(callable_)
    def error_remapped_callable(*args, **kwargs):
        try:
            result = callable_(*args, **kwargs)
            # Auto-fetching the first result causes PubSub client's streaming pull
            # to hang when re-opening the stream, thus we need examine the hacky
            # hidden flag to see if pre-fetching is disabled.
            # https://github.com/googleapis/python-pubsub/issues/93#issuecomment-630762257
            prefetch_first = getattr(callable_, "_prefetch_first_result_", True)
            return _StreamingResponseIterator(
                result, prefetch_first_result=prefetch_first
            )
        except grpc.RpcError as exc:
            raise exceptions.from_grpc_error(exc) from exc

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


def _create_composite_credentials(
    credentials=None,
    credentials_file=None,
    default_scopes=None,
    scopes=None,
    ssl_credentials=None,
    quota_project_id=None,
    default_host=None,
):
    """Create the composite credentials for secure channels.

    Args:
        credentials (google.auth.credentials.Credentials): The credentials. If
            not specified, then this function will attempt to ascertain the
            credentials from the environment using :func:`google.auth.default`.
        credentials_file (str): Deprecated. A file with credentials that can be loaded with
            :func:`google.auth.load_credentials_from_file`. This argument is
            mutually exclusive with credentials. This argument will be
            removed in the next major version of `google-api-core`.

            .. warning::
                Important: If you accept a credential configuration (credential JSON/File/Stream)
                from an external source for authentication to Google Cloud Platform, you must
                validate it before providing it to any Google API or client library. Providing an
                unvalidated credential configuration to Google APIs or libraries can compromise
                the security of your systems and data. For more information, refer to
                `Validate credential configurations from external sources`_.

            .. _Validate credential configurations from external sources:

            https://cloud.google.com/docs/authentication/external/externally-sourced-credentials
        default_scopes (Sequence[str]): A optional list of scopes needed for this
            service. These are only used when credentials are not specified and
            are passed to :func:`google.auth.default`.
        scopes (Sequence[str]): A optional list of scopes needed for this
            service. These are only used when credentials are not specified and
            are passed to :func:`google.auth.default`.
        ssl_credentials (grpc.ChannelCredentials): Optional SSL channel
            credentials. This can be used to specify different certificates.
        quota_project_id (str): An optional project to use for billing and quota.
        default_host (str): The default endpoint. e.g., "pubsub.googleapis.com".

    Returns:
        grpc.ChannelCredentials: The composed channel credentials object.

    Raises:
        google.api_core.DuplicateCredentialArgs: If both a credentials object and credentials_file are passed.
    """
    if credentials_file is not None:
        warnings.warn(general_helpers._CREDENTIALS_FILE_WARNING, DeprecationWarning)

    if credentials and credentials_file:
        raise exceptions.DuplicateCredentialArgs(
            "'credentials' and 'credentials_file' are mutually exclusive."
        )

    if credentials_file:
        credentials, _ = google.auth.load_credentials_from_file(
            credentials_file, scopes=scopes, default_scopes=default_scopes
        )
    elif credentials:
        credentials = google.auth.credentials.with_scopes_if_required(
            credentials, scopes=scopes, default_scopes=default_scopes
        )
    else:
        credentials, _ = google.auth.default(
            scopes=scopes, default_scopes=default_scopes
        )

    if quota_project_id and isinstance(
        credentials, google.auth.credentials.CredentialsWithQuotaProject
    ):
        credentials = credentials.with_quota_project(quota_project_id)

    request = google.auth.transport.requests.Request()

    # Create the metadata plugin for inserting the authorization header.
    try:
        metadata_plugin = google.auth.transport.grpc.AuthMetadataPlugin(
            credentials,
            request,
            default_host=default_host,
            suppress_metrics_header=True,
        )
    except TypeError:
        # Support older versions of google-auth that do not accept suppress_metrics_header
        metadata_plugin = google.auth.transport.grpc.AuthMetadataPlugin(
            credentials,
            request,
            default_host=default_host,
        )

    # Create a set of grpc.CallCredentials using the metadata plugin.
    google_auth_credentials = grpc.metadata_call_credentials(metadata_plugin)

    # if `ssl_credentials` is set, use `grpc.composite_channel_credentials` instead of
    # `grpc.compute_engine_channel_credentials` as the former supports passing
    # `ssl_credentials` via `channel_credentials` which is needed for mTLS.
    if ssl_credentials:
        # Combine the ssl credentials and the authorization credentials.
        # See https://grpc.github.io/grpc/python/grpc.html#grpc.composite_channel_credentials
        return grpc.composite_channel_credentials(
            ssl_credentials, google_auth_credentials
        )
    else:
        # Use grpc.compute_engine_channel_credentials in order to support Direct Path.
        # See https://grpc.github.io/grpc/python/grpc.html#grpc.compute_engine_channel_credentials
        # TODO(https://github.com/googleapis/python-api-core/issues/598):
        # Although `grpc.compute_engine_channel_credentials` returns channel credentials
        # outside of a Google Compute Engine environment (GCE), we should determine if
        # there is a way to reliably detect a GCE environment so that
        # `grpc.compute_engine_channel_credentials` is not called outside of GCE.
        return grpc.compute_engine_channel_credentials(google_auth_credentials)


def _setup_direct_path_and_credentials(
    target,
    credentials=None,
    scopes=None,
    ssl_credentials=None,
    credentials_file=None,
    quota_project_id=None,
    default_scopes=None,
    default_host=None,
    attempt_direct_path: Optional[bool] = False,
    attempt_direct_path_xds_over_interconnect: Optional[bool] = None,
    **kwargs,
):
    """Configures credentials, options, and target for DirectPath and Interconnect.

    Args:
        target (str): The target service address in the format 'hostname:port'.
        credentials (google.auth.credentials.Credentials): The credentials. If
            not specified, then this function will attempt to ascertain the
            credentials from the environment using :func:`google.auth.default`.
        scopes (Sequence[str]): A optional list of scopes needed for this
            service. These are only used when credentials are not specified and
            are passed to :func:`google.auth.default`.
        ssl_credentials (grpc.ChannelCredentials): Optional SSL channel
            credentials. This can be used to specify different certificates.
        credentials_file (str): Deprecated. A file with credentials that can be
            loaded with :func:`google.auth.load_credentials_from_file`.
        quota_project_id (str): An optional project to use for billing and quota.
        default_scopes (Sequence[str]): Default scopes passed by a Google client
            library. Use 'scopes' for user-defined scopes.
        default_host (str): The default endpoint. e.g., "pubsub.googleapis.com".
        attempt_direct_path (Optional[bool]): If set, Direct Path will be attempted.
        attempt_direct_path_xds_over_interconnect (Optional[bool]): If set,
            DirectPath over Cloud Interconnect will be attempted using standard
            TLS credentials and ``?force-xds`` C2P target resolution. If None
            (default), the setting is resolved from the
            ``GOOGLE_CLOUD_ENABLE_DIRECT_PATH_XDS_OVER_INTERCONNECT``
            environment variable.
        kwargs: Additional key-word args passed to the channel creation function.

    Returns:
        tuple[str, grpc.ChannelCredentials, dict]: A tuple containing the resolved
            target, composite credentials, and kwargs.

    Raises:
        google.api_core.DuplicateCredentialArgs: If both a credentials object
            and credentials_file are passed.
        ValueError: If `ssl_credentials` is set and `attempt_direct_path` is
            set to `True` without `attempt_direct_path_xds_over_interconnect`.
    """
    if attempt_direct_path or attempt_direct_path_xds_over_interconnect is not None:
        use_dp_interconnect = _resolve_direct_path_interconnect(
            attempt_direct_path_xds_over_interconnect
        )
    else:
        use_dp_interconnect = False

    # If `ssl_credentials` is set and `attempt_direct_path` is set to `True`,
    # raise ValueError as this is not yet supported for GCE ALTS DirectPath.
    # See https://github.com/googleapis/python-api-core/issues/590
    if ssl_credentials and attempt_direct_path and not use_dp_interconnect:
        raise ValueError("Using ssl_credentials with Direct Path is not supported")

    if use_dp_interconnect and ssl_credentials is None:
        ssl_credentials = grpc.ssl_channel_credentials()

    composite_credentials = _create_composite_credentials(
        credentials=credentials,
        credentials_file=credentials_file,
        default_scopes=default_scopes,
        scopes=scopes,
        ssl_credentials=ssl_credentials,
        quota_project_id=quota_project_id,
        default_host=default_host,
    )

    if use_dp_interconnect:
        authority = _extract_direct_path_authority(target)
        if authority:
            existing_options = tuple(kwargs.get("options") or ())
            option_keys = {opt[0] for opt in existing_options}
            if (
                "grpc.ssl_target_name_override" not in option_keys
                and "grpc.default_authority" not in option_keys
            ):
                kwargs["options"] = existing_options + (
                    ("grpc.default_authority", authority),
                )

    if attempt_direct_path or use_dp_interconnect:
        target = _modify_target_for_direct_path(
            target,
            attempt_direct_path_xds_over_interconnect=use_dp_interconnect,
        )
    elif not target.startswith("google-c2p:///"):
        clean_host = _extract_target_host(target)
        if clean_host.endswith("-direct.googleapis.com") and len(clean_host) > len(
            "-direct.googleapis.com"
        ):
            new_host = (
                clean_host.removesuffix("-direct.googleapis.com") + ".googleapis.com"
            )
            target = target.replace(clean_host, new_host, 1)

    return target, composite_credentials, kwargs


def create_channel(
    target,
    credentials=None,
    scopes=None,
    ssl_credentials=None,
    credentials_file=None,
    quota_project_id=None,
    default_scopes=None,
    default_host=None,
    compression=None,
    attempt_direct_path: Optional[bool] = False,
    attempt_direct_path_xds_over_interconnect: Optional[bool] = None,
    **kwargs,
):
    """Create a secure channel with credentials.

    Args:
        target (str): The target service address in the format 'hostname:port'.
        credentials (google.auth.credentials.Credentials): The credentials. If
            not specified, then this function will attempt to ascertain the
            credentials from the environment using :func:`google.auth.default`.
        scopes (Sequence[str]): A optional list of scopes needed for this
            service. These are only used when credentials are not specified and
            are passed to :func:`google.auth.default`.
        ssl_credentials (grpc.ChannelCredentials): Optional SSL channel
            credentials. This can be used to specify different certificates.
        credentials_file (str): A file with credentials that can be loaded with
            :func:`google.auth.load_credentials_from_file`. This argument is
            mutually exclusive with credentials.

            .. warning::
                Important: If you accept a credential configuration (credential JSON/File/Stream)
                from an external source for authentication to Google Cloud Platform, you must
                validate it before providing it to any Google API or client library. Providing an
                unvalidated credential configuration to Google APIs or libraries can compromise
                the security of your systems and data. For more information, refer to
                `Validate credential configurations from external sources`_.

            .. _Validate credential configurations from external sources:

            https://cloud.google.com/docs/authentication/external/externally-sourced-credentials
        quota_project_id (str): An optional project to use for billing and quota.
        default_scopes (Sequence[str]): Default scopes passed by a Google client
            library. Use 'scopes' for user-defined scopes.
        default_host (str): The default endpoint. e.g., "pubsub.googleapis.com".
        compression (grpc.Compression): An optional value indicating the
            compression method to be used over the lifetime of the channel.
        attempt_direct_path (Optional[bool]): If set, Direct Path will be attempted
            when the request is made. Direct Path is only available within a Google
            Compute Engine (GCE) environment and provides a proxyless connection
            which increases the available throughput, reduces latency, and increases
            reliability. Note:

            - This argument should only be set in a GCE environment and for Services
              that are known to support Direct Path.
            - If this argument is set outside of GCE, then this request will fail
              unless the back-end service happens to have configured fall-back to DNS.
            - If the request causes a `ServiceUnavailable` response, it is recommended
              that the client repeat the request with `attempt_direct_path` set to
              `False` as the Service may not support Direct Path.
            - Using `ssl_credentials` with `attempt_direct_path` set to `True` will
              result in `ValueError` as this combination  is not yet supported.
        attempt_direct_path_xds_over_interconnect (Optional[bool]): If set,
            DirectPath over Cloud Interconnect will be attempted using standard
            TLS credentials and ``?force-xds`` C2P target resolution. If None
            (default), the setting is resolved from the
            ``GOOGLE_CLOUD_ENABLE_DIRECT_PATH_XDS_OVER_INTERCONNECT``
            environment variable.

        kwargs: Additional key-word args passed to
            :func:`grpc.secure_channel`.

    Returns:
        grpc.Channel: The created channel.

    Raises:
        google.api_core.DuplicateCredentialArgs: If both a credentials object
            and credentials_file are passed.
        ValueError: If `ssl_credentials` is set and `attempt_direct_path` is
            set to `True` without `attempt_direct_path_xds_over_interconnect`.
    """

    target, composite_credentials, kwargs = _setup_direct_path_and_credentials(
        target=target,
        credentials=credentials,
        scopes=scopes,
        ssl_credentials=ssl_credentials,
        credentials_file=credentials_file,
        quota_project_id=quota_project_id,
        default_scopes=default_scopes,
        default_host=default_host,
        attempt_direct_path=attempt_direct_path,
        attempt_direct_path_xds_over_interconnect=attempt_direct_path_xds_over_interconnect,
        **kwargs,
    )

    return grpc.secure_channel(
        target, composite_credentials, compression=compression, **kwargs
    )


def _modify_target_for_direct_path(
    target: str,
    attempt_direct_path_xds_over_interconnect: Optional[bool] = False,
) -> str:
    """
    Given a target, return a modified version which is compatible with Direct Path.

    Args:
        target (str): The target service address in the format 'hostname[:port]' or
            'dns://hostname[:port]'.
        attempt_direct_path_xds_over_interconnect (Optional[bool]): Whether to
            append ``?force-xds`` for DirectPath over Cloud Interconnect.

    Returns:
        target (str): The target service address which is converted into a format compatible with Direct Path.
            If the target contains `dns:///` or does not contain `:///`, the target will be converted in
            a format compatible with Direct Path; otherwise the original target will be returned as the
            original target may already denote Direct Path.
    """

    # Strip standard URI scheme prefixes ("dns:///", "https://", "http://") if
    # `attempt_direct_path` is enabled, as the Direct Path prefix `google-c2p:///`
    # will be used instead.
    for scheme_prefix in ("dns:///", "https://", "http://"):
        if target.startswith(scheme_prefix):
            target = target.removeprefix(scheme_prefix)
            break

    direct_path_separator = ":///"
    if direct_path_separator not in target:
        if "?" in target:
            host_part, query_part = target.split("?", 1)
            target_without_port = host_part.split("/")[0].split(":")[0]
            target = (
                f"google-c2p{direct_path_separator}{target_without_port}?{query_part}"
            )
        else:
            target_without_port = target.split("/")[0].split(":")[0]
            # Modify the target to use Direct Path by adding the `google-c2p:///` prefix
            target = f"google-c2p{direct_path_separator}{target_without_port}"

    if attempt_direct_path_xds_over_interconnect and target.startswith(
        "google-c2p:///"
    ):
        if "force-xds" not in target:
            separator = "&" if "?" in target else "?"
            target = f"{target}{separator}force-xds"
    return target


def apply_channel_interceptors(
    channel: grpc.Channel,
    interceptors: (
        Sequence[ClientInterceptor | Callable[[grpc.Channel], grpc.Channel]] | None
    ) = None,
) -> grpc.Channel:
    """Applies client interceptors or channel-intercepting callables to a gRPC channel.

    Executes in reverse order so the first interceptor in the sequence becomes the
    outermost layer on outbound requests and the innermost layer on inbound responses,
    aligning with the behavior of ``grpc.intercept_channel``.

    Args:
        channel (grpc.Channel): The channel to intercept.
        interceptors (Optional[Sequence[Union[ClientInterceptor, Callable[[grpc.Channel], grpc.Channel]]]]):
            Additional interceptors (or callables that apply interceptors) to apply to the gRPC channel.

    Returns:
        grpc.Channel: The intercepted channel, or the original channel if no
            interceptors were provided.

    Raises:
        TypeError: If an item in ``interceptors`` is neither a gRPC ClientInterceptor
            nor a Callable[[Channel], Channel].
    """
    if not interceptors:
        return channel

    modified_channel = channel
    # Reverse the inputs to align with the behavior of grpc.create_channel(*interceptors)
    for interceptor in reversed(list(interceptors)):
        if isinstance(interceptor, _CLIENT_INTERCEPTOR_CLASSES):
            modified_channel = grpc.intercept_channel(modified_channel, interceptor)
        elif callable(interceptor):
            interceptor_callable = cast(
                Callable[[grpc.Channel], grpc.Channel], interceptor
            )
            modified_channel = interceptor_callable(modified_channel)
        else:
            raise TypeError(
                f"Expected ClientInterceptor or Callable[[Channel], Channel], got {type(interceptor).__name__}"
            )

    return modified_channel


_MethodCall = collections.namedtuple(
    "_MethodCall", ("request", "timeout", "metadata", "credentials", "compression")
)

_ChannelRequest = collections.namedtuple("_ChannelRequest", ("method", "request"))


class _CallableStub(object):
    """Stub for the grpc.*MultiCallable interfaces."""

    def __init__(self, method, channel):
        self._method = method
        self._channel = channel
        self.response = None
        """Union[protobuf.Message, Callable[protobuf.Message], exception]:
        The response to give when invoking this callable. If this is a
        callable, it will be invoked with the request protobuf. If it's an
        exception, the exception will be raised when this is invoked.
        """
        self.responses = None
        """Iterator[
            Union[protobuf.Message, Callable[protobuf.Message], exception]]:
        An iterator of responses. If specified, self.response will be populated
        on each invocation by calling ``next(self.responses)``."""
        self.requests = []
        """List[protobuf.Message]: All requests sent to this callable."""
        self.calls = []
        """List[Tuple]: All invocations of this callable. Each tuple is the
        request, timeout, metadata, compression, and credentials."""

    def __call__(
        self, request, timeout=None, metadata=None, credentials=None, compression=None
    ):
        self._channel.requests.append(_ChannelRequest(self._method, request))
        self.calls.append(
            _MethodCall(request, timeout, metadata, credentials, compression)
        )
        self.requests.append(request)

        response = self.response
        if self.responses is not None:
            if response is None:
                response = next(self.responses)
            else:
                raise ValueError(
                    "{method}.response and {method}.responses are mutually "
                    "exclusive.".format(method=self._method)
                )

        if callable(response):
            return response(request)

        if isinstance(response, Exception):
            raise response

        if response is not None:
            return response

        raise ValueError('Method stub for "{}" has no response.'.format(self._method))


def _simplify_method_name(method):
    """Simplifies a gRPC method name.

    When gRPC invokes the channel to create a callable, it gives a full
    method name like "/google.pubsub.v1.Publisher/CreateTopic". This
    returns just the name of the method, in this case "CreateTopic".

    Args:
        method (str): The name of the method.

    Returns:
        str: The simplified name of the method.
    """
    return method.rsplit("/", 1).pop()


class ChannelStub(grpc.Channel):
    """A testing stub for the grpc.Channel interface.

    This can be used to test any client that eventually uses a gRPC channel
    to communicate. By passing in a channel stub, you can configure which
    responses are returned and track which requests are made.

    For example:

    .. code-block:: python

        channel_stub = grpc_helpers.ChannelStub()
        client = FooClient(channel=channel_stub)

        channel_stub.GetFoo.response = foo_pb2.Foo(name='bar')

        foo = client.get_foo(labels=['baz'])

        assert foo.name == 'bar'
        assert channel_stub.GetFoo.requests[0].labels = ['baz']

    Each method on the stub can be accessed and configured on the channel.
    Here's some examples of various configurations:

    .. code-block:: python

        # Return a basic response:

        channel_stub.GetFoo.response = foo_pb2.Foo(name='bar')
        assert client.get_foo().name == 'bar'

        # Raise an exception:
        channel_stub.GetFoo.response = NotFound('...')

        with pytest.raises(NotFound):
            client.get_foo()

        # Use a sequence of responses:
        channel_stub.GetFoo.responses = iter([
            foo_pb2.Foo(name='bar'),
            foo_pb2.Foo(name='baz'),
        ])

        assert client.get_foo().name == 'bar'
        assert client.get_foo().name == 'baz'

        # Use a callable

        def on_get_foo(request):
            return foo_pb2.Foo(name='bar' + request.id)

        channel_stub.GetFoo.response = on_get_foo

        assert client.get_foo(id='123').name == 'bar123'
    """

    def __init__(self, responses=[]):
        self.requests = []
        """Sequence[Tuple[str, protobuf.Message]]: A list of all requests made
        on this channel in order. The tuple is of method name, request
        message."""
        self._method_stubs = {}

    def _stub_for_method(self, method):
        method = _simplify_method_name(method)
        self._method_stubs[method] = _CallableStub(method, self)
        return self._method_stubs[method]

    def __getattr__(self, key):
        try:
            return self._method_stubs[key]
        except KeyError:
            raise AttributeError

    def unary_unary(
        self,
        method,
        request_serializer=None,
        response_deserializer=None,
        _registered_method=False,
    ):
        """grpc.Channel.unary_unary implementation."""
        return self._stub_for_method(method)

    def unary_stream(
        self,
        method,
        request_serializer=None,
        response_deserializer=None,
        _registered_method=False,
    ):
        """grpc.Channel.unary_stream implementation."""
        return self._stub_for_method(method)

    def stream_unary(
        self,
        method,
        request_serializer=None,
        response_deserializer=None,
        _registered_method=False,
    ):
        """grpc.Channel.stream_unary implementation."""
        return self._stub_for_method(method)

    def stream_stream(
        self,
        method,
        request_serializer=None,
        response_deserializer=None,
        _registered_method=False,
    ):
        """grpc.Channel.stream_stream implementation."""
        return self._stub_for_method(method)

    def subscribe(self, callback, try_to_connect=False):
        """grpc.Channel.subscribe implementation."""
        pass

    def unsubscribe(self, callback):
        """grpc.Channel.unsubscribe implementation."""
        pass

    def close(self):
        """grpc.Channel.close implementation."""
        pass


class _BaseRotatingMultiCallable:
    """Base helper for MultiCallable proxies bound to a _RotatingGrpcChannel."""

    # Name of the grpc.Channel method that builds the inner multicallable.
    _factory_name: str

    def __init__(
        self,
        rotating_channel: "_RotatingGrpcChannel",
        method: str,
        request_serializer: Optional[Callable] = None,
        response_deserializer: Optional[Callable] = None,
        _registered_method: Optional[bool] = False,
    ) -> None:
        self._rotating_channel = rotating_channel
        self._method = method
        self._request_serializer = request_serializer
        self._response_deserializer = response_deserializer
        self._registered_method = _registered_method

    def _resolve_callable(self) -> Any:
        rotating = self._rotating_channel
        # grpcio before 1.63 doesn't accept _registered_method, so only pass it
        # when True. GAPIC leaves it False.
        if not self._registered_method:
            channel, _ = rotating._get_active_channel_and_generation()
            factory = getattr(channel, self._factory_name)
            return factory(
                self._method, self._request_serializer, self._response_deserializer
            )
        # grpcio crashes if a registered call handle is requested on a closed
        # channel, so check and register under the lock.
        with rotating._lock:
            if rotating._closed:
                raise ValueError("Cannot invoke RPC on closed channel!")
            rotating._replace_stale_channel_locked()
            factory = getattr(rotating._channel, self._factory_name)
            return factory(
                self._method,
                self._request_serializer,
                self._response_deserializer,
                _registered_method=True,
            )


class _RotatingUnaryUnaryMultiCallable(
    _BaseRotatingMultiCallable, grpc.UnaryUnaryMultiCallable
):
    """UnaryUnaryMultiCallable proxy that resolves the active inner channel per call."""

    _factory_name = "unary_unary"

    def __call__(
        self,
        request: Any,
        timeout: Optional[float] = None,
        metadata: Optional[Any] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None,
    ) -> Any:
        response, _ = self.with_call(
            request,
            timeout=timeout,
            metadata=metadata,
            credentials=credentials,
            wait_for_ready=wait_for_ready,
            compression=compression,
        )
        return response

    def with_call(
        self,
        request: Any,
        timeout: Optional[float] = None,
        metadata: Optional[Any] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None,
    ) -> Tuple[Any, grpc.Call]:
        return self._resolve_callable().with_call(
            request,
            timeout=timeout,
            metadata=metadata,
            credentials=credentials,
            wait_for_ready=wait_for_ready,
            compression=compression,
        )

    def future(
        self,
        request: Any,
        timeout: Optional[float] = None,
        metadata: Optional[Any] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None,
    ) -> grpc.Future:
        return self._resolve_callable().future(
            request,
            timeout=timeout,
            metadata=metadata,
            credentials=credentials,
            wait_for_ready=wait_for_ready,
            compression=compression,
        )


class _RotatingUnaryStreamMultiCallable(
    _BaseRotatingMultiCallable, grpc.UnaryStreamMultiCallable
):
    """UnaryStreamMultiCallable proxy that resolves the active inner channel per call."""

    _factory_name = "unary_stream"

    def __call__(
        self,
        request: Any,
        timeout: Optional[float] = None,
        metadata: Optional[Any] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None,
    ) -> Any:
        return self._resolve_callable()(
            request,
            timeout=timeout,
            metadata=metadata,
            credentials=credentials,
            wait_for_ready=wait_for_ready,
            compression=compression,
        )


class _RotatingStreamUnaryMultiCallable(
    _BaseRotatingMultiCallable, grpc.StreamUnaryMultiCallable
):
    """StreamUnaryMultiCallable proxy that resolves the active inner channel per call."""

    _factory_name = "stream_unary"

    def __call__(
        self,
        request_iterator: Iterator[Any],
        timeout: Optional[float] = None,
        metadata: Optional[Any] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None,
    ) -> Any:
        response, _ = self.with_call(
            request_iterator,
            timeout=timeout,
            metadata=metadata,
            credentials=credentials,
            wait_for_ready=wait_for_ready,
            compression=compression,
        )
        return response

    def with_call(
        self,
        request_iterator: Iterator[Any],
        timeout: Optional[float] = None,
        metadata: Optional[Any] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None,
    ) -> Tuple[Any, grpc.Call]:
        return self._resolve_callable().with_call(
            request_iterator,
            timeout=timeout,
            metadata=metadata,
            credentials=credentials,
            wait_for_ready=wait_for_ready,
            compression=compression,
        )

    def future(
        self,
        request_iterator: Iterator[Any],
        timeout: Optional[float] = None,
        metadata: Optional[Any] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None,
    ) -> grpc.Future:
        return self._resolve_callable().future(
            request_iterator,
            timeout=timeout,
            metadata=metadata,
            credentials=credentials,
            wait_for_ready=wait_for_ready,
            compression=compression,
        )


class _RotatingStreamStreamMultiCallable(
    _BaseRotatingMultiCallable, grpc.StreamStreamMultiCallable
):
    """StreamStreamMultiCallable proxy that resolves the active inner channel per call."""

    _factory_name = "stream_stream"

    def __call__(
        self,
        request_iterator: Iterator[Any],
        timeout: Optional[float] = None,
        metadata: Optional[Any] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None,
    ) -> Any:
        return self._resolve_callable()(
            request_iterator,
            timeout=timeout,
            metadata=metadata,
            credentials=credentials,
            wait_for_ready=wait_for_ready,
            compression=compression,
        )


class _RotatingGrpcChannel(grpc.Channel):
    """A gRPC channel wrapper that supports swapping the underlying channel.

    Supports both mTLS client certificate rotation (when ``cert_manager`` is
    provided) and caller-driven channel replacement via :meth:`create_channel`
    and :meth:`swap_channel` (when ``cert_manager`` is ``None``).
    """

    def __init__(
        self,
        channel_factory: Callable[[], grpc.Channel],
        cert_manager: Optional[Any] = None,
    ) -> None:
        self._channel_factory = channel_factory
        self._cert_manager = cert_manager
        self._lock = threading.Lock()
        self._subscribers: List[
            Tuple[Callable[[grpc.ChannelConnectivity], None], bool]
        ] = []
        # Certificate generation of each channel returned by create_channel().
        self._created_generations: "weakref.WeakKeyDictionary[grpc.Channel, int]" = (
            weakref.WeakKeyDictionary()
        )
        self._closed = False
        self._channel, self._channel_generation_id = self._build_channel()

    @property
    def channel(self) -> grpc.Channel:
        """Return the active inner gRPC channel."""
        return self._channel

    def _current_generation(self) -> int:
        return self._cert_manager.generation_id if self._cert_manager is not None else 0

    def _build_channel(self) -> Tuple[grpc.Channel, int]:
        # Read the generation before building, so a channel built mid-rotation
        # is tagged with the older generation and replaced on the next check.
        generation = self._current_generation()
        return self._channel_factory(), generation

    def create_channel(self) -> grpc.Channel:
        """Create a fresh inner gRPC channel using ``channel_factory``.

        The channel is not installed. Pass it to :meth:`swap_channel` to make
        it active.

        Returns:
            grpc.Channel: The new channel, not yet installed.

        Raises:
            ValueError: If the channel was closed.
        """
        with self._lock:
            if self._closed:
                raise ValueError("Cannot create an inner channel after close().")
        channel, generation = self._build_channel()
        with self._lock:
            if not self._closed:
                self._created_generations[channel] = generation
                return channel
        channel.close()
        raise ValueError("Cannot create an inner channel after close().")

    def _install_channel_locked(
        self, new_channel: grpc.Channel, generation: int
    ) -> grpc.Channel:
        old_channel = self._channel
        for callback, try_to_connect in self._subscribers:
            old_channel.unsubscribe(callback)
            new_channel.subscribe(callback, try_to_connect=try_to_connect)
        # Write the channel before its generation. Callers read them without
        # the lock in the opposite order, and the generation never goes down,
        # so they never pair a channel with a newer generation than the one it
        # was built with.
        self._channel = new_channel
        self._channel_generation_id = generation
        return old_channel

    def swap_channel(self, new_channel: Optional[grpc.Channel] = None) -> grpc.Channel:
        """Replace the active inner channel and return the previous channel.

        The previous channel is not closed, so calls running on it can finish.

        Args:
            new_channel (Optional[grpc.Channel]): The channel to install,
                usually one returned by :meth:`create_channel`. If it was
                created before the latest certificate rotation, it is closed
                and a new channel is built instead. A channel that did not
                come from :meth:`create_channel` is assumed to use the current
                certificate. If ``None``, a new channel is built.

        Returns:
            grpc.Channel: The previous inner channel.

        Raises:
            ValueError: If the channel was closed.
        """
        stale_channel: Optional[grpc.Channel] = None
        with self._lock:
            if self._closed:
                raise ValueError("Cannot swap the inner channel after close().")
            current = self._current_generation()
            if new_channel is None:
                new_channel, generation = self._build_channel()
            else:
                generation = self._created_generations.get(new_channel, current)
                if generation < current:
                    stale_channel = new_channel
                    new_channel, generation = self._build_channel()
                    self._created_generations.pop(stale_channel, None)
                else:
                    self._created_generations.pop(new_channel, None)
            old_channel = self._install_channel_locked(new_channel, generation)
        if stale_channel is not None:
            stale_channel.close()
        return old_channel

    def _replace_stale_channel_locked(self) -> None:
        """Install a channel built with the current certificate if needed."""
        if self._closed:
            return
        if self._current_generation() > self._channel_generation_id:
            self._install_channel_locked(*self._build_channel())

    def _get_active_channel_and_generation(self) -> Tuple[grpc.Channel, int]:
        gen = self._channel_generation_id
        channel = self._channel
        if self._current_generation() <= gen:
            return channel, gen
        with self._lock:
            self._replace_stale_channel_locked()
            return self._channel, self._channel_generation_id

    def unary_unary(
        self,
        method: str,
        request_serializer: Optional[Callable] = None,
        response_deserializer: Optional[Callable] = None,
        _registered_method: Optional[bool] = False,
    ) -> grpc.UnaryUnaryMultiCallable:
        return _RotatingUnaryUnaryMultiCallable(
            self,
            method,
            request_serializer,
            response_deserializer,
            _registered_method,
        )

    def unary_stream(
        self,
        method: str,
        request_serializer: Optional[Callable] = None,
        response_deserializer: Optional[Callable] = None,
        _registered_method: Optional[bool] = False,
    ) -> grpc.UnaryStreamMultiCallable:
        return _RotatingUnaryStreamMultiCallable(
            self,
            method,
            request_serializer,
            response_deserializer,
            _registered_method,
        )

    def stream_unary(
        self,
        method: str,
        request_serializer: Optional[Callable] = None,
        response_deserializer: Optional[Callable] = None,
        _registered_method: Optional[bool] = False,
    ) -> grpc.StreamUnaryMultiCallable:
        return _RotatingStreamUnaryMultiCallable(
            self,
            method,
            request_serializer,
            response_deserializer,
            _registered_method,
        )

    def stream_stream(
        self,
        method: str,
        request_serializer: Optional[Callable] = None,
        response_deserializer: Optional[Callable] = None,
        _registered_method: Optional[bool] = False,
    ) -> grpc.StreamStreamMultiCallable:
        return _RotatingStreamStreamMultiCallable(
            self,
            method,
            request_serializer,
            response_deserializer,
            _registered_method,
        )

    def subscribe(
        self,
        callback: Callable[[grpc.ChannelConnectivity], None],
        try_to_connect: bool = False,
    ) -> None:
        with self._lock:
            if self._closed:
                return
            self._channel.subscribe(callback, try_to_connect=try_to_connect)
            self._subscribers.append((callback, try_to_connect))

    def unsubscribe(self, callback: Callable[[grpc.ChannelConnectivity], None]) -> None:
        with self._lock:
            for index, (subscribed_cb, _) in enumerate(self._subscribers):
                if subscribed_cb == callback:
                    self._subscribers.pop(index)
                    break
            self._channel.unsubscribe(callback)

    def close(self) -> None:
        """Close the active inner channel and stop building new ones.

        Calls still running on channels that were replaced by a swap are not
        cancelled. They finish on their own.
        """
        with self._lock:
            self._closed = True
            self._subscribers.clear()
            self._channel.close()

    def __enter__(self) -> "_RotatingGrpcChannel":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Literal[False]:
        self.close()
        return False

    def __getattr__(self, name: str) -> Any:
        # Only reached when normal lookup fails. If _channel itself is missing
        # (copy.copy, unpickling, or a failed __init__), stop here instead of
        # recursing.
        if name == "_channel":
            raise AttributeError(name)
        return getattr(self._channel, name)
