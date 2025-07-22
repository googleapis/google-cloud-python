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

import os
import pytest
import json
import logging

from unittest.mock import mock_open, MagicMock

from cli import (
    _read_json_file,
    _determine_bazel_rule,
    handle_generate,
    handle_build,
    handle_configure,
    LIBRARIAN_DIR,
    GENERATE_REQUEST_FILE,
)


@pytest.fixture
def mock_generate_request_file(tmp_path, monkeypatch):
    """Creates the mock request file at the correct path inside a temp dir."""
    # Create the path as expected by the script: .librarian/generate-request.json
    request_path = f"{LIBRARIAN_DIR}/{GENERATE_REQUEST_FILE}"
    request_dir = tmp_path / os.path.dirname(request_path)
    request_dir.mkdir()
    request_file = request_dir / os.path.basename(request_path)

    request_content = {
        "id": "google-cloud-language",
        "apis": [{"path": "google/cloud/language/v1"}],
    }
    request_file.write_text(json.dumps(request_content))

    # Change the current working directory to the temp path for the test.
    monkeypatch.chdir(tmp_path)
    return request_file


def test_handle_configure_success(caplog, mock_generate_request_file):
    """
    Tests the successful execution path of handle_configure.
    """
    caplog.set_level(logging.INFO)

    handle_configure()

    assert "'configure' command executed." in caplog.text


def test_determine_bazel_rule_success(mocker, caplog):
    """
    Tests the happy path of _determine_bazel_rule.
    """
    caplog.set_level(logging.INFO)
    mock_result = MagicMock(
        stdout="//google/cloud/language/v1:google-cloud-language-v1-py\n"
    )
    mocker.patch("cli.subprocess.run", return_value=mock_result)

    rule = _determine_bazel_rule("google/cloud/language/v1")

    assert rule == "//google/cloud/language/v1:google-cloud-language-v1-py"
    assert "Found Bazel rule" in caplog.text


def test_handle_generate_success(caplog, mock_generate_request_file, mocker):
    """
    Tests the successful execution path of handle_generate.
    """
    caplog.set_level(logging.INFO)

    mock_determine_rule = mocker.patch(
        "cli._determine_bazel_rule", return_value="mock-rule"
    )

    handle_generate()

    mock_determine_rule.assert_called_once_with("google/cloud/language/v1")


def test_handle_generate_fail(caplog):
    """
    Tests the failed to read `librarian/generate-request.json` file in handle_generates.
    """
    with pytest.raises(ValueError):
        handle_generate()


def test_handle_build_success(caplog, mock_generate_request_file):
    """
    Tests the successful execution path of handle_build.
    """
    caplog.set_level(logging.INFO)

    handle_build()

    assert "'build' command executed." in caplog.text


def test_read_valid_json(mocker):
    """Tests reading a valid JSON file."""
    mock_content = '{"key": "value"}'
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_content))
    result = _read_json_file("fake/path.json")
    assert result == {"key": "value"}


def test_file_not_found(mocker):
    """Tests behavior when the file does not exist."""
    mocker.patch("builtins.open", side_effect=FileNotFoundError("No such file"))

    with pytest.raises(FileNotFoundError):
        _read_json_file("non/existent/path.json")


def test_invalid_json(mocker):
    """Tests reading a file with malformed JSON."""
    mock_content = '{"key": "value",}'
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_content))

    with pytest.raises(json.JSONDecodeError):
        _read_json_file("fake/path.json")
