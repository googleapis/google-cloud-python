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
import proto  # type: ignore

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.video.transcoder.v1beta1",
    manifest={
        "Job",
        "JobTemplate",
        "JobConfig",
        "Input",
        "Output",
        "EditAtom",
        "AdBreak",
        "ElementaryStream",
        "MuxStream",
        "Manifest",
        "PubsubDestination",
        "SpriteSheet",
        "Overlay",
        "PreprocessingConfig",
        "VideoStream",
        "AudioStream",
        "TextStream",
        "SegmentSettings",
        "Encryption",
        "Progress",
        "FailureDetail",
    },
)


class Job(proto.Message):
    r"""Transcoding job resource.
    Attributes:
        name (str):
            The resource name of the job. Format:
            ``projects/{project}/locations/{location}/jobs/{job}``
        input_uri (str):
            Input only. Specify the ``input_uri`` to populate empty
            ``uri`` fields in each element of ``Job.config.inputs`` or
            ``JobTemplate.config.inputs`` when using template. URI of
            the media. It must be stored in Cloud Storage. For example,
            ``gs://bucket/inputs/file.mp4``.
        output_uri (str):
            Input only. Specify the ``output_uri`` to populate an empty
            ``Job.config.output.uri`` or
            ``JobTemplate.config.output.uri`` when using template. URI
            for the output file(s). For example,
            ``gs://my-bucket/outputs/``.
        template_id (str):
            Input only. Specify the ``template_id`` to use for
            populating ``Job.config``. The default is ``preset/web-hd``.

            Preset Transcoder templates:

            -  ``preset/{preset_id}``

            -  User defined JobTemplate: ``{job_template_id}``
        config (google.cloud.video.transcoder_v1beta1.types.JobConfig):
            The configuration for this job.
        priority (int):
            Specify the priority of the job. Enter a
            value between 0 and 100, where 0 is the lowest
            priority and 100 is the highest priority. The
            default is 0.
        origin_uri (google.cloud.video.transcoder_v1beta1.types.Job.OriginUri):
            Output only. The origin URI.
        state (google.cloud.video.transcoder_v1beta1.types.Job.ProcessingState):
            Output only. The current state of the job.
        progress (google.cloud.video.transcoder_v1beta1.types.Progress):
            Output only. Estimated fractional progress, from ``0`` to
            ``1`` for each step.
        failure_reason (str):
            Output only. A description of the reason for the failure.
            This property is always present when ``state`` is
            ``FAILED``.
        failure_details (Sequence[google.cloud.video.transcoder_v1beta1.types.FailureDetail]):
            Output only. List of failure details. This property may
            contain additional information about the failure when
            ``failure_reason`` is present.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the job was created.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the transcoding
            started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the transcoding
            finished.
    """

    class ProcessingState(proto.Enum):
        r"""The current state of the job."""
        PROCESSING_STATE_UNSPECIFIED = 0
        PENDING = 1
        RUNNING = 2
        SUCCEEDED = 3
        FAILED = 4

    class OriginUri(proto.Message):
        r"""The origin URI.
        Attributes:
            hls (str):
                HLS master manifest URI. If multiple HLS
                master manifests are created only first one is
                listed.
            dash (str):
                Dash manifest URI. If multiple Dash manifests
                are created, only the first one is listed.
        """

        hls = proto.Field(proto.STRING, number=1,)
        dash = proto.Field(proto.STRING, number=2,)

    name = proto.Field(proto.STRING, number=1,)
    input_uri = proto.Field(proto.STRING, number=2,)
    output_uri = proto.Field(proto.STRING, number=3,)
    template_id = proto.Field(proto.STRING, number=4, oneof="job_config",)
    config = proto.Field(
        proto.MESSAGE, number=5, oneof="job_config", message="JobConfig",
    )
    priority = proto.Field(proto.INT32, number=6,)
    origin_uri = proto.Field(proto.MESSAGE, number=7, message=OriginUri,)
    state = proto.Field(proto.ENUM, number=8, enum=ProcessingState,)
    progress = proto.Field(proto.MESSAGE, number=9, message="Progress",)
    failure_reason = proto.Field(proto.STRING, number=10,)
    failure_details = proto.RepeatedField(
        proto.MESSAGE, number=11, message="FailureDetail",
    )
    create_time = proto.Field(
        proto.MESSAGE, number=12, message=timestamp_pb2.Timestamp,
    )
    start_time = proto.Field(proto.MESSAGE, number=13, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=14, message=timestamp_pb2.Timestamp,)


class JobTemplate(proto.Message):
    r"""Transcoding job template resource.
    Attributes:
        name (str):
            The resource name of the job template. Format:
            ``projects/{project}/locations/{location}/jobTemplates/{job_template}``
        config (google.cloud.video.transcoder_v1beta1.types.JobConfig):
            The configuration for this template.
    """

    name = proto.Field(proto.STRING, number=1,)
    config = proto.Field(proto.MESSAGE, number=2, message="JobConfig",)


