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
    package="google.cloud.batch.v1",
    manifest={
        "Volume",
        "NFS",
        "GCS",
    },
)


class Volume(proto.Message):
    r"""Volume and mount parameters to be associated with a TaskSpec.
    A TaskSpec might describe zero, one, or multiple volumes to be
    mounted as part of the task.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        nfs (google.cloud.batch_v1.types.NFS):
            An NFS source for the volume (could be a
            Filestore, for example).

            This field is a member of `oneof`_ ``source``.
        gcs (google.cloud.batch_v1.types.GCS):
            A Google Cloud Storage source for the volume.

            This field is a member of `oneof`_ ``source``.
        device_name (str):
            Device name of an attached disk

            This field is a member of `oneof`_ ``source``.
        mount_path (str):
            Mount path for the volume, e.g. /mnt/share
        mount_options (Sequence[str]):
            Mount options For Google Cloud Storage, mount options are
            the global options supported by gcsfuse tool. Batch will use
            them to mount the volume with the following command:
            "gcsfuse [global options] bucket mountpoint". For PD, NFS,
            mount options are these supported by /etc/fstab. Batch will
            use Fstab to mount such volumes.
            https://help.ubuntu.com/community/Fstab
    """

    nfs = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="source",
        message="NFS",
    )
    gcs = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="source",
        message="GCS",
    )
    device_name = proto.Field(
        proto.STRING,
        number=6,
        oneof="source",
    )
    mount_path = proto.Field(
        proto.STRING,
        number=4,
    )
    mount_options = proto.RepeatedField(
        proto.STRING,
        number=5,
    )


class NFS(proto.Message):
    r"""Represents an NFS server and remote path: :<remote_path>

    Attributes:
        server (str):
            URI of the NFS server, e.g. an IP address.
        remote_path (str):
            Remote source path exported from NFS, e.g.,
            "/share".
    """

    server = proto.Field(
        proto.STRING,
        number=1,
    )
    remote_path = proto.Field(
        proto.STRING,
        number=2,
    )


class GCS(proto.Message):
    r"""Represents a Google Cloud Storage volume source config.

    Attributes:
        remote_path (str):
            Remote path, either a bucket name or a subdirectory of a
            bucket, e.g.: bucket_name, bucket_name/subdirectory/
    """

    remote_path = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
