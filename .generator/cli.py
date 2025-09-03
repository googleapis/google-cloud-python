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

import argparse
import glob
import itertools
import json
import logging
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import yaml

try:
    import synthtool
    from synthtool.languages import python_mono_repo

    SYNTHTOOL_INSTALLED = True
    SYNTHTOOL_IMPORT_ERROR = None
except ImportError as e:  # pragma: NO COVER
    SYNTHTOOL_IMPORT_ERROR = e
    SYNTHTOOL_INSTALLED = False

logger = logging.getLogger()

BUILD_REQUEST_FILE = "build-request.json"
GENERATE_REQUEST_FILE = "generate-request.json"
RELEASE_INIT_REQUEST_FILE = "release-init-request.json"
STATE_YAML_FILE = "state.yaml"

INPUT_DIR = "input"
LIBRARIAN_DIR = "librarian"
OUTPUT_DIR = "output"
REPO_DIR = "repo"
SOURCE_DIR = "source"


def _read_json_file(path: str) -> Dict:
    """Helper function that reads a json file path and returns the loaded json content.

    Args:
        path(str): The file path to read.

    Returns:
        dict: The parsed JSON content.

    Raises:
        FileNotFoundError: If the file is not found at the specified path.
        json.JSONDecodeError: If the file does not contain valid JSON.
        IOError: If there is an issue reading the file.
    """
    with open(path, "r") as f:
        return json.load(f)


def handle_configure():
    # TODO(https://github.com/googleapis/librarian/issues/466): Implement configure command and update docstring.
    logger.info("'configure' command executed.")


def _determine_bazel_rule(api_path: str, source: str) -> str:
    """Finds a Bazel rule by parsing the BUILD.bazel file directly.

    Args:
        api_path (str): The API path, e.g., 'google/cloud/language/v1'.
        source(str): The path to the root of the Bazel workspace.

    Returns:
        str: The discovered Bazel rule, e.g., '//google/cloud/language/v1:language-v1-py'.

    Raises:
        ValueError: If the file can't be processed or no matching rule is found.
    """
    logger.info(f"Determining Bazel rule for api_path: '{api_path}' by parsing file.")
    try:
        build_file_path = os.path.join(source, api_path, "BUILD.bazel")

        with open(build_file_path, "r") as f:
            content = f.read()

        match = re.search(r'name\s*=\s*"([^"]+-py)"', content)

        # This check is for a logical failure (no match), not a runtime exception.
        # It's good to keep it for clear error messaging.
        if not match:  # pragma: NO COVER
            raise ValueError(
                f"No Bazel rule with a name ending in '-py' found in {build_file_path}"
            )

        rule_name = match.group(1)
        bazel_rule = f"//{api_path}:{rule_name}"

        logger.info(f"Found Bazel rule: {bazel_rule}")
        return bazel_rule
    except Exception as e:
        raise ValueError(
            f"Failed to determine Bazel rule for '{api_path}' by parsing."
        ) from e


def _get_library_id(request_data: Dict) -> str:
    """Retrieve the library id from the given request dictionary

    Args:
        request_data(Dict): The contents `generate-request.json`.

    Raises:
        ValueError: If the key `id` does not exist in `request_data`.

    Returns:
        str: The id of the library in `generate-request.json`
    """
    library_id = request_data.get("id")
    if not library_id:
        raise ValueError("Request file is missing required 'id' field.")
    return library_id