class JobConfig(proto.Message):
    r"""Job configuration
    Attributes:
        inputs (Sequence[google.cloud.video.transcoder_v1beta1.types.Input]):
            List of input assets stored in Cloud Storage.
        edit_list (Sequence[google.cloud.video.transcoder_v1beta1.types.EditAtom]):
            List of ``Edit atom``\ s. Defines the ultimate timeline of
            the resulting file or manifest.
        elementary_streams (Sequence[google.cloud.video.transcoder_v1beta1.types.ElementaryStream]):
            List of elementary streams.
        mux_streams (Sequence[google.cloud.video.transcoder_v1beta1.types.MuxStream]):
            List of multiplexing settings for output
            streams.
        manifests (Sequence[google.cloud.video.transcoder_v1beta1.types.Manifest]):
            List of output manifests.
        output (google.cloud.video.transcoder_v1beta1.types.Output):
            Output configuration.
        ad_breaks (Sequence[google.cloud.video.transcoder_v1beta1.types.AdBreak]):
            List of ad breaks. Specifies where to insert
            ad break tags in the output manifests.
        pubsub_destination (google.cloud.video.transcoder_v1beta1.types.PubsubDestination):
            Destination on Pub/Sub.
        sprite_sheets (Sequence[google.cloud.video.transcoder_v1beta1.types.SpriteSheet]):
            List of output sprite sheets.
        overlays (Sequence[google.cloud.video.transcoder_v1beta1.types.Overlay]):
            List of overlays on the output video, in
            descending Z-order.
    """

    inputs = proto.RepeatedField(proto.MESSAGE, number=1, message="Input",)
    edit_list = proto.RepeatedField(proto.MESSAGE, number=2, message="EditAtom",)
    elementary_streams = proto.RepeatedField(
        proto.MESSAGE, number=3, message="ElementaryStream",
    )
    mux_streams = proto.RepeatedField(proto.MESSAGE, number=4, message="MuxStream",)
    manifests = proto.RepeatedField(proto.MESSAGE, number=5, message="Manifest",)
    output = proto.Field(proto.MESSAGE, number=6, message="Output",)
    ad_breaks = proto.RepeatedField(proto.MESSAGE, number=7, message="AdBreak",)
    pubsub_destination = proto.Field(
        proto.MESSAGE, number=8, message="PubsubDestination",
    )
    sprite_sheets = proto.RepeatedField(proto.MESSAGE, number=9, message="SpriteSheet",)
    overlays = proto.RepeatedField(proto.MESSAGE, number=10, message="Overlay",)


class Input(proto.Message):
    r"""Input asset.
    Attributes:
        key (str):
            A unique key for this input. Must be
            specified when using advanced mapping and edit
            lists.
        uri (str):
            URI of the media. It must be stored in Cloud Storage.
            Example ``gs://bucket/inputs/file.mp4``. If empty the value
            will be populated from ``Job.input_uri``.
        preprocessing_config (google.cloud.video.transcoder_v1beta1.types.PreprocessingConfig):
            Preprocessing configurations.
    """

    key = proto.Field(proto.STRING, number=1,)
    uri = proto.Field(proto.STRING, number=2,)
    preprocessing_config = proto.Field(
        proto.MESSAGE, number=3, message="PreprocessingConfig",
    )


class Output(proto.Message):
    r"""Location of output file(s) in a Cloud Storage bucket.
    Attributes:
        uri (str):
            URI for the output file(s). For example,
            ``gs://my-bucket/outputs/``. If empty the value is populated
            from ``Job.output_uri``.
    """

    uri = proto.Field(proto.STRING, number=1,)


class EditAtom(proto.Message):
    r"""Edit atom.
    Attributes:
        key (str):
            A unique key for this atom. Must be specified
            when using advanced mapping.
        inputs (Sequence[str]):
            List of ``Input.key``\ s identifying files that should be
            used in this atom. The listed ``inputs`` must have the same
            timeline.
        end_time_offset (google.protobuf.duration_pb2.Duration):
            End time in seconds for the atom, relative to the input file
            timeline. When ``end_time_offset`` is not specified, the
            ``inputs`` are used until the end of the atom.
        start_time_offset (google.protobuf.duration_pb2.Duration):
            Start time in seconds for the atom, relative to the input
            file timeline. The default is ``0s``.
    """

    key = proto.Field(proto.STRING, number=1,)
    inputs = proto.RepeatedField(proto.STRING, number=2,)
    end_time_offset = proto.Field(
        proto.MESSAGE, number=3, message=duration_pb2.Duration,
    )
    start_time_offset = proto.Field(
        proto.MESSAGE, number=4, message=duration_pb2.Duration,
    )


class AdBreak(proto.Message):
    r"""Ad break.
    Attributes:
        start_time_offset (google.protobuf.duration_pb2.Duration):
            Start time in seconds for the ad break, relative to the
            output file timeline. The default is ``0s``.
    """

    start_time_offset = proto.Field(
        proto.MESSAGE, number=1, message=duration_pb2.Duration,
    )


