"""Custom script to run PyLint on gcloud codebase.

This runs pylint as a script via subprocess in two different
subprocesses. The first lints the production/library code
using the default rc file (PRODUCTION_RC). The second lints the
demo/test code using an rc file (TEST_RC) which allows more style
violations (hence it has a reduced number of style checks).
"""

import subprocess
import sys


IGNORED_FILES = [
    'gcloud/datastore/datastore_v1_pb2.py',
    'docs/conf.py',
    'setup.py',
]
PRODUCTION_RC = 'pylintrc_default'
TEST_RC = 'pylintrc_reduced'


def valid_filename(filename):
    """Checks if a file is a Python file and is not ignored."""
    return (filename.endswith('.py') and
            filename not in IGNORED_FILES)


def is_production_filename(filename):
    """Checks if the file contains production code.

    :rtype: `bool`
    :returns: Boolean indicating production status.
    """
    return not ('demo' in filename or 'test' in filename
                or filename.startswith('regression'))


def get_python_files():
    """Gets a list of all Python files in the repository.

    NOTE: This requires `git` to be installed and requires that this
          is run within the `git` repository.

    :rtype: `tuple`
    :returns: A tuple containing two lists. The first list contains
              all production files and the next all test/demo files.
    """
    all_files = subprocess.check_output(['git', 'ls-files'])

    library_files = []
    non_library_files = []
    for filename in all_files.split('\n'):
        if valid_filename(filename):
            if is_production_filename(filename):
                library_files.append(filename)
            else:
                non_library_files.append(filename)

    return library_files, non_library_files


def lint_fileset(filenames, rcfile, description):
    """Lints a group of files using a given rcfile."""
    rc_flag = '--rcfile=%s' % (rcfile,)
    pylint_shell_command = ['pylint', rc_flag] + filenames
    status_code = subprocess.call(pylint_shell_command)
    if status_code != 0:
        error_message = ('Pylint failed on %s with '
                         'status %d.' % (description, status_code))
        print >> sys.stderr, error_message
        sys.exit(status_code)


def main():
    """Script entry point. Lints both sets of files."""
    library_files, non_library_files = get_python_files()
    lint_fileset(library_files, PRODUCTION_RC, 'library code')
    lint_fileset(non_library_files, TEST_RC, 'test and demo code')


if __name__ == '__main__':
    main()
