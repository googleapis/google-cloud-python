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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import duration_pb2  # type: ignore
from google.type import datetime_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.video.livestream.v1",
    manifest={
        "ElementaryStream",
        "MuxStream",
        "Manifest",
        "SpriteSheet",
        "PreprocessingConfig",
        "VideoStream",
        "AudioStream",
        "TextStream",
        "SegmentSettings",
        "TimecodeConfig",
    },
)


class ElementaryStream(proto.Message):
    r"""Encoding of an input element such as an audio, video, or text
    track. Elementary streams must be packaged before mapping and
    sharing between different output formats.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        key (str):
            A unique key for this elementary stream. The
            key must be 1-63 characters in length. The key
            must begin and end with a letter (regardless of
            case) or a number, but can contain dashes or
            underscores in between.
        video_stream (google.cloud.video.live_stream_v1.types.VideoStream):
            Encoding of a video stream.

            This field is a member of `oneof`_ ``elementary_stream``.
        audio_stream (google.cloud.video.live_stream_v1.types.AudioStream):
            Encoding of an audio stream.

            This field is a member of `oneof`_ ``elementary_stream``.
        text_stream (google.cloud.video.live_stream_v1.types.TextStream):
            Encoding of a text stream. For example,
            closed captions or subtitles.

            This field is a member of `oneof`_ ``elementary_stream``.
    """

    key: str = proto.Field(
        proto.STRING,
        number=4,
    )
    video_stream: "VideoStream" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="elementary_stream",
        message="VideoStream",
    )
    audio_stream: "AudioStream" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="elementary_stream",
        message="AudioStream",
    )
    text_stream: "TextStream" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="elementary_stream",
        message="TextStream",
    )


class MuxStream(proto.Message):
    r"""Multiplexing settings for output stream.

    Attributes:
        key (str):
            A unique key for this multiplexed stream. The
            key must be 1-63 characters in length. The key
            must begin and end with a letter (regardless of
            case) or a number, but can contain dashes or
            underscores in between.
        container (str):
            The container format. The default is ``fmp4``.

            Supported container formats:

            -  ``fmp4`` - the corresponding file extension is ``.m4s``
            -  ``ts`` - the corresponding file extension is ``.ts``
        elementary_streams (MutableSequence[str]):
            List of ``ElementaryStream``
            [key][google.cloud.video.livestream.v1.ElementaryStream.key]s
            multiplexed in this stream.

            -  For ``fmp4`` container, must contain either one video or
               one audio stream.
            -  For ``ts`` container, must contain exactly one audio
               stream and up to one video stream.
        segment_settings (google.cloud.video.live_stream_v1.types.SegmentSettings):
            Segment settings for ``fmp4`` and ``ts``.
        encryption_id (str):
            Identifier of the encryption configuration to
            use. If omitted, output will be unencrypted.
    """

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    container: str = proto.Field(
        proto.STRING,
        number=3,
    )
    elementary_streams: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    segment_settings: "SegmentSettings" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="SegmentSettings",
    )
    encryption_id: str = proto.Field(
        proto.STRING,
        number=6,
    )


