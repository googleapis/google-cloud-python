# Copyright 2023 Google LLC
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

from bigframes.core import log_adapter

MAX_LABELS_COUNT = 64


@pytest.fixture
def test_instance():
    # Create a simple class for testing
    @log_adapter.class_logger
    class TestClass:
        def method1(self):
            pass

        def method2(self):
            pass

    return TestClass()


def test_method_logging(test_instance):
    test_instance.method1()
    test_instance.method2()

    # Check if the methods were added to the _api_methods list
    api_methods = log_adapter.get_and_reset_api_methods()
    assert api_methods is not None
    assert "method1" in api_methods
    assert "method2" in api_methods


def test_add_api_method_limit(test_instance):
    # Ensure that add_api_method correctly adds a method to _api_methods
    for i in range(70):
        test_instance.method2()
    assert len(log_adapter._api_methods) == MAX_LABELS_COUNT


def test_get_and_reset_api_methods(test_instance):
    # Ensure that get_and_reset_api_methods returns a copy and resets the list
    test_instance.method1()
    test_instance.method2()
    previous_methods = log_adapter.get_and_reset_api_methods()
    assert previous_methods is not None
    assert log_adapter._api_methods == []
