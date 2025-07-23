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
import sys
import subprocess

logger = logging.getLogger()

LIBRARIAN_DIR = "librarian"
GENERATE_REQUEST_FILE = "generate-request.json"
SOURCE_DIR = "source"


def _read_json_file(path):
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


def _determine_bazel_rule(api_path):
    """Executes a `bazelisk query` to find a Bazel rule.

    Args:
        api_path (str): The API path to query for.

    Returns:
        str: The discovered Bazel rule.

    Raises:
        ValueError: If the subprocess call fails or returns an empty result.
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


def _build_bazel_target(bazel_rule):
    """Executes `bazelisk build` on a given Bazel rule.

    Args:
        bazel_rule (str): The Bazel rule to build.

    Raises:
        ValueError: If the subprocess call fails.
    """
    logger.info(f"Executing build for rule: {bazel_rule}")
    try:
        command = ["bazelisk", "build", bazel_rule]
        subprocess.run(
            command,
            cwd=f"{SOURCE_DIR}/googleapis",
            capture_output=True,
            text=True,
            check=True,
        )
        logger.info(f"Bazel build for {bazel_rule} rule completed successfully.")
    except Exception as e:
        raise ValueError(f"Bazel build for {bazel_rule} rule failed.") from e


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
        library_id = request_data.get("id")
        if not library_id:
            raise ValueError("Request file is missing required 'id' field.")

        for api in request_data.get("apis", []):
            api_path = api.get("path")
            if api_path:
                bazel_rule = _determine_bazel_rule(api_path)
                _build_bazel_target(bazel_rule)

            logger.info(json.dumps(request_data, indent=2))
    except Exception as e:
        raise ValueError("Generation failed.") from e

    # TODO(https://github.com/googleapis/librarian/issues/448): Implement generate command and update docstring.
    logger.info("'generate' command executed.")


def handle_build():
    # TODO(https://github.com/googleapis/librarian/issues/450): Implement build command and update docstring.
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
