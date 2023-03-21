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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.video.live_stream_v1.types import outputs

__protobuf__ = proto.module(
    package="google.cloud.video.livestream.v1",
    manifest={
        "Input",
        "Channel",
        "InputConfig",
        "LogConfig",
        "InputStreamProperty",
        "VideoStreamProperty",
        "VideoFormat",
        "AudioStreamProperty",
        "AudioFormat",
        "InputAttachment",
        "Event",
        "Encryption",
    },
)


class Input(proto.Message):
    r"""Input resource represents the endpoint from which the channel
    ingests the input stream.

    Attributes:
        name (str):
            The resource name of the input, in the form of:
            ``projects/{project}/locations/{location}/inputs/{inputId}``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The update time.
        labels (MutableMapping[str, str]):
            User-defined key/value metadata.
        type_ (google.cloud.video.live_stream_v1.types.Input.Type):
            Source type.
        tier (google.cloud.video.live_stream_v1.types.Input.Tier):
            Tier defines the maximum input specification that is
            accepted by the video pipeline. The billing is charged based
            on the tier specified here. See
            `Pricing <https://cloud.google.com/livestream/pricing>`__
            for more detail. The default is ``HD``.
        uri (str):
            Output only. URI to push the input stream to. Its format
            depends on the input
            [type][google.cloud.video.livestream.v1.Input.type], for
            example:

            -  ``RTMP_PUSH``: ``rtmp://1.2.3.4/live/{STREAM-ID}``
            -  ``SRT_PUSH``: ``srt://1.2.3.4:4201?streamid={STREAM-ID}``
        preprocessing_config (google.cloud.video.live_stream_v1.types.PreprocessingConfig):
            Preprocessing configurations.
        security_rules (google.cloud.video.live_stream_v1.types.Input.SecurityRule):
            Security rule for access control.
        input_stream_property (google.cloud.video.live_stream_v1.types.InputStreamProperty):
            Output only. The information for the input
            stream. This field will be present only when
            this input receives the input stream.
    """

    class Type(proto.Enum):
        r"""The type of the input.

        Values:
            TYPE_UNSPECIFIED (0):
                Input type is not specified.
            RTMP_PUSH (1):
                Input will take an rtmp input stream.
            SRT_PUSH (2):
                Input will take an srt (Secure Reliable
                Transport) input stream.
        """
        TYPE_UNSPECIFIED = 0
        RTMP_PUSH = 1
        SRT_PUSH = 2

    class Tier(proto.Enum):
        r"""Tier of the input specification.

        Values:
            TIER_UNSPECIFIED (0):
                Tier is not specified.
            SD (1):
                Resolution < 1280x720. Bitrate <= 6 Mbps. FPS
                <= 60.
            HD (2):
                Resolution <= 1920x1080. Bitrate <= 25 Mbps.
                FPS <= 60.
            UHD (3):
                Resolution <= 4096x2160. Not supported yet.
        """
        TIER_UNSPECIFIED = 0
        SD = 1
        HD = 2
        UHD = 3

    class SecurityRule(proto.Message):
        r"""Security rules for access control. Each field represents one
        security rule. Only when the source of the input stream
        satisfies all the fields, this input stream can be accepted.

        Attributes:
            ip_ranges (MutableSequence[str]):
                At least one ip range must match unless none specified. The
                IP range is defined by CIDR block: for example,
                ``192.0.1.0/24`` for a range and ``192.0.1.0/32`` for a
                single IP address.
        """

        ip_ranges: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=5,
        enum=Type,
    )
    tier: Tier = proto.Field(
        proto.ENUM,
        number=14,
        enum=Tier,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=6,
    )
    preprocessing_config: outputs.PreprocessingConfig = proto.Field(
        proto.MESSAGE,
        number=9,
        message=outputs.PreprocessingConfig,
    )
    security_rules: SecurityRule = proto.Field(
        proto.MESSAGE,
        number=12,
        message=SecurityRule,
    )
    input_stream_property: "InputStreamProperty" = proto.Field(
        proto.MESSAGE,
        number=15,
        message="InputStreamProperty",
    )


