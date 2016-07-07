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


from gcloud.bigtable.client import Client


_ERR_MSG = """\
gRPC is required for using the Cloud Bigtable API, but
importing the gRPC library (grpcio in PyPI) has failed.

As of June 2016, grpcio is only supported in Python 2.7,
which unfortunately means the Cloud Bigtable API isn't
available if you're using Python 3 or Python < 2.7.

If you're using Python 2.7 and importing / installing
grpcio has failed, this likely means you have a non-standard version
of Python installed. Check http://grpc.io if you're
having trouble installing the grpcio package.
"""

try:
    import grpc.beta.implementations
except ImportError as exc:  # pragma: NO COVER
    raise ImportError(_ERR_MSG, exc)
