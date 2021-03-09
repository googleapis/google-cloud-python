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

# Note: there is a max character count constraint
SERVICE_NAME="log-go-run-$(echo $ENVCTL_ID | head -c 8)x"
SA_NAME=$SERVICE_NAME-invoker
LIBRARY_NAME="google-cloud-go"

add_service_accounts() {
  set +e
  local PROJECT_ID=$(gcloud config list --format 'value(core.project)')
  local PROJECT_NUMBER=$(gcloud projects list --filter=$PROJECT_ID --format="value(PROJECT_NUMBER)")
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com \
     --role=roles/iam.serviceAccountTokenCreator 2> /dev/null
  gcloud iam service-accounts create $SA_NAME \
     --display-name "Pub/Sub Invoker" 2> /dev/null
  gcloud run services add-iam-policy-binding  $SERVICE_NAME \
     --member=serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com \
     --role=roles/run.invoker 2> /dev/null
  RUN_URL=$(gcloud run services list --filter=$SERVICE_NAME --format="value(URL)")
  gcloud pubsub subscriptions create $SERVICE_NAME-subscriber --topic $SERVICE_NAME \
    --push-endpoint=$RUN_URL \
    --push-auth-service-account=$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com 2> /dev/null
  set -e
}

build_go_container() {
  export GCR_PATH=gcr.io/$PROJECT_ID/logging:$SERVICE_NAME
  # copy super-repo into deployable dir
  _env_tests_relative_path=${REPO_ROOT#"$SUPERREPO_ROOT/"}
  _deployable_dir=$REPO_ROOT/deployable/$LANGUAGE

  # copy over local copy of library
  pushd $SUPERREPO_ROOT
    tar -cvf $_deployable_dir/lib.tar --exclude internal/logging --exclude .nox --exclude docs --exclude __pycache__ .
  popd
  mkdir -p $_deployable_dir/$LIBRARY_NAME
  tar -xvf $_deployable_dir/lib.tar --directory $_deployable_dir/$LIBRARY_NAME
  # build container
  docker build -t $GCR_PATH $_deployable_dir
  docker push $GCR_PATH
}

deploy() {
    build_go_container
    
    gcloud config set run/platform managed
    gcloud config set run/region us-west1
    gcloud run deploy  \
        --allow-unauthenticated \
        --image $GCR_PATH \
        $SERVICE_NAME
    
    # Create pubsub subscription
    add_service_accounts
}

destroy() {
  set +e
  # delete pubsub resources
  gcloud pubsub topics delete $SERVICE_NAME -q 2> /dev/null
  gcloud pubsub subscriptions delete $SERVICE_NAME-subscriber -q 2> /dev/null
  # delete service account
  gcloud iam service-accounts delete $SA_NAME -q 2> /dev/null
  # delete container images
  export GCR_PATH=gcr.io/$PROJECT_ID/logging:$SERVICE_NAME
  gcloud container images delete $GCR_PATH -q --force-delete-tags 2> /dev/null
  # delete service
  gcloud run services delete $SERVICE_NAME -q  2> /dev/null
  set -e
}

verify() {
  set +e
  gcloud run services describe $SERVICE_NAME > /dev/null 2> /dev/null
  if [[ $? == 0 ]]; then
     echo "TRUE"
     exit 0
   else
     echo "FALSE"
     exit 1
  fi
  set -e
}

filter-string() {
  echo "resource.type=\"global\""
}