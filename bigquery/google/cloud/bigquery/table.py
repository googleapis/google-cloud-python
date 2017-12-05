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

"""Define API Tables."""

from __future__ import absolute_import

import copy
import datetime
import operator

import six
try:
    import pandas
except ImportError:  # pragma: NO COVER
    pandas = None

from google.api_core.page_iterator import HTTPIterator

from google.cloud._helpers import _datetime_from_microseconds
from google.cloud._helpers import _millis_from_datetime
from google.cloud.bigquery._helpers import _item_to_row
from google.cloud.bigquery._helpers import _rows_page_start
from google.cloud.bigquery._helpers import _snake_to_camel_case
from google.cloud.bigquery._helpers import _field_to_index_mapping
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery.schema import _build_schema_resource
from google.cloud.bigquery.schema import _parse_schema_resource
from google.cloud.bigquery.external_config import ExternalConfig


_TABLE_HAS_NO_SCHEMA = "Table has no schema:  call 'client.get_table()'"
_MARKER = object()


def _reference_getter(table):
    """A :class:`~google.cloud.bigquery.table.TableReference` pointing to
    this table.

    Returns:
        google.cloud.bigquery.table.TableReference: pointer to this table.
    """
    from google.cloud.bigquery import dataset

    dataset_ref = dataset.DatasetReference(table.project, table.dataset_id)
    return TableReference(dataset_ref, table.table_id)


def _view_use_legacy_sql_getter(table):
    """Specifies whether to execute the view with Legacy or Standard SQL.

    If this table is not a view, None is returned.

    Returns:
        bool: True if the view is using legacy SQL, or None if not a view
    """
    view = table._properties.get('view')
    if view is not None:
        # The server-side default for useLegacySql is True.
        return view.get('useLegacySql', True)
    # In some cases, such as in a table list no view object is present, but the
    # resource still represents a view. Use the type as a fallback.
    if table.table_type == 'VIEW':
        # The server-side default for useLegacySql is True.
        return True


