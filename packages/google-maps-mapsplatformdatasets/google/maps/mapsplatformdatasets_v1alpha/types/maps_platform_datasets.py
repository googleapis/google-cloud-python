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
from typing import MutableMapping, MutableSequence

from google.protobuf import field_mask_pb2  # type: ignore
import proto  # type: ignore

from google.maps.mapsplatformdatasets_v1alpha.types import dataset as gmm_dataset

__protobuf__ = proto.module(
    package="google.maps.mapsplatformdatasets.v1alpha",
    manifest={
        "CreateDatasetRequest",
        "UpdateDatasetMetadataRequest",
        "GetDatasetRequest",
        "ListDatasetVersionsRequest",
        "ListDatasetVersionsResponse",
        "ListDatasetsRequest",
        "ListDatasetsResponse",
        "DeleteDatasetRequest",
        "DeleteDatasetVersionRequest",
    },
)


class CreateDatasetRequest(proto.Message):
    r"""Request to create a maps dataset.

    Attributes:
        parent (str):
            Required. Parent project that will own the dataset. Format:
            projects/{$project_number}
        dataset (google.maps.mapsplatformdatasets_v1alpha.types.Dataset):
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
        dataset (google.maps.mapsplatformdatasets_v1alpha.types.Dataset):
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
            Required. Resource name. Can also fetch a specified version
            projects/{project}/datasets/{dataset_id}
            projects/{project}/datasets/{dataset_id}@{version-id}

            In order to retrieve a previous version of the dataset, also
            provide the version ID. Example:
            projects/123/datasets/assisted-driving-preferences@c7cfa2a8
        published_usage (google.maps.mapsplatformdatasets_v1alpha.types.Usage):
            If specified, will fetch the dataset details
            of the version published for the specified use
            case rather than the latest, if one exists. If a
            published version does not exist, will default
            to getting the dataset details of the latest
            version.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    published_usage: gmm_dataset.Usage = proto.Field(
        proto.ENUM,
        number=2,
        enum=gmm_dataset.Usage,
    )


class ListDatasetVersionsRequest(proto.Message):
    r"""Request to list of all versions of the dataset.

    Attributes:
        name (str):
            Required. The name of the dataset to list all
            the versions for.
        page_size (int):
            The maximum number of versions to return per
            page. If unspecified (or zero), at most 1000
            versions will be returned. The maximum value is
            1000; values above 1000 will be coerced to 1000.
        page_token (str):
            The page token, received from a previous
            GetDatasetVersions call. Provide this to
            retrieve the subsequent page.
    """

    name: str = proto.Field(
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


class ListDatasetVersionsResponse(proto.Message):
    r"""Response with list of all versions of the dataset.

    Attributes:
        datasets (MutableSequence[google.maps.mapsplatformdatasets_v1alpha.types.Dataset]):
            All the versions of the dataset.
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


class ListDatasetsRequest(proto.Message):
    r"""Request to list datasets for the project.

    Attributes:
        parent (str):
            Required. The name of the project to list all
            the datasets for.
        page_size (int):
            The maximum number of versions to return per
            page. If unspecified (or zero), at most 1000
            datasets will be returned. The maximum value is
            1000; values above 1000 will be coerced to 1000.
        page_token (str):
            The page token, received from a previous
            GetDatasetVersions call. Provide this to
            retrieve the subsequent page.
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
        datasets (MutableSequence[google.maps.mapsplatformdatasets_v1alpha.types.Dataset]):
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
        force (bool):
            If set to true, any dataset version for this
            dataset will also be deleted. (Otherwise, the
            request will only work if the dataset has no
            versions.)
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class DeleteDatasetVersionRequest(proto.Message):
    r"""Request to delete a version of a dataset.

    Attributes:
        name (str):
            Required. Format:
            projects/${project}/datasets/{dataset_id}@{version-id}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
