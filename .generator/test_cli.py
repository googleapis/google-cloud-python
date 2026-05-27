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
from datetime import date, datetime
from pathlib import Path
from unittest.mock import MagicMock, mock_open

import pytest
from cli import (
    BUILD_REQUEST_FILE,
    CONFIGURE_REQUEST_FILE,
    RELEASE_STAGE_REQUEST_FILE,
    SOURCE_DIR,
    STATE_YAML_FILE,
    LIBRARIAN_DIR,
    REPO_DIR,
    _create_main_version_header,
    _determine_library_namespace,
    _get_library_dist_name,
    _get_library_id,
    _get_package_name,
    _get_library_path,
    _get_libraries_to_prepare_for_release,
    _get_new_library_config,
    _get_previous_version,
    _get_repo_name_from_repo_metadata,
    _add_new_library_version,
    _prepare_new_library_config,
    _process_changelog,
    _process_version_file,
    _read_json_file,
    _read_text_file,
    _run_individual_session,
    _run_nox_sessions,
    _update_changelog_for_library,
    _update_global_changelog,
    _update_version_for_library,
    _verify_library_dist_name,
    _verify_library_namespace,
    _write_json_file,
    _write_text_file,
    _create_new_changelog_for_library,
    handle_build,
    handle_configure,
    handle_release_stage,
)


_MOCK_LIBRARY_CHANGES = [
    {
        "type": "feat",
        "subject": "add new UpdateRepository API",
        "body": "This adds the ability to update a repository's properties.",
        "piper_cl_number": "786353207",
        "commit_hash": "9461532e7d19c8d71709ec3b502e5d81340fb661",
    },
    {
        "type": "fix",
        "subject": "some fix",
        "body": "some body",
        "piper_cl_number": "786353208",
        "commit_hash": "1231532e7d19c8d71709ec3b502e5d81340fb661",
    },
    {
        "type": "fix",
        "subject": "another fix",
        "body": "",
        "piper_cl_number": "786353209",
        "commit_hash": "1241532e7d19c8d71709ec3b502e5d81340fb661",
    },
    {
        "type": "docs",
        "subject": "fix typo in BranchRule comment",
        "body": "",
        "piper_cl_number": "786353210",
        "commit_hash": "9461532e7d19c8d71709ec3b502e5d81340fb661",
    },
]



@pytest.fixture
def setup_dirs(tmp_path):
    """Creates input and output directories."""
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    return input_dir, output_dir


@pytest.fixture(autouse=True)
def _clear_lru_cache():
    """Automatically clears the cache of all LRU-cached functions after each test."""
    yield
    _get_repo_name_from_repo_metadata.cache_clear()


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
def mock_configure_request_data():
    """Returns mock data for configure-request.json."""
    return {
        "libraries": [
            {
                "id": "google-cloud-language",
                "apis": [{"path": "google/cloud/language/v1", "status": "new"}],
                "version": "",
            }
        ]
    }


@pytest.fixture
def mock_configure_request_file(tmp_path, monkeypatch, mock_configure_request_data):
    """Creates the mock request file at the correct path inside a temp dir."""
    # Create the path as expected by the script: .librarian/configure-request.json
    request_path = f"{LIBRARIAN_DIR}/{CONFIGURE_REQUEST_FILE}"
    request_dir = tmp_path / os.path.dirname(request_path)
    request_dir.mkdir(parents=True, exist_ok=True)
    request_file = request_dir / os.path.basename(request_path)

    request_file.write_text(json.dumps(mock_configure_request_data))

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