class TableReference(object):
    """TableReferences are pointers to tables.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables

    :type dataset_ref: :class:`google.cloud.bigquery.dataset.DatasetReference`
    :param dataset_ref: a pointer to the dataset

    :type table_id: str
    :param table_id: the ID of the table
    """

    def __init__(self, dataset_ref, table_id):
        self._project = dataset_ref.project
        self._dataset_id = dataset_ref.dataset_id
        self._table_id = table_id

    @property
    def project(self):
        """Project bound to the table.

        :rtype: str
        :returns: the project (derived from the dataset reference).
        """
        return self._project

    @property
    def dataset_id(self):
        """ID of dataset containing the table.

        :rtype: str
        :returns: the ID (derived from the dataset reference).
        """
        return self._dataset_id

    @property
    def table_id(self):
        """Table ID.

        :rtype: str
        :returns: the table ID.
        """
        return self._table_id

    @property
    def path(self):
        """URL path for the table's APIs.

        :rtype: str
        :returns: the path based on project, dataset and table IDs.
        """
        return '/projects/%s/datasets/%s/tables/%s' % (
            self._project, self._dataset_id, self._table_id)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory:  construct a table reference given its API representation

        :type resource: dict
        :param resource: table reference representation returned from the API

        :rtype: :class:`google.cloud.bigquery.table.TableReference`
        :returns: Table reference parsed from ``resource``.
        """
        from google.cloud.bigquery.dataset import DatasetReference

        project = resource['projectId']
        dataset_id = resource['datasetId']
        table_id = resource['tableId']
        return cls(DatasetReference(project, dataset_id), table_id)

    def to_api_repr(self):
        """Construct the API resource representation of this table reference.

        :rtype: dict
        :returns: Table reference as represented as an API resource
        """
        return {
            'projectId': self._project,
            'datasetId': self._dataset_id,
            'tableId': self._table_id,
        }

    def _key(self):
        """A tuple key that uniquely describes this field.

        Used to compute this instance's hashcode and evaluate equality.

        Returns:
            tuple: The contents of this :class:`DatasetReference`.
        """
        return (
            self._project,
            self._dataset_id,
            self._table_id,
        )

    def __eq__(self, other):
        if not isinstance(other, TableReference):
            return NotImplemented
        return self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return 'TableReference{}'.format(self._key())


class Table(object):
    """Tables represent a set of rows whose values correspond to a schema.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables

    :type table_ref: :class:`google.cloud.bigquery.table.TableReference`
    :param table_ref: a pointer to a table

    :type schema: list of :class:`~google.cloud.bigquery.schema.SchemaField`
    :param schema: The table's schema
    """

    _schema = None

    all_fields = [
        'description', 'friendly_name', 'expires', 'location',
        'partitioning_type', 'view_use_legacy_sql', 'view_query', 'schema',
        'external_data_configuration', 'labels',
    ]

    def __init__(self, table_ref, schema=()):
        self._project = table_ref.project
        self._table_id = table_ref.table_id
        self._dataset_id = table_ref.dataset_id
        self._external_config = None
        self._properties = {'labels': {}}
        # Let the @property do validation.
        self.schema = schema

    @property
    def project(self):
        """Project bound to the table.

        :rtype: str
        :returns: the project (derived from the dataset).
        """
        return self._project

    @property
    def dataset_id(self):
        """ID of dataset containing the table.

        :rtype: str
        :returns: the ID (derived from the dataset).
        """
        return self._dataset_id

    @property
    def table_id(self):
        """ID of the table.

        :rtype: str
        :returns: the table ID.
        """
        return self._table_id

    reference = property(_reference_getter)

    @property
    def path(self):
        """URL path for the table's APIs.

        :rtype: str
        :returns: the path based on project, dataset and table IDs.
        """
        return '/projects/%s/datasets/%s/tables/%s' % (
            self._project, self._dataset_id, self._table_id)

    @property
    def schema(self):
        """Table's schema.

        :rtype: list of :class:`~google.cloud.bigquery.schema.SchemaField`
        :returns: fields describing the schema
        """
        return list(self._schema)

    @schema.setter
    def schema(self, value):
        """Update table's schema

        :type value: list of :class:`~google.cloud.bigquery.schema.SchemaField`
        :param value: fields describing the schema

        :raises: TypeError if 'value' is not a sequence, or ValueError if
                 any item in the sequence is not a SchemaField
        """
        if value is None:
            self._schema = ()
        elif not all(isinstance(field, SchemaField) for field in value):
            raise ValueError('Schema items must be fields')
        else:
            self._schema = tuple(value)

    @property
    def labels(self):
        """Labels for the table.

        This method always returns a dict. To change a table's labels,
        modify the dict, then call ``Client.update_table``. To delete a
        label, set its value to ``None`` before updating.

        :rtype: dict, {str -> str}
        :returns: A dict of the the table's labels.
        """
        return self._properties.get('labels', {})

    @labels.setter
    def labels(self, value):
        """Update labels for the table.

        :type value: dict, {str -> str}
        :param value: new labels

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, dict):
            raise ValueError("Pass a dict")
        self._properties['labels'] = value

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
    def full_table_id(self):
        """ID for the table, in the form ``project_id:dataset_id:table_id``.

        :rtype: str, or ``NoneType``
        :returns: the full ID (None until set from the server).
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
        :param value: partition experiation time in milliseconds
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

        By default, the query is treated as Standard SQL. To use Legacy
        SQL, set view_use_legacy_sql to True.

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
        view = self._properties.get('view')
        if view is None:
            view = self._properties['view'] = {}
        view['query'] = value
        # The service defaults useLegacySql to True, but this
        # client uses Standard SQL by default.
        if view.get('useLegacySql') is None:
            view['useLegacySql'] = False

    @view_query.deleter
    def view_query(self):
        """Delete SQL query defining the table as a view."""
        self._properties.pop('view', None)

    view_use_legacy_sql = property(_view_use_legacy_sql_getter)

    @view_use_legacy_sql.setter
    def view_use_legacy_sql(self, value):
        """Update the view sub-property 'useLegacySql'.

        This boolean specifies whether to execute the view with Legacy SQL
        (True) or Standard SQL (False). The default, if not specified, is
        'False'.

        :type value: bool
        :param value: The boolean for view.useLegacySql

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, bool):
            raise ValueError("Pass a boolean")
        if self._properties.get('view') is None:
            self._properties['view'] = {}
        self._properties['view']['useLegacySql'] = value

    @property
    def streaming_buffer(self):
        """Information about a table's streaming buffer.

        :rtype: :class:`~google.cloud.bigquery.StreamingBuffer`
        :returns: Streaming buffer information, returned from get_table.
        """
        sb = self._properties.get('streamingBuffer')
        if sb is not None:
            return StreamingBuffer(sb)

    @property
    def external_data_configuration(self):
        """Configuration for an external data source.

        If not set, None is returned.

        :rtype: :class:`~google.cloud.bigquery.ExternalConfig`, or ``NoneType``
        :returns: The external configuration, or None (the default).
        """
        return self._external_config

    @external_data_configuration.setter
    def external_data_configuration(self, value):
        """Sets the configuration for an external data source.

        :type value:
            :class:`~google.cloud.bigquery.ExternalConfig`, or ``NoneType``
        :param value: The ExternalConfig, or None to unset.
        """
        if not (value is None or isinstance(value, ExternalConfig)):
            raise ValueError("Pass an ExternalConfig or None")
        self._external_config = value

    @classmethod
    def from_api_repr(cls, resource):
        """Factory:  construct a table given its API representation

        :type resource: dict
        :param resource: table resource representation returned from the API

        :type dataset: :class:`google.cloud.bigquery.dataset.Dataset`
        :param dataset: The dataset containing the table.

        :rtype: :class:`google.cloud.bigquery.table.Table`
        :returns: Table parsed from ``resource``.
        """
        from google.cloud.bigquery import dataset

        if ('tableReference' not in resource or
                'tableId' not in resource['tableReference']):
            raise KeyError('Resource lacks required identity information:'
                           '["tableReference"]["tableId"]')
        project_id = resource['tableReference']['projectId']
        table_id = resource['tableReference']['tableId']
        dataset_id = resource['tableReference']['datasetId']
        dataset_ref = dataset.DatasetReference(project_id, dataset_id)

        table = cls(dataset_ref.table(table_id))
        table._set_properties(resource)
        return table

    def _set_properties(self, api_response):
        """Update properties from resource in body of ``api_response``

        :type api_response: dict
        :param api_response: response returned from an API call
        """
        self._properties.clear()
        cleaned = api_response.copy()
        schema = cleaned.pop('schema', {'fields': ()})
        self.schema = _parse_schema_resource(schema)
        ec = cleaned.pop('externalDataConfiguration', None)
        if ec:
            self.external_data_configuration = ExternalConfig.from_api_repr(ec)
        if 'creationTime' in cleaned:
            cleaned['creationTime'] = float(cleaned['creationTime'])
        if 'lastModifiedTime' in cleaned:
            cleaned['lastModifiedTime'] = float(cleaned['lastModifiedTime'])
        if 'expirationTime' in cleaned:
            cleaned['expirationTime'] = float(cleaned['expirationTime'])
        if 'labels' not in cleaned:
            cleaned['labels'] = {}
        self._properties.update(cleaned)

    def _populate_expires_resource(self, resource):
        resource['expirationTime'] = _millis_from_datetime(self.expires)

    def _populate_partitioning_type_resource(self, resource):
        resource['timePartitioning'] = self._properties.get('timePartitioning')

    def _populate_view_use_legacy_sql_resource(self, resource):
        if 'view' not in resource:
            resource['view'] = {}
        resource['view']['useLegacySql'] = self.view_use_legacy_sql

    def _populate_view_query_resource(self, resource):
        if self.view_query is None:
            resource['view'] = None
            return
        if 'view' not in resource:
            resource['view'] = {}
        resource['view']['query'] = self.view_query

    def _populate_schema_resource(self, resource):
        if not self._schema:
            resource['schema'] = None
        else:
            resource['schema'] = {
                'fields': _build_schema_resource(self._schema),
            }

    def _populate_external_config(self, resource):
        if not self.external_data_configuration:
            resource['externalDataConfiguration'] = None
        else:
            resource['externalDataConfiguration'] = ExternalConfig.to_api_repr(
                self.external_data_configuration)

    custom_resource_fields = {
        'expires': _populate_expires_resource,
        'partitioning_type': _populate_partitioning_type_resource,
        'view_query': _populate_view_query_resource,
        'view_use_legacy_sql': _populate_view_use_legacy_sql_resource,
        'schema': _populate_schema_resource,
        'external_data_configuration': _populate_external_config,
    }

    def _build_resource(self, filter_fields):
        """Generate a resource for ``create`` or ``update``."""
        resource = {
            'tableReference': {
                'projectId': self._project,
                'datasetId': self._dataset_id,
                'tableId': self.table_id},
        }
        for f in filter_fields:
            if f in self.custom_resource_fields:
                self.custom_resource_fields[f](self, resource)
            else:
                api_field = _snake_to_camel_case(f)
                resource[api_field] = getattr(self, f)
        return resource


