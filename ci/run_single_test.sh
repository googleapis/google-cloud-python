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
# `PY_VERSION` should be one of ["3.10", "3.11", "3.12", "3.13"]

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
    mypy)
        nox -s mypy-3.14
        retval=$?
        ;;
    prerelease)
        nox -s prerelease_deps-3.14
        retval=$?
        ;;
    unit)
        case ${PY_VERSION} in
        "3.9")
            if nox --list-sessions | grep -q "unit-3.9"; then
                nox -s unit-3.9
                retval=$?
            else
                echo "Skipping unit-3.9 as it is not supported by this package."
                retval=0
            fi
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
        "3.14")
            nox -s unit-3.14
            retval=$?
            ;;
        *)
            echo "unsupported PY_VERSION"
            exit 1
            ;;
        esac
        ;;
    import_profile)
        if [ -f setup.py ] || [ -f pyproject.toml ]; then
            echo "Creating temporary virtualenv for import profile..."
            python3 -m venv .venv-profiler
            source .venv-profiler/bin/activate
            python -m pip install --upgrade pip setuptools
            
            PACKAGE_NAME=$(basename $(pwd))
            PROFILER_TEMP_DIR=$(mktemp -d)
            cp ../../scripts/import_profiler/profiler.py "${PROFILER_TEMP_DIR}/profiler.py"
            PROFILER_SCRIPT="${PROFILER_TEMP_DIR}/profiler.py"
            BASELINE_CSV="${PROFILER_TEMP_DIR}/baseline_${PACKAGE_NAME}.csv"
            
            if [ -n "${TARGET_BRANCH}" ]; then
                # Try upstream first (for forks), then origin
                BASELINE_COMMIT=$(git merge-base HEAD "upstream/${TARGET_BRANCH}" 2>/dev/null || \
                                 git merge-base HEAD "origin/${TARGET_BRANCH}" 2>/dev/null || \
                                 git merge-base HEAD "${TARGET_BRANCH}" 2>/dev/null || true)
                if [ -n "${BASELINE_COMMIT}" ]; then
                    echo "Checking out baseline commit ${BASELINE_COMMIT} in a temporary worktree..."
                    REPO_PREFIX=$(git rev-parse --show-prefix)
                    WORKTREE_DIR=$(mktemp -d)
                    rmdir "${WORKTREE_DIR}"
                    if git worktree add "${WORKTREE_DIR}" "${BASELINE_COMMIT}" 2>/dev/null; then
                        (
                            cd "${WORKTREE_DIR}/${REPO_PREFIX}"
                            if [ -f setup.py ] || [ -f pyproject.toml ]; then
                                pip install -e .
                                python "${PROFILER_SCRIPT}" --package "${PACKAGE_NAME}" --iterations 11 --csv "${BASELINE_CSV}"
                            fi
                        )
                        git worktree remove -f "${WORKTREE_DIR}"
                    else
                        echo "Failed to create git worktree for baseline. Skipping baseline generation."
                    fi
                else
                    echo "Could not find baseline commit for ${TARGET_BRANCH:-main}. Skipping baseline generation."
                fi
            fi
            
            pip install -e .
            
            if [ -f "${BASELINE_CSV}" ]; then
                python ${PROFILER_SCRIPT} --package ${PACKAGE_NAME} --iterations 11 --fail-threshold 5000 --diff-baseline "${BASELINE_CSV}" --diff-threshold 100
            else
                python ${PROFILER_SCRIPT} --package ${PACKAGE_NAME} --iterations 11 --fail-threshold 5000
            fi
            retval=$?
            deactivate
            rm -rf .venv-profiler
            rm -rf "${PROFILER_TEMP_DIR}"
        else
            echo "Skipping import_profile as this does not appear to be a Python package (no setup.py or pyproject.toml)."
            retval=0
        fi
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
