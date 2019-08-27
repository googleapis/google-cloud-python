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

import google
import mock
import pandas
import pytest
import re

from google.api_core import exceptions
from google.cloud import automl_v1beta1


class TestGcsClient(object):
    def gcs_client(self, client_attrs={}):
        client_mock = mock.Mock(**client_attrs)
        return automl_v1beta1.tables.gcs_client.GcsClient(client=client_mock)

    def test_ensure_bucket_exists(self):
        gcs_client = self.gcs_client(
            {"get_bucket.side_effect": google.cloud.exceptions.NotFound("err")}
        )
        returned_bucket_name = gcs_client.ensure_bucket_exists(project="my-project")
        gcs_client.client.get_bucket.assert_called_with(
            "my-project-automl-tables-staging"
        )
        gcs_client.client.create_bucket.assert_called_with(
            "my-project-automl-tables-staging"
        )
        assert returned_bucket_name == "my-project-automl-tables-staging"

    def test_ensure_bucket_exists_name(self):
        gcs_client = self.gcs_client(
            {"get_bucket.side_effect": google.cloud.exceptions.NotFound("err")}
        )
        returned_bucket_name = gcs_client.ensure_bucket_exists(bucket_name="my-bucket")
        gcs_client.client.get_bucket.assert_called_with("my-bucket")
        gcs_client.client.create_bucket.assert_called_with("my-bucket")
        assert returned_bucket_name == "my-bucket"

    def test_ensure_bucket_exists_bucket_already_exists(self):
        gcs_client = self.gcs_client()
        returned_bucket_name = gcs_client.ensure_bucket_exists(bucket_name="my-bucket")
        gcs_client.client.get_bucket.assert_called_with("my-bucket")
        gcs_client.client.create_bucket.assert_not_called()
        assert returned_bucket_name == "my-bucket"

    def test_ensure_bucket_exists_no_project_or_bucket_name(self):
        gcs_client = self.gcs_client()
        with pytest.raises(ValueError):
            gcs_client.ensure_bucket_exists()
        gcs_client.client.get_bucket.assert_not_called()
        gcs_client.client.create_bucket.assert_not_called()

    def test_upload_pandas_dataframe(self):
        mock_blob = mock.Mock()
        mock_bucket = mock.Mock(**{"blob.return_value": mock_blob})
        gcs_client = self.gcs_client({"get_bucket.return_value": mock_bucket})
        dataframe = pandas.DataFrame({})

        gcs_uri = gcs_client.upload_pandas_dataframe(
            "my-bucket", dataframe, "my-file.csv"
        )

        gcs_client.client.get_bucket.assert_called_with("my-bucket")
        mock_bucket.blob.assert_called_with("my-file.csv")
        mock_blob.upload_from_filename.assert_called_with("my-file.csv")
        assert gcs_uri == "gs://my-bucket/my-file.csv"

    def test_upload_pandas_dataframe_no_csv_name(self):
        mock_blob = mock.Mock()
        mock_bucket = mock.Mock(**{"blob.return_value": mock_blob})
        gcs_client = self.gcs_client({"get_bucket.return_value": mock_bucket})
        dataframe = pandas.DataFrame({})

        gcs_uri = gcs_client.upload_pandas_dataframe("my-bucket", dataframe)
        generated_csv_name = gcs_uri.split("/")[-1]

        gcs_client.client.get_bucket.assert_called_with("my-bucket")
        mock_bucket.blob.assert_called_with(generated_csv_name)
        mock_blob.upload_from_filename.assert_called_with(generated_csv_name)
        assert re.match("gs://my-bucket/automl-tables-dataframe-([0-9]*).csv", gcs_uri)

    def test_upload_pandas_dataframe_not_type_dataframe(self):
        gcs_client = self.gcs_client()
        with pytest.raises(ValueError):
            gcs_client.upload_pandas_dataframe("my-bucket", "my-dataframe")
        gcs_client.client.upload_pandas_dataframe.assert_not_called()
