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
import os

import six

from google import resumable_media
from google.resumable_media.requests import MultipartUpload
from google.resumable_media.requests import ResumableUpload

from google.api_core import page_iterator
from google.cloud import exceptions
from google.cloud._helpers import _datetime_from_microseconds
from google.cloud._helpers import _millis_from_datetime
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery._helpers import _item_to_row
from google.cloud.bigquery._helpers import _rows_page_start
from google.cloud.bigquery._helpers import _SCALAR_VALUE_TO_JSON_ROW


_TABLE_HAS_NO_SCHEMA = "Table has no schema:  call 'table.reload()'"
_MARKER = object()
_DEFAULT_CHUNKSIZE = 1048576  # 1024 * 1024 B = 1 MB
_BASE_UPLOAD_TEMPLATE = (
    u'https://www.googleapis.com/upload/bigquery/v2/projects/'
    u'{project}/jobs?uploadType=')
_MULTIPART_URL_TEMPLATE = _BASE_UPLOAD_TEMPLATE + u'multipart'
_RESUMABLE_URL_TEMPLATE = _BASE_UPLOAD_TEMPLATE + u'resumable'
_GENERIC_CONTENT_TYPE = u'*/*'
_READ_LESS_THAN_SIZE = (
    'Size {:d} was specified but the file-like object only had '
    '{:d} bytes remaining.')
_DEFAULT_NUM_RETRIES = 6


