#!/bin/bash
# Copyright 2023 Google LLC
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

set -e -o pipefail
set -x

# Replace the docs version by the desired commit
BIGFRAMES_DOCS_VERSION=8ce2a3e

BIGFRAMES_FIREBASE_PROJECT=bigframes-dev-d4d9a
BIGFRAMES_DOCS_GCS_BUCKET=bigframes-docs

BIGFRAMES_DOCS_DIR=`mktemp -d`


# Install firebase if not already installed
if ! which firebase; then
    npm install -g firebase-tools
fi

# Prepare a working directory for firebase
mkdir -p ${BIGFRAMES_DOCS_DIR}
pushd ${BIGFRAMES_DOCS_DIR}

# Copy the bigframes version
if [ ! -d ${BIGFRAMES_DOCS_VERSION} ]; then
    gsutil -m cp -r gs://${BIGFRAMES_DOCS_GCS_BUCKET}/${BIGFRAMES_DOCS_VERSION} .
fi

rm -f latest
ln -s ${BIGFRAMES_DOCS_VERSION} latest

# Set up firebase
firebase login --no-localhost
firebase init hosting

versions="${BIGFRAMES_DOCS_VERSION} latest"
for version in ${versions}; do
    site_name=bigframes-docs-${version}
    if ! firebase hosting:sites:list | grep ${site_name}; then
        firebase hosting:sites:create ${site_name}
    fi

    firebase target:apply hosting ${version} ${site_name}
done

# Make sure the firebase json config is consistent with ${versions}
# TODO(shobs): Come up with a better way of updating the config than
# a hard overwrite
cat > firebase.json << EOF
{
  "hosting": [
        {
          "target": "latest",
          "public": "latest",
          "ignore": [
                "firebase.json",
                "**/.*",
                "**/node_modules/**"
          ]
        }
        ,
        {
          "target": "${BIGFRAMES_DOCS_VERSION}",
          "public": "${BIGFRAMES_DOCS_VERSION}",
          "ignore": [
                "firebase.json",
                "**/.*",
                "**/node_modules/**"
          ]
        }
  ]
}
EOF

# Verify that the intended sites look good
for version in ${versions}; do
    echo "Preview the local hosting of the docs site \"${version}\" before actually deploying (Press Ctrl+C to stop)"
    firebase serve --only hosting:${version}
done

echo -n "Go ahead and deploy? [y/N]: "
read deploy_consent

# Deploy the sites
if [ "$deploy_consent" = y ]; then
    echo "Deploying ..."
    firebase deploy --only hosting
else
    echo "Not Deploying anything."
fi

popd
