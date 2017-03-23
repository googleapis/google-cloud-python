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
import six

from google.cloud._helpers import _datetime_from_microseconds
from google.cloud.exceptions import NotFound
from google.cloud.bigquery.table import Table
from google.cloud.iterator import HTTPIterator


class AccessGrant(object):
    """Represent grant of an access role to an entity.

    Every entry in the access list will have exactly one of
    ``userByEmail``, ``groupByEmail``, ``domain``, ``specialGroup`` or
    ``view`` set. And if anything but ``view`` is set, it'll also have a
    ``role`` specified. ``role`` is omitted for a ``view``, since
    ``view`` s are always read-only.

    See https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets.

    :type role: str
    :param role: Role granted to the entity. One of

                 * ``'OWNER'``
                 * ``'WRITER'``
                 * ``'READER'``

                 May also be ``None`` if the ``entity_type`` is ``view``.

    :type entity_type: str
    :param entity_type: Type of entity being granted the role. One of
                        :attr:`ENTITY_TYPES`.

    :type entity_id: str
    :param entity_id: ID of entity being granted the role.

    :raises: :class:`ValueError` if the ``entity_type`` is not among
             :attr:`ENTITY_TYPES`, or if a ``view`` has ``role`` set or
             a non ``view`` **does not** have a ``role`` set.
    """

    ENTITY_TYPES = frozenset(['userByEmail', 'groupByEmail', 'domain',
                              'specialGroup', 'view'])
    """Allowed entity types."""

    def __init__(self, role, entity_type, entity_id):
        if entity_type not in self.ENTITY_TYPES:
            message = 'Entity type %r not among: %s' % (
                entity_type, ', '.join(self.ENTITY_TYPES))
            raise ValueError(message)
        if entity_type == 'view':
            if role is not None:
                raise ValueError('Role must be None for a view. Received '
                                 'role: %r' % (role,))
        else:
            if role is None:
                raise ValueError('Role must be set for entity '
                                 'type %r' % (entity_type,))

        self.role = role
        self.entity_type = entity_type
        self.entity_id = entity_id

    def __eq__(self, other):
        return (
            self.role == other.role and
            self.entity_type == other.entity_type and
            self.entity_id == other.entity_id)

    def __repr__(self):
        return '<AccessGrant: role=%s, %s=%s>' % (
            self.role, self.entity_type, self.entity_id)


