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


SERVICE_NAME="logging-py-standard-$(echo $ENVCTL_ID | head -c 10)"\

destroy() {
  set +e
  # delete pubsub resources
  gcloud pubsub topics delete $SERVICE_NAME -q 2> /dev/null
  gcloud pubsub subscriptions delete $SERVICE_NAME-subscriber -q 2> /dev/null
  # delete service
  gcloud app services delete $SERVICE_NAME -q 2> /dev/null
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
  # set up deployment directory
  # copy over local copy of library
  pushd $SUPERREPO_ROOT
    tar -cvf $TMP_DIR/lib.tar --exclude tests --exclude .nox --exclude samples --exclude docs --exclude __pycache__ .
  popd
  mkdir $TMP_DIR/python-logging
  tar -xvf $TMP_DIR/lib.tar --directory $TMP_DIR/python-logging
  # copy test scripts
  cp $REPO_ROOT/deployable/python/*.py $TMP_DIR
  echo  $'\n-e ./python-logging' | cat $REPO_ROOT/deployable/python/requirements.txt - > $TMP_DIR/requirements.txt
  # build app.yaml
  cat <<EOF > $TMP_DIR/app.yaml
    runtime: python37
    service: $SERVICE_NAME
    entrypoint: python router.py
    manual_scaling:
      instances: 1
    env_variables:
      ENABLE_SUBSCRIBER: "true"
      PUBSUB_TOPIC: $SERVICE_NAME
EOF
  # deploy
  pushd $TMP_DIR
    gcloud app deploy -q
  popd
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
  echo "resource.type=\"gae_app\" AND resource.labels.module_id=\"$SERVICE_NAME\""
}



