# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-bigquery-datatransfer


def sample_create_transfer_config(project_id, dataset_id, authorization_code=""):
    # [START bigquerydatatransfer_create_scheduled_query]
    from google.cloud import bigquery_datatransfer

    client = bigquery_datatransfer.DataTransferServiceClient()

    # TODO(developer): Set the project_id to the project that contains the
    #                  destination dataset.
    # project_id = "your-project-id"

    # TODO(developer): Set the destination dataset. The authorized user must
    #                  have owner permissions on the dataset.
    # dataset_id = "your_dataset_id"

    # TODO(developer): The first time you run this sample, set the
    # authorization code to a value from the URL:
    # https://www.gstatic.com/bigquerydatatransfer/oauthz/auth?client_id=433065040935-hav5fqnc9p9cht3rqneus9115ias2kn1.apps.googleusercontent.com&scope=https://www.googleapis.com/auth/bigquery%20https://www.googleapis.com/auth/drive&redirect_uri=urn:ietf:wg:oauth:2.0:oob
    #
    # authorization_code = "_4/ABCD-EFGHIJKLMNOP-QRSTUVWXYZ"
    #
    # You can use an empty string for authorization_code in subsequent runs of
    # this code sample with the same credentials.
    #
    # authorization_code = ""

    # Use standard SQL syntax for the query.
    query_string = """
    SELECT
      CURRENT_TIMESTAMP() as current_time,
      @run_time as intended_run_time,
      @run_date as intended_run_date,
      17 as some_integer
    """

    parent = f"projects/{project_id}"

    transfer_config = bigquery_datatransfer.TransferConfig(
        destination_dataset_id=dataset_id,
        display_name="Your Scheduled Query Name",
        data_source_id="scheduled_query",
        params={
            "query": query_string,
            "destination_table_name_template": "your_table_{run_date}",
            "write_disposition": "WRITE_TRUNCATE",
            "partitioning_field": "",
        },
        schedule="every 24 hours",
    )

    response = client.create_transfer_config(
        request={
            "parent": parent,
            "transfer_config": transfer_config,
            "authorization_code": authorization_code,
        }
    )

    print("Created scheduled query '{}'".format(response.name))
    # [END bigquerydatatransfer_create_scheduled_query]
    # Return the config name for testing purposes, so that it can be deleted.
    return response.name


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", type=str, default="your-project-id")
    parser.add_argument("--dataset_id", type=str, default="your_dataset_id")
    parser.add_argument("--authorization_code", type=str, default="")
    args = parser.parse_args()

    sample_create_transfer_config(args.project_id, args.dataset_id, args.authorization_code)


if __name__ == "__main__":
    main()
