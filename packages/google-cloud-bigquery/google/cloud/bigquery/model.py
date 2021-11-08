# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Define resources for the BigQuery ML Models API."""

import copy

from google.protobuf import json_format

import google.cloud._helpers  # type: ignore
from google.api_core import datetime_helpers  # type: ignore
from google.cloud.bigquery import _helpers
from google.cloud.bigquery_v2 import types
from google.cloud.bigquery.encryption_configuration import EncryptionConfiguration


class Model(object):
    """Model represents a machine learning model resource.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/models

    Args:
        model_ref (Union[google.cloud.bigquery.model.ModelReference, str]):
            A pointer to a model. If ``model_ref`` is a string, it must
            included a project ID, dataset ID, and model ID, each separated
            by ``.``.
    """

    _PROPERTY_TO_API_FIELD = {
        "expires": "expirationTime",
        "friendly_name": "friendlyName",
        # Even though it's not necessary for field mapping to map when the
        # property name equals the resource name, we add these here so that we
        # have an exhaustive list of all mutable properties.
        "labels": "labels",
        "description": "description",
        "encryption_configuration": "encryptionConfiguration",
    }

    def __init__(self, model_ref):
        # Use _proto on read-only properties to use it's built-in type
        # conversion.
        self._proto = types.Model()._pb

        # Use _properties on read-write properties to match the REST API
        # semantics. The BigQuery API makes a distinction between an unset
        # value, a null value, and a default value (0 or ""), but the protocol
        # buffer classes do not.
        self._properties = {}

        if isinstance(model_ref, str):
            model_ref = ModelReference.from_string(model_ref)

        if model_ref:
            self._proto.model_reference.CopyFrom(model_ref._proto)

    @property
    def reference(self):
        """A :class:`~google.cloud.bigquery.model.ModelReference` pointing to
        this model.

        Read-only.

        Returns:
            google.cloud.bigquery.model.ModelReference: pointer to this model.
        """
        ref = ModelReference()
        ref._proto = self._proto.model_reference
        return ref

    @property
    def project(self):
        """str: Project bound to the model"""
        return self.reference.project

    @property
    def dataset_id(self):
        """str: ID of dataset containing the model."""
        return self.reference.dataset_id

    @property
    def model_id(self):
        """str: The model ID."""
        return self.reference.model_id

    @property
    def path(self):
        """str: URL path for the model's APIs."""
        return self.reference.path

    @property
    def location(self):
        """str: The geographic location where the model resides. This value
        is inherited from the dataset.

        Read-only.
        """
        return self._proto.location

    @property
    def etag(self):
        """str: ETag for the model resource (:data:`None` until
        set from the server).

        Read-only.
        """
        return self._proto.etag

    @property
    def created(self):
        """Union[datetime.datetime, None]: Datetime at which the model was
        created (:data:`None` until set from the server).

        Read-only.
        """
        value = self._proto.creation_time
        if value is not None and value != 0:
            # value will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(value)
            )

    @property
    def modified(self):
        """Union[datetime.datetime, None]: Datetime at which the model was last
        modified (:data:`None` until set from the server).

        Read-only.
        """
        value = self._proto.last_modified_time
        if value is not None and value != 0:
            # value will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(value)
            )

    @property
    def model_type(self):
        """google.cloud.bigquery_v2.types.Model.ModelType: Type of the
        model resource.

        Read-only.

        The value is one of elements of the
        :class:`~google.cloud.bigquery_v2.types.Model.ModelType`
        enumeration.
        """
        return self._proto.model_type

    @property
    def training_runs(self):
        """Sequence[google.cloud.bigquery_v2.types.Model.TrainingRun]: Information
        for all training runs in increasing order of start time.

        Read-only.

        An iterable of :class:`~google.cloud.bigquery_v2.types.Model.TrainingRun`.
        """
        return self._proto.training_runs

    @property
    def feature_columns(self):
        """Sequence[google.cloud.bigquery_v2.types.StandardSqlField]: Input
        feature columns that were used to train this model.

        Read-only.

        An iterable of :class:`~google.cloud.bigquery_v2.types.StandardSqlField`.
        """
        return self._proto.feature_columns

    @property
    def label_columns(self):
        """Sequence[google.cloud.bigquery_v2.types.StandardSqlField]: Label
        columns that were used to train this model. The output of the model
        will have a ``predicted_`` prefix to these columns.

        Read-only.

        An iterable of :class:`~google.cloud.bigquery_v2.types.StandardSqlField`.
        """
        return self._proto.label_columns

    @property
    def expires(self):
        """Union[datetime.datetime, None]: The datetime when this model
        expires. If not present, the model will persist indefinitely. Expired
        models will be deleted and their storage reclaimed.
        """
        value = self._properties.get("expirationTime")
        if value is not None:
            # value will be in milliseconds.
            return google.cloud._helpers._datetime_from_microseconds(
                1000.0 * float(value)
            )

    @expires.setter
    def expires(self, value):
        if value is not None:
            value = str(google.cloud._helpers._millis_from_datetime(value))
        self._properties["expirationTime"] = value

    @property
    def description(self):
        """Optional[str]: Description of the model (defaults to
        :data:`None`).
        """
        return self._properties.get("description")

    @description.setter
    def description(self, value):
        self._properties["description"] = value

    @property
    def friendly_name(self):
        """Optional[str]: Title of the table (defaults to :data:`None`).

        Raises:
            ValueError: For invalid value types.
        """
        return self._properties.get("friendlyName")

    @friendly_name.setter
    def friendly_name(self, value):
        self._properties["friendlyName"] = value

    @property
    def labels(self):
        """Optional[Dict[str, str]]: Labels for the table.

        This method always returns a dict. To change a model's labels,
        modify the dict, then call ``Client.update_model``. To delete a
        label, set its value to :data:`None` before updating.
        """
        return self._properties.setdefault("labels", {})

    @labels.setter
    def labels(self, value):
        if value is None:
            value = {}
        self._properties["labels"] = value

    @property
    def encryption_configuration(self):
        """Optional[google.cloud.bigquery.encryption_configuration.EncryptionConfiguration]: Custom
        encryption configuration for the model.

        Custom encryption configuration (e.g., Cloud KMS keys) or :data:`None`
        if using default encryption.

        See `protecting data with Cloud KMS keys
        <https://cloud.google.com/bigquery/docs/customer-managed-encryption>`_
        in the BigQuery documentation.
        """
        prop = self._properties.get("encryptionConfiguration")
        if prop:
            prop = EncryptionConfiguration.from_api_repr(prop)
        return prop

    @encryption_configuration.setter
    def encryption_configuration(self, value):
        api_repr = value
        if value:
            api_repr = value.to_api_repr()
        self._properties["encryptionConfiguration"] = api_repr

    @classmethod
    def from_api_repr(cls, resource: dict) -> "Model":
        """Factory: construct a model resource given its API representation

        Args:
            resource (Dict[str, object]):
                Model resource representation from the API

        Returns:
            google.cloud.bigquery.model.Model: Model parsed from ``resource``.
        """
        this = cls(None)
        # Keep a reference to the resource as a workaround to find unknown
        # field values.
        this._properties = resource

        # Convert from millis-from-epoch to timestamp well-known type.
        # TODO: Remove this hack once CL 238585470 hits prod.
        resource = copy.deepcopy(resource)
        for training_run in resource.get("trainingRuns", ()):
            start_time = training_run.get("startTime")
            if not start_time or "-" in start_time:  # Already right format?
                continue
            start_time = datetime_helpers.from_microseconds(1e3 * float(start_time))
            training_run["startTime"] = datetime_helpers.to_rfc3339(start_time)

        try:
            this._proto = json_format.ParseDict(
                resource, types.Model()._pb, ignore_unknown_fields=True
            )
        except json_format.ParseError:
            resource["modelType"] = "MODEL_TYPE_UNSPECIFIED"
            this._proto = json_format.ParseDict(
                resource, types.Model()._pb, ignore_unknown_fields=True
            )
        return this

    def _build_resource(self, filter_fields):
        """Generate a resource for ``update``."""
        return _helpers._build_resource_from_properties(self, filter_fields)

    def __repr__(self):
        return "Model(reference={})".format(repr(self.reference))

    def to_api_repr(self) -> dict:
        """Construct the API resource representation of this model.

        Returns:
            Dict[str, object]: Model reference represented as an API resource
        """
        return json_format.MessageToDict(self._proto)