class Table(object):
    """Tables represent a set of rows whose values correspond to a schema.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables

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

        Possible values are "TABLE", "VIEW", or "EXTERNAL".

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
        if self._properties.get('view') is None:
            self._properties['view'] = {}
        self._properties['view']['query'] = value

    @view_query.deleter
    def view_query(self):
        """Delete SQL query defining the table as a view."""
        self._properties.pop('view', None)

    @property
    def view_use_legacy_sql(self):
        """Specifies whether to execute the view with legacy or standard SQL.

        If not set, None is returned. BigQuery's default mode is equivalent to
        useLegacySql = True.

        :rtype: bool, or ``NoneType``
        :returns: The boolean for view.useLegacySql as set by the user, or
                  None (the default).
        """
        view = self._properties.get('view')
        if view is not None:
            return view.get('useLegacySql')

    @view_use_legacy_sql.setter
    def view_use_legacy_sql(self, value):
        """Update the view sub-property 'useLegacySql'.

        This boolean specifies whether to execute the view with legacy SQL
        (True) or standard SQL (False). The default, if not specified, is
        'True'.

        :type value: bool
        :param value: The boolean for view.useLegacySql

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, bool):
            raise ValueError("Pass a boolean")
        if self._properties.get('view') is None:
            self._properties['view'] = {}
        self._properties['view']['useLegacySql'] = value

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

        :type api_response: dict
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
            if self.view_use_legacy_sql is not None:
                view['useLegacySql'] = self.view_use_legacy_sql

        if self._schema:
            resource['schema'] = {
                'fields': _build_schema_resource(self._schema)
            }

        return resource

    def create(self, client=None):
        """API call:  create the table via a PUT request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert

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
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/get

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
        except exceptions.NotFound:
            return False
        else:
            return True

    def reload(self, client=None):
        """API call:  refresh table properties via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/get

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
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch

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
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/update

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

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        client._connection.api_request(method='DELETE', path=self.path)

    def fetch_data(self, max_results=None, page_token=None, client=None):
        """API call:  fetch the table data via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list

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

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of row data :class:`tuple`s. During each page, the
                  iterator will have the ``total_rows`` attribute set,
                  which counts the total number of rows **in the table**
                  (this is distinct from the total number of rows in the
                  current page: ``iterator.page.num_items``).
        """
        if len(self._schema) == 0:
            raise ValueError(_TABLE_HAS_NO_SCHEMA)

        params = {}

        if max_results is not None:
            params['maxResults'] = max_results

        client = self._require_client(client)
        path = '%s/data' % (self.path,)
        iterator = page_iterator.HTTPIterator(
            client=client,
            api_request=client._connection.api_request,
            path=path,
            item_to_value=_item_to_row,
            items_key='rows',
            page_token=page_token,
            page_start=_rows_page_start,
            next_token='pageToken',
            extra_params=params)
        iterator.schema = self._schema
        return iterator

    def row_from_mapping(self, mapping):
        """Convert a mapping to a row tuple using the schema.

        :type mapping: dict
        :param mapping: Mapping of row data: must contain keys for all
               required fields in the schema.  Keys which do not correspond
               to a field in the schema are ignored.

        :rtype: tuple
        :returns: Tuple whose elements are ordered according to the table's
                  schema.
        :raises: ValueError if table's schema is not set
        """
        if len(self._schema) == 0:
            raise ValueError(_TABLE_HAS_NO_SCHEMA)

        row = []
        for field in self.schema:
            if field.mode == 'REQUIRED':
                row.append(mapping[field.name])
            elif field.mode == 'REPEATED':
                row.append(mapping.get(field.name, ()))
            elif field.mode == 'NULLABLE':
                row.append(mapping.get(field.name))
            else:
                raise ValueError(
                    "Unknown field mode: {}".format(field.mode))
        return tuple(row)

    def insert_data(self,
                    rows,
                    row_ids=None,
                    skip_invalid_rows=None,
                    ignore_unknown_values=None,
                    template_suffix=None,
                    client=None):
        """API call:  insert table data via a POST request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/insertAll

        :type rows: list of tuples
        :param rows: Row data to be inserted. Each tuple should contain data
                     for each schema field on the current table and in the
                     same order as the schema fields.

        :type row_ids: list of string
        :param row_ids: Unique ids, one per row being inserted.  If not
                        passed, no de-duplication occurs.

        :type skip_invalid_rows: bool
        :param skip_invalid_rows: (Optional)  Insert all valid rows of a
                                  request, even if invalid rows exist.
                                  The default value is False, which causes
                                  the entire request to fail if any invalid
                                  rows exist.

        :type ignore_unknown_values: bool
        :param ignore_unknown_values: (Optional) Accept rows that contain
                                      values that do not match the schema.
                                      The unknown values are ignored. Default
                                      is False, which treats unknown values as
                                      errors.

        :type template_suffix: str
        :param template_suffix:
            (Optional) treat ``name`` as a template table and provide a suffix.
            BigQuery will create the table ``<name> + <template_suffix>`` based
            on the schema of the template table. See
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
                converter = _SCALAR_VALUE_TO_JSON_ROW.get(field.field_type)
                if converter is not None:  # STRING doesn't need converting
                    value = converter(value)
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

    def _get_transport(self, client):
        """Return the client's transport.

        :type client: :class:`~google.cloud.bigquery.client.Client`
        :param client: The client to use.

        :rtype transport:
            :class:`~google.auth.transport.requests.AuthorizedSession`
        :returns: The transport (with credentials) that will
                  make authenticated requests.
        """
        return client._http

    def _initiate_resumable_upload(self, client, stream,
                                   metadata, num_retries):
        """Initiate a resumable upload.

        :type client: :class:`~google.cloud.bigquery.client.Client`
        :param client: The client to use.

        :type stream: IO[bytes]
        :param stream: A bytes IO object open for reading.

        :type metadata: dict
        :param metadata: The metadata associated with the upload.

        :type num_retries: int
        :param num_retries: Number of upload retries. (Deprecated: This
                            argument will be removed in a future release.)

        :rtype: tuple
        :returns:
            Pair of

            * The :class:`~google.resumable_media.requests.ResumableUpload`
              that was created
            * The ``transport`` used to initiate the upload.
        """
        chunk_size = _DEFAULT_CHUNKSIZE
        transport = self._get_transport(client)
        headers = _get_upload_headers(client._connection.USER_AGENT)
        upload_url = _RESUMABLE_URL_TEMPLATE.format(project=self.project)
        upload = ResumableUpload(upload_url, chunk_size, headers=headers)

        if num_retries is not None:
            upload._retry_strategy = resumable_media.RetryStrategy(
                max_retries=num_retries)

        upload.initiate(
            transport, stream, metadata, _GENERIC_CONTENT_TYPE,
            stream_final=False)

        return upload, transport

    def _do_resumable_upload(self, client, stream, metadata, num_retries):
        """Perform a resumable upload.

        :type client: :class:`~google.cloud.bigquery.client.Client`
        :param client: The client to use.

        :type stream: IO[bytes]
        :param stream: A bytes IO object open for reading.

        :type metadata: dict
        :param metadata: The metadata associated with the upload.

        :type num_retries: int
        :param num_retries: Number of upload retries. (Deprecated: This
                            argument will be removed in a future release.)

        :rtype: :class:`~requests.Response`
        :returns: The "200 OK" response object returned after the final chunk
                  is uploaded.
        """
        upload, transport = self._initiate_resumable_upload(
            client, stream, metadata, num_retries)

        while not upload.finished:
            response = upload.transmit_next_chunk(transport)

        return response

    def _do_multipart_upload(self, client, stream, metadata,
                             size, num_retries):
        """Perform a multipart upload.

        :type client: :class:`~google.cloud.bigquery.client.Client`
        :param client: The client to use.

        :type stream: IO[bytes]
        :param stream: A bytes IO object open for reading.

        :type metadata: dict
        :param metadata: The metadata associated with the upload.

        :type size: int
        :param size: The number of bytes to be uploaded (which will be read
                     from ``stream``). If not provided, the upload will be
                     concluded once ``stream`` is exhausted (or :data:`None`).

        :type num_retries: int
        :param num_retries: Number of upload retries. (Deprecated: This
                            argument will be removed in a future release.)

        :rtype: :class:`~requests.Response`
        :returns: The "200 OK" response object returned after the multipart
                  upload request.
        :raises: :exc:`ValueError` if the ``stream`` has fewer than ``size``
                 bytes remaining.
        """
        data = stream.read(size)
        if len(data) < size:
            msg = _READ_LESS_THAN_SIZE.format(size, len(data))
            raise ValueError(msg)

        transport = self._get_transport(client)
        headers = _get_upload_headers(client._connection.USER_AGENT)

        upload_url = _MULTIPART_URL_TEMPLATE.format(project=self.project)
        upload = MultipartUpload(upload_url, headers=headers)

        if num_retries is not None:
            upload._retry_strategy = resumable_media.RetryStrategy(
                max_retries=num_retries)

        response = upload.transmit(
            transport, data, metadata, _GENERIC_CONTENT_TYPE)

        return response

    def _do_upload(self, client, stream, metadata, size, num_retries):
        """Determine an upload strategy and then perform the upload.

        If ``size`` is :data:`None`, then a resumable upload will be used,
        otherwise the content and the metadata will be uploaded
        in a single multipart upload request.

        :type client: :class:`~google.cloud.bigquery.client.Client`
        :param client: The client to use.

        :type stream: IO[bytes]
        :param stream: A bytes IO object open for reading.

        :type metadata: dict
        :param metadata: The metadata associated with the upload.

        :type size: int
        :param size: The number of bytes to be uploaded (which will be read
                     from ``stream``). If not provided, the upload will be
                     concluded once ``stream`` is exhausted (or :data:`None`).

        :type num_retries: int
        :param num_retries: Number of upload retries. (Deprecated: This
                            argument will be removed in a future release.)

        :rtype: dict
        :returns: The parsed JSON from the "200 OK" response. This will be the
                  **only** response in the multipart case and it will be the
                  **final** response in the resumable case.
        """
        if size is None:
            response = self._do_resumable_upload(
                client, stream, metadata, num_retries)
        else:
            response = self._do_multipart_upload(
                client, stream, metadata, size, num_retries)

        return response.json()

    # pylint: disable=too-many-arguments,too-many-locals
    def upload_from_file(self,
                         file_obj,
                         source_format,
                         rewind=False,
                         size=None,
                         num_retries=_DEFAULT_NUM_RETRIES,
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
                         client=None,
                         job_name=None,
                         null_marker=None):
        """Upload the contents of this table from a file-like object.

        :type file_obj: file
        :param file_obj: A file handle opened in binary mode for reading.

        :type source_format: str
        :param source_format: Any supported format. The full list of supported
            formats is documented under the
            ``configuration.extract.destinationFormat`` property on this page:
            https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs

        :type rewind: bool
        :param rewind: If True, seek to the beginning of the file handle before
                       writing the file.

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

        :type client: :class:`~google.cloud.bigquery.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the current table.

        :type job_name: str
        :param job_name: Optional. The id of the job. Generated if not
                         explicitly passed in.

        :type null_marker: str
        :param null_marker: Optional. A custom null marker (example: "\\N")

        :rtype: :class:`~google.cloud.bigquery.jobs.LoadTableFromStorageJob`

        :returns: the job instance used to load the data (e.g., for
                  querying status). Note that the job is already started:
                  do not call ``job.begin()``.
        :raises: :class:`ValueError` if ``size`` is not passed in and can not
                 be determined, or if the ``file_obj`` can be detected to be
                 a file opened in text mode.
        """
        client = self._require_client(client)
        _maybe_rewind(file_obj, rewind=rewind)
        _check_mode(file_obj)
        metadata = _get_upload_metadata(
            source_format, self._schema, self._dataset, self.name)
        _configure_job_metadata(metadata, allow_jagged_rows,
                                allow_quoted_newlines, create_disposition,
                                encoding, field_delimiter,
                                ignore_unknown_values, max_bad_records,
                                quote_character, skip_leading_rows,
                                write_disposition, job_name, null_marker)

        try:
            created_json = self._do_upload(
                client, file_obj, metadata, size, num_retries)
            return client.job_from_resource(created_json)
        except resumable_media.InvalidResponse as exc:
            raise exceptions.from_http_response(exc.response)
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
                            write_disposition,
                            job_name,
                            null_marker):
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

    if job_name is not None:
        load_config['jobReference'] = {'jobId': job_name}

    if null_marker is not None:
        load_config['nullMarker'] = null_marker


def _parse_schema_resource(info):
    """Parse a resource fragment into a schema field.

    :type info: mapping
    :param info: should contain a "fields" key to be parsed

    :rtype: list of :class:`SchemaField`, or ``NoneType``
    :returns: a list of parsed fields, or ``None`` if no "fields" key is
                present in ``info``.
    """
    if 'fields' not in info:
        return ()

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
        if field.fields:
            info['fields'] = _build_schema_resource(field.fields)
        infos.append(info)
    return infos
# pylint: enable=unused-argument


def _maybe_rewind(stream, rewind=False):
    """Rewind the stream if desired.

    :type stream: IO[bytes]
    :param stream: A bytes IO object open for reading.

    :type rewind: bool
    :param rewind: Indicates if we should seek to the beginning of the stream.
    """
    if rewind:
        stream.seek(0, os.SEEK_SET)


def _check_mode(stream):
    """Check that a stream was opened in read-binary mode.

    :type stream: IO[bytes]
    :param stream: A bytes IO object open for reading.

    :raises: :exc:`ValueError` if the ``stream.mode`` is a valid attribute
             and is not among ``rb``, ``r+b`` or ``rb+``.
    """
    mode = getattr(stream, 'mode', None)

    if mode is not None and mode not in ('rb', 'r+b', 'rb+'):
        raise ValueError(
            "Cannot upload files opened in text mode:  use "
            "open(filename, mode='rb') or open(filename, mode='r+b')")


def _get_upload_headers(user_agent):
    """Get the headers for an upload request.

    :type user_agent: str
    :param user_agent: The user-agent for requests.

    :rtype: dict
    :returns: The headers to be used for the request.
    """
    return {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': user_agent,
        'content-type': 'application/json',
    }


def _get_upload_metadata(source_format, schema, dataset, name):
    """Get base metadata for creating a table.

    :type source_format: str
    :param source_format: one of 'CSV' or 'NEWLINE_DELIMITED_JSON'.
                          job configuration option.

    :type schema: list
    :param schema: List of :class:`SchemaField` associated with a table.

    :type dataset: :class:`~google.cloud.bigquery.dataset.Dataset`
    :param dataset: A dataset which contains a table.

    :type name: str
    :param name: The name of the table.

    :rtype: dict
    :returns: The metadata dictionary.
    """
    load_config = {
        'sourceFormat': source_format,
        'destinationTable': {
            'projectId': dataset.project,
            'datasetId': dataset.name,
            'tableId': name,
        },
    }
    if schema:
        load_config['schema'] = {
            'fields': _build_schema_resource(schema),
        }

    return {
        'configuration': {
            'load': load_config,
        },
    }
