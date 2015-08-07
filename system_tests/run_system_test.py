# Copyright 2014 Google Inc. All rights reserved.
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
import unittest2

# This assumes the command is being run via tox hence the
# repository root is the current directory.
from system_tests import system_test_utils

REQUIREMENTS = {
    'datastore': ['dataset_id', 'credentials'],
    'storage': ['project', 'credentials'],
    'pubsub': ['project', 'credentials'],
    'bigquery': ['project', 'credentials'],
}


def get_parser():
    parser = argparse.ArgumentParser(
        description='GCloud test runner against actual project.')
    parser.add_argument('--package', dest='package',
                        choices=REQUIREMENTS.keys(),
                        default='datastore', help='Package to be tested.')
    return parser


def run_module_tests(module_name):
    suite = unittest2.TestSuite()
    tests = unittest2.defaultTestLoader.loadTestsFromName(module_name)
    suite.addTest(tests)
    return unittest2.TextTestRunner(verbosity=2).run(suite)


def main():
    parser = get_parser()
    args = parser.parse_args()
    # Make sure environ is set before running test.
    requirements = REQUIREMENTS[args.package]
    system_test_utils.check_environ(*requirements)

    test_result = run_module_tests(args.package)
    if not test_result.wasSuccessful():
        sys.exit(1)


if __name__ == '__main__':
    main()
