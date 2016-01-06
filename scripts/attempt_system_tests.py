# Copyright 2016 Google Inc. All rights reserved.
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

"""Attempt to run system tests.

If the system tests are being run on Travis, no test need be run if
the build is for a PR and not a merged commit.

If being run as part of a Travis build for a merged commit, the
encrypted `key.json` file need be decrypted before running tests.
"""


from system_tests.run_system_test import run_module_tests


MODULES = (
    'datastore',
    'storage',
    'pubsub',
    'bigquery',
)


def main():
    """Run all the system tests.

    Uses module objects to directly load test cases.
    """
    for module in MODULES:
        run_module_tests(module)


if __name__ == '__main__':
    main()
