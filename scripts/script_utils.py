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
    """
    return os.getenv(TRAVIS_BRANCH_ENV)
