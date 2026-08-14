#!/usr/bin/env -S uv run --active --script
#
# /// script
# dependencies = [
#   "jinja2",
#   "pyyaml",
#   "ruff==0.14.14",
# ]
# ///
#
# Copyright 2026 Google LLC
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

import pathlib
import sys

scripts_dir = pathlib.Path(__file__).parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from bigquery_generator import constants, file_generator, yaml_parser  # noqa: E402


def main() -> None:
    modules = []

    for yaml_file in sorted(constants.DATA_DIR.glob("**/*.yaml")):
        modules.append(yaml_parser.parse_yaml(yaml_file))

    file_generator.generate(modules)


if __name__ == "__main__":
    main()
