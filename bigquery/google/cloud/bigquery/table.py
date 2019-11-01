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
import functools
import logging
import operator
import warnings

import six

try:
    from google.cloud import bigquery_storage_v1beta1
except ImportError:  # pragma: NO COVER
    bigquery_storage_v1beta1 = None

try:
    import pandas
except ImportError:  # pragma: NO COVER
    pandas = None

try:
    import pyarrow
except ImportError:  # pragma: NO COVER
    pyarrow = None

try:
    import tqdm
except ImportError:  # pragma: NO COVER
    tqdm = None

import google.api_core.exceptions
from google.api_core.page_iterator import HTTPIterator

import google.cloud._helpers
from google.cloud.bigquery import _helpers
from google.cloud.bigquery import _pandas_helpers
from google.cloud.bigquery.schema import _build_schema_resource
from google.cloud.bigquery.schema import _parse_schema_resource
from google.cloud.bigquery.schema import _to_schema_fields
from google.cloud.bigquery.external_config import ExternalConfig
from google.cloud.bigquery.encryption_configuration import EncryptionConfiguration


_LOGGER = logging.getLogger(__name__)

_NO_BQSTORAGE_ERROR = (
    "The google-cloud-bigquery-storage library is not installed, "
    "please install google-cloud-bigquery-storage to use bqstorage features."
)
_NO_PANDAS_ERROR = (
    "The pandas library is not installed, please install "
    "pandas to use the to_dataframe() function."
)
_NO_PYARROW_ERROR = (
    "The pyarrow library is not installed, please install "
    "pandas to use the to_arrow() function."
)
_NO_TQDM_ERROR = (
    "A progress bar was requested, but there was an error loading the tqdm "
    "library. Please install tqdm to use the progress bar functionality."
)
_TABLE_HAS_NO_SCHEMA = 'Table has no schema:  call "client.get_table()"'


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
    view = table._properties.get("view")
    if view is not None:
        # The server-side default for useLegacySql is True.
        return view.get("useLegacySql", True)
    # In some cases, such as in a table list no view object is present, but the
    # resource still represents a view. Use the type as a fallback.
    if table.table_type == "VIEW":
        # The server-side default for useLegacySql is True.
        return True