class ElementaryStream(proto.Message):
    r"""Encoding of an input file such as an audio, video, or text
    track. Elementary streams must be packaged before
    mapping and sharing between different output formats.

    Attributes:
        key (str):
            A unique key for this elementary stream.
        video_stream (google.cloud.video.transcoder_v1beta1.types.VideoStream):
            Encoding of a video stream.
        audio_stream (google.cloud.video.transcoder_v1beta1.types.AudioStream):
            Encoding of an audio stream.
        text_stream (google.cloud.video.transcoder_v1beta1.types.TextStream):
            Encoding of a text stream. For example,
            closed captions or subtitles.
    """

    key = proto.Field(proto.STRING, number=4,)
    video_stream = proto.Field(
        proto.MESSAGE, number=1, oneof="elementary_stream", message="VideoStream",
    )
    audio_stream = proto.Field(
        proto.MESSAGE, number=2, oneof="elementary_stream", message="AudioStream",
    )
    text_stream = proto.Field(
        proto.MESSAGE, number=3, oneof="elementary_stream", message="TextStream",
    )


class MuxStream(proto.Message):
    r"""Multiplexing settings for output stream.
    Attributes:
        key (str):
            A unique key for this multiplexed stream. HLS media
            manifests will be named ``MuxStream.key`` with the
            ``".m3u8"`` extension suffix.
        file_name (str):
            The name of the generated file. The default is
            ``MuxStream.key`` with the extension suffix corresponding to
            the ``MuxStream.container``.

            Individual segments also have an incremental 10-digit
            zero-padded suffix starting from 0 before the extension,
            such as ``"mux_stream0000000123.ts"``.
        container (str):
            The container format. The default is ``"mp4"``

            Supported container formats:

            -  'ts'
            -  'fmp4'- the corresponding file extension is ``".m4s"``
            -  'mp4'
            -  'vtt'
        elementary_streams (Sequence[str]):
            List of ``ElementaryStream.key``\ s multiplexed in this
            stream.
        segment_settings (google.cloud.video.transcoder_v1beta1.types.SegmentSettings):
            Segment settings for ``"ts"``, ``"fmp4"`` and ``"vtt"``.
        encryption (google.cloud.video.transcoder_v1beta1.types.Encryption):
            Encryption settings.
    """

    key = proto.Field(proto.STRING, number=1,)
    file_name = proto.Field(proto.STRING, number=2,)
    container = proto.Field(proto.STRING, number=3,)
    elementary_streams = proto.RepeatedField(proto.STRING, number=4,)
    segment_settings = proto.Field(proto.MESSAGE, number=5, message="SegmentSettings",)
    encryption = proto.Field(proto.MESSAGE, number=6, message="Encryption",)


class Manifest(proto.Message):
    r"""Manifest configuration.
    Attributes:
        file_name (str):
            The name of the generated file. The default is
            ``"manifest"`` with the extension suffix corresponding to
            the ``Manifest.type``.
        type_ (google.cloud.video.transcoder_v1beta1.types.Manifest.ManifestType):
            Required. Type of the manifest, can be "HLS"
            or "DASH".
        mux_streams (Sequence[str]):
            Required. List of user given ``MuxStream.key``\ s that
            should appear in this manifest.

            When ``Manifest.type`` is ``HLS``, a media manifest with
            name ``MuxStream.key`` and ``.m3u8`` extension is generated
            for each element of the ``Manifest.mux_streams``.
    """

    class ManifestType(proto.Enum):
        r"""The manifest type can be either ``"HLS"`` or ``"DASH"``."""
        MANIFEST_TYPE_UNSPECIFIED = 0
        HLS = 1
        DASH = 2

    file_name = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.ENUM, number=2, enum=ManifestType,)
    mux_streams = proto.RepeatedField(proto.STRING, number=3,)


class PubsubDestination(proto.Message):
    r"""A Pub/Sub destination.
    Attributes:
        topic (str):
            The name of the Pub/Sub topic to publish job completion
            notification to. For example:
            ``projects/{project}/topics/{topic}``.
    """

    topic = proto.Field(proto.STRING, number=1,)


class SpriteSheet(proto.Message):
    r"""Sprite sheet configuration.

    Attributes:
        format_ (str):
            Format type. The default is ``"jpeg"``.

            Supported formats:

            -  'jpeg'
        file_prefix (str):
            Required. File name prefix for the generated sprite sheets.

            Each sprite sheet has an incremental 10-digit zero-padded
            suffix starting from 0 before the extension, such as
            ``"sprite_sheet0000000123.jpeg"``.
        sprite_width_pixels (int):
            Required. The width of sprite in pixels. Must
            be an even integer.
        sprite_height_pixels (int):
            Required. The height of sprite in pixels.
            Must be an even integer.
        column_count (int):
            The maximum number of sprites per row in a
            sprite sheet. The default is 0, which indicates
            no maximum limit.
        row_count (int):
            The maximum number of rows per sprite sheet.
            When the sprite sheet is full, a new sprite
            sheet is created. The default is 0, which
            indicates no maximum limit.
        start_time_offset (google.protobuf.duration_pb2.Duration):
            Start time in seconds, relative to the output file timeline.
            Determines the first sprite to pick. The default is ``0s``.
        end_time_offset (google.protobuf.duration_pb2.Duration):
            End time in seconds, relative to the output file timeline.
            When ``end_time_offset`` is not specified, the sprites are
            generated until the end of the output file.
        total_count (int):
            Total number of sprites. Create the specified
            number of sprites distributed evenly across the
            timeline of the output media. The default is
            100.
        interval (google.protobuf.duration_pb2.Duration):
            Starting from ``0s``, create sprites at regular intervals.
            Specify the interval value in seconds.
    """

    format_ = proto.Field(proto.STRING, number=1,)
    file_prefix = proto.Field(proto.STRING, number=2,)
    sprite_width_pixels = proto.Field(proto.INT32, number=3,)
    sprite_height_pixels = proto.Field(proto.INT32, number=4,)
    column_count = proto.Field(proto.INT32, number=5,)
    row_count = proto.Field(proto.INT32, number=6,)
    start_time_offset = proto.Field(
        proto.MESSAGE, number=7, message=duration_pb2.Duration,
    )
    end_time_offset = proto.Field(
        proto.MESSAGE, number=8, message=duration_pb2.Duration,
    )
    total_count = proto.Field(proto.INT32, number=9, oneof="extraction_strategy",)
    interval = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="extraction_strategy",
        message=duration_pb2.Duration,
    )


