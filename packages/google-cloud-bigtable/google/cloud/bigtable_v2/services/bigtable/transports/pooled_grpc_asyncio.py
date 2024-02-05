# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
import asyncio
import warnings
from functools import partialmethod
from functools import partial
from typing import (
    Awaitable,
    Callable,
    Dict,
    Optional,
    Sequence,
    Tuple,
    Union,
    List,
    Type,
)

from google.api_core import gapic_v1
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.bigtable_v2.types import bigtable
from .base import BigtableTransport, DEFAULT_CLIENT_INFO
from .grpc_asyncio import BigtableGrpcAsyncIOTransport


class PooledMultiCallable:
    def __init__(self, channel_pool: "PooledChannel", *args, **kwargs):
        self._init_args = args
        self._init_kwargs = kwargs
        self.next_channel_fn = channel_pool.next_channel


class PooledUnaryUnaryMultiCallable(PooledMultiCallable, aio.UnaryUnaryMultiCallable):
    def __call__(self, *args, **kwargs) -> aio.UnaryUnaryCall:
        return self.next_channel_fn().unary_unary(
            *self._init_args, **self._init_kwargs
        )(*args, **kwargs)


class PooledUnaryStreamMultiCallable(PooledMultiCallable, aio.UnaryStreamMultiCallable):
    def __call__(self, *args, **kwargs) -> aio.UnaryStreamCall:
        return self.next_channel_fn().unary_stream(
            *self._init_args, **self._init_kwargs
        )(*args, **kwargs)


class PooledStreamUnaryMultiCallable(PooledMultiCallable, aio.StreamUnaryMultiCallable):
    def __call__(self, *args, **kwargs) -> aio.StreamUnaryCall:
        return self.next_channel_fn().stream_unary(
            *self._init_args, **self._init_kwargs
        )(*args, **kwargs)


class PooledStreamStreamMultiCallable(
    PooledMultiCallable, aio.StreamStreamMultiCallable
):
    def __call__(self, *args, **kwargs) -> aio.StreamStreamCall:
        return self.next_channel_fn().stream_stream(
            *self._init_args, **self._init_kwargs
        )(*args, **kwargs)


class PooledChannel(aio.Channel):
    def __init__(
        self,
        pool_size: int = 3,
        host: str = "bigtable.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        quota_project_id: Optional[str] = None,
        default_scopes: Optional[Sequence[str]] = None,
        scopes: Optional[Sequence[str]] = None,
        default_host: Optional[str] = None,
        insecure: bool = False,
        **kwargs,
    ):
        self._pool: List[aio.Channel] = []
        self._next_idx = 0
        if insecure:
            self._create_channel = partial(aio.insecure_channel, host)
        else:
            self._create_channel = partial(
                grpc_helpers_async.create_channel,
                target=host,
                credentials=credentials,
                credentials_file=credentials_file,
                quota_project_id=quota_project_id,
                default_scopes=default_scopes,
                scopes=scopes,
                default_host=default_host,
                **kwargs,
            )
        for i in range(pool_size):
            self._pool.append(self._create_channel())

    def next_channel(self) -> aio.Channel:
        channel = self._pool[self._next_idx]
        self._next_idx = (self._next_idx + 1) % len(self._pool)
        return channel

    def unary_unary(self, *args, **kwargs) -> grpc.aio.UnaryUnaryMultiCallable:
        return PooledUnaryUnaryMultiCallable(self, *args, **kwargs)

    def unary_stream(self, *args, **kwargs) -> grpc.aio.UnaryStreamMultiCallable:
        return PooledUnaryStreamMultiCallable(self, *args, **kwargs)

    def stream_unary(self, *args, **kwargs) -> grpc.aio.StreamUnaryMultiCallable:
        return PooledStreamUnaryMultiCallable(self, *args, **kwargs)

    def stream_stream(self, *args, **kwargs) -> grpc.aio.StreamStreamMultiCallable:
        return PooledStreamStreamMultiCallable(self, *args, **kwargs)

    async def close(self, grace=None):
        close_fns = [channel.close(grace=grace) for channel in self._pool]
        return await asyncio.gather(*close_fns)

    async def channel_ready(self):
        ready_fns = [channel.channel_ready() for channel in self._pool]
        return asyncio.gather(*ready_fns)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def get_state(self, try_to_connect: bool = False) -> grpc.ChannelConnectivity:
        raise NotImplementedError()

    async def wait_for_state_change(self, last_observed_state):
        raise NotImplementedError()

    async def replace_channel(
        self, channel_idx, grace=None, swap_sleep=1, new_channel=None
    ) -> aio.Channel:
        """
        Replaces a channel in the pool with a fresh one.

        The `new_channel` will start processing new requests immidiately,
        but the old channel will continue serving existing clients for `grace` seconds

        Args:
          channel_idx(int): the channel index in the pool to replace
          grace(Optional[float]): The time to wait until all active RPCs are
            finished. If a grace period is not specified (by passing None for
            grace), all existing RPCs are cancelled immediately.
          swap_sleep(Optional[float]): The number of seconds to sleep in between
            replacing channels and closing the old one
          new_channel(grpc.aio.Channel): a new channel to insert into the pool
            at `channel_idx`. If `None`, a new channel will be created.
        """
        if channel_idx >= len(self._pool) or channel_idx < 0:
            raise ValueError(
                f"invalid channel_idx {channel_idx} for pool size {len(self._pool)}"
            )
        if new_channel is None:
            new_channel = self._create_channel()
        old_channel = self._pool[channel_idx]
        self._pool[channel_idx] = new_channel
        await asyncio.sleep(swap_sleep)
        await old_channel.close(grace=grace)
        return new_channel


