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
from google.cloud.translate_v3 import gapic_version as package_version

__version__ = package_version.__version__


from .services.translation_service import TranslationServiceClient
from .services.translation_service import TranslationServiceAsyncClient

from .types.adaptive_mt import AdaptiveMtDataset
from .types.adaptive_mt import AdaptiveMtFile
from .types.adaptive_mt import AdaptiveMtSentence
from .types.adaptive_mt import AdaptiveMtTranslateRequest
from .types.adaptive_mt import AdaptiveMtTranslateResponse
from .types.adaptive_mt import AdaptiveMtTranslation
from .types.adaptive_mt import CreateAdaptiveMtDatasetRequest
from .types.adaptive_mt import DeleteAdaptiveMtDatasetRequest
from .types.adaptive_mt import DeleteAdaptiveMtFileRequest
from .types.adaptive_mt import GetAdaptiveMtDatasetRequest
from .types.adaptive_mt import GetAdaptiveMtFileRequest
from .types.adaptive_mt import ImportAdaptiveMtFileRequest
from .types.adaptive_mt import ImportAdaptiveMtFileResponse
from .types.adaptive_mt import ListAdaptiveMtDatasetsRequest
from .types.adaptive_mt import ListAdaptiveMtDatasetsResponse
from .types.adaptive_mt import ListAdaptiveMtFilesRequest
from .types.adaptive_mt import ListAdaptiveMtFilesResponse
from .types.adaptive_mt import ListAdaptiveMtSentencesRequest
from .types.adaptive_mt import ListAdaptiveMtSentencesResponse
from .types.automl_translation import BatchTransferResourcesResponse
from .types.automl_translation import CreateDatasetMetadata
from .types.automl_translation import CreateDatasetRequest
from .types.automl_translation import CreateModelMetadata
from .types.automl_translation import CreateModelRequest
from .types.automl_translation import Dataset
from .types.automl_translation import DatasetInputConfig
from .types.automl_translation import DatasetOutputConfig
from .types.automl_translation import DeleteDatasetMetadata
from .types.automl_translation import DeleteDatasetRequest
from .types.automl_translation import DeleteModelMetadata
from .types.automl_translation import DeleteModelRequest
from .types.automl_translation import Example
from .types.automl_translation import ExportDataMetadata
from .types.automl_translation import ExportDataRequest
from .types.automl_translation import GetDatasetRequest
from .types.automl_translation import GetModelRequest
from .types.automl_translation import ImportDataMetadata
from .types.automl_translation import ImportDataRequest
from .types.automl_translation import ListDatasetsRequest
from .types.automl_translation import ListDatasetsResponse
from .types.automl_translation import ListExamplesRequest
from .types.automl_translation import ListExamplesResponse
from .types.automl_translation import ListModelsRequest
from .types.automl_translation import ListModelsResponse
from .types.automl_translation import Model
from .types.common import FileInputSource
from .types.common import GcsInputSource
from .types.common import GcsOutputDestination
from .types.common import GlossaryEntry
from .types.common import GlossaryTerm
from .types.common import OperationState
from .types.translation_service import BatchDocumentInputConfig
from .types.translation_service import BatchDocumentOutputConfig
from .types.translation_service import BatchTranslateDocumentMetadata
from .types.translation_service import BatchTranslateDocumentRequest
from .types.translation_service import BatchTranslateDocumentResponse
from .types.translation_service import BatchTranslateMetadata
from .types.translation_service import BatchTranslateResponse
from .types.translation_service import BatchTranslateTextRequest
from .types.translation_service import CreateGlossaryEntryRequest
from .types.translation_service import CreateGlossaryMetadata
from .types.translation_service import CreateGlossaryRequest
from .types.translation_service import DeleteGlossaryEntryRequest
from .types.translation_service import DeleteGlossaryMetadata
from .types.translation_service import DeleteGlossaryRequest
from .types.translation_service import DeleteGlossaryResponse
from .types.translation_service import DetectedLanguage
from .types.translation_service import DetectLanguageRequest
from .types.translation_service import DetectLanguageResponse
from .types.translation_service import DocumentInputConfig
from .types.translation_service import DocumentOutputConfig
from .types.translation_service import DocumentTranslation
from .types.translation_service import GcsDestination
from .types.translation_service import GcsSource
from .types.translation_service import GetGlossaryEntryRequest
from .types.translation_service import GetGlossaryRequest
from .types.translation_service import GetSupportedLanguagesRequest
from .types.translation_service import Glossary
from .types.translation_service import GlossaryInputConfig
from .types.translation_service import InputConfig
from .types.translation_service import ListGlossariesRequest
from .types.translation_service import ListGlossariesResponse
from .types.translation_service import ListGlossaryEntriesRequest
from .types.translation_service import ListGlossaryEntriesResponse
from .types.translation_service import OutputConfig
from .types.translation_service import Romanization
from .types.translation_service import RomanizeTextRequest
from .types.translation_service import RomanizeTextResponse
from .types.translation_service import SupportedLanguage
from .types.translation_service import SupportedLanguages
from .types.translation_service import TranslateDocumentRequest
from .types.translation_service import TranslateDocumentResponse
from .types.translation_service import TranslateTextGlossaryConfig
from .types.translation_service import TranslateTextRequest
from .types.translation_service import TranslateTextResponse
from .types.translation_service import Translation
from .types.translation_service import TransliterationConfig
from .types.translation_service import UpdateGlossaryEntryRequest
from .types.translation_service import UpdateGlossaryMetadata
from .types.translation_service import UpdateGlossaryRequest

