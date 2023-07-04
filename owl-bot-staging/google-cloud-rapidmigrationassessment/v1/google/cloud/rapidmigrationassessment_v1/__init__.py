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
from google.cloud.rapidmigrationassessment_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.rapid_migration_assessment import RapidMigrationAssessmentClient
from .services.rapid_migration_assessment import RapidMigrationAssessmentAsyncClient

from .types.api_entities import Annotation
from .types.api_entities import Collector
from .types.api_entities import GuestOsScan
from .types.api_entities import VSphereScan
from .types.rapidmigrationassessment import CreateAnnotationRequest
from .types.rapidmigrationassessment import CreateCollectorRequest
from .types.rapidmigrationassessment import DeleteCollectorRequest
from .types.rapidmigrationassessment import GetAnnotationRequest
from .types.rapidmigrationassessment import GetCollectorRequest
from .types.rapidmigrationassessment import ListCollectorsRequest
from .types.rapidmigrationassessment import ListCollectorsResponse
from .types.rapidmigrationassessment import OperationMetadata
from .types.rapidmigrationassessment import PauseCollectorRequest
from .types.rapidmigrationassessment import RegisterCollectorRequest
from .types.rapidmigrationassessment import ResumeCollectorRequest
from .types.rapidmigrationassessment import UpdateCollectorRequest

__all__ = (
    'RapidMigrationAssessmentAsyncClient',
'Annotation',
'Collector',
'CreateAnnotationRequest',
'CreateCollectorRequest',
'DeleteCollectorRequest',
'GetAnnotationRequest',
'GetCollectorRequest',
'GuestOsScan',
'ListCollectorsRequest',
'ListCollectorsResponse',
'OperationMetadata',
'PauseCollectorRequest',
'RapidMigrationAssessmentClient',
'RegisterCollectorRequest',
'ResumeCollectorRequest',
'UpdateCollectorRequest',
'VSphereScan',
)
