# Copyright 2017 Google LLC
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

"""Print a list of packages which require testing."""

import pathlib
import subprocess

import ci_diff_helper


def print_environment(environment):
    print("-> CI environment:")
    print('Branch', environment.branch)
    print('PR', environment.pr)
    print('In PR', environment.in_pr)
    print('Repo URL', environment.repo_url)
    if environment.in_pr:
        print('PR Base', environment.base)


def get_base(environment):
    if environment.in_pr:
        return environment.base
    else:
        # If we're not in a PR, just calculate the changes between this commit
        # and its parent.
        return 'HEAD~1'


def get_changed_files(base):
    return subprocess.check_output([
        'git', 'diff', '--name-only', f'{base}..HEAD',
    ], stderr=subprocess.DEVNULL).decode('utf8').strip().split('\n')


def determine_changed_packages(changed_files):
    packages = [
        path.parent for path in pathlib.Path('.').glob('*/noxfile.py')
    ]

    changed_packages = set()
    for file in changed_files:
        file = pathlib.Path(file)
        for package in packages:
            if package in file.parents:
                changed_packages.add(package)

    return changed_packages


def main():
    environment = ci_diff_helper.get_config()
    print_environment(environment)
    base = get_base(environment)
    changed_files = get_changed_files(base)
    packages = determine_changed_packages(changed_files)

    print(f"Comparing against {base}.")
    print("-> Changed packages:")

    for package in packages:
        print(package)


main()
