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

SERVICE_NAME="log-go-func-$(echo $ENVCTL_ID | head -c 8)x"
LIBRARY_NAME="google-cloud-go"

destroy() {
  set +e
  # delete pubsub resources
  gcloud pubsub topics delete $SERVICE_NAME -q  2> /dev/null
  gcloud pubsub subscriptions delete $SERVICE_NAME-subscriber -q  2> /dev/null
  # delete service
  gcloud functions delete $SERVICE_NAME --region us-west2 -q  2> /dev/null
  set -e
}

verify() {
  set +e
  gcloud functions describe $SERVICE_NAME --region us-west2
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
  # Note: functions only supports go111 and go113 at the moment
  local RUNTIME="go113"
  
  # Copy over local copy of library to use as dependency
  _deployable_dir=$REPO_ROOT/deployable/$LANGUAGE
  pushd $SUPERREPO_ROOT
    tar -cvf $_deployable_dir/lib.tar --exclude internal/logging --exclude .nox --exclude docs --exclude __pycache__ .
  popd
  mkdir -p $_deployable_dir/google-cloud-go
  tar -xvf $_deployable_dir/lib.tar --directory $_deployable_dir/google-cloud-go
  
  # Create vendor folder based on local dependency
  pushd $REPO_ROOT/deployable/go
    go mod vendor
  popd

  # move code into a temp directory used to deploy the cloud function
  cp -rf $REPO_ROOT/deployable/go/vendor $TMP_DIR/vendor
  
  # Renames package as Cloud Functions cannot be 'main' packages. 
  sed 's/package main.*/package function/g' $REPO_ROOT/deployable/go/main.go > $TMP_DIR/main.go 

  # clean up vendor folder
  pushd $REPO_ROOT/deployable/go
    rm -rf vendor/
  popd

  # deploy function
  pushd $TMP_DIR
    gcloud functions deploy $SERVICE_NAME \
      --entry-point PubsubFunction \
      --trigger-topic $SERVICE_NAME \
      --runtime $RUNTIME \
      --region us-west2
  popd
}

filter-string() {
  echo "resource.type=\"cloud_function\" AND resource.labels.function_name=\"$SERVICE_NAME\""
}
