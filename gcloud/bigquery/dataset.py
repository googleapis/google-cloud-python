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

import pytz
import six

from gcloud.exceptions import NotFound


class Dataset(object):
    """Datasets are containers for tables.

    See:
    https://cloud.google.com/bigquery/docs/reference/v2/datasets

    :type name: string
    :param name: the name of the dataset

    :type client: :class:`gcloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).
    """

    def __init__(self, name, client):
        self.name = name
        self._client = client
        self._properties = {}

    @property
    def project(self):
        """Project bound to the dataset."""
        return self._client.project

    @property
    def path(self):
        """URL path for the dataset's APIs"""
        return '/projects/%s/datasets/%s' % (self.project, self.name)

    @property
    def created(self):
        """Datetime at which the dataset was created.

        :rtype: ``datetime.datetime``, or ``NoneType``
        """
        return _datetime_from_prop(self._properties.get('creationTime'))

    @property
    def dataset_id(self):
        """ID for the dataset resource.

        :rtype: string, or ``NoneType``
        """
        return self._properties.get('id')

    @property
    def etag(self):
        """ETag for the dataset resource.

        :rtype: string, or ``NoneType``
        """
        return self._properties.get('etag')

    @property
    def modified(self):
        """Datetime at which the dataset was last modified.

        :rtype: ``datetime.datetime``, or ``NoneType``
        """
        return _datetime_from_prop(self._properties.get('lastModifiedTime'))

    @property
    def self_link(self):
        """URL for the dataset resource.

        :rtype: string, or ``NoneType``
        """
        return self._properties.get('selfLink')

    @property
    def default_table_expiration_ms(self):
        """Default expiration time for tables in the dataset.

        :rtype: integer, or ``NoneType``
        """
        return self._properties.get('defaultTableExpirationMs')

    @default_table_expiration_ms.setter
    def default_table_expiration_ms(self, value):
        """Update default expiration time for tables in the dataset.

        :type value: integer, or ``NoneType``
        :param value: new default time, in milliseconds

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.integer_types) and value is not None:
            raise ValueError("Pass an integer, or None")
        self._properties['defaultTableExpirationMs'] = value

    @property
    def description(self):
        """Description of the dataset.

        :rtype: string, or ``NoneType``
        """
        return self._properties.get('description')

    @description.setter
    def description(self, value):
        """Update description of the dataset.

        :type value: string, or ``NoneType``
        :param value: new description

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['description'] = value

    @property
    def friendly_name(self):
        """Title of the dataset.

        :rtype: string, or ``NoneType``
        """
        return self._properties.get('friendlyName')

    @friendly_name.setter
    def friendly_name(self, value):
        """Update title of the dataset.

        :type value: string, or ``NoneType``
        :param value: new title

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['friendlyName'] = value

    @property
    def location(self):
        """Location in which the dataset is hosted.

        :rtype: string, or ``NoneType``
        """
        return self._properties.get('location')

    @location.setter
    def location(self, value):
        """Update location in which the dataset is hosted.

        :type value: string, or ``NoneType``
        :param value: new location

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['location'] = value

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: :class:`gcloud.bigquery.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
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
        self._properties.update(cleaned)

    def _build_resource(self):
        """Generate a resource for ``create`` or ``update``."""
        resource = {
            'datasetReference': {
                'projectId': self.project, 'datasetId': self.name},
        }
        if self.default_table_expiration_ms is not None:
            value = self.default_table_expiration_ms
            resource['defaultTableExpirationMs'] = value

        if self.description is not None:
            resource['description'] = self.description

        if self.friendly_name is not None:
            resource['friendlyName'] = self.friendly_name

        if self.location is not None:
            resource['location'] = self.location

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
        path = '/projects/%s/datasets' % self.project
        api_response = client.connection.api_request(
            method='POST', path=path, data=self._build_resource())
        self._set_properties(api_response)

    def exists(self, client=None):
        """API call:  test for the existence of the dataset via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/datasets/get

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
        """API call:  refresh dataset properties via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/datasets/get

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)

        api_response = client.connection.api_request(
            method='GET', path=self.path)
        self._set_properties(api_response)

    def patch(self, client=None, **kw):
        """API call:  update individual dataset properties via a PATCH request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/datasets/patch

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :type kw: ``dict``
        :param kw: properties to be patched.

        :raises: ValueError for invalid value types.
        """
        client = self._require_client(client)

        partial = {}

        if 'default_table_expiration_ms' in kw:
            value = kw['default_table_expiration_ms']
            if not isinstance(value, six.integer_types) and value is not None:
                raise ValueError("Pass an integer, or None")
            partial['defaultTableExpirationMs'] = value

        if 'description' in kw:
            partial['description'] = kw['description']

        if 'friendly_name' in kw:
            partial['friendlyName'] = kw['friendly_name']

        if 'location' in kw:
            partial['location'] = kw['location']

        api_response = client.connection.api_request(
            method='PATCH', path=self.path, data=partial)
        self._set_properties(api_response)

    def update(self, client=None):
        """API call:  update dataset properties via a PUT request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/datasets/update

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        api_response = client.connection.api_request(
            method='PUT', path=self.path, data=self._build_resource())
        self._set_properties(api_response)

    def delete(self, client=None):
        """API call:  delete the dataset via a DELETE request

        See:
        https://cloud.google.com/bigquery/reference/rest/v2/datasets/delete

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        client.connection.api_request(method='DELETE', path=self.path)


def _datetime_from_prop(value):
    """Convert non-none timestamp to datetime, assuming UTC.

    :rtype: ``datetime.datetime``, or ``NoneType``
    """
    if value is not None:
        # back-end returns timestamps as milliseconds since the epoch
        value = datetime.datetime.utcfromtimestamp(value / 1000.0)
        return value.replace(tzinfo=pytz.utc)
