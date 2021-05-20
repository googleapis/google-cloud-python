# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from .services.transcoder_service import TranscoderServiceClient
from .services.transcoder_service import TranscoderServiceAsyncClient

from .types.resources import AdBreak
from .types.resources import AudioStream
from .types.resources import EditAtom
from .types.resources import ElementaryStream
from .types.resources import Encryption
from .types.resources import FailureDetail
from .types.resources import Input
from .types.resources import Job
from .types.resources import JobConfig
from .types.resources import JobTemplate
from .types.resources import Manifest
from .types.resources import MuxStream
from .types.resources import Output
from .types.resources import Overlay
from .types.resources import PreprocessingConfig
from .types.resources import Progress
from .types.resources import PubsubDestination
from .types.resources import SegmentSettings
from .types.resources import SpriteSheet
from .types.resources import TextStream
from .types.resources import VideoStream
from .types.services import CreateJobRequest
from .types.services import CreateJobTemplateRequest
from .types.services import DeleteJobRequest
from .types.services import DeleteJobTemplateRequest
from .types.services import GetJobRequest
from .types.services import GetJobTemplateRequest
from .types.services import ListJobsRequest
from .types.services import ListJobsResponse
from .types.services import ListJobTemplatesRequest
from .types.services import ListJobTemplatesResponse

__all__ = (
    "TranscoderServiceAsyncClient",
    "AdBreak",
    "AudioStream",
    "CreateJobRequest",
    "CreateJobTemplateRequest",
    "DeleteJobRequest",
    "DeleteJobTemplateRequest",
    "EditAtom",
    "ElementaryStream",
    "Encryption",
    "FailureDetail",
    "GetJobRequest",
    "GetJobTemplateRequest",
    "Input",
    "Job",
    "JobConfig",
    "JobTemplate",
    "ListJobTemplatesRequest",
    "ListJobTemplatesResponse",
    "ListJobsRequest",
    "ListJobsResponse",
    "Manifest",
    "MuxStream",
    "Output",
    "Overlay",
    "PreprocessingConfig",
    "Progress",
    "PubsubDestination",
    "SegmentSettings",
    "SpriteSheet",
    "TextStream",
    "TranscoderServiceClient",
    "VideoStream",
)
