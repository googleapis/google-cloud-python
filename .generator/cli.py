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
import sys

def handle_configure(args):
    # TODO(https://github.com/googleapis/librarian/issues/466): Implement configure command.
    print("'configure' command executed.")

def handle_generate(args):
    # TODO(https://github.com/googleapis/librarian/issues/448): Implement generate command.
    print("'generate' command executed.")

def handle_build(args):
    # TODO(https://github.com/googleapis/librarian/issues/450): Implement build command.
    print("'build' command executed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple CLI tool.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Define commands
    for command_name, help_text in [
        ("configure", "Onboard a new library or an api path to Librarian workflow."),
        ("generate", "generate a python client for an API."),
        ("build", "Run unit tests via nox for the generated library.")
    ]:
        handler_map = {"configure": handle_configure, "generate": handle_generate, "build": handle_build}
        parser_cmd = subparsers.add_parser(command_name, help=help_text)
        parser_cmd.set_defaults(func=handler_map[command_name])

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)