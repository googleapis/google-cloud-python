# Copyright 2024 Google LLC
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

import unittest.mock as mock

import db_dtypes.pandas_backports as pandas_backports


@mock.patch("builtins.__import__")
def test_import_default_module_found(mock_import):
    mock_module = mock.MagicMock()
    mock_module.OpsMixin = "OpsMixin_from_module"  # Simulate successful import
    mock_import.return_value = mock_module

    default_class = type("OpsMixin", (), {})  # Dummy class
    result = pandas_backports.import_default("module_name", default=default_class)
    assert result == "OpsMixin_from_module"


@mock.patch("builtins.__import__")
def test_import_default_module_not_found(mock_import):
    mock_import.side_effect = ModuleNotFoundError

    default_class = type("OpsMixin", (), {})  # Dummy class
    result = pandas_backports.import_default("module_name", default=default_class)
    assert result == default_class


@mock.patch("builtins.__import__")
def test_import_default_force_true(mock_import):
    """
    Test that when force=True, the default is returned immediately
    without attempting an import.
    """
    default_class = type("ForcedMixin", (), {})  # A dummy class

    result = pandas_backports.import_default(
        "any_module_name", force=True, default=default_class
    )

    # Assert that the returned value is the default class itself
    assert result is default_class