@pytest.fixture
def mock_release_stage_request_file(tmp_path, monkeypatch):
    """Creates the mock request file at the correct path inside a temp dir."""
    # Create the path as expected by the script: .librarian/release-request.json
    request_path = f"{LIBRARIAN_DIR}/{RELEASE_STAGE_REQUEST_FILE}"
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
                "tag_format": "{id}-v{version}",
            },
            {
                "id": "google-cloud-language",
                "apis": [{"path": "google/cloud/language/v1"}],
                "release_triggered": True,
                "version": "1.2.3",
                "changes": [],
                "tag_format": "{id}-v{version}",
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


def test_handle_configure_success(mock_configure_request_file, mocker):
    """Tests the successful execution path of handle_configure."""
    mocker.patch("cli._update_global_changelog", return_value=None)
    mock_write_json = mocker.patch("cli._write_json_file")
    mock_prepare_config = mocker.patch(
        "cli._prepare_new_library_config", return_value={"id": "prepared"}
    )
    mock_create_changelog = mocker.patch("cli._create_new_changelog_for_library")

    handle_configure()

    mock_prepare_config.assert_called_once()
    mock_write_json.assert_called_once_with(
        f"{LIBRARIAN_DIR}/configure-response.json", {"id": "prepared"}
    )


def test_handle_configure_no_new_library(mocker):
    """Tests that handle_configure fails if no new library is found."""
    mocker.patch("cli._read_json_file", return_value={"libraries": []})
    # The call to _prepare_new_library_config with an empty dict will raise a ValueError
    # because _get_library_id will fail.
    with pytest.raises(ValueError, match="Configuring a new library failed."):
        handle_configure()


def test_create_new_changelog_for_library(mocker):
    """Tests that the changelog files are created correctly."""
    library_id = "google-cloud-language"
    output = "output"
    mock_makedirs = mocker.patch("os.makedirs")
    mock_write_text_file = mocker.patch("cli._write_text_file")

    _create_new_changelog_for_library(library_id, output)

    package_changelog_path = f"{output}/packages/{library_id}/CHANGELOG.md"
    docs_changelog_path = f"{output}/packages/{library_id}/docs/CHANGELOG.md"

    # Check that makedirs was called for both parent directories
    mock_makedirs.assert_any_call(
        os.path.dirname(package_changelog_path), exist_ok=True
    )
    mock_makedirs.assert_any_call(os.path.dirname(docs_changelog_path), exist_ok=True)
    assert mock_makedirs.call_count == 2

    # Check that the files were "written" with the correct content
    changelog_content = f"# Changelog\n\n[PyPI History][1]\n\n[1]: https://pypi.org/project/{library_id}/#history\n"
    mock_write_text_file.assert_any_call(package_changelog_path, changelog_content)
    mock_write_text_file.assert_any_call(docs_changelog_path, changelog_content)
    assert mock_write_text_file.call_count == 2


def test_get_new_library_config_found(mock_configure_request_data):
    """Tests that the new library configuration is returned when found."""
    config = _get_new_library_config(mock_configure_request_data)
    assert config["id"] == "google-cloud-language"
    # Assert that the config is NOT modified
    assert "status" in config["apis"][0]


def test_get_new_library_config_not_found():
    """Tests that an empty dictionary is returned when no new library is found."""
    request_data = {
        "libraries": [
            {
                "id": "existing-library",
                "apis": [{"path": "path/v1", "status": "existing"}],
            },
        ]
    }
    config = _get_new_library_config(request_data)
    assert config == {}


def test_get_new_library_config_empty_input():
    """Tests that an empty dictionary is returned for empty input."""
    config = _get_new_library_config({})
    assert config == {}


def test_prepare_new_library_config(mocker):
    """Tests the preparation of a new library's configuration."""
    raw_config = {
        "id": "google-cloud-language",
        "apis": [{"path": "google/cloud/language/v1", "status": "new"}],
        "source_roots": None,
        "preserve_regex": None,
        "remove_regex": None,
        "version": "",
    }

    prepared_config = _prepare_new_library_config(raw_config)

    # Check that status is removed
    assert "status" not in prepared_config["apis"][0]
    # Check that defaults are added
    assert prepared_config["source_roots"] == ["packages/google-cloud-language"]
    assert (
        "packages/google-cloud-language/CHANGELOG.md"
        in prepared_config["preserve_regex"]
    )
    assert prepared_config["remove_regex"] == ["packages/google-cloud-language"]
    assert prepared_config["tag_format"] == "{id}-v{version}"
    assert prepared_config["version"] == "0.0.0"


def test_prepare_new_library_config_preserves_existing_values(mocker):
    """Tests that existing values in the config are not overwritten."""
    raw_config = {
        "id": "google-cloud-language",
        "apis": [{"path": "google/cloud/language/v1", "status": "new"}],
        "source_roots": ["packages/google-cloud-language-custom"],
        "preserve_regex": ["custom/regex"],
        "remove_regex": ["custom/remove"],
        "tag_format": "custom-format-{{version}}",
        "version": "4.5.6",
    }

    prepared_config = _prepare_new_library_config(raw_config)

    # Check that status is removed
    assert "status" not in prepared_config["apis"][0]
    # Check that existing values are preserved
    assert prepared_config["source_roots"] == ["packages/google-cloud-language-custom"]
    assert prepared_config["preserve_regex"] == ["custom/regex"]
    assert prepared_config["remove_regex"] == ["custom/remove"]
    assert prepared_config["tag_format"] == "custom-format-{{version}}"
    assert prepared_config["version"] == "4.5.6"


def test_add_new_library_version_populates_version(mocker):
    """Tests that the version is populated if it's missing."""
    config = {"version": ""}
    _add_new_library_version(config)
    assert config["version"] == "0.0.0"


def test_add_new_library_version_preserves_version():
    """Tests that an existing version is preserved."""
    config = {"version": "4.5.6"}
    _add_new_library_version(config)
    assert config["version"] == "4.5.6"


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



@pytest.mark.parametrize("is_mono_repo", [False, True])
def test_run_individual_session_success(mocker, caplog, is_mono_repo):
    """Tests that _run_individual_session calls nox with correct arguments and logs success."""
    caplog.set_level(logging.INFO)

    mock_subprocess_run = mocker.patch(
        "cli.subprocess.run", return_value=MagicMock(returncode=0)
    )

    test_session = "unit-3.10"
    test_library_id = "test-library"
    repo = "repo"
    _run_individual_session(test_session, test_library_id, repo, is_mono_repo)

    expected_command = [
        "nox",
        "-s",
        test_session,
        "-f",
        (
            f"{REPO_DIR}/packages/{test_library_id}/noxfile.py"
            if is_mono_repo
            else f"{REPO_DIR}/noxfile.py"
        ),
    ]
    mock_subprocess_run.assert_called_once_with(
        expected_command, text=True, check=True, timeout=1200
    )


def test_run_individual_session_failure(mocker):
    """Tests that _run_individual_session raises CalledProcessError if nox command fails."""
    mocker.patch(
        "cli.subprocess.run",
        side_effect=subprocess.CalledProcessError(
            1, "nox", stderr="Nox session failed"
        ),
    )

    with pytest.raises(subprocess.CalledProcessError):
        _run_individual_session("lint", "another-library", "repo", True)


@pytest.mark.parametrize(
    "is_mono_repo, nox_session_python_runtime",
    [
        (False, "3.14"),
        (True, "3.14"),
    ],
)
def test_run_nox_sessions_success(
    mocker,
    mock_generate_request_data_for_nox,
    is_mono_repo,
    nox_session_python_runtime,
):
    """Tests that _run_nox_sessions successfully runs all specified sessions."""
    mocker.patch("cli._read_json_file", return_value=mock_generate_request_data_for_nox)
    mocker.patch("cli._get_library_id", return_value="mock-library")
    mock_run_individual_session = mocker.patch("cli._run_individual_session")

    sessions_to_run = [
        f"unit-{nox_session_python_runtime}(protobuf_implementation='python')",
    ]
    _run_nox_sessions("mock-library", "repo", is_mono_repo)

    assert mock_run_individual_session.call_count == len(sessions_to_run)
    mock_run_individual_session.assert_has_calls(
        [
            mocker.call(
                f"unit-{nox_session_python_runtime}(protobuf_implementation='python')",
                "mock-library",
                "repo",
                is_mono_repo,
            ),
        ]
    )


def test_run_nox_sessions_read_file_failure(mocker):
    """Tests that _run_nox_sessions raises ValueError if _read_json_file fails."""
    mocker.patch("cli._read_json_file", side_effect=FileNotFoundError("file not found"))

    with pytest.raises(ValueError, match="Failed to run the nox session"):
        _run_nox_sessions("mock-library", "repo", True)


def test_run_nox_sessions_get_library_id_failure(mocker):
    """Tests that _run_nox_sessions raises ValueError if _get_library_id fails."""
    mocker.patch("cli._read_json_file", return_value={"apis": []})  # Missing 'id'
    mocker.patch(
        "cli._get_library_id",
        side_effect=ValueError("Request file is missing required 'id' field."),
    )

    with pytest.raises(ValueError, match="Failed to run the nox session"):
        _run_nox_sessions("mock-library", "repo", True)


@pytest.mark.parametrize("is_mono_repo", [False, True])
def test_run_nox_sessions_individual_session_failure(
    mocker, mock_generate_request_data_for_nox, is_mono_repo
):
    """Tests that _run_nox_sessions raises ValueError if _run_individual_session fails."""
    mocker.patch("cli._read_json_file", return_value=mock_generate_request_data_for_nox)
    mocker.patch("cli._get_library_id", return_value="mock-library")
    mock_run_individual_session = mocker.patch(
        "cli._run_individual_session",
        side_effect=[subprocess.CalledProcessError(1, "nox", "session failed")],
    )

    with pytest.raises(ValueError, match="Failed to run the nox session"):
        _run_nox_sessions("mock-library", "repo", is_mono_repo)

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



def test_get_libraries_to_prepare_for_release(mock_release_stage_request_file):
    """
    Tests that only libraries with the `release_triggered` field set to `True` are
    returned.
    """
    request_data = _read_json_file(f"{LIBRARIAN_DIR}/{RELEASE_STAGE_REQUEST_FILE}")
    libraries_to_prep_for_release = _get_libraries_to_prepare_for_release(request_data)
    assert len(libraries_to_prep_for_release) == 1
    assert "google-cloud-language" in libraries_to_prep_for_release[0]["id"]
    assert libraries_to_prep_for_release[0]["release_triggered"]


def test_handle_release_stage_success(mocker, mock_release_stage_request_file):
    """
    Simply tests that `handle_release_stage` runs without errors.
    """
    mocker.patch("cli._update_global_changelog", return_value=None)
    mocker.patch("cli._update_version_for_library", return_value=None)
    mocker.patch("cli._get_previous_version", return_value=None)
    mocker.patch("cli._update_changelog_for_library", return_value=None)
    handle_release_stage()


def test_handle_release_stage_is_generated_success(
    mocker, mock_release_stage_request_file
):
    """
    Tests that `handle_release_stage` calls `_update_global_changelog` when the
    `packages` directory exists.
    """
    mocker.patch("pathlib.Path.exists", return_value=True)
    mock_update_global_changelog = mocker.patch("cli._update_global_changelog")
    mocker.patch("cli._update_version_for_library")
    mocker.patch("cli._get_previous_version", return_value="1.2.2")
    mocker.patch("cli._update_changelog_for_library")

    handle_release_stage()

    mock_update_global_changelog.assert_called_once()


def test_handle_release_stage_fail_value_error_file():
    """
    Tests that handle_release_stage fails to read `librarian/release-stage-request.json`.
    """
    with pytest.raises(ValueError, match="No such file or directory"):
        handle_release_stage()


def test_handle_release_stage_fail_value_error_version(mocker):
    m = mock_open()

    mock_release_stage_request_content = {
        "libraries": [
            {
                "id": "google-cloud-language",
                "apis": [{"path": "google/cloud/language/v1"}],
                "release_triggered": True,
                "version": "1.2.2",
                "changes": [],
                "tag_format": "{id}-v{version}",
            },
        ]
    }
    with unittest.mock.patch("cli.open", m):
        mocker.patch(
            "cli._get_libraries_to_prepare_for_release",
            return_value=mock_release_stage_request_content["libraries"],
        )
        mocker.patch("cli._get_previous_version", return_value="1.2.2")
        mocker.patch("cli._process_changelog", return_value=None)
        mocker.patch(
            "cli._read_json_file", return_value=mock_release_stage_request_content
        )
        with pytest.raises(
            ValueError, match="is the same as the version in state.yaml"
        ):
            handle_release_stage()


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


def test_update_global_changelog(mocker, mock_release_stage_request_file):
    """Tests that the global changelog is updated
    with the new version for a given library.
    See https://docs.python.org/3/library/unittest.mock.html#mock-open
    """
    m = mock_open()
    request_data = _read_json_file(f"{LIBRARIAN_DIR}/{RELEASE_STAGE_REQUEST_FILE}")
    libraries = _get_libraries_to_prepare_for_release(request_data)

    with unittest.mock.patch("cli.open", m):
        mocker.patch(
            "cli._read_text_file", return_value="[google-cloud-language==1.2.2]"
        )
        _update_global_changelog("source", "output", libraries)

        handle = m()
        handle.write.assert_called_once_with("[google-cloud-language==1.2.3]")


def test_update_version_for_library_success_gapic(mocker):
    mock_content = '__version__ = "1.2.2"'
    mock_json_metadata = {"clientLibrary": {"version": "0.1.0"}}
    mock_shutil_copy = mocker.patch("shutil.copy")

    m = mock_open()

    mock_rglob = mocker.patch("pathlib.Path.rglob")
    mock_rglob.side_effect = [
        [
            pathlib.Path("repo/gapic_version.py"),
            pathlib.Path("repo/tests/gapic_version.py"),
        ],  # 1st call (gapic_version.py)
        [pathlib.Path("repo/types/version.py")],  # 2nd call (types/version.py).
        [pathlib.Path("repo/samples/snippet_metadata.json")],  # 3rd call (snippets)
    ]
    mock_read_text_file = mocker.patch("cli._read_text_file")
    mock_read_text_file.side_effect = [
        mock_content,  # 1st call (gapic_version.py)
        # Do not process version files in the `types` directory as some
        # GAPIC libraries have `version.py` which are generated from
        # `version.proto` and do not include SDK versions.
        # Leave the content as empty because it doesn't contain version information
        "",  # 2nd call (tests/gapic_version.py)
        "",  # 3rd call (types/version.py)
    ]

    with unittest.mock.patch("cli.open", m):
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


def test_update_version_for_library_success_proto_only_setup_py(mocker):
    m = mock_open()

    mock_rglob = mocker.patch("pathlib.Path.rglob")
    mock_rglob.side_effect = [
        [],
        [pathlib.Path("repo/setup.py")],
        [pathlib.Path("repo/samples/snippet_metadata.json")],
    ]
    mock_shutil_copy = mocker.patch("shutil.copy")
    mock_content = 'version = "1.2.2"'
    mock_json_metadata = {"clientLibrary": {"version": "0.1.0"}}

    with unittest.mock.patch("cli.open", m):
        mocker.patch("cli._read_text_file", return_value=mock_content)
        mocker.patch("cli._read_json_file", return_value=mock_json_metadata)
        _update_version_for_library(
            "repo", "output", "packages/google-cloud-language", "1.2.3"
        )

        handle = m()
        assert handle.write.call_args_list[0].args[0] == 'version = "1.2.3"'
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


def test_update_version_for_library_success_with_date_string(mocker):
    m = mock_open()

    mock_rglob = mocker.patch("pathlib.Path.rglob")
    mock_rglob.side_effect = [
        [],
        [pathlib.Path("repo/setup.py")],
        [pathlib.Path("repo/samples/snippet_metadata.json")],
    ]
    mock_shutil_copy = mocker.patch("shutil.copy")
    mock_content = 'version = "1.2.2"\n__release_date__ = "2025-11-03"'
    mock_json_metadata = {"clientLibrary": {"version": "0.1.0"}}
    today_iso = date.today().isoformat()

    with unittest.mock.patch("cli.open", m):
        mocker.patch("cli._read_text_file", return_value=mock_content)
        mocker.patch("cli._read_json_file", return_value=mock_json_metadata)
        _update_version_for_library(
            "repo", "output", "packages/google-cloud-language", "1.2.3"
        )

        handle = m()
        assert (
            handle.write.call_args_list[0].args[0]
            == f'version = "1.2.3"\n__release_date__ = "{today_iso}"'
        )
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


def test_update_version_for_library_success_proto_only_pyproject_toml(mocker):
    m = mock_open()

    mock_path_exists = mocker.patch("pathlib.Path.exists", return_value=True)
    mock_rglob = mocker.patch("pathlib.Path.rglob")
    mock_rglob.side_effect = [
        [],  # gapic_version.py
        [],  # version.py
        [pathlib.Path("repo/samples/snippet_metadata.json")],
    ]
    mock_shutil_copy = mocker.patch("shutil.copy")
    mock_content = 'version = "1.2.2"'
    mock_json_metadata = {"clientLibrary": {"version": "0.1.0"}}

    with unittest.mock.patch("cli.open", m):
        mocker.patch("cli._read_text_file", return_value=mock_content)
        mocker.patch("cli._read_json_file", return_value=mock_json_metadata)
        _update_version_for_library(
            "repo", "output", "packages/google-cloud-language", "1.2.3"
        )

        handle = m()
        assert handle.write.call_args_list[0].args[0] == 'version = "1.2.3"'
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


def test_update_changelog_for_library_writes_both_changelogs(mocker):
    """Tests that _update_changelog_for_library writes to both changelogs."""
    mock_content = """# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-language/#history
"""
    mock_read = mocker.patch("cli._read_text_file", return_value=mock_content)
    mock_write = mocker.patch("cli._write_text_file")
    mock_path_exists = mocker.patch("cli.os.path.lexists", return_value=True)
    _update_changelog_for_library(
        "repo",
        "output",
        _MOCK_LIBRARY_CHANGES,
        "1.2.3",
        "1.2.2",
        "google-cloud-language",
        True,
        "{id}-v{version}",
    )

    assert mock_write.call_count == 2
    mock_write.assert_any_call(
        "output/packages/google-cloud-language/CHANGELOG.md", mocker.ANY
    )
    mock_write.assert_any_call(
        "output/packages/google-cloud-language/docs/CHANGELOG.md", mocker.ANY
    )


def test_update_changelog_for_library_single_repo(mocker):
    """Tests that _update_changelog_for_library writes to both changelogs in a single repo."""
    mock_content = """# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-language/#history
"""
    mock_read = mocker.patch("cli._read_text_file", return_value=mock_content)
    mock_write = mocker.patch("cli._write_text_file")
    mock_path_exists = mocker.patch("cli.os.path.lexists", return_value=True)
    mocker.patch(
        "cli._get_repo_name_from_repo_metadata",
        return_value="googleapis/google-cloud-python",
    )
    _update_changelog_for_library(
        "repo",
        "output",
        _MOCK_LIBRARY_CHANGES,
        "1.2.3",
        "1.2.2",
        "google-cloud-language",
        False,
        "v{version}",
    )

    assert mock_write.call_count == 2
    mock_write.assert_any_call("output/CHANGELOG.md", mocker.ANY)
    mock_write.assert_any_call("output/docs/CHANGELOG.md", mocker.ANY)


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
    tag_format = "{id}-v{version}"

    result = _process_changelog(
        mock_content,
        _MOCK_LIBRARY_CHANGES,
        version,
        previous_version,
        library_id,
        "googleapis/google-cloud-python",
        tag_format,
    )
    assert result == expected_result


def test_process_changelog_success_preview():
    """Tests that a preview package updates its changelog correctly when the anchor has the standard package name."""
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
    library_id = "google-cloud-language-preview"
    tag_format = "google-cloud-language-v{version}"

    result = _process_changelog(
        mock_content,
        _MOCK_LIBRARY_CHANGES,
        version,
        previous_version,
        library_id,
        "googleapis/google-cloud-python",
        tag_format,
    )
    assert result == expected_result


def test_process_changelog_failure():
    """Tests that value error is raised if the changelog anchor string cannot be found"""
    with pytest.raises(ValueError):
        _process_changelog("", [], "", "", "", "googleapis/google-cloud-python", "")


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
                True,
                "{id}-v{version}",
            )