class Channel(proto.Message):
    r"""Channel resource represents the processor that does a
    user-defined "streaming" operation, which includes getting an
    input stream through an input, transcoding it to multiple
    renditions, and publishing output live streams in certain
    formats (for example, HLS or DASH) to the specified location.

    Attributes:
        name (str):
            The resource name of the channel, in the form of:
            ``projects/{project}/locations/{location}/channels/{channelId}``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The update time.
        labels (MutableMapping[str, str]):
            User-defined key/value metadata.
        input_attachments (MutableSequence[google.cloud.video.live_stream_v1.types.InputAttachment]):
            A list of input attachments that this channel
            uses. One channel can have multiple inputs as
            the input sources. Only one input can be
            selected as the input source at one time.
        active_input (str):
            Output only. The
            [InputAttachment.key][google.cloud.video.livestream.v1.InputAttachment.key]
            that serves as the current input source. The first input in
            the
            [input_attachments][google.cloud.video.livestream.v1.Channel.input_attachments]
            is the initial input source.
        output (google.cloud.video.live_stream_v1.types.Channel.Output):
            Required. Information about the output (that
            is, the Cloud Storage bucket to store the
            generated live stream).
        elementary_streams (MutableSequence[google.cloud.video.live_stream_v1.types.ElementaryStream]):
            List of elementary streams.
        mux_streams (MutableSequence[google.cloud.video.live_stream_v1.types.MuxStream]):
            List of multiplexing settings for output
            streams.
        manifests (MutableSequence[google.cloud.video.live_stream_v1.types.Manifest]):
            List of output manifests.
        sprite_sheets (MutableSequence[google.cloud.video.live_stream_v1.types.SpriteSheet]):
            List of output sprite sheets.
        streaming_state (google.cloud.video.live_stream_v1.types.Channel.StreamingState):
            Output only. State of the streaming
            operation.
        streaming_error (google.rpc.status_pb2.Status):
            Output only. A description of the reason for the streaming
            error. This property is always present when
            [streaming_state][google.cloud.video.livestream.v1.Channel.streaming_state]
            is
            [STREAMING_ERROR][google.cloud.video.livestream.v1.Channel.StreamingState.STREAMING_ERROR].
        log_config (google.cloud.video.live_stream_v1.types.LogConfig):
            Configuration of platform logs for this
            channel.
        timecode_config (google.cloud.video.live_stream_v1.types.TimecodeConfig):
            Configuration of timecode for this channel.
        encryptions (MutableSequence[google.cloud.video.live_stream_v1.types.Encryption]):
            Encryption configurations for this channel.
            Each configuration has an ID which is referred
            to by each MuxStream to indicate which
            configuration is used for that output.
        input_config (google.cloud.video.live_stream_v1.types.InputConfig):
            The configuration for input sources defined in
            [input_attachments][google.cloud.video.livestream.v1.Channel.input_attachments].
    """

    class StreamingState(proto.Enum):
        r"""State of streaming operation that the channel is running.

        Values:
            STREAMING_STATE_UNSPECIFIED (0):
                Streaming state is not specified.
            STREAMING (1):
                Channel is getting the input stream,
                generating the live streams to the specified
                output location.
            AWAITING_INPUT (2):
                Channel is waiting for the input stream
                through the input.
            STREAMING_ERROR (4):
                Channel is running, but has trouble
                publishing the live streams onto the specified
                output location (for example, the specified
                Cloud Storage bucket is not writable).
            STREAMING_NO_INPUT (5):
                Channel is generating live streams with no
                input stream. Live streams are filled out with
                black screen, while input stream is missing. Not
                supported yet.
            STOPPED (6):
                Channel is stopped, finishing live streams.
            STARTING (7):
                Channel is starting.
            STOPPING (8):
                Channel is stopping.
        """
        STREAMING_STATE_UNSPECIFIED = 0
        STREAMING = 1
        AWAITING_INPUT = 2
        STREAMING_ERROR = 4
        STREAMING_NO_INPUT = 5
        STOPPED = 6
        STARTING = 7
        STOPPING = 8

    class Output(proto.Message):
        r"""Location of output file(s) in a Google Cloud Storage bucket.

        Attributes:
            uri (str):
                URI for the output file(s). For example,
                ``gs://my-bucket/outputs/``.
        """

        uri: str = proto.Field(
            proto.STRING,
            number=1,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    input_attachments: MutableSequence["InputAttachment"] = proto.RepeatedField(
        proto.MESSAGE,
        number=16,
        message="InputAttachment",
    )
    active_input: str = proto.Field(
        proto.STRING,
        number=6,
    )
    output: Output = proto.Field(
        proto.MESSAGE,
        number=9,
        message=Output,
    )
    elementary_streams: MutableSequence[outputs.ElementaryStream] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message=outputs.ElementaryStream,
    )
    mux_streams: MutableSequence[outputs.MuxStream] = proto.RepeatedField(
        proto.MESSAGE,
        number=11,
        message=outputs.MuxStream,
    )
    manifests: MutableSequence[outputs.Manifest] = proto.RepeatedField(
        proto.MESSAGE,
        number=12,
        message=outputs.Manifest,
    )
    sprite_sheets: MutableSequence[outputs.SpriteSheet] = proto.RepeatedField(
        proto.MESSAGE,
        number=13,
        message=outputs.SpriteSheet,
    )
    streaming_state: StreamingState = proto.Field(
        proto.ENUM,
        number=14,
        enum=StreamingState,
    )
    streaming_error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=18,
        message=status_pb2.Status,
    )
    log_config: "LogConfig" = proto.Field(
        proto.MESSAGE,
        number=19,
        message="LogConfig",
    )
    timecode_config: outputs.TimecodeConfig = proto.Field(
        proto.MESSAGE,
        number=21,
        message=outputs.TimecodeConfig,
    )
    encryptions: MutableSequence["Encryption"] = proto.RepeatedField(
        proto.MESSAGE,
        number=24,
        message="Encryption",
    )
    input_config: "InputConfig" = proto.Field(
        proto.MESSAGE,
        number=25,
        message="InputConfig",
    )