class Overlay(proto.Message):
    r"""Overlay configuration.
    Attributes:
        image (google.cloud.video.transcoder_v1beta1.types.Overlay.Image):
            Image overlay.
        animations (Sequence[google.cloud.video.transcoder_v1beta1.types.Overlay.Animation]):
            List of Animations. The list should be
            chronological, without any time overlap.
    """

    class FadeType(proto.Enum):
        r"""Fade type for the overlay: ``FADE_IN`` or ``FADE_OUT``."""
        FADE_TYPE_UNSPECIFIED = 0
        FADE_IN = 1
        FADE_OUT = 2

    class NormalizedCoordinate(proto.Message):
        r"""2D normalized coordinates. Default: ``{0.0, 0.0}``
        Attributes:
            x (float):
                Normalized x coordinate.
            y (float):
                Normalized y coordinate.
        """

        x = proto.Field(proto.DOUBLE, number=1,)
        y = proto.Field(proto.DOUBLE, number=2,)

    class Image(proto.Message):
        r"""Overlaid jpeg image.
        Attributes:
            uri (str):
                Required. URI of the image in Cloud Storage. For example,
                ``gs://bucket/inputs/image.jpeg``.
            resolution (google.cloud.video.transcoder_v1beta1.types.Overlay.NormalizedCoordinate):
                Normalized image resolution, based on output video
                resolution. Valid values: ``0.0``–``1.0``. To respect the
                original image aspect ratio, set either ``x`` or ``y`` to
                ``0.0``. To use the original image resolution, set both
                ``x`` and ``y`` to ``0.0``.
            alpha (float):
                Target image opacity. Valid values: ``1`` (solid, default),
                ``0`` (transparent).
        """

        uri = proto.Field(proto.STRING, number=1,)
        resolution = proto.Field(
            proto.MESSAGE, number=2, message="Overlay.NormalizedCoordinate",
        )
        alpha = proto.Field(proto.DOUBLE, number=3,)

    class AnimationStatic(proto.Message):
        r"""Display static overlay object.
        Attributes:
            xy (google.cloud.video.transcoder_v1beta1.types.Overlay.NormalizedCoordinate):
                Normalized coordinates based on output video resolution.
                Valid values: ``0.0``–``1.0``. ``xy`` is the upper-left
                coordinate of the overlay object.
            start_time_offset (google.protobuf.duration_pb2.Duration):
                The time to start displaying the overlay
                object, in seconds. Default: 0
        """

        xy = proto.Field(
            proto.MESSAGE, number=1, message="Overlay.NormalizedCoordinate",
        )
        start_time_offset = proto.Field(
            proto.MESSAGE, number=2, message=duration_pb2.Duration,
        )

    class AnimationFade(proto.Message):
        r"""Display overlay object with fade animation.
        Attributes:
            fade_type (google.cloud.video.transcoder_v1beta1.types.Overlay.FadeType):
                Required. Type of fade animation: ``FADE_IN`` or
                ``FADE_OUT``.
            xy (google.cloud.video.transcoder_v1beta1.types.Overlay.NormalizedCoordinate):
                Normalized coordinates based on output video resolution.
                Valid values: ``0.0``–``1.0``. ``xy`` is the upper-left
                coordinate of the overlay object.
            start_time_offset (google.protobuf.duration_pb2.Duration):
                The time to start the fade animation, in
                seconds. Default: 0
            end_time_offset (google.protobuf.duration_pb2.Duration):
                The time to end the fade animation, in seconds. Default:
                ``start_time_offset`` + 1s
        """

        fade_type = proto.Field(proto.ENUM, number=1, enum="Overlay.FadeType",)
        xy = proto.Field(
            proto.MESSAGE, number=2, message="Overlay.NormalizedCoordinate",
        )
        start_time_offset = proto.Field(
            proto.MESSAGE, number=3, message=duration_pb2.Duration,
        )
        end_time_offset = proto.Field(
            proto.MESSAGE, number=4, message=duration_pb2.Duration,
        )

    class AnimationEnd(proto.Message):
        r"""End previous overlay animation from the video. Without
        AnimationEnd, the overlay object will keep the state of previous
        animation until the end of the video.

        Attributes:
            start_time_offset (google.protobuf.duration_pb2.Duration):
                The time to end overlay object, in seconds.
                Default: 0
        """

        start_time_offset = proto.Field(
            proto.MESSAGE, number=1, message=duration_pb2.Duration,
        )

    class Animation(proto.Message):
        r"""Animation types.
        Attributes:
            animation_static (google.cloud.video.transcoder_v1beta1.types.Overlay.AnimationStatic):
                Display static overlay object.
            animation_fade (google.cloud.video.transcoder_v1beta1.types.Overlay.AnimationFade):
                Display overlay object with fade animation.
            animation_end (google.cloud.video.transcoder_v1beta1.types.Overlay.AnimationEnd):
                End previous animation.
        """

        animation_static = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="animation_type",
            message="Overlay.AnimationStatic",
        )
        animation_fade = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="animation_type",
            message="Overlay.AnimationFade",
        )
        animation_end = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="animation_type",
            message="Overlay.AnimationEnd",
        )

    image = proto.Field(proto.MESSAGE, number=1, message=Image,)
    animations = proto.RepeatedField(proto.MESSAGE, number=2, message=Animation,)


