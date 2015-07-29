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

from gcloud.exceptions import NotFound
from gcloud.bigquery._helpers import _datetime_from_prop
from gcloud.bigquery._helpers import _prop_from_datetime


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
        return _datetime_from_prop(self._properties.get('creationTime'))

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
        return _datetime_from_prop(self._properties.get('lastModifiedTime'))

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
        return _datetime_from_prop(self._properties.get('expirationTime'))

    @expires.setter
    def expires(self, value):
        """Update atetime at which the table will be removed.

        :type value: ``datetime.datetime``, or ``NoneType``
        :param value: the new expiration time, or None
        """
        if not isinstance(value, datetime.datetime) and value is not None:
            raise ValueError("Pass a datetime, or None")
        self._properties['expirationTime'] = _prop_from_datetime(value)

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
        :param value: new location

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types):
            raise ValueError("Pass a string")
        self._properties['view'] = {'query': value}

    @view_query.deleter
    def view_query(self):
        """Delete SQL query defining the table as a view."""
        self._properties.pop('view', None)

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
        cleaned['creationTime'] = float(cleaned['creationTime'])
        cleaned['lastModifiedTime'] = float(cleaned['lastModifiedTime'])
        if 'expirationTime' in cleaned:
            cleaned['expirationTime'] = float(cleaned['expirationTime'])
        self._properties.update(cleaned)

    def _build_schema_resource(self, fields=None):
        """Generate a resource fragment for table's schema."""
        if fields is None:
            fields = self._schema
        infos = []
        for field in fields:
            info = {'name': field.name,
                    'type': field.field_type,
                    'mode': field.mode}
            if field.description is not None:
                info['description'] = field.description
            if field.fields is not None:
                info['fields'] = self._build_schema_resource(field.fields)
            infos.append(info)
        return infos

    def _build_resource(self):
        """Generate a resource for ``create`` or ``update``."""
        resource = {
            'tableReference': {
                'projectId': self._dataset.project,
                'datasetId': self._dataset.name,
                'tableId': self.name},
            'schema': {'fields': self._build_schema_resource()},
        }
        if self.description is not None:
            resource['description'] = self.description

        if self.expires is not None:
            value = _prop_from_datetime(self.expires)
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
        https://cloud.google.com/bigquery/reference/rest/v2/tables/insert

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

    def patch(self, client=None, **kw):
        """API call:  update individual table properties via a PATCH request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/tables/patch

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :type kw: ``dict``
        :param kw: properties to be patched.

        :raises: ValueError for invalid value types.
        """
        client = self._require_client(client)

        partial = {}

        if 'expires' in kw:
            value = kw['expires']
            if not isinstance(value, datetime.datetime) and value is not None:
                raise ValueError("Pass a datetime, or None")
            partial['expirationTime'] = _prop_from_datetime(value)

        if 'description' in kw:
            partial['description'] = kw['description']

        if 'friendly_name' in kw:
            partial['friendlyName'] = kw['friendly_name']

        if 'location' in kw:
            partial['location'] = kw['location']

        if 'view_query' in kw:
            partial['view'] = {'query': kw['view_query']}

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
        https://cloud.google.com/bigquery/reference/rest/v2/tables/delete

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        client.connection.api_request(method='DELETE', path=self.path)
