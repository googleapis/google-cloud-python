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

"""Define API Document."""

import datetime

import six

from gcloud._helpers import _datetime_to_rfc3339
from gcloud._helpers import _rfc3339_to_datetime
from gcloud.exceptions import NotFound


class StringValue(object):
    """StringValues hold individual text values for a given field

    See:
    https://cloud.google.com/search/reference/rest/google/cloudsearch/v1/FieldValue

    :type string_value: string
    :param string_value: the actual value.

    :type string_format: string
    :param string_format: how the value should be indexed:  one of
                          'ATOM', 'TEXT', 'HTML' (leave as ``None`` to
                          use the server-supplied default).

    :type language: string
    :param language: Human language of the text.  Should be an ISO 639-1
                     language code.
    """

    value_type = 'string'

    def __init__(self, string_value, string_format=None, language=None):
        self.string_value = string_value
        self.string_format = string_format
        self.language = language


class NumberValue(object):
    """NumberValues hold individual numeric values for a given field

    See:
    https://cloud.google.com/search/reference/rest/google/cloudsearch/v1/FieldValue

    :type number_value: integer, float (long on Python2)
    :param number_value: the actual value.
    """

    value_type = 'number'

    def __init__(self, number_value):
        self.number_value = number_value


class TimestampValue(object):
    """TimestampValues hold individual datetime values for a given field
    See:
    https://cloud.google.com/search/reference/rest/google/cloudsearch/v1/FieldValue

    :type timestamp_value: class:``datetime.datetime``
    :param timestamp_value: the actual value.
    """

    value_type = 'timestamp'

    def __init__(self, timestamp_value):
        self.timestamp_value = timestamp_value


class GeoValue(object):
    """GeoValues hold individual latitude/longitude values for a given field
    See:
    https://cloud.google.com/search/reference/rest/google/cloudsearch/v1/FieldValue

    :type geo_value: tuple, (float, float)
    :param geo_value: latitude, longitude
    """

    value_type = 'geo'

    def __init__(self, geo_value):
        self.geo_value = geo_value


class Field(object):
    """Fields hold values for a given document

    See:
    https://cloud.google.com/search/reference/rest/google/cloudsearch/v1/FieldValueList

    :type name: string
    :param name: field name
    """

    def __init__(self, name):
        self.name = name
        self.values = []

    def add_value(self, value, **kw):
        """Add a value to the field.

        Selects type of value instance based on type of ``value``.

        :type value: string, integer, float, datetime, or tuple (float, float)
        :param value: the field value to add.

        :param kw: extra keyword arguments to be passed to the value instance
                   constructor.  Currently, only :class:`StringValue`
                   expects / honors additional parameters.

        :raises: ValueError if unable to match the type of ``value``.
        """
        if isinstance(value, six.string_types):
            self.values.append(StringValue(value, **kw))
        elif isinstance(value, (six.integer_types, float)):
            self.values.append(NumberValue(value, **kw))
        elif isinstance(value, datetime.datetime):
            self.values.append(TimestampValue(value, **kw))
        elif isinstance(value, tuple):
            self.values.append(GeoValue(value, **kw))
        else:
            raise ValueError("Couldn't determine value type: %s" % (value,))


