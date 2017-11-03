# Copyright 2017 Google LLC
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

"""Helpers for handling routing header params."""


try:
    from urllib.parse import urlencode
except ImportError:
    def urlencode(params):
        return '&'.join(['{}={}'.format(*pair) for pair in params])

ROUTING_METADATA_KEY = 'x-goog-header-params'


def _to_url_string(x):
    if not isinstance(x, bool):
        return str(x)
    elif x:
        return '1'
    else:
        return '0'


def to_routing_header(params):
    """Returns the routing header string that the params form"""
    return urlencode([(k, _to_url_string(v)) for k, v in params])


def to_grpc_metadata(params):
    """Returns the gRPC metadata that the routing header params form"""
    return (ROUTING_METADATA_KEY, to_routing_header(params))
