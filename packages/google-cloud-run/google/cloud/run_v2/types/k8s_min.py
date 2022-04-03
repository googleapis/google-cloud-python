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
    package="google.cloud.run.v2",
    manifest={
        "Container",
        "ResourceRequirements",
        "EnvVar",
        "EnvVarSource",
        "SecretKeySelector",
        "ContainerPort",
        "VolumeMount",
        "Volume",
        "SecretVolumeSource",
        "VersionToPath",
        "CloudSqlInstance",
    },
)


class Container(proto.Message):
    r"""A single application container.
    This specifies both the container to run, the command to run in
    the container and the arguments to supply to it.
    Note that additional arguments may be supplied by the system to
    the container at runtime.

    Attributes:
        name (str):
            Name of the container specified as a DNS_LABEL.
        image (str):
            Required. URL of the Container image in
            Google Container Registry or Docker More info:
            https://kubernetes.io/docs/concepts/containers/images
        command (Sequence[str]):
            Entrypoint array. Not executed within a shell. The docker
            image's ENTRYPOINT is used if this is not provided. Variable
            references $(VAR_NAME) are expanded using the container's
            environment. If a variable cannot be resolved, the reference
            in the input string will be unchanged. The $(VAR_NAME)
            syntax can be escaped with a double $$, ie: $$(VAR_NAME).
            Escaped references will never be expanded, regardless of
            whether the variable exists or not. More info:
            https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell
        args (Sequence[str]):
            Arguments to the entrypoint. The docker image's CMD is used
            if this is not provided. Variable references $(VAR_NAME) are
            expanded using the container's environment. If a variable
            cannot be resolved, the reference in the input string will
            be unchanged. The $(VAR_NAME) syntax can be escaped with a
            double $$, ie: $$(VAR_NAME). Escaped references will never
            be expanded, regardless of whether the variable exists or
            not. More info:
            https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell
        env (Sequence[google.cloud.run_v2.types.EnvVar]):
            List of environment variables to set in the
            container.
        resources (google.cloud.run_v2.types.ResourceRequirements):
            Compute Resource requirements by this
            container. More info:
            https://kubernetes.io/docs/concepts/storage/persistent-volumes#resources
        ports (Sequence[google.cloud.run_v2.types.ContainerPort]):
            List of ports to expose from the container.
            Only a single port can be specified. The
            specified ports must be listening on all
            interfaces (0.0.0.0) within the container to be
            accessible.
            If omitted, a port number will be chosen and
            passed to the container through the PORT
            environment variable for the container to listen
            on.
        volume_mounts (Sequence[google.cloud.run_v2.types.VolumeMount]):
            Volume to mount into the container's
            filesystem.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    image = proto.Field(
        proto.STRING,
        number=2,
    )
    command = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    args = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    env = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="EnvVar",
    )
    resources = proto.Field(
        proto.MESSAGE,
        number=6,
        message="ResourceRequirements",
    )
    ports = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="ContainerPort",
    )
    volume_mounts = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="VolumeMount",
    )


class ResourceRequirements(proto.Message):
    r"""ResourceRequirements describes the compute resource
    requirements.

    Attributes:
        limits (Sequence[google.cloud.run_v2.types.ResourceRequirements.LimitsEntry]):
            Only memory and CPU are supported. Note: The
            only supported values for CPU are '1', '2', and
            '4'. Setting 4 CPU requires at least 2Gi of
            memory.
            The values of the map is string form of the
            'quantity' k8s type:
            https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go
        cpu_idle (bool):
            Determines whether CPU should be throttled or
            not outside of requests.
    """

    limits = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )
    cpu_idle = proto.Field(
        proto.BOOL,
        number=2,
    )


class EnvVar(proto.Message):
    r"""EnvVar represents an environment variable present in a
    Container.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. Name of the environment variable. Must be a
            C_IDENTIFIER, and mnay not exceed 32768 characters.
        value (str):
            Variable references $(VAR_NAME) are expanded using the
            previous defined environment variables in the container and
            any route environment variables. If a variable cannot be
            resolved, the reference in the input string will be
            unchanged. The $(VAR_NAME) syntax can be escaped with a
            double $$, ie: $$(VAR_NAME). Escaped references will never
            be expanded, regardless of whether the variable exists or
            not. Defaults to "", and the maximum length is 32768 bytes.

            This field is a member of `oneof`_ ``values``.
        value_source (google.cloud.run_v2.types.EnvVarSource):
            Source for the environment variable's value.

            This field is a member of `oneof`_ ``values``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    value = proto.Field(
        proto.STRING,
        number=2,
        oneof="values",
    )
    value_source = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="values",
        message="EnvVarSource",
    )


class EnvVarSource(proto.Message):
    r"""EnvVarSource represents a source for the value of an EnvVar.

    Attributes:
        secret_key_ref (google.cloud.run_v2.types.SecretKeySelector):
            Selects a secret and a specific version from
            Cloud Secret Manager.
    """

    secret_key_ref = proto.Field(
        proto.MESSAGE,
        number=1,
        message="SecretKeySelector",
    )


class SecretKeySelector(proto.Message):
    r"""SecretEnvVarSource represents a source for the value of an
    EnvVar.

    Attributes:
        secret (str):
            Required. The name of the secret in Cloud Secret Manager.
            Format: {secret_name} if the secret is in the same project.
            projects/{project}/secrets/{secret_name} if the secret is in
            a different project.
        version (str):
            The Cloud Secret Manager secret version.
            Can be 'latest' for the latest value or an
            integer for a specific version.
    """

    secret = proto.Field(
        proto.STRING,
        number=1,
    )
    version = proto.Field(
        proto.STRING,
        number=2,
    )


