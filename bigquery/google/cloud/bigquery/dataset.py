# Copyright 2015 Google LLC
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

from __future__ import absolute_import

import six
import copy

from google.cloud._helpers import _datetime_from_microseconds
from google.cloud.bigquery.table import TableReference


class AccessEntry(object):
    """Represents grant of an access role to an entity.

    An entry must have exactly one of the allowed :attr:`ENTITY_TYPES`. If
    anything but ``view`` is set, a ``role`` is also required. ``role`` is
    omitted for a ``view``, because ``view`` s are always read-only.

    See https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets.

    Attributes:
        role (str):
            Role granted to the entity. The following string values are
            supported: `'READER'`, `'WRITER'`, `'OWNER'`. It may also be
            ``None`` if the ``entity_type`` is ``view``.

        entity_type (str):
            Type of entity being granted the role. One of :attr:`ENTITY_TYPES`.

        entity_id (Union[str, dict]):
            If the ``entity_type`` is not 'view', the ``entity_id`` is the
            ``str`` ID of the entity being granted the role. If the
            ``entity_type`` is 'view', the ``entity_id`` is a ``dict``
            representing the view from a different dataset to grant access to
            in the following format::

                {
                    'projectId': string,
                    'datasetId': string,
                    'tableId': string
                }

    Raises:
        ValueError:
            If the ``entity_type`` is not among :attr:`ENTITY_TYPES`, or if a
            ``view`` has ``role`` set, or a non ``view`` **does not** have a
            ``role`` set.

    Examples:
        >>> entry = AccessEntry('OWNER', 'userByEmail', 'user@example.com')

        >>> view = {
        ...     'projectId': 'my-project',
        ...     'datasetId': 'my_dataset',
        ...     'tableId': 'my_table'
        ... }
        >>> entry = AccessEntry(None, 'view', view)
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
        if not isinstance(other, AccessEntry):
            return NotImplemented
        return (
            self.role == other.role and
            self.entity_type == other.entity_type and
            self.entity_id == other.entity_id)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '<AccessEntry: role=%s, %s=%s>' % (
            self.role, self.entity_type, self.entity_id)

    def to_api_repr(self):
        """Construct the API resource representation of this access entry

        Returns:
            dict: Access entry represented as an API resource
        """
        resource = {self.entity_type: self.entity_id}
        if self.role is not None:
            resource['role'] = self.role
        return resource

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct an access entry given its API representation

        Args:
            resource (dict):
                Access entry resource representation returned from the API

        Returns:
            google.cloud.bigquery.dataset.AccessEntry:
                Access entry parsed from ``resource``.

        Raises:
            ValueError:
                If the resource has more keys than ``role`` and one additional
                key.
        """
        entry = resource.copy()
        role = entry.pop('role', None)
        entity_type, entity_id = entry.popitem()
        if len(entry) != 0:
            raise ValueError('Entry has unexpected keys remaining.', entry)
        return cls(role, entity_type, entity_id)


