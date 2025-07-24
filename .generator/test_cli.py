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

import json
import logging
import os
import subprocess
from unittest.mock import MagicMock, mock_open

import pytest

from cli import (
    GENERATE_REQUEST_FILE,
    LIBRARIAN_DIR,
    REPO_DIR,
    _build_bazel_target,
    _determine_bazel_rule,
    _get_library_id,
    _locate_and_extract_artifact,
    _read_json_file,
    _run_individual_session,
    _run_nox_sessions,
    _run_post_processor,
    handle_build,
    handle_configure,
    handle_generate,
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


@pytest.fixture
def mock_generate_request_data_for_nox():
    """Returns mock data for generate-request.json for nox tests."""
    return {
        "id": "mock-library",
        "apis": [
            {"path": "google/mock/v1"},
        ],
    }


def test_get_library_id_success():
    """Tests that _get_library_id returns the correct ID when present."""
    request_data = {"id": "test-library", "name": "Test Library"}
    library_id = _get_library_id(request_data)
    assert library_id == "test-library"


def test_get_library_id_missing_id():
    """Tests that _get_library_id raises ValueError when 'id' is missing."""
    request_data = {"name": "Test Library"}
    with pytest.raises(
        ValueError, match="Request file is missing required 'id' field."
    ):
        _get_library_id(request_data)


def test_get_library_id_empty_id():
    """Tests that _get_library_id raises ValueError when 'id' is an empty string."""
    request_data = {"id": "", "name": "Test Library"}
    with pytest.raises(
        ValueError, match="Request file is missing required 'id' field."
    ):
        _get_library_id(request_data)


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


def test_build_bazel_target_success(mocker, caplog):
    """
    Tests that the build helper logs success when the command runs correctly.
    """
    caplog.set_level(logging.INFO)
    mocker.patch("cli.subprocess.run", return_value=MagicMock(returncode=0))
    _build_bazel_target("mock/bazel:rule")
    assert "Bazel build for mock/bazel:rule rule completed successfully" in caplog.text


def test_build_bazel_target_fails(mocker, caplog):
    """
    Tests that ValueError is raised if the subprocess command fails.
    """
    caplog.set_level(logging.ERROR)
    mocker.patch(
        "cli.subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "cmd", stderr="Build failed"),
    )
    with pytest.raises(ValueError):
        _build_bazel_target("mock/bazel:rule")


def test_determine_bazel_rule_command_fails(mocker, caplog):
    """
    Tests that an exception is raised if the subprocess command fails.
    """
    caplog.set_level(logging.INFO)
    mocker.patch(
        "cli.subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "cmd", stderr="Bazel error"),
    )

    with pytest.raises(ValueError):
        _determine_bazel_rule("google/cloud/language/v1")

    assert "Found Bazel rule" not in caplog.text


def test_locate_and_extract_artifact_success(mocker, caplog):
    """
    Tests that the artifact helper calls the correct sequence of commands.
    """
    caplog.set_level(logging.INFO)
    mock_info_result = MagicMock(stdout="/path/to/bazel-bin\n")
    mock_tar_result = MagicMock(returncode=0)
    mocker.patch("cli.subprocess.run", side_effect=[mock_info_result, mock_tar_result])
    mock_makedirs = mocker.patch("cli.os.makedirs")
    _locate_and_extract_artifact(
        "//google/cloud/language/v1:rule-py",
        "google-cloud-language",
    )

    assert (
        "Found artifact at: /path/to/bazel-bin/google/cloud/language/v1/rule-py.tar.gz"
        in caplog.text
    )
    assert (
        "Preparing staging directory: output/owl-bot-staging/google-cloud-language"
        in caplog.text
    )
    assert (
        "Artifact /path/to/bazel-bin/google/cloud/language/v1/rule-py.tar.gz extracted successfully"
        in caplog.text
    )
    mock_makedirs.assert_called_once()


def test_locate_and_extract_artifact_fails(mocker, caplog):
    """
    Tests that an exception is raised if the subprocess command fails.
    """
    caplog.set_level(logging.INFO)
    mocker.patch(
        "cli.subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "cmd", stderr="Bazel error"),
    )

    with pytest.raises(ValueError):
        _locate_and_extract_artifact(
            "//google/cloud/language/v1:rule-py",
            "google-cloud-language",
        )


def test_run_post_processor_success(mocker, caplog):
    """
    Tests that the post-processor helper calls the correct command.
    """
    caplog.set_level(logging.INFO)
    mocker.patch("cli.SYNTHTOOL_INSTALLED", return_value=True)
    mock_subprocess = mocker.patch("cli.subprocess.run")

    _run_post_processor()

    mock_subprocess.assert_called_once()

    assert mock_subprocess.call_args.kwargs["cwd"] == "output"
    assert "Python post-processor ran successfully." in caplog.text


def test_locate_and_extract_artifact_fails(mocker, caplog):
    """
    Tests that an exception is raised if the subprocess command fails.
    """
    caplog.set_level(logging.INFO)
    mocker.patch("cli.SYNTHTOOL_INSTALLED", return_value=True)

    with pytest.raises(FileNotFoundError):
        _run_post_processor()


def test_handle_generate_success(caplog, mock_generate_request_file, mocker):
    """
    Tests the successful execution path of handle_generate.
    """
    caplog.set_level(logging.INFO)

    mock_determine_rule = mocker.patch(
        "cli._determine_bazel_rule", return_value="mock-rule"
    )
    mock_build_target = mocker.patch("cli._build_bazel_target")
    mock_locate_and_extract_artifact = mocker.patch("cli._locate_and_extract_artifact")
    mock_run_post_processor = mocker.patch("cli._run_post_processor")

    handle_generate()

    mock_determine_rule.assert_called_once_with("google/cloud/language/v1")


def test_handle_generate_fail(caplog):
    """
    Tests the failed to read `librarian/generate-request.json` file in handle_generates.
    """
    with pytest.raises(ValueError):
        handle_generate()


def test_run_individual_session_success(mocker, caplog):
    """Tests that _run_individual_session calls nox with correct arguments and logs success."""
    caplog.set_level(logging.INFO)

    mock_subprocess_run = mocker.patch(
        "cli.subprocess.run", return_value=MagicMock(returncode=0)
    )

    test_session = "unit-3.9"
    test_library_id = "test-library"
    _run_individual_session(test_session, test_library_id)

    expected_command = [
        "nox",
        "-s",
        test_session,
        "-f",
        f"{REPO_DIR}/packages/{test_library_id}",
    ]
    mock_subprocess_run.assert_called_once_with(expected_command, text=True, check=True)


def test_run_individual_session_failure(mocker):
    """Tests that _run_individual_session raises CalledProcessError if nox command fails."""
    mocker.patch(
        "cli.subprocess.run",
        side_effect=subprocess.CalledProcessError(
            1, "nox", stderr="Nox session failed"
        ),
    )

    with pytest.raises(subprocess.CalledProcessError):
        _run_individual_session("lint", "another-library")


def test_run_nox_sessions_success(mocker, mock_generate_request_data_for_nox):
    """Tests that _run_nox_sessions successfully runs all specified sessions."""
    mocker.patch("cli._read_json_file", return_value=mock_generate_request_data_for_nox)
    mocker.patch("cli._get_library_id", return_value="mock-library")
    mock_run_individual_session = mocker.patch("cli._run_individual_session")

    sessions_to_run = ["unit-3.9", "lint"]
    _run_nox_sessions(sessions_to_run)

    assert mock_run_individual_session.call_count == len(sessions_to_run)
    mock_run_individual_session.assert_has_calls(
        [
            mocker.call("unit-3.9", "mock-library"),
            mocker.call("lint", "mock-library"),
        ]
    )


def test_run_nox_sessions_read_file_failure(mocker):
    """Tests that _run_nox_sessions raises ValueError if _read_json_file fails."""
    mocker.patch("cli._read_json_file", side_effect=FileNotFoundError("file not found"))

    with pytest.raises(ValueError, match="Failed to run the nox session"):
        _run_nox_sessions(["unit-3.9"])


def test_run_nox_sessions_get_library_id_failure(mocker):
    """Tests that _run_nox_sessions raises ValueError if _get_library_id fails."""
    mocker.patch("cli._read_json_file", return_value={"apis": []})  # Missing 'id'
    mocker.patch(
        "cli._get_library_id",
        side_effect=ValueError("Request file is missing required 'id' field."),
    )

    with pytest.raises(ValueError, match="Failed to run the nox session"):
        _run_nox_sessions(["unit-3.9"])


def test_run_nox_sessions_individual_session_failure(
    mocker, mock_generate_request_data_for_nox
):
    """Tests that _run_nox_sessions raises ValueError if _run_individual_session fails."""
    mocker.patch("cli._read_json_file", return_value=mock_generate_request_data_for_nox)
    mocker.patch("cli._get_library_id", return_value="mock-library")
    mock_run_individual_session = mocker.patch(
        "cli._run_individual_session",
        side_effect=[None, subprocess.CalledProcessError(1, "nox", "session failed")],
    )

    sessions_to_run = ["unit-3.9", "lint"]
    with pytest.raises(ValueError, match="Failed to run the nox session"):
        _run_nox_sessions(sessions_to_run)

    # Check that _run_individual_session was called at least once
    assert mock_run_individual_session.call_count > 0


def test_handle_build_success(caplog, mocker):
    """
    Tests the successful execution path of handle_build.
    """
    caplog.set_level(logging.INFO)

    mocker.patch("cli._run_nox_sessions")
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