class PreprocessingConfig(proto.Message):
    r"""Preprocessing configurations.
    Attributes:
        color (google.cloud.video.transcoder_v1beta1.types.PreprocessingConfig.Color):
            Color preprocessing configuration.
        denoise (google.cloud.video.transcoder_v1beta1.types.PreprocessingConfig.Denoise):
            Denoise preprocessing configuration.
        deblock (google.cloud.video.transcoder_v1beta1.types.PreprocessingConfig.Deblock):
            Deblock preprocessing configuration.
        audio (google.cloud.video.transcoder_v1beta1.types.PreprocessingConfig.Audio):
            Audio preprocessing configuration.
    """

    class Color(proto.Message):
        r"""Color preprocessing configuration.
        Attributes:
            saturation (float):
                Control color saturation of the video. Enter
                a value between -1 and 1, where -1 is fully
                desaturated and 1 is maximum saturation. 0 is no
                change. The default is 0.
            contrast (float):
                Control black and white contrast of the
                video. Enter a value between -1 and 1, where -1
                is minimum contrast and 1 is maximum contrast. 0
                is no change. The default is 0.
            brightness (float):
                Control brightness of the video. Enter a
                value between -1 and 1, where -1 is minimum
                brightness and 1 is maximum brightness. 0 is no
                change. The default is 0.
        """

        saturation = proto.Field(proto.DOUBLE, number=1,)
        contrast = proto.Field(proto.DOUBLE, number=2,)
        brightness = proto.Field(proto.DOUBLE, number=3,)

    class Denoise(proto.Message):
        r"""Denoise preprocessing configuration.
        Attributes:
            strength (float):
                Set strength of the denoise. Enter a value
                between 0 and 1. The higher the value, the
                smoother the image. 0 is no denoising. The
                default is 0.
            tune (str):
                Set the denoiser mode. The default is ``"standard"``.

                Supported denoiser modes:

                -  'standard'
                -  'grain'
        """

        strength = proto.Field(proto.DOUBLE, number=1,)
        tune = proto.Field(proto.STRING, number=2,)

    class Deblock(proto.Message):
        r"""Deblock preprocessing configuration.
        Attributes:
            strength (float):
                Set strength of the deblocker. Enter a value
                between 0 and 1. The higher the value, the
                stronger the block removal. 0 is no deblocking.
                The default is 0.
            enabled (bool):
                Enable deblocker. The default is ``false``.
        """

        strength = proto.Field(proto.DOUBLE, number=1,)
        enabled = proto.Field(proto.BOOL, number=2,)

    class Audio(proto.Message):
        r"""Audio preprocessing configuration.
        Attributes:
            lufs (float):
                Specify audio loudness normalization in
                loudness units relative to full scale (LUFS).
                Enter a value between -24 and 0, where -24 is
                the Advanced Television Systems Committee (ATSC
                A/85), -23 is the EU R128 broadcast standard,
                -19 is the prior standard for online mono audio,
                -18 is the ReplayGain standard, -16 is the prior
                standard for stereo audio, -14 is the new online
                audio standard recommended by Spotify, as well
                as Amazon Echo, and 0 disables normalization.
                The default is 0.
            high_boost (bool):
                Enable boosting high frequency components. The default is
                ``false``.
            low_boost (bool):
                Enable boosting low frequency components. The default is
                ``false``.
        """

        lufs = proto.Field(proto.DOUBLE, number=1,)
        high_boost = proto.Field(proto.BOOL, number=2,)
        low_boost = proto.Field(proto.BOOL, number=3,)

    color = proto.Field(proto.MESSAGE, number=1, message=Color,)
    denoise = proto.Field(proto.MESSAGE, number=2, message=Denoise,)
    deblock = proto.Field(proto.MESSAGE, number=3, message=Deblock,)
    audio = proto.Field(proto.MESSAGE, number=4, message=Audio,)