def test_process_version_file_success():
    version_file_contents = 'version = "1.2.2"'
    new_version = "1.2.3"
    modified_content = _process_version_file(
        version_file_contents, new_version, Path("file.txt")
    )
    assert modified_content == f'version = "{new_version}"'


def test_process_version_file_failure():
    """Tests that value error is raised if the version string cannot be found"""
    with pytest.raises(ValueError):
        _process_version_file("", "", Path(""))


@pytest.mark.parametrize(
    "tag_format,expected_tag_result",
    [(r"{id}-v{version}", "google-cloud-language-v"), (r"v{version}", "v")],
)
def test_create_main_version_header(tag_format, expected_tag_result):
    current_date = datetime.now().strftime("%Y-%m-%d")
    expected_header = f"## [1.2.3](https://github.com/googleapis/google-cloud-python/compare/{expected_tag_result}1.2.2...{expected_tag_result}1.2.3) ({current_date})"
    previous_version = "1.2.2"
    version = "1.2.3"
    library_id = "google-cloud-language"
    tag_format = tag_format
    actual_header = _create_main_version_header(
        version,
        previous_version,
        library_id,
        "googleapis/google-cloud-python",
        tag_format,
    )
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


@pytest.mark.parametrize("is_mono_repo", [False, True])
def test_get_library_dist_name_success(mocker, is_mono_repo):
    mock_metadata = {"name": "my-lib", "version": "1.0.0"}
    mocker.patch("build.util.project_wheel_metadata", return_value=mock_metadata)
    assert _get_library_dist_name("my-lib", "repo", is_mono_repo) == "my-lib"


