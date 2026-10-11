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

"""Zero-copy deserializer for ``BidiReadObjectResponse`` messages.

The generated gRPC stub parses every response with proto-plus over upb, which
copies each data chunk twice (into the upb arena, then into a Python ``bytes``
for ``checksummed_data.content``) on the event-loop thread. Data responses are
structurally tiny apart from the chunk itself, so this module walks the wire
format directly and exposes ``content`` as a ``memoryview`` of the raw message.
Responses carrying object metadata (the first message of a stream opened
without a read handle) or anything unexpected fall back to the generated
parser, so callers never see a difference other than the type of ``content``.

:func:`wrapped_rpc` builds the matching ``BidiReadObject`` callable for a
transport; :class:`~google.cloud.storage.asyncio.async_read_object_stream._AsyncReadObjectStream`
prefers it over the generated one whenever :func:`is_enabled` holds for the
downloader's ``zero_copy`` argument.
"""

import os
import weakref

import google_crc32c
from google.api_core import gapic_v1

from google.cloud import _storage_v2
from google.cloud._storage_v2.services.storage.transports.base import (
    DEFAULT_CLIENT_INFO,
)
from google.cloud._storage_v2.services.storage.transports.grpc_asyncio import (
    StorageGrpcAsyncIOTransport,
)

# Process-wide default for downloaders created without an explicit ``zero_copy``
# argument. Accepted spellings match ``_opentelemetry_tracing._parse_bool_env``.
_ENV_VAR = "GOOGLE_CLOUD_STORAGE_ZERO_COPY_BIDI_READ"
_ENABLED_VALUES = ("1", "true", "yes", "on")

# Protobuf wire types (low 3 bits of a field tag): varint, 8-byte fixed,
# length-delimited, 4-byte fixed. Groups (3, 4) are left to the generated parser.
_WT_VARINT, _WT_I64, _WT_LEN, _WT_I32 = 0, 1, 2, 5


class _ReadRange:
    __slots__ = ("read_offset", "read_length", "read_id")

    def __init__(self):
        self.read_offset = 0
        self.read_length = 0
        self.read_id = 0


class _ChecksummedData:
    __slots__ = ("content", "crc32c", "_has_crc32c")

    def __init__(self):
        self.content = memoryview(b"")
        self.crc32c = 0
        self._has_crc32c = False

    def HasField(self, name):
        if name == "crc32c":
            return self._has_crc32c
        raise ValueError(f"Unknown field {name!r}")


class _ObjectRangeData:
    __slots__ = (
        "checksummed_data",
        "read_range",
        "range_end",
        "_has_checksummed_data",
        "_has_read_range",
    )

    def __init__(self):
        self.checksummed_data = _ChecksummedData()
        self.read_range = _ReadRange()
        self.range_end = False
        self._has_checksummed_data = False
        self._has_read_range = False

    def HasField(self, name):
        if name == "checksummed_data":
            return self._has_checksummed_data
        if name == "read_range":
            return self._has_read_range
        raise ValueError(f"Unknown field {name!r}")


class _ZeroCopyBidiReadObjectResponse:
    """Duck-typed stand-in for a ``BidiReadObjectResponse`` without metadata.

    Only the attributes the async read path uses are provided:
    ``object_data_ranges``, ``read_handle``, ``metadata`` (always ``None``),
    ``HasField`` and ``_pb`` (itself, so code that unwraps proto-plus messages
    keeps working).
    """

    __slots__ = ("object_data_ranges", "read_handle", "metadata")

    def __init__(self, ranges, read_handle):
        self.object_data_ranges = ranges
        self.read_handle = read_handle
        self.metadata = None

    @property
    def _pb(self):
        return self

    def HasField(self, name):
        if name == "read_handle":
            return self.read_handle is not None
        if name == "metadata":
            return False
        raise ValueError(f"Unknown field {name!r}")


class _Malformed(ValueError):
    """Raised when the wire bytes do not look like a well-formed message."""


