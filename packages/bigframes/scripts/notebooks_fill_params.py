# Copyright 2024 Google LLC
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

import json
import os
import re
import shutil
import sys

GOOGLE_CLOUD_PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]


def make_backup(notebook_path: str):
    shutil.copy(
        notebook_path,
        f"{notebook_path}.backup",
    )


def replace_project(line):
    """
    Notebooks contain special colab `param {type:"string"}`
    comments, which make it easy for customers to fill in their
    own information.
    """
    # Make sure we're robust to whitespace differences.
    cleaned = re.sub(r"\s", "", line)
    if cleaned == 'PROJECT_ID=""#@param{type:"string"}':
        return f'PROJECT_ID = "{GOOGLE_CLOUD_PROJECT}"  # @param {{type:"string"}}\n'
    else:
        return line


def replace_params(notebook_path: str):
    with open(notebook_path, "r", encoding="utf-8") as notebook_file:
        notebook_json = json.load(notebook_file)

    for cell in notebook_json["cells"]:
        lines = cell.get("source", [])
        new_lines = [replace_project(line) for line in lines]
        cell["source"] = new_lines

    with open(notebook_path, "w", encoding="utf-8") as notebook_file:
        json.dump(notebook_json, notebook_file, indent=2, ensure_ascii=False)


def main(notebook_paths):
    for notebook_path in notebook_paths:
        make_backup(notebook_path)
        replace_params(notebook_path)


if __name__ == "__main__":
    main(sys.argv[1:])
