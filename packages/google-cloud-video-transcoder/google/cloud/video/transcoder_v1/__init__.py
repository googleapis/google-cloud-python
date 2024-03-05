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
from google.cloud.video.transcoder_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.transcoder_service import (
    TranscoderServiceAsyncClient,
    TranscoderServiceClient,
)
from .types.resources import (
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
from .types.services import (
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
    "PubsubDestination",
    "SegmentSettings",
    "SpriteSheet",
    "TextStream",
    "TranscoderServiceClient",
    "VideoStream",
)