class TableListItem(object):
    """A read-only table resource from a list operation.

    For performance reasons, the BigQuery API only includes some of the table
    properties when listing tables. Notably,
    :attr:`~google.cloud.bigquery.table.Table.schema` and
    :attr:`~google.cloud.bigquery.table.Table.num_rows` are missing.

    For a full list of the properties that the BigQuery API returns, see the
    `REST documentation for tables.list
    <https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/list>`_.


    Args:
        resource (dict):
            A table-like resource object from a table list response. A
            ``tableReference`` property is required.

    Raises:
        ValueError:
            If ``tableReference`` or one of its required members is missing
            from ``resource``.
    """

    def __init__(self, resource):
        if 'tableReference' not in resource:
            raise ValueError('resource must contain a tableReference value')
        if 'projectId' not in resource['tableReference']:
            raise ValueError(
                "resource['tableReference'] must contain a projectId value")
        if 'datasetId' not in resource['tableReference']:
            raise ValueError(
                "resource['tableReference'] must contain a datasetId value")
        if 'tableId' not in resource['tableReference']:
            raise ValueError(
                "resource['tableReference'] must contain a tableId value")

        self._properties = resource

    @property
    def project(self):
        """The project ID of the project this table belongs to.

        Returns:
            str: the project ID of the table.
        """
        return self._properties['tableReference']['projectId']

    @property
    def dataset_id(self):
        """The dataset ID of the dataset this table belongs to.

        Returns:
            str: the dataset ID of the table.
        """
        return self._properties['tableReference']['datasetId']

    @property
    def table_id(self):
        """The table ID.

        Returns:
            str: the table ID.
        """
        return self._properties['tableReference']['tableId']

    reference = property(_reference_getter)

    @property
    def labels(self):
        """Labels for the table.

        This method always returns a dict. To change a table's labels,
        modify the dict, then call ``Client.update_table``. To delete a
        label, set its value to ``None`` before updating.

        Returns:
            Map[str, str]: A dictionary of the the table's labels
        """
        return self._properties.get('labels', {})

    @property
    def full_table_id(self):
        """ID for the table, in the form ``project_id:dataset_id:table_id``.

        Returns:
            str: The fully-qualified ID of the table
        """
        return self._properties.get('id')

    @property
    def table_type(self):
        """The type of the table.

        Possible values are "TABLE", "VIEW", or "EXTERNAL".

        Returns:
            str: The kind of table
        """
        return self._properties.get('type')

    @property
    def partitioning_type(self):
        """Time partitioning of the table.

        Returns:
            str:
                Type of partitioning if the table is partitioned, None
                otherwise.
        """
        return self._properties.get('timePartitioning', {}).get('type')

    @property
    def partition_expiration(self):
        """Expiration time in ms for a partition

        Returns:
            int: The time in ms for partition expiration
        """
        expiration = self._properties.get(
            'timePartitioning', {}).get('expirationMs')
        if expiration is not None:
            return int(expiration)

    @property
    def friendly_name(self):
        """Title of the table.

        Returns:
            str: The name as set by the user, or None (the default)
        """
        return self._properties.get('friendlyName')

    view_use_legacy_sql = property(_view_use_legacy_sql_getter)


