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
from google.cloud.translate import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.translate_v3.services.translation_service.client import TranslationServiceClient
from google.cloud.translate_v3.services.translation_service.async_client import TranslationServiceAsyncClient

from google.cloud.translate_v3.types.adaptive_mt import AdaptiveMtDataset
from google.cloud.translate_v3.types.adaptive_mt import AdaptiveMtFile
from google.cloud.translate_v3.types.adaptive_mt import AdaptiveMtSentence
from google.cloud.translate_v3.types.adaptive_mt import AdaptiveMtTranslateRequest
from google.cloud.translate_v3.types.adaptive_mt import AdaptiveMtTranslateResponse
from google.cloud.translate_v3.types.adaptive_mt import AdaptiveMtTranslation
from google.cloud.translate_v3.types.adaptive_mt import CreateAdaptiveMtDatasetRequest
from google.cloud.translate_v3.types.adaptive_mt import DeleteAdaptiveMtDatasetRequest
from google.cloud.translate_v3.types.adaptive_mt import DeleteAdaptiveMtFileRequest
from google.cloud.translate_v3.types.adaptive_mt import GetAdaptiveMtDatasetRequest
from google.cloud.translate_v3.types.adaptive_mt import GetAdaptiveMtFileRequest
from google.cloud.translate_v3.types.adaptive_mt import ImportAdaptiveMtFileRequest
from google.cloud.translate_v3.types.adaptive_mt import ImportAdaptiveMtFileResponse
from google.cloud.translate_v3.types.adaptive_mt import ListAdaptiveMtDatasetsRequest
from google.cloud.translate_v3.types.adaptive_mt import ListAdaptiveMtDatasetsResponse
from google.cloud.translate_v3.types.adaptive_mt import ListAdaptiveMtFilesRequest
from google.cloud.translate_v3.types.adaptive_mt import ListAdaptiveMtFilesResponse
from google.cloud.translate_v3.types.adaptive_mt import ListAdaptiveMtSentencesRequest
from google.cloud.translate_v3.types.adaptive_mt import ListAdaptiveMtSentencesResponse
from google.cloud.translate_v3.types.automl_translation import BatchTransferResourcesResponse
from google.cloud.translate_v3.types.automl_translation import CreateDatasetMetadata
from google.cloud.translate_v3.types.automl_translation import CreateDatasetRequest
from google.cloud.translate_v3.types.automl_translation import CreateModelMetadata
from google.cloud.translate_v3.types.automl_translation import CreateModelRequest
from google.cloud.translate_v3.types.automl_translation import Dataset
from google.cloud.translate_v3.types.automl_translation import DatasetInputConfig
from google.cloud.translate_v3.types.automl_translation import DatasetOutputConfig
from google.cloud.translate_v3.types.automl_translation import DeleteDatasetMetadata
from google.cloud.translate_v3.types.automl_translation import DeleteDatasetRequest
from google.cloud.translate_v3.types.automl_translation import DeleteModelMetadata
from google.cloud.translate_v3.types.automl_translation import DeleteModelRequest
from google.cloud.translate_v3.types.automl_translation import Example
from google.cloud.translate_v3.types.automl_translation import ExportDataMetadata
from google.cloud.translate_v3.types.automl_translation import ExportDataRequest
from google.cloud.translate_v3.types.automl_translation import GetDatasetRequest
from google.cloud.translate_v3.types.automl_translation import GetModelRequest
from google.cloud.translate_v3.types.automl_translation import ImportDataMetadata
from google.cloud.translate_v3.types.automl_translation import ImportDataRequest
from google.cloud.translate_v3.types.automl_translation import ListDatasetsRequest
from google.cloud.translate_v3.types.automl_translation import ListDatasetsResponse
from google.cloud.translate_v3.types.automl_translation import ListExamplesRequest
from google.cloud.translate_v3.types.automl_translation import ListExamplesResponse
from google.cloud.translate_v3.types.automl_translation import ListModelsRequest
from google.cloud.translate_v3.types.automl_translation import ListModelsResponse
from google.cloud.translate_v3.types.automl_translation import Model
from google.cloud.translate_v3.types.common import FileInputSource
from google.cloud.translate_v3.types.common import GcsInputSource
from google.cloud.translate_v3.types.common import GcsOutputDestination
from google.cloud.translate_v3.types.common import GlossaryEntry
from google.cloud.translate_v3.types.common import GlossaryTerm
from google.cloud.translate_v3.types.common import OperationState
from google.cloud.translate_v3.types.translation_service import BatchDocumentInputConfig
from google.cloud.translate_v3.types.translation_service import BatchDocumentOutputConfig
from google.cloud.translate_v3.types.translation_service import BatchTranslateDocumentMetadata
from google.cloud.translate_v3.types.translation_service import BatchTranslateDocumentRequest
from google.cloud.translate_v3.types.translation_service import BatchTranslateDocumentResponse
from google.cloud.translate_v3.types.translation_service import BatchTranslateMetadata
from google.cloud.translate_v3.types.translation_service import BatchTranslateResponse
from google.cloud.translate_v3.types.translation_service import BatchTranslateTextRequest
from google.cloud.translate_v3.types.translation_service import CreateGlossaryEntryRequest
from google.cloud.translate_v3.types.translation_service import CreateGlossaryMetadata
from google.cloud.translate_v3.types.translation_service import CreateGlossaryRequest
from google.cloud.translate_v3.types.translation_service import DeleteGlossaryEntryRequest
from google.cloud.translate_v3.types.translation_service import DeleteGlossaryMetadata
from google.cloud.translate_v3.types.translation_service import DeleteGlossaryRequest
from google.cloud.translate_v3.types.translation_service import DeleteGlossaryResponse
from google.cloud.translate_v3.types.translation_service import DetectedLanguage
from google.cloud.translate_v3.types.translation_service import DetectLanguageRequest
from google.cloud.translate_v3.types.translation_service import DetectLanguageResponse
from google.cloud.translate_v3.types.translation_service import DocumentInputConfig
from google.cloud.translate_v3.types.translation_service import DocumentOutputConfig
from google.cloud.translate_v3.types.translation_service import DocumentTranslation
from google.cloud.translate_v3.types.translation_service import GcsDestination
from google.cloud.translate_v3.types.translation_service import GcsSource
from google.cloud.translate_v3.types.translation_service import GetGlossaryEntryRequest
from google.cloud.translate_v3.types.translation_service import GetGlossaryRequest
from google.cloud.translate_v3.types.translation_service import GetSupportedLanguagesRequest
from google.cloud.translate_v3.types.translation_service import Glossary
from google.cloud.translate_v3.types.translation_service import GlossaryInputConfig
from google.cloud.translate_v3.types.translation_service import InputConfig
from google.cloud.translate_v3.types.translation_service import ListGlossariesRequest
from google.cloud.translate_v3.types.translation_service import ListGlossariesResponse
from google.cloud.translate_v3.types.translation_service import ListGlossaryEntriesRequest
from google.cloud.translate_v3.types.translation_service import ListGlossaryEntriesResponse
from google.cloud.translate_v3.types.translation_service import OutputConfig
from google.cloud.translate_v3.types.translation_service import Romanization
from google.cloud.translate_v3.types.translation_service import RomanizeTextRequest
from google.cloud.translate_v3.types.translation_service import RomanizeTextResponse
from google.cloud.translate_v3.types.translation_service import SupportedLanguage
from google.cloud.translate_v3.types.translation_service import SupportedLanguages
from google.cloud.translate_v3.types.translation_service import TranslateDocumentRequest
from google.cloud.translate_v3.types.translation_service import TranslateDocumentResponse
from google.cloud.translate_v3.types.translation_service import TranslateTextGlossaryConfig
from google.cloud.translate_v3.types.translation_service import TranslateTextRequest
from google.cloud.translate_v3.types.translation_service import TranslateTextResponse
from google.cloud.translate_v3.types.translation_service import Translation
from google.cloud.translate_v3.types.translation_service import TransliterationConfig
from google.cloud.translate_v3.types.translation_service import UpdateGlossaryEntryRequest
from google.cloud.translate_v3.types.translation_service import UpdateGlossaryMetadata
from google.cloud.translate_v3.types.translation_service import UpdateGlossaryRequest

