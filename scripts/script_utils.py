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

from __future__ import print_function

import ast
import os
import subprocess


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))
LOCAL_REMOTE_ENV = 'GOOGLE_CLOUD_TESTING_REMOTE'
LOCAL_BRANCH_ENV = 'GOOGLE_CLOUD_TESTING_BRANCH'
IN_TRAVIS_ENV = 'TRAVIS'
TRAVIS_PR_ENV = 'TRAVIS_PULL_REQUEST'
TRAVIS_BRANCH_ENV = 'TRAVIS_BRANCH'
INST_REQS_KWARG = 'install_requires'
REQ_VAR = 'REQUIREMENTS'
PACKAGE_PREFIX = 'google-cloud-'


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


def local_diff_branch():
    """Get a remote branch to diff against in a local checkout.

    Checks if the the local remote and local branch environment
    variables specify a remote branch.

    :rtype: str
    :returns: The diffbase `{remote}/{branch}` if the environment
              variables are defined. If not, returns ``None``.
    """
    # Only allow specified remote and branch in local dev.
    remote = os.getenv(LOCAL_REMOTE_ENV)
    branch = os.getenv(LOCAL_BRANCH_ENV)
    if remote is not None and branch is not None:
        return '%s/%s' % (remote, branch)


def get_affected_files(allow_limited=True):
    """Gets a list of files in the repository.

    By default, returns all files via ``git ls-files``. However, in some cases
    uses a specific commit or branch (a so-called diff base) to compare
    against for changed files. (This requires ``allow_limited=True``.)

    To speed up linting on Travis pull requests against master, we manually
    set the diff base to the branch the pull request is against. We don't do
    this on "push" builds since "master" will be the currently checked out
    code. One could potentially use ${TRAVIS_COMMIT_RANGE} to find a diff base
    but this value is not dependable.

    To allow faster local ``tox`` runs, the local remote and local branch
    environment variables can be set to specify a remote branch to diff
    against.

    :type allow_limited: bool
    :param allow_limited: Boolean indicating if a reduced set of files can
                          be used.

    :rtype: pair
    :returns: Tuple of the diff base using the list of filenames to be
              linted.
    """
    diff_base = None
    if in_travis():
        # In the case of a pull request into a branch, we want to
        # diff against HEAD in that branch.
        if in_travis_pr():
            diff_base = travis_branch()
    else:
        diff_base = local_diff_branch()

    if diff_base is not None and allow_limited:
        result = subprocess.check_output(['git', 'diff', '--name-only',
                                          diff_base])
        print('Using files changed relative to %s:' % (diff_base,))
        print('-' * 60)
        print(result.rstrip('\n'))  # Don't print trailing newlines.
        print('-' * 60)
    else:
        print('Diff base not specified, listing all files in repository.')
        result = subprocess.check_output(['git', 'ls-files'])

    # Only return filenames that exist. For example, 'git diff --name-only'
    # could spit out deleted / renamed files. Another alternative could
    # be to use 'git diff --name-status' and filter out files with a
    # status of 'D'.
    filenames = [filename
                 for filename in result.rstrip('\n').split('\n')
                 if os.path.exists(filename)]
    return filenames, diff_base


def get_required_packages(file_contents):
    """Get required packages from a ``setup.py`` file.

    Makes the following assumptions:

    * ``install_requires=REQUIREMENTS`` occurs in the call to
      ``setup()`` in the ``file_contents``.
    * The text ``install_requires`` occurs nowhere else in the file.
    * The text ``REQUIREMENTS`` only appears when being passed to
      ``setup()`` (as above) and when being defined.
    * The ``REQUIREMENTS`` variable is a list and the text from the
      ``setup.py`` file containing that list can be parsed using
      ``ast.literal_eval()``.

    :type file_contents: str
    :param file_contents: The contents of a ``setup.py`` file.

    :rtype: list
    :returns: The list of required packages.
    :raises: :class:`~exceptions.ValueError` if the file is in an
             unexpected format.
    """
    # Make sure the only ``install_requires`` happens in the
    # call to setup()
    if file_contents.count(INST_REQS_KWARG) != 1:
        raise ValueError('Expected only one use of keyword',
                         INST_REQS_KWARG, file_contents)
    # Make sure the only usage of ``install_requires`` is to set
    # install_requires=REQUIREMENTS.
    keyword_stmt = INST_REQS_KWARG + '=' + REQ_VAR
    if file_contents.count(keyword_stmt) != 1:
        raise ValueError('Expected keyword to be set with variable',
                         INST_REQS_KWARG, REQ_VAR, file_contents)
    # Split file on ``REQUIREMENTS`` variable while asserting that
    # it only appear twice.
    _, reqs_section, _ = file_contents.split(REQ_VAR)
    # Find ``REQUIREMENTS`` list variable defined in ``reqs_section``.
    reqs_begin = reqs_section.index('[')
    reqs_end = reqs_section.index(']') + 1

    # Convert the text to an actual list, but make sure no
    # locals or globals can be used.
    reqs_list_text = reqs_section[reqs_begin:reqs_end]
    # We use literal_eval() because it limits to evaluating
    # strings that only consist of a few Python literals: strings,
    # numbers, tuples, lists, dicts, booleans, and None.
    requirements = ast.literal_eval(reqs_list_text)

    # Take the list of requirements and strip off the package name
    # from each requirement.
    result = []
    for required in requirements:
        parts = required.split()
        result.append(parts[0])
    return result


def get_dependency_graph(package_list):
    """Get a directed graph of package dependencies.

    :type package_list: list
    :param package_list: The list of **all** valid packages.

    :rtype: dict
    :returns: A dictionary where keys are packages and values are
              the set of packages that depend on the key.
    """
    result = {package: set() for package in package_list}
    for package in package_list:
        setup_file = os.path.join(PROJECT_ROOT, package,
                                  'setup.py')
        with open(setup_file, 'r') as file_obj:
            file_contents = file_obj.read()

        requirements = get_required_packages(file_contents)
        for requirement in requirements:
            if not requirement.startswith(PACKAGE_PREFIX):
                continue
            _, req_package = requirement.split(PACKAGE_PREFIX)
            req_package = req_package.replace('-', '_')
            result[req_package].add(package)

    return result


def follow_dependencies(subset, package_list):
    """Get a directed graph of package dependencies.

    :type subset: list
    :param subset: List of a subset of package names.

    :type package_list: list
    :param package_list: The list of **all** valid packages.

    :rtype: list
    :returns: An expanded list of packages containing everything
              in ``subset`` and any packages that depend on those.
    """
    dependency_graph = get_dependency_graph(package_list)

    curr_pkgs = None
    updated_pkgs = set(subset)
    while curr_pkgs != updated_pkgs:
        curr_pkgs = updated_pkgs
        updated_pkgs = set(curr_pkgs)
        for package in curr_pkgs:
            updated_pkgs.update(dependency_graph[package])

    return sorted(curr_pkgs)
