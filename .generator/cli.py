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
import parse_googleapis_content
import re
import shutil
import subprocess
import sys
import yaml
from datetime import datetime
import tempfile
from pathlib import Path
from typing import Dict, List

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


def _read_text_file(path: str) -> str:
    """Helper function that reads a text file path and returns the content.

    Args:
        path(str): The file path to read.

    Returns:
        str: The contents of the file.
    """

    with open(path, "r") as f:
        return f.read()


def _write_text_file(path: str, updated_content: str):
    """Helper function that writes a text file path with the given content.

    Args:
        path(str): The file path to write.
        updated_content(str): The contents to write to the file.
    """

    with open(path, "w+") as f:
        os.makedirs(Path(updated_content).parent, exist_ok=True)
        f.write(updated_content)


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


def _write_json_file(path: str, updated_content: Dict):
    """Helper function that writes a json file with the given dictionary.

    Args:
        path(str): The file path to write.
        updated_content(Dict): The dictionary to write.
    """

    with open(path, "w") as f:
        json.dump(updated_content, f, indent=2)
        f.write("\n")


def handle_configure():
    # TODO(https://github.com/googleapis/librarian/issues/466): Implement configure command and update docstring.
    logger.info("'configure' command executed.")


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
                generator_options = []
                with open(f"{source}/{api_path}/BUILD.bazel", "r") as f:
                    content = f.read()
                    result = parse_googleapis_content.parse_content(content)
                    py_gapic_entry = [
                        key for key in result.keys() if key.endswith("_py_gapic")
                    ][0]

                    config_keys = [
                        "grpc_service_config",
                        "rest_numeric_enums",
                        "service_yaml",
                        "transport",
                    ]

                    for key in config_keys:
                        config_value = result[py_gapic_entry].get(key, None)
                        if config_value is not None:
                            new_key = key.replace("_", "-")
                            if key == "grpc_service_config":
                                new_key = "retry-config"

                            # There is a bug in the Python generator that treats all values of
                            # `rest-numeric-enums` as True, so just omit it if we want it to be False
                            if (
                                new_key == "rest-numeric-enums"
                                and config_value == "False"
                            ):
                                continue
                            elif new_key == "service-yaml" or new_key == "retry-config":
                                generator_options.append(
                                    f"{new_key}={api_path}/{config_value},"
                                )
                            else:
                                generator_options.append(f"{new_key}={config_value},")
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        generator_command = (
                            f"protoc {api_path}/*.proto --python_gapic_out={tmp_dir}"
                        )
                        if len(generator_options):
                            generator_command += f" --python_gapic_opt=metadata,"
                            for generator_option in generator_options:
                                generator_command += generator_option
                        subprocess.run([generator_command], cwd=source, shell=True)
                        api_version = api_path.split("/")[-1]
                        staging_dir = os.path.join(
                            output, "owl-bot-staging", library_id, api_version
                        )
                        os.makedirs(staging_dir, exist_ok=True)
                        logger.info(f"Preparing staging directory: {staging_dir}")
                        subprocess.run(f"cp -r {tmp_dir}/. {staging_dir}", shell=True)

        _copy_files_needed_for_post_processing(output, input, library_id)
        _run_post_processor(output, library_id)
        _clean_up_files_after_post_processing(output, library_id)

    except Exception as e:
        raise ValueError("Generation failed.") from e

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
        "unit-3.13",
        "docs",
        "system-3.13",
        "lint",
        "lint_setup_py",
        "mypy-3.13",
    ]
    _run_nox_sessions(sessions, librarian, repo)

    logger.info("'build' command executed.")


def _get_libraries_to_prepare_for_release(library_entries: Dict) -> List[dict]:
    """Get libraries which should be prepared for release. Only libraries
    which have the `release_triggered` field set to `True` will be returned.

    Args:
        library_entries(Dict): Dictionary containing all of the libraries to
        evaluate.

    Returns:
        List[dict]: List of all libraries which should be prepared for release,
        along with the corresponding information for the release.
    """
    return [
        library
        for library in library_entries["libraries"]
        if library.get("release_triggered")
    ]


