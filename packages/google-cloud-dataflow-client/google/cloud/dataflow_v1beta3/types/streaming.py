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
import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.dataflow.v1beta3",
    manifest={
        "TopologyConfig",
        "PubsubLocation",
        "StreamingStageLocation",
        "StreamingSideInputLocation",
        "CustomSourceLocation",
        "StreamLocation",
        "StateFamilyConfig",
        "ComputationTopology",
        "KeyRangeLocation",
        "MountedDataDisk",
        "DataDiskAssignment",
        "KeyRangeDataDiskAssignment",
        "StreamingComputationRanges",
        "StreamingApplianceSnapshotConfig",
    },
)


class TopologyConfig(proto.Message):
    r"""Global topology of the streaming Dataflow job, including all
    computations and their sharded locations.

    Attributes:
        computations (Sequence[google.cloud.dataflow_v1beta3.types.ComputationTopology]):
            The computations associated with a streaming
            Dataflow job.
        data_disk_assignments (Sequence[google.cloud.dataflow_v1beta3.types.DataDiskAssignment]):
            The disks assigned to a streaming Dataflow
            job.
        user_stage_to_computation_name_map (Sequence[google.cloud.dataflow_v1beta3.types.TopologyConfig.UserStageToComputationNameMapEntry]):
            Maps user stage names to stable computation
            names.
        forwarding_key_bits (int):
            The size (in bits) of keys that will be
            assigned to source messages.
        persistent_state_version (int):
            Version number for persistent state.
    """

    computations = proto.RepeatedField(
        proto.MESSAGE, number=1, message="ComputationTopology",
    )
    data_disk_assignments = proto.RepeatedField(
        proto.MESSAGE, number=2, message="DataDiskAssignment",
    )
    user_stage_to_computation_name_map = proto.MapField(
        proto.STRING, proto.STRING, number=3,
    )
    forwarding_key_bits = proto.Field(proto.INT32, number=4,)
    persistent_state_version = proto.Field(proto.INT32, number=5,)


class PubsubLocation(proto.Message):
    r"""Identifies a pubsub location to use for transferring data
    into or out of a streaming Dataflow job.

    Attributes:
        topic (str):
            A pubsub topic, in the form of
            "pubsub.googleapis.com/topics/<project-id>/<topic-name>".
        subscription (str):
            A pubsub subscription, in the form of
            "pubsub.googleapis.com/subscriptions/<project-id>/<subscription-name>".
        timestamp_label (str):
            If set, contains a pubsub label from which to
            extract record timestamps. If left empty, record
            timestamps will be generated upon arrival.
        id_label (str):
            If set, contains a pubsub label from which to
            extract record ids. If left empty, record
            deduplication will be strictly best effort.
        drop_late_data (bool):
            Indicates whether the pipeline allows
            late-arriving data.
        tracking_subscription (str):
            If set, specifies the pubsub subscription
            that will be used for tracking custom time
            timestamps for watermark estimation.
        with_attributes (bool):
            If true, then the client has requested to get
            pubsub attributes.
    """

    topic = proto.Field(proto.STRING, number=1,)
    subscription = proto.Field(proto.STRING, number=2,)
    timestamp_label = proto.Field(proto.STRING, number=3,)
    id_label = proto.Field(proto.STRING, number=4,)
    drop_late_data = proto.Field(proto.BOOL, number=5,)
    tracking_subscription = proto.Field(proto.STRING, number=6,)
    with_attributes = proto.Field(proto.BOOL, number=7,)


class StreamingStageLocation(proto.Message):
    r"""Identifies the location of a streaming computation stage, for
    stage-to-stage communication.

    Attributes:
        stream_id (str):
            Identifies the particular stream within the
            streaming Dataflow job.
    """

    stream_id = proto.Field(proto.STRING, number=1,)


class StreamingSideInputLocation(proto.Message):
    r"""Identifies the location of a streaming side input.

    Attributes:
        tag (str):
            Identifies the particular side input within
            the streaming Dataflow job.
        state_family (str):
            Identifies the state family where this side
            input is stored.
    """

    tag = proto.Field(proto.STRING, number=1,)
    state_family = proto.Field(proto.STRING, number=2,)


class CustomSourceLocation(proto.Message):
    r"""Identifies the location of a custom souce.

    Attributes:
        stateful (bool):
            Whether this source is stateful.
    """

    stateful = proto.Field(proto.BOOL, number=1,)


class StreamLocation(proto.Message):
    r"""Describes a stream of data, either as input to be processed
    or as output of a streaming Dataflow job.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        streaming_stage_location (google.cloud.dataflow_v1beta3.types.StreamingStageLocation):
            The stream is part of another computation
            within the current streaming Dataflow job.

            This field is a member of `oneof`_ ``location``.
        pubsub_location (google.cloud.dataflow_v1beta3.types.PubsubLocation):
            The stream is a pubsub stream.

            This field is a member of `oneof`_ ``location``.
        side_input_location (google.cloud.dataflow_v1beta3.types.StreamingSideInputLocation):
            The stream is a streaming side input.

            This field is a member of `oneof`_ ``location``.
        custom_source_location (google.cloud.dataflow_v1beta3.types.CustomSourceLocation):
            The stream is a custom source.

            This field is a member of `oneof`_ ``location``.
    """

    streaming_stage_location = proto.Field(
        proto.MESSAGE, number=1, oneof="location", message="StreamingStageLocation",
    )
    pubsub_location = proto.Field(
        proto.MESSAGE, number=2, oneof="location", message="PubsubLocation",
    )
    side_input_location = proto.Field(
        proto.MESSAGE, number=3, oneof="location", message="StreamingSideInputLocation",
    )
    custom_source_location = proto.Field(
        proto.MESSAGE, number=4, oneof="location", message="CustomSourceLocation",
    )