class Manifest(proto.Message):
    r"""Manifest configuration.

    Attributes:
        file_name (str):
            The name of the generated file. The default is ``manifest``
            with the extension suffix corresponding to the ``Manifest``
            [type][google.cloud.video.livestream.v1.Manifest.type]. If
            multiple manifests are added to the channel, each must have
            a unique file name.
        type_ (google.cloud.video.live_stream_v1.types.Manifest.ManifestType):
            Required. Type of the manifest, can be ``HLS`` or ``DASH``.
        mux_streams (MutableSequence[str]):
            Required. List of ``MuxStream``
            [key][google.cloud.video.livestream.v1.MuxStream.key]s that
            should appear in this manifest.

            -  For HLS, either ``fmp4`` or ``ts`` mux streams can be
               specified but not mixed.
            -  For DASH, only ``fmp4`` mux streams can be specified.
        max_segment_count (int):
            Maximum number of segments that this manifest
            holds. Once the manifest reaches this maximum
            number of segments, whenever a new segment is
            added to the manifest, the oldest segment will
            be removed from the manifest. The minimum value
            is 3 and the default value is 5.
        segment_keep_duration (google.protobuf.duration_pb2.Duration):
            How long to keep a segment on the output Google Cloud
            Storage bucket after it is removed from the manifest. This
            field should be large enough to cover the manifest
            propagation delay. Otherwise, a player could receive 404
            errors while accessing segments which are listed in the
            manifest that the player has, but were already deleted from
            the output Google Cloud Storage bucket. Default value is
            ``60s``.

            If both segment_keep_duration and
            [RetentionConfig.retention_window_duration][google.cloud.video.livestream.v1.RetentionConfig.retention_window_duration]
            are set,
            [RetentionConfig.retention_window_duration][google.cloud.video.livestream.v1.RetentionConfig.retention_window_duration]
            is used and segment_keep_duration is ignored.
        use_timecode_as_timeline (bool):
            Whether to use the timecode, as specified in timecode
            config, when setting:

            -  ``availabilityStartTime`` attribute in DASH manifests.
            -  ``#EXT-X-PROGRAM-DATE-TIME`` tag in HLS manifests.

            If false, ignore the input timecode and use the time from
            system clock when the manifest is first generated. This is
            the default behavior.
        key (str):
            Optional. A unique key for this manifest.
    """

    class ManifestType(proto.Enum):
        r"""The manifest type can be either ``HLS`` or ``DASH``.

        Values:
            MANIFEST_TYPE_UNSPECIFIED (0):
                The manifest type is not specified.
            HLS (1):
                Create an ``HLS`` manifest. The corresponding file extension
                is ``.m3u8``.
            DASH (2):
                Create a ``DASH`` manifest. The corresponding file extension
                is ``.mpd``.
        """
        MANIFEST_TYPE_UNSPECIFIED = 0
        HLS = 1
        DASH = 2

    file_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: ManifestType = proto.Field(
        proto.ENUM,
        number=2,
        enum=ManifestType,
    )
    mux_streams: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    max_segment_count: int = proto.Field(
        proto.INT32,
        number=4,
    )
    segment_keep_duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=5,
        message=duration_pb2.Duration,
    )
    use_timecode_as_timeline: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    key: str = proto.Field(
        proto.STRING,
        number=7,
    )


class SpriteSheet(proto.Message):
    r"""Sprite sheet configuration.

    Attributes:
        format_ (str):
            Format type. The default is ``jpeg``.

            Supported formats:

            -  ``jpeg``
        file_prefix (str):
            Required. File name prefix for the generated sprite sheets.
            If multiple sprite sheets are added to the channel, each
            must have a unique file prefix. Each sprite sheet has an
            incremental 10-digit zero-padded suffix starting from 0
            before the extension, such as
            ``sprite_sheet0000000123.jpeg``.
        sprite_width_pixels (int):
            Required. The width of the sprite in pixels.
            Must be an even integer.
        sprite_height_pixels (int):
            Required. The height of the sprite in pixels.
            Must be an even integer.
        column_count (int):
            The maximum number of sprites per row in a sprite sheet.
            Valid range is [1, 10] and the default value is 1.
        row_count (int):
            The maximum number of rows per sprite sheet. When the sprite
            sheet is full, a new sprite sheet is created. Valid range is
            [1, 10] and the default value is 1.
        interval (google.protobuf.duration_pb2.Duration):
            Create sprites at regular intervals. Valid range is [1
            second, 1 hour] and the default value is ``10s``.
        quality (int):
            The quality of the generated sprite sheet.
            Enter a value between 1 and 100, where 1 is the
            lowest quality and 100 is the highest quality.
            The default is 100. A high quality value
            corresponds to a low image data compression
            ratio.
    """

    format_: str = proto.Field(
        proto.STRING,
        number=1,
    )
    file_prefix: str = proto.Field(
        proto.STRING,
        number=2,
    )
    sprite_width_pixels: int = proto.Field(
        proto.INT32,
        number=3,
    )
    sprite_height_pixels: int = proto.Field(
        proto.INT32,
        number=4,
    )
    column_count: int = proto.Field(
        proto.INT32,
        number=5,
    )
    row_count: int = proto.Field(
        proto.INT32,
        number=6,
    )
    interval: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=7,
        message=duration_pb2.Duration,
    )
    quality: int = proto.Field(
        proto.INT32,
        number=8,
    )