@pytest.mark.parametrize("is_mono_repo", [False, True])
def test_verify_library_dist_name_setup_success(mocker, is_mono_repo):
    """Tests success when a library distribution name in setup.py is valid."""
    mock_setup_file = mocker.patch("cli._get_library_dist_name", return_value="my-lib")
    _verify_library_dist_name("my-lib", "repo", is_mono_repo)
    mock_setup_file.assert_called_once_with("my-lib", "repo", is_mono_repo)


def test_verify_library_dist_name_fail(mocker):
    """Tests failure when a library-id does not match the libary distribution name."""
    mocker.patch("cli._get_library_dist_name", return_value="invalid-lib")
    with pytest.raises(ValueError):
        _verify_library_dist_name("my-lib", "repo", True)


@pytest.mark.parametrize("is_mono_repo", [False, True])
def test_verify_library_namespace_success_valid(mocker, mock_path_class, is_mono_repo):
    """Tests success when a single valid namespace is found."""

    # 1. Get the mock instance from the mock class's return_value
    mock_instance = mock_path_class.return_value  # This is library_path

    # 2. Configure the mock instance
    mock_instance.is_dir.return_value = True
    mock_files_gapic_version = MagicMock(spec=Path)
    mock_gapic_parent = MagicMock(spec=Path)
    mock_gapic_parent.__str__.return_value = (
        "/abs/repo/packages/my-lib/google/cloud/language"
        if is_mono_repo
        else "/abs/repo/google/cloud/language"
    )
    mock_files_gapic_version.parent = mock_gapic_parent
    mock_files_proto = MagicMock(spec=Path)
    mock_proto_parent = MagicMock(spec=Path)
    mock_files_proto.parent = mock_proto_parent
    mock_proto_parent.relative_to.return_value = MagicMock()
    mock_proto_parent.relative_to.return_value.__str__.return_value = (
        "google/cloud/language/v1"
    )
    mock_proto_parent.__str__.return_value = (
        "/abs/repo/packages/my-lib/google/cloud/language/v1/proto"
        if is_mono_repo
        else "/abs/repo/google/cloud/language/v1/proto"
    )
    mock_instance.rglob.return_value = [mock_files_gapic_version, mock_files_proto]

    mock_determine_ns = mocker.patch(
        "cli._determine_library_namespace", return_value="google.cloud"
    )

    _verify_library_namespace("my-lib", "/abs/repo", is_mono_repo)

    # 3. Assert against the mock CLASS (from the fixture)
    mock_path_class.assert_called_once_with(
        "/abs/repo/packages/my-lib" if is_mono_repo else "/abs/repo"
    )

    # 4. Verify the helper was called with the correct instance
    assert mock_determine_ns.call_count == 2
    mock_determine_ns.assert_any_call(mock_gapic_parent, mock_instance)
    mock_determine_ns.assert_any_call(mock_proto_parent, mock_instance)