class TableReference(object):
    """TableReferences are pointers to tables.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#tablereference

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
        return "/projects/%s/datasets/%s/tables/%s" % (
            self._project,
            self._dataset_id,
            self._table_id,
        )

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

        (
            output_project_id,
            output_dataset_id,
            output_table_id,
        ) = _helpers._parse_3_part_id(
            table_id, default_project=default_project, property_name="table_id"
        )

        return cls(
            DatasetReference(output_project_id, output_dataset_id), output_table_id
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

        project = resource["projectId"]
        dataset_id = resource["datasetId"]
        table_id = resource["tableId"]
        return cls(DatasetReference(project, dataset_id), table_id)

    def to_api_repr(self):
        """Construct the API resource representation of this table reference.

        Returns:
            Dict[str, object]: Table reference represented as an API resource
        """
        return {
            "projectId": self._project,
            "datasetId": self._dataset_id,
            "tableId": self._table_id,
        }

    def to_bqstorage(self):
        """Construct a BigQuery Storage API representation of this table.

        Install the ``google-cloud-bigquery-storage`` package to use this
        feature.

        If the ``table_id`` contains a partition identifier (e.g.
        ``my_table$201812``) or a snapshot identifier (e.g.
        ``mytable@1234567890``), it is ignored. Use
        :class:`google.cloud.bigquery_storage_v1beta1.types.TableReadOptions`
        to filter rows by partition. Use
        :class:`google.cloud.bigquery_storage_v1beta1.types.TableModifiers`
        to select a specific snapshot to read from.

        Returns:
            google.cloud.bigquery_storage_v1beta1.types.TableReference:
                A reference to this table in the BigQuery Storage API.

        Raises:
            ValueError:
                If the :mod:`google.cloud.bigquery_storage_v1beta1` module
                cannot be imported.
        """
        if bigquery_storage_v1beta1 is None:
            raise ValueError(_NO_BQSTORAGE_ERROR)

        table_ref = bigquery_storage_v1beta1.types.TableReference()
        table_ref.project_id = self._project
        table_ref.dataset_id = self._dataset_id
        table_id = self._table_id

        if "@" in table_id:
            table_id = table_id.split("@")[0]

        if "$" in table_id:
            table_id = table_id.split("$")[0]

        table_ref.table_id = table_id

        return table_ref

    def _key(self):
        """A tuple key that uniquely describes this field.

        Used to compute this instance's hashcode and evaluate equality.

        Returns:
            Tuple[str]: The contents of this :class:`DatasetReference`.
        """
        return (self._project, self._dataset_id, self._table_id)

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
        return "TableReference({}, '{}')".format(repr(dataset_ref), self._table_id)


class Table(object):
    """Tables represent a set of rows whose values correspond to a schema.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#resource-table

    Args:
        table_ref (Union[google.cloud.bigquery.table.TableReference, str]):
            A pointer to a table. If ``table_ref`` is a string, it must
            included a project ID, dataset ID, and table ID, each separated
            by ``.``.
        schema (Optional[Sequence[Union[ \
                :class:`~google.cloud.bigquery.schema.SchemaField`, \
                Mapping[str, Any] \
        ]]]):
            The table's schema. If any item is a mapping, its content must be
            compatible with
            :meth:`~google.cloud.bigquery.schema.SchemaField.from_api_repr`.
    """

    _PROPERTY_TO_API_FIELD = {
        "friendly_name": "friendlyName",
        "expires": "expirationTime",
        "time_partitioning": "timePartitioning",
        "partitioning_type": "timePartitioning",
        "partition_expiration": "timePartitioning",
        "view_use_legacy_sql": "view",
        "view_query": "view",
        "external_data_configuration": "externalDataConfiguration",
        "encryption_configuration": "encryptionConfiguration",
        "require_partition_filter": "requirePartitionFilter",
    }

    def __init__(self, table_ref, schema=None):
        table_ref = _table_arg_to_table_ref(table_ref)
        self._properties = {"tableReference": table_ref.to_api_repr(), "labels": {}}
        # Let the @property do validation.
        if schema is not None:
            self.schema = schema

    @property
    def project(self):
        """str: Project bound to the table."""
        return self._properties["tableReference"]["projectId"]

    @property
    def dataset_id(self):
        """str: ID of dataset containing the table."""
        return self._properties["tableReference"]["datasetId"]

    @property
    def table_id(self):
        """str: ID of the table."""
        return self._properties["tableReference"]["tableId"]

    reference = property(_reference_getter)

    @property
    def path(self):
        """str: URL path for the table's APIs."""
        return "/projects/%s/datasets/%s/tables/%s" % (
            self.project,
            self.dataset_id,
            self.table_id,
        )

    @property
    def require_partition_filter(self):
        """bool: If set to true, queries over the partitioned table require a
        partition filter that can be used for partition elimination to be
        specified.
        """
        return self._properties.get("requirePartitionFilter")

    @require_partition_filter.setter
    def require_partition_filter(self, value):
        self._properties["requirePartitionFilter"] = value

    @property
    def schema(self):
        """Sequence[Union[ \
                :class:`~google.cloud.bigquery.schema.SchemaField`, \
                Mapping[str, Any] \
        ]]:
            Table's schema.

        Raises:
            Exception:
                If ``schema`` is not a sequence, or if any item in the sequence
                is not a :class:`~google.cloud.bigquery.schema.SchemaField`
                instance or a compatible mapping representation of the field.
        """
        prop = self._properties.get("schema")
        if not prop:
            return []
        else:
            return _parse_schema_resource(prop)

    @schema.setter
    def schema(self, value):
        if value is None:
            self._properties["schema"] = None
        else:
            value = _to_schema_fields(value)
            self._properties["schema"] = {"fields": _build_schema_resource(value)}

    @property
    def labels(self):
        """Dict[str, str]: Labels for the table.

        This method always returns a dict. To change a table's labels,
        modify the dict, then call ``Client.update_table``. To delete a
        label, set its value to :data:`None` before updating.

        Raises:
            ValueError: If ``value`` type is invalid.
        """
        return self._properties.setdefault("labels", {})

    @labels.setter
    def labels(self, value):
        if not isinstance(value, dict):
            raise ValueError("Pass a dict")
        self._properties["labels"] = value

    @property
    def encryption_configuration(self):
        """google.cloud.bigquery.encryption_configuration.EncryptionConfiguration: Custom
        encryption configuration for the table.

        Custom encryption configuration (e.g., Cloud KMS keys) or :data:`None`
        if using default encryption.

        See `protecting data with Cloud KMS keys
        <https://cloud.google.com/bigquery/docs/customer-managed-encryption>`_
        in the BigQuery documentation.
        """
        prop = self._properties.get("encryptionConfiguration")
        if prop is not None:
            prop = EncryptionConfiguration.from_api_repr(prop)
        return prop

    @encryption_configuration.setter
    def encryption_configuration(self, value):
        api_repr = value
        if value is not None:
            api_repr = value.to_api_repr()
        self._properties["encryptionConfiguration"] = api_repr

    @property
    def created(self):
        """Union[datetime.datetime, None]: Datetime at which the table was
        created (:data:`None` until set from the server).
        """
        creation_time = self._properties.get("creationTime")
        if creation_time is not None:
            # creation_time will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(creation_time)
            )

    @property
    def etag(self):
        """Union[str, None]: ETag for the table resource (:data:`None` until
        set from the server).
        """
        return self._properties.get("etag")

    @property
    def modified(self):
        """Union[datetime.datetime, None]: Datetime at which the table was last
        modified (:data:`None` until set from the server).
        """
        modified_time = self._properties.get("lastModifiedTime")
        if modified_time is not None:
            # modified_time will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(modified_time)
            )

    @property
    def num_bytes(self):
        """Union[int, None]: The size of the table in bytes (:data:`None` until
        set from the server).
        """
        return _helpers._int_or_none(self._properties.get("numBytes"))

    @property
    def num_rows(self):
        """Union[int, None]: The number of rows in the table (:data:`None`
        until set from the server).
        """
        return _helpers._int_or_none(self._properties.get("numRows"))

    @property
    def self_link(self):
        """Union[str, None]: URL for the table resource (:data:`None` until set
        from the server).
        """
        return self._properties.get("selfLink")

    @property
    def full_table_id(self):
        """Union[str, None]: ID for the table (:data:`None` until set from the
        server).

        In the format ``project_id:dataset_id.table_id``.
        """
        return self._properties.get("id")

    @property
    def table_type(self):
        """Union[str, None]: The type of the table (:data:`None` until set from
        the server).

        Possible values are ``'TABLE'``, ``'VIEW'``, or ``'EXTERNAL'``.
        """
        return self._properties.get("type")

    @property
    def range_partitioning(self):
        """Optional[google.cloud.bigquery.table.RangePartitioning]:
        Configures range-based partitioning for a table.

        .. note::
            **Beta**. The integer range partitioning feature is in a
            pre-release state and might change or have limited support.

        Only specify at most one of
        :attr:`~google.cloud.bigquery.table.Table.time_partitioning` or
        :attr:`~google.cloud.bigquery.table.Table.range_partitioning`.

        Raises:
            ValueError:
                If the value is not
                :class:`~google.cloud.bigquery.table.RangePartitioning` or
                :data:`None`.
        """
        resource = self._properties.get("rangePartitioning")
        if resource is not None:
            return RangePartitioning(_properties=resource)

    @range_partitioning.setter
    def range_partitioning(self, value):
        resource = value
        if isinstance(value, RangePartitioning):
            resource = value._properties
        elif value is not None:
            raise ValueError(
                "Expected value to be RangePartitioning or None, got {}.".format(value)
            )
        self._properties["rangePartitioning"] = resource

    @property
    def time_partitioning(self):
        """Optional[google.cloud.bigquery.table.TimePartitioning]: Configures time-based
        partitioning for a table.

        Only specify at most one of
        :attr:`~google.cloud.bigquery.table.Table.time_partitioning` or
        :attr:`~google.cloud.bigquery.table.Table.range_partitioning`.

        Raises:
            ValueError:
                If the value is not
                :class:`~google.cloud.bigquery.table.TimePartitioning` or
                :data:`None`.
        """
        prop = self._properties.get("timePartitioning")
        if prop is not None:
            return TimePartitioning.from_api_repr(prop)

    @time_partitioning.setter
    def time_partitioning(self, value):
        api_repr = value
        if isinstance(value, TimePartitioning):
            api_repr = value.to_api_repr()
        elif value is not None:
            raise ValueError(
                "value must be google.cloud.bigquery.table.TimePartitioning " "or None"
            )
        self._properties["timePartitioning"] = api_repr

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
            PendingDeprecationWarning,
            stacklevel=2,
        )
        if self.time_partitioning is not None:
            return self.time_partitioning.type_

    @partitioning_type.setter
    def partitioning_type(self, value):
        warnings.warn(
            "This method will be deprecated in future versions. Please use "
            "Table.time_partitioning.type_ instead.",
            PendingDeprecationWarning,
            stacklevel=2,
        )
        if self.time_partitioning is None:
            self._properties["timePartitioning"] = {}
        self._properties["timePartitioning"]["type"] = value

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
            PendingDeprecationWarning,
            stacklevel=2,
        )
        if self.time_partitioning is not None:
            return self.time_partitioning.expiration_ms

    @partition_expiration.setter
    def partition_expiration(self, value):
        warnings.warn(
            "This method will be deprecated in future versions. Please use "
            "Table.time_partitioning.expiration_ms instead.",
            PendingDeprecationWarning,
            stacklevel=2,
        )
        if self.time_partitioning is None:
            self._properties["timePartitioning"] = {"type": TimePartitioningType.DAY}
        self._properties["timePartitioning"]["expirationMs"] = str(value)

    @property
    def clustering_fields(self):
        """Union[List[str], None]: Fields defining clustering for the table

        (Defaults to :data:`None`).

        Clustering fields are immutable after table creation.

        .. note::

           As of 2018-06-29, clustering fields cannot be set on a table
           which does not also have time partioning defined.
        """
        prop = self._properties.get("clustering")
        if prop is not None:
            return list(prop.get("fields", ()))

    @clustering_fields.setter
    def clustering_fields(self, value):
        """Union[List[str], None]: Fields defining clustering for the table

        (Defaults to :data:`None`).
        """
        if value is not None:
            prop = self._properties.setdefault("clustering", {})
            prop["fields"] = value
        else:
            if "clustering" in self._properties:
                del self._properties["clustering"]

    @property
    def description(self):
        """Union[str, None]: Description of the table (defaults to
        :data:`None`).

        Raises:
            ValueError: For invalid value types.
        """
        return self._properties.get("description")

    @description.setter
    def description(self, value):
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties["description"] = value

    @property
    def expires(self):
        """Union[datetime.datetime, None]: Datetime at which the table will be
        deleted.

        Raises:
            ValueError: For invalid value types.
        """
        expiration_time = self._properties.get("expirationTime")
        if expiration_time is not None:
            # expiration_time will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(expiration_time)
            )

    @expires.setter
    def expires(self, value):
        if not isinstance(value, datetime.datetime) and value is not None:
            raise ValueError("Pass a datetime, or None")
        value_ms = google.cloud._helpers._millis_from_datetime(value)
        self._properties["expirationTime"] = _helpers._str_or_none(value_ms)

    @property
    def friendly_name(self):
        """Union[str, None]: Title of the table (defaults to :data:`None`).

        Raises:
            ValueError: For invalid value types.
        """
        return self._properties.get("friendlyName")

    @friendly_name.setter
    def friendly_name(self, value):
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties["friendlyName"] = value

    @property
    def location(self):
        """Union[str, None]: Location in which the table is hosted

        Defaults to :data:`None`.
        """
        return self._properties.get("location")

    @property
    def view_query(self):
        """Union[str, None]: SQL query defining the table as a view (defaults
        to :data:`None`).

        By default, the query is treated as Standard SQL. To use Legacy
        SQL, set :attr:`view_use_legacy_sql` to :data:`True`.

        Raises:
            ValueError: For invalid value types.
        """
        view = self._properties.get("view")
        if view is not None:
            return view.get("query")

    @view_query.setter
    def view_query(self, value):
        if not isinstance(value, six.string_types):
            raise ValueError("Pass a string")
        view = self._properties.get("view")
        if view is None:
            view = self._properties["view"] = {}
        view["query"] = value
        # The service defaults useLegacySql to True, but this
        # client uses Standard SQL by default.
        if view.get("useLegacySql") is None:
            view["useLegacySql"] = False

    @view_query.deleter
    def view_query(self):
        """Delete SQL query defining the table as a view."""
        self._properties.pop("view", None)

    view_use_legacy_sql = property(_view_use_legacy_sql_getter)

    @view_use_legacy_sql.setter
    def view_use_legacy_sql(self, value):
        if not isinstance(value, bool):
            raise ValueError("Pass a boolean")
        if self._properties.get("view") is None:
            self._properties["view"] = {}
        self._properties["view"]["useLegacySql"] = value

    @property
    def streaming_buffer(self):
        """google.cloud.bigquery.StreamingBuffer: Information about a table's
        streaming buffer.
        """
        sb = self._properties.get("streamingBuffer")
        if sb is not None:
            return StreamingBuffer(sb)

    @property
    def external_data_configuration(self):
        """Union[google.cloud.bigquery.ExternalConfig, None]: Configuration for
        an external data source (defaults to :data:`None`).

        Raises:
            ValueError: For invalid value types.
        """
        prop = self._properties.get("externalDataConfiguration")
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
        self._properties["externalDataConfiguration"] = api_repr

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

        Returns:
            google.cloud.bigquery.table.Table: Table parsed from ``resource``.

        Raises:
            KeyError:
                If the ``resource`` lacks the key ``'tableReference'``, or if
                the ``dict`` stored within the key ``'tableReference'`` lacks
                the keys ``'tableId'``, ``'projectId'``, or ``'datasetId'``.
        """
        from google.cloud.bigquery import dataset

        if (
            "tableReference" not in resource
            or "tableId" not in resource["tableReference"]
        ):
            raise KeyError(
                "Resource lacks required identity information:"
                '["tableReference"]["tableId"]'
            )
        project_id = resource["tableReference"]["projectId"]
        table_id = resource["tableReference"]["tableId"]
        dataset_id = resource["tableReference"]["datasetId"]
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

    def to_bqstorage(self):
        """Construct a BigQuery Storage API representation of this table.

        Returns:
            google.cloud.bigquery_storage_v1beta1.types.TableReference:
                A reference to this table in the BigQuery Storage API.
        """
        return self.reference.to_bqstorage()

    def _build_resource(self, filter_fields):
        """Generate a resource for ``update``."""
        return _helpers._build_resource_from_properties(self, filter_fields)

    def __repr__(self):
        return "Table({})".format(repr(self.reference))


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
        if "tableReference" not in resource:
            raise ValueError("resource must contain a tableReference value")
        if "projectId" not in resource["tableReference"]:
            raise ValueError(
                "resource['tableReference'] must contain a projectId value"
            )
        if "datasetId" not in resource["tableReference"]:
            raise ValueError(
                "resource['tableReference'] must contain a datasetId value"
            )
        if "tableId" not in resource["tableReference"]:
            raise ValueError("resource['tableReference'] must contain a tableId value")

        self._properties = resource

    @property
    def created(self):
        """Union[datetime.datetime, None]: Datetime at which the table was
        created (:data:`None` until set from the server).
        """
        creation_time = self._properties.get("creationTime")
        if creation_time is not None:
            # creation_time will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(creation_time)
            )

    @property
    def expires(self):
        """Union[datetime.datetime, None]: Datetime at which the table will be
        deleted.
        """
        expiration_time = self._properties.get("expirationTime")
        if expiration_time is not None:
            # expiration_time will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(expiration_time)
            )

    @property
    def project(self):
        """str: Project bound to the table."""
        return self._properties["tableReference"]["projectId"]

    @property
    def dataset_id(self):
        """str: ID of dataset containing the table."""
        return self._properties["tableReference"]["datasetId"]

    @property
    def table_id(self):
        """str: ID of the table."""
        return self._properties["tableReference"]["tableId"]

    reference = property(_reference_getter)

    @property
    def labels(self):
        """Dict[str, str]: Labels for the table.

        This method always returns a dict. To change a table's labels,
        modify the dict, then call ``Client.update_table``. To delete a
        label, set its value to :data:`None` before updating.
        """
        return self._properties.setdefault("labels", {})

    @property
    def full_table_id(self):
        """Union[str, None]: ID for the table (:data:`None` until set from the
        server).

        In the format ``project_id:dataset_id.table_id``.
        """
        return self._properties.get("id")

    @property
    def table_type(self):
        """Union[str, None]: The type of the table (:data:`None` until set from
        the server).

        Possible values are ``'TABLE'``, ``'VIEW'``, or ``'EXTERNAL'``.
        """
        return self._properties.get("type")

    @property
    def time_partitioning(self):
        """google.cloud.bigquery.table.TimePartitioning: Configures time-based
        partitioning for a table.
        """
        prop = self._properties.get("timePartitioning")
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
            PendingDeprecationWarning,
            stacklevel=2,
        )
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
            PendingDeprecationWarning,
            stacklevel=2,
        )
        if self.time_partitioning is not None:
            return self.time_partitioning.expiration_ms

    @property
    def friendly_name(self):
        """Union[str, None]: Title of the table (defaults to :data:`None`)."""
        return self._properties.get("friendlyName")

    view_use_legacy_sql = property(_view_use_legacy_sql_getter)

    @property
    def clustering_fields(self):
        """Union[List[str], None]: Fields defining clustering for the table

        (Defaults to :data:`None`).

        Clustering fields are immutable after table creation.

        .. note::

           As of 2018-06-29, clustering fields cannot be set on a table
           which does not also have time partioning defined.
        """
        prop = self._properties.get("clustering")
        if prop is not None:
            return list(prop.get("fields", ()))

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
        return cls(
            {"tableReference": TableReference.from_string(full_table_id).to_api_repr()}
        )

    def to_bqstorage(self):
        """Construct a BigQuery Storage API representation of this table.

        Returns:
            google.cloud.bigquery_storage_v1beta1.types.TableReference:
                A reference to this table in the BigQuery Storage API.
        """
        return self.reference.to_bqstorage()


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
        if field.mode == "REQUIRED":
            row.append(mapping[field.name])
        elif field.mode == "REPEATED":
            row.append(mapping.get(field.name, ()))
        elif field.mode == "NULLABLE":
            row.append(mapping.get(field.name))
        else:
            raise ValueError("Unknown field mode: {}".format(field.mode))
    return tuple(row)


class StreamingBuffer(object):
    """Information about a table's streaming buffer.

    See https://cloud.google.com/bigquery/streaming-data-into-bigquery.

    Args:
        resource (Dict[str, object]):
            streaming buffer representation returned from the API
    """

    def __init__(self, resource):
        self.estimated_bytes = int(resource["estimatedBytes"])
        self.estimated_rows = int(resource["estimatedRows"])
        # time is in milliseconds since the epoch.
        self.oldest_entry_time = google.cloud._helpers._datetime_from_microseconds(
            1000.0 * int(resource["oldestEntryTime"])
        )


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
    __slots__ = ("_xxx_values", "_xxx_field_to_index")

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
            raise AttributeError("no row field {!r}".format(name))
        return self._xxx_values[value]

    def __len__(self):
        return len(self._xxx_values)

    def __getitem__(self, key):
        if isinstance(key, six.string_types):
            value = self._xxx_field_to_index.get(key)
            if value is None:
                raise KeyError("no row field {!r}".format(key))
            key = value
        return self._xxx_values[key]

    def __eq__(self, other):
        if not isinstance(other, Row):
            return NotImplemented
        return (
            self._xxx_values == other._xxx_values
            and self._xxx_field_to_index == other._xxx_field_to_index
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        # sort field dict by value, for determinism
        items = sorted(self._xxx_field_to_index.items(), key=operator.itemgetter(1))
        f2i = "{" + ", ".join("%r: %d" % item for item in items) + "}"
        return "Row({}, {})".format(self._xxx_values, f2i)


class _NoopProgressBarQueue(object):
    """A fake Queue class that does nothing.

    This is used when there is no progress bar to send updates to.
    """

    def put_nowait(self, item):
        """Don't actually do anything with the item."""


