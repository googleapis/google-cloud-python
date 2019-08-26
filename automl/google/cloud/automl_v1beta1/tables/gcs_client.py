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

"""Wraps the Google Cloud Storage client library for use in tables helper."""

import os
import pandas
import time

from google.cloud import storage


class GcsClient(object):
    """Uploads Pandas DataFrame to a bucket in Google Cloud Storage."""

    def __init__(self, client=None, credentials=None, project=None, **kwargs):
        """Constructor.
        
        Args:
            client (Optional[storage.Client]): A Google Cloud Storage Client
                instance. Either `client` or `credentials` must be provided.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment. Either `client` or
                `credentials` must be provided.

        Raises:
            ValueError: If required parameters are missing.
        """
        if client is None and credentials is None:
            raise ValueError("One of 'client' or 'credentials' must be set.")

        if client is not None:
            self.client = client
        else:
            self.client = storage.Client(credentials=credentials)

    def ensure_bucket_exists(self, bucket_name=None):
        """Checks if a bucket with the given name exists.

        Creates this bucket if it doesn't exist and returns its name.
        
        Args:
            bucket_name (Optional[string]): The name of the bucket. We will
                set this to 'automl-tables-staging' if this parameter is not
                supplied.
        """
        if bucket_name is None:
            bucket_name = "automl-tables-staging"

        try:
            self.client.get_bucket(bucket_name)
        except google.cloud.exceptions.NotFound:
            self.client.create_bucket(bucket_name)
        return bucket_name

    def upload_pandas_dataframe(self, bucket_name, dataframe, uploaded_csv_name=None):
        """Uploads a Pandas DataFrame as CSV to the bucket.

        Returns the uploaded CSV name at the end.

        Args:
            bucket_name (string): The bucket name to upload the CSV to.
            dataframe (pandas.DataFrame): The Pandas Dataframe to be uploaded.
            uploaded_csv_name (Optional[string]): The name for the uploaded CSV file.
        """
        if not isinstance(dataframe, pandas.DataFrame):
            raise ValueError("'dataframe' must be a pandas.DataFrame instance.")

        if uploaded_csv_name is None:
            uploaded_csv_name = "automl-tables-dataframe-{}".format(int(time.time()))

        local_csv_name = uploaded_csv_name + ".csv"
        dataframe.to_csv(local_csv_name)
        
        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.blob(uploaded_csv_name)
        blob.upload_from_filename(local_csv_name)
        os.remove(local_csv_name)

        return uploaded_csv_name
