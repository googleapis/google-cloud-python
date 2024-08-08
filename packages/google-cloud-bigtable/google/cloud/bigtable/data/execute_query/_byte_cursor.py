# Copyright 2024 Google LLC
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

from typing import Any, Generic, Optional, TypeVar

from google.cloud.bigtable_v2 import ExecuteQueryResponse
from google.cloud.bigtable.data.execute_query.metadata import (
    Metadata,
    _pb_metadata_to_metadata_types,
)

MT = TypeVar("MT", bound=Metadata)  # metadata type


class _ByteCursor(Generic[MT]):
    """
    Buffers bytes from `ExecuteQuery` responses until resume_token is received or end-of-stream
    is reached. :class:`google.cloud.bigtable_v2.types.bigtable.ExecuteQueryResponse` obtained from
    the server should be passed to ``consume`` or ``consume_metadata`` methods and its non-None
    results should be passed to appropriate
    :class:`google.cloud.bigtable.execute_query_reader._Reader` for parsing gathered bytes.

    This class consumes data obtained externally to be usable in both sync and async clients.

    See :class:`google.cloud.bigtable.execute_query_reader._Reader` for more context.
    """

    def __init__(self):
        self._metadata: Optional[MT] = None
        self._buffer = bytearray()
        self._resume_token = None
        self._last_response_results_field = None

    @property
    def metadata(self) -> Optional[MT]:
        """
        Returns:
            Metadata or None: Metadata read from the first response of the stream
                or None if no response was consumed yet.
        """
        return self._metadata

    def prepare_for_new_request(self):
        """
        Prepares this ``_ByteCursor`` for retrying an ``ExecuteQuery`` request.

        Clears internal buffers of this ``_ByteCursor`` and returns last received
        ``resume_token`` to be used in retried request.

        This is the only method that returns ``resume_token`` to the user.
        Returning the token to the user is tightly coupled with clearing internal
        buffers to prevent accidental retry without clearing the state, what would
        cause invalid results. ``resume_token`` are not needed in other cases,
        thus they is no separate getter for it.

        Returns:
            bytes: Last received resume_token.
        """
        self._buffer = bytearray()
        # metadata is sent in the first response in a stream,
        # if we've already received one, but it was not already commited
        # by a subsequent resume_token, then we should clear it as well.
        if not self._resume_token:
            self._metadata = None

        return self._resume_token

    def consume_metadata(self, response: ExecuteQueryResponse) -> None:
        """
        Reads metadata from first response of ``ExecuteQuery`` responses stream.
        Should be called only once.

        Args:
            response (google.cloud.bigtable_v2.types.bigtable.ExecuteQueryResponse): First response
                from the stream.

        Raises:
            ValueError: If this method was already called or if metadata received from the server
                cannot be parsed.
        """
        if self._metadata is not None:
            raise ValueError("Invalid state - metadata already consumed")

        if "metadata" in response:
            metadata: Any = _pb_metadata_to_metadata_types(response.metadata)
            self._metadata = metadata
        else:
            raise ValueError("Invalid parameter - response without metadata")

        return None

    def consume(self, response: ExecuteQueryResponse) -> Optional[bytes]:
        """
        Reads results bytes from an ``ExecuteQuery`` response and adds them to a buffer.

        If the response contains a ``resume_token``:
        - the ``resume_token`` is saved in this ``_ByteCursor``, and
        - internal buffers are flushed and returned to the caller.

        ``resume_token`` is not available directly, but can be retrieved by calling
        :meth:`._ByteCursor.prepare_for_new_request` when preparing to retry a request.

        Args:
            response (google.cloud.bigtable_v2.types.bigtable.ExecuteQueryResponse):
                Response obtained from the stream.

        Returns:
            bytes or None: bytes if buffers were flushed or None otherwise.

        Raises:
            ValueError: If provided ``ExecuteQueryResponse`` is not valid
                or contains bytes representing response of a different kind than previously
                processed responses.
        """
        response_pb = response._pb  # proto-plus attribute retrieval is slow.

        if response_pb.HasField("results"):
            results = response_pb.results
            if results.HasField("proto_rows_batch"):
                self._buffer.extend(results.proto_rows_batch.batch_data)

            if results.resume_token:
                self._resume_token = results.resume_token

                if self._buffer:
                    return_value = memoryview(self._buffer)
                    self._buffer = bytearray()
                    return return_value
        elif response_pb.HasField("metadata"):
            self.consume_metadata(response)
        else:
            raise ValueError(f"Invalid ExecuteQueryResponse: {response}")
        return None
