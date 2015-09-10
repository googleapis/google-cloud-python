# Copyright 2015 Google Inc. All rights reserved.
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

"""Google Cloud Bigtable API package."""


from __future__ import print_function
import sys

try:
    from grpc._adapter import _c
except ImportError as exc:  # pragma: NO COVER
    if 'libgrpc.so' in str(exc):
        print('gRPC libraries could not be located. Please see '
              'instructions to locate these files. You\'ll want '
              'to set your LD_LIBRARY_PATH variable to help '
              'Python locate the libraries.', file=sys.stderr)
    raise