@pytest.mark.parametrize("is_mono_repo", [False, True])
def test_verify_library_namespace_excludes_proto_dir(
    mocker, mock_path_class, is_mono_repo
):
    """Tests that a proto file path ending in 'proto' is correctly excluded."""

    mock_instance = mock_path_class.return_value  # This is library_path
    mock_instance.is_dir.return_value = True

    mock_exclude_file = MagicMock(spec=Path)
    mock_exclude_parent = MagicMock(spec=Path)
    mock_exclude_file.parent = mock_exclude_parent

    mock_relative_result = MagicMock()
    mock_relative_result.__str__.return_value = "google/cloud/language/v1/proto"
    mock_exclude_parent.relative_to.return_value = mock_relative_result
    mock_exclude_parent.__str__.return_value = (
        "/abs/repo/packages/my-lib/google/cloud/language/v1/proto"
        if is_mono_repo
        else "/abs/repo/google/cloud/language/v1/proto"
    )

    mock_instance.rglob.side_effect = [[], [mock_exclude_file]]
    mock_determine_ns = mocker.patch("cli._determine_library_namespace", autospec=True)

    with pytest.raises(ValueError) as excinfo:
        _verify_library_namespace("my-lib", "/abs/repo", is_mono_repo)

    assert "namespace cannot be determined" in str(excinfo.value)
    mock_determine_ns.assert_not_called()
    mock_path_class.assert_called_once_with(
        "/abs/repo/packages/my-lib" if is_mono_repo else "/abs/repo"
    )