class PreprocessingConfig(proto.Message):
    r"""Preprocessing configurations.

    Attributes:
        audio (google.cloud.video.live_stream_v1.types.PreprocessingConfig.Audio):
            Audio preprocessing configuration.
        crop (google.cloud.video.live_stream_v1.types.PreprocessingConfig.Crop):
            Specify the video cropping configuration.
        pad (google.cloud.video.live_stream_v1.types.PreprocessingConfig.Pad):
            Specify the video pad filter configuration.
    """

    class Audio(proto.Message):
        r"""Audio preprocessing configuration.

        Attributes:
            lufs (float):
                Specify audio loudness normalization in
                loudness units relative to full scale (LUFS).
                Enter a value between -24 and 0 according to the
                following:

                - -24 is the Advanced Television Systems
                  Committee (ATSC A/85)
                - -23 is the EU R128 broadcast standard
                - -19 is the prior standard for online mono
                  audio
                - -18 is the ReplayGain standard
                - -16 is the prior standard for stereo audio
                - -14 is the new online audio standard
                  recommended by Spotify, as well as Amazon Echo
                - 0 disables normalization. The default is 0.
        """

        lufs: float = proto.Field(
            proto.DOUBLE,
            number=1,
        )

    class Crop(proto.Message):
        r"""Video cropping configuration for the input video. The cropped
        input video is scaled to match the output resolution.

        Attributes:
            top_pixels (int):
                The number of pixels to crop from the top.
                The default is 0.
            bottom_pixels (int):
                The number of pixels to crop from the bottom.
                The default is 0.
            left_pixels (int):
                The number of pixels to crop from the left.
                The default is 0.
            right_pixels (int):
                The number of pixels to crop from the right.
                The default is 0.
        """

        top_pixels: int = proto.Field(
            proto.INT32,
            number=1,
        )
        bottom_pixels: int = proto.Field(
            proto.INT32,
            number=2,
        )
        left_pixels: int = proto.Field(
            proto.INT32,
            number=3,
        )
        right_pixels: int = proto.Field(
            proto.INT32,
            number=4,
        )

    class Pad(proto.Message):
        r"""Pad filter configuration for the input video. The padded
        input video is scaled after padding with black to match the
        output resolution.

        Attributes:
            top_pixels (int):
                The number of pixels to add to the top. The
                default is 0.
            bottom_pixels (int):
                The number of pixels to add to the bottom.
                The default is 0.
            left_pixels (int):
                The number of pixels to add to the left. The
                default is 0.
            right_pixels (int):
                The number of pixels to add to the right. The
                default is 0.
        """

        top_pixels: int = proto.Field(
            proto.INT32,
            number=1,
        )
        bottom_pixels: int = proto.Field(
            proto.INT32,
            number=2,
        )
        left_pixels: int = proto.Field(
            proto.INT32,
            number=3,
        )
        right_pixels: int = proto.Field(
            proto.INT32,
            number=4,
        )

    audio: Audio = proto.Field(
        proto.MESSAGE,
        number=1,
        message=Audio,
    )
    crop: Crop = proto.Field(
        proto.MESSAGE,
        number=2,
        message=Crop,
    )
    pad: Pad = proto.Field(
        proto.MESSAGE,
        number=3,
        message=Pad,
    )


