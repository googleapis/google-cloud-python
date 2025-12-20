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


SERVICE_NAME="log-py-local-$(echo $ENVCTL_ID | head -c 10)"
SA_NAME=$SERVICE_NAME-invoker

destroy() {
  set +e
  # delete pubsub resources
  gcloud pubsub topics delete $SERVICE_NAME -q 2> /dev/null
  gcloud pubsub subscriptions delete $SERVICE_NAME-subscriber -q 2> /dev/null
  # stop container
  docker stop $SERVICE_NAME 2> /dev/null
  set -e
}

verify() {
  set +e
  docker container inspect -f '{{.State.Running}}' $SERVICE_NAME > /dev/null 2> /dev/null
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
  ARG=${1:-none}
  if [[ -z "${GOOGLE_APPLICATION_CREDENTIALS}" ]]; then
    echo "GOOGLE_APPLICATION_CREDENTIALS not set"
    echo "should point to a valid service account to mount into container"
    exit 1
  fi
  if [[ "$ARG" == "-i" ]]; then
    FLAG="-i"
  else
    FLAG="-d"
  fi
  build_container nopush
  docker run --rm \
    --name $SERVICE_NAME \
    -v $GOOGLE_APPLICATION_CREDENTIALS:/service-account.json \
    -e GOOGLE_APPLICATION_CREDENTIALS=/service-account.json \
    -e ENABLE_SUBSCRIBER=true -e PUBSUB_TOPIC="$SERVICE_NAME" \
    $FLAG -t $GCR_PATH
}

filter-string() {
  echo "unimplemented"
}