def _build_bazel_target(bazel_rule: str, source: str):
    """Executes `bazelisk build` on a given Bazel rule.

    Args:
        bazel_rule(str): The Bazel rule to build.
        source(str): The path to the root of the Bazel workspace.

    Raises:
        ValueError: If the subprocess call fails.
    """
    logger.info(f"Executing build for rule: {bazel_rule}")
    try:
        # We're using the prewarmed bazel cache from the docker image to speed up the bazelisk commands.
        # Previously built artifacts are stored in `/bazel_cache/_bazel_ubuntu/output_base` and will be
        # used to speed up the build. `disk_cache` is used as the 'remote cache' and is also prewarmed as part of
        # the docker image.
        # See https://bazel.build/remote/caching#disk-cache which explains using a file system as a 'remote cache'.
        command = [
            "bazelisk",
            "--output_base=/bazel_cache/_bazel_ubuntu/output_base",
            "build",
            "--disk_cache=/bazel_cache/_bazel_ubuntu/cache/repos",
            "--incompatible_strict_action_env",
            bazel_rule,
        ]
        subprocess.run(
            command,
            cwd=source,
            text=True,
            check=True,
        )
        logger.info(f"Bazel build for {bazel_rule} rule completed successfully.")
    except Exception as e:
        raise ValueError(f"Bazel build for {bazel_rule} rule failed.") from e


def _locate_and_extract_artifact(
    bazel_rule: str,
    library_id: str,
    source: str,
    output: str,
    api_path: str,
):
    """Finds and extracts the tarball artifact from a Bazel build.

    Args:
        bazel_rule(str): The Bazel rule that was built.
        library_id(str): The ID of the library being generated.
        source(str): The path to the root of the Bazel workspace.
        output(str): The path to the location where generated output
            should be stored.
        api_path(str): The API path for the artifact

    Raises:
        ValueError: If failed to locate or extract artifact.
    """
    try:
        # 1. Find the bazel-bin output directory.
        logger.info("Locating Bazel output directory...")
        # Previously built artifacts are stored in `/bazel_cache/_bazel_ubuntu/output_base`.
        # See `--output_base` in `_build_bazel_target`
        info_command = [
            "bazelisk",
            "--output_base=/bazel_cache/_bazel_ubuntu/output_base",
            "info",
            "bazel-bin",
        ]
        result = subprocess.run(
            info_command,
            cwd=source,
            text=True,
            check=True,
            capture_output=True,
        )
        bazel_bin_path = result.stdout.strip()

        # 2. Construct the path to the generated tarball.
        rule_path, rule_name = bazel_rule.split(":")
        tarball_name = f"{rule_name}.tar.gz"
        tarball_path = os.path.join(bazel_bin_path, rule_path.strip("/"), tarball_name)
        logger.info(f"Found artifact at: {tarball_path}")

        # 3. Create a staging directory.
        api_version = api_path.split("/")[-1]
        staging_dir = os.path.join(output, "owl-bot-staging", library_id, api_version)
        os.makedirs(staging_dir, exist_ok=True)
        logger.info(f"Preparing staging directory: {staging_dir}")

        # 4. Extract the artifact.
        extract_command = ["tar", "-xvf", tarball_path, "--strip-components=1"]
        subprocess.run(
            extract_command, cwd=staging_dir, capture_output=True, text=True, check=True
        )
        logger.info(f"Artifact {tarball_path} extracted successfully.")

    except Exception as e:
        raise ValueError(
            f"Failed to locate or extract artifact for {bazel_rule} rule"
        ) from e


def _run_post_processor(output: str, library_id: str):
    """Runs the synthtool post-processor on the output directory.

    Args:
        output(str): Path to the directory in the container where code
            should be generated.
        library_id(str): The library id to be used for post processing.

    """
    os.chdir(output)
    path_to_library = f"packages/{library_id}"
    logger.info("Running Python post-processor...")
    if SYNTHTOOL_INSTALLED:
        python_mono_repo.owlbot_main(path_to_library)
    else:
        raise SYNTHTOOL_IMPORT_ERROR  # pragma: NO COVER
    logger.info("Python post-processor ran successfully.")