class VideoStream(proto.Message):
    r"""Video stream resource.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        h264 (google.cloud.video.live_stream_v1.types.VideoStream.H264CodecSettings):
            H264 codec settings.

            This field is a member of `oneof`_ ``codec_settings``.
    """

    class H264CodecSettings(proto.Message):
        r"""H264 codec settings.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            width_pixels (int):
                Required. The width of the video in pixels. Must be an even
                integer. Valid range is [320, 1920].
            height_pixels (int):
                Required. The height of the video in pixels. Must be an even
                integer. Valid range is [180, 1080].
            frame_rate (float):
                Required. The target video frame rate in frames per second
                (FPS). Must be less than or equal to 60. Will default to the
                input frame rate if larger than the input frame rate. The
                API will generate an output FPS that is divisible by the
                input FPS, and smaller or equal to the target FPS. See
                `Calculating frame
                rate <https://cloud.google.com/transcoder/docs/concepts/frame-rate>`__
                for more information.
            bitrate_bps (int):
                Required. The video bitrate in bits per
                second. Minimum value is 10,000.

                - For SD resolution (< 720p), must be <=
                  3,000,000 (3 Mbps).
                - For HD resolution (<= 1080p), must be <=
                  15,000,000 (15 Mbps).
            allow_open_gop (bool):
                Specifies whether an open Group of Pictures (GOP) structure
                should be allowed or not. The default is ``false``.
            gop_frame_count (int):
                Select the GOP size based on the specified frame count. If
                GOP frame count is set instead of GOP duration, GOP duration
                will be calculated by ``gopFrameCount``/``frameRate``. The
                calculated GOP duration must satisfy the limitations on
                ``gopDuration`` as well. Valid range is [60, 600].

                This field is a member of `oneof`_ ``gop_mode``.
            gop_duration (google.protobuf.duration_pb2.Duration):
                Select the GOP size based on the specified duration. The
                default is ``2s``. Note that ``gopDuration`` must be less
                than or equal to
                [segment_duration][google.cloud.video.livestream.v1.SegmentSettings.segment_duration],
                and
                [segment_duration][google.cloud.video.livestream.v1.SegmentSettings.segment_duration]
                must be divisible by ``gopDuration``. Valid range is [2s,
                20s].

                All video streams in the same channel must have the same GOP
                size.

                This field is a member of `oneof`_ ``gop_mode``.
            vbv_size_bits (int):
                Size of the Video Buffering Verifier (VBV) buffer in bits.
                Must be greater than zero. The default is equal to
                [bitrate_bps][google.cloud.video.livestream.v1.VideoStream.H264CodecSettings.bitrate_bps].
            vbv_fullness_bits (int):
                Initial fullness of the Video Buffering Verifier (VBV)
                buffer in bits. Must be greater than zero. The default is
                equal to 90% of
                [vbv_size_bits][google.cloud.video.livestream.v1.VideoStream.H264CodecSettings.vbv_size_bits].
            entropy_coder (str):
                The entropy coder to use. The default is ``cabac``.

                Supported entropy coders:

                -  ``cavlc``
                -  ``cabac``
            b_pyramid (bool):
                Allow B-pyramid for reference frame selection. This may not
                be supported on all decoders. The default is ``false``.
            b_frame_count (int):
                The number of consecutive B-frames. Must be greater than or
                equal to zero. Must be less than
                [gop_frame_count][google.cloud.video.livestream.v1.VideoStream.H264CodecSettings.gop_frame_count]
                if set. The default is 0.
            aq_strength (float):
                Specify the intensity of the adaptive
                quantizer (AQ). Must be between 0 and 1, where 0
                disables the quantizer and 1 maximizes the
                quantizer. A higher value equals a lower bitrate
                but smoother image. The default is 0.
            profile (str):
                Enforces the specified codec profile. The following profiles
                are supported:

                -  ``baseline``
                -  ``main`` (default)
                -  ``high``

                The available options are `FFmpeg-compatible Profile
                Options <https://trac.ffmpeg.org/wiki/Encode/H.264#Profile>`__.
                Note that certain values for this field may cause the
                transcoder to override other fields you set in the
                [H264CodecSettings][google.cloud.video.livestream.v1.VideoStream.H264CodecSettings]
                message.
            tune (str):
                Enforces the specified codec tune. The available options are
                `FFmpeg-compatible Encode
                Options <https://trac.ffmpeg.org/wiki/Encode/H.264#Tune>`__
                Note that certain values for this field may cause the
                transcoder to override other fields you set in the
                [H264CodecSettings][google.cloud.video.livestream.v1.VideoStream.H264CodecSettings]
                message.
        """

        width_pixels: int = proto.Field(
            proto.INT32,
            number=1,
        )
        height_pixels: int = proto.Field(
            proto.INT32,
            number=2,
        )
        frame_rate: float = proto.Field(
            proto.DOUBLE,
            number=3,
        )
        bitrate_bps: int = proto.Field(
            proto.INT32,
            number=4,
        )
        allow_open_gop: bool = proto.Field(
            proto.BOOL,
            number=6,
        )
        gop_frame_count: int = proto.Field(
            proto.INT32,
            number=7,
            oneof="gop_mode",
        )
        gop_duration: duration_pb2.Duration = proto.Field(
            proto.MESSAGE,
            number=8,
            oneof="gop_mode",
            message=duration_pb2.Duration,
        )
        vbv_size_bits: int = proto.Field(
            proto.INT32,
            number=9,
        )
        vbv_fullness_bits: int = proto.Field(
            proto.INT32,
            number=10,
        )
        entropy_coder: str = proto.Field(
            proto.STRING,
            number=11,
        )
        b_pyramid: bool = proto.Field(
            proto.BOOL,
            number=12,
        )
        b_frame_count: int = proto.Field(
            proto.INT32,
            number=13,
        )
        aq_strength: float = proto.Field(
            proto.DOUBLE,
            number=14,
        )
        profile: str = proto.Field(
            proto.STRING,
            number=15,
        )
        tune: str = proto.Field(
            proto.STRING,
            number=16,
        )

    h264: H264CodecSettings = proto.Field(
        proto.MESSAGE,
        number=20,
        oneof="codec_settings",
        message=H264CodecSettings,
    )


