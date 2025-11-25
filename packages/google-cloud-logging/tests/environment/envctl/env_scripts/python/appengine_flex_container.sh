#!/bin/bash
# Copyright 2021 Google LLC
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

set -e # exit on any failure
set -o pipefail # any step in pipe caused failure
set -u # undefined variables cause exit


SERVICE_NAME="log-py-flex-con-$(echo $ENVCTL_ID | head -c 10)"

destroy() {
  set +e
  # delete pubsub resources
  gcloud pubsub topics delete $SERVICE_NAME -q 2> /dev/null
  gcloud pubsub subscriptions delete $SERVICE_NAME-subscriber -q 2> /dev/null
  # delete container images
  export GCR_PATH=gcr.io/$PROJECT_ID/logging:$SERVICE_NAME
  gcloud container images delete $GCR_PATH -q --force-delete-tags 2> /dev/null
  # delete service
  gcloud app services delete $SERVICE_NAME -q
  set -e
}

verify() {
  set +e
  gcloud app services describe $SERVICE_NAME -q > /dev/null 2> /dev/null
  if [[ $? == 0 ]]; then
     echo "TRUE"
     exit 0
   else
     echo "FALSE"
     exit 1
  fi
  set -e
}


deploy() {
  # create pub/sub topic
  set +e
  gcloud pubsub topics create $SERVICE_NAME 2>/dev/null
  set -e

  build_container

  cat <<EOF > $TMP_DIR/app.yaml
  runtime: custom
  service: $SERVICE_NAME
  env: flex
  manual_scaling:
    instances: 1
  env_variables:
    ENABLE_SUBSCRIBER: "true"
    PUBSUB_TOPIC: $SERVICE_NAME
EOF

  # deploy
  pushd $TMP_DIR
    gcloud app deploy --image-url $GCR_PATH -q
  popd
}

filter-string() {
  echo "resource.type=\"gae_app\" AND resource.labels.module_id=\"$SERVICE_NAME\""
}


