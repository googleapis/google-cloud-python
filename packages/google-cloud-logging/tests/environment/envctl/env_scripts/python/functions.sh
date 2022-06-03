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


SERVICE_NAME="log-py-func-$(echo $ENVCTL_ID | head -c 10)"

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
  RUNTIME="${RUNTIME:-python38}"
  # set up deployment directory
  # copy over local copy of library
  pushd $SUPERREPO_ROOT
    tar -cvf $TMP_DIR/lib.tar --exclude tests --exclude .nox --exclude samples \
      --exclude docs --exclude __pycache__ --exclude .git --exclude .github --exclude dist .
  popd
  mkdir $TMP_DIR/python-logging
  tar -xvf $TMP_DIR/lib.tar --directory $TMP_DIR/python-logging
  # copy test scripts
  cp $REPO_ROOT/deployable/python/router.py $TMP_DIR/main.py
  cp $REPO_ROOT/deployable/python/*.py $TMP_DIR/
  echo  "-e ./python-logging" | cat $REPO_ROOT/deployable/python/requirements.txt - > $TMP_DIR/requirements.txt
  # deploy function
  pushd $TMP_DIR
    gcloud functions deploy $SERVICE_NAME \
      --entry-point pubsub_gcf \
      --trigger-topic $SERVICE_NAME \
      --runtime $RUNTIME \
      --region us-west2
  popd
}

filter-string() {
  echo "resource.type=\"cloud_function\" AND resource.labels.function_name=\"$SERVICE_NAME\""
}

