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

import pathlib
import shutil
import sys


def restore_from_backup(notebook_path):
    backup_path = pathlib.Path(f"{notebook_path}.backup")
    if backup_path.exists():
        shutil.move(
            backup_path,
            notebook_path,
        )


def main(notebook_paths):
    for notebook_path in notebook_paths:
        restore_from_backup(notebook_path)


if __name__ == "__main__":
    main(sys.argv[1:])