class AudioStream(proto.Message):
    r"""Audio stream resource.

    Attributes:
        transmux (bool):
            Specifies whether pass through (transmuxing) is enabled or
            not. If set to ``true``, the rest of the settings, other
            than ``mapping``, will be ignored. The default is ``false``.
        codec (str):
            The codec for this audio stream. The default is ``aac``.

            Supported audio codecs:

            -  ``aac``
        bitrate_bps (int):
            Required. Audio bitrate in bits per second.
            Must be between 1 and 10,000,000.
        channel_count (int):
            Number of audio channels. Must be between 1
            and 6. The default is 2.
        channel_layout (MutableSequence[str]):
            A list of channel names specifying layout of the audio
            channels. This only affects the metadata embedded in the
            container headers, if supported by the specified format. The
            default is ``[fl, fr]``.

            Supported channel names:

            -  ``fl`` - Front left channel
            -  ``fr`` - Front right channel
            -  ``sl`` - Side left channel
            -  ``sr`` - Side right channel
            -  ``fc`` - Front center channel
            -  ``lfe`` - Low frequency
        mapping_ (MutableSequence[google.cloud.video.live_stream_v1.types.AudioStream.AudioMapping]):
            The mapping for the input streams and audio
            channels.
        sample_rate_hertz (int):
            The audio sample rate in Hertz. The default
            is 48000 Hertz.
    """

    class AudioMapping(proto.Message):
        r"""The mapping for the input streams and audio channels.

        Attributes:
            input_key (str):
                Required. The ``Channel``
                [InputAttachment.key][google.cloud.video.livestream.v1.InputAttachment.key]
                that identifies the input that this audio mapping applies
                to. If an active input doesn't have an audio mapping, the
                primary audio track in the input stream will be selected.
            input_track (int):
                Required. The zero-based index of the track in the input
                stream. All
                [mapping][google.cloud.video.livestream.v1.AudioStream.mapping]s
                in the same
                [AudioStream][google.cloud.video.livestream.v1.AudioStream]
                must have the same input track.
            input_channel (int):
                Required. The zero-based index of the channel
                in the input stream.
            output_channel (int):
                Required. The zero-based index of the channel in the output
                audio stream. Must be consistent with the
                [input_channel][google.cloud.video.livestream.v1.AudioStream.AudioMapping.input_channel].
            gain_db (float):
                Audio volume control in dB. Negative values
                decrease volume, positive values increase. The
                default is 0.
        """

        input_key: str = proto.Field(
            proto.STRING,
            number=6,
        )
        input_track: int = proto.Field(
            proto.INT32,
            number=2,
        )
        input_channel: int = proto.Field(
            proto.INT32,
            number=3,
        )
        output_channel: int = proto.Field(
            proto.INT32,
            number=4,
        )
        gain_db: float = proto.Field(
            proto.DOUBLE,
            number=5,
        )

    transmux: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    codec: str = proto.Field(
        proto.STRING,
        number=1,
    )
    bitrate_bps: int = proto.Field(
        proto.INT32,
        number=2,
    )
    channel_count: int = proto.Field(
        proto.INT32,
        number=3,
    )
    channel_layout: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    mapping_: MutableSequence[AudioMapping] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=AudioMapping,
    )
    sample_rate_hertz: int = proto.Field(
        proto.INT32,
        number=6,
    )


