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
import json
import logging
import os
import subprocess
import sys
import subprocess
import shutil
import glob

from typing import Dict, List

try:
    import synthtool
    from synthtool import gcp

    SYNTHTOOL_INSTALLED = True
    SYNTHTOOL_IMPORT_ERROR = None
except ImportError as e:
    SYNTHTOOL_IMPORT_ERROR = e
    SYNTHTOOL_INSTALLED = False

logger = logging.getLogger()

LIBRARIAN_DIR = "librarian"
GENERATE_REQUEST_FILE = "generate-request.json"
SOURCE_DIR = "/source"
OUTPUT_DIR = "output"
REPO_DIR = "repo"

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
    print(f"{input}/{path_to_library}/.repo-metadata.json")
    print(f"{output}/{path_to_library}/.repo-metadata.json")

    shutil.move(
        f"{input}/{path_to_library}/.repo-metadata.json",
        f"{output}/{path_to_library}/.repo-metadata.json",
    )
    # copy post-procesing files
    for post_processing_file in glob.glob(f"{input}/client-post-processing/*.yaml"):
        with open(post_processing_file, "r") as post_processing:
            if f"{path_to_library}/" in post_processing.read():
                shutil.move(
                    post_processing_file,
                    f"{output}/{path_to_library}/scripts/client-post-processing",
                )

def _read_json_file(path: str) -> Dict:
    """Helper function that reads a json file path and returns the loaded json content.

    Args:
        path (str): The file path to read.

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


import os
import re
import logging

# Assume logger and SOURCE_DIR are defined
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# SOURCE_DIR = "."

def _determine_bazel_rule(api_path: str) -> str:
    """Finds a Bazel rule by parsing the BUILD.bazel file directly.

    Args:
        api_path (str): The API path, e.g., 'google/cloud/language/v1'.

    Returns:
        str: The discovered Bazel rule, e.g., '//google/cloud/language/v1:language-v1-py'.

    Raises:
        ValueError: If the file can't be processed or no matching rule is found.
    """
    logger.info(f"Determining Bazel rule for api_path: '{api_path}' by parsing file.")
    try:
        build_file_path = os.path.join(
            SOURCE_DIR, api_path, "BUILD.bazel"
        )
        
        with open(build_file_path, "r") as f:
            content = f.read()

        match = re.search(r'name\s*=\s*"([^"]+-py)"', content)

        # This check is for a logical failure (no match), not a runtime exception.
        # It's good to keep it for clear error messaging.
        if not match:
            raise ValueError(
                f"No Bazel rule with a name ending in '-py' found in {build_file_path}"
            )

        rule_name = match.group(1)
        bazel_rule = f"//{api_path}:{rule_name}"

        logger.info(f"Found Bazel rule: {bazel_rule}")
        return bazel_rule
        
    except Exception as e:

        raise ValueError(f"Failed to determine Bazel rule for '{api_path}' by parsing.") from e


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
        raise ValueError(f"Request file is missing required 'id' field. {request_data}")
    return library_id


def _build_bazel_target(bazel_rule: str, source: str = SOURCE_DIR):
    """Executes `bazelisk build` on a given Bazel rule.

    Args:
        bazel_rule (str): The Bazel rule to build.
        source (str): The path to the root of the Bazel workspace.

    Raises:
        ValueError: If the subprocess call fails.
    """
    logger.info(f"Executing build for rule: {bazel_rule}")
    try:
        command = ["bazelisk",  "--output_base=/bazel_cache/_bazel_ubuntu/output_base", "build", "--disk_cache=/bazel_cache/_bazel_ubuntu/cache/repos", "--incompatible_strict_action_env", bazel_rule]
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
    output: str,
    api_path: str,
    source: str = SOURCE_DIR,
):
    """Finds and extracts the tarball artifact from a Bazel build.

    Args:
        bazel_rule (str): The Bazel rule that was built.
        library_id (str): The ID of the library being generated.
        source (str): The path to the root of the Bazel workspace.
        output (str): The path to the location where generated output
            should be stored.

    Raises:
        ValueError: If failed to locate or extract artifact.
    """
    try:
        # 1. Find the bazel-bin output directory.
        logger.info("Locating Bazel output directory...")
        info_command = ["bazelisk", "--output_base=/bazel_cache/_bazel_ubuntu/output_base", "info", "bazel-bin"]
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
            extract_command, cwd=staging_dir, text=True, check=True
        )
        logger.info(f"Artifact {tarball_path} extracted successfully.")

    except Exception as e:
        raise ValueError(
            f"Failed to locate or extract artifact for {bazel_rule} rule"
        ) from e


def _run_post_processor(output_path: str = OUTPUT_DIR):
    """Runs the synthtool post-processor on the output directory.

    Args:
        output_path(str): path to the output directory
    """
    logger.info("Running Python post-processor...")
    if SYNTHTOOL_INSTALLED:
        command = ["python3.9", "-m", "synthtool.languages.python_mono_repo"]
        subprocess.run(command, cwd=output_path, text=True, check=True)
    else:
        raise SYNTHTOOL_IMPORT_ERROR
    logger.info("Python post-processor ran successfully.")


def handle_generate(
    librarian: str = LIBRARIAN_DIR, source: str = SOURCE_DIR, output: str = OUTPUT_DIR
):
    """The main coordinator for the code generation process.

    This function orchestrates the generation of a client library by reading a
    `librarian/generate-request.json` file, determining the necessary Bazel rule for each API, and
    (in future steps) executing the build.

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
                bazel_rule = _determine_bazel_rule(api_path)
                _build_bazel_target(bazel_rule, source)
                print("succesfully built bazel target.")
                _locate_and_extract_artifact(bazel_rule, library_id, output, source)
                print("succesfully located and extracted bazel tarball.")
            _run_post_processor(output)
            _copy_files_needed_for_post_processing(output, input, library_id)
            print("succesfully ran Python Post Processor.")

    except Exception as e:
        raise ValueError("Generation failed.") from e

    # TODO(https://github.com/googleapis/librarian/issues/448): Implement generate command and update docstring.
    logger.info("'generate' command executed.")


