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

import pytest

from google.api_core import client_options


def test_constructor_dict():
    options = client_options.ClientOptions(
        options={"api_endpoint": "foo.googleapis.com"}
    )

    assert options.api_endpoint == "foo.googleapis.com"

def test_constructor_kwargs():
    options = client_options.ClientOptions(
        api_endpoint="foo.googleapis.com"
    )

    assert options.api_endpoint == "foo.googleapis.com"

def test_constructor_exception():
    with pytest.raises(Exception):
        options = client_options.ClientOptions(
            api_endpoint="a.googleapis.com", options={"b.googleapis.com"})