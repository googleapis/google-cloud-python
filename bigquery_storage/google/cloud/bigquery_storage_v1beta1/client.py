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

"""Parent client for calling the Cloud BigQuery Storage API.

This is the base from which all interactions with the API occur.
"""

from __future__ import absolute_import

import google.api_core.gapic_v1.method

from google.cloud.bigquery_storage_v1beta1 import reader
from google.cloud.bigquery_storage_v1beta1.gapic import big_query_storage_client  # noqa


_SCOPES = (
    "https://www.googleapis.com/auth/bigquery",
    "https://www.googleapis.com/auth/cloud-platform",
)


class BigQueryStorageClient(big_query_storage_client.BigQueryStorageClient):
    """Client for interacting with BigQuery Storage API.

    The BigQuery storage API can be used to read data stored in BigQuery.
    """

    def read_rows(
        self,
        read_position,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Reads rows from the table in the format prescribed by the read
        session. Each response contains one or more table rows, up to a
        maximum of 10 MiB per response; read requests which attempt to read
        individual rows larger than this will fail.

        Each request also returns a set of stream statistics reflecting the
        estimated total number of rows in the read stream. This number is
        computed based on the total table size and the number of active
        streams in the read session, and may change as other streams continue
        to read data.

        Example:
            >>> from google.cloud import bigquery_storage_v1beta1
            >>>
            >>> client = bigquery_storage_v1beta1.BigQueryStorageClient()
            >>>
            >>> # TODO: Initialize ``table_reference``:
            >>> table_reference = {
            ...     'project_id': 'your-data-project-id',
            ...     'dataset_id': 'your_dataset_id',
            ...     'table_id': 'your_table_id',
            ... }
            >>>
            >>> # TODO: Initialize `parent`:
            >>> parent = 'projects/your-billing-project-id'
            >>>
            >>> session = client.create_read_session(table_reference, parent)
            >>> read_position = bigquery_storage_v1beta1.types.StreamPosition(
            ...     stream=session.streams[0],  # TODO: Read the other streams.
            ... )
            >>>
            >>> for element in client.read_rows(read_position):
            ...     # process element
            ...     pass

        Args:
            read_position (Union[ \
                dict, \
                ~google.cloud.bigquery_storage_v1beta1.types.StreamPosition \
            ]):
                Required. Identifier of the position in the stream to start
                reading from. The offset requested must be less than the last
                row read from ReadRows. Requesting a larger offset is
                undefined. If a dict is provided, it must be of the same form
                as the protobuf message
                :class:`~google.cloud.bigquery_storage_v1beta1.types.StreamPosition`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            ~google.cloud.bigquery_storage_v1beta1.reader.ReadRowsStream:
                An iterable of
                :class:`~google.cloud.bigquery_storage_v1beta1.types.ReadRowsResponse`.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        gapic_client = super(BigQueryStorageClient, self)
        stream = gapic_client.read_rows(
            read_position, retry=retry, timeout=timeout, metadata=metadata
        )
        return reader.ReadRowsStream(
            stream,
            gapic_client,
            read_position,
            {"retry": retry, "timeout": timeout, "metadata": metadata},
        )