def _run_nox_sessions(sessions: List[str], librarian_path: str = LIBRARIAN_DIR):
    """Calls nox for all specified sessions.

    Args:
        path(List[str]): The list of nox sessions to run.
        librarian_path(str): The path to the librarian build configuration directory
    """
    # Read a build-request.json file
    current_session = None
    try:
        request_data = _read_json_file(f"{librarian_path}/{BUILD_REQUEST_FILE}")
        library_id = _get_library_id(request_data)
        for nox_session in sessions:
            _run_individual_session(nox_session, library_id)
    except Exception as e:
        raise ValueError(f"Failed to run the nox session: {current_session}") from e


def _run_individual_session(nox_session: str, library_id: str):
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
        f"{REPO_DIR}/packages/{library_id}",
    ]
    result = subprocess.run(command, text=True, check=True)
    logger.info(result)


def handle_build(librarian: str = LIBRARIAN_DIR):
    """The main coordinator for validating client library generation."""
    sessions = [
        "unit-3.9",
        "unit-3.10",
        "unit-3.11",
        "unit-3.12",
        "unit-3.13",
        "docs",
        "system",
        "lint",
        "lint_setup_py",
        "mypy",
        "check_lower_bounds",
    ]
    _run_nox_sessions(sessions, librarian)

    logger.info("'build' command executed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple CLI tool.")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # Define commands
    handler_map = {
        "configure": handle_configure,
        "generate": handle_generate,
        "build": handle_build,
    }

    for command_name, help_text in [
        ("configure", "Onboard a new library or an api path to Librarian workflow."),
        ("generate", "generate a python client for an API."),
        ("build", "Run unit tests via nox for the generated library."),
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
            default="/input",
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

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Pass specific arguments to the handler functions for generate/build
    if args.command == "generate":
        args.func(
            librarian=args.librarian, source=args.source, output=args.output
        )
    elif args.command == "build":
        args.func(librarian=args.librarian)
    else:
        args.func()