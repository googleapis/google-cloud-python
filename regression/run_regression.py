import argparse
import sys
import unittest2

# This assumes the command is being run via tox hence the
# repository root is the current directory.
from regression import regression_utils


def get_parser():
    parser = argparse.ArgumentParser(
        description='GCloud test runner against actual project.')
    parser.add_argument('--package', dest='package',
                        choices=('datastore',),
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
    regression_utils.get_environ()
    test_result = run_module_tests(args.package)
    if not test_result.wasSuccessful():
        sys.exit(1)


if __name__ == '__main__':
    main()
