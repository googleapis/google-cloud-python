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
import sys


def set_test_config(project, instance, user=None, password=None, host=None, port=None):
    config = configparser.ConfigParser()
    if user is not None and password is not None and host is not None and port is not None:
        url = (
            f"spanner+spanner://{user}:{password}@{host}:{port}"
            f"/projects/{project}/instances/{instance}/"
            "databases/compliance-test"
        )
    else:
        url = (
            f"spanner+spanner:///projects/{project}/instances/{instance}/"
            "databases/compliance-test"
        )
    config.add_section("db")
    config["db"]["default"] = url

    with open("test.cfg", "w") as configfile:
        config.write(configfile)


def main(argv):
    project = argv[0]
    instance = argv[1]
    if len(argv) == 6:
        user = argv[2]
        password = argv[3]
        host = argv[4]
        port = argv[5]
    else:
        user = None
        password = None
        host = None
        port = None
    set_test_config(project, instance, user, password, host, port)


if __name__ == "__main__":
    main(sys.argv[1:])
