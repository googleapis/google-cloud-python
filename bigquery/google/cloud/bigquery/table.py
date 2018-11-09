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
import warnings

import six
try:
    import pandas
except ImportError:  # pragma: NO COVER
    pandas = None

from google.api_core.page_iterator import HTTPIterator

import google.cloud._helpers
from google.cloud.bigquery import _helpers
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery.schema import _build_schema_resource
from google.cloud.bigquery.schema import _parse_schema_resource
from google.cloud.bigquery.external_config import ExternalConfig


_NO_PANDAS_ERROR = (
    'The pandas library is not installed, please install '
    'pandas to use the to_dataframe() function.'
)
_TABLE_HAS_NO_SCHEMA = 'Table has no schema:  call "client.get_table()"'
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
    """bool: Specifies whether to execute the view with Legacy or Standard SQL.

    This boolean specifies whether to execute the view with Legacy SQL
    (:data:`True`) or Standard SQL (:data:`False`). The client side default is
    :data:`False`. The server-side default is :data:`True`. If this table is
    not a view, :data:`None` is returned.

    Raises:
        ValueError: For invalid value types.
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


class EncryptionConfiguration(object):
    """Custom encryption configuration (e.g., Cloud KMS keys).

    Args:
        kms_key_name (str): resource ID of Cloud KMS key used for encryption
    """

    def __init__(self, kms_key_name=None):
        self._properties = {}
        if kms_key_name is not None:
            self._properties['kmsKeyName'] = kms_key_name

    @property
    def kms_key_name(self):
        """str: Resource ID of Cloud KMS key

        Resource ID of Cloud KMS key or :data:`None` if using default
        encryption.
        """
        return self._properties.get('kmsKeyName')

    @kms_key_name.setter
    def kms_key_name(self, value):
        self._properties['kmsKeyName'] = value

    @classmethod
    def from_api_repr(cls, resource):
        """Construct an encryption configuration from its API representation

        Args:
            resource (Dict[str, object]):
                An encryption configuration representation as returned from
                the API.

        Returns:
            google.cloud.bigquery.table.EncryptionConfiguration:
                An encryption configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        return config

    def to_api_repr(self):
        """Construct the API resource representation of this encryption
        configuration.

        Returns:
            Dict[str, object]:
                Encryption configuration as represented as an API resource
        """
        return copy.deepcopy(self._properties)

    def __eq__(self, other):
        if not isinstance(other, EncryptionConfiguration):
            return NotImplemented
        return self.kms_key_name == other.kms_key_name

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.kms_key_name)

    def __repr__(self):
        return 'EncryptionConfiguration({})'.format(self.kms_key_name)