def _row_from_mapping(mapping, schema):
    """Convert a mapping to a row tuple using the schema.

    :type mapping: dict
    :param mapping: Mapping of row data: must contain keys for all
           required fields in the schema.  Keys which do not correspond
           to a field in the schema are ignored.

    :type schema: list of :class:`~google.cloud.bigquery.schema.SchemaField`
    :param schema: The schema of the table destination for the rows

    :rtype: tuple
    :returns: Tuple whose elements are ordered according to the schema.
    :raises: ValueError if schema is empty
    """
    if len(schema) == 0:
        raise ValueError(_TABLE_HAS_NO_SCHEMA)

    row = []
    for field in schema:
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


class StreamingBuffer(object):
    """Information about a table's streaming buffer.

    See https://cloud.google.com/bigquery/streaming-data-into-bigquery.

    :type resource: dict
    :param resource: streaming buffer representation returned from the API
    """

    def __init__(self, resource):
        self.estimated_bytes = int(resource['estimatedBytes'])
        self.estimated_rows = int(resource['estimatedRows'])
        # time is in milliseconds since the epoch.
        self.oldest_entry_time = _datetime_from_microseconds(
            1000.0 * int(resource['oldestEntryTime']))


class Row(object):
    """A BigQuery row.

    Values can be accessed by position (index), by key like a dict,
    or as properties.

    :type values: tuple
    :param values:  the row values

    :type field_to_index: dict
    :param field_to_index:  a mapping from schema field names to indexes
    """

    # Choose unusual field names to try to avoid conflict with schema fields.
    __slots__ = ('_xxx_values', '_xxx_field_to_index')

    def __init__(self, values, field_to_index):
        self._xxx_values = values
        self._xxx_field_to_index = field_to_index

    def values(self):
        """Return the values included in this row.

        Returns:
            Sequence[object]: A sequence of length ``len(row)``.
        """
        return copy.deepcopy(self._xxx_values)

    def keys(self):
        """Return the keys for using a row as a dict.

        Returns:
            Sequence[str]: The keys corresponding to the columns of a row

        Examples:

            >>> list(Row(('a', 'b'), {'x': 0, 'y': 1}).keys())
            ['x', 'y']
        """
        return six.iterkeys(self._xxx_field_to_index)

    def items(self):
        """Return items as ``(key, value)`` pairs.

        Returns:
            Sequence[Tuple[str, object]]:
                The ``(key, value)`` pairs representing this row.

        Examples:

            >>> list(Row(('a', 'b'), {'x': 0, 'y': 1}).items())
            [('x', 'a'), ('y', 'b')]
        """
        for key, index in six.iteritems(self._xxx_field_to_index):
            yield (key, copy.deepcopy(self._xxx_values[index]))

    def get(self, key, default=None):
        """Return a value for key, with a default value if it does not exist.

        Args:
            key (str): The key of the column to access
            default (object):
                The default value to use if the key does not exist. (Defaults
                to :data:`None`.)

        Returns:
            object:
                The value associated with the provided key, or a default value.

        Examples:
            When the key exists, the value associated with it is returned.

            >>> Row(('a', 'b'), {'x': 0, 'y': 1}).get('x')
            'a'

            The default value is ``None`` when the key does not exist.

            >>> Row(('a', 'b'), {'x': 0, 'y': 1}).get('z')
            None

            The default value can be overrided with the ``default`` parameter.

            >>> Row(('a', 'b'), {'x': 0, 'y': 1}).get('z', '')
            ''

            >>> Row(('a', 'b'), {'x': 0, 'y': 1}).get('z', default = '')
            ''
        """
        index = self._xxx_field_to_index.get(key)
        if index is None:
            return default
        return self._xxx_values[index]

    def __getattr__(self, name):
        value = self._xxx_field_to_index.get(name)
        if value is None:
            raise AttributeError('no row field {!r}'.format(name))
        return self._xxx_values[value]

    def __len__(self):
        return len(self._xxx_values)

    def __getitem__(self, key):
        if isinstance(key, six.string_types):
            value = self._xxx_field_to_index.get(key)
            if value is None:
                raise KeyError('no row field {!r}'.format(key))
            key = value
        return self._xxx_values[key]

    def __eq__(self, other):
        if not isinstance(other, Row):
            return NotImplemented
        return(
            self._xxx_values == other._xxx_values and
            self._xxx_field_to_index == other._xxx_field_to_index)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        # sort field dict by value, for determinism
        items = sorted(self._xxx_field_to_index.items(),
                       key=operator.itemgetter(1))
        f2i = '{' + ', '.join('%r: %d' % item for item in items) + '}'
        return 'Row({}, {})'.format(self._xxx_values, f2i)