class TextStream(proto.Message):
    r"""Encoding of a text stream. For example, closed captions or
    subtitles.

    Attributes:
        codec (str):
            Required. The codec for this text stream.

            Supported text codecs:

            -  ``cea608``
            -  ``cea708``
    """

    codec: str = proto.Field(
        proto.STRING,
        number=1,
    )


class SegmentSettings(proto.Message):
    r"""Segment settings for ``fmp4`` and ``ts``.

    Attributes:
        segment_duration (google.protobuf.duration_pb2.Duration):
            Duration of the segments in seconds. The default is ``6s``.
            Note that ``segmentDuration`` must be greater than or equal
            to
            [gop_duration][google.cloud.video.livestream.v1.VideoStream.H264CodecSettings.gop_duration],
            and ``segmentDuration`` must be divisible by
            [gop_duration][google.cloud.video.livestream.v1.VideoStream.H264CodecSettings.gop_duration].
            Valid range is [2s, 20s].

            All
            [mux_streams][google.cloud.video.livestream.v1.Manifest.mux_streams]
            in the same manifest must have the same segment duration.
    """

    segment_duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=1,
        message=duration_pb2.Duration,
    )


class TimecodeConfig(proto.Message):
    r"""Timecode configuration.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        source (google.cloud.video.live_stream_v1.types.TimecodeConfig.TimecodeSource):
            The source of the timecode that will later be
            used in outputs/manifests. It determines the
            initial timecode/timestamp (first frame) of
            output streams.
        utc_offset (google.protobuf.duration_pb2.Duration):
            UTC offset. Must be whole seconds, between
            -18 hours and +18 hours.

            This field is a member of `oneof`_ ``time_offset``.
        time_zone (google.type.datetime_pb2.TimeZone):
            Time zone e.g. "America/Los_Angeles".

            This field is a member of `oneof`_ ``time_offset``.
    """

    class TimecodeSource(proto.Enum):
        r"""The source of timecode.

        Values:
            TIMECODE_SOURCE_UNSPECIFIED (0):
                The timecode source is not specified.
            MEDIA_TIMESTAMP (1):
                Use input media timestamp.
            EMBEDDED_TIMECODE (2):
                Use input embedded timecode e.g. picture
                timing SEI message.
        """
        TIMECODE_SOURCE_UNSPECIFIED = 0
        MEDIA_TIMESTAMP = 1
        EMBEDDED_TIMECODE = 2

    source: TimecodeSource = proto.Field(
        proto.ENUM,
        number=1,
        enum=TimecodeSource,
    )
    utc_offset: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="time_offset",
        message=duration_pb2.Duration,
    )
    time_zone: datetime_pb2.TimeZone = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="time_offset",
        message=datetime_pb2.TimeZone,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
