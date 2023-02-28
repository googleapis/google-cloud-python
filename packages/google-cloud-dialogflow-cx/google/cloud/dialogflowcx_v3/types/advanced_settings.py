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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.cloud.dialogflowcx_v3.types import gcs


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3",
    manifest={
        "AdvancedSettings",
    },
)


class AdvancedSettings(proto.Message):
    r"""Hierarchical advanced settings for
    agent/flow/page/fulfillment/parameter. Settings exposed at lower
    level overrides the settings exposed at higher level. Overriding
    occurs at the sub-setting level. For example, the
    playback_interruption_settings at fulfillment level only overrides
    the playback_interruption_settings at the agent level, leaving other
    settings at the agent level unchanged.

    DTMF settings does not override each other. DTMF settings set at
    different levels define DTMF detections running in parallel.

    Hierarchy: Agent->Flow->Page->Fulfillment/Parameter.

    Attributes:
        audio_export_gcs_destination (google.cloud.dialogflowcx_v3.types.GcsDestination):
            If present, incoming audio is exported by
            Dialogflow to the configured Google Cloud
            Storage destination. Exposed at the following
            levels:
            - Agent level
            - Flow level
        logging_settings (google.cloud.dialogflowcx_v3.types.AdvancedSettings.LoggingSettings):
            Settings for logging.
            Settings for Dialogflow History, Contact Center
            messages, StackDriver logs, and speech logging.
            Exposed at the following levels:
            - Agent level.
    """

    class LoggingSettings(proto.Message):
        r"""Define behaviors on logging.

        Attributes:
            enable_stackdriver_logging (bool):
                If true, StackDriver logging is currently
                enabled.
            enable_interaction_logging (bool):
                If true, DF Interaction logging is currently
                enabled.
        """

        enable_stackdriver_logging: bool = proto.Field(
            proto.BOOL,
            number=2,
        )
        enable_interaction_logging: bool = proto.Field(
            proto.BOOL,
            number=3,
        )

    audio_export_gcs_destination: gcs.GcsDestination = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcs.GcsDestination,
    )
    logging_settings: LoggingSettings = proto.Field(
        proto.MESSAGE,
        number=6,
        message=LoggingSettings,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
