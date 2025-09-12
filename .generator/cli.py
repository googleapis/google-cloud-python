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
import yaml
from datetime import datetime
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

_REPO_URL = "https://github.com/googleapis/google-cloud-python"


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

    os.makedirs(Path(path).parent, exist_ok=True)
    with open(path, "w") as f:
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

    logger.info("'generate' command executed.")


def _run_nox_sessions(library_id: str, repo: str):
    """Calls nox for all specified sessions.

    Args:
        library_id(str): The library id under test.
        repo(str): This directory will contain all directories that make up a
            library, the .librarian folder, and any global file declared in
            the config.yaml.
    """
    sessions = [
        "unit-3.9",
        "unit-3.13",
        "docs",
        "lint",
        "lint_setup_py",
        "mypy-3.13",
    ]
    current_session = None
    try:
        for nox_session in sessions:
            current_session = nox_session
            _run_individual_session(nox_session, library_id, repo)

    except Exception as e:
        raise ValueError(f"Failed to run the nox session: {current_session}") from e


def _run_individual_session(nox_session: str, library_id: str, repo: str):
    """
    Calls nox with the specified sessions.

    Args:
        nox_session(str): The nox session to run.
        library_id(str): The library id under test.
        repo(str): This directory will contain all directories that make up a
            library, the .librarian folder, and any global file declared in
            the config.yaml.
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


def _determine_library_namespace(
    gapic_parent_path: Path, package_root_path: Path
) -> str:
    """
    Determines the namespace from the gapic file's parent path relative
    to its package root.

    Args:
        gapic_parent_path (Path): The absolute path to the directory containing
                                  gapic_version.py (e.g., .../google/cloud/language).
        package_root_path (Path): The absolute path to the root of the package
                                  (e.g., .../packages/google-cloud-language).
    """
    # This robustly calculates the relative path, e.g., "google/cloud/language"
    relative_path = gapic_parent_path.relative_to(package_root_path)

    # relative_path.parts will be like: ('google', 'cloud', 'language')
    # We want all parts *except* the last one (the service dir) to form the namespace.
    namespace_parts = relative_path.parts[:-1]

    if not namespace_parts and relative_path.parts:
        # This handles the edge case where the parts are just ('google',).
        # This implies the namespace is just "google".
        return ".".join(relative_path.parts)

    return ".".join(namespace_parts)


def _verify_library_namespace(library_id: str, repo: str):
    """
    Verifies that all found package namespaces are one of
    `google`, `google.cloud`, or `google.ads`.

    Args:
        library_id (str): The library id under test (e.g., "google-cloud-language").
        repo (str): The path to the root of the repository.
    """
    # TODO(https://github.com/googleapis/google-cloud-python/issues/14376): Update the list of namespaces which are exceptions.
    exception_namespaces = ["google.cloud.billing"]
    valid_namespaces = [
        "google",
        "google.apps",
        "google.ads",
        "google.cloud",
        "google.maps",
        "google.shopping",
        *exception_namespaces,
    ]
    gapic_version_file = "gapic_version.py"

    # This is now the "package root" path we will use for comparison
    library_path = Path(f"{repo}/packages/{library_id}")

    if not library_path.is_dir():
        raise ValueError(f"Error: Path is not a directory: {library_path}")

    # Recursively glob (rglob) for all 'gapic_version.py' files
    all_gapic_files = list(library_path.rglob(gapic_version_file))

    if not all_gapic_files:
        raise ValueError(
            f"Error: namespace cannot be determined for {library_id}."
            f" Library is missing a `{gapic_version_file}`."
        )

    for gapic_file in all_gapic_files:
        # The directory we want is the parent of `gapic_version.py` file.
        gapic_parent_dir = gapic_file.parent

        # Pass both the specific dir and the package root for a safe relative comparison
        library_namespace = _determine_library_namespace(gapic_parent_dir, library_path)

        if library_namespace not in valid_namespaces:
            raise ValueError(
                f"The namespace `{library_namespace}` for `{library_id}` must be one of {valid_namespaces}."
            )


def handle_build(librarian: str = LIBRARIAN_DIR, repo: str = REPO_DIR):
    """The main coordinator for validating client library generation."""
    try:
        request_data = _read_json_file(f"{librarian}/{BUILD_REQUEST_FILE}")
        library_id = _get_library_id(request_data)
        _verify_library_namespace(library_id, repo)
        _run_nox_sessions(library_id, repo)
    except Exception as e:
        raise ValueError("Build failed.") from e

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
            library_id = library["id"]
            version = library["version"]
            # Find the entry for the given library in the format`<library_id>==<version>`
            # Replace the `<version>` part of the string.
            pattern = re.compile(f"(\\[{re.escape(library_id)})(==)([\\d\\.]+)(\\])")
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


def _get_previous_version(library_id: str, librarian: str) -> str:
    """Gets the previous version of the library from state.yaml.

    Args:
        library_id(str): id of the library.
        librarian(str): Path to the directory in the container which contains
            the `state.yaml` file.

    Returns:
        str: The version for a given library in state.yaml
    """
    state_yaml_path = f"{librarian}/{STATE_YAML_FILE}"

    with open(state_yaml_path, "r") as state_yaml_file:
        state_yaml = yaml.safe_load(state_yaml_file)
        for library in state_yaml.get("libraries", []):
            if library.get("id") == library_id:
                return library.get("version")

    raise ValueError(
        f"Could not determine previous version for {library_id} from state.yaml"
    )


def _create_main_version_header(
    version: str, previous_version: str, library_id: str
) -> str:
    """This function creates a header to be used in a changelog. The header has the following format:
    `## [{version}](https://github.com/googleapis/google-cloud-python/compare/{library_id}-v{previous_version}...{library_id}-v{version}) (YYYY-MM-DD)`

    Args:
        version(str): The new version of the library.
        previous_version(str): The previous version of the library.
        library_id(str): The id of the library where the changelog should
            be updated.

    Returns:
        A header to be used in the changelog.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    # Return the main version header
    return (
        f"## [{version}]({_REPO_URL}/compare/{library_id}-v{previous_version}"
        f"...{library_id}-v{version}) ({current_date})"
    )