class RowIterator(HTTPIterator):
    """A class for iterating through HTTP/JSON API row list responses.

    Args:
        client (google.cloud.bigquery.Client): The API client.
        api_request (Callable[google.cloud._http.JSONConnection.api_request]):
            The function to use to make API requests.
        path (str): The method path to query for the list of items.
        schema (Sequence[Union[ \
                :class:`~google.cloud.bigquery.schema.SchemaField`, \
                Mapping[str, Any] \
        ]]):
            The table's schema. If any item is a mapping, its content must be
            compatible with
            :meth:`~google.cloud.bigquery.schema.SchemaField.from_api_repr`.
        page_token (str): A token identifying a page in a result set to start
            fetching results from.
        max_results (int, optional): The maximum number of results to fetch.
        page_size (int, optional): The maximum number of rows in each page
            of results from this request. Non-positive values are ignored.
            Defaults to a sensible value set by the API.
        extra_params (Dict[str, object]):
            Extra query string parameters for the API call.
        table (Union[ \
            google.cloud.bigquery.table.Table, \
            google.cloud.bigquery.table.TableReference, \
        ]):
            Optional. The table which these rows belong to, or a reference to
            it. Used to call the BigQuery Storage API to fetch rows.
        selected_fields (Sequence[google.cloud.bigquery.schema.SchemaField]):
            Optional. A subset of columns to select from this table.

    """

    def __init__(
        self,
        client,
        api_request,
        path,
        schema,
        page_token=None,
        max_results=None,
        page_size=None,
        extra_params=None,
        table=None,
        selected_fields=None,
    ):
        super(RowIterator, self).__init__(
            client,
            api_request,
            path,
            item_to_value=_item_to_row,
            items_key="rows",
            page_token=page_token,
            max_results=max_results,
            extra_params=extra_params,
            page_start=_rows_page_start,
            next_token="pageToken",
        )
        schema = _to_schema_fields(schema)
        self._field_to_index = _helpers._field_to_index_mapping(schema)
        self._page_size = page_size
        self._preserve_order = False
        self._project = client.project
        self._schema = schema
        self._selected_fields = selected_fields
        self._table = table
        self._total_rows = getattr(table, "num_rows", None)

    def _get_next_page_response(self):
        """Requests the next page from the path provided.

        Returns:
            Dict[str, object]:
                The parsed JSON response of the next page's contents.
        """
        params = self._get_query_params()
        if self._page_size is not None:
            params["maxResults"] = self._page_size
        return self.api_request(
            method=self._HTTP_METHOD, path=self.path, query_params=params
        )

    @property
    def schema(self):
        """List[google.cloud.bigquery.schema.SchemaField]: The subset of
        columns to be read from the table."""
        return list(self._schema)

    @property
    def total_rows(self):
        """int: The total number of rows in the table."""
        return self._total_rows

    def _get_progress_bar(self, progress_bar_type):
        """Construct a tqdm progress bar object, if tqdm is installed."""
        if tqdm is None:
            if progress_bar_type is not None:
                warnings.warn(_NO_TQDM_ERROR, UserWarning, stacklevel=3)
            return None

        description = "Downloading"
        unit = "rows"

        try:
            if progress_bar_type == "tqdm":
                return tqdm.tqdm(desc=description, total=self.total_rows, unit=unit)
            elif progress_bar_type == "tqdm_notebook":
                return tqdm.tqdm_notebook(
                    desc=description, total=self.total_rows, unit=unit
                )
            elif progress_bar_type == "tqdm_gui":
                return tqdm.tqdm_gui(desc=description, total=self.total_rows, unit=unit)
        except (KeyError, TypeError):
            # Protect ourselves from any tqdm errors. In case of
            # unexpected tqdm behavior, just fall back to showing
            # no progress bar.
            warnings.warn(_NO_TQDM_ERROR, UserWarning, stacklevel=3)
        return None

    def _to_page_iterable(
        self, bqstorage_download, tabledata_list_download, bqstorage_client=None
    ):
        if bqstorage_client is not None:
            try:
                # Iterate over the stream so that read errors are raised (and
                # the method can then fallback to tabledata.list).
                for item in bqstorage_download():
                    yield item
                return
            except google.api_core.exceptions.Forbidden:
                # Don't hide errors such as insufficient permissions to create
                # a read session, or the API is not enabled. Both of those are
                # clearly problems if the developer has explicitly asked for
                # BigQuery Storage API support.
                raise
            except google.api_core.exceptions.GoogleAPICallError:
                # There is a known issue with reading from small anonymous
                # query results tables, so some errors are expected. Rather
                # than throw those errors, try reading the DataFrame again, but
                # with the tabledata.list API.
                pass

        _LOGGER.debug(
            "Started reading table '{}.{}.{}' with tabledata.list.".format(
                self._table.project, self._table.dataset_id, self._table.table_id
            )
        )
        for item in tabledata_list_download():
            yield item

    def _to_arrow_iterable(self, bqstorage_client=None):
        """Create an iterable of arrow RecordBatches, to process the table as a stream."""
        bqstorage_download = functools.partial(
            _pandas_helpers.download_arrow_bqstorage,
            self._project,
            self._table,
            bqstorage_client,
            preserve_order=self._preserve_order,
            selected_fields=self._selected_fields,
        )
        tabledata_list_download = functools.partial(
            _pandas_helpers.download_arrow_tabledata_list, iter(self.pages), self.schema
        )
        return self._to_page_iterable(
            bqstorage_download,
            tabledata_list_download,
            bqstorage_client=bqstorage_client,
        )

    # If changing the signature of this method, make sure to apply the same
    # changes to job.QueryJob.to_arrow()
    def to_arrow(self, progress_bar_type=None, bqstorage_client=None):
        """[Beta] Create a class:`pyarrow.Table` by loading all pages of a
        table or query.

        Args:
            progress_bar_type (Optional[str]):
                If set, use the `tqdm <https://tqdm.github.io/>`_ library to
                display a progress bar while the data downloads. Install the
                ``tqdm`` package to use this feature.

                Possible values of ``progress_bar_type`` include:

                ``None``
                  No progress bar.
                ``'tqdm'``
                  Use the :func:`tqdm.tqdm` function to print a progress bar
                  to :data:`sys.stderr`.
                ``'tqdm_notebook'``
                  Use the :func:`tqdm.tqdm_notebook` function to display a
                  progress bar as a Jupyter notebook widget.
                ``'tqdm_gui'``
                  Use the :func:`tqdm.tqdm_gui` function to display a
                  progress bar as a graphical dialog box.
            bqstorage_client (google.cloud.bigquery_storage_v1beta1.BigQueryStorageClient):
                **Beta Feature** Optional. A BigQuery Storage API client. If
                supplied, use the faster BigQuery Storage API to fetch rows
                from BigQuery. This API is a billable API.

                This method requires the ``pyarrow`` and
                ``google-cloud-bigquery-storage`` libraries.

                Reading from a specific partition or snapshot is not
                currently supported by this method.

        Returns:
            pyarrow.Table
                A :class:`pyarrow.Table` populated with row data and column
                headers from the query results. The column headers are derived
                from the destination table's schema.

        Raises:
            ValueError: If the :mod:`pyarrow` library cannot be imported.

        ..versionadded:: 1.17.0
        """
        if pyarrow is None:
            raise ValueError(_NO_PYARROW_ERROR)

        progress_bar = self._get_progress_bar(progress_bar_type)

        record_batches = []
        for record_batch in self._to_arrow_iterable(bqstorage_client=bqstorage_client):
            record_batches.append(record_batch)

            if progress_bar is not None:
                # In some cases, the number of total rows is not populated
                # until the first page of rows is fetched. Update the
                # progress bar's total to keep an accurate count.
                progress_bar.total = progress_bar.total or self.total_rows
                progress_bar.update(record_batch.num_rows)

        if progress_bar is not None:
            # Indicate that the download has finished.
            progress_bar.close()

        if record_batches:
            return pyarrow.Table.from_batches(record_batches)
        else:
            # No records, use schema based on BigQuery schema.
            arrow_schema = _pandas_helpers.bq_to_arrow_schema(self._schema)
            return pyarrow.Table.from_batches(record_batches, schema=arrow_schema)

    def _to_dataframe_iterable(self, bqstorage_client=None, dtypes=None):
        """Create an iterable of pandas DataFrames, to process the table as a stream.

        See ``to_dataframe`` for argument descriptions.
        """
        column_names = [field.name for field in self._schema]
        bqstorage_download = functools.partial(
            _pandas_helpers.download_dataframe_bqstorage,
            self._project,
            self._table,
            bqstorage_client,
            column_names,
            dtypes,
            preserve_order=self._preserve_order,
            selected_fields=self._selected_fields,
        )
        tabledata_list_download = functools.partial(
            _pandas_helpers.download_dataframe_tabledata_list,
            iter(self.pages),
            self.schema,
            dtypes,
        )
        return self._to_page_iterable(
            bqstorage_download,
            tabledata_list_download,
            bqstorage_client=bqstorage_client,
        )

    # If changing the signature of this method, make sure to apply the same
    # changes to job.QueryJob.to_dataframe()
    def to_dataframe(self, bqstorage_client=None, dtypes=None, progress_bar_type=None):
        """Create a pandas DataFrame by loading all pages of a query.

        Args:
            bqstorage_client (google.cloud.bigquery_storage_v1beta1.BigQueryStorageClient):
                **Beta Feature** Optional. A BigQuery Storage API client. If
                supplied, use the faster BigQuery Storage API to fetch rows
                from BigQuery. This API is a billable API.

                This method requires the ``pyarrow`` and
                ``google-cloud-bigquery-storage`` libraries.

                Reading from a specific partition or snapshot is not
                currently supported by this method.

                **Caution**: There is a known issue reading small anonymous
                query result tables with the BQ Storage API. When a problem
                is encountered reading a table, the tabledata.list method
                from the BigQuery API is used, instead.
            dtypes (Map[str, Union[str, pandas.Series.dtype]]):
                Optional. A dictionary of column names pandas ``dtype``s. The
                provided ``dtype`` is used when constructing the series for
                the column specified. Otherwise, the default pandas behavior
                is used.
            progress_bar_type (Optional[str]):
                If set, use the `tqdm <https://tqdm.github.io/>`_ library to
                display a progress bar while the data downloads. Install the
                ``tqdm`` package to use this feature.

                Possible values of ``progress_bar_type`` include:

                ``None``
                  No progress bar.
                ``'tqdm'``
                  Use the :func:`tqdm.tqdm` function to print a progress bar
                  to :data:`sys.stderr`.
                ``'tqdm_notebook'``
                  Use the :func:`tqdm.tqdm_notebook` function to display a
                  progress bar as a Jupyter notebook widget.
                ``'tqdm_gui'``
                  Use the :func:`tqdm.tqdm_gui` function to display a
                  progress bar as a graphical dialog box.

                ..versionadded:: 1.11.0

        Returns:
            pandas.DataFrame:
                A :class:`~pandas.DataFrame` populated with row data and column
                headers from the query results. The column headers are derived
                from the destination table's schema.

        Raises:
            ValueError:
                If the :mod:`pandas` library cannot be imported, or the
                :mod:`google.cloud.bigquery_storage_v1beta1` module is
                required but cannot be imported.

        """
        if pandas is None:
            raise ValueError(_NO_PANDAS_ERROR)
        if dtypes is None:
            dtypes = {}

        if bqstorage_client and self.max_results is not None:
            warnings.warn(
                "Cannot use bqstorage_client if max_results is set, "
                "reverting to fetching data with the tabledata.list endpoint.",
                stacklevel=2,
            )
            bqstorage_client = None

        progress_bar = self._get_progress_bar(progress_bar_type)

        frames = []
        for frame in self._to_dataframe_iterable(
            bqstorage_client=bqstorage_client, dtypes=dtypes
        ):
            frames.append(frame)

            if progress_bar is not None:
                # In some cases, the number of total rows is not populated
                # until the first page of rows is fetched. Update the
                # progress bar's total to keep an accurate count.
                progress_bar.total = progress_bar.total or self.total_rows
                progress_bar.update(len(frame))

        if progress_bar is not None:
            # Indicate that the download has finished.
            progress_bar.close()

        # Avoid concatting an empty list.
        if not frames:
            column_names = [field.name for field in self._schema]
            return pandas.DataFrame(columns=column_names)
        return pandas.concat(frames, ignore_index=True)