class DatasetReference(object):
    """DatasetReferences are pointers to datasets.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets

    Args:
        project (str): The ID of the project
        dataset_id (str): The ID of the dataset

    Raises:
        ValueError: If either argument is not of type ``str``.
    """

    def __init__(self, project, dataset_id):
        if not isinstance(project, six.string_types):
            raise ValueError("Pass a string for project")
        if not isinstance(dataset_id, six.string_types):
            raise ValueError("Pass a string for dataset_id")
        self._project = project
        self._dataset_id = dataset_id

    @property
    def project(self):
        """Project ID of the dataset.

        Returns:
            str: The project ID.
        """
        return self._project

    @property
    def dataset_id(self):
        """Dataset ID.

        Returns:
            str: The dataset ID.
        """
        return self._dataset_id

    @property
    def path(self):
        """URL path for the dataset's APIs.

        Returns:
            str: the path based on project and dataset name.
        """
        return '/projects/%s/datasets/%s' % (self.project, self.dataset_id)

    def table(self, table_id):
        """Constructs a TableReference.

        Args:
            table_id (str): The ID of the table.

        Returns:
            google.cloud.bigquery.table.TableReference:
                A table reference for a table in this dataset.
        """
        return TableReference(self, table_id)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a dataset reference given its API representation

        Args:
            resource (dict):
                Dataset reference resource representation returned from the API

        Returns:
            google.cloud.bigquery.dataset.DatasetReference:
                Dataset reference parsed from ``resource``.
        """
        project = resource['projectId']
        dataset_id = resource['datasetId']
        return cls(project, dataset_id)

    def to_api_repr(self):
        """Construct the API resource representation of this dataset reference

        Returns:
            dict: dataset reference represented as an API resource
        """
        return {
            'projectId': self._project,
            'datasetId': self._dataset_id,
        }

    def _key(self):
        """A tuple key that uniquely describes this field.

        Used to compute this instance's hashcode and evaluate equality.

        Returns:
            tuple: The contents of this :class:`.DatasetReference`.
        """
        return (
            self._project,
            self._dataset_id,
        )

    def __eq__(self, other):
        if not isinstance(other, DatasetReference):
            return NotImplemented
        return self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return 'DatasetReference{}'.format(self._key())


class Dataset(object):
    """Datasets are containers for tables.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets

    Args:
        dataset_ref (google.cloud.bigquery.dataset.DatasetReference):
            a pointer to a dataset
    """

    _PROPERTY_TO_API_FIELD = {
        'access_entries': 'access',
        'created': 'creationTime',
        'default_table_expiration_ms': 'defaultTableExpirationMs',
        'description': 'description',
        'friendly_name': 'friendlyName',
        'location': 'location',
        'labels': 'labels',
    }

    def __init__(self, dataset_ref):
        self._properties = {
            'datasetReference': dataset_ref.to_api_repr(),
            'labels': {},
        }

    @property
    def project(self):
        """Project bound to the dataset.

        Returns:
            str: the project ID
        """
        return self._properties['datasetReference']['projectId']

    @property
    def path(self):
        """URL path for the dataset's APIs.

        Returns:
            str: the path based on project and dataset ID.
        """
        return '/projects/%s/datasets/%s' % (self.project, self.dataset_id)

    @property
    def access_entries(self):
        """Dataset's access entries.

        ``role`` augments the entity type and must be present **unless** the
        entity type is ``view``.

        Returns:
            List[google.cloud.bigquery.dataset.AccessEntry]:
                roles granted to entities for this dataset
        """
        entries = self._properties.get('access', [])
        return [AccessEntry.from_api_repr(entry) for entry in entries]

    @access_entries.setter
    def access_entries(self, value):
        """Update dataset's access entries

        Args:
            value (List[google.cloud.bigquery.dataset.AccessEntry]):
                Roles granted to entities for this dataset

        Raises:
            TypeError: If 'value' is not a sequence
            ValueError:
                If any item in the sequence is not an
                :class:`~google.cloud.bigquery.dataset.AccessEntry`.
        """
        if not all(isinstance(field, AccessEntry) for field in value):
            raise ValueError('Values must be AccessEntry instances')
        entries = [entry.to_api_repr() for entry in value]
        self._properties['access'] = entries

    @property
    def created(self):
        """Datetime at which the dataset was created.

        Returns:
            Union[datetime.datetime, None]:
                the creation time (``None`` until set from the server).
        """
        creation_time = self._properties.get('creationTime')
        if creation_time is not None:
            # creation_time will be in milliseconds.
            return _datetime_from_microseconds(1000.0 * creation_time)

    @property
    def dataset_id(self):
        """Dataset ID.

        Returns:
            str: the dataset ID.
        """
        return self._properties['datasetReference']['datasetId']

    @property
    def full_dataset_id(self):
        """ID for the dataset resource, in the form ``project_id:dataset_id``.

        Returns:
            Union[str, None]: the ID (``None`` until set from the server).
        """
        return self._properties.get('id')

    @property
    def reference(self):
        """A reference to this dataset.

        Returns:
            google.cloud.bigquery.dataset.DatasetReference:
                A pointer to this dataset
        """
        return DatasetReference(self.project, self.dataset_id)

    @property
    def etag(self):
        """ETag for the dataset resource.

        Returns:
            Union[str, None]: The ETag (``None`` until set from the server).
        """
        return self._properties.get('etag')

    @property
    def modified(self):
        """Datetime at which the dataset was last modified.

        Returns:
            Union[datetime.datetime, None]:
                The modification time (``None`` until set from the server).
        """
        modified_time = self._properties.get('lastModifiedTime')
        if modified_time is not None:
            # modified_time will be in milliseconds.
            return _datetime_from_microseconds(1000.0 * modified_time)

    @property
    def self_link(self):
        """URL for the dataset resource.

        Returns:
            Union[str, None]: the URL (``None`` until set from the server).
        """
        return self._properties.get('selfLink')

    @property
    def default_table_expiration_ms(self):
        """Default expiration time for tables in the dataset.

        Returns:
            Union[int, None]:
                The time in milliseconds, or ``None`` (the default).
        """
        return self._properties.get('defaultTableExpirationMs')

    @default_table_expiration_ms.setter
    def default_table_expiration_ms(self, value):
        """Update default expiration time for tables in the dataset.

        Args:
            value (int, optional): new default time, in milliseconds

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.integer_types) and value is not None:
            raise ValueError("Pass an integer, or None")
        self._properties['defaultTableExpirationMs'] = value

    @property
    def description(self):
        """Description of the dataset.

        Returns:
            Union[str, None]:
                The description as set by the user, or ``None`` (the default).
        """
        return self._properties.get('description')

    @description.setter
    def description(self, value):
        """Update description of the dataset.

        Args:
            value (str, optional): new description

        Raises:
            ValueError: for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['description'] = value

    @property
    def friendly_name(self):
        """Title of the dataset.

        Returns:
            Union[str, None]:
                The name as set by the user, or ``None`` (the default).
        """
        return self._properties.get('friendlyName')

    @friendly_name.setter
    def friendly_name(self, value):
        """Update title of the dataset.

        Args:
            value (str, optional): new title

        Raises:
            ValueError: for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['friendlyName'] = value

    @property
    def location(self):
        """Location in which the dataset is hosted.

        Returns:
            Union[str, None]:
                The location as set by the user, or ``None`` (the default).
        """
        return self._properties.get('location')

    @location.setter
    def location(self, value):
        """Update location in which the dataset is hosted.

        Args:
            value (str, optional): the new location

        Raises:
            ValueError: for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['location'] = value

    @property
    def labels(self):
        """Labels for the dataset.

        This method always returns a dict. To change a dataset's labels,
        modify the dict, then call
        :meth:`google.cloud.bigquery.client.Client.update_dataset`. To delete
        a label, set its value to ``None`` before updating.

        Returns:
            Dict[str, str]: A dict of the the dataset's labels.
        """
        return self._properties.get('labels', {})

    @labels.setter
    def labels(self, value):
        """Update labels for the dataset.

        Args:
            value (Dict[str, str]): new labels

        Raises:
            ValueError: for invalid value types.
        """
        if not isinstance(value, dict):
            raise ValueError("Pass a dict")
        self._properties['labels'] = value

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a dataset given its API representation

        Args:
            resource (dict):
                Dataset resource representation returned from the API

        Returns:
            google.cloud.bigquery.dataset.Dataset:
                Dataset parsed from ``resource``.
        """
        if ('datasetReference' not in resource or
                'datasetId' not in resource['datasetReference']):
            raise KeyError('Resource lacks required identity information:'
                           '["datasetReference"]["datasetId"]')
        project_id = resource['datasetReference']['projectId']
        dataset_id = resource['datasetReference']['datasetId']
        dataset = cls(DatasetReference(project_id, dataset_id))
        dataset._properties = copy.deepcopy(resource)
        return dataset

    def to_api_repr(self):
        """Construct the API resource representation of this dataset

        Returns:
            dict: The dataset represented as an API resource
        """
        return copy.deepcopy(self._properties)

    def _build_resource(self, filter_fields):
        """Generate a resource for ``create`` or ``update``."""
        partial = {}
        for f in filter_fields:
            if not hasattr(self, f) and f not in self._properties:
                raise ValueError('No Dataset property %s' % f)
            api_field = self._PROPERTY_TO_API_FIELD.get(f)
            if api_field:
                partial[api_field] = self._properties.get(api_field)
            else:
                # allows properties that are not defined in the library
                partial[f] = self._properties[f]

        return partial

    def table(self, table_id):
        """Constructs a TableReference.

        Args:
            table_id (str): the ID of the table.

        Returns:
            google.cloud.bigquery.table.TableReference:
                A TableReference for a table in this dataset.
        """
        return TableReference(self.reference, table_id)


