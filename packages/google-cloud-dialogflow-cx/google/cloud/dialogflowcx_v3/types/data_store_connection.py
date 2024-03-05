# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3",
    manifest={
        "DataStoreType",
        "DataStoreConnection",
    },
)


class DataStoreType(proto.Enum):
    r"""Type of a data store.
    Determines how search is performed in the data store.

    Values:
        DATA_STORE_TYPE_UNSPECIFIED (0):
            Not specified. This value indicates that the
            data store type is not specified, so it will not
            be used during search.
        PUBLIC_WEB (1):
            A data store that contains public web
            content.
        UNSTRUCTURED (2):
            A data store that contains unstructured
            private data.
        STRUCTURED (3):
            A data store that contains structured data
            (for example FAQ).
    """
    DATA_STORE_TYPE_UNSPECIFIED = 0
    PUBLIC_WEB = 1
    UNSTRUCTURED = 2
    STRUCTURED = 3


class DataStoreConnection(proto.Message):
    r"""A data store connection. It represents a data store in
    Discovery Engine and the type of the contents it contains.

    Attributes:
        data_store_type (google.cloud.dialogflowcx_v3.types.DataStoreType):
            The type of the connected data store.
        data_store (str):
            The full name of the referenced data store. Formats:
            ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}``
            ``projects/{project}/locations/{location}/dataStores/{data_store}``
    """

    data_store_type: "DataStoreType" = proto.Field(
        proto.ENUM,
        number=1,
        enum="DataStoreType",
    )
    data_store: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