class _EmptyRowIterator(object):
    """An empty row iterator.

    This class prevents API requests when there are no rows to fetch or rows
    are impossible to fetch, such as with query results for DDL CREATE VIEW
    statements.
    """

    schema = ()
    pages = ()
    total_rows = 0

    def to_arrow(self, progress_bar_type=None):
        """[Beta] Create an empty class:`pyarrow.Table`.

        Args:
            progress_bar_type (Optional[str]): Ignored. Added for compatibility with RowIterator.

        Returns:
            pyarrow.Table: An empty :class:`pyarrow.Table`.
        """
        if pyarrow is None:
            raise ValueError(_NO_PYARROW_ERROR)
        return pyarrow.Table.from_arrays(())

    def to_dataframe(self, bqstorage_client=None, dtypes=None, progress_bar_type=None):
        """Create an empty dataframe.

        Args:
            bqstorage_client (Any): Ignored. Added for compatibility with RowIterator.
            dtypes (Any): Ignored. Added for compatibility with RowIterator.
            progress_bar_type (Any): Ignored. Added for compatibility with RowIterator.

        Returns:
            pandas.DataFrame: An empty :class:`~pandas.DataFrame`.
        """
        if pandas is None:
            raise ValueError(_NO_PANDAS_ERROR)
        return pandas.DataFrame()

    def __iter__(self):
        return iter(())


