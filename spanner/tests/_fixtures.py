# Copyright 2016 Google Inc. All rights reserved.
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

"""Test fixtures."""


DDL = """\
CREATE TABLE contacts (
    contact_id INT64,
    first_name STRING(1024),
    last_name STRING(1024),
    email STRING(1024) )
    PRIMARY KEY (contact_id);
CREATE TABLE contact_phones (
    contact_id INT64,
    phone_type STRING(1024),
    phone_number STRING(1024) )
    PRIMARY KEY (contact_id, phone_type),
    INTERLEAVE IN PARENT contacts ON DELETE CASCADE;
"""

DDL_STATEMENTS = [stmt.strip() for stmt in DDL.split(';') if stmt.strip()]
