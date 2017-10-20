# Copyright 2017 Google Inc.
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


def main():
    print('>>> import os')
    print('>>> os.name')
    print(repr(os.name))
    print('>>> print(os.environ.get(\'PYTHON_ARCH\'))')
    print(os.environ.get('PYTHON_ARCH'))
    print('>>> print(os.environ.get(\'PYTHON_VERSION\'))')
    print(os.environ.get('PYTHON_VERSION'))
    print('>>> import sys')
    print('>>> sys.platform')
    print(repr(sys.platform))
    print('>>> sys.maxsize')
    print(repr(sys.maxsize))
    if sys.maxsize == 2**63 - 1:
        print('>>> sys.maxsize == 2**63 - 1')
        print('True')
    elif sys.maxsize == 2**31 - 1:
        print('>>> sys.maxsize == 2**31 - 1')
        print('True')
    print('>>> print(sys.version)')
    print(sys.version)
    print('>>> import struct')
    print('>>> struct.calcsize(\'P\') * 8')
    print(repr(struct.calcsize('P') * 8))


if __name__ == '__main__':
    main()