def test_verify_library_namespace_failure_invalid(mocker, mock_path_class):
    """Tests failure when a namespace is found that is NOT in the valid list."""
    mock_instance = mock_path_class.return_value
    mock_instance.is_dir.return_value = True

    mock_file = MagicMock(spec=Path)
    mock_parent = MagicMock(spec=Path)
    mock_parent.__str__.return_value = "/abs/repo/packages/my-lib/google/api/core"
    mock_file.parent = mock_parent
    mock_relative_result = MagicMock()
    mock_relative_result.__str__.return_value = (
        "google/api/core"  # Does not end with 'proto' or start with 'samples'
    )
    mock_parent.relative_to.return_value = mock_relative_result
    mock_instance.rglob.return_value = [mock_file]
    mock_determine_ns = mocker.patch(
        "cli._determine_library_namespace",
        return_value="google.apis",  # NOT in valid_namespaces
    )
    with pytest.raises(ValueError) as excinfo:
        _verify_library_namespace("my-lib", "/abs/repo", True)
    assert "The namespace `google.apis` for `my-lib` must be one of" in str(
        excinfo.value
    )

    # Verify the class was still called correctly
    mock_path_class.assert_called_once_with("/abs/repo/packages/my-lib")
    mock_determine_ns.assert_called_once_with(mock_parent, mock_instance)