class PartitionRange(object):
    """Definition of the ranges for range partitioning.

    .. note::
        **Beta**. The integer range partitioning feature is in a pre-release
        state and might change or have limited support.

    Args:
        start (Optional[int]):
            Sets the
            :attr:`~google.cloud.bigquery.table.PartitionRange.start`
            property.
        end (Optional[int]):
            Sets the
            :attr:`~google.cloud.bigquery.table.PartitionRange.end`
            property.
        interval (Optional[int]):
            Sets the
            :attr:`~google.cloud.bigquery.table.PartitionRange.interval`
            property.
        _properties (Optional[dict]):
            Private. Used to construct object from API resource.
    """

    def __init__(self, start=None, end=None, interval=None, _properties=None):
        if _properties is None:
            _properties = {}
        self._properties = _properties

        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        if interval is not None:
            self.interval = interval

    @property
    def start(self):
        """int: The start of range partitioning, inclusive."""
        return _helpers._int_or_none(self._properties.get("start"))

    @start.setter
    def start(self, value):
        self._properties["start"] = _helpers._str_or_none(value)

    @property
    def end(self):
        """int: The end of range partitioning, exclusive."""
        return _helpers._int_or_none(self._properties.get("end"))

    @end.setter
    def end(self, value):
        self._properties["end"] = _helpers._str_or_none(value)

    @property
    def interval(self):
        """int: The width of each interval."""
        return _helpers._int_or_none(self._properties.get("interval"))

    @interval.setter
    def interval(self, value):
        self._properties["interval"] = _helpers._str_or_none(value)

    def _key(self):
        return tuple(sorted(self._properties.items()))

    def __repr__(self):
        key_vals = ["{}={}".format(key, val) for key, val in self._key()]
        return "PartitionRange({})".format(", ".join(key_vals))


