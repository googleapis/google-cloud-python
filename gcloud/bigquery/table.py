# Copyright 2015 Google Inc. All rights reserved.
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

import six

from gcloud._helpers import _datetime_from_microseconds
from gcloud._helpers import _millis_from_datetime
from gcloud.exceptions import NotFound
from gcloud.bigquery._helpers import _rows_from_json


_MARKER = object()


class SchemaField(object):
    """Describe a single field within a table schema.

    :type name: string
    :param name: the name of the field

    :type field_type: string
    :param field_type: the type of the field (one of 'STRING', 'INTEGER',
                       'FLOAT', 'BOOLEAN', 'TIMESTAMP' or 'RECORD')

    :type mode: string
    :param mode: the type of the field (one of 'NULLABLE', 'REQUIRED',
                 or 'REPEATED')

    :type description: string
    :param description: optional description for the field

    :type fields: list of :class:`SchemaField`, or None
    :param fields: subfields (requires ``field_type`` of 'RECORD').
    """
    def __init__(self, name, field_type, mode='NULLABLE', description=None,
                 fields=None):
        self.name = name
        self.field_type = field_type
        self.mode = mode
        self.description = description
        self.fields = fields


class Table(object):
    """Tables represent a set of rows whose values correspond to a schema.

    See:
    https://cloud.google.com/bigquery/docs/reference/v2/tables

    :type name: string
    :param name: the name of the table

    :type dataset: :class:`gcloud.bigquery.dataset.Dataset`
    :param dataset: The dataset which contains the table.

    :type schema: list of :class:`SchemaField`
    :param schema: The table's schema
    """

    def __init__(self, name, dataset, schema=()):
        self.name = name
        self._dataset = dataset
        self._properties = {}
        self.schema = schema

    @property
    def project(self):
        """Project bound to the table.

        :rtype: string
        :returns: the project (derived from the dataset).
        """
        return self._dataset.project

    @property
    def dataset_name(self):
        """Name of dataset containing the table.

        :rtype: string
        :returns: the ID (derived from the dataset).
        """
        return self._dataset.name

    @property
    def path(self):
        """URL path for the table's APIs.

        :rtype: string
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

        :rtype: string, or ``NoneType``
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

        :rtype: integer, or ``NoneType``
        :returns: the byte count (None until set from the server).
        """
        return self._properties.get('numBytes')

    @property
    def num_rows(self):
        """The number of rows in the table.

        :rtype: integer, or ``NoneType``
        :returns: the row count (None until set from the server).
        """
        return self._properties.get('numRows')

    @property
    def self_link(self):
        """URL for the table resource.

        :rtype: string, or ``NoneType``
        :returns: the URL (None until set from the server).
        """
        return self._properties.get('selfLink')

    @property
    def table_id(self):
        """ID for the table resource.

        :rtype: string, or ``NoneType``
        :returns: the ID (None until set from the server).
        """
        return self._properties.get('id')

    @property
    def table_type(self):
        """The type of the table.

        Possible values are "TABLE" or "VIEW".

        :rtype: string, or ``NoneType``
        :returns: the URL (None until set from the server).
        """
        return self._properties.get('type')

    @property
    def description(self):
        """Description of the table.

        :rtype: string, or ``NoneType``
        :returns: The description as set by the user, or None (the default).
        """
        return self._properties.get('description')

    @description.setter
    def description(self, value):
        """Update description of the table.

        :type value: string, or ``NoneType``
        :param value: new description

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
        """Update atetime at which the table will be removed.

        :type value: ``datetime.datetime``, or ``NoneType``
        :param value: the new expiration time, or None
        """
        if not isinstance(value, datetime.datetime) and value is not None:
            raise ValueError("Pass a datetime, or None")
        self._properties['expirationTime'] = _millis_from_datetime(value)

    @property
    def friendly_name(self):
        """Title of the table.

        :rtype: string, or ``NoneType``
        :returns: The name as set by the user, or None (the default).
        """
        return self._properties.get('friendlyName')

    @friendly_name.setter
    def friendly_name(self, value):
        """Update title of the table.

        :type value: string, or ``NoneType``
        :param value: new title

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['friendlyName'] = value

    @property
    def location(self):
        """Location in which the table is hosted.

        :rtype: string, or ``NoneType``
        :returns: The location as set by the user, or None (the default).
        """
        return self._properties.get('location')

    @location.setter
    def location(self, value):
        """Update location in which the table is hosted.

        :type value: string, or ``NoneType``
        :param value: new location

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['location'] = value

    @property
    def view_query(self):
        """SQL query defining the table as a view.

        :rtype: string, or ``NoneType``
        :returns: The query as set by the user, or None (the default).
        """
        view = self._properties.get('view')
        if view is not None:
            return view.get('query')

    @view_query.setter
    def view_query(self, value):
        """Update SQL query defining the table as a view.

        :type value: string
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

    @classmethod
    def from_api_repr(cls, resource, dataset):
        """Factory:  construct a table given its API representation

        :type resource: dict
        :param resource: table resource representation returned from the API

        :type dataset: :class:`gcloud.bigquery.dataset.Dataset`
        :param dataset: The dataset containing the table.

        :rtype: :class:`gcloud.bigquery.table.Table`
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

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: :class:`gcloud.bigquery.client.Client`
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
            'schema': {'fields': _build_schema_resource(self._schema)},
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

        if self.view_query is not None:
            view = resource['view'] = {}
            view['query'] = self.view_query

        return resource

    def create(self, client=None):
        """API call:  create the dataset via a PUT request

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/tables/insert

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        path = '/projects/%s/datasets/%s/tables' % (
            self._dataset.project, self._dataset.name)
        api_response = client.connection.api_request(
            method='POST', path=path, data=self._build_resource())
        self._set_properties(api_response)

    def exists(self, client=None):
        """API call:  test for the existence of the table via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/tables/get

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)

        try:
            client.connection.api_request(method='GET', path=self.path,
                                          query_params={'fields': 'id'})
        except NotFound:
            return False
        else:
            return True

    def reload(self, client=None):
        """API call:  refresh table properties via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/tables/get

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)

        api_response = client.connection.api_request(
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

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :type friendly_name: string or ``NoneType``
        :param friendly_name: point in time at which the table expires.

        :type description: string or ``NoneType``
        :param description: point in time at which the table expires.

        :type location: string or ``NoneType``
        :param location: point in time at which the table expires.

        :type expires: :class:`datetime.datetime` or ``NoneType``
        :param expires: point in time at which the table expires.

        :type view_query: string
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

        api_response = client.connection.api_request(
            method='PATCH', path=self.path, data=partial)
        self._set_properties(api_response)

    def update(self, client=None):
        """API call:  update table properties via a PUT request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/tables/update

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        api_response = client.connection.api_request(
            method='PUT', path=self.path, data=self._build_resource())
        self._set_properties(api_response)

    def delete(self, client=None):
        """API call:  delete the table via a DELETE request

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/tables/delete

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        client.connection.api_request(method='DELETE', path=self.path)

    def fetch_data(self, max_results=None, page_token=None, client=None):
        """API call:  fetch the table data via a GET request

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/tabledata/list

        .. note::

           This method assumes that its instance's ``schema`` attribute is
           up-to-date with the schema as defined on the back-end:  if the
           two schemas are not identical, the values returned may be
           incomplete.  To ensure that the local copy of the schema is
           up-to-date, call the table's ``reload`` method.

        :type max_results: integer or ``NoneType``
        :param max_results: maximum number of rows to return.

        :type page_token: string or ``NoneType``
        :param page_token: token representing a cursor into the table's rows.

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: tuple
        :returns: ``(row_data, total_rows, page_token)``, where ``row_data``
                  is a list of tuples, one per result row, containing only
                  the values;  ``total_rows`` is a count of the total number
                  of rows in the table;  and ``page_token`` is an opaque
                  string which can be used to fetch the next batch of rows
                  (``None`` if no further batches can be fetched).
        """
        client = self._require_client(client)
        params = {}

        if max_results is not None:
            params['maxResults'] = max_results

        if page_token is not None:
            params['pageToken'] = page_token

        response = client.connection.api_request(method='GET',
                                                 path='%s/data' % self.path,
                                                 query_params=params)
        total_rows = response.get('totalRows')
        page_token = response.get('pageToken')
        rows_data = _rows_from_json(response.get('rows', ()), self._schema)

        return rows_data, total_rows, page_token

    def insert_data(self,
                    rows,
                    row_ids=None,
                    skip_invalid_rows=None,
                    ignore_unknown_values=None,
                    client=None):
        """API call:  insert table data via a POST request

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/tabledata/insertAll

        :type rows: list of tuples
        :param rows: row data to be inserted

        :type row_ids: list of string
        :param row_ids: Unique ids, one per row being inserted.  If not
                        passed, no de-duplication occurs.

        :type skip_invalid_rows: boolean or ``NoneType``
        :param skip_invalid_rows: skip rows w/ invalid data?

        :type ignore_unknown_values: boolean or ``NoneType``
        :param ignore_unknown_values: ignore columns beyond schema?

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: list of mappings
        :returns: One mapping per row with insert errors:  the "index" key
                  identifies the row, and the "errors" key contains a list
                  of the mappings describing one or more problems with the
                  row.
        """
        client = self._require_client(client)
        rows_info = []
        data = {'rows': rows_info}

        for index, row in enumerate(rows):
            row_info = {}

            for field, value in zip(self._schema, row):
                if field.field_type == 'TIMESTAMP':
                    value = _millis_from_datetime(value)
                row_info[field.name] = value

            info = {'json': row_info}
            if row_ids is not None:
                info['insertId'] = row_ids[index]

            rows_info.append(info)

        if skip_invalid_rows is not None:
            data['skipInvalidRows'] = skip_invalid_rows

        if ignore_unknown_values is not None:
            data['ignoreUnknownValues'] = ignore_unknown_values

        response = client.connection.api_request(
            method='POST',
            path='%s/insertAll' % self.path,
            data=data)
        errors = []

        for error in response.get('insertErrors', ()):
            errors.append({'index': int(error['index']),
                           'errors': error['errors']})

        return errors


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
        mode = r_field['mode']
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
    :returns; a mapping describing the schema of the supplied fields.
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
