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

# DO NOT EDIT! This is a generated sample ("Request",  "scheduled_query")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-bigquerydatatransfer


def sample_create_transfer_config(project_id):
    # [START bigquerydatatransfer_create_scheduled_query]
    from google.cloud import bigquery_datatransfer_v1
    import google.protobuf.json_format

    client = bigquery_datatransfer_v1.DataTransferServiceClient()

    # TODO(developer): Set the project_id to the project that contains the
    #                  destination dataset.
    # project_id = 'your-project-id'

    parent = client.project_path(project_id)

    transfer_config = google.protobuf.json_format.ParseDict(
        {
            "destination_dataset_id": "your_dataset_id",
            "display_name": "Your Scheduled Query Name",
            "data_source_id": "scheduled_query",
            "params": {
                "fields": {
                    "query": "SELECT 1;  -- Use standard SQL syntax.",
                    "destination_table_name_template": "your_table_{run_date}",
                    "write_disposition": "WRITE_TRUNCATE",
                    "partitioning_field": "",
                }
            },
            "schedule": "every 24 hours",
        },
        bigquery_datatransfer_v1.types.TransferConfig(),
    )

    response = client.create_transfer_config(parent, transfer_config)

    print(response)
    # [END bigquerydatatransfer_create_scheduled_query]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", type=str, default="your-project-id")
    args = parser.parse_args()

    sample_create_transfer_config(args.project_id)


if __name__ == "__main__":
    main()
