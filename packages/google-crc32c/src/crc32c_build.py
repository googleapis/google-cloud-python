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

import cffi


_HEADER = """\
uint32_t crc32c_extend(uint32_t crc, const uint8_t* data, size_t count);
uint32_t crc32c_value(const uint8_t* data, size_t count);
"""
FFIBUILDER = cffi.FFI()
FFIBUILDER.cdef(_HEADER)
FFIBUILDER.set_source(
    "_crc32c_cffi",
    '#include "crc32c/crc32c.h"',
    libraries=["crc32c"],
    include_dirs=["/usr/local/include"],
)


if __name__ == "__main__":
    FFIBUILDER.compile(verbose=True)