class ContainerPort(proto.Message):
    r"""ContainerPort represents a network port in a single
    container.

    Attributes:
        name (str):
            If specified, used to specify which protocol
            to use. Allowed values are "http1" and "h2c".
        container_port (int):
            Port number the container listens on. This must be a valid
            TCP port number, 0 < container_port < 65536.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    container_port = proto.Field(
        proto.INT32,
        number=3,
    )


class VolumeMount(proto.Message):
    r"""VolumeMount describes a mounting of a Volume within a
    container.

    Attributes:
        name (str):
            Required. This must match the Name of a
            Volume.
        mount_path (str):
            Required. Path within the container at which the volume
            should be mounted. Must not contain ':'. For Cloud SQL
            volumes, it can be left empty, or must otherwise be
            ``/cloudsql``. All instances defined in the Volume will be
            available as ``/cloudsql/[instance]``. For more information
            on Cloud SQL volumes, visit
            https://cloud.google.com/sql/docs/mysql/connect-run
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    mount_path = proto.Field(
        proto.STRING,
        number=3,
    )


class Volume(proto.Message):
    r"""Volume represents a named volume in a container.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. Volume's name.
        secret (google.cloud.run_v2.types.SecretVolumeSource):
            Secret represents a secret that should
            populate this volume. More info:
            https://kubernetes.io/docs/concepts/storage/volumes#secret

            This field is a member of `oneof`_ ``volume_type``.
        cloud_sql_instance (google.cloud.run_v2.types.CloudSqlInstance):
            For Cloud SQL volumes, contains the specific
            instances that should be mounted. Visit
            https://cloud.google.com/sql/docs/mysql/connect-run
            for more information on how to connect Cloud SQL
            and Cloud Run.

            This field is a member of `oneof`_ ``volume_type``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    secret = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="volume_type",
        message="SecretVolumeSource",
    )
    cloud_sql_instance = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="volume_type",
        message="CloudSqlInstance",
    )


class SecretVolumeSource(proto.Message):
    r"""The secret's value will be presented as the content of a file
    whose name is defined in the item path. If no items are defined,
    the name of the file is the secret.

    Attributes:
        secret (str):
            Required. The name of the secret in Cloud
            Secret Manager. Format: {secret} if the secret
            is in the same project.
            projects/{project}/secrets/{secret} if the
            secret is in a different project.
        items (Sequence[google.cloud.run_v2.types.VersionToPath]):
            If unspecified, the volume will expose a file whose name is
            the secret, relative to VolumeMount.mount_path. If
            specified, the key will be used as the version to fetch from
            Cloud Secret Manager and the path will be the name of the
            file exposed in the volume. When items are defined, they
            must specify a path and a version.
        default_mode (int):
            Integer representation of mode bits to use on created files
            by default. Must be a value between 0000 and 0777 (octal),
            defaulting to 0644. Directories within the path are not
            affected by this setting.

            Notes

            -  Internally, a umask of 0222 will be applied to any
               non-zero value.
            -  This is an integer representation of the mode bits. So,
               the octal integer value should look exactly as the chmod
               numeric notation with a leading zero. Some examples: for
               chmod 777 (a=rwx), set to 0777 (octal) or 511 (base-10).
               For chmod 640 (u=rw,g=r), set to 0640 (octal) or 416
               (base-10). For chmod 755 (u=rwx,g=rx,o=rx), set to 0755
               (octal) or 493 (base-10).
            -  This might be in conflict with other options that affect
               the file mode, like fsGroup, and the result can be other
               mode bits set.

            This might be in conflict with other options that affect the
            file mode, like fsGroup, and as a result, other mode bits
            could be set.
    """

    secret = proto.Field(
        proto.STRING,
        number=1,
    )
    items = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="VersionToPath",
    )
    default_mode = proto.Field(
        proto.INT32,
        number=3,
    )


class VersionToPath(proto.Message):
    r"""VersionToPath maps a specific version of a secret to a relative file
    to mount to, relative to VolumeMount's mount_path.

    Attributes:
        path (str):
            Required. The relative path of the secret in
            the container.
        version (str):
            The Cloud Secret Manager secret version.
            Can be 'latest' for the latest value or an
            integer for a specific version.
        mode (int):
            Integer octal mode bits to use on this file, must be a value
            between 01 and 0777 (octal). If 0 or not set, the Volume's
            default mode will be used.

            Notes

            -  Internally, a umask of 0222 will be applied to any
               non-zero value.
            -  This is an integer representation of the mode bits. So,
               the octal integer value should look exactly as the chmod
               numeric notation with a leading zero. Some examples: for
               chmod 777 (a=rwx), set to 0777 (octal) or 511 (base-10).
               For chmod 640 (u=rw,g=r), set to 0640 (octal) or 416
               (base-10). For chmod 755 (u=rwx,g=rx,o=rx), set to 0755
               (octal) or 493 (base-10).
            -  This might be in conflict with other options that affect
               the file mode, like fsGroup, and the result can be other
               mode bits set.
    """

    path = proto.Field(
        proto.STRING,
        number=1,
    )
    version = proto.Field(
        proto.STRING,
        number=2,
    )
    mode = proto.Field(
        proto.INT32,
        number=3,
    )


class CloudSqlInstance(proto.Message):
    r"""Represents a specific Cloud SQL instance.

    Attributes:
        connections (Sequence[str]):
            The Cloud SQL instance connection names, as
            can be found in
            https://console.cloud.google.com/sql/instances.
            Visit
            https://cloud.google.com/sql/docs/mysql/connect-run
            for more information on how to connect Cloud SQL
            and Cloud Run. Format:
            {project}:{location}:{instance}
    """

    connections = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
