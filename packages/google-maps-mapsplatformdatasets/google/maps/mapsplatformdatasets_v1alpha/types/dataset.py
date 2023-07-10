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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.maps.mapsplatformdatasets_v1alpha.types import data_source

__protobuf__ = proto.module(
    package="google.maps.mapsplatformdatasets.v1alpha",
    manifest={
        "Usage",
        "State",
        "Dataset",
    },
)


class Usage(proto.Enum):
    r"""Usage specifies where the data is intended to be used to
    inform how to process the data.

    Values:
        USAGE_UNSPECIFIED (0):
            The usage of this dataset is not set.
        USAGE_DATA_DRIVEN_STYLING (1):
            This dataset will be used for data driven
            styling.
        USAGE_AREA_AFFORDANCES (2):
            This dataset will be used for area
            affordances in routing.
        USAGE_ASSISTED_DRIVING (3):
            This dataset will be used for assisted
            driving in routing.
    """
    USAGE_UNSPECIFIED = 0
    USAGE_DATA_DRIVEN_STYLING = 1
    USAGE_AREA_AFFORDANCES = 2
    USAGE_ASSISTED_DRIVING = 3


class State(proto.Enum):
    r"""State specifies the status of the import of the latest
    dataset version.

    Values:
        STATE_UNSPECIFIED (0):
            The state of this dataset is not set.
        STATE_IMPORTING (1):
            The dataset version is getting imported.
        STATE_IMPORT_SUCCEEDED (2):
            The dataset version succeeded in getting
            imported.
        STATE_IMPORT_FAILED (3):
            The dataset version failed to get imported.
    """
    STATE_UNSPECIFIED = 0
    STATE_IMPORTING = 1
    STATE_IMPORT_SUCCEEDED = 2
    STATE_IMPORT_FAILED = 3


class Dataset(proto.Message):
    r"""A representation of a maps platform dataset.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Resource name, projects/{project}/datasets/{dataset_id}
        display_name (str):
            Human readable name, shown in the console UI.
            Set by customer.
        description (str):
            A description of this dataset; set by the
            customer.
        version_id (str):
            The version of the dataset.
        usage (MutableSequence[google.maps.mapsplatformdatasets_v1alpha.types.Usage]):
            Specified use case(s) for this dataset.
        local_file_source (google.maps.mapsplatformdatasets_v1alpha.types.LocalFileSource):
            A local file source for the dataset for a
            single upload.

            This field is a member of `oneof`_ ``data_source``.
        gcs_source (google.maps.mapsplatformdatasets_v1alpha.types.GcsSource):
            A Google Cloud Storage file source for the
            dataset for a single upload.

            This field is a member of `oneof`_ ``data_source``.
        status (google.maps.mapsplatformdatasets_v1alpha.types.State):
            The status of the import of the latest
            dataset version.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the dataset was first
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the dataset metadata
            was last updated.
        version_create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this version of
            dataset was created. (It happened when importing
            data to the dataset)
        version_description (str):
            Output only. The description for this version
            of dataset. It is provided when importing data
            to the dataset.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    version_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    usage: MutableSequence["Usage"] = proto.RepeatedField(
        proto.ENUM,
        number=5,
        enum="Usage",
    )
    local_file_source: data_source.LocalFileSource = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="data_source",
        message=data_source.LocalFileSource,
    )
    gcs_source: data_source.GcsSource = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="data_source",
        message=data_source.GcsSource,
    )
    status: "State" = proto.Field(
        proto.ENUM,
        number=12,
        enum="State",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    version_create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    version_description: str = proto.Field(
        proto.STRING,
        number=11,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