class VideoStream(proto.Message):
    r"""Video stream resource.
    Attributes:
        codec (str):
            Codec type. The default is ``"h264"``.

            Supported codecs:

            -  'h264'
            -  'h265'
            -  'vp9'
        profile (str):
            Enforce specified codec profile. The default is ``"high"``.

            Supported codec profiles:

            -  'baseline'
            -  'main'
            -  'high'
        tune (str):
            Enforce specified codec tune.
        preset (str):
            Enforce specified codec preset. The default is
            ``"veryfast"``.
        height_pixels (int):
            The height of the video in pixels. Must be an
            even integer. When not specified, the height is
            adjusted to match the specified width and input
            aspect ratio. If both are omitted, the input
            height is used.
        width_pixels (int):
            The width of the video in pixels. Must be an
            even integer. When not specified, the width is
            adjusted to match the specified height and input
            aspect ratio. If both are omitted, the input
            width is used.
        pixel_format (str):
            Pixel format to use. The default is ``"yuv420p"``.

            Supported pixel formats:

            -  'yuv420p' pixel format.
            -  'yuv422p' pixel format.
            -  'yuv444p' pixel format.
            -  'yuv420p10' 10-bit HDR pixel format.
            -  'yuv422p10' 10-bit HDR pixel format.
            -  'yuv444p10' 10-bit HDR pixel format.
            -  'yuv420p12' 12-bit HDR pixel format.
            -  'yuv422p12' 12-bit HDR pixel format.
            -  'yuv444p12' 12-bit HDR pixel format.
        bitrate_bps (int):
            Required. The video bitrate in bits per
            second. Must be between 1 and 1,000,000,000.
        rate_control_mode (str):
            Specify the ``rate_control_mode``. The default is ``"vbr"``.

            Supported rate control modes:

            -  'vbr' - variable bitrate
            -  'crf' - constant rate factor
        enable_two_pass (bool):
            Use two-pass encoding strategy to achieve better video
            quality. ``VideoStream.rate_control_mode`` must be
            ``"vbr"``. The default is ``false``.
        crf_level (int):
            Target CRF level. Must be between 10 and 36,
            where 10 is the highest quality and 36 is the
            most efficient compression. The default is 21.
        vbv_size_bits (int):
            Size of the Video Buffering Verifier (VBV) buffer in bits.
            Must be greater than zero. The default is equal to
            ``VideoStream.bitrate_bps``.
        vbv_fullness_bits (int):
            Initial fullness of the Video Buffering Verifier (VBV)
            buffer in bits. Must be greater than zero. The default is
            equal to 90% of ``VideoStream.vbv_size_bits``.
        allow_open_gop (bool):
            Specifies whether an open Group of Pictures (GOP) structure
            should be allowed or not. The default is ``false``.
        gop_frame_count (int):
            Select the GOP size based on the specified
            frame count. Must be greater than zero.
        gop_duration (google.protobuf.duration_pb2.Duration):
            Select the GOP size based on the specified duration. The
            default is ``"3s"``.
        entropy_coder (str):
            The entropy coder to use. The default is ``"cabac"``.

            Supported entropy coders:

            -  'cavlc'
            -  'cabac'
        b_pyramid (bool):
            Allow B-pyramid for reference frame selection. This may not
            be supported on all decoders. The default is ``false``.
        b_frame_count (int):
            The number of consecutive B-frames. Must be greater than or
            equal to zero. Must be less than
            ``VideoStream.gop_frame_count`` if set. The default is 0.
        frame_rate (float):
            Required. The target video frame rate in frames per second
            (FPS). Must be less than or equal to 120. Will default to
            the input frame rate if larger than the input frame rate.
            The API will generate an output FPS that is divisible by the
            input FPS, and smaller or equal to the target FPS.

            The following table shows the computed video FPS given the
            target FPS (in parenthesis) and input FPS (in the first
            column):

            ::

               |        | (30)   | (60)   | (25) | (50) |
               |--------|--------|--------|------|------|
               | 240    | Fail   | Fail   | Fail | Fail |
               | 120    | 30     | 60     | 20   | 30   |
               | 100    | 25     | 50     | 20   | 30   |
               | 50     | 25     | 50     | 20   | 30   |
               | 60     | 30     | 60     | 20   | 30   |
               | 59.94  | 29.97  | 59.94  | 20   | 30   |
               | 48     | 24     | 48     | 20   | 30   |
               | 30     | 30     | 30     | 20   | 30   |
               | 25     | 25     | 25     | 20   | 30   |
               | 24     | 24     | 24     | 20   | 30   |
               | 23.976 | 23.976 | 23.976 | 20   | 30   |
               | 15     | 15     | 15     | 20   | 30   |
               | 12     | 12     | 12     | 20   | 30   |
               | 10     | 10     | 10     | 20   | 30   |
        aq_strength (float):
            Specify the intensity of the adaptive
            quantizer (AQ). Must be between 0 and 1, where 0
            disables the quantizer and 1 maximizes the
            quantizer. A higher value equals a lower bitrate
            but smoother image. The default is 0.
    """

    codec = proto.Field(proto.STRING, number=1,)
    profile = proto.Field(proto.STRING, number=2,)
    tune = proto.Field(proto.STRING, number=3,)
    preset = proto.Field(proto.STRING, number=4,)
    height_pixels = proto.Field(proto.INT32, number=5,)
    width_pixels = proto.Field(proto.INT32, number=6,)
    pixel_format = proto.Field(proto.STRING, number=7,)
    bitrate_bps = proto.Field(proto.INT32, number=8,)
    rate_control_mode = proto.Field(proto.STRING, number=9,)
    enable_two_pass = proto.Field(proto.BOOL, number=10,)
    crf_level = proto.Field(proto.INT32, number=11,)
    vbv_size_bits = proto.Field(proto.INT32, number=12,)
    vbv_fullness_bits = proto.Field(proto.INT32, number=13,)
    allow_open_gop = proto.Field(proto.BOOL, number=14,)
    gop_frame_count = proto.Field(proto.INT32, number=15, oneof="gop_mode",)
    gop_duration = proto.Field(
        proto.MESSAGE, number=16, oneof="gop_mode", message=duration_pb2.Duration,
    )
    entropy_coder = proto.Field(proto.STRING, number=17,)
    b_pyramid = proto.Field(proto.BOOL, number=18,)
    b_frame_count = proto.Field(proto.INT32, number=19,)
    frame_rate = proto.Field(proto.DOUBLE, number=20,)
    aq_strength = proto.Field(proto.DOUBLE, number=21,)


