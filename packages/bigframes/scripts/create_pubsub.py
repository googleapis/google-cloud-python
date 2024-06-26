# Copyright 2024 Google LLC
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

# This script create the bigtable resources required for
# bigframes.streaming testing if they don't already exist

import os
import sys

from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

if not PROJECT_ID:
    print(
        "Please set GOOGLE_CLOUD_PROJECT environment variable before running.",
        file=sys.stderr,
    )
    sys.exit(1)


def create_topic(topic_id):
    # based on
    # https://cloud.google.com/pubsub/docs/samples/pubsub-quickstart-create-topic?hl=en

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, topic_id)

    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")


def main():
    create_topic("penguins")


if __name__ == "__main__":
    main()