def _copy_files_needed_for_post_processing(output: str, input: str, library_id: str):
    """Copy files to the output directory whcih are needed during the post processing
    step, such as .repo-metadata.json and script/client-post-processing, using
    the input directory as the source.

    Args:
        output(str): Path to the directory in the container where code
            should be generated.
        input(str): The path to the directory in the container
            which contains additional generator input.
        library_id(str): The library id to be used for post processing.
    """

    path_to_library = f"packages/{library_id}"

    # We need to create these directories so that we can copy files necessary for post-processing.
    os.makedirs(f"{output}/{path_to_library}")
    os.makedirs(f"{output}/{path_to_library}/scripts/client-post-processing")
    shutil.copy(
        f"{input}/{path_to_library}/.repo-metadata.json",
        f"{output}/{path_to_library}/.repo-metadata.json",
    )

    # copy post-procesing files
    for post_processing_file in glob.glob(
        f"{input}/client-post-processing/*.yaml"
    ):  # pragma: NO COVER
        with open(post_processing_file, "r") as post_processing:
            if f"{path_to_library}/" in post_processing.read():
                shutil.copy(
                    post_processing_file,
                    f"{output}/{path_to_library}/scripts/client-post-processing",
                )


def _clean_up_files_after_post_processing(output: str, library_id: str):
    """
    Clean up files which should not be included in the generated client.
    This function is idempotent and will not fail if files are already removed.

    Args:
        output(str): Path to the directory in the container where code
            should be generated.
        library_id(str): The library id to be used for post processing.
    """
    path_to_library = f"packages/{library_id}"

    # Safely remove directories, ignoring errors if they don't exist.
    shutil.rmtree(f"{output}/{path_to_library}/.nox", ignore_errors=True)
    shutil.rmtree(f"{output}/owl-bot-staging", ignore_errors=True)

    # Safely remove specific files if they exist using pathlib.
    Path(f"{output}/{path_to_library}/CHANGELOG.md").unlink(missing_ok=True)
    Path(f"{output}/{path_to_library}/docs/CHANGELOG.md").unlink(missing_ok=True)
    Path(f"{output}/{path_to_library}/docs/README.rst").unlink(missing_ok=True)

    # Remove  `.repo-metadata.json` file to avoid ownership issues between
    # the container and librarian. Instead, preserve this file in the destination.
    Path(f"{output}/{path_to_library}/.repo-metadata.json").unlink(missing_ok=True)

    # The glob loops are already safe, as they do nothing if no files match.
    for post_processing_file in glob.glob(
        f"{output}/{path_to_library}/scripts/client-post-processing/*.yaml"
    ):  # pragma: NO COVER
        os.remove(post_processing_file)

    for gapic_version_file in glob.glob(
        f"{output}/{path_to_library}/**/gapic_version.py", recursive=True
    ):  # pragma: NO COVER
        os.remove(gapic_version_file)

    for snippet_metadata_file in glob.glob(
        f"{output}/{path_to_library}/samples/generated_samples/snippet_metadata*.json"
    ):  # pragma: NO COVER
        os.remove(snippet_metadata_file)


def handle_generate(
    librarian: str = LIBRARIAN_DIR,
    source: str = SOURCE_DIR,
    output: str = OUTPUT_DIR,
    input: str = INPUT_DIR,
):
    """The main coordinator for the code generation process.

    This function orchestrates the generation of a client library by reading a
    `librarian/generate-request.json` file, determining the necessary Bazel rule for each API, and
    (in future steps) executing the build.

    See https://github.com/googleapis/librarian/blob/main/doc/container-contract.md#generate-container-command

    Args:
        librarian(str): Path to the directory in the container which contains
            the librarian configuration.
        source(str): Path to the directory in the container which contains
            API protos.
        output(str): Path to the directory in the container where code
            should be generated.
        input(str): The path to the directory in the container
            which contains additional generator input.

    Raises:
        ValueError: If the `generate-request.json` file is not found or read.
    """

    try:
        # Read a generate-request.json file
        request_data = _read_json_file(f"{librarian}/{GENERATE_REQUEST_FILE}")
        library_id = _get_library_id(request_data)
        for api in request_data.get("apis", []):
            api_path = api.get("path")
            if api_path:
                bazel_rule = _determine_bazel_rule(api_path, source)
                _build_bazel_target(bazel_rule, source)
                _locate_and_extract_artifact(
                    bazel_rule, library_id, source, output, api_path
                )

        _copy_files_needed_for_post_processing(output, input, library_id)
        _run_post_processor(output, library_id)
        _clean_up_files_after_post_processing(output, library_id)

    except Exception as e:
        raise ValueError("Generation failed.") from e

    # TODO(https://github.com/googleapis/librarian/issues/448): Implement generate command and update docstring.
    logger.info("'generate' command executed.")


