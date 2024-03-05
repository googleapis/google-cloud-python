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
from google.cloud.video.transcoder import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.video.transcoder_v1.services.transcoder_service.async_client import (
    TranscoderServiceAsyncClient,
)
from google.cloud.video.transcoder_v1.services.transcoder_service.client import (
    TranscoderServiceClient,
)
from google.cloud.video.transcoder_v1.types.resources import (
    AdBreak,
    AudioStream,
    EditAtom,
    ElementaryStream,
    Encryption,
    Input,
    Job,
    JobConfig,
    JobTemplate,
    Manifest,
    MuxStream,
    Output,
    Overlay,
    PreprocessingConfig,
    PubsubDestination,
    SegmentSettings,
    SpriteSheet,
    TextStream,
    VideoStream,
)
from google.cloud.video.transcoder_v1.types.services import (
    CreateJobRequest,
    CreateJobTemplateRequest,
    DeleteJobRequest,
    DeleteJobTemplateRequest,
    GetJobRequest,
    GetJobTemplateRequest,
    ListJobsRequest,
    ListJobsResponse,
    ListJobTemplatesRequest,
    ListJobTemplatesResponse,
)

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
