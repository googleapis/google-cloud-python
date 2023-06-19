# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import field_mask_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.documentai_v1beta3.types import dataset as gcd_dataset
from google.cloud.documentai_v1beta3.types import operation_metadata

__protobuf__ = proto.module(
    package="google.cloud.documentai.v1beta3",
    manifest={
        "UpdateDatasetRequest",
        "UpdateDatasetOperationMetadata",
        "GetDatasetSchemaRequest",
        "UpdateDatasetSchemaRequest",
    },
)


class UpdateDatasetRequest(proto.Message):
    r"""

    Attributes:
        dataset (google.cloud.documentai_v1beta3.types.Dataset):
            Required. The ``name`` field of the ``Dataset`` is used to
            identify the resource to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The update mask applies to the resource.
    """

    dataset: gcd_dataset.Dataset = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_dataset.Dataset,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class UpdateDatasetOperationMetadata(proto.Message):
    r"""

    Attributes:
        common_metadata (google.cloud.documentai_v1beta3.types.CommonOperationMetadata):
            The basic metadata of the long running
            operation.
    """

    common_metadata: operation_metadata.CommonOperationMetadata = proto.Field(
        proto.MESSAGE,
        number=1,
        message=operation_metadata.CommonOperationMetadata,
    )


class GetDatasetSchemaRequest(proto.Message):
    r"""Request for ``GetDatasetSchema``.

    Attributes:
        name (str):
            Required. The dataset schema resource name.
            Format:
            projects/{project}/locations/{location}/processors/{processor}/dataset/datasetSchema
        visible_fields_only (bool):
            If set, only returns the visible fields of
            the schema.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    visible_fields_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class UpdateDatasetSchemaRequest(proto.Message):
    r"""Request for ``UpdateDatasetSchema``.

    Attributes:
        dataset_schema (google.cloud.documentai_v1beta3.types.DatasetSchema):
            Required. The name field of the ``DatasetSchema`` is used to
            identify the resource to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The update mask applies to the resource.
    """

    dataset_schema: gcd_dataset.DatasetSchema = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_dataset.DatasetSchema,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
