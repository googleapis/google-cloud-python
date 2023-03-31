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

# This script was written as part of a project to migrate
# split repositories to a mono repository google-cloud-python.
#
# This script will update the various metadata files migrated from the split
# repo into formats and locations suitable for the monorepo.
#
# Pre-condition: the split repo has been copied to the path indicated when
# calling this function.
#
# Invocation:
#   split-repo-post-process.sh PACKAGE_PATH
# where PACKAGE_PATH is the path (absolute or relative) from pwd to the
# directory in google-cloud-python holding the copied split repo. Typically, if
# running from the top level of google-cloud-python, this is something like
# "packages/google-cloud-APINAME"
# Example from the root directory of the monorepo:
#   split-repo-post-process.sh packages/google-cloud-speech
#
# For debugging/developing this script, you can have additional parameters:
#  ./split-repo-post-process.sh SPLIT_REPO_DIR MONOREPO_DIR MONOREPO_PACKAGE_NAME
# Example from this script's directory:
#  ./split-repo-post-process.sh ../../../python-speech ../../ google-cloud-speech

# `-e` enables the script to automatically fail when a command fails
set -e

NOP="echo -e ''"
DEBUG="yes"  # set to blank for a real run

[[ -n ${DEBUG} ]] && {
  # Comment out some commands for development/debugging
  RM='echo "*** would run:" rm'
  GIT='echo "*** would run:" git'

  # It's easier to debug if keys don't get reordered
  SORT_JSON_KEYS="" 
} || {
  # Real commands for actual runs
  RM='rm'
  GIT='git'

  # Sort keys for easier look-up.
  SORT_JSON_KEYS="--sort-keys"
}

