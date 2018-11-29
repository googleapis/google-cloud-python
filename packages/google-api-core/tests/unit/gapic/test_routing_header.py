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


from google.api_core.gapic_v1 import routing_header


def test_to_routing_header():
    params = [("name", "meep"), ("book.read", "1")]
    value = routing_header.to_routing_header(params)
    assert value == "name=meep&book.read=1"


def test_to_routing_header_with_slashes():
    params = [("name", "me/ep"), ("book.read", "1&2")]
    value = routing_header.to_routing_header(params)
    assert value == "name=me/ep&book.read=1%262"


def test_to_grpc_metadata():
    params = [("name", "meep"), ("book.read", "1")]
    metadata = routing_header.to_grpc_metadata(params)
    assert metadata == (routing_header.ROUTING_METADATA_KEY, "name=meep&book.read=1")
