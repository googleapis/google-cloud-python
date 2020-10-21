# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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


def sample_update_transfer_config(config_name, display_name):
    # [START bigquerydatatransfer_update_config]
    from google.cloud import bigquery_datatransfer

    client = bigquery_datatransfer.DataTransferServiceClient()
    # TODO(developer): Set the config_name which user wants to update.
    # config_name = "your-created-transfer-config-name"

    # TODO(developer): Set the display_name of transfer_config.
    # config_name = "your-created-transfer-config-name"

    transfer_config = client.get_transfer_config(name=config_name)
    transfer_config.display_name = display_name
    field_mask = {"paths": ["display_name"]}
    response = client.update_transfer_config(
        transfer_config=transfer_config, update_mask=field_mask
    )

    print("Transfer config updated for '{}'".format(response.name))
    # [END bigquerydatatransfer_update_config]
    # Return the config name for testing purposes, so that it can be deleted.
    return response


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--transfer_config_name", type=str, default="your-created-transfer-config-name")
    args = parser.parse_args()

    sample_update_transfer_config(args.transfer_config_name)


if __name__ == "__main__":
    main()
