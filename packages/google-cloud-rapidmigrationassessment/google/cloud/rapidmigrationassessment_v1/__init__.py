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
from google.cloud.rapidmigrationassessment_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.rapid_migration_assessment import (
    RapidMigrationAssessmentAsyncClient,
    RapidMigrationAssessmentClient,
)
from .types.api_entities import Annotation, Collector, GuestOsScan, VSphereScan
from .types.rapidmigrationassessment import (
    CreateAnnotationRequest,
    CreateCollectorRequest,
    DeleteCollectorRequest,
    GetAnnotationRequest,
    GetCollectorRequest,
    ListCollectorsRequest,
    ListCollectorsResponse,
    OperationMetadata,
    PauseCollectorRequest,
    RegisterCollectorRequest,
    ResumeCollectorRequest,
    UpdateCollectorRequest,
)

__all__ = (
    "RapidMigrationAssessmentAsyncClient",
    "Annotation",
    "Collector",
    "CreateAnnotationRequest",
    "CreateCollectorRequest",
    "DeleteCollectorRequest",
    "GetAnnotationRequest",
    "GetCollectorRequest",
    "GuestOsScan",
    "ListCollectorsRequest",
    "ListCollectorsResponse",
    "OperationMetadata",
    "PauseCollectorRequest",
    "RapidMigrationAssessmentClient",
    "RegisterCollectorRequest",
    "ResumeCollectorRequest",
    "UpdateCollectorRequest",
    "VSphereScan",
)
