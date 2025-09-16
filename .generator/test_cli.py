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
import pathlib
import re
import subprocess
import yaml
import unittest.mock
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, mock_open

import pytest
from cli import (
    GENERATE_REQUEST_FILE,
    BUILD_REQUEST_FILE,
    RELEASE_INIT_REQUEST_FILE,
    SOURCE_DIR,
    STATE_YAML_FILE,
    LIBRARIAN_DIR,
    REPO_DIR,
    _clean_up_files_after_post_processing,
    _copy_files_needed_for_post_processing,
    _create_main_version_header,
    _get_library_dist_name,
    _determine_library_namespace,
    _get_library_id,
    _get_libraries_to_prepare_for_release,
    _get_previous_version,
    _process_changelog,
    _process_version_file,
    _read_json_file,
    _read_text_file,
    _run_individual_session,
    _run_nox_sessions,
    _run_post_processor,
    _update_changelog_for_library,
    _update_global_changelog,
    _update_version_for_library,
    _verify_library_dist_name,
    _verify_library_namespace,
    _write_json_file,
    _write_text_file,
    handle_build,
    handle_configure,
    handle_generate,
    handle_release_init,
)


_MOCK_LIBRARY_CHANGES = [
    {
        "type": "feat",
        "subject": "add new UpdateRepository API",
        "body": "This adds the ability to update a repository's properties.",
        "piper_cl_number": "786353207",
        "source_commit_hash": "9461532e7d19c8d71709ec3b502e5d81340fb661",
    },
    {
        "type": "fix",
        "subject": "some fix",
        "body": "",
        "piper_cl_number": "786353208",
        "source_commit_hash": "1231532e7d19c8d71709ec3b502e5d81340fb661",
    },
    {
        "type": "fix",
        "subject": "another fix",
        "body": "",
        "piper_cl_number": "786353209",
        "source_commit_hash": "1241532e7d19c8d71709ec3b502e5d81340fb661",
    },
    {
        "type": "docs",
        "subject": "fix typo in BranchRule comment",
        "body": "",
        "piper_cl_number": "786353210",
        "source_commit_hash": "9461532e7d19c8d71709ec3b502e5d81340fb661",
    },
]


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
def mock_build_request_file(tmp_path, monkeypatch):
    """Creates the mock request file at the correct path inside a temp dir."""
    # Create the path as expected by the script: .librarian/build-request.json
    request_path = f"{LIBRARIAN_DIR}/{BUILD_REQUEST_FILE}"
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
def mock_build_bazel_file(tmp_path, monkeypatch):
    """Creates the mock request file at the correct path inside a temp dir."""
    # Create the path as expected by the script: .librarian/build-request.json
    bazel_build_path = f"{SOURCE_DIR}/google/cloud/language/v1/BUILD.bazel"
    bazel_build_dir = tmp_path / Path(bazel_build_path).parent
    os.makedirs(bazel_build_dir, exist_ok=True)
    build_bazel_file = bazel_build_dir / os.path.basename(bazel_build_path)

    build_bazel_content = """load(
    "@com_google_googleapis_imports//:imports.bzl",
    "py_gapic_assembly_pkg",
    "py_gapic_library",
    "py_test",
)

py_gapic_library(
    name = "language_py_gapic",
    srcs = [":language_proto"],
    grpc_service_config = "language_grpc_service_config.json",
    rest_numeric_enums = True,
    service_yaml = "language_v1.yaml",
    transport = "grpc+rest",
    deps = [
    ],
    opt_args = [
        "python-gapic-namespace=google.cloud",
    ],
)"""
    build_bazel_file.write_text(build_bazel_content)
    return build_bazel_file


@pytest.fixture
def mock_generate_request_data_for_nox():
    """Returns mock data for generate-request.json for nox tests."""
    return {
        "id": "mock-library",
        "apis": [
            {"path": "google/mock/v1"},
        ],
    }


