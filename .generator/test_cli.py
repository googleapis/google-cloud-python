# Copyright 2025 Google LLC
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
import json

from cli import _read_json_file, handle_generate, handle_build, handle_configure


def test_handle_configure_dry_run():
    # This is a simple test to ensure that the dry run command succeeds.
    handle_configure(dry_run=True)


def test_handle_generate_dry_run():
    # This is a simple test to ensure that the dry run command succeeds.
    handle_generate(dry_run=True)


def test_handle_build_dry_run():
    # This is a simple test to ensure that the dry run command succeeds.
    handle_build(dry_run=True)


def test_read_valid_json(mocker):
    """Tests reading a valid JSON file."""
    mock_content = '{"key": "value"}'
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_content))
    result = _read_json_file("fake/path.json")
    assert result == {"key": "value"}


def test_file_not_found(mocker):
    """Tests behavior when the file does not exist."""
    mocker.patch("os.path.exists", return_value=False)

    with pytest.raises(FileNotFoundError):
        _read_json_file("non/existent/path.json")


def test_invalid_json(mocker):
    """Tests reading a file with malformed JSON."""
    mock_content = '{"key": "value",}'
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_content))

    with pytest.raises(json.JSONDecodeError):
        _read_json_file("fake/path.json")


def test_io_error_on_read(mocker):
    """Tests for a generic IOError."""
    mocker.patch("os.path.exists", return_value=True)
    mocked_open = mocker.mock_open()
    mocked_open.side_effect = IOError("permission denied")
    mocker.patch("builtins.open", mocked_open)

    with pytest.raises(IOError):
        _read_json_file("fake/path.json")
