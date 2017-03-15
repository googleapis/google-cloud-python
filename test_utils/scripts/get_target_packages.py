# Copyright 2017 Google Inc.
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

"""Print a list of packages which require testing."""

import os
import subprocess
import warnings


CURRENT_DIR = os.path.realpath(os.path.dirname(__file__))
BASE_DIR = os.path.realpath(os.path.join(CURRENT_DIR, '..', '..'))
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'google-cloud-python')

# This is the current set of dependencies by package.
# As of this writing, the only "real" dependency is that of error_reporting
# (on logging), the rest are just system test dependencies.
PKG_DEPENDENCIES = {
    'bigquery': {'storage'},
    'error_reporting': {'logging'},
    'language': {'storage'},
    'logging': {'bigquery', 'pubsub', 'storage'},
    'speech': {'storage'},
    'vision': {'storage'},
}


def get_baseline():
    """Return the baseline commit.

    On a pull request, or on a branch, return the master tip.

    Locally, return a value pulled from environment variables, or None if
    the environment variables are not set.

    On a push to master, return None. This will effectively cause everything
    to be considered to be affected.
    """
    # If this is a pull request or branch, return the tip for master.
    # We will test only packages which have changed since that point.
    ci_non_master = os.environ.get('CI', '') == 'true' and any([
        os.environ.get('CIRCLE_BRANCH', '') != 'master',
        os.environ.get('CIRCLE_PR_NUMBER', ''),
    ])
    if ci_non_master:
        subprocess.run(['git', 'remote', 'add', 'baseline',
                        'git@github.com:GoogleCloudPlatform/%s' % GITHUB_REPO],
                        stderr=subprocess.DEVNULL)
        subprocess.run(['git', 'pull', 'baseline'], stderr=subprocess.DEVNULL)
        return 'baseline/master'

    # If environment variables are set identifying what the master tip is,
    # use that.
    if os.environ.get('GOOGLE_CLOUD_TESTING_REMOTE', ''):
        remote = os.environ['GOOGLE_CLOUD_TESTING_REMOTE']
        branch = os.environ.get('GOOGLE_CLOUD_TESTING_BRANCH', 'master')
        return '%s/%s' % (remote, branch)

    # If we are not in CI and we got this far, issue a warning.
    if not os.environ.get('CI', ''):
        warnings.warn('No baseline could be determined; this means tests '
                      'will run for every package. If this is local '
                      'development, set the $GOOGLE_CLOUD_TESTING_REMOTE '
                      'environment variable.')

    # That is all we can do; return None.
    return None


def get_changed_files():
    """Return a list of files that have been changed since the baseline.

    If there is no base, return None.
    """
    # Get the baseline, and fail quickly if there is no baseline.
    baseline = get_baseline()
    if not baseline:
        return None

    # Return a list of altered files.
    try:
        return subprocess.check_output([
            'git', 'diff', '--name-only', '%s..HEAD' % baseline,
        ], stderr=subprocess.DEVNULL).decode('utf8').strip().split('\n')
    except subprocess.CalledProcessError:
        warnings.warn('Unable to perform git diff; falling back to assuming '
                      'all packages have changed.')
        return None


def get_changed_packages(file_list):
    """Return a list of changed packages based on the provided file list.

    If the file list is None, then all packages should be considered to be
    altered.
    """
    # Determine a complete list of packages.
    all_packages = set()
    for file_ in os.listdir(BASE_DIR):
        abs_file = os.path.realpath(os.path.join(BASE_DIR, file_))
        if os.path.isdir(abs_file) and os.path.isfile('%s/nox.py' % abs_file):
            all_packages.add(file_)

    # If ther is no file list, send down the full package set.
    if file_list is None:
        return all_packages

    # Create a set based on the list of changed files.
    answer = set()
    for file_ in file_list:
        # Ignore root directory changes (setup.py, .gitignore, etc.).
        if '/' not in file_:
            continue

        # Ignore changes that are not in a package (usually this will be docs).
        package = file_.split('/')[0]
        if package not in all_packages:
            continue

        # If there is a change in core, short-circuit now and return
        # everything.
        if package == 'core':
            return all_packages

        # Add the package, as well as any dependencies this package has.
        # NOTE: For now, dependencies only go down one level.
        answer.add(package)
        answer = answer.union(PKG_DEPENDENCIES.get(package, set()))

    # We got this far without being short-circuited; return the final answer.
    return answer


if __name__ == '__main__':
    # Figure out what packages have changed.
    file_list = get_changed_files()
    for package in sorted(get_changed_packages(file_list)):
        print(package)
