# Copyright (C) 2019  Google LLC
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

from collections import namedtuple

# Injected dummy test types

DummyMethod = namedtuple(
    "DummyMethod",
    [
        "input",
        "output",
        "lro",
        "paged_result_field",
        "client_streaming",
        "server_streaming",
    ],
)

DummyMethod.__new__.__defaults__ = (False,) * len(DummyMethod._fields)

DummyMessage = namedtuple("DummyMessage", ["fields", "type"])
DummyMessage.__new__.__defaults__ = (False,) * len(DummyMessage._fields)

DummyField = namedtuple("DummyField", ["message", "repeated"])
DummyField.__new__.__defaults__ = (False,) * len(DummyField._fields)

DummyService = namedtuple("DummyService", ["methods"])

DummyApiSchema = namedtuple("DummyApiSchema", ["services", "naming"])
DummyApiSchema.__new__.__defaults__ = (False,) * len(DummyApiSchema._fields)

DummyNaming = namedtuple(
    "DummyNaming", ["warehouse_package_name", "name", "version"])
DummyNaming.__new__.__defaults__ = (False,) * len(DummyNaming._fields)