class InputConfig(proto.Message):
    r"""Configuration for the input sources of a channel.

    Attributes:
        input_switch_mode (google.cloud.video.live_stream_v1.types.InputConfig.InputSwitchMode):
            Input switch mode. Default mode is
            ``FAILOVER_PREFER_PRIMARY``.
    """

    class InputSwitchMode(proto.Enum):
        r"""Input switch mode.

        Values:
            INPUT_SWITCH_MODE_UNSPECIFIED (0):
                The input switch mode is not specified.
            FAILOVER_PREFER_PRIMARY (1):
                Automatic failover is enabled. The primary input stream is
                always preferred over its backup input streams configured
                using the
                [AutomaticFailover][google.cloud.video.livestream.v1.InputAttachment.AutomaticFailover]
                field.
            MANUAL (3):
                Automatic failover is disabled. You must use the
                [inputSwitch][google.cloud.video.livestream.v1.Event.input_switch]
                event to switch the active input source for the channel to
                stream from. When this mode is chosen, the
                [AutomaticFailover][google.cloud.video.livestream.v1.InputAttachment.AutomaticFailover]
                field is ignored.
        """
        INPUT_SWITCH_MODE_UNSPECIFIED = 0
        FAILOVER_PREFER_PRIMARY = 1
        MANUAL = 3

    input_switch_mode: InputSwitchMode = proto.Field(
        proto.ENUM,
        number=1,
        enum=InputSwitchMode,
    )


class LogConfig(proto.Message):
    r"""Configuration of platform logs. See `Using and managing platform
    logs <https://cloud.google.com/logging/docs/api/platform-logs#managing-logs>`__
    for more information about how to view platform logs through Cloud
    Logging.

    Attributes:
        log_severity (google.cloud.video.live_stream_v1.types.LogConfig.LogSeverity):
            The severity level of platform logging for
            this resource.
    """

    class LogSeverity(proto.Enum):
        r"""The severity level of platform logging for this channel. Logs with a
        severity level higher than or equal to the chosen severity level
        will be logged and can be viewed through Cloud Logging. The severity
        level of a log is ranked as followed from low to high: DEBUG < INFO
        < NOTICE < WARNING < ERROR < CRITICAL < ALERT < EMERGENCY. See
        `LogSeverity <https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry#logseverity>`__
        for more information.

        Values:
            LOG_SEVERITY_UNSPECIFIED (0):
                Log severity is not specified. This is the
                same as log severity is OFF.
            OFF (1):
                Log is turned off.
            DEBUG (100):
                Log with severity higher than or equal to
                DEBUG are logged.
            INFO (200):
                Logs with severity higher than or equal to
                INFO are logged.
            WARNING (400):
                Logs with severity higher than or equal to
                WARNING are logged.
            ERROR (500):
                Logs with severity higher than or equal to
                ERROR are logged.
        """
        LOG_SEVERITY_UNSPECIFIED = 0
        OFF = 1
        DEBUG = 100
        INFO = 200
        WARNING = 400
        ERROR = 500

    log_severity: LogSeverity = proto.Field(
        proto.ENUM,
        number=1,
        enum=LogSeverity,
    )


