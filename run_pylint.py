"""Custom script to run PyLint on gcloud codebase.

This runs pylint as a script via subprocess in two different
subprocesses. The first lints the production/library code
using the default rc file (PRODUCTION_RC). The second lints the
demo/test code using an rc file (TEST_RC) which allows more style
violations (hence it has a reduced number of style checks).
"""

import ConfigParser
import copy
import os
import subprocess
import sys


IGNORED_FILES = [
    'gcloud/datastore/datastore_v1_pb2.py',
    'docs/conf.py',
    'setup.py',
]
PRODUCTION_RC = 'pylintrc_default'
TEST_RC = 'pylintrc_reduced'
TEST_DISABLED_MESSAGES = [
    'invalid-name',
    'missing-docstring',
    'too-many-public-methods',
    'too-few-public-methods',
    'attribute-defined-outside-init',
    'unbalanced-tuple-unpacking',
    'too-many-locals',
    'exec-used',
    'no-init',
    'no-self-use',
]
TEST_RC_ADDITIONS = {
    'MESSAGES CONTROL': {
        'disable': ', '.join(TEST_DISABLED_MESSAGES),
    },
}


def read_config(filename):
    """Reads pylintrc config onto native ConfigParser object."""
    config = ConfigParser.ConfigParser()
    with open(filename, 'r') as file_obj:
        config.readfp(file_obj)
    return config


def make_test_rc(base_rc_filename, additions_dict, target_filename):
    """Combines a base rc and test additions into single file."""
    main_cfg = read_config(base_rc_filename)

    # Create fresh config for test, which must extend production.
    test_cfg = ConfigParser.ConfigParser()
    test_cfg._sections = copy.deepcopy(main_cfg._sections)

    for section, opts in additions_dict.items():
        curr_section = test_cfg._sections.setdefault(
            section, test_cfg._dict())
        for opt, opt_val in opts.items():
            curr_val = curr_section.get(opt)
            if curr_val is None:
                raise KeyError('Expected to be adding to existing option.')
            curr_section[opt] = '%s, %s' % (curr_val, opt_val)

    with open(target_filename, 'w') as file_obj:
        test_cfg.write(file_obj)


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


def get_files_for_linting():
    """Gets a list of files in the repository.

    By default returns all files via `git ls-files`. However, if the
    environment variables `GCLOUD_REMOTE_FOR_LINT` and `GCLOUD_BRANCH_FOR_LINT`
    are set, this will return only those files which have changed since
    the last commit in `REMOTE_FOR_LINT/BRANCH_FOR_LINT`
    """
    remote = os.getenv('GCLOUD_REMOTE_FOR_LINT')
    branch = os.getenv('GCLOUD_BRANCH_FOR_LINT')

    if remote is None or branch is None:
        print 'Remote branch not specified, listing all files in repository.'
        result = subprocess.check_output(['git', 'ls-files'])
    else:
        remote_branch = '%s/%s' % (remote, branch)
        result = subprocess.check_output(['git', 'diff', '--name-only',
                                          remote_branch])
        print 'Using files changed relative to %s:' % (remote_branch,)
        print '-' * 60
        print result.rstrip('\n')  # Don't print trailing newlines.
        print '-' * 60

    return result.rstrip('\n').split('\n')


def get_python_files():
    """Gets a list of all Python files in the repository that need linting.

    Relies on get_files_for_linting() to determine which files should be
    considered.

    NOTE: This requires `git` to be installed and requires that this
          is run within the `git` repository.

    :rtype: `tuple`
    :returns: A tuple containing two lists. The first list contains
              all production files and the next all test/demo files.
    """
    all_files = get_files_for_linting()

    library_files = []
    non_library_files = []
    for filename in all_files:
        if valid_filename(filename):
            if is_production_filename(filename):
                library_files.append(filename)
            else:
                non_library_files.append(filename)

    return library_files, non_library_files


def lint_fileset(filenames, rcfile, description):
    """Lints a group of files using a given rcfile."""
    if filenames:
        rc_flag = '--rcfile=%s' % (rcfile,)
        pylint_shell_command = ['pylint', rc_flag] + filenames
        status_code = subprocess.call(pylint_shell_command)
        if status_code != 0:
            error_message = ('Pylint failed on %s with '
                             'status %d.' % (description, status_code))
            print >> sys.stderr, error_message
            sys.exit(status_code)
    else:
        print 'Skipping %s, no files to lint.' % (description,)


def main():
    """Script entry point. Lints both sets of files."""
    make_test_rc(PRODUCTION_RC, TEST_RC_ADDITIONS, TEST_RC)
    library_files, non_library_files = get_python_files()
    lint_fileset(library_files, PRODUCTION_RC, 'library code')
    lint_fileset(non_library_files, TEST_RC, 'test and demo code')


if __name__ == '__main__':
    main()
