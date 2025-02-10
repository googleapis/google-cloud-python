#!/bin/bash
#
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script requires the following environment variables to be set:
# `TEST_TYPE` should be one of ["lint", "lint_setup_py", "docs", "docfx", "prerelease"]
# `PY_VERSION` should be one of ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]

# This script is called by the `ci/run_conditional_tests.sh` script.
# A specific `nox` session will be run, depending on the value of 
# `TEST_TYPE` and `PY_VERSION`. For example, if `TEST_TYPE` is
# `lint`, the `nox -s lint` session will be run.


set -e

if [ -z "${TEST_TYPE}" ]; then
    echo "missing TEST_TYPE env var"
    exit 1
fi

if [ -z "${PY_VERSION}" ]; then
    echo "missing PY_VERSION env var"
    exit 1
fi

# Don't fail on errors so we can capture all of the output
set +e

case ${TEST_TYPE} in
    docs)
        nox -s docs
        # This line needs to be directly after `nox -s docs` in order
        # for the failure to appear in Github presubmits
        retval=$?
        # Clean up built docs and python cache after the build process to avoid
        # `[Errno 28] No space left on device`
        # See https://github.com/googleapis/google-cloud-python/issues/12271
        rm -rf docs/_build
        ;;
    docfx)
        nox -s docfx
        # This line needs to be directly after `nox -s docfx` in order
        # for the failure to appear in Github presubmits
        retval=$?
        # Clean up built docs and python cache after the build process to avoid
        # `[Errno 28] No space left on device`
        # See https://github.com/googleapis/google-cloud-python/issues/12271
        rm -rf docs/_build
        ;;
    prerelease)
        nox -s prerelease_deps-3.13
        retval=$?
        ;;
    unit)
        case ${PY_VERSION} in
        "3.7")
            nox -s unit-3.7
            retval=$?
            ;;
        "3.8")
            nox -s unit-3.8
            retval=$?
            ;;
        "3.9")
            nox -s unit-3.9
            retval=$?
            ;;
        "3.10")
            nox -s unit-3.10
            retval=$?
            ;;
        "3.11")
            nox -s unit-3.11
            retval=$?
            ;;
        "3.12")
            nox -s unit-3.12
            retval=$?
            ;;
        "3.13")
            nox -s unit-3.13
            retval=$?
            ;;
        *)
            echo "unsupported PY_VERSION"
            exit 1
            ;;
        esac
        ;;
    *)
        nox -s ${TEST_TYPE}
        retval=$?
        ;;
    esac

# Clean up `__pycache__` and `.nox` directories to avoid error
# `No space left on device` seen when running tests in Github Actions
find . | grep -E "(__pycache__)" | xargs rm -rf
rm -rf .nox

exit ${retval}