class Dataset(object):
    """Datasets are containers for tables.

    See:
    https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets

    :type name: str
    :param name: the name of the dataset

    :type client: :class:`google.cloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).

    :type access_grants: list of :class:`AccessGrant`
    :param access_grants: roles granted to entities for this dataset

    :type project: str
    :param project: (Optional) project ID for the dataset (defaults to
                    the project of the client).
    """

    _access_grants = None

    def __init__(self, name, client, access_grants=(), project=None):
        self.name = name
        self._client = client
        self._properties = {}
        # Let the @property do validation.
        self.access_grants = access_grants
        self._project = project or client.project

    @property
    def project(self):
        """Project bound to the dataset.

        :rtype: str
        :returns: the project (derived from the client).
        """
        return self._project

    @property
    def path(self):
        """URL path for the dataset's APIs.

        :rtype: str
        :returns: the path based on project and dataste name.
        """
        return '/projects/%s/datasets/%s' % (self.project, self.name)

    @property
    def access_grants(self):
        """Dataset's access grants.

        :rtype: list of :class:`AccessGrant`
        :returns: roles granted to entities for this dataset
        """
        return list(self._access_grants)

    @access_grants.setter
    def access_grants(self, value):
        """Update dataset's access grants

        :type value: list of :class:`AccessGrant`
        :param value: roles granted to entities for this dataset

        :raises: TypeError if 'value' is not a sequence, or ValueError if
                 any item in the sequence is not an AccessGrant
        """
        if not all(isinstance(field, AccessGrant) for field in value):
            raise ValueError('Values must be AccessGrant instances')
        self._access_grants = tuple(value)

    @property
    def created(self):
        """Datetime at which the dataset was created.

        :rtype: ``datetime.datetime``, or ``NoneType``
        :returns: the creation time (None until set from the server).
        """
        creation_time = self._properties.get('creationTime')
        if creation_time is not None:
            # creation_time will be in milliseconds.
            return _datetime_from_microseconds(1000.0 * creation_time)

    @property
    def dataset_id(self):
        """ID for the dataset resource.

        :rtype: str, or ``NoneType``
        :returns: the ID (None until set from the server).
        """
        return self._properties.get('id')

    @property
    def etag(self):
        """ETag for the dataset resource.

        :rtype: str, or ``NoneType``
        :returns: the ETag (None until set from the server).
        """
        return self._properties.get('etag')

    @property
    def modified(self):
        """Datetime at which the dataset was last modified.

        :rtype: ``datetime.datetime``, or ``NoneType``
        :returns: the modification time (None until set from the server).
        """
        modified_time = self._properties.get('lastModifiedTime')
        if modified_time is not None:
            # modified_time will be in milliseconds.
            return _datetime_from_microseconds(1000.0 * modified_time)

    @property
    def self_link(self):
        """URL for the dataset resource.

        :rtype: str, or ``NoneType``
        :returns: the URL (None until set from the server).
        """
        return self._properties.get('selfLink')

    @property
    def default_table_expiration_ms(self):
        """Default expiration time for tables in the dataset.

        :rtype: int, or ``NoneType``
        :returns: The time in milliseconds, or None (the default).
        """
        return self._properties.get('defaultTableExpirationMs')

    @default_table_expiration_ms.setter
    def default_table_expiration_ms(self, value):
        """Update default expiration time for tables in the dataset.

        :type value: int
        :param value: (Optional) new default time, in milliseconds

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.integer_types) and value is not None:
            raise ValueError("Pass an integer, or None")
        self._properties['defaultTableExpirationMs'] = value

    @property
    def description(self):
        """Description of the dataset.

        :rtype: str, or ``NoneType``
        :returns: The description as set by the user, or None (the default).
        """
        return self._properties.get('description')

    @description.setter
    def description(self, value):
        """Update description of the dataset.

        :type value: str
        :param value: (Optional) new description

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['description'] = value

    @property
    def friendly_name(self):
        """Title of the dataset.

        :rtype: str, or ``NoneType``
        :returns: The name as set by the user, or None (the default).
        """
        return self._properties.get('friendlyName')

    @friendly_name.setter
    def friendly_name(self, value):
        """Update title of the dataset.

        :type value: str
        :param value: (Optional) new title

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['friendlyName'] = value

    @property
    def location(self):
        """Location in which the dataset is hosted.

        :rtype: str, or ``NoneType``
        :returns: The location as set by the user, or None (the default).
        """
        return self._properties.get('location')

    @location.setter
    def location(self, value):
        """Update location in which the dataset is hosted.

        :type value: str
        :param value: (Optional) new location

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['location'] = value

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a dataset given its API representation

        :type resource: dict
        :param resource: dataset resource representation returned from the API

        :type client: :class:`google.cloud.bigquery.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the dataset.

        :rtype: :class:`google.cloud.bigquery.dataset.Dataset`
        :returns: Dataset parsed from ``resource``.
        """
        if ('datasetReference' not in resource or
                'datasetId' not in resource['datasetReference']):
            raise KeyError('Resource lacks required identity information:'
                           '["datasetReference"]["datasetId"]')
        name = resource['datasetReference']['datasetId']
        dataset = cls(name, client=client)
        dataset._set_properties(resource)
        return dataset

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

    @staticmethod
    def _parse_access_grants(access):
        """Parse a resource fragment into a set of access grants.

        ``role`` augments the entity type and present **unless** the entity
        type is ``view``.

        :type access: list of mappings
        :param access: each mapping represents a single access grant.

        :rtype: list of :class:`AccessGrant`
        :returns: a list of parsed grants.
        :raises: :class:`ValueError` if a grant in ``access`` has more keys
                 than ``role`` and one additional key.
        """
        result = []
        for grant in access:
            grant = grant.copy()
            role = grant.pop('role', None)
            entity_type, entity_id = grant.popitem()
            if len(grant) != 0:
                raise ValueError('Grant has unexpected keys remaining.', grant)
            result.append(
                AccessGrant(role, entity_type, entity_id))
        return result

    def _set_properties(self, api_response):
        """Update properties from resource in body of ``api_response``

        :type api_response: httplib2.Response
        :param api_response: response returned from an API call.
        """
        self._properties.clear()
        cleaned = api_response.copy()
        access = cleaned.pop('access', ())
        self.access_grants = self._parse_access_grants(access)
        if 'creationTime' in cleaned:
            cleaned['creationTime'] = float(cleaned['creationTime'])
        if 'lastModifiedTime' in cleaned:
            cleaned['lastModifiedTime'] = float(cleaned['lastModifiedTime'])
        if 'defaultTableExpirationMs' in cleaned:
            cleaned['defaultTableExpirationMs'] = int(
                cleaned['defaultTableExpirationMs'])
        self._properties.update(cleaned)

    def _build_access_resource(self):
        """Generate a resource fragment for dataset's access grants."""
        result = []
        for grant in self.access_grants:
            info = {grant.entity_type: grant.entity_id}
            if grant.role is not None:
                info['role'] = grant.role
            result.append(info)
        return result

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

        if len(self.access_grants) > 0:
            resource['access'] = self._build_access_resource()

        return resource

    def create(self, client=None):
        """API call:  create the dataset via a PUT request.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        path = '/projects/%s/datasets' % (self.project,)
        api_response = client._connection.api_request(
            method='POST', path=path, data=self._build_resource())
        self._set_properties(api_response)

    def exists(self, client=None):
        """API call:  test for the existence of the dataset via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: bool
        :returns: Boolean indicating existence of the dataset.
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
        """API call:  refresh dataset properties via a GET request.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)

        api_response = client._connection.api_request(
            method='GET', path=self.path)
        self._set_properties(api_response)

    def patch(self, client=None, **kw):
        """API call:  update individual dataset properties via a PATCH request.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
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

        api_response = client._connection.api_request(
            method='PATCH', path=self.path, data=partial)
        self._set_properties(api_response)

    def update(self, client=None):
        """API call:  update dataset properties via a PUT request.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/update

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
        """API call:  delete the dataset via a DELETE request.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        client._connection.api_request(method='DELETE', path=self.path)

    def list_tables(self, max_results=None, page_token=None):
        """List tables for the project associated with this client.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/list

        :type max_results: int
        :param max_results: (Optional) Maximum number of tables to return.
                            If not passed, defaults to a value set by the API.

        :type page_token: str
        :param page_token: (Optional) Opaque marker for the next "page" of
                           datasets. If not passed, the API will return the
                           first page of datasets.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns: Iterator of :class:`~google.cloud.bigquery.table.Table`
                  contained within the current dataset.
        """
        path = '/projects/%s/datasets/%s/tables' % (self.project, self.name)
        result = HTTPIterator(client=self._client, path=path,
                              item_to_value=_item_to_table, items_key='tables',
                              page_token=page_token, max_results=max_results)
        result.dataset = self
        return result

    def table(self, name, schema=()):
        """Construct a table bound to this dataset.

        :type name: str
        :param name: Name of the table.

        :type schema: list of :class:`google.cloud.bigquery.table.SchemaField`
        :param schema: The table's schema

        :rtype: :class:`google.cloud.bigquery.table.Table`
        :returns: a new ``Table`` instance
        """
        return Table(name, dataset=self, schema=schema)


def _item_to_table(iterator, resource):
    """Convert a JSON table to the native object.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: An item to be converted to a table.

    :rtype: :class:`~google.cloud.bigquery.table.Table`
    :returns: The next table in the page.
    """
    return Table.from_api_repr(resource, iterator.dataset)
