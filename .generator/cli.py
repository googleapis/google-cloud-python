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
import subprocess
import sys
import subprocess
from typing import Dict, List

logger = logging.getLogger()

LIBRARIAN_DIR = "librarian"
GENERATE_REQUEST_FILE = "generate-request.json"
SOURCE_DIR = "source"


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


def _determine_bazel_rule(api_path: str) -> str:
    """Executes a `bazelisk query` to find a Bazel rule.

    Args:
        api_path (str): The API path to query for.

    Returns:
        str: The discovered Bazel rule.

    Raises:
        Exception: If the subprocess call fails or returns an empty result.
    """
    logger.info(f"Determining Bazel rule for api_path: '{api_path}'")
    try:
        query = f'filter("-py$", kind("rule", //{api_path}/...:*))'
        command = ["bazelisk", "query", query]
        result = subprocess.run(
            command,
            cwd=f"{SOURCE_DIR}/googleapis",
            capture_output=True,
            text=True,
            check=True,
        )
        bazel_rule = result.stdout.strip()
        if not bazel_rule:
            raise ValueError(f"Bazelisk query `{query}` returned an empty bazel rule.")

        logger.info(f"Found Bazel rule: {bazel_rule}")
        return bazel_rule
    except Exception as e:
        raise ValueError(f"Bazelisk query `{query}` failed") from e
    
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

def handle_generate():
    """The main coordinator for the code generation process.

    This function orchestrates the generation of a client library by reading a
    `librarian/generate-request.json` file, determining the necessary Bazel rule for each API, and
    (in future steps) executing the build.

    Raises:
        ValueError: If the `generate-request.json` file is not found or read.
    """

    # Read a generate-request.json file
    try:
        request_data = _read_json_file(f"{LIBRARIAN_DIR}/{GENERATE_REQUEST_FILE}")
        library_id = _get_library_id(request_data)

        for api in request_data.get("apis", []):
            api_path = api.get("path")
            if api_path:
                bazel_rule = _determine_bazel_rule(api_path)

            logger.info(json.dumps(request_data, indent=2))
    except Exception as e:
        raise ValueError("Generation failed.") from e

    # TODO(https://github.com/googleapis/librarian/issues/448): Implement generate command and update docstring.
    logger.info("'generate' command executed.")


def _run_nox_sessions(sessions: List[str]):
    """Calls nox with the specified sessions.

    Args:
        path (List[str]): The list of nox sessions to run.
    """
    # Read a generate-request.json file
    current_session = None
    try:
        request_data = _read_json_file(f"{LIBRARIAN_DIR}/{GENERATE_REQUEST_FILE}")
        library_id = _get_library_id(request_data)
        for nox_session in sessions:
            current_session = nox_session
            command = [
                "nox",
                "-s",
                current_session,
                "-f",
                f"{SOURCE_DIR}/packages/{library_id}",
            ]
            result = subprocess.run(command, text=True, check=True)
            logger.info(result)
    except Exception as e:
        raise ValueError(f"Failed to run the nox session: {current_session}") from e


def handle_build():
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
    _run_nox_sessions(sessions)

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

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func()