class TableReference(object):
    """TableReferences are pointers to tables.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables

    Args:
        dataset_ref (google.cloud.bigquery.dataset.DatasetReference):
            A pointer to the dataset
        table_id (str): The ID of the table
    """

    def __init__(self, dataset_ref, table_id):
        self._project = dataset_ref.project
        self._dataset_id = dataset_ref.dataset_id
        self._table_id = table_id

    @property
    def project(self):
        """str: Project bound to the table"""
        return self._project

    @property
    def dataset_id(self):
        """str: ID of dataset containing the table."""
        return self._dataset_id

    @property
    def table_id(self):
        """str: The table ID."""
        return self._table_id

    @property
    def path(self):
        """str: URL path for the table's APIs."""
        return '/projects/%s/datasets/%s/tables/%s' % (
            self._project, self._dataset_id, self._table_id)

    @classmethod
    def from_string(cls, table_id, default_project=None):
        """Construct a table reference from table ID string.

        Args:
            table_id (str):
                A table ID in standard SQL format. If ``default_project``
                is not specified, this must included a project ID, dataset
                ID, and table ID, each separated by ``.``.
            default_project (str):
                Optional. The project ID to use when ``table_id`` does not
                include a project ID.

        Returns:
            TableReference: Table reference parsed from ``table_id``.

        Examples:
            >>> TableReference.from_string('my-project.mydataset.mytable')
            TableRef...(DatasetRef...('my-project', 'mydataset'), 'mytable')

        Raises:
            ValueError:
                If ``table_id`` is not a fully-qualified table ID in
                standard SQL format.
        """
        from google.cloud.bigquery.dataset import DatasetReference

        output_project_id = default_project
        output_dataset_id = None
        output_table_id = None
        parts = table_id.split('.')

        if len(parts) < 2:
            raise ValueError(
                'table_id must be a fully-qualified table ID in '
                'standard SQL format. e.g. "project.dataset.table", got '
                '{}'.format(table_id))
        elif len(parts) == 2:
            if not default_project:
                raise ValueError(
                    'When default_project is not set, table_id must be a '
                    'fully-qualified table ID in standard SQL format. '
                    'e.g. "project.dataset_id.table_id", got {}'.format(
                        table_id))
            output_dataset_id, output_table_id = parts
        elif len(parts) == 3:
            output_project_id, output_dataset_id, output_table_id = parts
        if len(parts) > 3:
            raise ValueError(
                'Too many parts in table_id. Must be a fully-qualified table '
                'ID in standard SQL format. e.g. "project.dataset.table", '
                'got {}'.format(table_id))

        return cls(
            DatasetReference(output_project_id, output_dataset_id),
            output_table_id,
        )

    @classmethod
    def from_api_repr(cls, resource):
        """Factory:  construct a table reference given its API representation

        Args:
            resource (Dict[str, object]):
                Table reference representation returned from the API

        Returns:
            google.cloud.bigquery.table.TableReference:
                Table reference parsed from ``resource``.
        """
        from google.cloud.bigquery.dataset import DatasetReference

        project = resource['projectId']
        dataset_id = resource['datasetId']
        table_id = resource['tableId']
        return cls(DatasetReference(project, dataset_id), table_id)

    def to_api_repr(self):
        """Construct the API resource representation of this table reference.

        Returns:
            Dict[str, object]: Table reference represented as an API resource
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
            Tuple[str]: The contents of this :class:`DatasetReference`.
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
        from google.cloud.bigquery.dataset import DatasetReference
        dataset_ref = DatasetReference(self._project, self._dataset_id)
        return "TableReference({}, '{}')".format(
            repr(dataset_ref), self._table_id)


class Table(object):
    """Tables represent a set of rows whose values correspond to a schema.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables

    Args:
        table_ref (google.cloud.bigquery.table.TableReference):
            A pointer to a table
        schema (List[google.cloud.bigquery.schema.SchemaField]):
            The table's schema
    """

    _PROPERTY_TO_API_FIELD = {
        'friendly_name': 'friendlyName',
        'expires': 'expirationTime',
        'time_partitioning': 'timePartitioning',
        'partitioning_type': 'timePartitioning',
        'partition_expiration': 'timePartitioning',
        'view_use_legacy_sql': 'view',
        'view_query': 'view',
        'external_data_configuration': 'externalDataConfiguration',
        'encryption_configuration': 'encryptionConfiguration',
    }

    def __init__(self, table_ref, schema=None):
        self._properties = {
            'tableReference': table_ref.to_api_repr(),
            'labels': {},
        }
        # Let the @property do validation.
        if schema is not None:
            self.schema = schema

    @property
    def project(self):
        """str: Project bound to the table."""
        return self._properties['tableReference']['projectId']

    @property
    def dataset_id(self):
        """str: ID of dataset containing the table."""
        return self._properties['tableReference']['datasetId']

    @property
    def table_id(self):
        """str: ID of the table."""
        return self._properties['tableReference']['tableId']

    reference = property(_reference_getter)

    @property
    def path(self):
        """str: URL path for the table's APIs."""
        return '/projects/%s/datasets/%s/tables/%s' % (
            self.project, self.dataset_id, self.table_id)

    @property
    def schema(self):
        """List[google.cloud.bigquery.schema.SchemaField]: Table's schema.

        Raises:
            TypeError: If 'value' is not a sequence
            ValueError:
                If any item in the sequence is not a
                :class:`~google.cloud.bigquery.schema.SchemaField`
        """
        prop = self._properties.get('schema')
        if not prop:
            return []
        else:
            return _parse_schema_resource(prop)

    @schema.setter
    def schema(self, value):
        if value is None:
            self._properties['schema'] = None
        elif not all(isinstance(field, SchemaField) for field in value):
            raise ValueError('Schema items must be fields')
        else:
            self._properties['schema'] = {
                'fields': _build_schema_resource(value)
            }

    @property
    def labels(self):
        """Dict[str, str]: Labels for the table.

        This method always returns a dict. To change a table's labels,
        modify the dict, then call ``Client.update_table``. To delete a
        label, set its value to :data:`None` before updating.

        Raises:
            ValueError: If ``value`` type is invalid.
        """
        return self._properties.setdefault('labels', {})

    @labels.setter
    def labels(self, value):
        if not isinstance(value, dict):
            raise ValueError("Pass a dict")
        self._properties['labels'] = value

    @property
    def encryption_configuration(self):
        """google.cloud.bigquery.table.EncryptionConfiguration: Custom
        encryption configuration for the table.

        Custom encryption configuration (e.g., Cloud KMS keys) or :data:`None`
        if using default encryption.

        See `protecting data with Cloud KMS keys
        <https://cloud.google.com/bigquery/docs/customer-managed-encryption>`_
        in the BigQuery documentation.
        """
        prop = self._properties.get('encryptionConfiguration')
        if prop is not None:
            prop = EncryptionConfiguration.from_api_repr(prop)
        return prop

    @encryption_configuration.setter
    def encryption_configuration(self, value):
        api_repr = value
        if value is not None:
            api_repr = value.to_api_repr()
        self._properties['encryptionConfiguration'] = api_repr

    @property
    def created(self):
        """Union[datetime.datetime, None]: Datetime at which the table was
        created (:data:`None` until set from the server).
        """
        creation_time = self._properties.get('creationTime')
        if creation_time is not None:
            # creation_time will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(creation_time))

    @property
    def etag(self):
        """Union[str, None]: ETag for the table resource (:data:`None` until
        set from the server).
        """
        return self._properties.get('etag')

    @property
    def modified(self):
        """Union[datetime.datetime, None]: Datetime at which the table was last
        modified (:data:`None` until set from the server).
        """
        modified_time = self._properties.get('lastModifiedTime')
        if modified_time is not None:
            # modified_time will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(modified_time))

    @property
    def num_bytes(self):
        """Union[int, None]: The size of the table in bytes (:data:`None` until
        set from the server).
        """
        return _helpers._int_or_none(self._properties.get('numBytes'))

    @property
    def num_rows(self):
        """Union[int, None]: The number of rows in the table (:data:`None`
        until set from the server).
        """
        return _helpers._int_or_none(self._properties.get('numRows'))

    @property
    def self_link(self):
        """Union[str, None]: URL for the table resource (:data:`None` until set
        from the server).
        """
        return self._properties.get('selfLink')

    @property
    def full_table_id(self):
        """Union[str, None]: ID for the table (:data:`None` until set from the
        server).

        In the format ``project_id:dataset_id.table_id``.
        """
        return self._properties.get('id')

    @property
    def table_type(self):
        """Union[str, None]: The type of the table (:data:`None` until set from
        the server).

        Possible values are ``'TABLE'``, ``'VIEW'``, or ``'EXTERNAL'``.
        """
        return self._properties.get('type')

    @property
    def time_partitioning(self):
        """google.cloud.bigquery.table.TimePartitioning: Configures time-based
        partitioning for a table.

        Raises:
            ValueError:
                If the value is not :class:`TimePartitioning` or :data:`None`.
        """
        prop = self._properties.get('timePartitioning')
        if prop is not None:
            return TimePartitioning.from_api_repr(prop)

    @time_partitioning.setter
    def time_partitioning(self, value):
        api_repr = value
        if isinstance(value, TimePartitioning):
            api_repr = value.to_api_repr()
        elif value is not None:
            raise ValueError(
                "value must be google.cloud.bigquery.table.TimePartitioning "
                "or None")
        self._properties['timePartitioning'] = api_repr

    @property
    def partitioning_type(self):
        """Union[str, None]: Time partitioning of the table if it is
        partitioned (Defaults to :data:`None`).

        The only partitioning type that is currently supported is
        :attr:`~google.cloud.bigquery.table.TimePartitioningType.DAY`.
        """
        warnings.warn(
            "This method will be deprecated in future versions. Please use "
            "Table.time_partitioning.type_ instead.",
            PendingDeprecationWarning, stacklevel=2)
        if self.time_partitioning is not None:
            return self.time_partitioning.type_

    @partitioning_type.setter
    def partitioning_type(self, value):
        warnings.warn(
            "This method will be deprecated in future versions. Please use "
            "Table.time_partitioning.type_ instead.",
            PendingDeprecationWarning, stacklevel=2)
        if self.time_partitioning is None:
            self._properties['timePartitioning'] = {}
        self._properties['timePartitioning']['type'] = value

    @property
    def partition_expiration(self):
        """Union[int, None]: Expiration time in milliseconds for a partition.

        If :attr:`partition_expiration` is set and :attr:`type_` is
        not set, :attr:`type_` will default to
        :attr:`~google.cloud.bigquery.table.TimePartitioningType.DAY`.
        """
        warnings.warn(
            "This method will be deprecated in future versions. Please use "
            "Table.time_partitioning.expiration_ms instead.",
            PendingDeprecationWarning, stacklevel=2)
        if self.time_partitioning is not None:
            return self.time_partitioning.expiration_ms

    @partition_expiration.setter
    def partition_expiration(self, value):
        warnings.warn(
            "This method will be deprecated in future versions. Please use "
            "Table.time_partitioning.expiration_ms instead.",
            PendingDeprecationWarning, stacklevel=2)
        if self.time_partitioning is None:
            self._properties['timePartitioning'] = {
                'type': TimePartitioningType.DAY}
        self._properties['timePartitioning']['expirationMs'] = str(value)

    @property
    def clustering_fields(self):
        """Union[List[str], None]: Fields defining clustering for the table

        (Defaults to :data:`None`).

        Clustering fields are immutable after table creation.

        .. note::

           As of 2018-06-29, clustering fields cannot be set on a table
           which does not also have time partioning defined.
        """
        prop = self._properties.get('clustering')
        if prop is not None:
            return list(prop.get('fields', ()))

    @clustering_fields.setter
    def clustering_fields(self, value):
        """Union[List[str], None]: Fields defining clustering for the table

        (Defaults to :data:`None`).
        """
        if value is not None:
            prop = self._properties.setdefault('clustering', {})
            prop['fields'] = value
        else:
            if 'clustering' in self._properties:
                del self._properties['clustering']

    @property
    def description(self):
        """Union[str, None]: Description of the table (defaults to
        :data:`None`).

        Raises:
            ValueError: For invalid value types.
        """
        return self._properties.get('description')

    @description.setter
    def description(self, value):
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['description'] = value

    @property
    def expires(self):
        """Union[datetime.datetime, None]: Datetime at which the table will be
        deleted.

        Raises:
            ValueError: For invalid value types.
        """
        expiration_time = self._properties.get('expirationTime')
        if expiration_time is not None:
            # expiration_time will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(expiration_time))

    @expires.setter
    def expires(self, value):
        if not isinstance(value, datetime.datetime) and value is not None:
            raise ValueError("Pass a datetime, or None")
        value_ms = google.cloud._helpers._millis_from_datetime(value)
        self._properties['expirationTime'] = _helpers._str_or_none(value_ms)

    @property
    def friendly_name(self):
        """Union[str, None]: Title of the table (defaults to :data:`None`).

        Raises:
            ValueError: For invalid value types.
        """
        return self._properties.get('friendlyName')

    @friendly_name.setter
    def friendly_name(self, value):
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['friendlyName'] = value

    @property
    def location(self):
        """Union[str, None]: Location in which the table is hosted

        Defaults to :data:`None`.
        """
        return self._properties.get('location')

    @property
    def view_query(self):
        """Union[str, None]: SQL query defining the table as a view (defaults
        to :data:`None`).

        By default, the query is treated as Standard SQL. To use Legacy
        SQL, set :attr:`view_use_legacy_sql` to :data:`True`.

        Raises:
            ValueError: For invalid value types.
        """
        view = self._properties.get('view')
        if view is not None:
            return view.get('query')

    @view_query.setter
    def view_query(self, value):
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
        if not isinstance(value, bool):
            raise ValueError("Pass a boolean")
        if self._properties.get('view') is None:
            self._properties['view'] = {}
        self._properties['view']['useLegacySql'] = value

    @property
    def streaming_buffer(self):
        """google.cloud.bigquery.StreamingBuffer: Information about a table's
        streaming buffer.
        """
        sb = self._properties.get('streamingBuffer')
        if sb is not None:
            return StreamingBuffer(sb)

    @property
    def external_data_configuration(self):
        """Union[google.cloud.bigquery.ExternalConfig, None]: Configuration for
        an external data source (defaults to :data:`None`).

        Raises:
            ValueError: For invalid value types.
        """
        prop = self._properties.get('externalDataConfiguration')
        if prop is not None:
            prop = ExternalConfig.from_api_repr(prop)
        return prop

    @external_data_configuration.setter
    def external_data_configuration(self, value):
        if not (value is None or isinstance(value, ExternalConfig)):
            raise ValueError("Pass an ExternalConfig or None")
        api_repr = value
        if value is not None:
            api_repr = value.to_api_repr()
        self._properties['externalDataConfiguration'] = api_repr

    @classmethod
    def from_string(cls, full_table_id):
        """Construct a table from fully-qualified table ID.

        Args:
            full_table_id (str):
                A fully-qualified table ID in standard SQL format. Must
                included a project ID, dataset ID, and table ID, each
                separated by ``.``.

        Returns:
            Table: Table parsed from ``full_table_id``.

        Examples:
            >>> Table.from_string('my-project.mydataset.mytable')
            Table(TableRef...(D...('my-project', 'mydataset'), 'mytable'))

        Raises:
            ValueError:
                If ``full_table_id`` is not a fully-qualified table ID in
                standard SQL format.
        """
        return cls(TableReference.from_string(full_table_id))

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a table given its API representation

        Args:
            resource (Dict[str, object]):
                Table resource representation from the API
            dataset (google.cloud.bigquery.dataset.Dataset):
                The dataset containing the table.

        Returns:
            google.cloud.bigquery.table.Table: Table parsed from ``resource``.

        Raises:
            KeyError:
                If the ``resource`` lacks the key ``'tableReference'``, or if
                the ``dict`` stored within the key ``'tableReference'`` lacks
                the keys ``'tableId'``, ``'projectId'``, or ``'datasetId'``.
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
        table._properties = resource

        return table

    def to_api_repr(self):
        """Constructs the API resource of this table

        Returns:
            Dict[str, object]: Table represented as an API resource
        """
        return copy.deepcopy(self._properties)

    def _build_resource(self, filter_fields):
        """Generate a resource for ``update``."""
        partial = {}
        for filter_field in filter_fields:
            api_field = self._PROPERTY_TO_API_FIELD.get(filter_field)
            if api_field is None and filter_field not in self._properties:
                raise ValueError('No Table property %s' % filter_field)
            elif api_field is not None:
                partial[api_field] = self._properties.get(api_field)
            else:
                # allows properties that are not defined in the library
                # and properties that have the same name as API resource key
                partial[filter_field] = self._properties[filter_field]

        return partial

    def __repr__(self):
        return 'Table({})'.format(repr(self.reference))


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
        resource (Dict[str, object]):
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
        """str: Project bound to the table."""
        return self._properties['tableReference']['projectId']

    @property
    def dataset_id(self):
        """str: ID of dataset containing the table."""
        return self._properties['tableReference']['datasetId']

    @property
    def table_id(self):
        """str: ID of the table."""
        return self._properties['tableReference']['tableId']

    reference = property(_reference_getter)

    @property
    def labels(self):
        """Dict[str, str]: Labels for the table.

        This method always returns a dict. To change a table's labels,
        modify the dict, then call ``Client.update_table``. To delete a
        label, set its value to :data:`None` before updating.
        """
        return self._properties.setdefault('labels', {})

    @property
    def full_table_id(self):
        """Union[str, None]: ID for the table (:data:`None` until set from the
        server).

        In the format ``project_id:dataset_id.table_id``.
        """
        return self._properties.get('id')

    @property
    def table_type(self):
        """Union[str, None]: The type of the table (:data:`None` until set from
        the server).

        Possible values are ``'TABLE'``, ``'VIEW'``, or ``'EXTERNAL'``.
        """
        return self._properties.get('type')

    @property
    def time_partitioning(self):
        """google.cloud.bigquery.table.TimePartitioning: Configures time-based
        partitioning for a table.
        """
        prop = self._properties.get('timePartitioning')
        if prop is not None:
            return TimePartitioning.from_api_repr(prop)

    @property
    def partitioning_type(self):
        """Union[str, None]: Time partitioning of the table if it is
        partitioned (Defaults to :data:`None`).
        """
        warnings.warn(
            "This method will be deprecated in future versions. Please use "
            "TableListItem.time_partitioning.type_ instead.",
            PendingDeprecationWarning, stacklevel=2)
        if self.time_partitioning is not None:
            return self.time_partitioning.type_

    @property
    def partition_expiration(self):
        """Union[int, None]: Expiration time in milliseconds for a partition.

        If this property is set and :attr:`type_` is not set, :attr:`type_`
        will default to :attr:`TimePartitioningType.DAY`.
        """
        warnings.warn(
            "This method will be deprecated in future versions. Please use "
            "TableListItem.time_partitioning.expiration_ms instead.",
            PendingDeprecationWarning, stacklevel=2)
        if self.time_partitioning is not None:
            return self.time_partitioning.expiration_ms

    @property
    def friendly_name(self):
        """Union[str, None]: Title of the table (defaults to :data:`None`)."""
        return self._properties.get('friendlyName')

    view_use_legacy_sql = property(_view_use_legacy_sql_getter)


