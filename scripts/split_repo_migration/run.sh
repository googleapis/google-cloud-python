#!/bin/bash
# Copyright 2023 Google LLC
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
 
set -e
 
if [ $# -lt 2 ]
then
  echo "Usage: $0 <split-repo-name> <target-path>"
  exit 1
fi
 
# repo name (e.g. nodejs-asset)
SPLIT_REPO=$1
# destination directory (e.g. google-cloud-asset)
ARTIFACT_NAME=$2
 
## Get the directory of the build script
SCRIPT_DIR=$(realpath $(dirname "${BASH_SOURCE[0]}"))
 
#export UPDATE_SCRIPT="${SCRIPT_DIR}/split-repo-post-process.sh"
export PACKAGE_PATH="packages/${ARTIFACT_NAME}"
 
# Args to migrate git
# 1. source GitHub repository. format: <owner>/<repo>
# 2. destination GitHub repository. format: <owner>/<repo>
# 3. path in the source repo to copy code from. Defaults to the root directory
# 4. path in the target repo to put the copied code
# 5. comma-separated list of files/folders to skip
# 6. keep these specific files that would otherwise be deleted by IGNORE_FOLDERS
# 7. override the HEAD branch name for the migration PR
# 8. path for update script.

echo ${PACKAGE_PATH}

# run the migrate script, remove .kokoro and .github folders
# keep the .github/.OwlBot.yaml config
${SCRIPT_DIR}/git-migrate-history.sh \
  "googleapis/${SPLIT_REPO}" \
  "googleapis/google-cloud-python" \
  "" \
  "${PACKAGE_PATH}" \
  "" \
  ".github/.OwlBot.yaml"
