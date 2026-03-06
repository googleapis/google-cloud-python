# Copyright (c) 2021 The sqlalchemy-bigquery Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
SQLAlchemy dialect for Google BigQuery
"""

from google.cloud import bigquery
import pytest
import sqlalchemy
import test_utils.prefixer

prefixer = test_utils.prefixer.Prefixer("python-bigquery-sqlalchemy", "tests/system")


@pytest.fixture(scope="session")
def client():
    return bigquery.Client()


@pytest.fixture(scope="session")
def dataset_id(client: bigquery.Client):
    project_id = client.project
    dataset_id = prefixer.create_prefix()
    dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
    dataset = client.create_dataset(dataset)
    yield dataset_id
    client.delete_dataset(dataset_id, delete_contents=True)


@pytest.fixture(scope="session")
def engine(dataset_id):
    return sqlalchemy.create_engine(f"bigquery:///{dataset_id}")
