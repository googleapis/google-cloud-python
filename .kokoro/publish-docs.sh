#!/bin/bash
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# `-e` enables the script to automatically fail when a command fails
# `-o pipefail` sets the exit code to non-zero if any command fails,
# or zero if all commands in the pipeline exit successfully.
set -eo pipefail

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

export PATH="${HOME}/.local/bin:${PATH}"

# In order to determine which packages to publish, we need
# to know the difference in */gapic_version.py from the previous
# commit (HEAD~1). This assumes we use squash commit when merging PRs.
git fetch origin main --deepen=1

subdirs=(
    packages
)
RETVAL=0

export PROJECT_ROOT=$(realpath $(dirname "${BASH_SOURCE[0]}")/..)

# A file for publishing docs
publish_docs_script="${PROJECT_ROOT}/.kokoro/publish-docs-single.sh"

for subdir in ${subdirs[@]}; do
    for d in `ls -d ${subdir}/*/`; do
        should_publish=false
        echo "checking changes with 'git diff HEAD~.. ${d}/**/gapic_version.py'"
        set +e
        changed=$(git diff "HEAD~.." ${d}/**/gapic_version.py | wc -l)
        set -e
        if [[ "${changed}" -eq 0 ]]; then
            echo "no change detected in ${d}, skipping"
        else
            echo "change detected in ${d}"
            should_publish=true
        fi
        if [ "${should_publish}" = true ]; then
            echo "publishing docs in ${d}"
            pushd ${d}
            # Temporarily allow failure.
            set +e
            ${publish_docs_script}
            ret=$?
            set -e
            if [ ${ret} -ne 0 ]; then
                RETVAL=${ret}
            fi
            popd
        fi
    done
done

exit ${RETVAL}