@pytest.fixture
def mock_release_init_request_file(tmp_path, monkeypatch):
    """Creates the mock request file at the correct path inside a temp dir."""
    # Create the path as expected by the script: .librarian/release-request.json
    request_path = f"{LIBRARIAN_DIR}/{RELEASE_INIT_REQUEST_FILE}"
    request_dir = tmp_path / os.path.dirname(request_path)
    request_dir.mkdir()
    request_file = request_dir / os.path.basename(request_path)

    request_content = {
        "libraries": [
            {
                "id": "google-cloud-another-library",
                "apis": [{"path": "google/cloud/another/library/v1"}],
                "release_triggered": False,
                "version": "1.2.3",
                "changes": [],
            },
            {
                "id": "google-cloud-language",
                "apis": [{"path": "google/cloud/language/v1"}],
                "release_triggered": True,
                "version": "1.2.3",
                "changes": [],
            },
        ]
    }
    request_file.write_text(json.dumps(request_content))

    # Change the current working directory to the temp path for the test.
    monkeypatch.chdir(tmp_path)
    return request_file


@pytest.fixture
def mock_state_file(tmp_path, monkeypatch):
    """Creates the state file at the correct path inside a temp dir."""
    # Create the path as expected by the script: .librarian/state.yaml
    request_path = f"{LIBRARIAN_DIR}/{STATE_YAML_FILE}"
    request_dir = tmp_path / os.path.dirname(request_path)
    request_dir.mkdir()
    request_file = request_dir / os.path.basename(request_path)

    state_yaml_contents = {
        "libraries": [{"id": "google-cloud-language", "version": "1.2.3"}]
    }
    request_file.write_text(yaml.dump(state_yaml_contents))

    # Change the current working directory to the temp path for the test.
    monkeypatch.chdir(tmp_path)
    return request_file


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


def test_run_post_processor_success(mocker, caplog):
    """
    Tests that the post-processor helper calls the correct command.
    """
    caplog.set_level(logging.INFO)
    mocker.patch("cli.SYNTHTOOL_INSTALLED", return_value=True)
    mock_chdir = mocker.patch("cli.os.chdir")
    mock_owlbot_main = mocker.patch(
        "cli.synthtool.languages.python_mono_repo.owlbot_main"
    )
    _run_post_processor("output", "google-cloud-language")

    mock_chdir.assert_called_once()

    mock_owlbot_main.assert_called_once_with("packages/google-cloud-language")
    assert "Python post-processor ran successfully." in caplog.text