def _row_from_mapping(mapping, schema):
    """Convert a mapping to a row tuple using the schema.

    Args:
        mapping (Dict[str, object])
            Mapping of row data: must contain keys for all required fields in
            the schema. Keys which do not correspond to a field in the schema
            are ignored.
        schema (List[google.cloud.bigquery.schema.SchemaField]):
            The schema of the table destination for the rows

    Returns:
        Tuple[object]:
            Tuple whose elements are ordered according to the schema.

    Raises:
        ValueError: If schema is empty.
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

    Args:
        resource (Dict[str, object]):
            streaming buffer representation returned from the API
    """

    def __init__(self, resource):
        self.estimated_bytes = int(resource['estimatedBytes'])
        self.estimated_rows = int(resource['estimatedRows'])
        # time is in milliseconds since the epoch.
        self.oldest_entry_time = (
            google.cloud._helpers._datetime_from_microseconds(
                1000.0 * int(resource['oldestEntryTime'])))


class Row(object):
    """A BigQuery row.

    Values can be accessed by position (index), by key like a dict,
    or as properties.

    Args:
        values (Sequence[object]): The row values
        field_to_index (Dict[str, int]):
            A mapping from schema field names to indexes
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
            Iterable[str]: The keys corresponding to the columns of a row

        Examples:

            >>> list(Row(('a', 'b'), {'x': 0, 'y': 1}).keys())
            ['x', 'y']
        """
        return six.iterkeys(self._xxx_field_to_index)

    def items(self):
        """Return items as ``(key, value)`` pairs.

        Returns:
            Iterable[Tuple[str, object]]:
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

            The default value is :data:`None` when the key does not exist.

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
        max_results (int, optional): The maximum number of results to fetch.
        page_size (int, optional): The number of items to return per page.
        extra_params (Dict[str, object]):
            Extra query string parameters for the API call.
    """

    def __init__(self, client, api_request, path, schema, page_token=None,
                 max_results=None, page_size=None, extra_params=None):
        super(RowIterator, self).__init__(
            client, api_request, path, item_to_value=_item_to_row,
            items_key='rows', page_token=page_token, max_results=max_results,
            extra_params=extra_params, page_start=_rows_page_start,
            next_token='pageToken')
        self._schema = schema
        self._field_to_index = _helpers._field_to_index_mapping(schema)
        self._total_rows = None
        self._page_size = page_size

    def _get_next_page_response(self):
        """Requests the next page from the path provided.

        Returns:
            Dict[str, object]:
                The parsed JSON response of the next page's contents.
        """
        params = self._get_query_params()
        if self._page_size is not None:
            params['maxResults'] = self._page_size
        return self.api_request(
            method=self._HTTP_METHOD,
            path=self.path,
            query_params=params)

    @property
    def schema(self):
        """List[google.cloud.bigquery.schema.SchemaField]: Table's schema."""
        return list(self._schema)

    @property
    def total_rows(self):
        """int: The total number of rows in the table."""
        return self._total_rows

    def to_dataframe(self):
        """Create a pandas DataFrame from the query results.

        Returns:
            pandas.DataFrame:
                A :class:`~pandas.DataFrame` populated with row data and column
                headers from the query results. The column headers are derived
                from the destination table's schema.

        Raises:
            ValueError: If the :mod:`pandas` library cannot be imported.

        """
        if pandas is None:
            raise ValueError(_NO_PANDAS_ERROR)

        column_headers = [field.name for field in self.schema]
        # Use generator, rather than pulling the whole rowset into memory.
        rows = (row.values() for row in iter(self))

        return pandas.DataFrame(rows, columns=column_headers)