def _run_nox_sessions(sessions: List[str], librarian: str, repo: str):
    """Calls nox for all specified sessions.

    Args:
        sessions(List[str]): The list of nox sessions to run.
        librarian(str): The path to the librarian build configuration directory
    """
    # Read a build-request.json file
    current_session = None
    try:
        request_data = _read_json_file(f"{librarian}/{BUILD_REQUEST_FILE}")
        library_id = _get_library_id(request_data)
        for nox_session in sessions:
            _run_individual_session(nox_session, library_id, repo)

    except Exception as e:
        raise ValueError(f"Failed to run the nox session: {current_session}") from e


def _run_individual_session(nox_session: str, library_id: str, repo: str):
    """
    Calls nox with the specified sessions.

    Args:
        nox_session(str): The nox session to run
        library_id(str): The library id under test
    """

    command = [
        "nox",
        "-s",
        nox_session,
        "-f",
        f"{repo}/packages/{library_id}/noxfile.py",
    ]
    result = subprocess.run(command, text=True, check=True)
    logger.info(result)


def handle_build(librarian: str = LIBRARIAN_DIR, repo: str = REPO_DIR):
    """The main coordinator for validating client library generation."""
    sessions = [
        "unit-3.9",
        "unit-3.10",
        "unit-3.11",
        "unit-3.12",
        "unit-3.13",
        "docs",
        "system-3.13",
        "lint",
        "lint_setup_py",
        "mypy-3.13",
    ]
    _run_nox_sessions(sessions, librarian, repo)

    logger.info("'build' command executed.")


