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

SERVICE_NAME="log-node-gce-$(echo $ENVCTL_ID | head -c 8)"
ZONE="us-west2-a"
LIBRARY_NAME="nodejs-logging"

destroy() {
  set +e
  # delete pubsub resources
  gcloud pubsub topics delete $SERVICE_NAME -q 2> /dev/null
  gcloud pubsub subscriptions delete $SERVICE_NAME-subscriber -q 2> /dev/null
  # delete container images
  export GCR_PATH=gcr.io/$PROJECT_ID/logging:$SERVICE_NAME
  gcloud container images delete $GCR_PATH -q --force-delete-tags 2> /dev/null
  # delete service
  gcloud compute instances delete $SERVICE_NAME -q
  set -e
}

verify() {
  set +e
  gcloud compute instances describe $SERVICE_NAME > /dev/null 2> /dev/null
  if [[ $? == 0 ]]; then
     echo "TRUE"
     exit 0
   else
     echo "FALSE"
     exit 1
  fi
  set -e
}


build_node_container() {
  export GCR_PATH=gcr.io/$PROJECT_ID/logging:$SERVICE_NAME
  # copy super-repo into deployable dir
  _env_tests_relative_path=${REPO_ROOT#"$SUPERREPO_ROOT/"}
  _deployable_dir=$REPO_ROOT/deployable/$LANGUAGE

  # copy over local copy of library
  pushd $SUPERREPO_ROOT
      tar -cvf $_deployable_dir/lib.tar --exclude node_modules --exclude env-tests-logging --exclude test --exclude system-test --exclude .nox --exclude samples --exclude docs .
  popd
  mkdir -p $_deployable_dir/$LIBRARY_NAME
  tar -xvf $_deployable_dir/lib.tar --directory $_deployable_dir/$LIBRARY_NAME
  # build container
  docker build -t $GCR_PATH $_deployable_dir
  docker push $GCR_PATH
}

deploy() {
  build_node_container
  gcloud config set compute/zone $ZONE
  gcloud compute instances create-with-container \
    $SERVICE_NAME \
    --container-image $GCR_PATH \
    --container-env PUBSUB_TOPIC="$SERVICE_NAME",ENABLE_SUBSCRIBER="true"
  # wait for the pub/sub subscriber to start
  NUM_SUBSCRIBERS=0
  TRIES=0
  while [[ "${NUM_SUBSCRIBERS}" -lt 1 && "${TRIES}" -lt 10 ]]; do
    sleep 30
    NUM_SUBSCRIBERS=$(gcloud pubsub topics list-subscriptions $SERVICE_NAME 2> /dev/null | wc -l)
    TRIES=$((TRIES + 1))
  done

}

filter-string() {
  #INSTANCE_ID=$(gcloud compute instances list --filter="name~^$SERVICE_NAME$" --format="value(ID)")
  #echo "resource.type=\"gce_instance\" AND resource.labels.instance_id=\"$INSTANCE_ID\""
  echo "resource.type=\"global\""
}

