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
from google.cloud.rapidmigrationassessment import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.rapidmigrationassessment_v1.services.rapid_migration_assessment.client import RapidMigrationAssessmentClient
from google.cloud.rapidmigrationassessment_v1.services.rapid_migration_assessment.async_client import RapidMigrationAssessmentAsyncClient

from google.cloud.rapidmigrationassessment_v1.types.api_entities import Annotation
from google.cloud.rapidmigrationassessment_v1.types.api_entities import Collector
from google.cloud.rapidmigrationassessment_v1.types.api_entities import GuestOsScan
from google.cloud.rapidmigrationassessment_v1.types.api_entities import VSphereScan
from google.cloud.rapidmigrationassessment_v1.types.rapidmigrationassessment import CreateAnnotationRequest
from google.cloud.rapidmigrationassessment_v1.types.rapidmigrationassessment import CreateCollectorRequest
from google.cloud.rapidmigrationassessment_v1.types.rapidmigrationassessment import DeleteCollectorRequest
from google.cloud.rapidmigrationassessment_v1.types.rapidmigrationassessment import GetAnnotationRequest
from google.cloud.rapidmigrationassessment_v1.types.rapidmigrationassessment import GetCollectorRequest
from google.cloud.rapidmigrationassessment_v1.types.rapidmigrationassessment import ListCollectorsRequest
from google.cloud.rapidmigrationassessment_v1.types.rapidmigrationassessment import ListCollectorsResponse
from google.cloud.rapidmigrationassessment_v1.types.rapidmigrationassessment import OperationMetadata
from google.cloud.rapidmigrationassessment_v1.types.rapidmigrationassessment import PauseCollectorRequest
from google.cloud.rapidmigrationassessment_v1.types.rapidmigrationassessment import RegisterCollectorRequest
from google.cloud.rapidmigrationassessment_v1.types.rapidmigrationassessment import ResumeCollectorRequest
from google.cloud.rapidmigrationassessment_v1.types.rapidmigrationassessment import UpdateCollectorRequest

__all__ = ('RapidMigrationAssessmentClient',
    'RapidMigrationAssessmentAsyncClient',
    'Annotation',
    'Collector',
    'GuestOsScan',
    'VSphereScan',
    'CreateAnnotationRequest',
    'CreateCollectorRequest',
    'DeleteCollectorRequest',
    'GetAnnotationRequest',
    'GetCollectorRequest',
    'ListCollectorsRequest',
    'ListCollectorsResponse',
    'OperationMetadata',
    'PauseCollectorRequest',
    'RegisterCollectorRequest',
    'ResumeCollectorRequest',
    'UpdateCollectorRequest',
)
