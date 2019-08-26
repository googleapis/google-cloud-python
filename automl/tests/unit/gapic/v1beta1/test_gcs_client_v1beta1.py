# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

"""Unit tests."""

import mock
import pandas
import pytest
import re

from google.cloud import automl_v1beta1
from google.api_core import exceptions


class TestGcsClient(object):
    def gcs_client(self):
        client_mock = mock.Mock()
        return automl_v1beta1.tables.gcs_client.GcsClient(client=client_mock)

    def test_create_bucket_name(self):
        gcs_client = self.gcs_client()
        gcs_client.create_bucket("my-bucket-name")
        gcs_client.client.create_bucket.assert_called_with("my-bucket-name")

    def test_create_bucket_no_bucket_name(self):
        gcs_client = self.gcs_client()
        generated_bucket_name = gcs_client.create_bucket()
        gcs_client.client.create_bucket.assert_called_with(generated_bucket_name)
        assert re.match('^automl-tables-bucket-[0-9]*$', generated_bucket_name) 

    def test_upload_pandas_dataframe(self):
        gcs_client = self.gcs_client()
        dataframe = pandas.DataFrame({})

        gcs_client.upload_pandas_dataframe("my-bucket-name", dataframe, "my-csv-name")
        gcs_client.client.get_bucket.assert_called_with("my-bucket-name")

        mock_bucket = gcs_client.client.get_bucket.return_value
        mock_bucket.blob.assert_called_with("my-csv-name")
        mock_blob = mock_bucket.blob.return_value
        mock_blob.upload_from_filename.assert_called_with("my-csv-name.csv")

    def test_upload_pandas_dataframe_not_type_dataframe(self):
        gcs_client = self.gcs_client()
        with pytest.raises(ValueError):
            gcs_client.upload_pandas_dataframe("my-bucket-name", "my-dataframe")
        gcs_client.client.upload_pandas_dataframe.assert_not_called()

    def test_upload_pandas_dataframe_no_csv_name(self):
        gcs_client = self.gcs_client()
        dataframe = pandas.DataFrame({})

        generated_csv_name = gcs_client.upload_pandas_dataframe("my-bucket-name", dataframe)
        gcs_client.client.get_bucket.assert_called_with("my-bucket-name")

        mock_bucket = gcs_client.client.get_bucket.return_value
        mock_bucket.blob.assert_called_with(generated_csv_name)
        mock_blob = mock_bucket.blob.return_value
        mock_blob.upload_from_filename.assert_called_with(generated_csv_name + ".csv")
        assert re.match('^automl-tables-dataframe-[0-9]*$', generated_csv_name)