def test_handle_generate_success(
    caplog, mock_generate_request_file, mock_build_bazel_file, mocker
):
    """
    Tests the successful execution path of handle_generate.
    """
    caplog.set_level(logging.INFO)

    mock_run_post_processor = mocker.patch("cli._generate_api")
    mock_run_post_processor = mocker.patch("cli._run_post_processor")
    mock_copy_files_needed_for_post_processing = mocker.patch(
        "cli._copy_files_needed_for_post_processing"
    )
    mock_clean_up_files_after_post_processing = mocker.patch(
        "cli._clean_up_files_after_post_processing"
    )

    handle_generate()

    mock_run_post_processor.assert_called_once_with("output", "google-cloud-language")
    mock_copy_files_needed_for_post_processing.assert_called_once_with(
        "output", "input", "google-cloud-language"
    )
    mock_clean_up_files_after_post_processing.assert_called_once_with(
        "output", "google-cloud-language"
    )


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
    repo = "repo"
    _run_individual_session(test_session, test_library_id, repo)

    expected_command = [
        "nox",
        "-s",
        test_session,
        "-f",
        f"{REPO_DIR}/packages/{test_library_id}/noxfile.py",
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
        _run_individual_session("lint", "another-library", "repo")


def test_run_nox_sessions_success(mocker, mock_generate_request_data_for_nox):
    """Tests that _run_nox_sessions successfully runs all specified sessions."""
    mocker.patch("cli._read_json_file", return_value=mock_generate_request_data_for_nox)
    mocker.patch("cli._get_library_id", return_value="mock-library")
    mock_run_individual_session = mocker.patch("cli._run_individual_session")

    sessions_to_run = [
        "unit-3.9",
        "unit-3.13",
        "docs",
        "lint",
        "lint_setup_py",
        "mypy-3.13",
    ]
    _run_nox_sessions("mock-library", "repo")

    assert mock_run_individual_session.call_count == len(sessions_to_run)
    mock_run_individual_session.assert_has_calls(
        [
            mocker.call("unit-3.9", "mock-library", "repo"),
            mocker.call("unit-3.13", "mock-library", "repo"),
            mocker.call("docs", "mock-library", "repo"),
            mocker.call("lint", "mock-library", "repo"),
            mocker.call("lint_setup_py", "mock-library", "repo"),
            mocker.call("mypy-3.13", "mock-library", "repo"),
        ]
    )


def test_run_nox_sessions_read_file_failure(mocker):
    """Tests that _run_nox_sessions raises ValueError if _read_json_file fails."""
    mocker.patch("cli._read_json_file", side_effect=FileNotFoundError("file not found"))

    with pytest.raises(ValueError, match="Failed to run the nox session"):
        _run_nox_sessions("mock-library", "repo")


def test_run_nox_sessions_get_library_id_failure(mocker):
    """Tests that _run_nox_sessions raises ValueError if _get_library_id fails."""
    mocker.patch("cli._read_json_file", return_value={"apis": []})  # Missing 'id'
    mocker.patch(
        "cli._get_library_id",
        side_effect=ValueError("Request file is missing required 'id' field."),
    )

    with pytest.raises(ValueError, match="Failed to run the nox session"):
        _run_nox_sessions("mock-library", "repo")


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

    with pytest.raises(ValueError, match="Failed to run the nox session"):
        _run_nox_sessions("mock-library", "repo")

    # Check that _run_individual_session was called at least once
    assert mock_run_individual_session.call_count > 0


def test_handle_build_success(caplog, mocker, mock_build_request_file):
    """
    Tests the successful execution path of handle_build.
    """
    caplog.set_level(logging.INFO)

    mocker.patch("cli._run_nox_sessions")
    mocker.patch("cli._verify_library_namespace")
    mocker.patch("cli._verify_library_dist_name")
    handle_build()

    assert "'build' command executed." in caplog.text


def test_handle_build_fail(caplog):
    """
    Tests the failed to read `librarian/build-request.json` file in handle_generates.
    """
    with pytest.raises(ValueError):
        handle_build()


def test_read_valid_json(mocker):
    """Tests reading a valid JSON file."""
    mock_content = '{"key": "value"}'
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_content))
    result = _read_json_file("fake/path.json")
    assert result == {"key": "value"}


def test_json_file_not_found(mocker):
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


def test_copy_files_needed_for_post_processing_success(mocker):
    mock_makedirs = mocker.patch("os.makedirs")
    mock_shutil_copy = mocker.patch("shutil.copy")
    _copy_files_needed_for_post_processing("output", "input", "library_id")

    mock_makedirs.assert_called()
    mock_shutil_copy.assert_called_once()


def test_clean_up_files_after_post_processing_success(mocker):
    mock_shutil_rmtree = mocker.patch("shutil.rmtree")
    mock_os_remove = mocker.patch("os.remove")
    _clean_up_files_after_post_processing("output", "library_id")


def test_get_libraries_to_prepare_for_release(mock_release_init_request_file):
    """
    Tests that only libraries with the `release_triggered` field set to `True` are
    returned.
    """
    request_data = _read_json_file(f"{LIBRARIAN_DIR}/{RELEASE_INIT_REQUEST_FILE}")
    libraries_to_prep_for_release = _get_libraries_to_prepare_for_release(request_data)
    assert len(libraries_to_prep_for_release) == 1
    assert "google-cloud-language" in libraries_to_prep_for_release[0]["id"]
    assert libraries_to_prep_for_release[0]["release_triggered"]


