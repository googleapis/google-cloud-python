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

from google.cloud.video.transcoder_v1.services.transcoder_service.client import (
    TranscoderServiceClient,
)
from google.cloud.video.transcoder_v1.services.transcoder_service.async_client import (
    TranscoderServiceAsyncClient,
)

from google.cloud.video.transcoder_v1.types.resources import AdBreak
from google.cloud.video.transcoder_v1.types.resources import AudioStream
from google.cloud.video.transcoder_v1.types.resources import EditAtom
from google.cloud.video.transcoder_v1.types.resources import ElementaryStream
from google.cloud.video.transcoder_v1.types.resources import Encryption
from google.cloud.video.transcoder_v1.types.resources import Input
from google.cloud.video.transcoder_v1.types.resources import Job
from google.cloud.video.transcoder_v1.types.resources import JobConfig
from google.cloud.video.transcoder_v1.types.resources import JobTemplate
from google.cloud.video.transcoder_v1.types.resources import Manifest
from google.cloud.video.transcoder_v1.types.resources import MuxStream
from google.cloud.video.transcoder_v1.types.resources import Output
from google.cloud.video.transcoder_v1.types.resources import Overlay
from google.cloud.video.transcoder_v1.types.resources import PreprocessingConfig
from google.cloud.video.transcoder_v1.types.resources import PubsubDestination
from google.cloud.video.transcoder_v1.types.resources import SegmentSettings
from google.cloud.video.transcoder_v1.types.resources import SpriteSheet
from google.cloud.video.transcoder_v1.types.resources import TextStream
from google.cloud.video.transcoder_v1.types.resources import VideoStream
from google.cloud.video.transcoder_v1.types.services import CreateJobRequest
from google.cloud.video.transcoder_v1.types.services import CreateJobTemplateRequest
from google.cloud.video.transcoder_v1.types.services import DeleteJobRequest
from google.cloud.video.transcoder_v1.types.services import DeleteJobTemplateRequest
from google.cloud.video.transcoder_v1.types.services import GetJobRequest
from google.cloud.video.transcoder_v1.types.services import GetJobTemplateRequest
from google.cloud.video.transcoder_v1.types.services import ListJobsRequest
from google.cloud.video.transcoder_v1.types.services import ListJobsResponse
from google.cloud.video.transcoder_v1.types.services import ListJobTemplatesRequest
from google.cloud.video.transcoder_v1.types.services import ListJobTemplatesResponse

__all__ = (
    "TranscoderServiceClient",
    "TranscoderServiceAsyncClient",
    "AdBreak",
    "AudioStream",
    "EditAtom",
    "ElementaryStream",
    "Encryption",
    "Input",
    "Job",
    "JobConfig",
    "JobTemplate",
    "Manifest",
    "MuxStream",
    "Output",
    "Overlay",
    "PreprocessingConfig",
    "PubsubDestination",
    "SegmentSettings",
    "SpriteSheet",
    "TextStream",
    "VideoStream",
    "CreateJobRequest",
    "CreateJobTemplateRequest",
    "DeleteJobRequest",
    "DeleteJobTemplateRequest",
    "GetJobRequest",
    "GetJobTemplateRequest",
    "ListJobsRequest",
    "ListJobsResponse",
    "ListJobTemplatesRequest",
    "ListJobTemplatesResponse",
)
