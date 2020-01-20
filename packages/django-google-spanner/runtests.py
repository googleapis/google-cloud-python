# Copyright (c) 2020 Google LLC. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import sys
import unittest


def run_unittests(module):
    test_suite = unittest.TestLoader().discover(module)
    result = unittest.TextTestRunner(verbosity=1).run(test_suite)
    sys.exit(any(result.failures or result.errors))


def run_parse_util_tests():
    pass


def run_django_tests():
    raise Exception('Unimplemented')


def main():
    run_unittests('tests.spanner.dbapi')


if __name__ == '__main__':
    main()
