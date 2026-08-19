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
import json
import os
import re
import time

from create_test_config import set_test_config
from google.api_core import datetime_helpers
from google.api_core.exceptions import AlreadyExists, ResourceExhausted
from google.cloud.spanner_v1 import Client
from google.cloud.spanner_v1.database import Database
from google.cloud.spanner_v1.instance import Instance

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


def format_duration(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    if mins > 0:
        return f"{mins} minutes and {secs} seconds"
    else:
        return f"{secs} seconds"


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

    instance = CLIENT.instance(instance_id="".join(instance_id).replace("/", ""))
    database_id_str = "".join(database_id).replace("/", "")
    database = instance.database(database_id_str)
    database.drop()

    # Calculate and report active duration
    meta_path = os.path.join(os.path.dirname(__file__), ".db_session_info.json")
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r") as f:
                meta = json.load(f)
            creation_time = meta.get("creation_time", time.time())
            db_name = meta.get("database_id", database_id_str)
            elapsed_seconds = time.time() - creation_time
            duration_str = format_duration(elapsed_seconds)
            print(f"[Spanner DB] Database {db_name} was active for {duration_str} before teardown.")
        except Exception:
            pass
        finally:
            if os.path.exists(meta_path):
                os.remove(meta_path)


delete_test_database()
