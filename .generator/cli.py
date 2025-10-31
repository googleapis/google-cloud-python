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
import tempfile
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import build.util
import parse_googleapis_content


try:
    import synthtool
    from synthtool.languages import python, python_mono_repo

    SYNTHTOOL_INSTALLED = True
    SYNTHTOOL_IMPORT_ERROR = None
except ImportError as e:  # pragma: NO COVER
    SYNTHTOOL_IMPORT_ERROR = e
    SYNTHTOOL_INSTALLED = False

logger = logging.getLogger()

BUILD_REQUEST_FILE = "build-request.json"
GENERATE_REQUEST_FILE = "generate-request.json"
CONFIGURE_REQUEST_FILE = "configure-request.json"
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


def _add_new_library_source_roots(library_config: Dict, library_id: str) -> None:
    """Adds the default source_roots to the library configuration if not present.

    Args:
        library_config(Dict): The library configuration.
        library_id(str): The id of the library.
    """
    if library_config["source_roots"] is None:
        library_config["source_roots"] = [f"packages/{library_id}"]


def _add_new_library_preserve_regex(library_config: Dict, library_id: str) -> None:
    """Adds the default preserve_regex to the library configuration if not present.

    Args:
        library_config(Dict): The library configuration.
        library_id(str): The id of the library.
    """
    if library_config["preserve_regex"] is None:
        library_config["preserve_regex"] = [
            f"packages/{library_id}/CHANGELOG.md",
            "docs/CHANGELOG.md",
            "docs/README.rst",
            "samples/README.txt",
            "scripts/client-post-processing",
            "samples/snippets/README.rst",
            "tests/system",
        ]


def _add_new_library_remove_regex(library_config: Dict, library_id: str) -> None:
    """Adds the default remove_regex to the library configuration if not present.

    Args:
        library_config(Dict): The library configuration.
        library_id(str): The id of the library.
    """
    if library_config["remove_regex"] is None:
        library_config["remove_regex"] = [f"packages/{library_id}"]


def _add_new_library_tag_format(library_config: Dict) -> None:
    """Adds the default tag_format to the library configuration if not present.

    Args:
        library_config(Dict): The library configuration.
    """
    if "tag_format" not in library_config:
        library_config["tag_format"] = "{id}-v{version}"


def _get_new_library_config(request_data: Dict) -> Dict:
    """Finds and returns the configuration for a new library.

    Args:
        request_data(Dict): The request data from which to extract the new
        library config.

    Returns:
        Dict: The unmodified configuration of a new library, or an empty
        dictionary if not found.
    """
    for library_config in request_data.get("libraries", []):
        all_apis = library_config.get("apis", [])
        for api in all_apis:
            if api.get("status") == "new":
                return library_config
    return {}


def _add_new_library_version(library_config: Dict) -> None:
    """Adds the library version to the configuration if it's not present.

    Args:
        library_config(Dict): The library configuration.
    """
    if "version" not in library_config or not library_config["version"]:
        library_config["version"] = "0.0.0"


def _prepare_new_library_config(library_config: Dict) -> Dict:
    """
    Prepares the new library's configuration by removing temporary keys and
    adding default values.

    Args:
        library_config (Dict): The raw library configuration.

    Returns:
        Dict: The prepared library configuration.
    """
    # remove status key from new library config.
    all_apis = library_config.get("apis", [])
    for api in all_apis:
        if "status" in api:
            del api["status"]

    library_id = _get_library_id(library_config)
    _add_new_library_source_roots(library_config, library_id)
    _add_new_library_preserve_regex(library_config, library_id)
    _add_new_library_remove_regex(library_config, library_id)
    _add_new_library_tag_format(library_config)
    _add_new_library_version(library_config)

    return library_config


def _create_new_changelog_for_library(library_id: str, output: str):
    """Creates a new changelog for the library.
    Args:
        library_id(str): The id of the library.
        output(str): Path to the directory in the container where code
            should be generated.
    """
    package_changelog_path = f"{output}/packages/{library_id}/CHANGELOG.md"
    docs_changelog_path = f"{output}/packages/{library_id}/docs/CHANGELOG.md"

    changelog_content = f"# Changelog\n\n[PyPI History][1]\n\n[1]: https://pypi.org/project/{library_id}/#history\n"

    os.makedirs(os.path.dirname(package_changelog_path), exist_ok=True)
    _write_text_file(package_changelog_path, changelog_content)

    os.makedirs(os.path.dirname(docs_changelog_path), exist_ok=True)
    _write_text_file(docs_changelog_path, changelog_content)