class RowIterator(HTTPIterator):
    """A class for iterating through HTTP/JSON API row list responses.

    Args:
        client (google.cloud.bigquery.Client): The API client.
        api_request (Callable[google.cloud._http.JSONConnection.api_request]):
            The function to use to make API requests.
        path (str): The method path to query for the list of items.
        page_token (str): A token identifying a page in a result set to start
            fetching results from.
        max_results (int): The maximum number of results to fetch.
        extra_params (dict): Extra query string parameters for the API call.

    .. autoattribute:: pages
    """

    def __init__(self, client, api_request, path, schema, page_token=None,
                 max_results=None, extra_params=None):
        super(RowIterator, self).__init__(
            client, api_request, path, item_to_value=_item_to_row,
            items_key='rows', page_token=page_token, max_results=max_results,
            extra_params=extra_params, page_start=_rows_page_start,
            next_token='pageToken')
        self._schema = schema
        self._field_to_index = _field_to_index_mapping(schema)
        self._total_rows = None

    @property
    def schema(self):
        """Schema for the table containing the rows

        Returns:
            list of :class:`~google.cloud.bigquery.schema.SchemaField`:
                fields describing the schema
        """
        return list(self._schema)

    @property
    def total_rows(self):
        """The total number of rows in the table.

        Returns:
            int: the row count.
        """
        return self._total_rows

    def to_dataframe(self):
        """Create a pandas DataFrame from the query results.

        Returns:
            A :class:`~pandas.DataFrame` populated with row data and column
            headers from the query results. The column headers are derived
            from the destination table's schema.

        Raises:
            ValueError: If the `pandas` library cannot be imported.

        """
        if pandas is None:
            raise ValueError('The pandas library is not installed, please '
                             'install pandas to use the to_dataframe() '
                             'function.')

        column_headers = [field.name for field in self.schema]
        rows = [row.values() for row in iter(self)]

        return pandas.DataFrame(rows, columns=column_headers)