class Document(object):
    """Documents hold values for search within indexes.

    See:
    https://cloud.google.com/search/reference/rest/v1/projects/indexes/documents

    :type name: string
    :param name: the name of the document

    :type index: :class:`gcloud.search.index.Index`
    :param index: the index to which the document belongs.

    :type rank: positive integer
    :param rank: override the server-generated rank for ordering the document
                 within in queries.  If not passed, the server generates a
                 timestamp-based value.  See the ``rank`` entry on the
                 page above for details.
    """
    def __init__(self, name, index, rank=None):
        self.name = name
        self.index = index
        self.rank = rank
        self.fields = {}

    @classmethod
    def from_api_repr(cls, resource, index):
        """Factory:  construct a document given its API representation

        :type resource: dict
        :param resource: document resource representation returned from the API

        :type index: :class:`gcloud.search.index.Index`
        :param index: Index holding the document.

        :rtype: :class:`gcloud.search.document.Document`
        :returns: Document parsed from ``resource``.
        """
        name = resource.get('docId')
        if name is None:
            raise KeyError(
                'Resource lacks required identity information: ["docId"]')
        rank = resource.get('rank')
        document = cls(name, index, rank)
        document._parse_fields_resource(resource)
        return document

    @staticmethod
    def _parse_value_resource(resource):
        """Helper for _parse_fields_resource"""
        if 'stringValue' in resource:
            string_format = resource.get('stringFormat')
            language = resource.get('lang')
            value = resource['stringValue']
            return StringValue(value, string_format, language)
        if 'numberValue' in resource:
            value = resource['numberValue']
            if isinstance(value, six.string_types):
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            return NumberValue(value)
        if 'timestampValue' in resource:
            stamp = resource['timestampValue']
            value = _rfc3339_to_datetime(stamp)
            return TimestampValue(value)
        if 'geoValue' in resource:
            lat_long = resource['geoValue']
            latitude, longitude = [float(coord.strip())
                                   for coord in lat_long.split(',')]
            return GeoValue((latitude, longitude))
        raise ValueError("Unknown value type")

    def _parse_fields_resource(self, resource):
        """Helper for from_api_repr, create, reload"""
        self.fields.clear()
        for field_name, val_obj in resource.get('fields', {}).items():
            field = self.field(field_name)
            for value in val_obj['values']:
                field.values.append(self._parse_value_resource(value))

    @property
    def path(self):
        """URL path for the document's APIs"""
        return '%s/documents/%s' % (self.index.path, self.name)

    def field(self, name):
        """Construct a Field instance.

        :type name: string
        :param name: field's name
        """
        field = self.fields[name] = Field(name)
        return field

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`gcloud.search.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the index of the
                       current document.

        :rtype: :class:`gcloud.search.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self.index._client
        return client

    @staticmethod
    def _build_value_resource(value):
        """Helper for _build_fields_resource"""
        result = {}
        if value.value_type == 'string':
            result['stringValue'] = value.string_value
            if value.string_format is not None:
                result['stringFormat'] = value.string_format
            if value.language is not None:
                result['lang'] = value.language
        elif value.value_type == 'number':
            result['numberValue'] = value.number_value
        elif value.value_type == 'timestamp':
            stamp = _datetime_to_rfc3339(value.timestamp_value)
            result['timestampValue'] = stamp
        elif value.value_type == 'geo':
            result['geoValue'] = '%s, %s' % value.geo_value
        else:
            raise ValueError('Unknown value_type: %s' % value.value_type)
        return result

    def _build_fields_resource(self):
        """Helper for create"""
        fields = {}
        for field_name, field in self.fields.items():
            if field.values:
                values = []
                fields[field_name] = {'values': values}
                for value in field.values:
                    values.append(self._build_value_resource(value))
        return fields

    def _set_properties(self, api_response):
        """Helper for create, reload"""
        self.rank = api_response.get('rank')
        self._parse_fields_resource(api_response)

    def create(self, client=None):
        """API call:  create the document via a PUT request

        See:
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/documents/create

        :type client: :class:`gcloud.search.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current document's index.
        """
        data = {'docId': self.name}

        if self.rank is not None:
            data['rank'] = self.rank

        fields = self._build_fields_resource()
        if fields:
            data['fields'] = fields

        client = self._require_client(client)
        api_response = client.connection.api_request(
            method='PUT', path=self.path, data=data)

        self._set_properties(api_response)

    def exists(self, client=None):
        """API call:  test existence of the document via a GET request

        See
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/documents/get

        :type client: :class:`gcloud.search.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current document's index.
        """
        client = self._require_client(client)
        try:
            client.connection.api_request(method='GET', path=self.path)
        except NotFound:
            return False
        else:
            return True

    def reload(self, client=None):
        """API call:  sync local document configuration via a GET request

        See
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/documents/get

        :type client: :class:`gcloud.search.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current document's index.
        """
        client = self._require_client(client)
        api_response = client.connection.api_request(
            method='GET', path=self.path)
        self._set_properties(api_response)

    def delete(self, client=None):
        """API call:  delete the document via a DELETE request.

        See:
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/documents/delete

        :type client: :class:`gcloud.search.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current document's index.
        """
        client = self._require_client(client)
        client.connection.api_request(method='DELETE', path=self.path)