def test_handle_release_init_success(mocker, mock_release_init_request_file):
    """
    Simply tests that `handle_release_init` runs without errors.
    """
    mocker.patch("cli._update_global_changelog", return_value=None)
    mocker.patch("cli._update_version_for_library", return_value=None)
    mocker.patch("cli._get_previous_version", return_value=None)
    mocker.patch("cli._update_changelog_for_library", return_value=None)
    handle_release_init()


def test_handle_release_init_fail_value_error_file():
    """
    Tests that handle_release_init fails to read `librarian/release-init-request.json`.
    """
    with pytest.raises(ValueError, match="No such file or directory"):
        handle_release_init()


def test_handle_release_init_fail_value_error_version(mocker):
    m = mock_open()

    mock_release_init_request_content = {
        "libraries": [
            {
                "id": "google-cloud-language",
                "apis": [{"path": "google/cloud/language/v1"}],
                "release_triggered": True,
                "version": "1.2.2",
                "changes": [],
            },
        ]
    }
    with unittest.mock.patch("cli.open", m):
        mocker.patch(
            "cli._get_libraries_to_prepare_for_release",
            return_value=mock_release_init_request_content["libraries"],
        )
        mocker.patch("cli._get_previous_version", return_value="1.2.2")
        mocker.patch("cli._process_changelog", return_value=None)
        mocker.patch(
            "cli._read_json_file", return_value=mock_release_init_request_content
        )
        with pytest.raises(
            ValueError, match="is the same as the version in state.yaml"
        ):
            handle_release_init()


def test_read_valid_text_file(mocker):
    """Tests reading a valid text file."""
    mock_content = "some text"
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_content))
    result = _read_text_file("fake/path.txt")
    assert result == "some text"


def test_text_file_not_found(mocker):
    """Tests behavior when the file does not exist."""
    mocker.patch("builtins.open", side_effect=FileNotFoundError("No such file"))

    with pytest.raises(FileNotFoundError):
        _read_text_file("non/existent/path.text")


def test_write_text_file():
    """Tests writing a text file.
    See https://docs.python.org/3/library/unittest.mock.html#mock-open
    """
    m = mock_open()

    with unittest.mock.patch("cli.open", m):
        _write_text_file("fake_path.txt", "modified content")

        handle = m()
        handle.write.assert_called_once_with("modified content")


def test_write_json_file():
    """Tests writing a json file.
    See https://docs.python.org/3/library/unittest.mock.html#mock-open
    """
    m = mock_open()

    expected_dict = {"name": "call me json"}

    with unittest.mock.patch("cli.open", m):
        _write_json_file("fake_path.json", expected_dict)

        handle = m()
        # Get all the arguments passed to the mock's write method
        # and join them into a single string.
        written_content = "".join(
            [call.args[0] for call in handle.write.call_args_list]
        )

        # Create the expected output string with the correct formatting.
        expected_output = json.dumps(expected_dict, indent=2) + "\n"

        # Assert that the content written to the mock file matches the expected output.
        assert written_content == expected_output


def test_update_global_changelog(mocker, mock_release_init_request_file):
    """Tests that the global changelog is updated
    with the new version for a given library.
    See https://docs.python.org/3/library/unittest.mock.html#mock-open
    """
    m = mock_open()
    request_data = _read_json_file(f"{LIBRARIAN_DIR}/{RELEASE_INIT_REQUEST_FILE}")
    libraries = _get_libraries_to_prepare_for_release(request_data)

    with unittest.mock.patch("cli.open", m):
        mocker.patch(
            "cli._read_text_file", return_value="[google-cloud-language==1.2.2]"
        )
        _update_global_changelog("source", "output", libraries)

        handle = m()
        handle.write.assert_called_once_with("[google-cloud-language==1.2.3]")


