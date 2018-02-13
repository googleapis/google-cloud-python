# Copyright 2016 Google LLC All rights reserved.
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
CREATE TABLE all_types (
    list_goes_on ARRAY<INT64>,
    are_you_sure BOOL,
    raw_data BYTES(16),
    hwhen DATE,
    approx_value FLOAT64,
    eye_d INT64,
    description STRING(16),
    exactly_hwhen TIMESTAMP)
    PRIMARY KEY (eye_d);
CREATE TABLE counters (
    name STRING(1024),
    value INT64 )
    PRIMARY KEY (name);
CREATE TABLE string_plus_array_of_string (
    id INT64,
    name STRING(16),
    tags ARRAY<STRING(16)> )
    PRIMARY KEY (id);
CREATE INDEX name ON contacts(first_name, last_name);
"""

DDL_STATEMENTS = [stmt.strip() for stmt in DDL.split(';') if stmt.strip()]
