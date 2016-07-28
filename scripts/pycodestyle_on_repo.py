# Copyright 2016 Google Inc. All rights reserved.
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

"""Custom script to run pycodestyle on gcloud codebase.

This runs pycodestyle as a script via subprocess but only runs it on the
.py files that are checked in to the repository.
"""


import os
import subprocess
import sys


def main():
    """Run pycodestyle on all Python files in the repository."""
    git_root = subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel']).strip()
    os.chdir(git_root)
    python_files = subprocess.check_output(['git', 'ls-files', '*py'])
    python_files = python_files.strip().split()

    pycodestyle_command = ['pycodestyle'] + python_files
    status_code = subprocess.call(pycodestyle_command)
    sys.exit(status_code)


if __name__ == '__main__':
    main()
