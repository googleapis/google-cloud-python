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


SERVICE_NAME="log-py-run-$(echo $ENVCTL_ID | head -c 10)"
SA_NAME=$SERVICE_NAME-invoker

add_service_accounts() {
  set +e
  local PROJECT_ID=$(gcloud config list --format 'value(core.project)')
  local PROJECT_NUMBER=$(gcloud projects list --filter=$PROJECT_ID --format="value(PROJECT_NUMBER)")
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com \
     --role=roles/iam.serviceAccountTokenCreator
  gcloud iam service-accounts create $SA_NAME \
     --display-name "Pub/Sub Invoker"
  gcloud run services add-iam-policy-binding  $SERVICE_NAME \
     --member=serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com \
     --role=roles/run.invoker
  RUN_URL=$(gcloud run services list --filter=$SERVICE_NAME --format="value(URL)")
  gcloud pubsub subscriptions create $SERVICE_NAME-subscriber --topic $SERVICE_NAME \
    --push-endpoint=$RUN_URL \
    --push-auth-service-account=$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com
  set -e
}

destroy() {
  set +e
  # delete pubsub resources
  gcloud pubsub topics delete $SERVICE_NAME -q 2> /dev/null
  gcloud pubsub subscriptions delete $SERVICE_NAME-subscriber -q 2> /dev/null
  # delete service account
  gcloud iam service-accounts delete $SA_NAME@$PROJECT_ID.iam.gserviceaccount.com -q 2> /dev/null
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

deploy() {
  build_container
  gcloud config set run/platform managed
  gcloud config set run/region us-west1
  gcloud run deploy  \
    --image $GCR_PATH \
    --update-env-vars ENABLE_FLASK=true \
    --no-allow-unauthenticated \
    $SERVICE_NAME
  # create pubsub subscription
  add_service_accounts
}

filter-string() {
  echo "resource.type=\"global\""
}