class AudioStream(proto.Message):
    r"""Audio stream resource.
    Attributes:
        codec (str):
            The codec for this audio stream. The default is ``"aac"``.

            Supported audio codecs:

            -  'aac'
            -  'aac-he'
            -  'aac-he-v2'
            -  'mp3'
            -  'ac3'
            -  'eac3'
        bitrate_bps (int):
            Required. Audio bitrate in bits per second.
            Must be between 1 and 10,000,000.
        channel_count (int):
            Number of audio channels. Must be between 1
            and 6. The default is 2.
        channel_layout (Sequence[str]):
            A list of channel names specifying layout of the audio
            channels. This only affects the metadata embedded in the
            container headers, if supported by the specified format. The
            default is ``["fl", "fr"]``.

            Supported channel names:

            -  'fl' - Front left channel
            -  'fr' - Front right channel
            -  'sl' - Side left channel
            -  'sr' - Side right channel
            -  'fc' - Front center channel
            -  'lfe' - Low frequency
        mapping (Sequence[google.cloud.video.transcoder_v1beta1.types.AudioStream.AudioAtom]):
            The mapping for the ``Job.edit_list`` atoms with audio
            ``EditAtom.inputs``.
        sample_rate_hertz (int):
            The audio sample rate in Hertz. The default
            is 48000 Hertz.
    """

    class AudioAtom(proto.Message):
        r"""The mapping for the ``Job.edit_list`` atoms with audio
        ``EditAtom.inputs``.

        Attributes:
            key (str):
                Required. The ``EditAtom.key`` that references the atom with
                audio inputs in the ``Job.edit_list``.
            channels (Sequence[google.cloud.video.transcoder_v1beta1.types.AudioStream.AudioAtom.AudioChannel]):
                List of ``Channel``\ s for this audio stream. for in-depth
                explanation.
        """

        class AudioChannel(proto.Message):
            r"""The audio channel.
            Attributes:
                inputs (Sequence[google.cloud.video.transcoder_v1beta1.types.AudioStream.AudioAtom.AudioChannel.AudioChannelInput]):
                    List of ``Job.inputs`` for this audio channel.
            """

            class AudioChannelInput(proto.Message):
                r"""Identifies which input file, track, and channel should be
                used.

                Attributes:
                    key (str):
                        Required. The ``Input.key`` that identifies the input file.
                    track (int):
                        Required. The zero-based index of the track
                        in the input file.
                    channel (int):
                        Required. The zero-based index of the channel
                        in the input file.
                    gain_db (float):
                        Audio volume control in dB. Negative values
                        decrease volume, positive values increase. The
                        default is 0.
                """

                key = proto.Field(proto.STRING, number=1,)
                track = proto.Field(proto.INT32, number=2,)
                channel = proto.Field(proto.INT32, number=3,)
                gain_db = proto.Field(proto.DOUBLE, number=4,)

            inputs = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message="AudioStream.AudioAtom.AudioChannel.AudioChannelInput",
            )

        key = proto.Field(proto.STRING, number=1,)
        channels = proto.RepeatedField(
            proto.MESSAGE, number=2, message="AudioStream.AudioAtom.AudioChannel",
        )

    codec = proto.Field(proto.STRING, number=1,)
    bitrate_bps = proto.Field(proto.INT32, number=2,)
    channel_count = proto.Field(proto.INT32, number=3,)
    channel_layout = proto.RepeatedField(proto.STRING, number=4,)
    mapping = proto.RepeatedField(proto.MESSAGE, number=5, message=AudioAtom,)
    sample_rate_hertz = proto.Field(proto.INT32, number=6,)


