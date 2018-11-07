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
import functools
import itertools

import pytest

import crc32c


# From: https://tools.ietf.org/html/rfc3720#appendix-B.4
ISCSI_SCSI_READ_10_COMMAND_PDU = [
    0x01, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00,
    0x00, 0x00, 0x00, 0x14, 0x00, 0x00, 0x00, 0x18, 0x28, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
ISCSI_LENGTH = len(ISCSI_SCSI_READ_10_COMMAND_PDU)
ISCSI_BYTES = bytes(ISCSI_SCSI_READ_10_COMMAND_PDU)
ISCSI_CRC = 0xd9963a56

_EXPECTED = [
    (b'', 0x00000000),
    (b'\x00' * 32, 0x8a9136aa),
    (b'\xff' * 32, 0x62a8ab43),
    (bytes(range(32)), 0x46dd794e),
    (bytes(reversed(range(32))), 0x113fdb5c),
    (ISCSI_SCSI_READ_10_COMMAND_PDU, ISCSI_CRC),
    (ISCSI_BYTES, ISCSI_CRC),
]


def test_extend_w_empty_chunk():
    crc = 123
    assert crc32c.extend(crc, b'') == crc


def test_extend_w_multiple_chunks():
    crc = 0

    for index in itertools.islice(range(ISCSI_LENGTH), 0, None, 7):
        chunk = ISCSI_SCSI_READ_10_COMMAND_PDU[index:index + 7]
        crc = crc32c.extend(crc, chunk)

    assert crc == ISCSI_CRC


def test_extend_w_reduce():
    chunks = (
        ISCSI_BYTES[index:index + 3]
        for index in itertools.islice(range(ISCSI_LENGTH), 0, None, 3)
    )
    assert functools.reduce(crc32c.extend, chunks, 0) == ISCSI_CRC


@pytest.mark.parametrize("chunk, expected", _EXPECTED)
def test_value(chunk, expected):
    assert crc32c.value(chunk) == expected
