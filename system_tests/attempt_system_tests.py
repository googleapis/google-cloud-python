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

"""Attempt to run system tests.

If the system tests are being run on Travis, no test need be run if
the build is for a PR and not a merged commit.

If being run as part of a Travis build for a merged commit, the
encrypted `key.json` file need be decrypted before running tests.

Before encrypting:

* Visit ``https://github.com/settings/tokens/new``, get a token,
  and store the token in travis.token file.
* Visit
  ``https://console.cloud.google.com/apis/credentials?project={PROJ}``
* Click "Create credentials >> Service account key", select your
  service account and create a JSON key (we'll call it ``key.json``)

Encrypt the file via::

$ travis login --github-token=$(cat travis.token)
$ travis encrypt-file --repo=GoogleCloudPlatform/google-cloud-python key.json

After running ``travis encrypt-file``, take note of the ``openssl`` command
printed out. In particular, it'll give the name of the key and
IV (initialization vector) environment variables added to the Travis
project.

See:
https://docs.travis-ci.com/user/encrypting-files/
"""


from __future__ import print_function
import argparse
import os
import subprocess
import sys

from google.cloud.environment_vars import CREDENTIALS

from run_system_test import FailedSystemTestModule
from run_system_test import run_module_tests


MODULES = (  # ordered from most to least stable
    'datastore',
    'storage',
    'bigquery',
    'pubsub',
    'language',
    'logging',
    'translate',
    'monitoring',
    'bigtable',
)

SCRIPTS_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(SCRIPTS_DIR, '..'))
ENCRYPTED_KEYFILE = os.path.join(ROOT_DIR, 'system_tests', 'key.json.enc')
ENCRYPTED_KEY_ENV = 'encrypted_c16407eb06cc_key'
ENCRYPTED_INIT_VECTOR_ENV = 'encrypted_c16407eb06cc_iv'
ALL_MODULES = object()  # Sentinel for argparser


def check_environment():
    """Check what environment this is running in.

    In particular, if the environment is Travis.

    :rtype: tuple
    :returns: A pair of booleans. The first indicates if the test
              is running in Travis and the second indicates if
              the current build is a non-PR for a merge to master.
    """
    if os.getenv('TRAVIS') == 'true':
        is_travis = True
        non_pr = (os.getenv('TRAVIS_PULL_REQUEST') == 'false' and
                  os.getenv('TRAVIS_BRANCH') == 'master')
    else:
        is_travis = non_pr = False

    return is_travis, non_pr


def decrypt_keyfile():
    """Decrypt a keyfile."""
    print('Running in Travis during merge, decrypting stored '
          'key file.')

    encrypted_key = os.getenv(ENCRYPTED_KEY_ENV)
    encrypted_iv = os.getenv(ENCRYPTED_INIT_VECTOR_ENV)
    out_file = os.getenv(CREDENTIALS)
    # Convert encrypted key file into decrypted file to be used.
    subprocess.call([
        'openssl', 'aes-256-cbc',
        '-K', encrypted_key,
        '-iv', encrypted_iv,
        '-in', ENCRYPTED_KEYFILE,
        '-out', out_file, '-d'
    ])


def prepare_to_run():
    """Prepare to run system tests.

    If on Travis during a PR, exit the entire program; there is
    no need to run the system tests.

    If on Travis during a build for a non-PR merge to master,
    decrypts stored keyfile.
    """
    is_travis, non_pr = check_environment()
    # Nothing to prepare outside of Travis. Proceed to tests.
    if not is_travis:
        return

    # On a Travis PR, exit the program.
    if not non_pr:
        print('Running in Travis during non-merge to master, '
              'doing nothing.')
        sys.exit(0)

    # On a Travis build for a merge commit to master, decrypt.
    decrypt_keyfile()


def get_parser():
    """Get an argument parser to determine a list of packages."""
    parser = argparse.ArgumentParser(
        description='google-cloud tests runner.')
    help_msg = ('List of packages to be tested. '
                'If left blank, tests all packages.')
    parser.add_argument('packages', nargs='*',
                        default=ALL_MODULES, help=help_msg)
    return parser


def get_modules():
    """Get the list of modules names to run system tests for."""
    parser = get_parser()
    args = parser.parse_args()
    if args.packages is ALL_MODULES:
        result = list(MODULES)
    else:
        result = []
        invalid = []
        for package in args.packages:
            if package in MODULES:
                result.append(package)
            else:
                invalid.append(package)

        if invalid:
            msg = 'No system test for packages: ' + ', '.join(invalid)
            print(msg, file=sys.stderr)
            sys.exit(1)

    return result


def main():
    """Run all the system tests if necessary."""
    prepare_to_run()

    failed_modules = 0
    modules = get_modules()
    for module in modules:
        try:
            run_module_tests(module)
        except FailedSystemTestModule:
            failed_modules += 1

    sys.exit(failed_modules)


if __name__ == '__main__':
    main()