def _update_global_changelog(
    changelog_src: str, changelog_dest: str, all_libraries: List[dict]
):
    """Updates the versions of libraries in the main CHANGELOG.md.

    Args:
        changelog_src(str): Path to the changelog file to read.
        changelog_dest(str): Path to the changelog file to write.
        all_libraries(Dict): Dictionary containing all of the library versions to
        modify.
    """

    def replace_version_in_changelog(content):
        new_content = content
        for library in all_libraries:
            package_name = library["id"]
            version = library["version"]
            # Find the entry for the given package in the format`<package name>==<version>`
            # Replace the `<version>` part of the string.
            pattern = re.compile(f"(\\[{re.escape(package_name)})(==)([\\d\\.]+)(\\])")
            replacement = f"\\g<1>=={version}\\g<4>"
            new_content = pattern.sub(replacement, new_content)
        return new_content

    updated_content = replace_version_in_changelog(_read_text_file(changelog_src))
    _write_text_file(changelog_dest, updated_content)


def _process_version_file(content, version, version_path) -> str:
    """This function searches for a version string in the
    given content, replaces the version and returns the content.

    Args:
        content(str): The contents where the version string should be replaced.
        version(str): The new version of the library.
        version_path(str): The relative path to the version file

    Raises: ValueError if the version string could not be found in the given content

    Returns: A string with the modified content.
    """
    pattern = r"(__version__\s*=\s*[\"'])([^\"']+)([\"'].*)"
    replacement_string = f"\\g<1>{version}\\g<3>"
    new_content, num_replacements = re.subn(pattern, replacement_string, content)
    if num_replacements == 0:
        raise ValueError(
            f"Could not find version string in {version_path}. File was not modified."
        )
    return new_content


def _update_version_for_library(
    repo: str, output: str, path_to_library: str, version: str
):
    """Updates the version string in `**/gapic_version.py` and `samples/**/snippet_metadata.json`
        for a given library.

    Args:
        repo(str): This directory will contain all directories that make up a
            library, the .librarian folder, and any global file declared in
            the config.yaml.
        output(str): Path to the directory in the container where modified
            code should be placed.
        path_to_library(str): Relative path to the library to update
        version(str): The new version of the library

    Raises: `ValueError` if a version string could not be located in `**/gapic_version.py`
        within the given library.
    """

    # Find and update gapic_version.py files
    gapic_version_files = Path(f"{repo}/{path_to_library}").rglob("**/gapic_version.py")
    for version_file in gapic_version_files:
        updated_content = _process_version_file(
            _read_text_file(version_file), version, version_file
        )
        output_path = f"{output}/{version_file.relative_to(repo)}"
        _write_text_file(output_path, updated_content)

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
        _write_json_file(output_path, metadata_contents)


def _get_previous_version(package_name: str, librarian: str) -> str:
    """Gets the previous version of the library from state.yaml.

    Args:
        package_name(str): name of the package.
        librarian(str): Path to the directory in the container which contains
            the `state.yaml` file.

    Returns:
        str: The version for a given library in state.yaml
    """
    state_yaml_path = f"{librarian}/{STATE_YAML_FILE}"

    with open(state_yaml_path, "r") as state_yaml_file:
        state_yaml = yaml.safe_load(state_yaml_file)
        for library in state_yaml.get("libraries", []):
            if library.get("id") == package_name:
                return library.get("version")

    raise ValueError(
        f"Could not determine previous version for {package_name} from state.yaml"
    )


