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

from crc32c import _crc32c_cffi


def main():
    print("_crc32c_cffi: {}".format(_crc32c_cffi))
    print("_crc32c_cffi.lib: {}".format(_crc32c_cffi.lib))
    print("dir(_crc32c_cffi.lib): {}".format(dir(_crc32c_cffi.lib)))


if __name__ == "__main__":
    main()
