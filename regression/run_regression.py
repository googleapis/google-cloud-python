import argparse
import unittest2


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
    unittest2.TextTestRunner(verbosity=2).run(suite)


def main():
    parser = get_parser()
    args = parser.parse_args()
    run_module_tests(args.package)


if __name__ == '__main__':
    main()