class PooledBigtableGrpcAsyncIOTransport(BigtableGrpcAsyncIOTransport):
    """Pooled gRPC AsyncIO backend transport for Bigtable.

    Service for reading from and writing to existing Bigtable
    tables.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.

    This class allows channel pooling, so multiple channels can be used concurrently
    when making requests. Channels are rotated in a round-robin fashion.
    """

    @classmethod
    def with_fixed_size(cls, pool_size) -> Type["PooledBigtableGrpcAsyncIOTransport"]:
        """
        Creates a new class with a fixed channel pool size.

        A fixed channel pool makes compatibility with other transports easier,
        as the initializer signature is the same.
        """

        class PooledTransportFixed(cls):
            __init__ = partialmethod(cls.__init__, pool_size=pool_size)

        PooledTransportFixed.__name__ = f"{cls.__name__}_{pool_size}"
        PooledTransportFixed.__qualname__ = PooledTransportFixed.__name__
        return PooledTransportFixed

    @classmethod
    def create_channel(
        cls,
        pool_size: int = 3,
        host: str = "bigtable.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a PooledChannel object, representing a pool of gRPC AsyncIO channels
        Args:
            pool_size (int): The number of channels in the pool.
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            PooledChannel: a channel pool object
        """

        return PooledChannel(
            pool_size,
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        pool_size: int = 3,
        host: str = "bigtable.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            pool_size (int): the number of grpc channels to maintain in a pool
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
            ValueError: if ``pool_size`` <= 0
        """
        if pool_size <= 0:
            raise ValueError(f"invalid pool_size: {pool_size}")
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if api_mtls_endpoint:
            host = api_mtls_endpoint

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                self._ssl_channel_credentials = SslCredentials().ssl_credentials

        else:
            if client_cert_source_for_mtls and not ssl_channel_credentials:
                cert, key = client_cert_source_for_mtls()
                self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )

        # The base transport sets the host, credentials and scopes
        BigtableTransport.__init__(
            self,
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._quota_project_id = quota_project_id
        self._grpc_channel = type(self).create_channel(
            pool_size,
            self._host,
            # use the credentials which are saved
            credentials=self._credentials,
            # Set ``credentials_file`` to ``None`` here as
            # the credentials that we saved earlier should be used.
            credentials_file=None,
            scopes=self._scopes,
            ssl_credentials=self._ssl_channel_credentials,
            quota_project_id=self._quota_project_id,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def pool_size(self) -> int:
        """The number of grpc channels in the pool."""
        return len(self._grpc_channel._pool)

    @property
    def channels(self) -> List[grpc.Channel]:
        """Acccess the internal list of grpc channels."""
        return self._grpc_channel._pool

    async def replace_channel(
        self, channel_idx, grace=None, swap_sleep=1, new_channel=None
    ) -> aio.Channel:
        """
        Replaces a channel in the pool with a fresh one.

        The `new_channel` will start processing new requests immidiately,
        but the old channel will continue serving existing clients for `grace` seconds

        Args:
          channel_idx(int): the channel index in the pool to replace
          grace(Optional[float]): The time to wait until all active RPCs are
            finished. If a grace period is not specified (by passing None for
            grace), all existing RPCs are cancelled immediately.
          swap_sleep(Optional[float]): The number of seconds to sleep in between
            replacing channels and closing the old one
          new_channel(grpc.aio.Channel): a new channel to insert into the pool
            at `channel_idx`. If `None`, a new channel will be created.
        """
        return await self._grpc_channel.replace_channel(
            channel_idx, grace, swap_sleep, new_channel
        )


__all__ = ("PooledBigtableGrpcAsyncIOTransport",)
