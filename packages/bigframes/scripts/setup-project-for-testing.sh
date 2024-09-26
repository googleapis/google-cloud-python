#!/bin/bash

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


if [ $# -lt 1 ]; then
  echo "USAGE: `basename $0` <project-id> [<principal>]"
  echo "EXAMPLES:"
  echo "       `basename $0` my-project"
  echo "       `basename $0` my-project user:user_id@example.com"
  echo "       `basename $0` my-project group:group_id@example.com"
  echo "       `basename $0` my-project serviceAccount:service_account_id@example.com"
  exit 1
fi

PROJECT_ID=$1
PRINCIPAL=$2
BIGFRAMES_DEFAULT_CONNECTION_NAME=bigframes-default-connection
BIGFRAMES_RF_CONNECTION_NAME=bigframes-rf-conn

if [ "$PRINCIPAL" != "" ]; then
  echo $PRINCIPAL | grep -E "(user|group|serviceAccount):" >/dev/null
  if [ $? -ne 0 ]; then
    echo "principal must have prefix 'user:', 'group:' or 'serviceAccount:'"
    exit 1
  fi
fi

if ! test `which gcloud`; then
  echo "gcloud CLI is not installed. Install it from https://cloud.google.com/sdk/docs/install." >&2
  exit 1
fi

################################################################################
# Log and execute a command
################################################################################
function log_and_execute() {
  echo Running command: $*
  $*
}


################################################################################
# Enable APIs
################################################################################
function enable_apis() {
  for service in aiplatform.googleapis.com \
                 artifactregistry.googleapis.com \
                 bigquery.googleapis.com \
                 bigqueryconnection.googleapis.com \
                 bigquerystorage.googleapis.com \
                 cloudbuild.googleapis.com \
                 cloudfunctions.googleapis.com \
                 cloudresourcemanager.googleapis.com \
                 compute.googleapis.com \
                 run.googleapis.com \
    ; do
    log_and_execute gcloud --project=$PROJECT_ID services enable $service
    if [ $? -ne 0 ]; then
      echo "Failed to enable service $service, exiting..."
      exit 1
    fi
  done
}


################################################################################
# Ensure a BQ connection exists with desired IAM rols
################################################################################
function ensure_bq_connection_with_iam() {
  if [ $# -ne 2 ]; then
    echo "USAGE: `basename $0` <location> <connection-name>"
    echo "EXAMPLES:"
    echo "       `basename $0` my-project my-connection"
    exit 1
  fi

  location=$1
  connection_name=$2

  log_and_execute bq show \
                    --connection \
                    --project_id=$PROJECT_ID \
                    --location=$location \
                    $connection_name 2>&1 >/dev/null
  if [ $? -ne 0 ]; then
    echo "Connection $connection_name doesn't exists in location \"$location\", creating..."
    log_and_execute bq mk \
                      --connection \
                      --project_id=$PROJECT_ID \
                      --location=$location \
                      --connection_type=CLOUD_RESOURCE \
                      $connection_name
    if [ $? -ne 0 ]; then
      echo "Failed creating connection, exiting."
      exit 1
    fi
  else
    echo "Connection $connection_name already exists in location $location."
  fi

  compact_json_info_cmd="bq show --connection \
                          --project_id=$PROJECT_ID \
                          --location=$location \
                          --format=json \
                          $connection_name"
  compact_json_info_cmd_output=`$compact_json_info_cmd`
  if [ $? -ne 0 ]; then
    echo "Failed to fetch connection info: $compact_json_info_cmd_output"
    exit 1
  fi

  connection_service_account=`echo $compact_json_info_cmd_output | sed -e 's/.*"cloudResource":{"serviceAccountId":"//' -e 's/".*//'`

  # Configure roles for the service accounts associated with the connection
  for role in run.invoker aiplatform.user; do
    log_and_execute gcloud projects add-iam-policy-binding $PROJECT_ID \
                      --member=serviceAccount:$connection_service_account \
                      --role=roles/$role
    if [ $? -ne 0 ]; then
      echo "Failed to set IAM, exiting..."
      exit 1
    fi
  done
}


################################################################################
# Create the default BQ connection in US location
################################################################################
function ensure_bq_connections_with_iam() {
  ensure_bq_connection_with_iam "us" "$BIGFRAMES_DEFAULT_CONNECTION_NAME"

  # Create commonly used BQ connection in various locations
  for location in asia-southeast1 \
                  eu \
                  europe-west4 \
                  southamerica-west1 \
                  us \
                  us-central1 \
                  us-east5 \
    ; do
    ensure_bq_connection_with_iam "$location" "$BIGFRAMES_RF_CONNECTION_NAME"
  done
}


################################################################################
# Set up IAM roles for principal
################################################################################
function setup_iam_roles () {
  if [ "$PRINCIPAL" != "" ]; then
    for role in aiplatform.user \
                bigquery.user \
                bigquery.connectionAdmin \
                bigquery.dataEditor \
                browser \
                cloudfunctions.developer \
                iam.serviceAccountUser \
      ; do
      log_and_execute gcloud projects add-iam-policy-binding $PROJECT_ID \
                        --member=$PRINCIPAL \
                        --role=roles/$role
      if [ $? -ne 0 ]; then
        echo "Failed to set IAM, exiting..."
        exit 1
      fi
    done
  fi
}


################################################################################
# Create vertex endpoint for test ML model
################################################################################
function create_bq_model_vertex_endpoint () {
  vertex_region=us-central1
  model_name=bigframes-test-linreg2
  endpoint_name=$model_name-endpoint

  # Create vertex model
  log_and_execute python scripts/create_test_model_vertex.py \
                    -m $model_name \
                    -p $PROJECT_ID
  if [ $? -ne 0 ]; then
    echo "Failed to create model, exiting..."
    exit 1
  fi

  # Create vertex endpoint
  log_and_execute gcloud ai endpoints create \
                    --project=$PROJECT_ID \
                    --region=$vertex_region \
                    --display-name=$endpoint_name
  if [ $? -ne 0 ]; then
    echo "Failed to create vertex endpoint, exiting..."
    exit 1
  fi

  # Fetch endpoint id
  endpoint_id=`gcloud ai endpoints list \
                --project=$PROJECT_ID \
                --region=$vertex_region \
                --filter=display_name=$endpoint_name 2>/dev/null \
                | tail -n1 | cut -d' '  -f 1`
  if [ "$endpoint_id" = "" ]; then
    echo "Failed to fetch vertex endpoint id, exiting..."
    exit 1
  fi

  # Deploy the model to the vertex endpoint
  log_and_execute gcloud ai endpoints deploy-model $endpoint_id \
                    --project=$PROJECT_ID \
                    --region=$vertex_region \
                    --model=$model_name \
                    --display-name=$model_name
  if [ $? -ne 0 ]; then
    echo "Failed to deploy model to vertex endpoint, exiting..."
    exit 1
  fi

  # Form the endpoint
  endpoint_rel_path=`gcloud ai endpoints describe \
                      --project=$PROJECT_ID \
                      --region=us-central1 \
                      $endpoint_id 2>/dev/null \
                      | grep "^name:" | cut -d' ' -f2`
  if [ "$endpoint_rel_path" = "" ]; then
    echo "Failed to fetch vertex endpoint relativr path, exiting..."
    exit 1
  fi
  endpoint_path=https://$vertex_region-aiplatform.googleapis.com/v1/$endpoint_rel_path

  # Print the endpoint configuration to be used in tests
  echo
  echo Run following command to set test model vertex endpoint:
  echo export BIGFRAMES_TEST_MODEL_VERTEX_ENDPOINT=$endpoint_path
}


################################################################################
# Set the things up
################################################################################
enable_apis
ensure_bq_connections_with_iam
setup_iam_roles
create_bq_model_vertex_endpoint