def test_update_version_for_library_success(mocker):
    m = mock_open()

    mock_rglob = mocker.patch(
        "pathlib.Path.rglob", return_value=[pathlib.Path("repo/gapic_version.py")]
    )
    mock_shutil_copy = mocker.patch("shutil.copy")
    mock_content = '__version__ = "1.2.2"'
    mock_json_metadata = {"clientLibrary": {"version": "0.1.0"}}

    with unittest.mock.patch("cli.open", m):
        mocker.patch("cli._read_text_file", return_value=mock_content)
        mocker.patch("cli._read_json_file", return_value=mock_json_metadata)
        _update_version_for_library(
            "repo", "output", "packages/google-cloud-language", "1.2.3"
        )

        handle = m()
        assert handle.write.call_args_list[0].args[0] == '__version__ = "1.2.3"'

        # Get all the arguments passed to the mock's write method
        # and join them into a single string.
        written_content = "".join(
            [call.args[0] for call in handle.write.call_args_list[1:]]
        )
        # Create the expected output string with the correct formatting.
        assert (
            written_content
            == '{\n  "clientLibrary": {\n    "version": "1.2.3"\n  }\n}\n'
        )


def test_update_version_for_library_failure(mocker):
    """Tests that value error is raised if the version string cannot be found"""
    m = mock_open()

    mock_rglob = mocker.patch(
        "pathlib.Path.rglob", return_value=[pathlib.Path("repo/gapic_version.py")]
    )
    mock_content = "not found"
    with pytest.raises(ValueError):
        with unittest.mock.patch("cli.open", m):
            mocker.patch("cli._read_text_file", return_value=mock_content)
            _update_version_for_library(
                "repo", "output", "packages/google-cloud-language", "1.2.3"
            )


def test_get_previous_version_success(mock_state_file):
    """Test that the version can be retrieved from the state.yaml for a given library"""
    previous_version = _get_previous_version("google-cloud-language", LIBRARIAN_DIR)
    assert previous_version == "1.2.3"


def test_get_previous_version_failure(mock_state_file):
    """Test that ValueError is raised when a library does not exist in state.yaml"""
    with pytest.raises(ValueError):
        _get_previous_version("google-cloud-does-not-exist", LIBRARIAN_DIR)


def test_update_changelog_for_library_success(mocker):
    m = mock_open()

    mock_content = """# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-language/#history

## [2.17.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-language-v2.17.1...google-cloud-language-v2.17.2) (2025-06-11)

"""
    with unittest.mock.patch("cli.open", m):
        mocker.patch("cli._read_text_file", return_value=mock_content)
        _update_changelog_for_library(
            "repo",
            "output",
            _MOCK_LIBRARY_CHANGES,
            "1.2.3",
            "1.2.2",
            "google-cloud-language",
        )


def test_process_changelog_success():
    """Tests that value error is raised if the changelog anchor string cannot be found"""
    current_date = datetime.now().strftime("%Y-%m-%d")
    mock_content = """# Changelog\n[PyPI History][1]\n[1]: https://pypi.org/project/google-cloud-language/#history\n
## [1.2.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-language-v1.2.1...google-cloud-language-v1.2.2) (2025-06-11)"""
    expected_result = f"""# Changelog\n[PyPI History][1]\n[1]: https://pypi.org/project/google-cloud-language/#history\n
## [1.2.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-language-v1.2.2...google-cloud-language-v1.2.3) ({current_date})\n\n
### Documentation\n
* fix typo in BranchRule comment ([9461532e7d19c8d71709ec3b502e5d81340fb661](https://github.com/googleapis/google-cloud-python/commit/9461532e7d19c8d71709ec3b502e5d81340fb661))\n\n
### Features\n
* add new UpdateRepository API ([9461532e7d19c8d71709ec3b502e5d81340fb661](https://github.com/googleapis/google-cloud-python/commit/9461532e7d19c8d71709ec3b502e5d81340fb661))\n\n
### Bug Fixes\n
* some fix ([1231532e7d19c8d71709ec3b502e5d81340fb661](https://github.com/googleapis/google-cloud-python/commit/1231532e7d19c8d71709ec3b502e5d81340fb661))
* another fix ([1241532e7d19c8d71709ec3b502e5d81340fb661](https://github.com/googleapis/google-cloud-python/commit/1241532e7d19c8d71709ec3b502e5d81340fb661))\n
## [1.2.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-language-v1.2.1...google-cloud-language-v1.2.2) (2025-06-11)"""
    version = "1.2.3"
    previous_version = "1.2.2"
    library_id = "google-cloud-language"

    result = _process_changelog(
        mock_content, _MOCK_LIBRARY_CHANGES, version, previous_version, library_id
    )
    assert result == expected_result