__all__ = ('TranslationServiceClient',
    'TranslationServiceAsyncClient',
    'AdaptiveMtDataset',
    'AdaptiveMtFile',
    'AdaptiveMtSentence',
    'AdaptiveMtTranslateRequest',
    'AdaptiveMtTranslateResponse',
    'AdaptiveMtTranslation',
    'CreateAdaptiveMtDatasetRequest',
    'DeleteAdaptiveMtDatasetRequest',
    'DeleteAdaptiveMtFileRequest',
    'GetAdaptiveMtDatasetRequest',
    'GetAdaptiveMtFileRequest',
    'ImportAdaptiveMtFileRequest',
    'ImportAdaptiveMtFileResponse',
    'ListAdaptiveMtDatasetsRequest',
    'ListAdaptiveMtDatasetsResponse',
    'ListAdaptiveMtFilesRequest',
    'ListAdaptiveMtFilesResponse',
    'ListAdaptiveMtSentencesRequest',
    'ListAdaptiveMtSentencesResponse',
    'BatchTransferResourcesResponse',
    'CreateDatasetMetadata',
    'CreateDatasetRequest',
    'CreateModelMetadata',
    'CreateModelRequest',
    'Dataset',
    'DatasetInputConfig',
    'DatasetOutputConfig',
    'DeleteDatasetMetadata',
    'DeleteDatasetRequest',
    'DeleteModelMetadata',
    'DeleteModelRequest',
    'Example',
    'ExportDataMetadata',
    'ExportDataRequest',
    'GetDatasetRequest',
    'GetModelRequest',
    'ImportDataMetadata',
    'ImportDataRequest',
    'ListDatasetsRequest',
    'ListDatasetsResponse',
    'ListExamplesRequest',
    'ListExamplesResponse',
    'ListModelsRequest',
    'ListModelsResponse',
    'Model',
    'FileInputSource',
    'GcsInputSource',
    'GcsOutputDestination',
    'GlossaryEntry',
    'GlossaryTerm',
    'OperationState',
    'BatchDocumentInputConfig',
    'BatchDocumentOutputConfig',
    'BatchTranslateDocumentMetadata',
    'BatchTranslateDocumentRequest',
    'BatchTranslateDocumentResponse',
    'BatchTranslateMetadata',
    'BatchTranslateResponse',
    'BatchTranslateTextRequest',
    'CreateGlossaryEntryRequest',
    'CreateGlossaryMetadata',
    'CreateGlossaryRequest',
    'DeleteGlossaryEntryRequest',
    'DeleteGlossaryMetadata',
    'DeleteGlossaryRequest',
    'DeleteGlossaryResponse',
    'DetectedLanguage',
    'DetectLanguageRequest',
    'DetectLanguageResponse',
    'DocumentInputConfig',
    'DocumentOutputConfig',
    'DocumentTranslation',
    'GcsDestination',
    'GcsSource',
    'GetGlossaryEntryRequest',
    'GetGlossaryRequest',
    'GetSupportedLanguagesRequest',
    'Glossary',
    'GlossaryInputConfig',
    'InputConfig',
    'ListGlossariesRequest',
    'ListGlossariesResponse',
    'ListGlossaryEntriesRequest',
    'ListGlossaryEntriesResponse',
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
    'TransliterationConfig',
    'UpdateGlossaryEntryRequest',
    'UpdateGlossaryMetadata',
    'UpdateGlossaryRequest',
)
