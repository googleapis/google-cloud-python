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

"""Define API Datasets."""

import datetime
import json
import os

import httplib2
import six

from google.cloud._helpers import _datetime_from_microseconds
from google.cloud._helpers import _microseconds_from_datetime
from google.cloud._helpers import _millis_from_datetime
from google.cloud.exceptions import NotFound
from google.cloud.exceptions import make_exception
from google.cloud.streaming.exceptions import HttpError
from google.cloud.streaming.http_wrapper import Request
from google.cloud.streaming.http_wrapper import make_api_request
from google.cloud.streaming.transfer import RESUMABLE_UPLOAD
from google.cloud.streaming.transfer import Upload
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery._helpers import _row_from_json
from google.cloud.iterator import HTTPIterator


_TABLE_HAS_NO_SCHEMA = "Table has no schema:  call 'table.reload()'"
_MARKER = object()


class Table(object):
    """Tables represent a set of rows whose values correspond to a schema.

    See:
    https://cloud.google.com/bigquery/docs/reference/v2/tables

    :type name: str
    :param name: the name of the table

    :type dataset: :class:`google.cloud.bigquery.dataset.Dataset`
    :param dataset: The dataset which contains the table.

    :type schema: list of :class:`SchemaField`
    :param schema: The table's schema
    """

    _schema = None

    def __init__(self, name, dataset, schema=()):
        self.name = name
        self._dataset = dataset
        self._properties = {}
        # Let the @property do validation.
        self.schema = schema

    @property
    def project(self):
        """Project bound to the table.

        :rtype: str
        :returns: the project (derived from the dataset).
        """
        return self._dataset.project

    @property
    def dataset_name(self):
        """Name of dataset containing the table.

        :rtype: str
        :returns: the ID (derived from the dataset).
        """
        return self._dataset.name

    @property
    def path(self):
        """URL path for the table's APIs.

        :rtype: str
        :returns: the path based on project and dataste name.
        """
        return '%s/tables/%s' % (self._dataset.path, self.name)

    @property
    def schema(self):
        """Table's schema.

        :rtype: list of :class:`SchemaField`
        :returns: fields describing the schema
        """
        return list(self._schema)

    @schema.setter
    def schema(self, value):
        """Update table's schema

        :type value: list of :class:`SchemaField`
        :param value: fields describing the schema

        :raises: TypeError if 'value' is not a sequence, or ValueError if
                 any item in the sequence is not a SchemaField
        """
        if not all(isinstance(field, SchemaField) for field in value):
            raise ValueError('Schema items must be fields')
        self._schema = tuple(value)

    @property
    def created(self):
        """Datetime at which the table was created.

        :rtype: ``datetime.datetime``, or ``NoneType``
        :returns: the creation time (None until set from the server).
        """
        creation_time = self._properties.get('creationTime')
        if creation_time is not None:
            # creation_time will be in milliseconds.
            return _datetime_from_microseconds(1000.0 * creation_time)

    @property
    def etag(self):
        """ETag for the table resource.

        :rtype: str, or ``NoneType``
        :returns: the ETag (None until set from the server).
        """
        return self._properties.get('etag')

    @property
    def modified(self):
        """Datetime at which the table was last modified.

        :rtype: ``datetime.datetime``, or ``NoneType``
        :returns: the modification time (None until set from the server).
        """
        modified_time = self._properties.get('lastModifiedTime')
        if modified_time is not None:
            # modified_time will be in milliseconds.
            return _datetime_from_microseconds(1000.0 * modified_time)

    @property
    def num_bytes(self):
        """The size of the table in bytes.

        :rtype: int, or ``NoneType``
        :returns: the byte count (None until set from the server).
        """
        num_bytes_as_str = self._properties.get('numBytes')
        if num_bytes_as_str is not None:
            return int(num_bytes_as_str)

    @property
    def num_rows(self):
        """The number of rows in the table.

        :rtype: int, or ``NoneType``
        :returns: the row count (None until set from the server).
        """
        num_rows_as_str = self._properties.get('numRows')
        if num_rows_as_str is not None:
            return int(num_rows_as_str)

    @property
    def self_link(self):
        """URL for the table resource.

        :rtype: str, or ``NoneType``
        :returns: the URL (None until set from the server).
        """
        return self._properties.get('selfLink')

    @property
    def table_id(self):
        """ID for the table resource.

        :rtype: str, or ``NoneType``
        :returns: the ID (None until set from the server).
        """
        return self._properties.get('id')

    @property
    def table_type(self):
        """The type of the table.

        Possible values are "TABLE" or "VIEW".

        :rtype: str, or ``NoneType``
        :returns: the URL (None until set from the server).
        """
        return self._properties.get('type')

    @property
    def partitioning_type(self):
        """Time partitioning of the table.
        :rtype: str, or ``NoneType``
        :returns: Returns type if the table is partitioned, None otherwise.
        """
        return self._properties.get('timePartitioning', {}).get('type')

    @partitioning_type.setter
    def partitioning_type(self, value):
        """Update the partitioning type of the table

        :type value: str
        :param value: partitioning type only "DAY" is currently supported
        """
        if value not in ('DAY', None):
            raise ValueError("value must be one of ['DAY', None]")

        if value is None:
            self._properties.pop('timePartitioning', None)
        else:
            time_part = self._properties.setdefault('timePartitioning', {})
            time_part['type'] = value.upper()

    @property
    def partition_expiration(self):
        """Expiration time in ms for a partition
        :rtype: int, or ``NoneType``
        :returns: Returns the time in ms for partition expiration
        """
        return self._properties.get('timePartitioning', {}).get('expirationMs')

    @partition_expiration.setter
    def partition_expiration(self, value):
        """Update the experation time in ms for a partition

        :type value: int
        :param value: partition experiation time in ms
        """
        if not isinstance(value, (int, type(None))):
            raise ValueError(
                "must be an integer representing millisseconds or None")

        if value is None:
            if 'timePartitioning' in self._properties:
                self._properties['timePartitioning'].pop('expirationMs')
        else:
            try:
                self._properties['timePartitioning']['expirationMs'] = value
            except KeyError:
                self._properties['timePartitioning'] = {'type': 'DAY'}
                self._properties['timePartitioning']['expirationMs'] = value

    @property
    def description(self):
        """Description of the table.

        :rtype: str, or ``NoneType``
        :returns: The description as set by the user, or None (the default).
        """
        return self._properties.get('description')

    @description.setter
    def description(self, value):
        """Update description of the table.

        :type value: str
        :param value: (Optional) new description

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['description'] = value

    @property
    def expires(self):
        """Datetime at which the table will be removed.

        :rtype: ``datetime.datetime``, or ``NoneType``
        :returns: the expiration time, or None
        """
        expiration_time = self._properties.get('expirationTime')
        if expiration_time is not None:
            # expiration_time will be in milliseconds.
            return _datetime_from_microseconds(1000.0 * expiration_time)

    @expires.setter
    def expires(self, value):
        """Update datetime at which the table will be removed.

        :type value: ``datetime.datetime``
        :param value: (Optional) the new expiration time, or None
        """
        if not isinstance(value, datetime.datetime) and value is not None:
            raise ValueError("Pass a datetime, or None")
        self._properties['expirationTime'] = _millis_from_datetime(value)

    @property
    def friendly_name(self):
        """Title of the table.

        :rtype: str, or ``NoneType``
        :returns: The name as set by the user, or None (the default).
        """
        return self._properties.get('friendlyName')

    @friendly_name.setter
    def friendly_name(self, value):
        """Update title of the table.

        :type value: str
        :param value: (Optional) new title

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['friendlyName'] = value

    @property
    def location(self):
        """Location in which the table is hosted.

        :rtype: str, or ``NoneType``
        :returns: The location as set by the user, or None (the default).
        """
        return self._properties.get('location')

    @location.setter
    def location(self, value):
        """Update location in which the table is hosted.

        :type value: str
        :param value: (Optional) new location

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['location'] = value

    @property
    def view_query(self):
        """SQL query defining the table as a view.

        :rtype: str, or ``NoneType``
        :returns: The query as set by the user, or None (the default).
        """
        view = self._properties.get('view')
        if view is not None:
            return view.get('query')

    @view_query.setter
    def view_query(self, value):
        """Update SQL query defining the table as a view.

        :type value: str
        :param value: new query

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types):
            raise ValueError("Pass a string")
        self._properties['view'] = {'query': value}

    @view_query.deleter
    def view_query(self):
        """Delete SQL query defining the table as a view."""
        self._properties.pop('view', None)

    def list_partitions(self, client=None):
        """List the partitions in a table.

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: list
        :returns: a list of time partitions
        """
        query = self._require_client(client).run_sync_query(
            'SELECT partition_id from [%s.%s$__PARTITIONS_SUMMARY__]' %
            (self.dataset_name, self.name))
        query.run()
        return [row[0] for row in query.rows]

    @classmethod
    def from_api_repr(cls, resource, dataset):
        """Factory:  construct a table given its API representation

        :type resource: dict
        :param resource: table resource representation returned from the API

        :type dataset: :class:`google.cloud.bigquery.dataset.Dataset`
        :param dataset: The dataset containing the table.

        :rtype: :class:`google.cloud.bigquery.table.Table`
        :returns: Table parsed from ``resource``.
        """
        if ('tableReference' not in resource or
                'tableId' not in resource['tableReference']):
            raise KeyError('Resource lacks required identity information:'
                           '["tableReference"]["tableId"]')
        table_name = resource['tableReference']['tableId']
        table = cls(table_name, dataset=dataset)
        table._set_properties(resource)
        return table

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
            client = self._dataset._client
        return client

    def _set_properties(self, api_response):
        """Update properties from resource in body of ``api_response``

        :type api_response: httplib2.Response
        :param api_response: response returned from an API call
        """
        self._properties.clear()
        cleaned = api_response.copy()
        schema = cleaned.pop('schema', {'fields': ()})
        self.schema = _parse_schema_resource(schema)
        if 'creationTime' in cleaned:
            cleaned['creationTime'] = float(cleaned['creationTime'])
        if 'lastModifiedTime' in cleaned:
            cleaned['lastModifiedTime'] = float(cleaned['lastModifiedTime'])
        if 'expirationTime' in cleaned:
            cleaned['expirationTime'] = float(cleaned['expirationTime'])
        self._properties.update(cleaned)

    def _build_resource(self):
        """Generate a resource for ``create`` or ``update``."""
        resource = {
            'tableReference': {
                'projectId': self._dataset.project,
                'datasetId': self._dataset.name,
                'tableId': self.name},
        }
        if self.description is not None:
            resource['description'] = self.description

        if self.expires is not None:
            value = _millis_from_datetime(self.expires)
            resource['expirationTime'] = value

        if self.friendly_name is not None:
            resource['friendlyName'] = self.friendly_name

        if self.location is not None:
            resource['location'] = self.location

        if self.partitioning_type is not None:
            resource['timePartitioning'] = self._properties['timePartitioning']

        if self.view_query is not None:
            view = resource['view'] = {}
            view['query'] = self.view_query
        elif self._schema:
            resource['schema'] = {
                'fields': _build_schema_resource(self._schema)
            }
        else:
            raise ValueError("Set either 'view_query' or 'schema'.")

        return resource

    def create(self, client=None):
        """API call:  create the dataset via a PUT request

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/tables/insert

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        path = '/projects/%s/datasets/%s/tables' % (
            self._dataset.project, self._dataset.name)
        api_response = client._connection.api_request(
            method='POST', path=path, data=self._build_resource())
        self._set_properties(api_response)

    def exists(self, client=None):
        """API call:  test for the existence of the table via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/tables/get

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: bool
        :returns: Boolean indicating existence of the table.
        """
        client = self._require_client(client)

        try:
            client._connection.api_request(method='GET', path=self.path,
                                           query_params={'fields': 'id'})
        except NotFound:
            return False
        else:
            return True

    def reload(self, client=None):
        """API call:  refresh table properties via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/tables/get

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)

        api_response = client._connection.api_request(
            method='GET', path=self.path)
        self._set_properties(api_response)

    def patch(self,
              client=None,
              friendly_name=_MARKER,
              description=_MARKER,
              location=_MARKER,
              expires=_MARKER,
              view_query=_MARKER,
              schema=_MARKER):
        """API call:  update individual table properties via a PATCH request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/tables/patch

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :type friendly_name: str
        :param friendly_name: (Optional) a descriptive name for this table.

        :type description: str
        :param description: (Optional) a description of this table.

        :type location: str
        :param location:
            (Optional) the geographic location where the table resides.

        :type expires: :class:`datetime.datetime`
        :param expires: (Optional) point in time at which the table expires.

        :type view_query: str
        :param view_query: SQL query defining the table as a view

        :type schema: list of :class:`SchemaField`
        :param schema: fields describing the schema

        :raises: ValueError for invalid value types.
        """
        client = self._require_client(client)

        partial = {}

        if expires is not _MARKER:
            if (not isinstance(expires, datetime.datetime) and
                    expires is not None):
                raise ValueError("Pass a datetime, or None")
            partial['expirationTime'] = _millis_from_datetime(expires)

        if description is not _MARKER:
            partial['description'] = description

        if friendly_name is not _MARKER:
            partial['friendlyName'] = friendly_name

        if location is not _MARKER:
            partial['location'] = location

        if view_query is not _MARKER:
            if view_query is None:
                partial['view'] = None
            else:
                partial['view'] = {'query': view_query}

        if schema is not _MARKER:
            if schema is None:
                partial['schema'] = None
            else:
                partial['schema'] = {
                    'fields': _build_schema_resource(schema)}

        api_response = client._connection.api_request(
            method='PATCH', path=self.path, data=partial)
        self._set_properties(api_response)

    def update(self, client=None):
        """API call:  update table properties via a PUT request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/tables/update

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        api_response = client._connection.api_request(
            method='PUT', path=self.path, data=self._build_resource())
        self._set_properties(api_response)

    def delete(self, client=None):
        """API call:  delete the table via a DELETE request

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/tables/delete

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        client._connection.api_request(method='DELETE', path=self.path)

    def fetch_data(self, max_results=None, page_token=None, client=None):
        """API call:  fetch the table data via a GET request

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/tabledata/list

        .. note::

           This method assumes that its instance's ``schema`` attribute is
           up-to-date with the schema as defined on the back-end:  if the
           two schemas are not identical, the values returned may be
           incomplete.  To ensure that the local copy of the schema is
           up-to-date, call :meth:`reload`.

        :type max_results: int
        :param max_results: (Optional) Maximum number of rows to return.

        :type page_token: str
        :param page_token: (Optional) Token representing a cursor into the
                           table's rows.

        :type client: :class:`~google.cloud.bigquery.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls
                       back to the ``client`` stored on the current dataset.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns: Iterator of row data :class:`tuple`s. During each page, the
                  iterator will have the ``total_rows`` attribute set,
                  which counts the total number of rows **in the table**
                  (this is distinct from the total number of rows in the
                  current page: ``iterator.page.num_items``).
        """
        client = self._require_client(client)
        path = '%s/data' % (self.path,)
        iterator = HTTPIterator(client=client, path=path,
                                item_to_value=_item_to_row, items_key='rows',
                                page_token=page_token, max_results=max_results,
                                page_start=_rows_page_start)
        iterator.schema = self._schema
        # Over-ride the key used to retrieve the next page token.
        iterator._NEXT_TOKEN = 'pageToken'
        return iterator

    def insert_data(self,
                    rows,
                    row_ids=None,
                    skip_invalid_rows=None,
                    ignore_unknown_values=None,
                    template_suffix=None,
                    client=None):
        """API call:  insert table data via a POST request

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/tabledata/insertAll

        :type rows: list of tuples
        :param rows: Row data to be inserted. Each tuple should contain data
                     for each schema field on the current table and in the
                     same order as the schema fields.

        :type row_ids: list of string
        :param row_ids: Unique ids, one per row being inserted.  If not
                        passed, no de-duplication occurs.

        :type skip_invalid_rows: bool
        :param skip_invalid_rows: (Optional) skip rows w/ invalid data?

        :type ignore_unknown_values: bool
        :param ignore_unknown_values: (Optional) ignore columns beyond schema?

        :type template_suffix: str
        :param template_suffix:
            (Optional) treat ``name`` as a template table and provide a suffix.
            BigQuery will create the table ``<name> + <template_suffix>`` based
            on the schema of the template table. See:
            https://cloud.google.com/bigquery/streaming-data-into-bigquery#template-tables

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: list of mappings
        :returns: One mapping per row with insert errors:  the "index" key
                  identifies the row, and the "errors" key contains a list
                  of the mappings describing one or more problems with the
                  row.
        :raises: ValueError if table's schema is not set
        """
        if len(self._schema) == 0:
            raise ValueError(_TABLE_HAS_NO_SCHEMA)

        client = self._require_client(client)
        rows_info = []
        data = {'rows': rows_info}

        for index, row in enumerate(rows):
            row_info = {}

            for field, value in zip(self._schema, row):
                if field.field_type == 'TIMESTAMP':
                    # BigQuery stores TIMESTAMP data internally as a
                    # UNIX timestamp with microsecond precision.
                    # Specifies the number of seconds since the epoch.
                    value = _convert_timestamp(value)
                row_info[field.name] = value

            info = {'json': row_info}
            if row_ids is not None:
                info['insertId'] = row_ids[index]

            rows_info.append(info)

        if skip_invalid_rows is not None:
            data['skipInvalidRows'] = skip_invalid_rows

        if ignore_unknown_values is not None:
            data['ignoreUnknownValues'] = ignore_unknown_values

        if template_suffix is not None:
            data['templateSuffix'] = template_suffix

        response = client._connection.api_request(
            method='POST',
            path='%s/insertAll' % self.path,
            data=data)
        errors = []

        for error in response.get('insertErrors', ()):
            errors.append({'index': int(error['index']),
                           'errors': error['errors']})

        return errors

    @staticmethod
    def _check_response_error(request, http_response):
        """Helper for :meth:`upload_from_file`."""
        info = http_response.info
        status = int(info['status'])
        if not 200 <= status < 300:
            faux_response = httplib2.Response({'status': status})
            raise make_exception(faux_response, http_response.content,
                                 error_info=request.url)

    # pylint: disable=too-many-arguments,too-many-locals
    def upload_from_file(self,
                         file_obj,
                         source_format,
                         rewind=False,
                         size=None,
                         num_retries=6,
                         allow_jagged_rows=None,
                         allow_quoted_newlines=None,
                         create_disposition=None,
                         encoding=None,
                         field_delimiter=None,
                         ignore_unknown_values=None,
                         max_bad_records=None,
                         quote_character=None,
                         skip_leading_rows=None,
                         write_disposition=None,
                         client=None):
        """Upload the contents of this table from a file-like object.

        The content type of the upload will either be
        - The value passed in to the function (if any)
        - ``text/csv``.

        :type file_obj: file
        :param file_obj: A file handle opened in binary mode for reading.

        :type source_format: str
        :param source_format: one of 'CSV' or 'NEWLINE_DELIMITED_JSON'.
                              job configuration option; see
                              :meth:`google.cloud.bigquery.job.LoadJob`

        :type rewind: bool
        :param rewind: If True, seek to the beginning of the file handle before
                       writing the file to Cloud Storage.

        :type size: int
        :param size: The number of bytes to read from the file handle.
                     If not provided, we'll try to guess the size using
                     :func:`os.fstat`. (If the file handle is not from the
                     filesystem this won't be possible.)

        :type num_retries: int
        :param num_retries: Number of upload retries. Defaults to 6.

        :type allow_jagged_rows: bool
        :param allow_jagged_rows: job configuration option;  see
                                  :meth:`google.cloud.bigquery.job.LoadJob`.

        :type allow_quoted_newlines: bool
        :param allow_quoted_newlines: job configuration option; see
                                      :meth:`google.cloud.bigquery.job.LoadJob`.

        :type create_disposition: str
        :param create_disposition: job configuration option; see
                                   :meth:`google.cloud.bigquery.job.LoadJob`.

        :type encoding: str
        :param encoding: job configuration option; see
                         :meth:`google.cloud.bigquery.job.LoadJob`.

        :type field_delimiter: str
        :param field_delimiter: job configuration option; see
                                :meth:`google.cloud.bigquery.job.LoadJob`.

        :type ignore_unknown_values: bool
        :param ignore_unknown_values: job configuration option; see
                                      :meth:`google.cloud.bigquery.job.LoadJob`.

        :type max_bad_records: int
        :param max_bad_records: job configuration option; see
                                :meth:`google.cloud.bigquery.job.LoadJob`.

        :type quote_character: str
        :param quote_character: job configuration option; see
                                :meth:`google.cloud.bigquery.job.LoadJob`.

        :type skip_leading_rows: int
        :param skip_leading_rows: job configuration option; see
                                  :meth:`google.cloud.bigquery.job.LoadJob`.

        :type write_disposition: str
        :param write_disposition: job configuration option; see
                                  :meth:`google.cloud.bigquery.job.LoadJob`.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current dataset.

        :rtype: :class:`google.cloud.bigquery.jobs.LoadTableFromStorageJob`
        :returns: the job instance used to load the data (e.g., for
                  querying status). Note that the job is already started:
                  do not call ``job.begin()``.
        :raises: :class:`ValueError` if ``size`` is not passed in and can not
                 be determined, or if the ``file_obj`` can be detected to be
                 a file opened in text mode.
        """
        client = self._require_client(client)
        connection = client._connection
        content_type = 'application/octet-stream'

        # Rewind the file if desired.
        if rewind:
            file_obj.seek(0, os.SEEK_SET)

        mode = getattr(file_obj, 'mode', None)

        if mode is not None and mode not in ('rb', 'r+b', 'rb+'):
            raise ValueError(
                "Cannot upload files opened in text mode:  use "
                "open(filename, mode='rb') or open(filename, mode='r+b')")

        # Get the basic stats about the file.
        total_bytes = size
        if total_bytes is None:
            if hasattr(file_obj, 'fileno'):
                total_bytes = os.fstat(file_obj.fileno()).st_size
            else:
                raise ValueError('total bytes could not be determined. Please '
                                 'pass an explicit size.')
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': connection.USER_AGENT,
            'content-type': 'application/json',
        }

        metadata = {
            'configuration': {
                'load': {
                    'sourceFormat': source_format,
                    'schema': {
                        'fields': _build_schema_resource(self._schema),
                    },
                    'destinationTable': {
                        'projectId': self._dataset.project,
                        'datasetId': self._dataset.name,
                        'tableId': self.name,
                    }
                }
            }
        }

        _configure_job_metadata(metadata, allow_jagged_rows,
                                allow_quoted_newlines, create_disposition,
                                encoding, field_delimiter,
                                ignore_unknown_values, max_bad_records,
                                quote_character, skip_leading_rows,
                                write_disposition)

        upload = Upload(file_obj, content_type, total_bytes,
                        auto_transfer=False)

        url_builder = _UrlBuilder()
        upload_config = _UploadConfig()

        # Base URL may change once we know simple vs. resumable.
        base_url = connection.API_BASE_URL + '/upload'
        path = '/projects/%s/jobs' % (self._dataset.project,)
        upload_url = connection.build_api_url(api_base_url=base_url, path=path)

        # Use apitools 'Upload' facility.
        request = Request(upload_url, 'POST', headers,
                          body=json.dumps(metadata))

        upload.configure_request(upload_config, request, url_builder)
        query_params = url_builder.query_params
        base_url = connection.API_BASE_URL + '/upload'
        request.url = connection.build_api_url(api_base_url=base_url,
                                               path=path,
                                               query_params=query_params)
        try:
            upload.initialize_upload(request, connection.http)
        except HttpError as err_response:
            faux_response = httplib2.Response(err_response.response)
            raise make_exception(faux_response, err_response.content,
                                 error_info=request.url)

        if upload.strategy == RESUMABLE_UPLOAD:
            http_response = upload.stream_file(use_chunks=True)
        else:
            http_response = make_api_request(connection.http, request,
                                             retries=num_retries)

        self._check_response_error(request, http_response)

        response_content = http_response.content
        if not isinstance(response_content,
                          six.string_types):  # pragma: NO COVER  Python3
            response_content = response_content.decode('utf-8')
        return client.job_from_resource(json.loads(response_content))
    # pylint: enable=too-many-arguments,too-many-locals