def handle_configure(
    librarian: str = LIBRARIAN_DIR,
    source: str = SOURCE_DIR,
    repo: str = REPO_DIR,
    input: str = INPUT_DIR,
    output: str = OUTPUT_DIR,
):
    """Onboards a new library by completing its configuration.

    This function reads a partial library definition from `configure-request.json`,
    fills in missing fields like the version, source roots, and preservation
    rules, and writes the complete configuration to `configure-response.json`.
    It ensures that new libraries conform to the repository's standard structure.

    See https://github.com/googleapis/librarian/blob/main/doc/container-contract.md#configure-container-command

    Args:
        librarian(str): Path to the directory in the container which contains
            the librarian configuration.
        source(str): Path to the directory in the container which contains
            API protos.
        repo(str): This directory will contain all directories that make up a
            library, the .librarian folder, and any global file declared in
            the config.yaml.
        input(str): The path to the directory in the container
            which contains additional generator input.
        output(str): Path to the directory in the container where code
            should be generated.

    Raises:
        ValueError: If configuring a new library fails.
    """
    try:
        # configure-request.json contains the library definitions.
        request_data = _read_json_file(f"{librarian}/{CONFIGURE_REQUEST_FILE}")
        new_library_config = _get_new_library_config(request_data)

        _update_global_changelog(
            f"{repo}/CHANGELOG.md",
            f"{output}/CHANGELOG.md",
            [new_library_config],
        )
        prepared_config = _prepare_new_library_config(new_library_config)

        # Create a `CHANGELOG.md` and `docs/CHANGELOG.md` file for the new library
        library_id = _get_library_id(prepared_config)
        _create_new_changelog_for_library(library_id, output)

        # Write the new library configuration to configure-response.json.
        _write_json_file(f"{librarian}/configure-response.json", prepared_config)

    except Exception as e:
        raise ValueError("Configuring a new library failed.") from e
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


def _run_post_processor(output: str, library_id: str, is_mono_repo: bool):
    """Runs the synthtool post-processor on the output directory.

    Args:
        output(str): Path to the directory in the container where code
            should be generated.
        library_id(str): The library id to be used for post processing.
        is_mono_repo(bool): True if the current repository is a mono-repo.
    """
    os.chdir(output)
    path_to_library = f"packages/{library_id}" if is_mono_repo else "."
    logger.info("Running Python post-processor...")
    if SYNTHTOOL_INSTALLED:
        if is_mono_repo:
            python_mono_repo.owlbot_main(path_to_library)
        else:
            # Some repositories have customizations in `owlbot.py`. If this file exists,
            # run those customizations instead of `owlbot_main`
            if Path(f"{output}/owlbot.py").exists():
                subprocess.run(["python3.14", f"{output}/owlbot.py"])
            else:
                python.owlbot_main()
    else:
        raise SYNTHTOOL_IMPORT_ERROR  # pragma: NO COVER

    # If there is no noxfile, run `isort`` and `black` on the output.
    # This is required for proto-only libraries which are not GAPIC.
    if not Path(f"{output}/{path_to_library}/noxfile.py").exists():
        subprocess.run(["isort", output])
        subprocess.run(["black", output])

    logger.info("Python post-processor ran successfully.")


