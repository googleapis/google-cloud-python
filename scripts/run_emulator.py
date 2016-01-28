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

"""Run system tests locally with the emulator.

First makes system calls to spawn the emulator and get the local environment
variable needed for it. Then calls the system tests.
"""


import argparse
import os
import subprocess

from gcloud.environment_vars import GCD_DATASET
from gcloud.environment_vars import GCD_HOST
from gcloud.environment_vars import PUBSUB_EMULATOR
from system_tests.run_system_test import run_module_tests


PACKAGE_INFO = {
    'datastore': (GCD_DATASET, GCD_HOST),
    'pubsub': (PUBSUB_EMULATOR,)
}


def get_parser():
    """Get simple ``argparse`` parser to determine package.

    :rtype: :class:`argparse.ArgumentParser`
    :returns: The parser for this script.
    """
    parser = argparse.ArgumentParser(
        description='Run GCloud system tests against local emulator.')
    parser.add_argument('--package', dest='package',
                        choices=('datastore', 'pubsub'),
                        default='datastore', help='Package to be tested.')
    return parser


def get_start_command(package):
    """Get command line arguments for starting emulator.

    :type package: str
    :param package: The package to start an emulator for.

    :rtype: tuple
    :returns: The arguments to be used, in a tuple.
    """
    return ('gcloud', 'beta', 'emulators', package, 'start')


def get_env_init_command(package):
    """Get command line arguments for getting emulator env. info.

    :type package: str
    :param package: The package to get environment info for.

    :rtype: tuple
    :returns: The arguments to be used, in a tuple.
    """
    return ('gcloud', 'beta', 'emulators', package, 'env-init')


def run_tests_in_emulator(package):
    """Spawn an emulator instance and run the system tests.

    :type package: str
    :param package: The package to run system tests against.
    """
    # Make sure this package has environment vars to replace.
    env_vars = PACKAGE_INFO[package]

    start_command = get_start_command(package)
    # Ignore stdin and stdout, don't pollute the user's output with them.
    proc_start = subprocess.Popen(start_command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    try:
        env_init_command = get_env_init_command(package)
        env_lines = subprocess.check_output(
            env_init_command).strip().split('\n')
        # Set environment variables before running the system tests.
        for env_var in env_vars:
            line_prefix = 'export ' + env_var + '='
            value, = [line.split(line_prefix, 1)[1] for line in env_lines
                      if line.startswith(line_prefix)]
            os.environ[env_var] = value
        run_module_tests(package,
                         ignore_requirements=True)
    finally:
        # NOTE: This is mostly defensive. Since ``proc_start`` will be spawned
        #       by this current process, it should be killed when this process
        #       exits whether or not we kill it.
        proc_start.kill()


def main():
    """Main method to run this script."""
    parser = get_parser()
    args = parser.parse_args()
    run_tests_in_emulator(args.package)


if __name__ == '__main__':
    main()
