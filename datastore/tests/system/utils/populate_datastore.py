# Copyright 2014 Google LLC
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

"""Script to populate datastore with system test data."""


from __future__ import print_function

import os
import sys
import time
import uuid

import six

from google.cloud import datastore


ANCESTOR = ("Book", "GoT")
RICKARD = ANCESTOR + ("Character", "Rickard")
EDDARD = RICKARD + ("Character", "Eddard")
KEY_PATHS = (
    RICKARD,
    EDDARD,
    ANCESTOR + ("Character", "Catelyn"),
    EDDARD + ("Character", "Arya"),
    EDDARD + ("Character", "Sansa"),
    EDDARD + ("Character", "Robb"),
    EDDARD + ("Character", "Bran"),
    EDDARD + ("Character", "Jon Snow"),
)
CHARACTERS = (
    {"name": u"Rickard", "family": u"Stark", "appearances": 0, "alive": False},
    {"name": u"Eddard", "family": u"Stark", "appearances": 9, "alive": False},
    {
        "name": u"Catelyn",
        "family": [u"Stark", u"Tully"],
        "appearances": 26,
        "alive": False,
    },
    {"name": u"Arya", "family": u"Stark", "appearances": 33, "alive": True},
    {"name": u"Sansa", "family": u"Stark", "appearances": 31, "alive": True},
    {"name": u"Robb", "family": u"Stark", "appearances": 22, "alive": False},
    {"name": u"Bran", "family": u"Stark", "appearances": 25, "alive": True},
    {"name": u"Jon Snow", "family": u"Stark", "appearances": 32, "alive": True},
)


def print_func(message):
    if os.getenv("GOOGLE_CLOUD_NO_PRINT") != "true":
        print(message)


def add_characters(client=None):
    if client is None:
        # Get a client that uses the test dataset.
        client = datastore.Client()
    with client.transaction() as xact:
        for key_path, character in six.moves.zip(KEY_PATHS, CHARACTERS):
            if key_path[-1] != character["name"]:
                raise ValueError(("Character and key don't agree", key_path, character))
            entity = datastore.Entity(key=client.key(*key_path))
            entity.update(character)
            xact.put(entity)
            print_func(
                "Adding Character %s %s" % (character["name"], character["family"])
            )


def add_uid_keys(client=None):
    if client is None:
        # Get a client that uses the test dataset.
        client = datastore.Client()

    num_batches = 2
    batch_size = 500

    for batch_num in range(num_batches):
        with client.batch() as batch:
            for seq_no in range(batch_size):
                uid = str(uuid.uuid4())
                key = client.key("uuid_key", uid)
                entity = datastore.Entity(key=key)
                entity["batch_num"] = batch_num
                entity["seq_no"] = seq_no
                batch.put(entity)


def add_timestamp_keys(client=None):
    if client is None:
        # Get a client that uses the test dataset.
        client = datastore.Client()

    num_batches = 2
    batch_size = 500

    timestamp_micros = set()
    for batch_num in range(num_batches):
        with client.batch() as batch:
            for seq_no in range(batch_size):
                print("time_time: batch: {}, sequence: {}".format(batch_num, seq_no))
                now_micros = int(time.time() * 1e6)
                while now_micros in timestamp_micros:
                    now_micros = int(time.time() * 1e6)
                timestamp_micros.add(now_micros)
                key = client.key("timestamp_key", now_micros)
                entity = datastore.Entity(key=key)
                entity["batch_num"] = batch_num
                entity["seq_no"] = seq_no
                batch.put(entity)


def main():
    client = datastore.Client()
    flags = sys.argv[1:]

    if len(flags) == 0:
        flags = ["--characters", "--uuid", "--timestamps"]

    if "--characters" in flags:
        add_characters(client)

    if "--uuid" in flags:
        add_uid_keys(client)

    if "--timestamps" in flags:
        add_timestamp_keys(client)


if __name__ == "__main__":
    main()
