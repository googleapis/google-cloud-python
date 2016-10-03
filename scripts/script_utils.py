# Copyright 2016 Google Inc.
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

"""Common helpers for testing scripts."""

import os
import subprocess


LOCAL_REMOTE_ENV = 'GOOGLE_CLOUD_TESTING_REMOTE'
LOCAL_BRANCH_ENV = 'GOOGLE_CLOUD_TESTING_BRANCH'
IN_TRAVIS_ENV = 'TRAVIS'
TRAVIS_PR_ENV = 'TRAVIS_PULL_REQUEST'
TRAVIS_BRANCH_ENV = 'TRAVIS_BRANCH'


def in_travis():
    """Detect if we are running in Travis.

    .. _Travis env docs: https://docs.travis-ci.com/user/\
                         environment-variables\
                         #Default-Environment-Variables

    See `Travis env docs`_.

    :rtype: bool
    :returns: Flag indicating if we are running on Travis.
    """
    return os.getenv(IN_TRAVIS_ENV) == 'true'


def in_travis_pr():
    """Detect if we are running in a pull request on Travis.

    .. _Travis env docs: https://docs.travis-ci.com/user/\
                         environment-variables\
                         #Default-Environment-Variables

    See `Travis env docs`_.

    .. note::

        This assumes we already know we are running in Travis.

    :rtype: bool
    :returns: Flag indicating if we are in a pull request on Travis.
    """
    # NOTE: We're a little extra cautious and make sure that the
    #       PR environment variable is an integer.
    try:
        int(os.getenv(TRAVIS_PR_ENV, ''))
        return True
    except ValueError:
        return False


def travis_branch():
    """Get the current branch of the PR.

    .. _Travis env docs: https://docs.travis-ci.com/user/\
                         environment-variables\
                         #Default-Environment-Variables

    See `Travis env docs`_.

    .. note::

        This assumes we already know we are running in Travis
        during a PR.

    :rtype: str
    :returns: The name of the branch the current pull request is
              changed against.
    :raises: :class:`~exceptions.OSError` if the ``TRAVIS_BRANCH_ENV``
             environment variable isn't set during a pull request
             build.
    """
    try:
        return os.environ[TRAVIS_BRANCH_ENV]
    except KeyError:
        msg = ('Pull request build does not have an '
               'associated branch set (via %s)') % (TRAVIS_BRANCH_ENV,)
        raise OSError(msg)


def check_output(*args):
    """Run a command on the operation system.

    :type args: tuple
    :param args: Arguments to pass to ``subprocess.check_output``.

    :rtype: str
    :returns: The raw STDOUT from the command (converted from bytes
              if necessary).
    """
    cmd_output = subprocess.check_output(args)
    # On Python 3, this returns bytes (from STDOUT), so we
    # convert to a string.
    cmd_output = cmd_output.decode('utf-8')
    # Also strip the output since it usually has a trailing newline.
    return cmd_output.strip()


def rootname(filename):
    """Get the root directory that a file is contained in.

    :type filename: str
    :param filename: The path / name of a file.

    :rtype: str
    :returns: The root directory containing the file.
    """
    if os.path.sep not in filename:
        return ''
    else:
        file_root, _ = filename.split(os.path.sep, 1)
        return file_root


def get_changed_packages(blob_name1, blob_name2, package_list):
    """Get a list of packages which have changed between two changesets.

    :type blob_name1: str
    :param blob_name1: The name of a commit hash or branch name or other
                       ``git`` artifact.

    :type blob_name2: str
    :param blob_name2: The name of a commit hash or branch name or other
                       ``git`` artifact.

    :type package_list: list
    :param package_list: The list of **all** valid packages with unit tests.

    :rtype: list
    :returns: A list of all package directories that have changed
              between ``blob_name1`` and ``blob_name2``. Starts
              with a list of valid packages (``package_list``)
              and filters out the unchanged directories.
    """
    changed_files = check_output(
        'git', 'diff', '--name-only', blob_name1, blob_name2)
    changed_files = changed_files.split('\n')

    result = set()
    for filename in changed_files:
        file_root = rootname(filename)
        if file_root in package_list:
            result.add(file_root)

    return sorted(result)
