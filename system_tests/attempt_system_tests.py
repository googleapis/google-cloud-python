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
"""


import os
import subprocess
import sys

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
)
if sys.version_info[:2] == (2, 7):
    MODULES += ('bigtable',)

SCRIPTS_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(SCRIPTS_DIR, '..'))
ENCRYPTED_KEYFILE = os.path.join(ROOT_DIR, 'system_tests', 'key.json.enc')


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

    encrypted_key = os.getenv('encrypted_a1b222e8c14d_key')
    encrypted_iv = os.getenv('encrypted_a1b222e8c14d_iv')
    out_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
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


def main():
    """Run all the system tests if necessary."""
    prepare_to_run()
    failed_modules = 0
    for module in MODULES:
        try:
            run_module_tests(module)
        except FailedSystemTestModule:
            failed_modules += 1

    sys.exit(failed_modules)

if __name__ == '__main__':
    main()