def _configure_job_metadata(metadata,  # pylint: disable=too-many-arguments
                            allow_jagged_rows,
                            allow_quoted_newlines,
                            create_disposition,
                            encoding,
                            field_delimiter,
                            ignore_unknown_values,
                            max_bad_records,
                            quote_character,
                            skip_leading_rows,
                            write_disposition):
    """Helper for :meth:`Table.upload_from_file`."""
    load_config = metadata['configuration']['load']

    if allow_jagged_rows is not None:
        load_config['allowJaggedRows'] = allow_jagged_rows

    if allow_quoted_newlines is not None:
        load_config['allowQuotedNewlines'] = allow_quoted_newlines

    if create_disposition is not None:
        load_config['createDisposition'] = create_disposition

    if encoding is not None:
        load_config['encoding'] = encoding

    if field_delimiter is not None:
        load_config['fieldDelimiter'] = field_delimiter

    if ignore_unknown_values is not None:
        load_config['ignoreUnknownValues'] = ignore_unknown_values

    if max_bad_records is not None:
        load_config['maxBadRecords'] = max_bad_records

    if quote_character is not None:
        load_config['quote'] = quote_character

    if skip_leading_rows is not None:
        load_config['skipLeadingRows'] = skip_leading_rows

    if write_disposition is not None:
        load_config['writeDisposition'] = write_disposition


