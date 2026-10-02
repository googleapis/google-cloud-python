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

"""Internal structural types shared by the storage implementations."""

from collections.abc import Iterator, Sequence
from typing import TYPE_CHECKING, Any, ParamSpec, Protocol, TypeAlias, TypeVar

# Requests supports separate connect/read timeouts, including unlimited waits.
Timeout: TypeAlias = float | tuple[float | None, float | None] | None


class Checksum(Protocol):
    """Common operations supplied by hashlib and google-crc32c checksums."""

    def update(self, data: bytes, /) -> None:
        pass

    def digest(self) -> bytes:
        pass


class Readable(Protocol):
    """Binary input required by uploads; a full IO implementation is unnecessary."""

    def read(self, size: int = -1, /) -> bytes:
        pass


class Writable(Protocol):
    """Binary output required by downloads, including custom write-only sinks."""

    def write(self, data: bytes, /) -> int | None:
        pass


class SeekableReadable(Readable, Protocol):
    """Binary input supporting resumable uploads and checksum calculation."""

    def seek(self, offset: int, whence: int = 0, /) -> int:
        pass

    def tell(self) -> int:
        pass


# The shared page iterator predates generic annotations. These protocols retain
# its pagination API while specifying the resource returned by each listing.
if TYPE_CHECKING:
    from google.cloud.storage.bucket import Bucket
    from google.cloud.storage.client import Client


_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_P = ParamSpec("_P")


class _StoragePage(Protocol[_T_co]):
    prefixes: tuple[str, ...]
    unreachable: list[str]

    @property
    def num_items(self) -> int:
        pass

    @property
    def remaining(self) -> int:
        pass

    @property
    def raw_page(self) -> dict[str, Any]:
        pass

    def __iter__(self) -> Iterator[_T_co]:
        pass

    def __next__(self) -> _T_co:
        pass


class _StorageIterator(Protocol[_T_co]):
    client: "Client"
    bucket: "Bucket"
    prefixes: set[str]
    page_number: int
    num_results: int
    next_page_token: str | None
    max_results: int | None

    @property
    def pages(self) -> Iterator[_StoragePage[_T_co]]:
        pass

    def __iter__(self) -> Iterator[_T_co]:
        pass

    def __next__(self) -> _T_co:
        pass


AttributeValue: TypeAlias = (
    str
    | bool
    | int
    | float
    | Sequence[str]
    | Sequence[bool]
    | Sequence[int]
    | Sequence[float]
    | None
)


_Request_contra = TypeVar("_Request_contra", contravariant=True)
_Response_co = TypeVar("_Response_co", covariant=True)


class _AsyncBidiRpc(Protocol[_Request_contra, _Response_co]):
    """The proto-plus and end-of-stream interface supported by AsyncBidiRpc.

    api-core annotates this helper with protobuf Message, but GAPIC transports
    also pass proto-plus messages and accept None to close the request stream.
    """

    async def open(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def send(self, request: _Request_contra | None) -> None:
        pass

    async def recv(self) -> _Response_co:
        pass

    @property
    def is_active(self) -> bool:
        pass


class _MediaResponse(Protocol):
    """Response fields read by transport-independent media uploads."""

    @property
    def status_code(self) -> int:
        pass

    @property
    def text(self) -> str:
        pass

    def json(self) -> dict[str, Any]:
        pass


_MediaTransport = TypeVar("_MediaTransport")
_MediaResponseT = TypeVar("_MediaResponseT", bound=_MediaResponse)