def _copy_files_needed_for_post_processing(
    output: str, input: str, library_id: str, is_mono_repo: bool
):
    """Copy files to the output directory whcih are needed during the post processing
    step, such as .repo-metadata.json and script/client-post-processing, using
    the input directory as the source.

    Args:
        output(str): Path to the directory in the container where code
            should be generated.
        input(str): The path to the directory in the container
            which contains additional generator input.
        library_id(str): The library id to be used for post processing.
        is_mono_repo(bool): True if the current repository is a mono-repo.
    """

    path_to_library = f"packages/{library_id}" if is_mono_repo else "."
    source_dir = f"{input}/{path_to_library}"

    if Path(source_dir).exists():
        shutil.copytree(
            source_dir,
            f"{output}/{path_to_library}",
            dirs_exist_ok=True,
        )

    # We need to create these directories so that we can copy files necessary for post-processing.
    os.makedirs(
        f"{output}/{path_to_library}/scripts/client-post-processing", exist_ok=True
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


def _clean_up_files_after_post_processing(
    output: str, library_id: str, is_mono_repo: bool
):
    """
    Clean up files which should not be included in the generated client.
    This function is idempotent and will not fail if files are already removed.

    Args:
        output(str): Path to the directory in the container where code
            should be generated.
        library_id(str): The library id to be used for post processing.
        is_mono_repo(bool): True if the current repository is a mono-repo.
    """
    path_to_library = f"packages/{library_id}" if is_mono_repo else "."

    # Safely remove directories, ignoring errors if they don't exist.
    shutil.rmtree(f"{output}/{path_to_library}/.nox", ignore_errors=True)
    shutil.rmtree(f"{output}/owl-bot-staging", ignore_errors=True)

    # Safely remove specific files if they exist using pathlib.
    Path(f"{output}/{path_to_library}/CHANGELOG.md").unlink(missing_ok=True)
    Path(f"{output}/{path_to_library}/docs/CHANGELOG.md").unlink(missing_ok=True)

    # The glob loops are already safe, as they do nothing if no files match.
    for post_processing_file in glob.glob(
        f"{output}/{path_to_library}/scripts/client-post-processing/*.yaml"
    ):  # pragma: NO COVER
        os.remove(post_processing_file)


def _determine_release_level(api_path: str) -> str:
    # TODO(https://github.com/googleapis/librarian/issues/2352): Determine if
    # this logic can be used to set the release level.
    # For now, we set the release_level as "preview" for newly generated clients.
    """Determines the release level from the API path.

    Args:
        api_path (str): The path to the API.

    Returns:
        str: The release level, which can be 'preview' or 'stable'.
    """
    version = Path(api_path).name
    if "beta" in version or "alpha" in version:
        return "preview"
    return "stable"


def _create_repo_metadata_from_service_config(
    service_config_name: str, api_path: str, source: str, library_id: str
) -> Dict:
    """Creates the .repo-metadata.json content from the service config.

    Args:
        service_config_name (str): The name of the service config file.
        api_path (str): The path to the API.
        source (str): The path to the source directory.
        library_id (str): The ID of the library.

    Returns:
        Dict: The content of the .repo-metadata.json file.
    """
    full_service_config_path = f"{source}/{api_path}/{service_config_name}"
    with open(full_service_config_path, "r") as f:
        service_config = yaml.safe_load(f)

    api_id = service_config.get("name", {})
    publishing = service_config.get("publishing", {})
    name_pretty = service_config.get("title", "")
    product_documentation = publishing.get("documentation_uri", "")
    api_shortname = service_config.get("name", "").split(".")[0]
    documentation = service_config.get("documentation", {})
    api_description = documentation.get("summary", "")
    issue_tracker = publishing.get(
        "new_issue_uri", "https://github.com/googleapis/google-cloud-python/issues"
    )

    # TODO(https://github.com/googleapis/librarian/issues/2352): Determine if
    # `_determine_release_level` can be used to
    # set the release level. For now, we set the release_level as "preview" for
    # newly generated clients.
    release_level = "preview"

    return {
        "name": library_id,
        "name_pretty": name_pretty,
        "api_description": api_description,
        "product_documentation": product_documentation,
        "client_documentation": f"https://cloud.google.com/python/docs/reference/{library_id}/latest",
        "issue_tracker": issue_tracker,
        "release_level": release_level,
        "language": "python",
        "library_type": "GAPIC_AUTO",
        "repo": "googleapis/google-cloud-python",
        "distribution_name": library_id,
        "api_id": api_id,
        # TODO(https://github.com/googleapis/librarian/issues/2369):
        # Remove the dependency on `default_version` for Python post processor.
        "default_version": Path(api_path).name,
        "api_shortname": api_shortname,
    }


def _generate_repo_metadata_file(
    output: str, library_id: str, source: str, apis: List[Dict], is_mono_repo: bool
):
    """Generates the .repo-metadata.json file from the primary API service config.

    Args:
        output (str): The path to the output directory.
        library_id (str): The ID of the library.
        source (str): The path to the source directory.
        apis (List[Dict]): A list of APIs to generate.
        is_mono_repo(bool): True if the current repository is a mono-repo.
    """
    path_to_library = f"packages/{library_id}" if is_mono_repo else "."
    output_repo_metadata = f"{output}/{path_to_library}/.repo-metadata.json"

    # TODO(https://github.com/googleapis/librarian/issues/2334)): If `.repo-metadata.json`
    # already exists in the `output` dir, then this means that it has been successfully copied
    # over from the `input` dir and we can skip the logic here. Remove the following logic
    # once we clean up all the `.repo-metadata.json` files from `.librarian/generator-input`.
    if os.path.exists(output_repo_metadata):
        return

    os.makedirs(f"{output}/{path_to_library}", exist_ok=True)

    # TODO(https://github.com/googleapis/librarian/issues/2333): Programatically
    # determine the primary api to be used to
    # to determine the information for metadata. For now, let's use the first
    # api in the list.
    primary_api = apis[0]

    metadata_content = _create_repo_metadata_from_service_config(
        primary_api.get("service_config"),
        primary_api.get("path"),
        source,
        library_id,
    )
    _write_json_file(output_repo_metadata, metadata_content)


def _copy_readme_to_docs(output: str, library_id: str, is_mono_repo: bool):
    """Copies the README.rst file for a generated library to docs/README.rst.

    This function is robust against various symlink configurations that could
    cause `shutil.copy` to fail with a `SameFileError`. It reads the content
    from the source and writes it to the destination, ensuring the final
    destination is a real file.

    Args:
        output(str): Path to the directory in the container where code
            should be generated.
        library_id(str): The library id.
    """
    path_to_library = f"packages/{library_id}" if is_mono_repo else "."
    source_path = f"{output}/{path_to_library}/README.rst"
    docs_path = f"{output}/{path_to_library}/docs"
    destination_path = f"{docs_path}/README.rst"

    # If the source file doesn't exist (not even as a broken symlink),
    # there's nothing to copy.
    if not os.path.lexists(source_path):
        return

    # Read the content from the source, which will resolve any symlinks.
    with open(source_path, "r") as f:
        content = f.read()

    # Remove any symlinks at the destination to prevent errors.
    if os.path.islink(destination_path):
        os.remove(destination_path)
    elif os.path.islink(docs_path):
        os.remove(docs_path)

    # Ensure the destination directory exists as a real directory.
    os.makedirs(docs_path, exist_ok=True)

    # Write the content to the destination, creating a new physical file.
    with open(destination_path, "w") as f:
        f.write(content)


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
        is_mono_repo = _is_mono_repo(input)
        # Read a generate-request.json file
        request_data = _read_json_file(f"{librarian}/{GENERATE_REQUEST_FILE}")
        library_id = _get_library_id(request_data)
        apis_to_generate = request_data.get("apis", [])
        version = request_data.get("version")
        for api in apis_to_generate:
            api_path = api.get("path")
            if api_path:
                _generate_api(
                    api_path, library_id, source, output, version, is_mono_repo
                )
        _copy_files_needed_for_post_processing(output, input, library_id, is_mono_repo)
        _generate_repo_metadata_file(
            output, library_id, source, apis_to_generate, is_mono_repo
        )
        _run_post_processor(output, library_id, is_mono_repo)
        _copy_readme_to_docs(output, library_id, is_mono_repo)
        _clean_up_files_after_post_processing(output, library_id, is_mono_repo)
    except Exception as e:
        raise ValueError("Generation failed.") from e
    logger.info("'generate' command executed.")


def _read_bazel_build_py_rule(api_path: str, source: str) -> Dict:
    """
    Reads and parses the BUILD.bazel file to find the Python GAPIC rule content.

    Args:
        api_path (str): The relative path to the API directory (e.g., 'google/cloud/language/v1').
        source (str): Path to the directory containing API protos.

    Returns:
        Dict: A dictionary containing the parsed attributes of the `_py_gapic` rule, if found.
    """
    build_file_path = f"{source}/{api_path}/BUILD.bazel"
    content = _read_text_file(build_file_path)

    result = parse_googleapis_content.parse_content(content)
    py_gapic_entries = [key for key in result.keys() if key.endswith("_py_gapic")]

    # Assuming at most one _py_gapic rule per BUILD file for a given language
    if len(py_gapic_entries) > 0:
        return result[py_gapic_entries[0]]
    else:
        return {}


def _get_api_generator_options(
    api_path: str, py_gapic_config: Dict, gapic_version: str
) -> List[str]:
    """
    Extracts generator options from the parsed Python GAPIC rule configuration.

    Args:
        api_path (str): The relative path to the API directory.
        py_gapic_config (Dict): The parsed attributes of the Python GAPIC rule.
        gapic_version(str): The desired version number for the GAPIC client library
            in a format which follows PEP-440.

    Returns:
        List[str]: A list of formatted generator options (e.g., ['retry-config=...', 'transport=...']).
    """
    generator_options = []

    # Mapping of Bazel rule attributes to protoc-gen-python_gapic options
    config_key_map = {
        "grpc_service_config": "retry-config",
        "rest_numeric_enums": "rest-numeric-enums",
        "service_yaml": "service-yaml",
        "transport": "transport",
    }

    for bazel_key, protoc_key in config_key_map.items():
        config_value = py_gapic_config.get(bazel_key)
        if config_value is not None:
            if bazel_key in ("service_yaml", "grpc_service_config"):
                # These paths are relative to the source root
                generator_options.append(f"{protoc_key}={api_path}/{config_value}")
            else:
                # Other options use the value directly
                generator_options.append(f"{protoc_key}={config_value}")

    # The value of `opt_args` in the `py_gapic` bazel rule is already a list of strings.
    optional_arguments = py_gapic_config.get("opt_args", [])
    # Specify `gapic-version` using the version from `state.yaml`
    optional_arguments.extend([f"gapic-version={gapic_version}"])
    # Add optional arguments
    generator_options.extend(optional_arguments)

    return generator_options


def _construct_protoc_command(api_path: str, tmp_dir: str) -> str:
    """
    Constructs the full protoc command string.

    Args:
        api_path (str): The relative path to the API directory.
        tmp_dir (str): The temporary directory for protoc output.

    Returns:
        str: The complete protoc command string suitable for shell execution.
    """
    command_parts = [
        f"protoc {api_path}/*.proto",
        f"--python_out={tmp_dir}",
        f"--pyi_out={tmp_dir}",
    ]

    return " ".join(command_parts)


def _determine_generator_command(
    api_path: str, tmp_dir: str, generator_options: List[str]
) -> str:
    """
    Constructs the full protoc command string.

    Args:
        api_path (str): The relative path to the API directory.
        tmp_dir (str): The temporary directory for protoc output.
        generator_options (List[str]): Extracted generator options.

    Returns:
        str: The complete protoc command string suitable for shell execution.
    """
    # Start with the protoc base command. The glob pattern requires shell=True.
    command_parts = [
        f"protoc {api_path}/*.proto",
        f"--python_gapic_out={tmp_dir}",
    ]

    if generator_options:
        # Protoc options are passed as a comma-separated list to --python_gapic_opt.
        option_string = "metadata," + ",".join(generator_options)
        command_parts.append(f"--python_gapic_opt={option_string}")

    return " ".join(command_parts)


def _run_protoc_command(generator_command: str, source: str):
    """
    Executes the protoc generation command using subprocess.

    Args:
        generator_command (str): The complete protoc command string.
        source (str): Path to the directory where the command should be run (API protos root).
    """
    # shell=True is required because the command string contains a glob pattern (*.proto)
    subprocess.run(
        [generator_command],
        cwd=source,
        shell=True,
        check=True,
        capture_output=True,
        text=True,
    )


def _get_staging_child_directory(api_path: str, is_proto_only_library: bool) -> str:
    """
    Determines the correct sub-path within 'owl-bot-staging' for the generated code.

    For proto-only libraries, the structure is usually just the proto directory,
    e.g., 'thing-py/google/thing'.
    For GAPIC libraries, it's typically the version segment, e.g., 'v1'.

    Args:
        api_path (str): The relative path to the API directory (e.g., 'google/cloud/language/v1').
        is_proto_only_library(bool): True, if this is a proto-only library.

    Returns:
        str: The sub-directory name to use for staging.
    """

    version_candidate = api_path.split("/")[-1]
    if version_candidate.startswith("v") and not is_proto_only_library:
        return version_candidate
    elif is_proto_only_library:
        # Fallback for non-'v' version segment for proto-only library
        return f"{os.path.basename(api_path)}-py/{api_path}"
    else:
        # Fallback for non-'v' version segment for GAPIC
        return f"{os.path.basename(api_path)}-py"


def _stage_proto_only_library(
    api_path: str, source_dir: str, tmp_dir: str, staging_dir: str
) -> None:
    """
    Handles staging for proto-only libraries (e.g., common protos).

    This involves copying the generated python files and the original proto files.

    Args:
        api_path (str): The relative path to the API directory.
        source_dir (str): Path to the directory containing API protos.
        tmp_dir (str): The temporary directory where protoc output was placed.
        staging_dir (str): The final destination for the staged code.
    """
    # 1. Copy the generated Python files (e.g., *_pb2.py) from the protoc output
    # The generated Python files are placed under a directory corresponding to `api_path`
    # inside the temporary directory, since the protoc command ran with `api_path`
    # specified.
    shutil.copytree(f"{tmp_dir}/{api_path}", staging_dir, dirs_exist_ok=True)

    # 2. Copy the original proto files to the staging directory
    # This is typically done for proto-only libraries so that the protos are included
    # in the distributed package.
    proto_glob_path = f"{source_dir}/{api_path}/*.proto"
    for proto_file in glob.glob(proto_glob_path):
        # The glob is expected to find the file inside the source_dir.
        # We copy only the filename to the target staging directory.
        shutil.copyfile(proto_file, f"{staging_dir}/{os.path.basename(proto_file)}")


def _stage_gapic_library(tmp_dir: str, staging_dir: str) -> None:
    """
    Handles staging for GAPIC client libraries.

    This involves copying all contents from the temporary output directory.

    Args:
        tmp_dir (str): The temporary directory where protoc/GAPIC generator output was placed.
        staging_dir (str): The final destination for the staged code.
    """
    # For GAPIC, the generator output is flat in `tmp_dir` and includes all
    # necessary files like setup.py, client library, etc.
    shutil.copytree(tmp_dir, staging_dir, dirs_exist_ok=True)


def _generate_api(
    api_path: str,
    library_id: str,
    source: str,
    output: str,
    gapic_version: str,
    is_mono_repo: bool,
):
    """
    Handles the generation and staging process for a single API path.

    Args:
        api_path (str): The relative path to the API directory (e.g., 'google/cloud/language/v1').
        library_id (str): The ID of the library being generated.
        source (str): Path to the directory containing API protos.
        output (str): Path to the output directory where code should be staged.
        gapic_version(str): The desired version number for the GAPIC client library
            in a format which follows PEP-440.
        is_mono_repo(bool): True if the current repository is a mono-repo.
    """
    py_gapic_config = _read_bazel_build_py_rule(api_path, source)
    is_proto_only_library = len(py_gapic_config) == 0

    with tempfile.TemporaryDirectory() as tmp_dir:
        # 1. Determine the command for code generation
        if is_proto_only_library:
            command = _construct_protoc_command(api_path, tmp_dir)
        else:
            generator_options = _get_api_generator_options(
                api_path, py_gapic_config, gapic_version=gapic_version
            )
            command = _determine_generator_command(api_path, tmp_dir, generator_options)

        # 2. Execute the code generation command
        _run_protoc_command(command, source)

        # 3. Determine staging location
        staging_child_directory = _get_staging_child_directory(
            api_path, is_proto_only_library
        )
        staging_dir = os.path.join(output, "owl-bot-staging")
        if is_mono_repo:
            staging_dir = os.path.join(staging_dir, library_id)
        staging_dir = os.path.join(staging_dir, staging_child_directory)

        # 4. Stage the generated code
        if is_proto_only_library:
            _stage_proto_only_library(api_path, source, tmp_dir, staging_dir)
        else:
            _stage_gapic_library(tmp_dir, staging_dir)


def _run_nox_sessions(library_id: str, repo: str):
    """Calls nox for all specified sessions.

    Args:
        library_id(str): The library id under test.
        repo(str): This directory will contain all directories that make up a
            library, the .librarian folder, and any global files declared in
            the config.yaml.
    """
    sessions = [
        "unit-3.14(protobuf_implementation='upb')",
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
    the hardcoded `exception_namespaces` or
    `valid_namespaces`.

    Args:
        library_id (str): The library id under test (e.g., "google-cloud-language").
        repo (str): The path to the root of the repository.
    """
    # TODO(https://github.com/googleapis/google-cloud-python/issues/14376): Update the list of namespaces which are exceptions.
    exception_namespaces = [
        "google.area120",
        "google.api",
        "google.apps.script",
        "google.apps.script.type",
        "google.cloud.alloydb",
        "google.cloud.billing",
        "google.cloud.devtools",
        "google.cloud.gkeconnect",
        "google.cloud.gkehub_v1",
        "google.cloud.orchestration.airflow",
        "google.cloud.orgpolicy",
        "google.cloud.security",
        "google.cloud.video",
        "google.cloud.workflows",
        "google.iam",
        "google.gapic",
        "google.identity.accesscontextmanager",
        "google.logging",
        "google.monitoring",
        "google.rpc",
    ]
    valid_namespaces = [
        "google",
        "google.ads",
        "google.ai",
        "google.analytics",
        "google.apps",
        "google.cloud",
        "google.geo",
        "google.maps",
        "google.shopping",
        "grafeas",
        *exception_namespaces,
    ]
    gapic_version_file = "gapic_version.py"
    proto_file = "*.proto"

    library_path = Path(f"{repo}/packages/{library_id}")

    if not library_path.is_dir():
        raise ValueError(f"Error: Path is not a directory: {library_path}")

    # Use a set to store unique parent directories of relevant directories
    relevant_dirs = set()

    # Find all parent directories for 'gapic_version.py' files
    for gapic_file in library_path.rglob(gapic_version_file):
        relevant_dirs.add(gapic_file.parent)

    # Find all parent directories for '*.proto' files
    for proto_file in library_path.rglob(proto_file):
        relevant_dirs.add(proto_file.parent)

    if not relevant_dirs:
        raise ValueError(
            f"Error: namespace cannot be determined for {library_id}."
            f" Library is missing a `{gapic_version_file}` or `{proto_file}` file."
        )

    for relevant_dir in relevant_dirs:
        library_namespace = _determine_library_namespace(relevant_dir, library_path)

        if library_namespace not in valid_namespaces:
            raise ValueError(
                f"The namespace `{library_namespace}` for `{library_id}` must be one of {valid_namespaces}."
            )


def _get_library_dist_name(library_id: str, repo: str) -> str:
    """
    Gets the package name by programmatically building the metadata.

    Args:
        library_id: id of the library.
        repo: This directory will contain all directories that make up a
            library, the .librarian folder, and any global file declared in
            the config.yaml.

    Returns:
        str: The library name string if found, otherwise None.
    """
    library_path = f"{repo}/packages/{library_id}"
    metadata = build.util.project_wheel_metadata(library_path)
    return metadata.get("name")


def _verify_library_dist_name(library_id: str, repo: str):
    """Verifies the library distribution name against its config files.

    This function ensures that:
    1. At least one of `setup.py` or `pyproject.toml` exists and is valid.
    2. Any existing config file's 'name' property matches the `library_id`.

    Args:
        library_id: id of the library.
        repo: This directory will contain all directories that make up a
            library, the .librarian folder, and any global file declared in
            the config.yaml.

    Raises:
        ValueError: If a name in an existing config file does not match the `library_id`.
    """
    dist_name = _get_library_dist_name(library_id, repo)
    if dist_name != library_id:
        raise ValueError(
            f"The distribution name `{dist_name}` does not match the folder `{library_id}`."
        )


def handle_build(librarian: str = LIBRARIAN_DIR, repo: str = REPO_DIR):
    """The main coordinator for validating client library generation."""
    try:
        request_data = _read_json_file(f"{librarian}/{BUILD_REQUEST_FILE}")
        library_id = _get_library_id(request_data)
        _verify_library_namespace(library_id, repo)
        _verify_library_dist_name(library_id, repo)
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
    if version_path.name.endswith("gapic_version.py") or version_path.name.endswith(
        "version.py"
    ):
        pattern = r"(__version__\s*=\s*[\"'])([^\"']+)([\"'].*)"
    else:
        pattern = r"(version\s*=\s*[\"'])([^\"']+)([\"'].*)"
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
    """Updates the version string in `**/gapic_version.py`, `**/version.py`, `setup.py`,
        `pyproject.toml` and `samples/**/snippet_metadata.json` for a
        given library, if applicable.

    Args:
        repo(str): This directory will contain all directories that make up a
            library, the .librarian folder, and any global file declared in
            the config.yaml.
        output(str): Path to the directory in the container where modified
            code should be placed.
        path_to_library(str): Relative path to the library to update
        version(str): The new version of the library

    Raises: `ValueError` if a version string could not be located in `**/gapic_version.py`
        or `**/version.py` within the given library.
    """

    # Find and update version.py or gapic_version.py files
    search_base = Path(f"{repo}/{path_to_library}")
    version_files = list(search_base.rglob("**/gapic_version.py"))
    excluded_dirs = {
        ".nox",
        ".venv",
        "venv",
        "site-packages",
        ".git",
        "build",
        "dist",
        "__pycache__",
    }
    version_files.extend(
        [
            p
            for p in search_base.rglob("**/version.py")
            if not any(part in excluded_dirs for part in p.parts)
        ]
    )

    if not version_files:
        # Fallback to `pyproject.toml`` or `setup.py``. Proto-only libraries have
        # version information in `setup.py` or `pyproject.toml` instead of `gapic_version.py`.
        pyproject_toml = Path(f"{repo}/{path_to_library}/pyproject.toml")
        setup_py = Path(f"{repo}/{path_to_library}/setup.py")
        version_files = [pyproject_toml if pyproject_toml.exists() else setup_py]

    for version_file in version_files:
        # Do not process version files in the types directory as some
        # GAPIC libraries have `version.py` which are generated from
        # `version.proto` and do not include SDK versions.
        if version_file.parent.name == "types":
            continue
        updated_content = _process_version_file(
            _read_text_file(version_file), version, version_file
        )
        output_path = f"{output}/{version_file.relative_to(repo)}"
        _write_text_file(output_path, updated_content)

    # Find and update snippet_metadata.json files
    snippet_metadata_files = Path(f"{repo}/{path_to_library}").rglob(
        "samples/**/*snippet*.json"
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
    commit_hash_key = "commit_hash"
    subject_key = "subject"
    body_key = "body"
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
                commit_link = f"([{change[commit_hash_key]}]({_REPO_URL}/commit/{change[commit_hash_key]}))"
                entry_parts.append(
                    f"* {change[subject_key]} {change[body_key]} {commit_link}"
                )

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
    is_mono_repo: bool,
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
        is_mono_repo(bool): True if the current repository is a mono-repo.
    """
    if is_mono_repo:
        relative_path = f"packages/{library_id}/CHANGELOG.md"
        docs_relative_path = f"packages/{library_id}/docs/CHANGELOG.md"
    else:
        relative_path = "CHANGELOG.md"
        docs_relative_path = f"docs/CHANGELOG.md"

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

    docs_changelog_src = f"{repo}/{docs_relative_path}"
    if os.path.lexists(docs_changelog_src):
        docs_changelog_dst = f"{output}/{docs_relative_path}"
        _write_text_file(docs_changelog_dst, updated_content)


def _is_mono_repo(repo: str) -> bool:
    """Determines if a library is generated or handwritten.

    Args:
        repo(str): This directory will contain all directories that make up a
            library, the .librarian folder, and any global file declared in
            the config.yaml.

    Returns: True if the library is generated, False otherwise.
    """
    return Path(f"{repo}/packages").exists()


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
        is_mono_repo = _is_mono_repo(repo)

        # Read a release-init-request.json file
        request_data = _read_json_file(f"{librarian}/{RELEASE_INIT_REQUEST_FILE}")
        libraries_to_prep_for_release = _get_libraries_to_prepare_for_release(
            request_data
        )

        if is_mono_repo:
            # only a mono repo has a global changelog
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

            # Get previous version from state.yaml
            previous_version = _get_previous_version(library_id, librarian)
            if previous_version == version:
                raise ValueError(
                    f"The version in {RELEASE_INIT_REQUEST_FILE} is the same as the version in {STATE_YAML_FILE}\n"
                    f"{library_id} version: {previous_version}\n"
                )

            path_to_library = f"packages/{library_id}" if is_mono_repo else "."

            _update_version_for_library(repo, output, path_to_library, version)
            _update_changelog_for_library(
                repo,
                output,
                library_changes,
                version,
                previous_version,
                library_id,
                is_mono_repo=is_mono_repo,
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
    if args.command == "configure":
        args.func(
            librarian=args.librarian,
            source=args.source,
            repo=args.repo,
            input=args.input,
            output=args.output,
        )
    elif args.command == "generate":
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