# A 10-byte varint carries 70 bits; like upb, keep only the low 64.
_UINT64_MASK = (1 << 64) - 1
# A field tag (``field_number << 3 | wire_type``) must fit in 32 bits, as in upb.
_UINT32_MAX = (1 << 32) - 1


def _varint(buf, i, end):
    """Decode the varint at ``buf[i]``; it must end at or before ``end``.

    Like upb, accept up to ten bytes and keep only the low 64 bits.
    """
    shift = 0
    result = 0
    while True:
        b = buf[i]
        i += 1
        result |= (b & 0x7F) << shift
        if b < 0x80:
            break
        shift += 7
        if shift > 63:
            raise _Malformed("varint longer than 10 bytes")
    if i > end:
        raise _Malformed("varint runs past its enclosing message")
    return result & _UINT64_MASK, i


def _int64(value):
    """Reinterpret the low 64 bits of a varint as a signed integer."""
    return value - (1 << 64) if value >> 63 else value


def _tag(buf, i, end):
    """Decode a field tag at ``buf[i]`` into ``(field_number, wire_type, i)``.

    upb rejects field number 0, tags above 32 bits and tags encoded in more
    than five bytes.
    """
    start = i
    tag, i = _varint(buf, i, end)
    if tag < 8 or tag > _UINT32_MAX or i - start > 5:
        raise _Malformed("invalid field tag")
    return tag >> 3, tag & 7, i


def _length_prefixed(buf, i, end):
    """Return ``(start, stop)`` of the length-delimited field body at ``i``."""
    n, i = _varint(buf, i, end)
    stop = i + n
    if stop > end:
        raise _Malformed("field runs past its enclosing message")
    return i, stop


def _skip(buf, i, wt, end):
    if wt == _WT_VARINT:
        return _varint(buf, i, end)[1]
    if wt == _WT_LEN:
        return _length_prefixed(buf, i, end)[1]
    if wt == _WT_I64:
        i += 8
    elif wt == _WT_I32:
        i += 4
    else:
        raise _Malformed(f"unsupported wire type {wt}")
    if i > end:
        raise _Malformed("field runs past its enclosing message")
    return i


# The sub-message parsers fill in an existing object so that a singular
# embedded message occurring more than once is merged, as the generated
# parser does, instead of replacing what the earlier occurrence set.


def _parse_read_range(rr, buf, i, end):
    while i < end:
        f, wt, i = _tag(buf, i, end)
        if wt == _WT_VARINT:
            v, i = _varint(buf, i, end)
            if f == 1:
                rr.read_offset = _int64(v)
            elif f == 2:
                rr.read_length = _int64(v)
            elif f == 3:
                rr.read_id = _int64(v)
        else:
            i = _skip(buf, i, wt, end)


def _parse_checksummed(cd, buf, mv, i, end):
    while i < end:
        f, wt, i = _tag(buf, i, end)
        if f == 1 and wt == _WT_LEN:
            start, i = _length_prefixed(buf, i, end)
            cd.content = mv[start:i]
        elif f == 2 and wt == _WT_I32:
            if i + 4 > end:
                raise _Malformed("crc32c runs past its enclosing message")
            cd.crc32c = int.from_bytes(buf[i : i + 4], "little")
            cd._has_crc32c = True
            i += 4
        else:
            i = _skip(buf, i, wt, end)


def _parse_range_data(buf, mv, i, end):
    rd = _ObjectRangeData()
    while i < end:
        f, wt, i = _tag(buf, i, end)
        if wt == _WT_LEN:
            start, i = _length_prefixed(buf, i, end)
            if f == 1:
                _parse_checksummed(rd.checksummed_data, buf, mv, start, i)
                rd._has_checksummed_data = True
            elif f == 2:
                _parse_read_range(rd.read_range, buf, start, i)
                rd._has_read_range = True
        elif f == 3 and wt == _WT_VARINT:
            v, i = _varint(buf, i, end)
            rd.range_end = bool(v)
        else:
            i = _skip(buf, i, wt, end)
    return rd