class RangePartitioning(object):
    """Range-based partitioning configuration for a table.

    .. note::
        **Beta**. The integer range partitioning feature is in a pre-release
        state and might change or have limited support.

    Args:
        range_ (Optional[google.cloud.bigquery.table.PartitionRange]):
            Sets the
            :attr:`google.cloud.bigquery.table.RangePartitioning.range_`
            property.
        field (Optional[str]):
            Sets the
            :attr:`google.cloud.bigquery.table.RangePartitioning.field`
            property.
        _properties (Optional[dict]):
            Private. Used to construct object from API resource.
    """

    def __init__(self, range_=None, field=None, _properties=None):
        if _properties is None:
            _properties = {}
        self._properties = _properties

        if range_ is not None:
            self.range_ = range_
        if field is not None:
            self.field = field

    # Trailing underscore to prevent conflict with built-in range() function.
    @property
    def range_(self):
        """google.cloud.bigquery.table.PartitionRange: Defines the
        ranges for range partitioning.

        Raises:
            ValueError:
                If the value is not a :class:`PartitionRange`.
        """
        range_properties = self._properties.setdefault("range", {})
        return PartitionRange(_properties=range_properties)

    @range_.setter
    def range_(self, value):
        if not isinstance(value, PartitionRange):
            raise ValueError("Expected a PartitionRange, but got {}.".format(value))
        self._properties["range"] = value._properties

    @property
    def field(self):
        """str: The table is partitioned by this field.

        The field must be a top-level ``NULLABLE`` / ``REQUIRED`` field. The
        only supported type is ``INTEGER`` / ``INT64``.
        """
        return self._properties.get("field")

    @field.setter
    def field(self, value):
        self._properties["field"] = value

    def _key(self):
        return (("field", self.field), ("range_", self.range_))

    def __repr__(self):
        key_vals = ["{}={}".format(key, repr(val)) for key, val in self._key()]
        return "RangePartitioning({})".format(", ".join(key_vals))


