# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct

# NOTE: ``__config__`` **must** be the first import because it (may)
#       modify the search path used to locate shared libraries.
import crc32c.__config__
import crc32c._crc32c_cffi


def extend(crc, chunk):
    """Update an existing CRC checksum with new chunk of data.

    Args
        crc (int): An existing CRC check sum.
        chunk (Union[bytes, List[int], Tuple[int]]): A new chunk of data.
            Intended to be a byte string or similar.

    Returns
        int: New CRC checksum computed by extending existing CRC
        with ``chunk``.
    """
    return crc32c._crc32c_cffi.lib.crc32c_extend(crc, chunk, len(chunk))


def value(chunk):
    """Compute a CRC checksum for a chunk of data.

    Args
        chunk (Union[bytes, List[int], Tuple[int]]): A new chunk of data.
            Intended to be a byte string or similar.

    Returns
        int: New CRC checksum computed for ``chunk``.
    """
    return crc32c._crc32c_cffi.lib.crc32c_value(chunk, len(chunk))


class Checksum(object):
    """Hashlib-alike helper for CRC32C operations.

    Args:
        initial_value (Optional[bytes]): the initial chunk of data from
            which the CRC32C checksum is computed.  Defaults to b''.
    """

    __slots__ = ("_crc",)

    def __init__(self, initial_value=b""):
        self._crc = value(initial_value)

    def update(self, chunk):
        """Update the checksum with a new chunk of data.

        Args:
            chunk (Optional[bytes]): a chunk of data used to extend
                the CRC32C checksum.
        """
        self._crc = extend(self._crc, chunk)

    def digest(self):
        """Big-endian order, per RFC 4960.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects#crc32c

        Returns:
            bytes: An eight-byte digest string.
        """
        return struct.pack(">L", self._crc)

    def hexdigest(self):
        """Like :meth:`digest` except returns as a bytestring of double length.

        Returns
            bytes: A sixteen byte digest string, contaiing only hex digits.
        """
        return "{:08x}".format(self._crc).encode("ascii")

    def copy(self):
        """Create another checksum with the same CRC32C value.

        Returns:
            Checksum: the new instance.
        """
        clone = self.__class__()
        clone._crc = self._crc
        return clone

    def consume(self, stream, chunksize):
        """Consume chunks from a stream, extending our CRC32 checksum.

        Args:
            stream (BinaryIO): the stream to consume.
            chunksize (int): the size of the read to perform

        Returns:
            Generator[bytes, None, None]: Tterable of the chunks read from the
            stream.
        """
        while True:
            chunk = stream.read(chunksize)
            if not chunk:
                break
            self._crc = extend(self._crc, chunk)
            yield chunk