def _process_changelog(
    content, library_changes, version, previous_version, package_name
):
    """This function searches the given content for the anchor pattern
    `[1]: https://pypi.org/project/{package_name}/#history`
    and adds an entry in the following format:

    ## [{version}](https://github.com/googleapis/google-cloud-python/compare/{package_name}-v{previous_version}...{package_name}-v{version}) (YYYY-MM-DD)

    ### Documentation

    * Update import statement example in README ([868b006](https://github.com/googleapis/google-cloud-python/commit/868b0069baf1a4bf6705986e0b6885419b35cdcc))

    Args:
        content(str): The contents of an existing changelog.
        library_changes(List[Dict]): List of dictionaries containing the changes
            for a given library.
        version(str): The new version of the library.
        previous_version: The previous version of the library.
        package_name(str): The name of the package where the changelog should
            be updated.

    Raises: ValueError if the anchor pattern string could not be found in the given content

    Returns: A string with the modified content.
    """
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
        adjusted_change_type = change_type.replace("!", "")
        change_type_map = {
            "feat": "Features",
            "fix": "Bug Fixes",
            "docs": "Documentation",
        }
        if adjusted_change_type in ["feat", "fix", "docs"]:
            entry_parts.append(f"\n\n### {change_type_map[adjusted_change_type]}\n")
            for change in changes:
                commit_link = f"([{change['source_commit_hash']}]({repo_url}/commit/{change['source_commit_hash']}))"
                entry_parts.append(f"* {change['subject']} {commit_link}")

    new_entry_text = "\n".join(entry_parts)
    anchor_pattern = re.compile(
        rf"(\[1\]: https://pypi\.org/project/{package_name}/#history)",
        re.MULTILINE,
    )
    replacement_text = f"\\g<1>\n\n{new_entry_text}"
    updated_content, num_subs = anchor_pattern.subn(replacement_text, content, count=1)
    if num_subs == 0:
        raise ValueError("Changelog anchor '[1]: ...#history' not found.")

    return updated_content


def _update_changelog_for_library(
    repo: str,
    output: str,
    library_changes: List[Dict],
    version: str,
    previous_version: str,
    package_name: str,
):
    """Prepends a new release entry with multiple, grouped changes, to a changelog.

    Args:
        repo(str): This directory will contain all directories that make up a
            library, the .librarian folder, and any global file declared in
            the config.yaml.
        output(str): Path to the directory in the container where modified
            code should be placed.
        library_changes(List[Dict]): List of dictionaries containing the changes
            for a given library
        version(str): The desired version
        previous_version(str): The version in state.yaml for a given package
        package_name(str): The name of the package where the changelog should
            be updated.
    """

    source_path = f"{repo}/packages/{package_name}/CHANGELOG.md"
    output_path = f"{output}/packages/{package_name}/CHANGELOG.md"
    updated_content = _process_changelog(
        _read_text_file(source_path),
        library_changes,
        version,
        previous_version,
        package_name,
    )
    _write_text_file(output_path, updated_content)


def handle_release_init(
    librarian: str = LIBRARIAN_DIR, repo: str = REPO_DIR, output: str = OUTPUT_DIR
):
    """The main coordinator for the release preparation process.

    This function prepares for the release of client libraries by reading a
    `librarian/release-init-request.json` file. The primary responsibility is
    to update all required files with the new version and commit information
    for libraries that have the `release_triggered` field set to `True`.

    See https://github.com/googleapis/librarian/blob/main/doc/container-contract.md#generate-container-command

    Args:
        librarian(str): Path to the directory in the container which contains
            the `release-init-request.json` file.
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

        _update_global_changelog(
            f"{repo}/CHANGELOG.md",
            f"{output}/CHANGELOG.md",
            libraries_to_prep_for_release,
        )

        # Prepare the release for each library by updating the
        # library specific version files and library specific changelog.
        for library_release_data in libraries_to_prep_for_release:
            version = library_release_data["version"]
            package_name = library_release_data["id"]
            library_changes = library_release_data["changes"]
            path_to_library = f"packages/{package_name}"
            _update_version_for_library(repo, output, path_to_library, version)

            # Get previous version from state.yaml
            previous_version = _get_previous_version(package_name, librarian)
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

    logger.info("'release-init' command executed.")


if __name__ == "__main__":  # pragma: NO COVER
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
        ("release-init", "Prepare to release a given set of libraries"),
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
            default=REPO_DIR,
        )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Pass specific arguments to the handler functions for generate/build
    if args.command == "generate":
        args.func(
            librarian=args.librarian,
            source=args.source,
            output=args.output,
            input=args.input,
        )
    elif args.command == "build":
        args.func(librarian=args.librarian, repo=args.repo)
    elif args.command == "release-init":
        args.func(librarian=args.librarian, repo=args.repo, output=args.output)
    else:
        args.func()