class ModelReference(object):
    """ModelReferences are pointers to models.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/models#modelreference
    """

    def __init__(self):
        self._proto = types.ModelReference()._pb
        self._properties = {}

    @property
    def project(self):
        """str: Project bound to the model"""
        return self._proto.project_id

    @property
    def dataset_id(self):
        """str: ID of dataset containing the model."""
        return self._proto.dataset_id

    @property
    def model_id(self):
        """str: The model ID."""
        return self._proto.model_id

    @property
    def path(self):
        """str: URL path for the model's APIs."""
        return "/projects/%s/datasets/%s/models/%s" % (
            self._proto.project_id,
            self._proto.dataset_id,
            self._proto.model_id,
        )

    @classmethod
    def from_api_repr(cls, resource):
        """Factory:  construct a model reference given its API representation

        Args:
            resource (Dict[str, object]):
                Model reference representation returned from the API

        Returns:
            google.cloud.bigquery.model.ModelReference:
                Model reference parsed from ``resource``.
        """
        ref = cls()
        # Keep a reference to the resource as a workaround to find unknown
        # field values.
        ref._properties = resource
        ref._proto = json_format.ParseDict(
            resource, types.ModelReference()._pb, ignore_unknown_fields=True
        )

        return ref

    @classmethod
    def from_string(
        cls, model_id: str, default_project: str = None
    ) -> "ModelReference":
        """Construct a model reference from model ID string.

        Args:
            model_id (str):
                A model ID in standard SQL format. If ``default_project``
                is not specified, this must included a project ID, dataset
                ID, and model ID, each separated by ``.``.
            default_project (Optional[str]):
                The project ID to use when ``model_id`` does not include
                a project ID.

        Returns:
            google.cloud.bigquery.model.ModelReference:
                Model reference parsed from ``model_id``.

        Raises:
            ValueError:
                If ``model_id`` is not a fully-qualified table ID in
                standard SQL format.
        """
        proj, dset, model = _helpers._parse_3_part_id(
            model_id, default_project=default_project, property_name="model_id"
        )
        return cls.from_api_repr(
            {"projectId": proj, "datasetId": dset, "modelId": model}
        )

    def to_api_repr(self) -> dict:
        """Construct the API resource representation of this model reference.

        Returns:
            Dict[str, object]: Model reference represented as an API resource
        """
        return json_format.MessageToDict(self._proto)

    def _key(self):
        """Unique key for this model.

        This is used for hashing a ModelReference.
        """
        return self.project, self.dataset_id, self.model_id

    def __eq__(self, other):
        if not isinstance(other, ModelReference):
            return NotImplemented
        return self._proto == other._proto

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return "ModelReference(project_id='{}', dataset_id='{}', model_id='{}')".format(
            self.project, self.dataset_id, self.model_id
        )


def _model_arg_to_model_ref(value, default_project=None):
    """Helper to convert a string or Model to ModelReference.

    This function keeps ModelReference and other kinds of objects unchanged.
    """
    if isinstance(value, str):
        return ModelReference.from_string(value, default_project=default_project)
    if isinstance(value, Model):
        return value.reference
    return value