def _parse_handle(handle, buf, i, end):
    while i < end:
        f, wt, i = _tag(buf, i, end)
        if f == 1 and wt == _WT_LEN:
            start, i = _length_prefixed(buf, i, end)
            handle = bytes(buf[start:i])
        else:
            i = _skip(buf, i, wt, end)
    return handle


_generated_deserialize = _storage_v2.BidiReadObjectResponse.deserialize


def deserialize(buf):
    """Parse a serialized ``BidiReadObjectResponse``; chunk payloads alias ``buf``.

    Anything that is not a plain data response (object metadata present, or
    bytes that do not parse cleanly) is handed to the generated parser, which
    either produces the real message or raises its usual ``DecodeError``. So
    is any buffer that is not an immutable ``bytes``: the chunks alias ``buf``,
    which is only safe when nothing can change or recycle it.
    """
    if type(buf) is not bytes:
        return _generated_deserialize(buf)
    try:
        mv = memoryview(buf)
        n = len(buf)
        i = 0
        ranges = []
        handle = None
        while i < n:
            f, wt, i = _tag(buf, i, n)
            if wt == _WT_LEN:
                start, end = _length_prefixed(buf, i, n)
                if f == 6:
                    ranges.append(_parse_range_data(buf, mv, start, end))
                elif f == 7:
                    handle = _parse_handle(handle or b"", buf, start, end)
                elif f == 4:
                    return _generated_deserialize(buf)
                i = end
            else:
                i = _skip(buf, i, wt, n)
        if handle is not None:
            # A real message: the handle is stored and passed back in the
            # BidiReadObjectSpec of the next open, which only accepts the
            # proto type.
            handle = _storage_v2.BidiReadHandle(handle=handle)
        return _ZeroCopyBidiReadObjectResponse(ranges, handle)
    except Exception:
        return _generated_deserialize(buf)


def is_supported():
    """Whether the installed ``google_crc32c`` can hash ``memoryview`` inputs.

    The parser hands chunk payloads to the read path as ``memoryview`` objects
    and checksum verification feeds them to ``google_crc32c``; releases that
    only accept ``bytes`` would fail on them, so the parser is never used
    without this capability.
    """
    try:
        google_crc32c.value(memoryview(b"\0"))
    except Exception:
        return False
    return True


def is_enabled(zero_copy=None):
    """Whether a stream should use the zero-copy parser.

    ``zero_copy`` is the downloader's argument: ``True`` asks for the parser,
    ``False`` keeps the generated one, ``None`` defers to the
    ``GOOGLE_CLOUD_STORAGE_ZERO_COPY_BIDI_READ`` environment variable. Either
    way the parser is used only when :func:`is_supported` holds.
    """
    if zero_copy is None:
        zero_copy = os.environ.get(_ENV_VAR, "").strip().lower() in _ENABLED_VALUES
    return bool(zero_copy) and is_supported()


_rpcs = weakref.WeakKeyDictionary()


def wrapped_rpc(transport, zero_copy=None, client_info=None):
    """Return the zero-copy ``BidiReadObject`` callable for ``transport``.

    The callable is the generated transport's stub with :func:`deserialize`
    swapped in, wrapped exactly like ``transport._wrapped_methods`` entries
    (error mapping, no default retry or timeout, the ``x-goog-api-client``
    header from ``client_info``, the transport's own by default). Returns
    ``None`` when :func:`is_enabled` is false for ``zero_copy`` or
    ``transport`` is not the generated grpc_asyncio transport, in which case
    callers should use the generated wrapped method.
    """
    if not isinstance(transport, StorageGrpcAsyncIOTransport) or not is_enabled(
        zero_copy
    ):
        return None
    rpc = _rpcs.get(transport)
    if rpc is None:
        stub = transport._logged_channel.stream_stream(
            "/google.storage.v2.Storage/BidiReadObject",
            request_serializer=_storage_v2.BidiReadObjectRequest.serialize,
            response_deserializer=deserialize,
        )
        rpc = gapic_v1.method_async.wrap_method(
            stub, default_timeout=None, client_info=client_info or DEFAULT_CLIENT_INFO
        )
        _rpcs[transport] = rpc
    return rpc