class InputStreamProperty(proto.Message):
    r"""Properties of the input stream.

    Attributes:
        last_establish_time (google.protobuf.timestamp_pb2.Timestamp):
            The time that the current input stream is
            accepted and the connection is established.
        video_streams (MutableSequence[google.cloud.video.live_stream_v1.types.VideoStreamProperty]):
            Properties of the video streams.
        audio_streams (MutableSequence[google.cloud.video.live_stream_v1.types.AudioStreamProperty]):
            Properties of the audio streams.
    """

    last_establish_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    video_streams: MutableSequence["VideoStreamProperty"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="VideoStreamProperty",
    )
    audio_streams: MutableSequence["AudioStreamProperty"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="AudioStreamProperty",
    )


class VideoStreamProperty(proto.Message):
    r"""Properties of the video stream.

    Attributes:
        index (int):
            Index of this video stream.
        video_format (google.cloud.video.live_stream_v1.types.VideoFormat):
            Properties of the video format.
    """

    index: int = proto.Field(
        proto.INT32,
        number=1,
    )
    video_format: "VideoFormat" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="VideoFormat",
    )


class VideoFormat(proto.Message):
    r"""Properties of the video format.

    Attributes:
        codec (str):
            Video codec used in this video stream.
        width_pixels (int):
            The width of the video stream in pixels.
        height_pixels (int):
            The height of the video stream in pixels.
        frame_rate (float):
            The frame rate of the input video stream.
    """

    codec: str = proto.Field(
        proto.STRING,
        number=1,
    )
    width_pixels: int = proto.Field(
        proto.INT32,
        number=2,
    )
    height_pixels: int = proto.Field(
        proto.INT32,
        number=3,
    )
    frame_rate: float = proto.Field(
        proto.DOUBLE,
        number=4,
    )


class AudioStreamProperty(proto.Message):
    r"""Properties of the audio stream.

    Attributes:
        index (int):
            Index of this audio stream.
        audio_format (google.cloud.video.live_stream_v1.types.AudioFormat):
            Properties of the audio format.
    """

    index: int = proto.Field(
        proto.INT32,
        number=1,
    )
    audio_format: "AudioFormat" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="AudioFormat",
    )


class AudioFormat(proto.Message):
    r"""Properties of the audio format.

    Attributes:
        codec (str):
            Audio codec used in this audio stream.
        channel_count (int):
            The number of audio channels.
        channel_layout (MutableSequence[str]):
            A list of channel names specifying the layout
            of the audio channels.
    """

    codec: str = proto.Field(
        proto.STRING,
        number=1,
    )
    channel_count: int = proto.Field(
        proto.INT32,
        number=2,
    )
    channel_layout: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class InputAttachment(proto.Message):
    r"""A group of information for attaching an input resource to
    this channel.

    Attributes:
        key (str):
            A unique key for this input attachment.
        input (str):
            The resource name of an existing input, in the form of:
            ``projects/{project}/locations/{location}/inputs/{inputId}``.
        automatic_failover (google.cloud.video.live_stream_v1.types.InputAttachment.AutomaticFailover):
            Automatic failover configurations.
    """

    class AutomaticFailover(proto.Message):
        r"""Configurations to follow when automatic failover happens.

        Attributes:
            input_keys (MutableSequence[str]):
                The
                [InputAttachment.key][google.cloud.video.livestream.v1.InputAttachment.key]s
                of inputs to failover to when this input is disconnected.
                Currently, only up to one backup input is supported.
        """

        input_keys: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    input: str = proto.Field(
        proto.STRING,
        number=2,
    )
    automatic_failover: AutomaticFailover = proto.Field(
        proto.MESSAGE,
        number=3,
        message=AutomaticFailover,
    )


