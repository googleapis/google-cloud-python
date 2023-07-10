# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.maps.mapsplatformdatasets_v1.types import dataset as gmm_dataset

__protobuf__ = proto.module(
    package="google.maps.mapsplatformdatasets.v1",
    manifest={
        "CreateDatasetRequest",
        "UpdateDatasetMetadataRequest",
        "GetDatasetRequest",
        "ListDatasetsRequest",
        "ListDatasetsResponse",
        "DeleteDatasetRequest",
    },
)


class CreateDatasetRequest(proto.Message):
    r"""Request to create a maps dataset.

    Attributes:
        parent (str):
            Required. Parent project that will own the
            dataset. Format: projects/{$project}
        dataset (google.maps.mapsplatformdatasets_v1.types.Dataset):
            Required. The dataset version to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset: gmm_dataset.Dataset = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gmm_dataset.Dataset,
    )


class UpdateDatasetMetadataRequest(proto.Message):
    r"""Request to update the metadata fields of the dataset.

    Attributes:
        dataset (google.maps.mapsplatformdatasets_v1.types.Dataset):
            Required. The dataset to update. The dataset's name is used
            to identify the dataset to be updated. The name has the
            format: projects/{project}/datasets/{dataset_id}
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated. Support the value "*" for
            full replacement.
    """

    dataset: gmm_dataset.Dataset = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gmm_dataset.Dataset,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class GetDatasetRequest(proto.Message):
    r"""Request to get the specified dataset.

    Attributes:
        name (str):
            Required. Resource name.
            projects/{project}/datasets/{dataset_id}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListDatasetsRequest(proto.Message):
    r"""Request to list datasets for the project.

    Attributes:
        parent (str):
            Required. The name of the project to list all
            the datasets for.
        page_size (int):
            The maximum number of versions to return per
            page. If unspecified (or zero), all datasets
            will be returned.
        page_token (str):
            The page token, received from a previous
            ListDatasets call. Provide this to retrieve the
            subsequent page.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListDatasetsResponse(proto.Message):
    r"""Response to list datasets for the project.

    Attributes:
        datasets (MutableSequence[google.maps.mapsplatformdatasets_v1.types.Dataset]):
            All the datasets for the project.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    datasets: MutableSequence[gmm_dataset.Dataset] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gmm_dataset.Dataset,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteDatasetRequest(proto.Message):
    r"""Request to delete a dataset.
    The dataset to be deleted.

    Attributes:
        name (str):
            Required. Format: projects/${project}/datasets/{dataset_id}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
