# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
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
"""System tests for reading rows from tables."""

import os

import pytest

from google.cloud import bigquery_storage_v1beta1


@pytest.fixture()
def project_id():
    return os.environ['PROJECT_ID']


@pytest.fixture()
def client():
    return bigquery_storage_v1beta1.BigQueryStorageClient()


@pytest.fixture()
def table_reference():
    table_ref = bigquery_storage_v1beta1.types.TableReference()
    table_ref.project_id = 'bigquery-public-data'
    table_ref.dataset_id = 'usa_names'
    table_ref.table_id = 'usa_1910_2013'
    return table_ref


def test_read_rows(client, project_id, table_reference):
    session = client.create_read_session(
        table_reference,
        'projects/{}'.format(project_id),
        requested_streams=1,
    )

    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=session.streams[0])
    rowstream = client.read_rows(stream_pos)
    page = rowstream.next()

    assert page.status.estimated_row_count > 0
    assert len(page.avro_rows.serialized_binary_rows) > 0


def test_split_read_stream(client, project_id, table_reference):
    session = client.create_read_session(
        table_reference,
        parent='projects/{}'.format(project_id),
    )

    split = client.split_read_stream(session.streams[0])

    assert split.primary_stream is not None
    assert split.remainder_stream is not None
    assert split.primary_stream != split.remainder_stream
