#!/bin/bash
# Copyright 2022 Google LLC
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


SERVICE_NAME="logging-java-func-$(echo $ENVCTL_ID | head -c 10)"\

destroy() {
  set +e
  # delete pubsub resources
  gcloud pubsub topics delete $SERVICE_NAME -q  2> /dev/null
  gcloud pubsub subscriptions delete $SERVICE_NAME-subscriber -q  2> /dev/null
  # delete service
  gcloud functions delete $SERVICE_NAME --region us-west2 -q ${EXTRA_FUNCTIONS_FLAGS-} 2> /dev/null
  set -e
}

verify() {
  set +e
  gcloud functions describe $SERVICE_NAME --region us-west2 ${EXTRA_FUNCTIONS_FLAGS-} > /dev/null
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
  # available runtimes on Jun'22 are Java 11 (java11) and Java 17 (java17)
  # use java11 since it is closest to LTS Java runtime (Java 9)
  RUNTIME="${RUNTIME:-java17}"

  # create pub/sub topic
  set +e
  gcloud pubsub topics create $SERVICE_NAME 2>/dev/null
  set -e

  # use custom cloud functions Dockerfile
  export ENV_TEST_DOCKERFILE=Dockerfile.cloudfunctions
  # extract container
  build_container nopush
  id=$(docker create $GCR_PATH)
  docker cp $id:/app/target/deployable-1.0.0.jar $TMP_DIR/deployable-1.0.0.jar
  docker rm -v $id
  ls $TMP_DIR

  # deploy
  pushd $TMP_DIR
  gcloud functions deploy $SERVICE_NAME \
    --entry-point envtest.deployable.CloudFunctionTrigger \
    --source $TMP_DIR \
    --memory 512MB \
    --trigger-topic $SERVICE_NAME \
    --runtime $RUNTIME \
    --region us-west2 \
    ${EXTRA_FUNCTIONS_FLAGS-}
  popd

}

filter-string() {
  echo "resource.type=\"cloud_function\" AND resource.labels.module_id=\"$SERVICE_NAME\""
}