class Event(proto.Message):
    r"""Event is a sub-resource of a channel, which can be scheduled
    by the user to execute operations on a channel resource without
    having to stop the channel.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            The resource name of the event, in the form of:
            ``projects/{project}/locations/{location}/channels/{channelId}/events/{eventId}``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The update time.
        labels (MutableMapping[str, str]):
            User-defined key/value metadata.
        input_switch (google.cloud.video.live_stream_v1.types.Event.InputSwitchTask):
            Required. Switches to another input stream.

            This field is a member of `oneof`_ ``task``.
        ad_break (google.cloud.video.live_stream_v1.types.Event.AdBreakTask):
            Required. Inserts a new ad opportunity.

            This field is a member of `oneof`_ ``task``.
        return_to_program (google.cloud.video.live_stream_v1.types.Event.ReturnToProgramTask):
            Required. Stops any running ad break.

            This field is a member of `oneof`_ ``task``.
        mute (google.cloud.video.live_stream_v1.types.Event.MuteTask):
            Required. Mutes the stream.

            This field is a member of `oneof`_ ``task``.
        unmute (google.cloud.video.live_stream_v1.types.Event.UnmuteTask):
            Required. Unmutes the stream.

            This field is a member of `oneof`_ ``task``.
        execute_now (bool):
            When this field is set to true, the event will be executed
            at the earliest time that the server can schedule the event
            and
            [execution_time][google.cloud.video.livestream.v1.Event.execution_time]
            will be populated with the time that the server actually
            schedules the event.
        execution_time (google.protobuf.timestamp_pb2.Timestamp):
            The time to execute the event. If you set
            [execute_now][google.cloud.video.livestream.v1.Event.execute_now]
            to ``true``, then do not set this field in the
            ``CreateEvent`` request. In this case, the server schedules
            the event and populates this field. If you set
            [execute_now][google.cloud.video.livestream.v1.Event.execute_now]
            to ``false``, then you must set this field to at least 10
            seconds in the future or else the event can't be created.
        state (google.cloud.video.live_stream_v1.types.Event.State):
            Output only. The state of the event.
        error (google.rpc.status_pb2.Status):
            Output only. An error object that describes the reason for
            the failure. This property is always present when ``state``
            is ``FAILED``.
    """

    class State(proto.Enum):
        r"""State of the event

        Values:
            STATE_UNSPECIFIED (0):
                Event state is not specified.
            SCHEDULED (1):
                Event is scheduled but not executed yet.
            RUNNING (2):
                Event is being executed.
            SUCCEEDED (3):
                Event has been successfully executed.
            FAILED (4):
                Event fails to be executed.
            PENDING (5):
                Event has been created but not scheduled yet.
            STOPPED (6):
                Event was stopped before running for its full
                duration.
        """
        STATE_UNSPECIFIED = 0
        SCHEDULED = 1
        RUNNING = 2
        SUCCEEDED = 3
        FAILED = 4
        PENDING = 5
        STOPPED = 6

    class InputSwitchTask(proto.Message):
        r"""Switches to another input stream. Automatic failover is then
        disabled.

        Attributes:
            input_key (str):
                The
                [InputAttachment.key][google.cloud.video.livestream.v1.InputAttachment.key]
                of the input to switch to.
        """

        input_key: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class AdBreakTask(proto.Message):
        r"""Inserts a new ad opportunity.

        Attributes:
            duration (google.protobuf.duration_pb2.Duration):
                Duration of an ad opportunity. Must be
                greater than 0.
        """

        duration: duration_pb2.Duration = proto.Field(
            proto.MESSAGE,
            number=1,
            message=duration_pb2.Duration,
        )

    class ReturnToProgramTask(proto.Message):
        r"""Stops any events which are currently running. This only
        applies to events with a duration.

        """

    class MuteTask(proto.Message):
        r"""Mutes the stream.

        Attributes:
            duration (google.protobuf.duration_pb2.Duration):
                Duration for which the stream should be
                muted. If omitted, the stream will be muted
                until an UnmuteTask event is sent.
        """

        duration: duration_pb2.Duration = proto.Field(
            proto.MESSAGE,
            number=1,
            message=duration_pb2.Duration,
        )

    class UnmuteTask(proto.Message):
        r"""Unmutes the stream. The task will fail if the stream is not
        currently muted.

        """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    input_switch: InputSwitchTask = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="task",
        message=InputSwitchTask,
    )
    ad_break: AdBreakTask = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="task",
        message=AdBreakTask,
    )
    return_to_program: ReturnToProgramTask = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof="task",
        message=ReturnToProgramTask,
    )
    mute: MuteTask = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="task",
        message=MuteTask,
    )
    unmute: UnmuteTask = proto.Field(
        proto.MESSAGE,
        number=16,
        oneof="task",
        message=UnmuteTask,
    )
    execute_now: bool = proto.Field(
        proto.BOOL,
        number=9,
    )
    execution_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=11,
        enum=State,
    )
    error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=12,
        message=status_pb2.Status,
    )