class DatasetListItem(object):
    """A read-only dataset resource from a list operation.

    For performance reasons, the BigQuery API only includes some of the
    dataset properties when listing datasets. Notably,
    :attr:`~google.cloud.bigquery.dataset.Dataset.access_entries` is missing.

    For a full list of the properties that the BigQuery API returns, see the
    `REST documentation for datasets.list
    <https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/list>`_.


    Args:
        resource (dict):
            A dataset-like resource object from a dataset list response. A
            ``datasetReference`` property is required.

    Raises:
        ValueError:
            If ``datasetReference`` or one of its required members is missing
            from ``resource``.
    """

    def __init__(self, resource):
        if 'datasetReference' not in resource:
            raise ValueError('resource must contain a datasetReference value')
        if 'projectId' not in resource['datasetReference']:
            raise ValueError(
                "resource['datasetReference'] must contain a projectId value")
        if 'datasetId' not in resource['datasetReference']:
            raise ValueError(
                "resource['datasetReference'] must contain a datasetId value")
        self._properties = resource

    @property
    def project(self):
        """Project bound to the dataset.

        :rtype: str
        :returns: the project.
        """
        return self._properties['datasetReference']['projectId']

    @property
    def dataset_id(self):
        """Dataset ID.

        :rtype: str
        :returns: the dataset ID.
        """
        return self._properties['datasetReference']['datasetId']

    @property
    def full_dataset_id(self):
        """ID for the dataset resource, in the form "project_id:dataset_id".

        :rtype: str, or ``NoneType``
        :returns: the ID (None until set from the server).
        """
        return self._properties.get('id')

    @property
    def friendly_name(self):
        """Title of the dataset.

        :rtype: str, or ``NoneType``
        :returns: The name as set by the user, or None (the default).
        """
        return self._properties.get('friendlyName')

    @property
    def labels(self):
        """Labels for the dataset.

        :rtype: dict, {str -> str}
        :returns: A dict of the the dataset's labels.
        """
        return self._properties.get('labels', {})

    @property
    def reference(self):
        """A reference to this dataset.

        Returns:
            google.cloud.bigquery.dataset.DatasetReference:
                A pointer to this dataset
        """
        return DatasetReference(self.project, self.dataset_id)

    def table(self, table_id):
        """Constructs a TableReference.

        :type table_id: str
        :param table_id: the ID of the table.

        :rtype: :class:`~google.cloud.bigquery.table.TableReference`
        :returns: a TableReference for a table in this dataset.
        """
        return TableReference(self.reference, table_id)
