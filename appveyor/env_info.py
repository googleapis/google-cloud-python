# Copyright 2017 Google LLC All Rights Reserved.
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

"""Get environment information."""

from __future__ import print_function

import os
import struct
import sys


def env_var(var_name):
    value = os.environ.get(var_name)
    print("os.environ[{!r}]: {}".format(var_name, value))


def main():
    print("os.name: {}".format(os.name))
    env_var("PYTHON_ARCH")
    env_var("PYTHON_VERSION")
    print("sys.platform: {}".format(sys.platform))

    if sys.maxsize == 2 ** 63 - 1:
        print("sys.maxsize: 2^(63) - 1")
    elif sys.maxsize == 2 ** 31 - 1:
        print("sys.maxsize: 2^(31) - 1")
    else:
        print("sys.maxsize: {}".format(sys.maxsize))

    print("sys.version:\n{}".format(sys.version))
    bitness = struct.calcsize("P") * 8
    print("struct.calcsize('P') * 8: {}".format(bitness))


if __name__ == "__main__":
    main()