def _parse_schema_resource(info):
    """Parse a resource fragment into a schema field.

    :type info: mapping
    :param info: should contain a "fields" key to be parsed

    :rtype: list of :class:`SchemaField`, or ``NoneType``
    :returns: a list of parsed fields, or ``None`` if no "fields" key is
                present in ``info``.
    """
    if 'fields' not in info:
        return None

    schema = []
    for r_field in info['fields']:
        name = r_field['name']
        field_type = r_field['type']
        mode = r_field.get('mode', 'NULLABLE')
        description = r_field.get('description')
        sub_fields = _parse_schema_resource(r_field)
        schema.append(
            SchemaField(name, field_type, mode, description, sub_fields))
    return schema


def _build_schema_resource(fields):
    """Generate a resource fragment for a schema.

    :type fields: sequence of :class:`SchemaField`
    :param fields: schema to be dumped

    :rtype: mapping
    :returns: a mapping describing the schema of the supplied fields.
    """
    infos = []
    for field in fields:
        info = {'name': field.name,
                'type': field.field_type,
                'mode': field.mode}
        if field.description is not None:
            info['description'] = field.description
        if field.fields is not None:
            info['fields'] = _build_schema_resource(field.fields)
        infos.append(info)
    return infos


def _item_to_row(iterator, resource):
    """Convert a JSON row to the native object.

    .. note::

        This assumes that the ``schema`` attribute has been
        added to the iterator after being created, which
        should be done by the caller.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: An item to be converted to a row.

    :rtype: tuple
    :returns: The next row in the page.
    """
    return _row_from_json(resource, iterator.schema)


# pylint: disable=unused-argument
def _rows_page_start(iterator, page, response):
    """Grab total rows after a :class:`~google.cloud.iterator.Page` started.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type page: :class:`~google.cloud.iterator.Page`
    :param page: The page that was just created.

    :type response: dict
    :param response: The JSON API response for a page of rows in a table.
    """
    total_rows = response.get('totalRows')
    if total_rows is not None:
        total_rows = int(total_rows)
    iterator.total_rows = total_rows
# pylint: enable=unused-argument


class _UploadConfig(object):
    """Faux message FBO apitools' 'configure_request'."""
    accept = ['*/*']
    max_size = None
    resumable_multipart = True
    resumable_path = u'/upload/bigquery/v2/projects/{project}/jobs'
    simple_multipart = True
    simple_path = u'/upload/bigquery/v2/projects/{project}/jobs'


class _UrlBuilder(object):
    """Faux builder FBO apitools' 'configure_request'"""
    def __init__(self):
        self.query_params = {}
        self._relative_path = ''


def _convert_timestamp(value):
    """Helper for :meth:`Table.insert_data`."""
    if isinstance(value, datetime.datetime):
        value = _microseconds_from_datetime(value) * 1e-6
    return value
