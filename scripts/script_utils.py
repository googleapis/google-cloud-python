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

import json
import os
import re
import sys
import subprocess

# Mimic six here, but avoid any dependencies outside
# the standard library.
try:
    import httplib as http_client
except ImportError:
    import http.client as http_client
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


LOCAL_REMOTE_ENV = 'GOOGLE_CLOUD_TESTING_REMOTE'
LOCAL_BRANCH_ENV = 'GOOGLE_CLOUD_TESTING_BRANCH'
IN_TRAVIS_ENV = 'TRAVIS'
TRAVIS_PR_ENV = 'TRAVIS_PULL_REQUEST'
TRAVIS_BRANCH_ENV = 'TRAVIS_BRANCH'
TRAVIS_TAG_ENV = 'TRAVIS_TAG'
PR_ID_REGEX = re.compile(r'#(\d+)')
GITHUB_API_PR_TEMPLATE = ('https://api.github.com/repos/GoogleCloudPlatform/'
                          'google-cloud-python/pulls/%d')
GITHUB_FILE_CHG_TEMPLATE = GITHUB_API_PR_TEMPLATE + '/files'


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


def in_travis_tag():
    """Detect if we are running in a Travis tag build.

    .. _Travis env docs: https://docs.travis-ci.com/user/\
                         environment-variables\
                         #Default-Environment-Variables

    See `Travis env docs`_.

    .. note::

        This assumes we already know we are running in Travis.

    :rtype: bool
    :returns: Flag indicating if we are in Travis tag build.
    """
    tag_val = os.getenv(TRAVIS_TAG_ENV, '')
    return tag_val != ''


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


def packages_from_files(changed_files, package_list):
    """Determine a list of packages from a list of files.

    :type changed_files: list
    :param changed_files: A list of filenames.

    :type package_list: list
    :param package_list: The list of **all** valid packages with unit tests.

    :rtype: list
    :returns: The list of packages with changes among the files
              in ``changed_files``.
    """
    result = set()
    for filename in changed_files:
        file_root = rootname(filename)
        if file_root in package_list:
            result.add(file_root)

    return sorted(result)


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
    return packages_from_files(changed_files, package_list)


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

    return result.rstrip('\n').split('\n'), diff_base


def get_pr_from_latest_commit():
    """Attempt to determine a pull request from the latest commit.

    Checks that there is only one ``#`` character in the commit subject
    and then reads the integer that comes after.

    If a valid integer is found, confirms that such a PR exists and has
    the same ``merge_commit_sha`` as the ``HEAD`` commit.

    :rtype: int
    :returns: The ID of the pull request found in the latest commit.
              If none can be found, returns -1.
    """
    commit_info = check_output(
        'git', 'log', '-1', 'HEAD', '--pretty=%H|%s')
    head_commit_sha, commit_subject = commit_info.split('|', 1)

    # First, attempt to determine the PR ID from the commit subject.
    matches = PR_ID_REGEX.findall(commit_subject)
    if len(matches) != 1:
        msg = '\n'.join([
            'Cannot uniquely determine a commit ID from commit subject:',
            commit_subject])
        print(msg, file=sys.stderr)
        return -1

    # Then, use the computed ID to get PR info from GitHub.
    id_val = int(matches[0])
    api_url = GITHUB_API_PR_TEMPLATE % (id_val,)

    response = urlopen(api_url)
    if response.getcode() != http_client.OK:
        msg = '\n'.join([
            'GitHub API request failed:',
            'URL: %r' % (api_url,)])
        print(msg, file=sys.stderr)
        return -1

    # NOTE: We assume the GitHub API will always return valid
    #       JSON when the response status code is OK.
    content = response.read().decode('utf-8')
    response.close()
    api_response = json.loads(content)

    # Then, check if the PR has been merged.
    if not api_response['merged']:
        msg = 'Matched GitHub PR (%d) has not been merged.' % (id_val,)
        print(msg, file=sys.stderr)
        return -1

    merge_commit_sha = api_response['merge_commit_sha']

    # Finally, check if the merge commit SHA from GitHub agrees with
    # the current HEAD commit.
    if merge_commit_sha == head_commit_sha:
        return id_val
    else:
        msg = '\n'.join([
            'GitHub PR merge commit SHA does not match HEAD:',
            '        HEAD commit: %s' % (head_commit_sha,),
            'GitHub merge commit: %s' % (merge_commit_sha,)])
        print(msg, file=sys.stderr)
        return -1


def get_github_changes(pr_id):
    """Get list of changed files in a GitHub PR.

    .. note::

        This assumes ``pr_id`` corresponds to a valid merged
        pull request.

    :type pr_id: int
    :param pr_id: The ID of a GitHub pull request.

    :rtype: list
    :returns: List of filenames changed in the PR. If the GitHub
              API request fails, will return ``None``.
    """
    api_url = GITHUB_FILE_CHG_TEMPLATE % (pr_id,)

    # Make GitHub API request.
    response = urlopen(api_url)
    if response.getcode() != http_client.OK:
        msg = '\n'.join([
            'GitHub API request failed:',
            'URL: %r' % (api_url,)])
        print(msg, file=sys.stderr)
        return

    # NOTE: We assume the GitHub API will always return valid
    #       JSON when the response status code is OK.
    content = response.read().decode('utf-8')
    response.close()
    api_response = json.loads(content)
    return [info['filename'] for info in api_response]
