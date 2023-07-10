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
from google.cloud.dataqna_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.auto_suggestion_service import (
    AutoSuggestionServiceAsyncClient,
    AutoSuggestionServiceClient,
)
from .services.question_service import QuestionServiceAsyncClient, QuestionServiceClient
from .types.annotated_string import AnnotatedString
from .types.auto_suggestion_service import (
    Suggestion,
    SuggestionInfo,
    SuggestionType,
    SuggestQueriesRequest,
    SuggestQueriesResponse,
)
from .types.question import (
    BigQueryJob,
    DataQuery,
    DebugFlags,
    ExecutionInfo,
    HumanReadable,
    Interpretation,
    InterpretationStructure,
    InterpretEntity,
    InterpretError,
    Question,
)
from .types.question_service import (
    CreateQuestionRequest,
    ExecuteQuestionRequest,
    GetQuestionRequest,
    GetUserFeedbackRequest,
    UpdateUserFeedbackRequest,
)
from .types.user_feedback import UserFeedback

__all__ = (
    "AutoSuggestionServiceAsyncClient",
    "QuestionServiceAsyncClient",
    "AnnotatedString",
    "AutoSuggestionServiceClient",
    "BigQueryJob",
    "CreateQuestionRequest",
    "DataQuery",
    "DebugFlags",
    "ExecuteQuestionRequest",
    "ExecutionInfo",
    "GetQuestionRequest",
    "GetUserFeedbackRequest",
    "HumanReadable",
    "InterpretEntity",
    "InterpretError",
    "Interpretation",
    "InterpretationStructure",
    "Question",
    "QuestionServiceClient",
    "SuggestQueriesRequest",
    "SuggestQueriesResponse",
    "Suggestion",
    "SuggestionInfo",
    "SuggestionType",
    "UpdateUserFeedbackRequest",
    "UserFeedback",
)
