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
import unittest

import bigquery
import bigtable
import datastore
import language
import logging_
import monitoring
import pubsub
import storage
import system_test_utils
import translate


TEST_MODULES = {
    'datastore': datastore,
    'storage': storage,
    'pubsub': pubsub,
    'bigquery': bigquery,
    'bigtable': bigtable,
    'language': language,
    'logging': logging_,
    'monitoring': monitoring,
    'translate': translate,
}


class FailedSystemTestModule(Exception):
    pass


def get_parser():
    parser = argparse.ArgumentParser(
        description='GCloud test runner against actual project.')
    parser.add_argument('--package', dest='package',
                        choices=TEST_MODULES.keys(),
                        default='datastore', help='Package to be tested.')
    parser.add_argument(
        '--ignore-requirements',
        dest='ignore_requirements', action='store_true',
        help='Ignore the credentials requirement for the test.')
    return parser


def run_module_tests(module_name, ignore_requirements=False):
    if not ignore_requirements:
        # Make sure environ is set before running test.
        system_test_utils.check_environ()

    suite = unittest.TestSuite()
    test_mod = TEST_MODULES[module_name]
    tests = unittest.defaultTestLoader.loadTestsFromModule(test_mod)
    suite.addTest(tests)

    # Run tests.
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    # Exit if not successful.
    if not test_result.wasSuccessful():
        raise FailedSystemTestModule(module_name)


def main():
    parser = get_parser()
    args = parser.parse_args()
    try:
        run_module_tests(args.package,
                         ignore_requirements=args.ignore_requirements)
    except FailedSystemTestModule:
        sys.exit(1)


if __name__ == '__main__':
    main()