class _EmptyRowIterator(object):
    """An empty row iterator.

    This class prevents API requests when there are no rows to fetch or rows
    are impossible to fetch, such as with query results for DDL CREATE VIEW
    statements.
    """
    schema = ()
    pages = ()
    total_rows = 0

    def to_dataframe(self):
        if pandas is None:
            raise ValueError(_NO_PANDAS_ERROR)
        return pandas.DataFrame()

    def __iter__(self):
        return iter(())


class TimePartitioningType(object):
    """Specifies the type of time partitioning to perform."""

    DAY = 'DAY'
    """str: Generates one partition per day."""


class TimePartitioning(object):
    """Configures time-based partitioning for a table.

    Args:
        type_ (google.cloud.bigquery.table.TimePartitioningType, optional):
            Specifies the type of time partitioning to perform. Defaults to
            :attr:`~google.cloud.bigquery.table.TimePartitioningType.DAY`,
            which is the only currently supported type.
        field (str, optional):
            If set, the table is partitioned by this field. If not set, the
            table is partitioned by pseudo column ``_PARTITIONTIME``. The field
            must be a top-level ``TIMESTAMP`` or ``DATE`` field. Its mode must
            be ``NULLABLE`` or ``REQUIRED``.
        expiration_ms(int, optional):
            Number of milliseconds for which to keep the storage for a
            partition.
        require_partition_filter (bool, optional):
            If set to true, queries over the partitioned table require a
            partition filter that can be used for partition elimination to be
            specified.
    """
    def __init__(self, type_=None, field=None, expiration_ms=None,
                 require_partition_filter=None):
        self._properties = {}
        if type_ is None:
            self.type_ = TimePartitioningType.DAY
        else:
            self.type_ = type_
        if field is not None:
            self.field = field
        if expiration_ms is not None:
            self.expiration_ms = expiration_ms
        if require_partition_filter is not None:
            self.require_partition_filter = require_partition_filter

    @property
    def type_(self):
        """google.cloud.bigquery.table.TimePartitioningType: The type of time
        partitioning to use.
        """
        return self._properties['type']

    @type_.setter
    def type_(self, value):
        self._properties['type'] = value

    @property
    def field(self):
        """str: Field in the table to use for partitioning"""
        return self._properties.get('field')

    @field.setter
    def field(self, value):
        self._properties['field'] = value

    @property
    def expiration_ms(self):
        """int: Number of milliseconds to keep the storage for a partition."""
        return _helpers._int_or_none(self._properties.get('expirationMs'))

    @expiration_ms.setter
    def expiration_ms(self, value):
        self._properties['expirationMs'] = str(value)

    @property
    def require_partition_filter(self):
        """bool: Specifies whether partition filters are required for queries
        """
        return self._properties.get('requirePartitionFilter')

    @require_partition_filter.setter
    def require_partition_filter(self, value):
        self._properties['requirePartitionFilter'] = value

    @classmethod
    def from_api_repr(cls, api_repr):
        """Return a :class:`TimePartitioning` object deserialized from a dict.

        This method creates a new ``TimePartitioning`` instance that points to
        the ``api_repr`` parameter as its internal properties dict. This means
        that when a ``TimePartitioning`` instance is stored as a property of
        another object, any changes made at the higher level will also appear
        here::

            >>> time_partitioning = TimePartitioning()
            >>> table.time_partitioning = time_partitioning
            >>> table.time_partitioning.field = 'timecolumn'
            >>> time_partitioning.field
            'timecolumn'

        Args:
            api_repr (Mapping[str, str]):
                The serialized representation of the TimePartitioning, such as
                what is output by :meth:`to_api_repr`.

        Returns:
            google.cloud.bigquery.table.TimePartitioning:
                The ``TimePartitioning`` object.
        """
        instance = cls(api_repr['type'])
        instance._properties = api_repr
        return instance

    def to_api_repr(self):
        """Return a dictionary representing this object.

        This method returns the properties dict of the ``TimePartitioning``
        instance rather than making a copy. This means that when a
        ``TimePartitioning`` instance is stored as a property of another
        object, any changes made at the higher level will also appear here.

        Returns:
            dict:
                A dictionary representing the TimePartitioning object in
                serialized form.
        """
        return self._properties

    def _key(self):
        return tuple(sorted(self._properties.items()))

    def __eq__(self, other):
        if not isinstance(other, TimePartitioning):
            return NotImplemented
        return self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        key_vals = ['{}={}'.format(key, val) for key, val in self._key()]
        return 'TimePartitioning({})'.format(','.join(key_vals))


def _item_to_row(iterator, resource):
    """Convert a JSON row to the native object.

    .. note::

        This assumes that the ``schema`` attribute has been
        added to the iterator after being created, which
        should be done by the caller.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: An item to be converted to a row.

    :rtype: :class:`~google.cloud.bigquery.table.Row`
    :returns: The next row in the page.
    """
    return Row(_helpers._row_tuple_from_json(resource, iterator.schema),
               iterator._field_to_index)


# pylint: disable=unused-argument
def _rows_page_start(iterator, page, response):
    """Grab total rows when :class:`~google.cloud.iterator.Page` starts.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type page: :class:`~google.api_core.page_iterator.Page`
    :param page: The page that was just created.

    :type response: dict
    :param response: The JSON API response for a page of rows in a table.
    """
    total_rows = response.get('totalRows')
    if total_rows is not None:
        total_rows = int(total_rows)
    iterator._total_rows = total_rows
# pylint: enable=unused-argument