@pytest.mark.parametrize("is_mono_repo", [False, True])
def test_verify_library_namespace_error_no_directory(
    mocker, mock_path_class, is_mono_repo
):
    """Tests that the specific ValueError is raised if the path isn't a directory."""
    mock_instance = mock_path_class.return_value
    mock_instance.is_dir.return_value = False  # Configure the failure case

    with pytest.raises(ValueError, match="Error: Path is not a directory"):
        _verify_library_namespace("my-lib", "repo", is_mono_repo)

    # Verify the function was called and triggered the check
    mock_path_class.assert_called_once_with(
        "repo/packages/my-lib" if is_mono_repo else "repo"
    )


@pytest.mark.parametrize("is_mono_repo", [False, True])
def test_verify_library_namespace_error_no_gapic_file(
    mocker, mock_path_class, is_mono_repo
):
    """Tests that the specific ValueError is raised if no gapic files are found."""
    mock_instance = mock_path_class.return_value
    mock_instance.is_dir.return_value = True
    mock_instance.rglob.return_value = []  # rglob returns an empty list

    with pytest.raises(ValueError, match="Library is missing a `gapic_version.py`"):
        _verify_library_namespace("my-lib", "repo", is_mono_repo)

    # Verify the initial path logic still ran
    mock_path_class.assert_called_once_with(
        "repo/packages/my-lib" if is_mono_repo else "repo"
    )