def _process_changelog(
    content: str,
    library_changes: List[Dict],
    version: str,
    previous_version: str,
    library_id: str,
):
    """This function searches the given content for the anchor pattern
    `[1]: https://pypi.org/project/{library_id}/#history`
    and adds an entry in the following format:

    ## [{version}](https://github.com/googleapis/google-cloud-python/compare/{library_id}-v{previous_version}...{library_id}-v{version}) (YYYY-MM-DD)

    ### Documentation

    * Update import statement example in README ([868b006](https://github.com/googleapis/google-cloud-python/commit/868b0069baf1a4bf6705986e0b6885419b35cdcc))

    Args:
        content(str): The contents of an existing changelog.
        library_changes(List[Dict]): List of dictionaries containing the changes
            for a given library.
        version(str): The new version of the library.
        previous_version(str): The previous version of the library.
        library_id(str): The id of the library where the changelog should
            be updated.

    Raises: ValueError if the anchor pattern string could not be found in the given content

    Returns: A string with the modified content.
    """
    entry_parts = []
    entry_parts.append(
        _create_main_version_header(
            version=version, previous_version=previous_version, library_id=library_id
        )
    )

    # Group changes by type (e.g., feat, fix, docs)
    type_key = "type"
    source_commit_hash_key = "source_commit_hash"
    subject_key = "subject"
    library_changes.sort(key=lambda x: x[type_key])
    grouped_changes = itertools.groupby(library_changes, key=lambda x: x[type_key])

    change_type_map = {
        "feat": "Features",
        "fix": "Bug Fixes",
        "docs": "Documentation",
    }
    for library_change_type, library_changes in grouped_changes:
        # We only care about feat, fix, docs
        adjusted_change_type = library_change_type.replace("!", "")
        if adjusted_change_type in change_type_map:
            entry_parts.append(f"\n\n### {change_type_map[adjusted_change_type]}\n")
            for change in library_changes:
                commit_link = f"([{change[source_commit_hash_key]}]({_REPO_URL}/commit/{change[source_commit_hash_key]}))"
                entry_parts.append(f"* {change[subject_key]} {commit_link}")

    new_entry_text = "\n".join(entry_parts)
    anchor_pattern = re.compile(
        rf"(\[1\]: https://pypi\.org/project/{library_id}/#history)",
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
    library_id: str,
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
        previous_version(str): The version in state.yaml for a given library
        library_id(str): The id of the library where the changelog should
            be updated.
    """

    relative_path = f"packages/{library_id}/CHANGELOG.md"
    changelog_src = f"{repo}/{relative_path}"
    changelog_dest = f"{output}/{relative_path}"
    updated_content = _process_changelog(
        _read_text_file(changelog_src),
        library_changes,
        version,
        previous_version,
        library_id,
    )
    _write_text_file(changelog_dest, updated_content)


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

    Raises:
        ValueError: if the version in `release-init-request.json` is
            the same as the version in state.yaml or if the
            `release-init-request.json` file in the given
            librarian directory cannot be read.
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
            library_id = library_release_data["id"]
            library_changes = library_release_data["changes"]
            path_to_library = f"packages/{library_id}"

            # Get previous version from state.yaml
            previous_version = _get_previous_version(library_id, librarian)
            if previous_version == version:
                raise ValueError(
                    f"The version in {RELEASE_INIT_REQUEST_FILE} is the same as the version in {STATE_YAML_FILE}\n"
                    f"{library_id} version: {previous_version}\n"
                )

            _update_version_for_library(repo, output, path_to_library, version)
            _update_changelog_for_library(
                repo,
                output,
                library_changes,
                version,
                previous_version,
                library_id,
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
