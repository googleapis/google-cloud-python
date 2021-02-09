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

SERVICE_NAME="logging-py-gke-$(echo $ENVCTL_ID | head -c 10)"
ZONE=us-central1-a

destroy() {
  set +e
  # delete pubsub resources
  gcloud pubsub topics delete $SERVICE_NAME -q 2> /dev/null
  gcloud pubsub subscriptions delete $SERVICE_NAME-subscriber -q 2> /dev/null
  # delete container images
  export GCR_PATH=gcr.io/$PROJECT_ID/logging:$SERVICE_NAME
  gcloud container images delete $GCR_PATH -q --force-delete-tags 2> /dev/null
  # delete cluster
  gcloud container clusters delete --zone $ZONE $SERVICE_NAME -q
  set -e
}

verify() {
  set +e
  gcloud container clusters describe --zone $ZONE $SERVICE_NAME > /dev/null 2> /dev/null
  if [[ $? == 0 ]]; then
     echo "TRUE"
     exit 0
   else
     echo "FALSE"
     exit 1
  fi
  set -e
}

attach_or_create_gke_cluster(){
  set +e
  gcloud container clusters get-credentials $SERVICE_NAME
  if [[ $? -ne 0 ]]; then
    echo "cluster not found. creating..."
    gcloud container clusters create $SERVICE_NAME \
      --zone $ZONE \
      --scopes "https://www.googleapis.com/auth/pubsub"
  fi
  set -e
}

deploy() {
  local SCRIPT="${1:-router.py}"

  attach_or_create_gke_cluster
  build_container
  cat <<EOF > $TMP_DIR/gke.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: $SERVICE_NAME
    spec:
      selector:
        matchLabels:
          app: $SERVICE_NAME
      template:
        metadata:
          labels:
            app: $SERVICE_NAME
        spec:
          containers:
          - name: $SERVICE_NAME
            image:  $GCR_PATH
            env:
            - name: PUBSUB_TOPIC
              value: $SERVICE_NAME
            - name: ENABLE_SUBSCRIBER
              value: "true"
EOF
  # clean cluster
  set +e
  kubectl delete deployments --all 2>/dev/null
  kubectl delete -f $TMP_DIR 2>/dev/null
  set -e
  # deploy test container
  kubectl apply -f $TMP_DIR
}

filter-string() {
  echo "resource.type=\"k8s_container\" AND resource.labels.cluster_name=\"$SERVICE_NAME\""
}

