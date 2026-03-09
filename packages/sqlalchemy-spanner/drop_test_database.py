# -*- coding: utf-8 -*-
#
# Copyright 2021 Google LLC
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

import configparser
import os
import re
import time

from create_test_config import set_test_config
from google.api_core import datetime_helpers
from google.api_core.exceptions import AlreadyExists, ResourceExhausted
from google.cloud.spanner_v1 import Client
from google.cloud.spanner_v1.instance import Instance
from google.cloud.spanner_v1.database import Database


USE_EMULATOR = os.getenv("SPANNER_EMULATOR_HOST") is not None

PROJECT = os.getenv(
    "GOOGLE_CLOUD_PROJECT",
    os.getenv("PROJECT_ID", "emulator-test-project"),
)
CLIENT = None

if USE_EMULATOR:
    from google.auth.credentials import AnonymousCredentials

    CLIENT = Client(project=PROJECT, credentials=AnonymousCredentials())
else:
    CLIENT = Client(project=PROJECT)


def delete_test_database():
    """Delete the currently configured test database."""
    config = configparser.ConfigParser()
    if os.path.exists("test.cfg"):
        config.read("test.cfg")
    else:
        config.read("setup.cfg")
    db_url = config.get("db", "default")

    instance_id = re.findall(r"instances(.*?)databases", db_url)
    database_id = re.findall(r"databases(.*?)$", db_url)

    instance = CLIENT.instance(
        instance_id="".join(instance_id).replace("/", ""))
    database = instance.database("".join(database_id).replace("/", ""))
    database.drop()

delete_test_database()
