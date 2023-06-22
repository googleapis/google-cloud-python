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

import copy

import typing

import google.cloud._helpers  # type: ignore

from google.cloud.bigquery import _helpers
from google.cloud.bigquery.model import ModelReference
from google.cloud.bigquery.routine import Routine, RoutineReference
from google.cloud.bigquery.table import Table, TableReference
from google.cloud.bigquery.encryption_configuration import EncryptionConfiguration

from typing import Optional, List, Dict, Any, Union


def _get_table_reference(self, table_id: str) -> TableReference:
    """Constructs a TableReference.

    Args:
        table_id (str): The ID of the table.

    Returns:
        google.cloud.bigquery.table.TableReference:
            A table reference for a table in this dataset.
    """
    return TableReference(self, table_id)


def _get_model_reference(self, model_id):
    """Constructs a ModelReference.

    Args:
        model_id (str): the ID of the model.

    Returns:
        google.cloud.bigquery.model.ModelReference:
            A ModelReference for a model in this dataset.
    """
    return ModelReference.from_api_repr(
        {"projectId": self.project, "datasetId": self.dataset_id, "modelId": model_id}
    )


def _get_routine_reference(self, routine_id):
    """Constructs a RoutineReference.

    Args:
        routine_id (str): the ID of the routine.

    Returns:
        google.cloud.bigquery.routine.RoutineReference:
            A RoutineReference for a routine in this dataset.
    """
    return RoutineReference.from_api_repr(
        {
            "projectId": self.project,
            "datasetId": self.dataset_id,
            "routineId": routine_id,
        }
    )


class DatasetReference(object):
    """DatasetReferences are pointers to datasets.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets#datasetreference

    Args:
        project (str): The ID of the project
        dataset_id (str): The ID of the dataset

    Raises:
        ValueError: If either argument is not of type ``str``.
    """

    def __init__(self, project, dataset_id):
        if not isinstance(project, str):
            raise ValueError("Pass a string for project")
        if not isinstance(dataset_id, str):
            raise ValueError("Pass a string for dataset_id")
        self._project = project
        self._dataset_id = dataset_id

    @property
    def project(self):
        """str: Project ID of the dataset."""
        return self._project

    @property
    def dataset_id(self):
        """str: Dataset ID."""
        return self._dataset_id

    @property
    def path(self):
        """str: URL path for the dataset based on project and dataset ID."""
        return "/projects/%s/datasets/%s" % (self.project, self.dataset_id)

    table = _get_table_reference

    model = _get_model_reference

    routine = _get_routine_reference

    @classmethod
    def from_api_repr(cls, resource: dict) -> "DatasetReference":
        """Factory: construct a dataset reference given its API representation

        Args:
            resource (Dict[str, str]):
                Dataset reference resource representation returned from the API

        Returns:
            google.cloud.bigquery.dataset.DatasetReference:
                Dataset reference parsed from ``resource``.
        """
        project = resource["projectId"]
        dataset_id = resource["datasetId"]
        return cls(project, dataset_id)

    @classmethod
    def from_string(
        cls, dataset_id: str, default_project: Optional[str] = None
    ) -> "DatasetReference":
        """Construct a dataset reference from dataset ID string.

        Args:
            dataset_id (str):
                A dataset ID in standard SQL format. If ``default_project``
                is not specified, this must include both the project ID and
                the dataset ID, separated by ``.``.
            default_project (Optional[str]):
                The project ID to use when ``dataset_id`` does not include a
                project ID.

        Returns:
            DatasetReference:
                Dataset reference parsed from ``dataset_id``.

        Examples:
            >>> DatasetReference.from_string('my-project-id.some_dataset')
            DatasetReference('my-project-id', 'some_dataset')

        Raises:
            ValueError:
                If ``dataset_id`` is not a fully-qualified dataset ID in
                standard SQL format.
        """
        output_dataset_id = dataset_id
        output_project_id = default_project
        parts = _helpers._split_id(dataset_id)

        if len(parts) == 1 and not default_project:
            raise ValueError(
                "When default_project is not set, dataset_id must be a "
                "fully-qualified dataset ID in standard SQL format, "
                'e.g., "project.dataset_id" got {}'.format(dataset_id)
            )
        elif len(parts) == 2:
            output_project_id, output_dataset_id = parts
        elif len(parts) > 2:
            raise ValueError(
                "Too many parts in dataset_id. Expected a fully-qualified "
                "dataset ID in standard SQL format. e.g. "
                '"project.dataset_id", got {}'.format(dataset_id)
            )

        return cls(output_project_id, output_dataset_id)

    def to_api_repr(self) -> dict:
        """Construct the API resource representation of this dataset reference

        Returns:
            Dict[str, str]: dataset reference represented as an API resource
        """
        return {"projectId": self._project, "datasetId": self._dataset_id}

    def _key(self):
        """A tuple key that uniquely describes this field.

        Used to compute this instance's hashcode and evaluate equality.

        Returns:
            Tuple[str]: The contents of this :class:`.DatasetReference`.
        """
        return (self._project, self._dataset_id)

    def __eq__(self, other):
        if not isinstance(other, DatasetReference):
            return NotImplemented
        return self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._key())

    def __str__(self):
        return f"{self.project}.{self._dataset_id}"

    def __repr__(self):
        return "DatasetReference{}".format(self._key())