class StateFamilyConfig(proto.Message):
    r"""State family configuration.

    Attributes:
        state_family (str):
            The state family value.
        is_read (bool):
            If true, this family corresponds to a read
            operation.
    """

    state_family = proto.Field(proto.STRING, number=1,)
    is_read = proto.Field(proto.BOOL, number=2,)


class ComputationTopology(proto.Message):
    r"""All configuration data for a particular Computation.

    Attributes:
        system_stage_name (str):
            The system stage name.
        computation_id (str):
            The ID of the computation.
        key_ranges (Sequence[google.cloud.dataflow_v1beta3.types.KeyRangeLocation]):
            The key ranges processed by the computation.
        inputs (Sequence[google.cloud.dataflow_v1beta3.types.StreamLocation]):
            The inputs to the computation.
        outputs (Sequence[google.cloud.dataflow_v1beta3.types.StreamLocation]):
            The outputs from the computation.
        state_families (Sequence[google.cloud.dataflow_v1beta3.types.StateFamilyConfig]):
            The state family values.
    """

    system_stage_name = proto.Field(proto.STRING, number=1,)
    computation_id = proto.Field(proto.STRING, number=5,)
    key_ranges = proto.RepeatedField(
        proto.MESSAGE, number=2, message="KeyRangeLocation",
    )
    inputs = proto.RepeatedField(proto.MESSAGE, number=3, message="StreamLocation",)
    outputs = proto.RepeatedField(proto.MESSAGE, number=4, message="StreamLocation",)
    state_families = proto.RepeatedField(
        proto.MESSAGE, number=7, message="StateFamilyConfig",
    )


class KeyRangeLocation(proto.Message):
    r"""Location information for a specific key-range of a sharded
    computation. Currently we only support UTF-8 character splits to
    simplify encoding into JSON.

    Attributes:
        start (str):
            The start (inclusive) of the key range.
        end (str):
            The end (exclusive) of the key range.
        delivery_endpoint (str):
            The physical location of this range
            assignment to be used for streaming computation
            cross-worker message delivery.
        data_disk (str):
            The name of the data disk where data for this
            range is stored. This name is local to the
            Google Cloud Platform project and uniquely
            identifies the disk within that project, for
            example
            "myproject-1014-104817-4c2-harness-0-disk-1".
        deprecated_persistent_directory (str):
            DEPRECATED. The location of the persistent
            state for this range, as a persistent directory
            in the worker local filesystem.
    """

    start = proto.Field(proto.STRING, number=1,)
    end = proto.Field(proto.STRING, number=2,)
    delivery_endpoint = proto.Field(proto.STRING, number=3,)
    data_disk = proto.Field(proto.STRING, number=5,)
    deprecated_persistent_directory = proto.Field(proto.STRING, number=4,)


class MountedDataDisk(proto.Message):
    r"""Describes mounted data disk.

    Attributes:
        data_disk (str):
            The name of the data disk.
            This name is local to the Google Cloud Platform
            project and uniquely identifies the disk within
            that project, for example
            "myproject-1014-104817-4c2-harness-0-disk-1".
    """

    data_disk = proto.Field(proto.STRING, number=1,)


class DataDiskAssignment(proto.Message):
    r"""Data disk assignment for a given VM instance.

    Attributes:
        vm_instance (str):
            VM instance name the data disks mounted to,
            for example
            "myproject-1014-104817-4c2-harness-0".
        data_disks (Sequence[str]):
            Mounted data disks. The order is important a
            data disk's 0-based index in this list defines
            which persistent directory the disk is mounted
            to, for example the list of {
            "myproject-1014-104817-4c2-harness-0-disk-0" },
            { "myproject-1014-104817-4c2-harness-0-disk-1"
            }.
    """

    vm_instance = proto.Field(proto.STRING, number=1,)
    data_disks = proto.RepeatedField(proto.STRING, number=2,)


class KeyRangeDataDiskAssignment(proto.Message):
    r"""Data disk assignment information for a specific key-range of
    a sharded computation.
    Currently we only support UTF-8 character splits to simplify
    encoding into JSON.

    Attributes:
        start (str):
            The start (inclusive) of the key range.
        end (str):
            The end (exclusive) of the key range.
        data_disk (str):
            The name of the data disk where data for this
            range is stored. This name is local to the
            Google Cloud Platform project and uniquely
            identifies the disk within that project, for
            example
            "myproject-1014-104817-4c2-harness-0-disk-1".
    """

    start = proto.Field(proto.STRING, number=1,)
    end = proto.Field(proto.STRING, number=2,)
    data_disk = proto.Field(proto.STRING, number=3,)


class StreamingComputationRanges(proto.Message):
    r"""Describes full or partial data disk assignment information of
    the computation ranges.

    Attributes:
        computation_id (str):
            The ID of the computation.
        range_assignments (Sequence[google.cloud.dataflow_v1beta3.types.KeyRangeDataDiskAssignment]):
            Data disk assignments for ranges from this
            computation.
    """

    computation_id = proto.Field(proto.STRING, number=1,)
    range_assignments = proto.RepeatedField(
        proto.MESSAGE, number=2, message="KeyRangeDataDiskAssignment",
    )


class StreamingApplianceSnapshotConfig(proto.Message):
    r"""Streaming appliance snapshot configuration.

    Attributes:
        snapshot_id (str):
            If set, indicates the snapshot id for the
            snapshot being performed.
        import_state_endpoint (str):
            Indicates which endpoint is used to import
            appliance state.
    """

    snapshot_id = proto.Field(proto.STRING, number=1,)
    import_state_endpoint = proto.Field(proto.STRING, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
