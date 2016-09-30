# Copyright 2016 Google Inc.
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

"""Script to run unit tests for the entire project.

This script orchestrates stepping into each sub-package and
running tests. It also allows running a limited subset of tests
in cases where such a limited subset can be identified.
"""

from __future__ import print_function

import argparse
import os
import subprocess
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))
IGNORED_DIRECTORIES = (
    'appveyor',
    'docs',
    'scripts',
    'system_tests',
)
TOX_ENV_VAR = 'TOXENV'
ACCEPTED_VERSIONS = {
    (2, 7): 'py27',
    (3, 4): 'py34',
    (3, 5): 'py35',
}


def check_output(*args):
    """Run a command on the operation system.

    :type args: tuple
    :param args: Keyword arguments to pass to ``subprocess.check_output``.

    :rtype: str
    :returns: The raw STDOUT from the command (converted from bytes
              if necessary).
    """
    cmd_output = subprocess.check_output(args)
    # On Python 3, this returns bytes (from STDOUT), so we
    # convert to a string.
    cmd_output = cmd_output.decode('utf-8')
    # Also strip the output since it usually has a trailing newline.
    return cmd_output.strip()


def get_package_directories():
    """Get a list of directories containing sub-packages.

    :rtype: list
    :returns: A list of all sub-package directories.
    """
    # Run ls-tree with
    #          -d: For directories only
    # --name-only: No extra info like the type/hash/permission bits.
    # --full-name: Give path relative to root, rather than cwd.
    ls_tree_out = check_output(
        'git', 'ls-tree',
        '-d', '--name-only', '--full-name',
        'HEAD', PROJECT_ROOT)
    result = []
    for package in ls_tree_out.split('\n'):
        if package not in IGNORED_DIRECTORIES:
            result.append(package)
    return result


def run_package(package, tox_env):
    """Run tox environment for a given package.

    :type package: str
    :param package: The name of the subdirectory which holds the sub-package.
                    This will be a path relative to ``PROJECT_ROOT``.

    :type tox_env: str
    :param tox_env: The ``tox`` environment(s) to run in each sub-package.

    :rtype: bool
    :returns: Flag indicating if the test run succeeded.
    """
    curr_dir = os.getcwd()
    package_dir = os.path.join(PROJECT_ROOT, package)
    try:
        os.chdir(package_dir)
        return_code = subprocess.call(['tox', '-e', tox_env])
        return return_code == 0
    finally:
        os.chdir(curr_dir)


def get_parser():
    """Get simple ``argparse`` parser to determine configuration.

    :rtype: :class:`argparse.ArgumentParser`
    :returns: The parser for this script.
    """
    description = 'Run tox environment(s) in all sub-packages.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--tox-env', dest='tox_env',
        help='The tox environment(s) to run in sub-packages.')
    return parser


def get_tox_env_from_version():
    """Get ``tox`` environment from the current Python version.

    :rtype: str
    :returns: The current ``tox`` environment to be used, e.g. ``"py27"``.
    :raises: :class:`EnvironmentError` if the first two options
             don't yield any value and the current version of
             Python is not in ``ACCEPTED_VERSIONS``.
    """
    version_info = sys.version_info[:2]
    try:
        return ACCEPTED_VERSIONS[version_info]
    except KeyError:
        raise EnvironmentError(
            'Invalid Python version', version_info,
            'Accepted versions are',
            sorted(ACCEPTED_VERSIONS.keys()))


def get_tox_env():
    """Get the environment to be used with ``tox``.

    Tries to infer the ``tox`` environment in the following order

    * From the ``--tox-env`` command line flag
    * From the ``TOXENV`` environment variable
    * From the version of the current running Python

    :rtype: str
    :returns: The current ``tox`` environment to be used, e.g. ``"py27"``.
    """
    parser = get_parser()
    args = parser.parse_args()
    if args.tox_env is not None:
        tox_env = args.tox_env
    elif TOX_ENV_VAR in os.environ:
        tox_env = os.environ[TOX_ENV_VAR]
    else:
        tox_env = get_tox_env_from_version()

    return tox_env


def main():
    """Run all the unit tests that need to be run."""
    packages_to_run = get_package_directories()
    if not packages_to_run:
        print('No tests to run.')
        return

    tox_env = get_tox_env()
    failed_packages = []
    for package in packages_to_run:
        succeeded = run_package(package, tox_env)
        if not succeeded:
            failed_packages.append(package)

    if failed_packages:
        msg_parts = ['Sub-packages failed:']
        for package in failed_packages:
            msg_parts.append('- ' + package)
        msg = '\n'.join(msg_parts)
        print(msg, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