def test_get_repo_name_from_repo_metadata_success(mocker):
    """Tests that the repo name is returned when it exists."""
    mocker.patch(
        "cli._read_json_file", return_value={"repo": "googleapis/google-cloud-python"}
    )
    repo_name = _get_repo_name_from_repo_metadata("base", "library_id", False)
    assert repo_name == "googleapis/google-cloud-python"


def test_get_repo_name_from_repo_metadata_missing_repo(mocker):
    """Tests that a ValueError is raised when the repo field is missing."""
    mocker.patch("cli._read_json_file", return_value={})
    with pytest.raises(ValueError):
        _get_repo_name_from_repo_metadata("base", "library_id", False)


def test_get_package_name():
    assert _get_package_name("google-cloud-language") == "google-cloud-language"
    assert _get_package_name("google-cloud-language-preview") == "google-cloud-language"
    assert _get_package_name("google-cloud-language-preview-preview") == "google-cloud-language-preview"


@pytest.mark.parametrize(
    "library_id, is_mono_repo, expected_path",
    [
        ("google-cloud-language", True, "packages/google-cloud-language"),
        ("google-cloud-language-preview", True, "preview-packages/google-cloud-language"),
        ("google-cloud-language", False, "."),
        ("google-cloud-language-preview", False, "."),
    ],
)
def test_get_library_path(library_id, is_mono_repo, expected_path):
    assert _get_library_path(library_id, is_mono_repo) == expected_path


def test_update_changelog_for_library_preview_package(mocker):
    """Tests that _update_changelog_for_library writes to preview-packages directory for preview libraries."""
    mock_content = """# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-language/#history
"""
    mock_read = mocker.patch("cli._read_text_file", return_value=mock_content)
    mock_write = mocker.patch("cli._write_text_file")
    mock_path_exists = mocker.patch("cli.os.path.lexists", return_value=True)
    _update_changelog_for_library(
        "repo",
        "output",
        _MOCK_LIBRARY_CHANGES,
        "1.2.3",
        "1.2.2",
        "google-cloud-language-preview",
        True,
        "{id}-v{version}",
    )

    assert mock_write.call_count == 2
    mock_write.assert_any_call(
        "output/preview-packages/google-cloud-language/CHANGELOG.md", mocker.ANY
    )
    mock_write.assert_any_call(
        "output/preview-packages/google-cloud-language/docs/CHANGELOG.md", mocker.ANY
    )