class TimePartitioningType(object):
    """Specifies the type of time partitioning to perform."""

    DAY = "DAY"
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
            DEPRECATED: Use
            :attr:`~google.cloud.bigquery.table.Table.require_partition_filter`,
            instead.
    """

    def __init__(
        self, type_=None, field=None, expiration_ms=None, require_partition_filter=None
    ):
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
        return self._properties.get("type")

    @type_.setter
    def type_(self, value):
        self._properties["type"] = value

    @property
    def field(self):
        """str: Field in the table to use for partitioning"""
        return self._properties.get("field")

    @field.setter
    def field(self, value):
        self._properties["field"] = value

    @property
    def expiration_ms(self):
        """int: Number of milliseconds to keep the storage for a partition."""
        return _helpers._int_or_none(self._properties.get("expirationMs"))

    @expiration_ms.setter
    def expiration_ms(self, value):
        if value is not None:
            # Allow explicitly setting the expiration to None.
            value = str(value)
        self._properties["expirationMs"] = value

    @property
    def require_partition_filter(self):
        """bool: Specifies whether partition filters are required for queries

        DEPRECATED: Use
        :attr:`~google.cloud.bigquery.table.Table.require_partition_filter`,
        instead.
        """
        warnings.warn(
            (
                "TimePartitioning.require_partition_filter will be removed in "
                "future versions. Please use Table.require_partition_filter "
                "instead."
            ),
            PendingDeprecationWarning,
            stacklevel=2,
        )
        return self._properties.get("requirePartitionFilter")

    @require_partition_filter.setter
    def require_partition_filter(self, value):
        warnings.warn(
            (
                "TimePartitioning.require_partition_filter will be removed in "
                "future versions. Please use Table.require_partition_filter "
                "instead."
            ),
            PendingDeprecationWarning,
            stacklevel=2,
        )
        self._properties["requirePartitionFilter"] = value

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
        instance = cls()
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
        key_vals = ["{}={}".format(key, val) for key, val in self._key()]
        return "TimePartitioning({})".format(",".join(key_vals))


def _item_to_row(iterator, resource):
    """Convert a JSON row to the native object.

    .. note::

        This assumes that the ``schema`` attribute has been
        added to the iterator after being created, which
        should be done by the caller.

    Args:
        iterator (google.api_core.page_iterator.Iterator): The iterator that is currently in use.
        resource (Dict): An item to be converted to a row.

    Returns:
        google.cloud.bigquery.table.Row: The next row in the page.
    """
    return Row(
        _helpers._row_tuple_from_json(resource, iterator.schema),
        iterator._field_to_index,
    )


def _tabledata_list_page_columns(schema, response):
    """Make a generator of all the columns in a page from tabledata.list.

    This enables creating a :class:`pandas.DataFrame` and other
    column-oriented data structures such as :class:`pyarrow.RecordBatch`
    """
    columns = []
    rows = response.get("rows", [])

    def get_column_data(field_index, field):
        for row in rows:
            yield _helpers._field_from_json(row["f"][field_index]["v"], field)

    for field_index, field in enumerate(schema):
        columns.append(get_column_data(field_index, field))

    return columns


# pylint: disable=unused-argument
def _rows_page_start(iterator, page, response):
    """Grab total rows when :class:`~google.cloud.iterator.Page` starts.

    Args:
        iterator (google.api_core.page_iterator.Iterator): The iterator that is currently in use.
        page (google.api_core.page_iterator.Page): The page that was just created.
        response (Dict): The JSON API response for a page of rows in a table.
    """
    # Make a (lazy) copy of the page in column-oriented format for use in data
    # science packages.
    page._columns = _tabledata_list_page_columns(iterator._schema, response)

    total_rows = response.get("totalRows")
    if total_rows is not None:
        total_rows = int(total_rows)
    iterator._total_rows = total_rows


# pylint: enable=unused-argument


def _table_arg_to_table_ref(value, default_project=None):
    """Helper to convert a string or Table to TableReference.

    This function keeps TableReference and other kinds of objects unchanged.
    """
    if isinstance(value, six.string_types):
        value = TableReference.from_string(value, default_project=default_project)
    if isinstance(value, (Table, TableListItem)):
        value = value.reference
    return value


def _table_arg_to_table(value, default_project=None):
    """Helper to convert a string or TableReference to a Table.

    This function keeps Table and other kinds of objects unchanged.
    """
    if isinstance(value, six.string_types):
        value = TableReference.from_string(value, default_project=default_project)
    if isinstance(value, TableReference):
        value = Table(value)
    if isinstance(value, TableListItem):
        newvalue = Table(value.reference)
        newvalue._properties = value._properties
        value = newvalue

    return value