def test_process_changelog_failure():
    """Tests that value error is raised if the changelog anchor string cannot be found"""
    with pytest.raises(ValueError):
        _process_changelog("", [], "", "", "")


def test_update_changelog_for_library_failure(mocker):
    m = mock_open()

    mock_content = """# Changelog"""

    with pytest.raises(ValueError):
        with unittest.mock.patch("cli.open", m):
            mocker.patch("cli._read_text_file", return_value=mock_content)
            _update_changelog_for_library(
                "repo",
                "output",
                _MOCK_LIBRARY_CHANGES,
                "1.2.3",
                "1.2.2",
                "google-cloud-language",
            )


def test_process_version_file_success():
    version_file_contents = '__version__ = "1.2.2"'
    new_version = "1.2.3"
    modified_content = _process_version_file(
        version_file_contents, new_version, "file.txt"
    )
    assert modified_content == f'__version__ = "{new_version}"'


def test_process_version_file_failure():
    """Tests that value error is raised if the version string cannot be found"""
    with pytest.raises(ValueError):
        _process_version_file("", "", "")


def test_create_main_version_header():
    current_date = datetime.now().strftime("%Y-%m-%d")
    expected_header = f"## [1.2.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-language-v1.2.2...google-cloud-language-v1.2.3) ({current_date})"
    previous_version = "1.2.2"
    version = "1.2.3"
    library_id = "google-cloud-language"
    actual_header = _create_main_version_header(version, previous_version, library_id)
    assert actual_header == expected_header


@pytest.fixture
def mock_path_class(mocker):
    """
    A mock instance is pre-configured as its return_value.
    """
    mock_instance = MagicMock(spec=Path)
    mock_class_patch = mocker.patch("cli.Path", return_value=mock_instance)
    return mock_class_patch


@pytest.mark.parametrize(
    "pkg_root_str, gapic_parent_str, expected_namespace",
    [
        (
            "repo/packages/google-cloud-lang",
            "repo/packages/google-cloud-lang/google/cloud/language",
            "google.cloud",
        ),
        (
            "repo/packages/google-ads",
            "repo/packages/google-ads/google/ads/v17",
            "google.ads",
        ),
        (
            "repo/packages/google-auth",
            "repo/packages/google-auth/google/auth",
            "google",
        ),
        ("repo/packages/google-api", "repo/packages/google-api/google", "google"),
    ],
)
def test_determine_library_namespace_success(
    pkg_root_str, gapic_parent_str, expected_namespace
):
    """Tests that the refactored namespace logic correctly calculates the relative namespace."""
    pkg_root_path = Path(pkg_root_str)
    gapic_parent_path = Path(gapic_parent_str)

    namespace = _determine_library_namespace(gapic_parent_path, pkg_root_path)
    assert namespace == expected_namespace


def test_determine_library_namespace_fails_not_subpath():
    """Tests that a ValueError is raised if the gapic path is not inside the package root."""
    pkg_root_path = Path("repo/packages/my-lib")
    gapic_parent_path = Path("SOME/OTHER/PATH/google/cloud/api")

    with pytest.raises(ValueError):
        _determine_library_namespace(gapic_parent_path, pkg_root_path)


