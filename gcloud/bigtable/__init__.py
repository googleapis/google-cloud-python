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

try:
    import grpc.beta.implementations
except ImportError as exc:
    message = ('gRPC is required for using the Cloud Bigtable API. '
               'Importing the grpc library (grpcio in PyPI) has failed. '
               'As of May 2016, grpcio is only supported in Python 2.7.')
    raise ImportError(message, exc)