class AccessEntry(object):
    """Represents grant of an access role to an entity.

    An entry must have exactly one of the allowed
    :class:`google.cloud.bigquery.enums.EntityTypes`. If anything but ``view``, ``routine``,
    or ``dataset`` are set, a ``role`` is also required. ``role`` is omitted for ``view``,
    ``routine``, ``dataset``, because they are always read-only.

    See https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets.

    Args:
        role:
            Role granted to the entity. The following string values are
            supported: `'READER'`, `'WRITER'`, `'OWNER'`. It may also be
            :data:`None` if the ``entity_type`` is ``view``, ``routine``, or ``dataset``.

        entity_type:
            Type of entity being granted the role. See
            :class:`google.cloud.bigquery.enums.EntityTypes` for supported types.

        entity_id:
            If the ``entity_type`` is not 'view', 'routine', or 'dataset', the
            ``entity_id`` is the ``str`` ID of the entity being granted the role. If
            the ``entity_type`` is 'view' or 'routine', the ``entity_id`` is a ``dict``
            representing the view or routine from a different dataset to grant access
            to in the following format for views::

                {
                    'projectId': string,
                    'datasetId': string,
                    'tableId': string
                }

            For routines::

                {
                    'projectId': string,
                    'datasetId': string,
                    'routineId': string
                }

            If the ``entity_type`` is 'dataset', the ``entity_id`` is a ``dict`` that includes
            a 'dataset' field with a ``dict`` representing the dataset and a 'target_types'
            field with a ``str`` value of the dataset's resource type::

                {
                    'dataset': {
                        'projectId': string,
                        'datasetId': string,
                    },
                    'target_types: 'VIEWS'
                }

    Raises:
        ValueError:
            If a ``view``, ``routine``, or ``dataset`` has ``role`` set, or a non ``view``,
            non ``routine``, and non ``dataset`` **does not** have a ``role`` set.

    Examples:
        >>> entry = AccessEntry('OWNER', 'userByEmail', 'user@example.com')

        >>> view = {
        ...     'projectId': 'my-project',
        ...     'datasetId': 'my_dataset',
        ...     'tableId': 'my_table'
        ... }
        >>> entry = AccessEntry(None, 'view', view)
    """

    def __init__(
        self,
        role: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[Union[Dict[str, Any], str]] = None,
    ):
        self._properties = {}
        if entity_type is not None:
            self._properties[entity_type] = entity_id
        self._properties["role"] = role
        self._entity_type = entity_type

    @property
    def role(self) -> Optional[str]:
        """The role of the entry."""
        return typing.cast(Optional[str], self._properties.get("role"))

    @role.setter
    def role(self, value):
        self._properties["role"] = value

    @property
    def dataset(self) -> Optional[DatasetReference]:
        """API resource representation of a dataset reference."""
        value = _helpers._get_sub_prop(self._properties, ["dataset", "dataset"])
        return DatasetReference.from_api_repr(value) if value else None

    @dataset.setter
    def dataset(self, value):
        if self.role is not None:
            raise ValueError(
                "Role must be None for a dataset. Current " "role: %r" % (self.role)
            )

        if isinstance(value, str):
            value = DatasetReference.from_string(value).to_api_repr()

        if isinstance(value, (Dataset, DatasetListItem)):
            value = value.reference.to_api_repr()

        _helpers._set_sub_prop(self._properties, ["dataset", "dataset"], value)
        _helpers._set_sub_prop(
            self._properties,
            ["dataset", "targetTypes"],
            self._properties.get("targetTypes"),
        )

    @property
    def dataset_target_types(self) -> Optional[List[str]]:
        """Which resources that the dataset in this entry applies to."""
        return typing.cast(
            Optional[List[str]],
            _helpers._get_sub_prop(self._properties, ["dataset", "targetTypes"]),
        )

    @dataset_target_types.setter
    def dataset_target_types(self, value):
        self._properties.setdefault("dataset", {})
        _helpers._set_sub_prop(self._properties, ["dataset", "targetTypes"], value)

    @property
    def routine(self) -> Optional[RoutineReference]:
        """API resource representation of a routine reference."""
        value = typing.cast(Optional[Dict], self._properties.get("routine"))
        return RoutineReference.from_api_repr(value) if value else None

    @routine.setter
    def routine(self, value):
        if self.role is not None:
            raise ValueError(
                "Role must be None for a routine. Current " "role: %r" % (self.role)
            )

        if isinstance(value, str):
            value = RoutineReference.from_string(value).to_api_repr()

        if isinstance(value, RoutineReference):
            value = value.to_api_repr()

        if isinstance(value, Routine):
            value = value.reference.to_api_repr()

        self._properties["routine"] = value

    @property
    def view(self) -> Optional[TableReference]:
        """API resource representation of a view reference."""
        value = typing.cast(Optional[Dict], self._properties.get("view"))
        return TableReference.from_api_repr(value) if value else None

    @view.setter
    def view(self, value):
        if self.role is not None:
            raise ValueError(
                "Role must be None for a view. Current " "role: %r" % (self.role)
            )

        if isinstance(value, str):
            value = TableReference.from_string(value).to_api_repr()

        if isinstance(value, TableReference):
            value = value.to_api_repr()

        if isinstance(value, Table):
            value = value.reference.to_api_repr()

        self._properties["view"] = value

    @property
    def group_by_email(self) -> Optional[str]:
        """An email address of a Google Group to grant access to."""
        return typing.cast(Optional[str], self._properties.get("groupByEmail"))

    @group_by_email.setter
    def group_by_email(self, value):
        self._properties["groupByEmail"] = value

    @property
    def user_by_email(self) -> Optional[str]:
        """An email address of a user to grant access to."""
        return typing.cast(Optional[str], self._properties.get("userByEmail"))

    @user_by_email.setter
    def user_by_email(self, value):
        self._properties["userByEmail"] = value

    @property
    def domain(self) -> Optional[str]:
        """A domain to grant access to."""
        return typing.cast(Optional[str], self._properties.get("domain"))

    @domain.setter
    def domain(self, value):
        self._properties["domain"] = value

    @property
    def special_group(self) -> Optional[str]:
        """A special group to grant access to."""
        return typing.cast(Optional[str], self._properties.get("specialGroup"))

    @special_group.setter
    def special_group(self, value):
        self._properties["specialGroup"] = value

    @property
    def entity_type(self) -> Optional[str]:
        """The entity_type of the entry."""
        return self._entity_type

    @property
    def entity_id(self) -> Optional[Union[Dict[str, Any], str]]:
        """The entity_id of the entry."""
        return self._properties.get(self._entity_type) if self._entity_type else None

    def __eq__(self, other):
        if not isinstance(other, AccessEntry):
            return NotImplemented
        return self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __repr__(self):

        return f"<AccessEntry: role={self.role}, {self._entity_type}={self.entity_id}>"

    def _key(self):
        """A tuple key that uniquely describes this field.
        Used to compute this instance's hashcode and evaluate equality.
        Returns:
            Tuple: The contents of this :class:`~google.cloud.bigquery.dataset.AccessEntry`.
        """
        properties = self._properties.copy()
        prop_tup = tuple(sorted(properties.items()))
        return (self.role, self._entity_type, self.entity_id, prop_tup)

    def __hash__(self):
        return hash(self._key())

    def to_api_repr(self):
        """Construct the API resource representation of this access entry

        Returns:
            Dict[str, object]: Access entry represented as an API resource
        """
        resource = copy.deepcopy(self._properties)
        return resource

    @classmethod
    def from_api_repr(cls, resource: dict) -> "AccessEntry":
        """Factory: construct an access entry given its API representation

        Args:
            resource (Dict[str, object]):
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
        role = entry.pop("role", None)
        entity_type, entity_id = entry.popitem()
        if len(entry) != 0:
            raise ValueError("Entry has unexpected keys remaining.", entry)

        config = cls(role, entity_type, entity_id)
        config._properties = copy.deepcopy(resource)
        return config


class Dataset(object):
    """Datasets are containers for tables.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets#resource-dataset

    Args:
        dataset_ref (Union[google.cloud.bigquery.dataset.DatasetReference, str]):
            A pointer to a dataset. If ``dataset_ref`` is a string, it must
            include both the project ID and the dataset ID, separated by
            ``.``.
    """

    _PROPERTY_TO_API_FIELD = {
        "access_entries": "access",
        "created": "creationTime",
        "default_partition_expiration_ms": "defaultPartitionExpirationMs",
        "default_table_expiration_ms": "defaultTableExpirationMs",
        "friendly_name": "friendlyName",
        "default_encryption_configuration": "defaultEncryptionConfiguration",
    }

    def __init__(self, dataset_ref) -> None:
        if isinstance(dataset_ref, str):
            dataset_ref = DatasetReference.from_string(dataset_ref)
        self._properties = {"datasetReference": dataset_ref.to_api_repr(), "labels": {}}

    @property
    def project(self):
        """str: Project ID of the project bound to the dataset."""
        return self._properties["datasetReference"]["projectId"]

    @property
    def path(self):
        """str: URL path for the dataset based on project and dataset ID."""
        return "/projects/%s/datasets/%s" % (self.project, self.dataset_id)

    @property
    def access_entries(self):
        """List[google.cloud.bigquery.dataset.AccessEntry]: Dataset's access
        entries.

        ``role`` augments the entity type and must be present **unless** the
        entity type is ``view`` or ``routine``.

        Raises:
            TypeError: If 'value' is not a sequence
            ValueError:
                If any item in the sequence is not an
                :class:`~google.cloud.bigquery.dataset.AccessEntry`.
        """
        entries = self._properties.get("access", [])
        return [AccessEntry.from_api_repr(entry) for entry in entries]

    @access_entries.setter
    def access_entries(self, value):
        if not all(isinstance(field, AccessEntry) for field in value):
            raise ValueError("Values must be AccessEntry instances")
        entries = [entry.to_api_repr() for entry in value]
        self._properties["access"] = entries

    @property
    def created(self):
        """Union[datetime.datetime, None]: Datetime at which the dataset was
        created (:data:`None` until set from the server).
        """
        creation_time = self._properties.get("creationTime")
        if creation_time is not None:
            # creation_time will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(creation_time)
            )

    @property
    def dataset_id(self):
        """str: Dataset ID."""
        return self._properties["datasetReference"]["datasetId"]

    @property
    def full_dataset_id(self):
        """Union[str, None]: ID for the dataset resource (:data:`None` until
        set from the server)

        In the format ``project_id:dataset_id``.
        """
        return self._properties.get("id")

    @property
    def reference(self):
        """google.cloud.bigquery.dataset.DatasetReference: A reference to this
        dataset.
        """
        return DatasetReference(self.project, self.dataset_id)

    @property
    def etag(self):
        """Union[str, None]: ETag for the dataset resource (:data:`None` until
        set from the server).
        """
        return self._properties.get("etag")

    @property
    def modified(self):
        """Union[datetime.datetime, None]: Datetime at which the dataset was
        last modified (:data:`None` until set from the server).
        """
        modified_time = self._properties.get("lastModifiedTime")
        if modified_time is not None:
            # modified_time will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(modified_time)
            )

    @property
    def self_link(self):
        """Union[str, None]: URL for the dataset resource (:data:`None` until
        set from the server).
        """
        return self._properties.get("selfLink")

    @property
    def default_partition_expiration_ms(self):
        """Optional[int]: The default partition expiration for all
        partitioned tables in the dataset, in milliseconds.

        Once this property is set, all newly-created partitioned tables in
        the dataset will have an ``time_paritioning.expiration_ms`` property
        set to this value, and changing the value will only affect new
        tables, not existing ones. The storage in a partition will have an
        expiration time of its partition time plus this value.

        Setting this property overrides the use of
        ``default_table_expiration_ms`` for partitioned tables: only one of
        ``default_table_expiration_ms`` and
        ``default_partition_expiration_ms`` will be used for any new
        partitioned table. If you provide an explicit
        ``time_partitioning.expiration_ms`` when creating or updating a
        partitioned table, that value takes precedence over the default
        partition expiration time indicated by this property.
        """
        return _helpers._int_or_none(
            self._properties.get("defaultPartitionExpirationMs")
        )

    @default_partition_expiration_ms.setter
    def default_partition_expiration_ms(self, value):
        self._properties["defaultPartitionExpirationMs"] = _helpers._str_or_none(value)

    @property
    def default_table_expiration_ms(self):
        """Union[int, None]: Default expiration time for tables in the dataset
        (defaults to :data:`None`).

        Raises:
            ValueError: For invalid value types.
        """
        return _helpers._int_or_none(self._properties.get("defaultTableExpirationMs"))

    @default_table_expiration_ms.setter
    def default_table_expiration_ms(self, value):
        if not isinstance(value, int) and value is not None:
            raise ValueError("Pass an integer, or None")
        self._properties["defaultTableExpirationMs"] = _helpers._str_or_none(value)

    @property
    def description(self):
        """Optional[str]: Description of the dataset as set by the user
        (defaults to :data:`None`).

        Raises:
            ValueError: for invalid value types.
        """
        return self._properties.get("description")

    @description.setter
    def description(self, value):
        if not isinstance(value, str) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties["description"] = value

    @property
    def friendly_name(self):
        """Union[str, None]: Title of the dataset as set by the user
        (defaults to :data:`None`).

        Raises:
            ValueError: for invalid value types.
        """
        return self._properties.get("friendlyName")

    @friendly_name.setter
    def friendly_name(self, value):
        if not isinstance(value, str) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties["friendlyName"] = value

    @property
    def location(self):
        """Union[str, None]: Location in which the dataset is hosted as set by
        the user (defaults to :data:`None`).

        Raises:
            ValueError: for invalid value types.
        """
        return self._properties.get("location")

    @location.setter
    def location(self, value):
        if not isinstance(value, str) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties["location"] = value

    @property
    def labels(self):
        """Dict[str, str]: Labels for the dataset.

        This method always returns a dict. To change a dataset's labels,
        modify the dict, then call
        :meth:`google.cloud.bigquery.client.Client.update_dataset`. To delete
        a label, set its value to :data:`None` before updating.

        Raises:
            ValueError: for invalid value types.
        """
        return self._properties.setdefault("labels", {})

    @labels.setter
    def labels(self, value):
        if not isinstance(value, dict):
            raise ValueError("Pass a dict")
        self._properties["labels"] = value

    @property
    def default_encryption_configuration(self):
        """google.cloud.bigquery.encryption_configuration.EncryptionConfiguration: Custom
        encryption configuration for all tables in the dataset.

        Custom encryption configuration (e.g., Cloud KMS keys) or :data:`None`
        if using default encryption.

        See `protecting data with Cloud KMS keys
        <https://cloud.google.com/bigquery/docs/customer-managed-encryption>`_
        in the BigQuery documentation.
        """
        prop = self._properties.get("defaultEncryptionConfiguration")
        if prop:
            prop = EncryptionConfiguration.from_api_repr(prop)
        return prop

    @default_encryption_configuration.setter
    def default_encryption_configuration(self, value):
        api_repr = value
        if value:
            api_repr = value.to_api_repr()
        self._properties["defaultEncryptionConfiguration"] = api_repr

    @classmethod
    def from_string(cls, full_dataset_id: str) -> "Dataset":
        """Construct a dataset from fully-qualified dataset ID.

        Args:
            full_dataset_id (str):
                A fully-qualified dataset ID in standard SQL format. Must
                include both the project ID and the dataset ID, separated by
                ``.``.

        Returns:
            Dataset: Dataset parsed from ``full_dataset_id``.

        Examples:
            >>> Dataset.from_string('my-project-id.some_dataset')
            Dataset(DatasetReference('my-project-id', 'some_dataset'))

        Raises:
            ValueError:
                If ``full_dataset_id`` is not a fully-qualified dataset ID in
                standard SQL format.
        """
        return cls(DatasetReference.from_string(full_dataset_id))

    @classmethod
    def from_api_repr(cls, resource: dict) -> "Dataset":
        """Factory: construct a dataset given its API representation

        Args:
            resource (Dict[str: object]):
                Dataset resource representation returned from the API

        Returns:
            google.cloud.bigquery.dataset.Dataset:
                Dataset parsed from ``resource``.
        """
        if (
            "datasetReference" not in resource
            or "datasetId" not in resource["datasetReference"]
        ):
            raise KeyError(
                "Resource lacks required identity information:"
                '["datasetReference"]["datasetId"]'
            )
        project_id = resource["datasetReference"]["projectId"]
        dataset_id = resource["datasetReference"]["datasetId"]
        dataset = cls(DatasetReference(project_id, dataset_id))
        dataset._properties = copy.deepcopy(resource)
        return dataset

    def to_api_repr(self) -> dict:
        """Construct the API resource representation of this dataset

        Returns:
            Dict[str, object]: The dataset represented as an API resource
        """
        return copy.deepcopy(self._properties)

    def _build_resource(self, filter_fields):
        """Generate a resource for ``update``."""
        return _helpers._build_resource_from_properties(self, filter_fields)

    table = _get_table_reference

    model = _get_model_reference

    routine = _get_routine_reference

    def __repr__(self):
        return "Dataset({})".format(repr(self.reference))


class DatasetListItem(object):
    """A read-only dataset resource from a list operation.

    For performance reasons, the BigQuery API only includes some of the
    dataset properties when listing datasets. Notably,
    :attr:`~google.cloud.bigquery.dataset.Dataset.access_entries` is missing.

    For a full list of the properties that the BigQuery API returns, see the
    `REST documentation for datasets.list
    <https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/list>`_.


    Args:
        resource (Dict[str, str]):
            A dataset-like resource object from a dataset list response. A
            ``datasetReference`` property is required.

    Raises:
        ValueError:
            If ``datasetReference`` or one of its required members is missing
            from ``resource``.
    """

    def __init__(self, resource):
        if "datasetReference" not in resource:
            raise ValueError("resource must contain a datasetReference value")
        if "projectId" not in resource["datasetReference"]:
            raise ValueError(
                "resource['datasetReference'] must contain a projectId value"
            )
        if "datasetId" not in resource["datasetReference"]:
            raise ValueError(
                "resource['datasetReference'] must contain a datasetId value"
            )
        self._properties = resource

    @property
    def project(self):
        """str: Project bound to the dataset."""
        return self._properties["datasetReference"]["projectId"]

    @property
    def dataset_id(self):
        """str: Dataset ID."""
        return self._properties["datasetReference"]["datasetId"]

    @property
    def full_dataset_id(self):
        """Union[str, None]: ID for the dataset resource (:data:`None` until
        set from the server)

        In the format ``project_id:dataset_id``.
        """
        return self._properties.get("id")

    @property
    def friendly_name(self):
        """Union[str, None]: Title of the dataset as set by the user
        (defaults to :data:`None`).
        """
        return self._properties.get("friendlyName")

    @property
    def labels(self):
        """Dict[str, str]: Labels for the dataset."""
        return self._properties.setdefault("labels", {})

    @property
    def reference(self):
        """google.cloud.bigquery.dataset.DatasetReference: A reference to this
        dataset.
        """
        return DatasetReference(self.project, self.dataset_id)

    table = _get_table_reference

    model = _get_model_reference

    routine = _get_routine_reference