class TextStream(proto.Message):
    r"""Encoding of a text stream. For example, closed captions or
    subtitles.

    Attributes:
        codec (str):
            The codec for this text stream. The default is ``"webvtt"``.

            Supported text codecs:

            -  'srt'
            -  'ttml'
            -  'cea608'
            -  'cea708'
            -  'webvtt'
        language_code (str):
            Required. The BCP-47 language code, such as ``"en-US"`` or
            ``"sr-Latn"``. For more information, see
            https://www.unicode.org/reports/tr35/#Unicode_locale_identifier.
        mapping (Sequence[google.cloud.video.transcoder_v1beta1.types.TextStream.TextAtom]):
            The mapping for the ``Job.edit_list`` atoms with text
            ``EditAtom.inputs``.
    """

    class TextAtom(proto.Message):
        r"""The mapping for the ``Job.edit_list`` atoms with text
        ``EditAtom.inputs``.

        Attributes:
            key (str):
                Required. The ``EditAtom.key`` that references atom with
                text inputs in the ``Job.edit_list``.
            inputs (Sequence[google.cloud.video.transcoder_v1beta1.types.TextStream.TextAtom.TextInput]):
                List of ``Job.inputs`` that should be embedded in this atom.
                Only one input is supported.
        """

        class TextInput(proto.Message):
            r"""Identifies which input file and track should be used.
            Attributes:
                key (str):
                    Required. The ``Input.key`` that identifies the input file.
                track (int):
                    Required. The zero-based index of the track
                    in the input file.
            """

            key = proto.Field(proto.STRING, number=1,)
            track = proto.Field(proto.INT32, number=2,)

        key = proto.Field(proto.STRING, number=1,)
        inputs = proto.RepeatedField(
            proto.MESSAGE, number=2, message="TextStream.TextAtom.TextInput",
        )

    codec = proto.Field(proto.STRING, number=1,)
    language_code = proto.Field(proto.STRING, number=2,)
    mapping = proto.RepeatedField(proto.MESSAGE, number=3, message=TextAtom,)


class SegmentSettings(proto.Message):
    r"""Segment settings for ``"ts"``, ``"fmp4"`` and ``"vtt"``.
    Attributes:
        segment_duration (google.protobuf.duration_pb2.Duration):
            Duration of the segments in seconds. The default is
            ``"6.0s"``.
        individual_segments (bool):
            Required. Create an individual segment file. The default is
            ``false``.
    """

    segment_duration = proto.Field(
        proto.MESSAGE, number=1, message=duration_pb2.Duration,
    )
    individual_segments = proto.Field(proto.BOOL, number=3,)


class Encryption(proto.Message):
    r"""Encryption settings.
    Attributes:
        key (str):
            Required. 128 bit encryption key represented
            as lowercase hexadecimal digits.
        iv (str):
            Required. 128 bit Initialization Vector (IV)
            represented as lowercase hexadecimal digits.
        aes_128 (google.cloud.video.transcoder_v1beta1.types.Encryption.Aes128Encryption):
            Configuration for AES-128 encryption.
        sample_aes (google.cloud.video.transcoder_v1beta1.types.Encryption.SampleAesEncryption):
            Configuration for SAMPLE-AES encryption.
        mpeg_cenc (google.cloud.video.transcoder_v1beta1.types.Encryption.MpegCommonEncryption):
            Configuration for MPEG Common Encryption
            (MPEG-CENC).
    """

    class Aes128Encryption(proto.Message):
        r"""Configuration for AES-128 encryption.
        Attributes:
            key_uri (str):
                Required. URI of the key delivery service.
                This URI is inserted into the M3U8 header.
        """

        key_uri = proto.Field(proto.STRING, number=1,)

    class SampleAesEncryption(proto.Message):
        r"""Configuration for SAMPLE-AES encryption.
        Attributes:
            key_uri (str):
                Required. URI of the key delivery service.
                This URI is inserted into the M3U8 header.
        """

        key_uri = proto.Field(proto.STRING, number=1,)

    class MpegCommonEncryption(proto.Message):
        r"""Configuration for MPEG Common Encryption (MPEG-CENC).
        Attributes:
            key_id (str):
                Required. 128 bit Key ID represented as
                lowercase hexadecimal digits for use with common
                encryption.
            scheme (str):
                Required. Specify the encryption scheme.
                Supported encryption schemes:
                - 'cenc'
                - 'cbcs'
        """

        key_id = proto.Field(proto.STRING, number=1,)
        scheme = proto.Field(proto.STRING, number=2,)

    key = proto.Field(proto.STRING, number=1,)
    iv = proto.Field(proto.STRING, number=2,)
    aes_128 = proto.Field(
        proto.MESSAGE, number=3, oneof="encryption_mode", message=Aes128Encryption,
    )
    sample_aes = proto.Field(
        proto.MESSAGE, number=4, oneof="encryption_mode", message=SampleAesEncryption,
    )
    mpeg_cenc = proto.Field(
        proto.MESSAGE, number=5, oneof="encryption_mode", message=MpegCommonEncryption,
    )


class Progress(proto.Message):
    r"""Estimated fractional progress for each step, from ``0`` to ``1``.
    Attributes:
        analyzed (float):
            Estimated fractional progress for ``analyzing`` step.
        encoded (float):
            Estimated fractional progress for ``encoding`` step.
        uploaded (float):
            Estimated fractional progress for ``uploading`` step.
        notified (float):
            Estimated fractional progress for ``notifying`` step.
    """

    analyzed = proto.Field(proto.DOUBLE, number=1,)
    encoded = proto.Field(proto.DOUBLE, number=2,)
    uploaded = proto.Field(proto.DOUBLE, number=3,)
    notified = proto.Field(proto.DOUBLE, number=4,)


class FailureDetail(proto.Message):
    r"""Additional information about the reasons for the failure.
    Attributes:
        description (str):
            A description of the failure.
    """

    description = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