def _read_and_process_file(input_path: str, output_path: str, process_func) -> None:
    """Helper function to read, process, and write a file.

    Args:
        input_path (str): The path to the file to read.
        output_path (str): The path to the file to write.
        process_func (callable): A function that takes the file content as a string
                                  and writes the modified string to the output path.
    """
    os.makedirs(Path(output_path).parent, exist_ok=True)
    shutil.copy(input_path, output_path)

    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()

    updated_content = process_func(content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(updated_content)


def _get_libraries_to_prepare_for_release(library_entries: Dict) -> List[dict]:
    """Note the request data may have multiple libraries in it. Locate all
    libraries which should be prepared for release. This can be done by
    checking whether the `release_triggered` field is `true`.

    Args:
        library_entries(Dict): Dictionary containing all of the libraries
        present in the repository.

    Returns:
        List[dict]: List of all libraries which should be prepared for release,
        along with the corresponding information for the release.
    """
    return [
        library
        for library in library_entries["libraries"]
        if library.get("release_triggered")
    ]


def handle_release_init(
    librarian: str = LIBRARIAN_DIR, repo: str = REPO_DIR, output: str = OUTPUT_DIR
):
    """The main coordinator for the release process.

    This function prepares for the release of client libraries by reading a
    `librarian/release-init-request.json` file. The primary responsibility is
    to update all required files with the new version and commit information
    for libraries that have the `release_triggered` field set to `true`.

    See https://github.com/googleapis/librarian/blob/main/doc/container-contract.md#generate-container-command

    Args:
        librarian(str): Path to the directory in the container which contains
            the `release-init-request.json` file
        repo(str): This directory will contain all directories that make up a
            library, the .librarian folder, and any global file declared in
            the config.yaml.
        output(str): Path to the directory in the container where modified
            code should be placed.
    """

    try:
        # Read a release-init-request.json file
        request_data = _read_json_file(f"{librarian}/{RELEASE_INIT_REQUEST_FILE}")
        libraries_to_prep_for_release = _get_libraries_to_prepare_for_release(
            request_data
        )

        # Update the main changelog file
        source_path = f"{repo}/CHANGELOG.md"
        output_path = f"{output}/CHANGELOG.md"
        _update_global_changelog(
            source_path, output_path, libraries_to_prep_for_release
        )

        # Process each library to be released
        for library_release_data in libraries_to_prep_for_release:
            version = library_release_data["version"]
            library_changes = library_release_data["changes"]
            package_name = library_release_data["id"]
            path_to_library = f"packages/{package_name}"

            # Get previous version from state.yaml
            previous_version = _get_previous_version(repo, package_name, librarian)

            _update_version_for_library(repo, output, path_to_library, version)
            if previous_version != version:
                _update_changelog_for_library(
                    repo,
                    output,
                    library_changes,
                    version,
                    previous_version,
                    package_name,
                )

    except Exception as e:
        raise ValueError(f"Release init failed: {e}") from e


def _get_previous_version(repo: str, package_name: str, librarian: str) -> str:
    """Gets the previous version of the library from state.yaml."""
    state_yaml_path = f"{repo}/{LIBRARIAN_DIR}/{STATE_YAML_FILE}"
    if not os.path.exists(state_yaml_path):
        raise FileNotFoundError(f"State file not found at {state_yaml_path}")

    with open(state_yaml_path, "r") as state_yaml_file:
        state_yaml = yaml.safe_load(state_yaml_file)
        for library in state_yaml.get("libraries", []):
            if library.get("id") == package_name:
                return library.get("version")

    raise ValueError(
        f"Could not determine previous version for {package_name} from state.yaml"
    )


def _update_global_changelog(source_path: str, output_path: str, libraries: List[dict]):
    """Updates the main CHANGELOG.md with new versions."""

    def process_content(content):
        new_content = content
        for lib in libraries:
            package_name = lib["id"]
            version = lib["version"]
            pattern = re.compile(f"(\\[{re.escape(package_name)})(==)([\\d\\.]+)(\\])")
            replacement = f"\\g<1>=={version}\\g<4>"
            new_content = pattern.sub(replacement, new_content)
        return new_content

    _read_and_process_file(source_path, output_path, process_content)


def _update_changelog_for_library(
    repo: str,
    output: str,
    library_changes: List[Dict],
    version: str,
    previous_version: str,
    package_name: str,
):
    """Prepends a new release entry with multiple, grouped changes to a changelog."""

    def process_content(content):
        repo_url = "https://github.com/googleapis/google-cloud-python"
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Create the main version header
        version_header = (
            f"## [{version}]({repo_url}/compare/{package_name}-v{previous_version}"
            f"...{package_name}-v{version}) ({current_date})"
        )
        entry_parts = [version_header]

        # Group changes by type (e.g., feat, fix, docs)
        library_changes.sort(key=lambda x: x["type"])
        grouped_changes = itertools.groupby(library_changes, key=lambda x: x["type"])

        for change_type, changes in grouped_changes:
            # We only care about feat, fix, docs
            if change_type.replace("!", "") in ["feat", "fix", "docs"]:
                entry_parts.append(
                    f"\n\n### {change_type.capitalize().replace('!', '')}\n"
                )
                for change in changes:
                    commit_link = f"([{change['source_commit_hash']}]({repo_url}/commit/{change['source_commit_hash']}))"
                    entry_parts.append(f"* {change['subject']} {commit_link}")

        new_entry_text = "\n".join(entry_parts)
        anchor_pattern = re.compile(
            r"(\[1\]: https://pypi\.org/project/google-cloud-language/#history)",
            re.MULTILINE,
        )
        replacement_text = f"\\g<1>\n\n{new_entry_text}"
        updated_content, num_subs = anchor_pattern.subn(
            replacement_text, content, count=1
        )

        if num_subs == 0:
            raise ValueError("Changelog anchor '[1]: ...#history' not found.")

        return updated_content

    source_path = f"{repo}/packages/{package_name}/CHANGELOG.md"
    output_path = f"{output}/packages/{package_name}/CHANGELOG.md"
    _read_and_process_file(source_path, output_path, process_content)


def _update_version_for_library(
    repo: str, output: str, path_to_library: str, version: str
):
    """Updates the version string in various files for a library."""

    # Find and update gapic_version.py files
    gapic_version_files = Path(f"{repo}/{path_to_library}").rglob("**/gapic_version.py")
    for version_file in gapic_version_files:

        def process_version_file(content):
            pattern = r"(__version__\s*=\s*[\"'])([^\"']+)([\"'].*)"
            replacement_string = f"\\g<1>{version}\\g<3>"
            new_content, num_replacements = re.subn(
                pattern, replacement_string, content
            )
            if num_replacements == 0:
                raise Exception(
                    f"Could not find version string in {version_file}. File was not modified."
                )
            return new_content

        output_path = f"{output}/{version_file.relative_to(repo)}"
        _read_and_process_file(str(version_file), output_path, process_version_file)

    # Find and update snippet_metadata.json files
    snippet_metadata_files = Path(f"{repo}/{path_to_library}").rglob(
        "samples/**/*.json"
    )
    for metadata_file in snippet_metadata_files:
        output_path = f"{output}/{metadata_file.relative_to(repo)}"
        os.makedirs(Path(output_path).parent, exist_ok=True)
        shutil.copy(metadata_file, output_path)

        metadata_contents = _read_json_file(metadata_file)
        metadata_contents["clientLibrary"]["version"] = version

        with open(output_path, "w") as f:
            json.dump(metadata_contents, f, indent=2)
            f.write("\n")


def main():
    parser = argparse.ArgumentParser(description="A simple CLI tool.")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # Define commands and their corresponding handler functions
    handler_map = {
        "configure": handle_configure,
        "generate": handle_generate,
        "build": handle_build,
        "release-init": handle_release_init,
    }

    for command_name, help_text in [
        ("configure", "Onboard a new library or an api path to Librarian workflow."),
        ("generate", "generate a python client for an API."),
        ("build", "Run unit tests via nox for the generated library."),
        ("release-init", "Prepare to release a specific library"),
    ]:
        parser_cmd = subparsers.add_parser(command_name, help=help_text)
        parser_cmd.set_defaults(func=handler_map[command_name])
        parser_cmd.add_argument(
            "--librarian",
            type=str,
            help="Path to the directory in the container which contains the librarian configuration",
            default=LIBRARIAN_DIR,
        )
        parser_cmd.add_argument(
            "--input",
            type=str,
            help="Path to the directory in the container which contains additional generator input",
            default=INPUT_DIR,
        )
        parser_cmd.add_argument(
            "--output",
            type=str,
            help="Path to the directory in the container where code should be generated",
            default=OUTPUT_DIR,
        )
        parser_cmd.add_argument(
            "--source",
            type=str,
            help="Path to the directory in the container which contains API protos",
            default=SOURCE_DIR,
        )
        parser_cmd.add_argument(
            "--repo",
            type=str,
            help="Path to the directory in the container which contains google-cloud-python repository",
            default=SOURCE_DIR,
        )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Pass arguments to the selected handler function using a dynamic approach
    handler_args = {
        k: v for k, v in vars(args).items() if k != "command" and k != "func"
    }
    # Filter out arguments not expected by the function
    import inspect

    handler_func = args.func
    arg_spec = inspect.getfullargspec(handler_func)

    valid_handler_args = {
        k: v for k, v in handler_args.items() if k in arg_spec.args or arg_spec.varkw
    }

    handler_func(**valid_handler_args)


if __name__ == "__main__":  # pragma: NO COVER
    main()