class Encryption(proto.Message):
    r"""Encryption settings.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        id (str):
            Required. Identifier for this set of
            encryption options.
        secret_manager_key_source (google.cloud.video.live_stream_v1.types.Encryption.SecretManagerSource):
            For keys stored in Google Secret Manager.

            This field is a member of `oneof`_ ``secret_source``.
        drm_systems (google.cloud.video.live_stream_v1.types.Encryption.DrmSystems):
            Required. Configuration for DRM systems.
        aes128 (google.cloud.video.live_stream_v1.types.Encryption.Aes128Encryption):
            Configuration for HLS AES-128 encryption.

            This field is a member of `oneof`_ ``encryption_mode``.
        sample_aes (google.cloud.video.live_stream_v1.types.Encryption.SampleAesEncryption):
            Configuration for HLS SAMPLE-AES encryption.

            This field is a member of `oneof`_ ``encryption_mode``.
        mpeg_cenc (google.cloud.video.live_stream_v1.types.Encryption.MpegCommonEncryption):
            Configuration for MPEG-Dash Common Encryption
            (MPEG-CENC).

            This field is a member of `oneof`_ ``encryption_mode``.
    """

    class SecretManagerSource(proto.Message):
        r"""Configuration for secrets stored in Google Secret Manager.

        Attributes:
            secret_version (str):
                Required. The name of the Secret Version containing the
                encryption key.
                ``projects/{project}/secrets/{secret_id}/versions/{version_number}``
        """

        secret_version: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class Widevine(proto.Message):
        r"""Widevine configuration."""

    class Fairplay(proto.Message):
        r"""Fairplay configuration."""

    class Playready(proto.Message):
        r"""Playready configuration."""

    class Clearkey(proto.Message):
        r"""Clearkey configuration."""

    class DrmSystems(proto.Message):
        r"""Defines configuration for DRM systems in use. If a field is
        omitted, that DRM system will be considered to be disabled.

        Attributes:
            widevine (google.cloud.video.live_stream_v1.types.Encryption.Widevine):
                Widevine configuration.
            fairplay (google.cloud.video.live_stream_v1.types.Encryption.Fairplay):
                Fairplay configuration.
            playready (google.cloud.video.live_stream_v1.types.Encryption.Playready):
                Playready configuration.
            clearkey (google.cloud.video.live_stream_v1.types.Encryption.Clearkey):
                Clearkey configuration.
        """

        widevine: "Encryption.Widevine" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Encryption.Widevine",
        )
        fairplay: "Encryption.Fairplay" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="Encryption.Fairplay",
        )
        playready: "Encryption.Playready" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="Encryption.Playready",
        )
        clearkey: "Encryption.Clearkey" = proto.Field(
            proto.MESSAGE,
            number=4,
            message="Encryption.Clearkey",
        )

    class Aes128Encryption(proto.Message):
        r"""Configuration for HLS AES-128 encryption."""

    class SampleAesEncryption(proto.Message):
        r"""Configuration for HLS SAMPLE-AES encryption."""

    class MpegCommonEncryption(proto.Message):
        r"""Configuration for MPEG-Dash Common Encryption (MPEG-CENC).

        Attributes:
            scheme (str):
                Required. Specify the encryption scheme, supported schemes:

                -  ``cenc`` - AES-CTR subsample
                -  ``cbcs``- AES-CBC subsample pattern
        """

        scheme: str = proto.Field(
            proto.STRING,
            number=1,
        )

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    secret_manager_key_source: SecretManagerSource = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="secret_source",
        message=SecretManagerSource,
    )
    drm_systems: DrmSystems = proto.Field(
        proto.MESSAGE,
        number=3,
        message=DrmSystems,
    )
    aes128: Aes128Encryption = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="encryption_mode",
        message=Aes128Encryption,
    )
    sample_aes: SampleAesEncryption = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="encryption_mode",
        message=SampleAesEncryption,
    )
    mpeg_cenc: MpegCommonEncryption = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="encryption_mode",
        message=MpegCommonEncryption,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