if [ $# -lt 1 ]
then
  echo "Usage: $0 <path to copied split-repo>"
  exit 1
fi

# variable naming convention
#   PATH_* are absolute system paths
#   MONOREPO_PATH_* are paths relative to the root of the monorepo
#   MONOREPO_* are values used in the monorepo

PATH_PACKAGE="$(realpath "$1")"

# optional second argument is useful for development.
PATH_MONOREPO="${2:-$(dirname $(dirname $PATH_PACKAGE))}"
PATH_MONOREPO="$(realpath "${PATH_MONOREPO}")"

# optional third argument is useful for development.
MONOREPO_PACKAGE_NAME="${3:-$(basename ${PATH_PACKAGE})}"

MONOREPO_PATH_PACKAGE="packages/${MONOREPO_PACKAGE_NAME}"

cat <<EOF
Post-processing ${MONOREPO_PACKAGE_NAME}
  PATH_PACKAGE:          ${PATH_PACKAGE}
  PATH_MONOREPO:         ${PATH_MONOREPO}
  MONOREPO_PACKAGE_NAME: ${MONOREPO_PACKAGE_NAME}
  MONOREPO_PATH_PACKAGE: ${MONOREPO_PATH_PACKAGE}
EOF

pushd "${PATH_MONOREPO}" >& /dev/null

## START release-please config migration ########################################
# variable prefix: RPC_*

RPC_MONO_PATH="release-please-config.json"
echo "Migrating: ${RPC_MONO_PATH}"

# enable this if we want sorted keys. Keep it disabled to append new entries at
# the end (useful for debugging):
RPC_SORT_KEYS="${SORT_JSON_KEYS}"

RPC_SPLIT_PATH="${PATH_PACKAGE}/release-please-config.json"
RPC_NEW_OBJECT="$(jq '.packages."."' "${RPC_SPLIT_PATH}")"

jq ${RPC_SORT_KEYS} --argjson newObject "${RPC_NEW_OBJECT}" ". * {\"packages\": {\"${MONOREPO_PATH_PACKAGE}\": \$newObject}}" ${RPC_MONO_PATH} | sponge ${RPC_MONO_PATH}
$RM ${RPC_SPLIT_PATH}

## END release-please config migration

## START release-please manifest migration ########################################
# variable prefix: RPM_*
RPM_MONO_PATH=".release-please-manifest.json"
echo "Migrating: ${RPM_MONO_PATH}"

# enable this if we want sorted keys. Keep it disabled to append new entries at
# the end (useful for debugging):
RPM_SORT_KEYS="${SORT_JSON_KEYS}"

RPM_SPLIT_PATH="${PATH_PACKAGE}/.release-please-manifest.json"
RPM_VERSION="$(jq '."."' "${RPM_SPLIT_PATH}")"
jq ${RPM_SORT_KEYS}  ". * {\"${MONOREPO_PATH_PACKAGE}\": ${RPM_VERSION}}" ${RPM_MONO_PATH} | sponge ${RPM_MONO_PATH}
$RM ${RPM_SPLIT_PATH}

## END release-please manifest migration


## START owlbot.yaml migration ########################################
# variable prefix: OWY_*
OWY_MONO_PATH="${MONOREPO_PATH_PACKAGE}/.OwlBot.yaml"
echo "Migrating: ${OWY_MONO_PATH}"
mkdir -p $(dirname ${OWY_MONO_PATH})

OWY_SPLIT_PATH="${PATH_PACKAGE}/.github/.OwlBot.yaml"
cp ${OWY_SPLIT_PATH} ${OWY_MONO_PATH}

# remove `docker:` line
sed -i "/docker:/d" "${OWY_MONO_PATH}"
# remove `image:` line
sed -i "/image:/d" "${OWY_MONO_PATH}"

# In the nodejs case, lines #1 and #2 below are treated as a disjoint case from
# line #3. However, in Python we see cases (eg aiplatform) where there are
# multiple entries in the same file that satisfy either of the criteria. As a
# result, we search for both cases. In doing that, to prevent #3 from altering
# lines already modified by #2, we temporarily insert ${TMP_MARKER} and remove
# it in #4
TMP_MARKER="<<__tmp__>>>"
sed -i 's|\.\*-py/(.*)|.*-py|' "${OWY_MONO_PATH}"   #1
sed -i "s|dest: /owl-bot-staging/\$1/\$2|dest: /owl-bot-${TMP_MARKER}staging/${MONOREPO_PACKAGE_NAME}/\$1|" "${OWY_MONO_PATH}" #2
sed -i "s|dest: /owl-bot-staging|dest: \/owl-bot-staging\/${MONOREPO_PACKAGE_NAME}/|" "${OWY_MONO_PATH}" #3
sed -i "s|${TMP_MARKER}||" "${OWY_MONO_PATH}"  #4

# TODO: Review the following: For consistency with NodeJS migration script:
# - we are not removing `begin-after-commit-hash`
# - we are not removing `deep-remove-regex`, even though it refers to a non-API-specific directory.

$RM ${OWY_SPLIT_PATH}
## END owlbot.yaml migration


## START owlbot.py migration ########################################
# variable prefix: OWP_*
OWP_MONO_PATH="${MONOREPO_PATH_PACKAGE}/owlbot.py"
echo "Migrating: ${OWP_MONO_PATH}"

OWP_SPLIT_PATH="${PATH_PACKAGE}/owlbot.py"
cp ${OWP_SPLIT_PATH} ${OWP_MONO_PATH}  # only needed for dev runs

[[ -f "${OWP_MONO_PATH}" ]] && {
  sed -i "s|import synthtool.languages.python as python|import synthtool.languages.python_mono_repo as python|" "${OWP_MONO_PATH}"
  sed -i "s|from synthtool.languages import python|from synthtool.languages import python_mono_repo as python|" "${OWP_MONO_PATH}"
  sed -i "s|python.owlbot_main(|python.owlbot_main(package_dir=\"${MONOREPO_PATH_PACKAGE}\",|" "${OWP_MONO_PATH}"
  # FIXME: owlbot.py makes freqent use of synthtool.languages.python.py_samples, but there is no py_samples in synthtool.languages.python_mono_repo
} || { $NOP ;}

## END owlbot.py migration

## START .repo-metadata.json migration ########################################
# variable prefix: RMJ_*
RMJ_MONO_PATH="${MONOREPO_PATH_PACKAGE}/.repo-metadata.json"
echo "Migrating: ${RMJ_MONO_PATH}"

RMJ_SPLIT_PATH="${PATH_PACKAGE}/.repo-metadata.json"
cp ${RMJ_SPLIT_PATH} ${RMJ_MONO_PATH}  # only needed for dev runs

jq '.repo = "googleapis/google-cloud-python"' ${RMJ_MONO_PATH} | sponge ${RMJ_MONO_PATH}
jq -r ".issue_tracker" "${RMJ_MONO_PATH}" | grep -q "github.com"  && {
  jq '.issue_tracker = "https://github.com/googleapis/google-cloud-python/issues"' ${RMJ_MONO_PATH} | sponge ${RMJ_MONO_PATH}
} || { $NOP ; }

## END .repo-metadata.json migration


## START .pre-commit-config migration ########################################
# variable prefix: PCC_*
PCC_MONO_PATH=".pre-commit-config.yaml"
echo "Migrating: ${PCC_MONO_PATH}"

PCC_SPLIT_PATH="${PATH_PACKAGE}/.pre-commit-config.yaml"

[[ ! -f "${PCC_MONO_PATH}" ]] && [[ -f "${PCC_SPLIT_PATH}" ]] && {
  cp ${PCC_SPLIT_PATH} ${PCC_MONO_PATH}
} || { $NOP ; }
$RM -f ${PCC_SPLIT_PATH}
## END .pre-commit-config migration


## FIXME: Do we need to do anything for testing?

## START run pre-processor #############################################
PPR="${PATH_PACKAGE}/owlbot.py"
[[ ! -f "${PPR}" ]] && {
   IMAGE="gcr.io/cloud-devrel-public-resources/owlbot-python-mono-repo:latest"
   read -r -d '' MESSAGE <<EOF
WARNING: ${PPR} not present.
Consider generating the image "${IMAGE}" by running the following:

  docker pull "${IMAGE}"
  docker run --rm \\
    --user $(id -u):$(id -g) \\
    -v $(pwd):/workspace/google-cloud-python \\
    -w /workspace/google-cloud-python \\
    -e "DEFAULT_BRANCH=main" \\
    "${IMAGE}"
EOF
 } || { $NOP ; }
 
## END run pre-processor

## START commit changes #############################################
echo "Committing changes locally"
${GIT} add .
${GIT} commit -am "build: ${MONOREPO_PACKAGE_NAME} migration: adjust metadata and automation configs"
## END commit changes

popd >& /dev/null # "${PATH_MONOREPO}"

[[ -z ${MESSAGE} ]] && echo "Done." || echo -e "Done, with a message:\n\n${MESSAGE}\n"



