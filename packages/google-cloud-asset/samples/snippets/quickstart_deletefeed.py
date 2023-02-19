#!/usr/bin/env python

# Copyright 2018 Google LLC.
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


import argparse


def delete_feed(feed_name: str, transport: str = None):
    """
    Args:
        feed_name(str): Feed name you want to delete.
        transport(str): The transport to use. For example, "grpc"
            or "rest". If set to None, a transport is chosen automatically.
    """
    # [START asset_quickstart_delete_feed]
    from google.cloud import asset_v1

    # TODO feed_name = 'Feed name you want to delete'
    # TODO transport = 'Transport that you want to use. Either "grpc" or "rest"'

    client = asset_v1.AssetServiceClient(transport=transport)
    client.delete_feed(request={"name": feed_name})
    print("deleted_feed")
    # [END asset_quickstart_delete_feed]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("feed_name", help="Feed name you want to delete")
    args = parser.parse_args()
    delete_feed(args.feed_name)