def test_get_library_dist_name_success(mocker):
    mock_metadata = {"name": "my-lib", "version": "1.0.0"}
    mocker.patch("build.util.project_wheel_metadata", return_value=mock_metadata)
    assert _get_library_dist_name("my-lib", "repo") == "my-lib"


def test_verify_library_dist_name_setup_success(mocker):
    """Tests success when a library distribution name in setup.py is valid."""
    mock_setup_file = mocker.patch("cli._get_library_dist_name", return_value="my-lib")
    _verify_library_dist_name("my-lib", "repo")
    mock_setup_file.assert_called_once_with("my-lib", "repo")


def test_verify_library_dist_name_fail(mocker):
    """Tests failure when a library-id does not match the libary distribution name."""
    mocker.patch("cli._get_library_dist_name", return_value="invalid-lib")
    with pytest.raises(ValueError):
        _verify_library_dist_name("my-lib", "repo")


def test_verify_library_namespace_success_valid(mocker, mock_path_class):
    """Tests success when a single valid namespace is found."""
    # 1. Get the mock instance from the mock class's return_value
    mock_instance = mock_path_class.return_value

    # 2. Configure the mock instance
    mock_instance.is_dir.return_value = True
    mock_file = MagicMock(spec=Path)
    mock_file.parent = Path("/abs/repo/packages/my-lib/google/cloud/language")
    mock_instance.rglob.return_value = [mock_file]

    mock_determine_ns = mocker.patch(
        "cli._determine_library_namespace", return_value="google.cloud"
    )

    _verify_library_namespace("my-lib", "/abs/repo")

    # 3. Assert against the mock CLASS (from the fixture)
    mock_path_class.assert_called_once_with("/abs/repo/packages/my-lib")

    # 4. Verify the helper was called with the correct instance
    mock_determine_ns.assert_called_once_with(mock_file.parent, mock_instance)


def test_verify_library_namespace_failure_invalid(mocker, mock_path_class):
    """Tests failure when a namespace is found that is NOT in the valid list."""
    mock_instance = mock_path_class.return_value
    mock_instance.is_dir.return_value = True

    mock_file = MagicMock(spec=Path)
    mock_file.parent = Path("/abs/repo/packages/my-lib/google/api/core")
    mock_instance.rglob.return_value = [mock_file]

    mock_determine_ns = mocker.patch(
        "cli._determine_library_namespace", return_value="google.api"
    )

    with pytest.raises(ValueError):
        _verify_library_namespace("my-lib", "/abs/repo")

    # Verify the class was still called correctly
    mock_path_class.assert_called_once_with("/abs/repo/packages/my-lib")
    mock_determine_ns.assert_called_once_with(mock_file.parent, mock_instance)


def test_verify_library_namespace_error_no_directory(mocker, mock_path_class):
    """Tests that the specific ValueError is raised if the path isn't a directory."""
    mock_instance = mock_path_class.return_value
    mock_instance.is_dir.return_value = False  # Configure the failure case

    with pytest.raises(ValueError, match="Error: Path is not a directory"):
        _verify_library_namespace("my-lib", "repo")

    # Verify the function was called and triggered the check
    mock_path_class.assert_called_once_with("repo/packages/my-lib")


def test_verify_library_namespace_error_no_gapic_file(mocker, mock_path_class):
    """Tests that the specific ValueError is raised if no gapic files are found."""
    mock_instance = mock_path_class.return_value
    mock_instance.is_dir.return_value = True
    mock_instance.rglob.return_value = []  # rglob returns an empty list

    with pytest.raises(ValueError, match="Library is missing a `gapic_version.py`"):
        _verify_library_namespace("my-lib", "repo")

    # Verify the initial path logic still ran
    mock_path_class.assert_called_once_with("repo/packages/my-lib")
