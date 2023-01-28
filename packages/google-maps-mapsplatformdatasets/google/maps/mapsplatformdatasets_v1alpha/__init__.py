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
from google.maps.mapsplatformdatasets_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.maps_platform_datasets_v1_alpha import (
    MapsPlatformDatasetsV1AlphaAsyncClient,
    MapsPlatformDatasetsV1AlphaClient,
)
from .types.data_source import FileFormat, GcsSource, LocalFileSource
from .types.dataset import Dataset, State, Usage
from .types.maps_platform_datasets import (
    CreateDatasetRequest,
    DeleteDatasetRequest,
    DeleteDatasetVersionRequest,
    GetDatasetRequest,
    ListDatasetsRequest,
    ListDatasetsResponse,
    ListDatasetVersionsRequest,
    ListDatasetVersionsResponse,
    UpdateDatasetMetadataRequest,
)

__all__ = (
    "MapsPlatformDatasetsV1AlphaAsyncClient",
    "CreateDatasetRequest",
    "Dataset",
    "DeleteDatasetRequest",
    "DeleteDatasetVersionRequest",
    "FileFormat",
    "GcsSource",
    "GetDatasetRequest",
    "ListDatasetVersionsRequest",
    "ListDatasetVersionsResponse",
    "ListDatasetsRequest",
    "ListDatasetsResponse",
    "LocalFileSource",
    "MapsPlatformDatasetsV1AlphaClient",
    "State",
    "UpdateDatasetMetadataRequest",
    "Usage",
)
