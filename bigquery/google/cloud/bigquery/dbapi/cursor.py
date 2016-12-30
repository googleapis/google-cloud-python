# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Cursor for the Google BigQuery DB-API."""

import collections
import uuid

import six

from google.cloud.bigquery.dbapi import _helpers
from google.cloud.bigquery.dbapi import exceptions


_ARRAYSIZE_DEFAULT = 20


class Cursor(object):
    """DB-API Cursor to Google BigQuery.

    :type: :class:`~google.cloud.bigquery.dbapi.Connection`
    :param connection: A DB-API connection to Google BigQuery.
    """
    def __init__(self, connection):
        self.connection = connection
        self.description = None
        self.rowcount = -1
        self.arraysize = None
        self._query_data = None
        self._page_token = None
        self._has_fetched_all_rows = True

    def close(self):
        """No-op."""

    def _set_description(self, schema):
        """Set description from schema.

        :type: list of :class:`~google.cloud.bigquery.schema.SchemaField`
        """
        if schema is None:
            self.description = None
            return

        desc = []
        for field in schema:
            desc.append(tuple([
                field.name,
                field.field_type,
                None,
                None,
                None,
                None,
                field.mode == 'NULLABLE']))
        self.description = tuple(desc)

    def _set_rowcount(self, query_results):
        """Set the rowcount from query results.

        Normally, this sets rowcount to the number of rows returned by the
        query, but if it was a DML statement, it sets rowcount to the number
        of modified rows.

        :type: :class:`~google.cloud.bigquery.query.QueryResults`
        :param query_results: results of a query
        """
        total_rows = 0
        num_dml_affected_rows = query_results.num_dml_affected_rows

        if (query_results.total_rows is not None
                and query_results.total_rows > 0):
            total_rows = query_results.total_rows
        if num_dml_affected_rows is not None and num_dml_affected_rows > 0:
            total_rows = num_dml_affected_rows
        self.rowcount = total_rows

    def _format_operation_list(self, operation, parameters):
        """Formats parameters in operation in way BigQuery expects.

        :type: str
        :param operation: A Google BigQuery query string.

        :type: list
        :param parameters: List parameter values.
        """
        formatted_params = ['?' for _ in parameters]

        try:
            return operation % tuple(formatted_params)
        except TypeError as ex:
            raise exceptions.ProgrammingError(ex)

    def _format_operation_dict(self, operation, parameters):
        """Formats parameters in operation in way BigQuery expects.

        :type: str
        :param operation: A Google BigQuery query string.

        :type: dict
        :param parameters: Dictionary of parameter values.
        """
        formatted_params = {}
        for name in parameters:
            formatted_params[name] = '@{}'.format(name)

        try:
            return operation % formatted_params
        except KeyError as ex:
            raise exceptions.ProgrammingError(ex)

    def _format_operation(self, operation, parameters=None):
        """Formats parameters in operation in way BigQuery expects.

        Raises a ProgrammingError if a parameter used in the operation is not
        found in the parameters dictionary.

        :type: str
        :param operation: A Google BigQuery query string.

        :type: dict or list
        :param parameters: Optional parameter values.
        """
        if parameters is None:
            return operation

        if isinstance(parameters, collections.Mapping):
            return self._format_operation_dict(operation, parameters)

        return self._format_operation_list(operation, parameters)

    def execute(self, operation, parameters=None):
        """Prepare and execute a database operation.

        :type: str
        :param operation: A Google BigQuery query string.

        :type: dict or list
        :param parameters: Optional dictionary or sequence of parameter values.
        """
        self._query_results = None
        self._page_token = None
        self._has_fetched_all_rows = False
        client = self.connection._client
        job_id = str(uuid.uuid4())

        # The DB-API uses the pyformat formatting, since the way BigQuery does
        # query parameters was not one of the standard options. Convert both
        # the query and the parameters to the format expected by the client
        # libraries.
        formatted_operation = self._format_operation(
            operation, parameters=parameters)
        query_parameters = _helpers.to_query_parameters(parameters)

        query_job = client.run_async_query(
            job_id,
            formatted_operation,
            query_parameters=query_parameters)
        query_job.use_legacy_sql = False
        query_job.begin()
        _helpers.wait_for_job(query_job)
        query_results = query_job.results()

        # Force the iterator to run because the query_results doesn't
        # have the total_rows populated. See:
        # https://github.com/GoogleCloudPlatform/google-cloud-python/issues/3506
        query_iterator = query_results.fetch_data()
        try:
            six.next(iter(query_iterator))
        except StopIteration:
            pass

        self._query_data = iter(
            query_results.fetch_data(max_results=self.arraysize))
        self._set_rowcount(query_results)
        self._set_description(query_results.schema)

    def executemany(self, operation, seq_of_parameters):
        """Prepare and execute a database operation multiple times.

        :type: str
        :param operation: A Google BigQuery query string.

        :type: list
        :param parameters: Sequence of many sets of parameter values.
        """
        for parameters in seq_of_parameters:
            self.execute(operation, parameters)

    def fetchone(self):
        """Fetch a single row from the results of the last ``execute*()`` call.

        :rtype: tuple
        :returns:
            A tuple representing a row or ``None`` if no more data is
            available.
        """
        if self._query_data is None:
            raise exceptions.InterfaceError(
                'No query results: execute() must be called before fetch.')

        try:
            return six.next(self._query_data)
        except StopIteration:
            return None

    def fetchmany(self, size=None):
        """Fetch multiple results from the last ``execute*()`` call.

        Note that the size parameter is not used for the request/response size.
        Use ``arraysize()`` before calling ``execute()`` to set the batch size.

        :type: int
        :param size:
            Optional maximum number of rows to return. Defaults to the
            arraysize attribute.

        :rtype: tuple
        :returns: A list of rows.
        """
        if self._query_data is None:
            raise exceptions.InterfaceError(
                'No query results: execute() must be called before fetch.')
        if size is None:
            size = self.arraysize
        if size is None:
            size = _ARRAYSIZE_DEFAULT

        rows = []
        for row in self._query_data:
            rows.append(row)
            if len(rows) >= size:
                break
        return rows

    def fetchall(self):
        """Fetch all remaining results from the last ``execute*()`` call.

        :rtype: list of tuples
        :returns: A list of all the rows in the results.
        """
        if self._query_data is None:
            raise exceptions.InterfaceError(
                'No query results: execute() must be called before fetch.')
        return [row for row in self._query_data]

    def setinputsizes(self, sizes):
        """No-op."""

    def setoutputsize(self, size, column=None):
        """No-op."""
