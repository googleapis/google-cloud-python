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

logger = logging.getLogger()

LIBRARIAN_DIR = "librarian"
GENERATE_REQUEST_FILE = "generate-request.json"


# Helper function that reads a json file path and returns the loaded json content.
def _read_json_file(path):
    with open(path, "r") as f:
        return json.load(f)


def handle_configure(dry_run=False):
    # TODO(https://github.com/googleapis/librarian/issues/466): Implement configure command.
    logger.info("'configure' command executed.")


def handle_generate(dry_run=False):

    # Read a generate-request.json file
    if not dry_run:
        try:
            request_data = _read_json_file(f"{LIBRARIAN_DIR}/{GENERATE_REQUEST_FILE}")
        except Exception as e:
            logger.error(f"failed to read {LIBRARIAN_DIR}/{GENERATE_REQUEST_FILE}: {e}")
            sys.exit(1)

        logger.info(json.dumps(request_data, indent=2))

    # TODO(https://github.com/googleapis/librarian/issues/448): Implement generate command.
    logger.info("'generate' command executed.")


def handle_build(dry_run=False):
    # TODO(https://github.com/googleapis/librarian/issues/450): Implement build command.
    logger.info("'build' command executed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple CLI tool.")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # This flag is needed for testing.
    parser.add_argument(
        "--dry-run", action="store_true", help="Perform a dry run for testing purposes."
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
    args.func(dry_run=args.dry_run)
