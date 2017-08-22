# Copyright 2015 Google Inc.
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

"""Define API Queries."""

import six

from google.api.core import page_iterator
from google.cloud.bigquery._helpers import _TypedProperty
from google.cloud.bigquery._helpers import _rows_from_json
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.job import QueryJob
from google.cloud.bigquery.table import _parse_schema_resource
from google.cloud.bigquery._helpers import QueryParametersProperty
from google.cloud.bigquery._helpers import UDFResourcesProperty
from google.cloud.bigquery._helpers import _item_to_row
from google.cloud.bigquery._helpers import _rows_page_start


class _SyncQueryConfiguration(object):
    """User-settable configuration options for synchronous query jobs.

    Values which are ``None`` -> server defaults.
    """
    _default_dataset = None
    _dry_run = None
    _max_results = None
    _timeout_ms = None
    _preserve_nulls = None
    _use_query_cache = None
    _use_legacy_sql = None


class QueryResults(object):
    """Synchronous job: query tables.

    :type query: str
    :param query: SQL query string

    :type client: :class:`google.cloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).

    :type udf_resources: tuple
    :param udf_resources: An iterable of
                        :class:`google.cloud.bigquery.job.UDFResource`
                        (empty by default)

    :type query_parameters: tuple
    :param query_parameters:
        An iterable of
        :class:`google.cloud.bigquery._helpers.AbstractQueryParameter`
        (empty by default)
    """

    _UDF_KEY = 'userDefinedFunctionResources'
    _QUERY_PARAMETERS_KEY = 'queryParameters'

    def __init__(self, query, client, udf_resources=(), query_parameters=()):
        self._client = client
        self._properties = {}
        self.query = query
        self._configuration = _SyncQueryConfiguration()
        self.udf_resources = udf_resources
        self.query_parameters = query_parameters
        self._job = None

    @classmethod
    def from_api_repr(cls, api_response, client):
        instance = cls(None, client)
        instance._set_properties(api_response)
        return instance

    @classmethod
    def from_query_job(cls, job):
        """Factory: construct from an existing job.

        :type job: :class:`~google.cloud.bigquery.job.QueryJob`
        :param job: existing job

        :rtype: :class:`QueryResults`
        :returns: the instance, bound to the job
        """
        instance = cls(job.query, job._client, job.udf_resources)
        instance._job = job
        job_ref = instance._properties.setdefault('jobReference', {})
        job_ref['jobId'] = job.name
        if job.default_dataset is not None:
            instance.default_dataset = job.default_dataset
        if job.use_query_cache is not None:
            instance.use_query_cache = job.use_query_cache
        if job.use_legacy_sql is not None:
            instance.use_legacy_sql = job.use_legacy_sql
        return instance

    @property
    def project(self):
        """Project bound to the job.

        :rtype: str
        :returns: the project (derived from the client).
        """
        return self._client.project

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: :class:`google.cloud.bigquery.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    @property
    def cache_hit(self):
        """Query results served from cache.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#cacheHit

        :rtype: bool or ``NoneType``
        :returns: True if the query results were served from cache (None
                  until set by the server).
        """
        return self._properties.get('cacheHit')

    @property
    def complete(self):
        """Server completed query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#jobComplete

        :rtype: bool or ``NoneType``
        :returns: True if the query completed on the server (None
                  until set by the server).
        """
        return self._properties.get('jobComplete')

    @property
    def errors(self):
        """Errors generated by the query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#errors

        :rtype: list of mapping, or ``NoneType``
        :returns: Mappings describing errors generated on the server (None
                  until set by the server).
        """
        return self._properties.get('errors')

    @property
    def name(self):
        """Job name, generated by the back-end.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#jobReference

        :rtype: list of mapping, or ``NoneType``
        :returns: Mappings describing errors generated on the server (None
                  until set by the server).
        """
        return self._properties.get('jobReference', {}).get('jobId')

    @property
    def job(self):
        """Job instance used to run the query.

        :rtype: :class:`google.cloud.bigquery.job.QueryJob`, or ``NoneType``
        :returns: Job instance used to run the query (None until
                  ``jobReference`` property is set by the server).
        """
        if self._job is None:
            job_ref = self._properties.get('jobReference')
            if job_ref is not None:
                self._job = QueryJob(job_ref['jobId'], self.query,
                                     self._client)
        return self._job

    @property
    def page_token(self):
        """Token for fetching next bach of results.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#pageToken

        :rtype: str, or ``NoneType``
        :returns: Token generated on the server (None until set by the server).
        """
        return self._properties.get('pageToken')

    @property
    def total_rows(self):
        """Total number of rows returned by the query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#totalRows

        :rtype: int, or ``NoneType``
        :returns: Count generated on the server (None until set by the server).
        """
        total_rows = self._properties.get('totalRows')
        if total_rows is not None:
            return int(total_rows)

    @property
    def total_bytes_processed(self):
        """Total number of bytes processed by the query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#totalBytesProcessed

        :rtype: int, or ``NoneType``
        :returns: Count generated on the server (None until set by the server).
        """
        total_bytes_processed = self._properties.get('totalBytesProcessed')
        if total_bytes_processed is not None:
            return int(total_bytes_processed)

    @property
    def num_dml_affected_rows(self):
        """Total number of rows affected by a DML query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#numDmlAffectedRows

        :rtype: int, or ``NoneType``
        :returns: Count generated on the server (None until set by the server).
        """
        num_dml_affected_rows = self._properties.get('numDmlAffectedRows')
        if num_dml_affected_rows is not None:
            return int(num_dml_affected_rows)

    @property
    def rows(self):
        """Query results.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#rows

        :rtype: list of tuples of row values, or ``NoneType``
        :returns: fields describing the schema (None until set by the server).
        """
        return _rows_from_json(self._properties.get('rows', ()), self.schema)

    @property
    def schema(self):
        """Schema for query results.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#schema

        :rtype: list of :class:`SchemaField`, or ``NoneType``
        :returns: fields describing the schema (None until set by the server).
        """
        return _parse_schema_resource(self._properties.get('schema', {}))

    default_dataset = _TypedProperty('default_dataset', Dataset)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#defaultDataset
    """

    dry_run = _TypedProperty('dry_run', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#dryRun
    """

    max_results = _TypedProperty('max_results', six.integer_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#maxResults
    """

    preserve_nulls = _TypedProperty('preserve_nulls', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#preserveNulls
    """

    query_parameters = QueryParametersProperty()

    timeout_ms = _TypedProperty('timeout_ms', six.integer_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#timeoutMs
    """

    udf_resources = UDFResourcesProperty()

    use_query_cache = _TypedProperty('use_query_cache', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#useQueryCache
    """

    use_legacy_sql = _TypedProperty('use_legacy_sql', bool)
    """See
    https://cloud.google.com/bigquery/docs/\
    reference/v2/jobs/query#useLegacySql
    """

    def _set_properties(self, api_response):
        """Update properties from resource in body of ``api_response``

        :type api_response: dict
        :param api_response: response returned from an API call
        """
        self._properties.clear()
        self._properties.update(api_response)

    def _build_resource(self):
        """Generate a resource for :meth:`begin`."""
        resource = {'query': self.query}

        if self.default_dataset is not None:
            resource['defaultDataset'] = {
                'projectId': self.project,
                'datasetId': self.default_dataset.name,
            }

        if self.max_results is not None:
            resource['maxResults'] = self.max_results

        if self.preserve_nulls is not None:
            resource['preserveNulls'] = self.preserve_nulls

        if self.timeout_ms is not None:
            resource['timeoutMs'] = self.timeout_ms

        if self.use_query_cache is not None:
            resource['useQueryCache'] = self.use_query_cache

        if self.use_legacy_sql is not None:
            resource['useLegacySql'] = self.use_legacy_sql

        if self.dry_run is not None:
            resource['dryRun'] = self.dry_run

        if len(self._udf_resources) > 0:
            resource[self._UDF_KEY] = [
                {udf_resource.udf_type: udf_resource.value}
                for udf_resource in self._udf_resources
            ]
        if len(self._query_parameters) > 0:
            resource[self._QUERY_PARAMETERS_KEY] = [
                query_parameter.to_api_repr()
                for query_parameter in self._query_parameters
            ]
            if self._query_parameters[0].name is None:
                resource['parameterMode'] = 'POSITIONAL'
            else:
                resource['parameterMode'] = 'NAMED'

        return resource

    def run(self, client=None):
        """API call:  run the query via a POST request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        if self.job is not None:
            raise ValueError("Query job is already running.")

        client = self._require_client(client)
        path = '/projects/%s/queries' % (self.project,)
        api_response = client._connection.api_request(
            method='POST', path=path, data=self._build_resource())
        self._set_properties(api_response)

    def fetch_data(self, max_results=None, page_token=None, start_index=None,
                   timeout_ms=None, client=None):
        """API call:  fetch a page of query result data via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults

        :type max_results: int
        :param max_results: (Optional) maximum number of rows to return.

        :type page_token: str
        :param page_token:
            (Optional) token representing a cursor into the table's rows.

        :type start_index: int
        :param start_index: (Optional) zero-based index of starting row

        :type timeout_ms: int
        :param timeout_ms:
            (Optional) How long to wait for the query to complete, in
            milliseconds, before the request times out and returns. Note that
            this is only a timeout for the request, not the query. If the query
            takes longer to run than the timeout value, the call returns
            without any results and with the 'jobComplete' flag set to false.
            You can call GetQueryResults() to wait for the query to complete
            and read the results. The default value is 10000 milliseconds (10
            seconds).

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: :class:`~google.api.core.page_iterator.Iterator`
        :returns: Iterator of row data :class:`tuple`s. During each page, the
                  iterator will have the ``total_rows`` attribute set,
                  which counts the total number of rows **in the result
                  set** (this is distinct from the total number of rows in
                  the current page: ``iterator.page.num_items``).
        :raises: ValueError if the query has not yet been executed.
        """
        if self.name is None:
            raise ValueError("Query not yet executed:  call 'run()'")

        client = self._require_client(client)
        params = {}

        if start_index is not None:
            params['startIndex'] = start_index

        if timeout_ms is not None:
            params['timeoutMs'] = timeout_ms

        if max_results is not None:
            params['maxResults'] = max_results

        path = '/projects/%s/queries/%s' % (self.project, self.name)
        iterator = page_iterator.HTTPIterator(
            client=client,
            api_request=client._connection.api_request,
            path=path,
            item_to_value=_item_to_row,
            items_key='rows',
            page_token=page_token,
            page_start=_rows_page_start_query,
            next_token='pageToken',
            extra_params=params)
        iterator.query_result = self
        return iterator


def _rows_page_start_query(iterator, page, response):
    """Update query response when :class:`~google.cloud.iterator.Page` starts.

    .. note::

        This assumes that the ``query_response`` attribute has been
        added to the iterator after being created, which
        should be done by the caller.

    :type iterator: :class:`~google.api.core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type page: :class:`~google.cloud.iterator.Page`
    :param page: The page that was just created.

    :type response: dict
    :param response: The JSON API response for a page of rows in a table.
    """
    iterator.query_result._set_properties(response)
    iterator.schema = iterator.query_result.schema
    _rows_page_start(iterator, page, response)
