# Copyright 2017 Google Inc.
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

import csv
import io
import json

from google import resumable_media
import google.auth.transport.requests
import mock
import requests
from six.moves import http_client
from six.moves import StringIO

FIELDS = (u'name', u'age')
ROWS = [
    (u'Phred Phlyntstone', 32),
    (u'Bharney Rhubble', 33),
    (u'Wylma Phlyntstone', 29),
    (u'Bhettye Rhubble', 27),
]


def rows_to_csv(fields, rows):
    """Convert the rows into a CSV-format unicode string."""
    out = StringIO()
    writer = csv.writer(out)
    writer.writerow(fields)
    writer.writerows(rows)
    return out.getvalue()


def make_table():
    from google.cloud.bigquery import _http
    from google.cloud.bigquery import client
    from google.cloud.bigquery import dataset
    from google.cloud.bigquery import table

    mock_connection = mock.Mock(spec=_http.Connection)
    mock_client = mock.Mock(spec=client.Client)
    mock_client._connection = mock_connection
    mock_client._credentials = mock.sentinel.credentials
    mock_client.project = 'project_id'

    dataset = dataset.Dataset('test_dataset', mock_client)
    table = table.Table('test_table', dataset)

    return table


def make_response(status_code, content, headers={}):
    return mock.Mock(
            content=content, headers=headers, status_code=status_code,
            spec=requests.Response)


def make_resumable_upload_responses(size):
    resumable_url = 'http://test.invalid?upload_id=and-then-there-was-1'
    initial_response = make_response(
        http_client.OK, b'', {'location': resumable_url})
    data_response = make_response(
        resumable_media.PERMANENT_REDIRECT,
        b'', {'range': 'bytes=0-{:d}'.format(size - 1)})
    final_response = make_response(
        http_client.OK,
        json.dumps({'size': size}),
        {'Content-Type': 'application/json'})
    return [initial_response, data_response, final_response]


def test_upload_from_file_simple():
    table = make_table()

    csv_file = io.BytesIO(
        rows_to_csv(FIELDS, ROWS).encode('utf-8'))
    csv_file_size = len(csv_file.getvalue())

    mock_transport = mock.Mock(
        spec=google.auth.transport.requests.AuthorizedSession)
    transport_patch = mock.patch.object(
        table, '_make_transport', return_value=mock_transport)

    with transport_patch:
        mock_transport.request.side_effect = make_resumable_upload_responses(
            csv_file_size)
        table.upload_from_file(csv_file, source_format='CSV')
