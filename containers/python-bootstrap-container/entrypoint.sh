#!/bin/bash 
# Copyright 2022 Google LLC
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
set -e

function save_to_temp_then_file() {
    TEMP_FILE="$(echo mktemp)"
    # Redirect output to temporary file TEMP_FILE
    cat > TEMP_FILE
    # Replace the original file
    mv -f TEMP_FILE "${1}"
}


MONO_REPO_NAME="google-cloud-python"
WORKSPACE_DIR="/workspace"
PATH_TO_CONTAINER_VARS="$WORKSPACE_DIR/interContainerVars.json"

cd "$WORKSPACE_DIR/$MONO_REPO_NAME/containers/python-bootstrap-container"

# API_ID has the form google.cloud.*.vX or `google.*.*.vX`
# Get the version of the API (the value after the last `.`)
# For example, the `API_VERSION` for `google.cloud.workflows.v1`
# will be `v1`
API_VERSION="$(echo $API_ID | sed 's/.*\.//')"

# API_ID has the form google.cloud.*.vX or `google.*.*.vX`
# Replace `.`` with `-`
FOLDER_NAME="$(echo $API_ID | sed -E 's/\./-/g')"

# if API_VERSION does not contain numbers, set API_VERSION to empty string
if [[ ! $API_VERSION =~ [0-9] ]]; then
    API_VERSION=""
else
    # Remove the trailing version from the FOLDER_NAME`
    # for `google.cloud.workflows.v1`
    # the folder should be `google-cloud-workflows`
    FOLDER_NAME="$(echo $FOLDER_NAME | sed 's/-[^-]*$//')"
fi

# Create the folder
mkdir -p "$WORKSPACE_DIR/$MONO_REPO_NAME/packages/$FOLDER_NAME"

# This is the path to the .OwlBot.yaml that will 
# be used by the bootstrapping container
PATH_TO_YAML="packages/$FOLDER_NAME/.OwlBot.yaml"

# Write the Path to .OwlBot.yaml in the interContainerVars.json folder
jq --arg PATH_TO_YAML "$PATH_TO_YAML" '. += {"owlbotYamlPath": $PATH_TO_YAML}' $PATH_TO_CONTAINER_VARS | save_to_temp_then_file $PATH_TO_CONTAINER_VARS

# If API_VERSION is empty
if [[ -z $API_VERSION ]]; then
    # Copy the templated .OwlBot_Without_Version.yaml
    cp ".OwlBot_Without_Version.yaml" "${WORKSPACE_DIR}/${MONO_REPO_NAME}/packages/${FOLDER_NAME}/.OwlBot.yaml"
else
    # Otherwise copy the templated .OwlBot.yaml
    cp ".OwlBot.yaml" "${WORKSPACE_DIR}/${MONO_REPO_NAME}/packages/${FOLDER_NAME}/.OwlBot.yaml"
fi

API_PATH="$(echo $FOLDER_NAME | sed -E 's/\-/\//g')"

# Update apiPath in .OwlBot.yaml 
sed -i -e "s|apiPath|$API_PATH|" "${WORKSPACE_DIR}/${MONO_REPO_NAME}/packages/${FOLDER_NAME}/.OwlBot.yaml"

# Update apiPathDashes in .OwlBot.yaml 
sed -i -e "s|apiDashes|$FOLDER_NAME|" "${WORKSPACE_DIR}/${MONO_REPO_NAME}/packages/${FOLDER_NAME}/.OwlBot.yaml"

# Copy the templated .repo-metadata.json
cp ".repo-metadata.json" "${WORKSPACE_DIR}/${MONO_REPO_NAME}/packages/${FOLDER_NAME}/.repo-metadata.json"

# Get the API shortname
# API_PATH has the form google/cloud/*/vX or `google/*/*/vX`
# We want the API shortname which is right before the version
# For example, the `API_SHORTNAME`` for `google.cloud.workflows.v1`
# is workflows
API_SHORTNAME="$(echo $API_PATH | sed 's:.*/::')"

# Update apiName in .repo-metadata.json
sed -i -e "s|apiName|$API_SHORTNAME|" "${WORKSPACE_DIR}/${MONO_REPO_NAME}/packages/${FOLDER_NAME}/.repo-metadata.json"

# Get the "display_name" field from apis.json (DRIFT)
DISPLAY_NAME=$(jq --arg API_SHORTNAME "$API_SHORTNAME" -r '.apis | to_entries[] | select(.value.api_shortname==$API_SHORTNAME) | .value.display_name' apis.json)

# Update apiPrettyName in .repo-metadata.json
sed -i -e "s|apiPrettyName|$DISPLAY_NAME|" "${WORKSPACE_DIR}/${MONO_REPO_NAME}/packages/${FOLDER_NAME}/.repo-metadata.json"

# Get the "docs_root_url" field from apis.json (DRIFT)
DOCS_ROOT_URL=$(jq --arg API_SHORTNAME "$API_SHORTNAME" -r '.apis | to_entries[] | select(.value.api_shortname==$API_SHORTNAME) | .value.docs_root_url' apis.json)

# Build the docs URL if DOCS_ROOT_URL is not empty
# If API_VERSION is empty
if [[ -n $DOCS_ROOT_URL ]]; then
    DOCS_URL="$(echo https://$DOCS_ROOT_URL)"
else
    DOCS_URL=""
fi

# Update apiProductDocumentation in .repo-metadata.json
sed -i -e "s|apiProductDocumentation|$DOCS_URL|" "${WORKSPACE_DIR}/${MONO_REPO_NAME}/packages/${FOLDER_NAME}/.repo-metadata.json"

# Update apiPackage in .repo-metadata.json
sed -i -e "s|apiPackage|$FOLDER_NAME|" "${WORKSPACE_DIR}/${MONO_REPO_NAME}/packages/${FOLDER_NAME}/.repo-metadata.json"

# If API_VERSION is not empty
if [[ -n $API_VERSION ]]; then
    # Update apiVersion in .repo-metadata.json
    sed -i -e "s|apiVersion|$API_VERSION|" "${WORKSPACE_DIR}/${MONO_REPO_NAME}/packages/${FOLDER_NAME}/.repo-metadata.json"
fi
