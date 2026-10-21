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
"""gRPC client surface against the accelerator daemon's UDS server.

The daemon registers the standard ``google.bigtable.v2.Bigtable`` service on
its Unix domain socket, so we register the same stubs the gapic transport
uses and send V2 protos verbatim. No translation in either direction.
"""

from __future__ import annotations

from google.cloud.bigtable.data._accelerator._health import (
    HEALTH_CHECK_METHOD,
    ServingStatus,
    parse_health_response,
    serialize_health_request,
)
from google.cloud.bigtable.data._cross_sync import CrossSync
from google.cloud.bigtable_v2.types import (
    MutateRowRequest,
    MutateRowResponse,
    ReadRowsRequest,
    ReadRowsResponse,
)

if CrossSync.is_async:
    from grpc.aio import insecure_channel
else:
    from grpc import insecure_channel

__CROSS_SYNC_OUTPUT__ = "google.cloud.bigtable.data._sync_autogen._accelerator_client"

_MUTATE_ROW_METHOD = "/google.bigtable.v2.Bigtable/MutateRow"
_READ_ROWS_METHOD = "/google.bigtable.v2.Bigtable/ReadRows"


@CrossSync.convert_class(sync_name="_AcceleratorClient")
class _AsyncAcceleratorClient:
    """Thin gRPC client bound to the daemon's UDS.

    Owns the channel and the per-RPC stubs. The set of registered RPCs is the
    same set the daemon supports today; the routing layer
    (``_accelerator/_routing.py``) decides which calls reach this object.
    """

    def __init__(self, uds_path: str, auth_secret: str):
        self._uds_path = uds_path
        self._metadata = (("x-accelerator-token", auth_secret),)
        self._channel = insecure_channel(f"unix://{uds_path}")
        self._mutate_row_stub = self._channel.unary_unary(
            _MUTATE_ROW_METHOD,
            request_serializer=MutateRowRequest.serialize,
            response_deserializer=MutateRowResponse.deserialize,
        )
        self._read_rows_stub = self._channel.unary_stream(
            _READ_ROWS_METHOD,
            request_serializer=ReadRowsRequest.serialize,
            response_deserializer=ReadRowsResponse.deserialize,
        )
        # Hand-rolled codec instead of the generated health stubs, which live in
        # a distribution we don't depend on. See ``_accelerator/_health.py``.
        self._health_stub = self._channel.unary_unary(
            HEALTH_CHECK_METHOD,
            request_serializer=serialize_health_request,
            response_deserializer=parse_health_response,
        )

    @property
    def uds_path(self) -> str:
        return self._uds_path

    @CrossSync.convert
    async def mutate_row(
        self, request: MutateRowRequest, *, timeout: float | None = None
    ) -> MutateRowResponse:
        return await self._mutate_row_stub(
            request, timeout=timeout, metadata=self._metadata
        )

    @CrossSync.convert
    async def read_rows(
        self, request: ReadRowsRequest, *, timeout: float | None = None
    ):
        """Open the server-streaming ReadRows RPC against the daemon.

        Returns the streaming call object — callers iterate it (``async for``
        in async, ``for`` in sync) to consume ``ReadRowsResponse`` messages.
        Shape matches what ``_gapic_client.read_rows`` returns so the existing
        chunk-merging machinery in ``_read_rows.py`` works unchanged.
        """
        return self._read_rows_stub(request, timeout=timeout, metadata=self._metadata)

    @CrossSync.convert
    async def check_health(self, *, timeout: float | None = None) -> ServingStatus:
        """Probe the daemon's overall serving status.

        The daemon answers this out of its own process without touching a
        session, the Channel, or the network, so how long it takes is almost
        purely a measure of how contended that process is. That makes the
        ``timeout`` the real signal here, more than the returned status.
        """
        return await self._health_stub(None, timeout=timeout, metadata=self._metadata)

    @CrossSync.convert
    async def close(self) -> None:
        if CrossSync.is_async:
            await self._channel.close()
        else:
            self._channel.close()