__all__ = (
    'TranslationServiceAsyncClient',
'AdaptiveMtDataset',
'AdaptiveMtFile',
'AdaptiveMtSentence',
'AdaptiveMtTranslateRequest',
'AdaptiveMtTranslateResponse',
'AdaptiveMtTranslation',
'BatchDocumentInputConfig',
'BatchDocumentOutputConfig',
'BatchTransferResourcesResponse',
'BatchTranslateDocumentMetadata',
'BatchTranslateDocumentRequest',
'BatchTranslateDocumentResponse',
'BatchTranslateMetadata',
'BatchTranslateResponse',
'BatchTranslateTextRequest',
'CreateAdaptiveMtDatasetRequest',
'CreateDatasetMetadata',
'CreateDatasetRequest',
'CreateGlossaryEntryRequest',
'CreateGlossaryMetadata',
'CreateGlossaryRequest',
'CreateModelMetadata',
'CreateModelRequest',
'Dataset',
'DatasetInputConfig',
'DatasetOutputConfig',
'DeleteAdaptiveMtDatasetRequest',
'DeleteAdaptiveMtFileRequest',
'DeleteDatasetMetadata',
'DeleteDatasetRequest',
'DeleteGlossaryEntryRequest',
'DeleteGlossaryMetadata',
'DeleteGlossaryRequest',
'DeleteGlossaryResponse',
'DeleteModelMetadata',
'DeleteModelRequest',
'DetectLanguageRequest',
'DetectLanguageResponse',
'DetectedLanguage',
'DocumentInputConfig',
'DocumentOutputConfig',
'DocumentTranslation',
'Example',
'ExportDataMetadata',
'ExportDataRequest',
'FileInputSource',
'GcsDestination',
'GcsInputSource',
'GcsOutputDestination',
'GcsSource',
'GetAdaptiveMtDatasetRequest',
'GetAdaptiveMtFileRequest',
'GetDatasetRequest',
'GetGlossaryEntryRequest',
'GetGlossaryRequest',
'GetModelRequest',
'GetSupportedLanguagesRequest',
'Glossary',
'GlossaryEntry',
'GlossaryInputConfig',
'GlossaryTerm',
'ImportAdaptiveMtFileRequest',
'ImportAdaptiveMtFileResponse',
'ImportDataMetadata',
'ImportDataRequest',
'InputConfig',
'ListAdaptiveMtDatasetsRequest',
'ListAdaptiveMtDatasetsResponse',
'ListAdaptiveMtFilesRequest',
'ListAdaptiveMtFilesResponse',
'ListAdaptiveMtSentencesRequest',
'ListAdaptiveMtSentencesResponse',
'ListDatasetsRequest',
'ListDatasetsResponse',
'ListExamplesRequest',
'ListExamplesResponse',
'ListGlossariesRequest',
'ListGlossariesResponse',
'ListGlossaryEntriesRequest',
'ListGlossaryEntriesResponse',
'ListModelsRequest',
'ListModelsResponse',
'Model',
'OperationState',
'OutputConfig',
'Romanization',
'RomanizeTextRequest',
'RomanizeTextResponse',
'SupportedLanguage',
'SupportedLanguages',
'TranslateDocumentRequest',
'TranslateDocumentResponse',
'TranslateTextGlossaryConfig',
'TranslateTextRequest',
'TranslateTextResponse',
'Translation',
'TranslationServiceClient',
'TransliterationConfig',
'UpdateGlossaryEntryRequest',
'UpdateGlossaryMetadata',
'UpdateGlossaryRequest',
)
