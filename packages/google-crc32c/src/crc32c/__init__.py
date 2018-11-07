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
