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


from google.protobuf import field_mask_pb2 as gp_field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.spanner.admin.instance.v1",
    manifest={
        "ReplicaInfo",
        "InstanceConfig",
        "Instance",
        "ListInstanceConfigsRequest",
        "ListInstanceConfigsResponse",
        "GetInstanceConfigRequest",
        "GetInstanceRequest",
        "CreateInstanceRequest",
        "ListInstancesRequest",
        "ListInstancesResponse",
        "UpdateInstanceRequest",
        "DeleteInstanceRequest",
        "CreateInstanceMetadata",
        "UpdateInstanceMetadata",
    },
)


class ReplicaInfo(proto.Message):
    r"""

    Attributes:
        location (str):
            The location of the serving resources, e.g.
            "us-central1".
        type_ (~.spanner_instance_admin.ReplicaInfo.ReplicaType):
            The type of replica.
        default_leader_location (bool):
            If true, this location is designated as the default leader
            location where leader replicas are placed. See the `region
            types
            documentation <https://cloud.google.com/spanner/docs/instances#region_types>`__
            for more details.
    """

    class ReplicaType(proto.Enum):
        r"""Indicates the type of replica. See the `replica types
        documentation <https://cloud.google.com/spanner/docs/replication#replica_types>`__
        for more details.
        """
        TYPE_UNSPECIFIED = 0
        READ_WRITE = 1
        READ_ONLY = 2
        WITNESS = 3

    location = proto.Field(proto.STRING, number=1)

    type_ = proto.Field(proto.ENUM, number=2, enum=ReplicaType,)

    default_leader_location = proto.Field(proto.BOOL, number=3)


class InstanceConfig(proto.Message):
    r"""A possible configuration for a Cloud Spanner instance.
    Configurations define the geographic placement of nodes and
    their replication.

    Attributes:
        name (str):
            A unique identifier for the instance configuration. Values
            are of the form
            ``projects/<project>/instanceConfigs/[a-z][-a-z0-9]*``
        display_name (str):
            The name of this instance configuration as it
            appears in UIs.
        replicas (Sequence[~.spanner_instance_admin.ReplicaInfo]):
            The geographic placement of nodes in this
            instance configuration and their replication
            properties.
    """

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    replicas = proto.RepeatedField(proto.MESSAGE, number=3, message="ReplicaInfo",)


class Instance(proto.Message):
    r"""An isolated set of Cloud Spanner resources on which databases
    can be hosted.

    Attributes:
        name (str):
            Required. A unique identifier for the instance, which cannot
            be changed after the instance is created. Values are of the
            form
            ``projects/<project>/instances/[a-z][-a-z0-9]*[a-z0-9]``.
            The final segment of the name must be between 2 and 64
            characters in length.
        config (str):
            Required. The name of the instance's configuration. Values
            are of the form
            ``projects/<project>/instanceConfigs/<configuration>``. See
            also
            [InstanceConfig][google.spanner.admin.instance.v1.InstanceConfig]
            and
            [ListInstanceConfigs][google.spanner.admin.instance.v1.InstanceAdmin.ListInstanceConfigs].
        display_name (str):
            Required. The descriptive name for this
            instance as it appears in UIs. Must be unique
            per project and between 4 and 30 characters in
            length.
        node_count (int):
            Required. The number of nodes allocated to this instance.
            This may be zero in API responses for instances that are not
            yet in state ``READY``.

            See `the
            documentation <https://cloud.google.com/spanner/docs/instances#node_count>`__
            for more information about nodes.
        state (~.spanner_instance_admin.Instance.State):
            Output only. The current instance state. For
            [CreateInstance][google.spanner.admin.instance.v1.InstanceAdmin.CreateInstance],
            the state must be either omitted or set to ``CREATING``. For
            [UpdateInstance][google.spanner.admin.instance.v1.InstanceAdmin.UpdateInstance],
            the state must be either omitted or set to ``READY``.
        labels (Sequence[~.spanner_instance_admin.Instance.LabelsEntry]):
            Cloud Labels are a flexible and lightweight mechanism for
            organizing cloud resources into groups that reflect a
            customer's organizational needs and deployment strategies.
            Cloud Labels can be used to filter collections of resources.
            They can be used to control how resource metrics are
            aggregated. And they can be used as arguments to policy
            management rules (e.g. route, firewall, load balancing,
            etc.).

            -  Label keys must be between 1 and 63 characters long and
               must conform to the following regular expression:
               ``[a-z]([-a-z0-9]*[a-z0-9])?``.
            -  Label values must be between 0 and 63 characters long and
               must conform to the regular expression
               ``([a-z]([-a-z0-9]*[a-z0-9])?)?``.
            -  No more than 64 labels can be associated with a given
               resource.

            See https://goo.gl/xmQnxf for more information on and
            examples of labels.

            If you plan to use labels in your own code, please note that
            additional characters may be allowed in the future. And so
            you are advised to use an internal label representation,
            such as JSON, which doesn't rely upon specific characters
            being disallowed. For example, representing labels as the
            string: name + "*" + value would prove problematic if we
            were to allow "*" in a future release.
        endpoint_uris (Sequence[str]):
            Deprecated. This field is not populated.
    """

    class State(proto.Enum):
        r"""Indicates the current state of the instance."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2

    name = proto.Field(proto.STRING, number=1)

    config = proto.Field(proto.STRING, number=2)

    display_name = proto.Field(proto.STRING, number=3)

    node_count = proto.Field(proto.INT32, number=5)

    state = proto.Field(proto.ENUM, number=6, enum=State,)

    labels = proto.MapField(proto.STRING, proto.STRING, number=7)

    endpoint_uris = proto.RepeatedField(proto.STRING, number=8)


class ListInstanceConfigsRequest(proto.Message):
    r"""The request for
    [ListInstanceConfigs][google.spanner.admin.instance.v1.InstanceAdmin.ListInstanceConfigs].

    Attributes:
        parent (str):
            Required. The name of the project for which a list of
            supported instance configurations is requested. Values are
            of the form ``projects/<project>``.
        page_size (int):
            Number of instance configurations to be
            returned in the response. If 0 or less, defaults
            to the server's maximum allowed page size.
        page_token (str):
            If non-empty, ``page_token`` should contain a
            [next_page_token][google.spanner.admin.instance.v1.ListInstanceConfigsResponse.next_page_token]
            from a previous
            [ListInstanceConfigsResponse][google.spanner.admin.instance.v1.ListInstanceConfigsResponse].
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListInstanceConfigsResponse(proto.Message):
    r"""The response for
    [ListInstanceConfigs][google.spanner.admin.instance.v1.InstanceAdmin.ListInstanceConfigs].

    Attributes:
        instance_configs (Sequence[~.spanner_instance_admin.InstanceConfig]):
            The list of requested instance
            configurations.
        next_page_token (str):
            ``next_page_token`` can be sent in a subsequent
            [ListInstanceConfigs][google.spanner.admin.instance.v1.InstanceAdmin.ListInstanceConfigs]
            call to fetch more of the matching instance configurations.
    """

    @property
    def raw_page(self):
        return self

    instance_configs = proto.RepeatedField(
        proto.MESSAGE, number=1, message="InstanceConfig",
    )

    next_page_token = proto.Field(proto.STRING, number=2)


class GetInstanceConfigRequest(proto.Message):
    r"""The request for
    [GetInstanceConfigRequest][google.spanner.admin.instance.v1.InstanceAdmin.GetInstanceConfig].

    Attributes:
        name (str):
            Required. The name of the requested instance configuration.
            Values are of the form
            ``projects/<project>/instanceConfigs/<config>``.
    """

    name = proto.Field(proto.STRING, number=1)


class GetInstanceRequest(proto.Message):
    r"""The request for
    [GetInstance][google.spanner.admin.instance.v1.InstanceAdmin.GetInstance].

    Attributes:
        name (str):
            Required. The name of the requested instance. Values are of
            the form ``projects/<project>/instances/<instance>``.
        field_mask (~.gp_field_mask.FieldMask):
            If field_mask is present, specifies the subset of
            [Instance][google.spanner.admin.instance.v1.Instance] fields
            that should be returned. If absent, all
            [Instance][google.spanner.admin.instance.v1.Instance] fields
            are returned.
    """

    name = proto.Field(proto.STRING, number=1)

    field_mask = proto.Field(proto.MESSAGE, number=2, message=gp_field_mask.FieldMask,)


class CreateInstanceRequest(proto.Message):
    r"""The request for
    [CreateInstance][google.spanner.admin.instance.v1.InstanceAdmin.CreateInstance].

    Attributes:
        parent (str):
            Required. The name of the project in which to create the
            instance. Values are of the form ``projects/<project>``.
        instance_id (str):
            Required. The ID of the instance to create. Valid
            identifiers are of the form ``[a-z][-a-z0-9]*[a-z0-9]`` and
            must be between 2 and 64 characters in length.
        instance (~.spanner_instance_admin.Instance):
            Required. The instance to create. The name may be omitted,
            but if specified must be
            ``<parent>/instances/<instance_id>``.
    """

    parent = proto.Field(proto.STRING, number=1)

    instance_id = proto.Field(proto.STRING, number=2)

    instance = proto.Field(proto.MESSAGE, number=3, message="Instance",)


class ListInstancesRequest(proto.Message):
    r"""The request for
    [ListInstances][google.spanner.admin.instance.v1.InstanceAdmin.ListInstances].

    Attributes:
        parent (str):
            Required. The name of the project for which a list of
            instances is requested. Values are of the form
            ``projects/<project>``.
        page_size (int):
            Number of instances to be returned in the
            response. If 0 or less, defaults to the server's
            maximum allowed page size.
        page_token (str):
            If non-empty, ``page_token`` should contain a
            [next_page_token][google.spanner.admin.instance.v1.ListInstancesResponse.next_page_token]
            from a previous
            [ListInstancesResponse][google.spanner.admin.instance.v1.ListInstancesResponse].
        filter (str):
            An expression for filtering the results of the request.
            Filter rules are case insensitive. The fields eligible for
            filtering are:

            -  ``name``
            -  ``display_name``
            -  ``labels.key`` where key is the name of a label

            Some examples of using filters are:

            -  ``name:*`` --> The instance has a name.
            -  ``name:Howl`` --> The instance's name contains the string
               "howl".
            -  ``name:HOWL`` --> Equivalent to above.
            -  ``NAME:howl`` --> Equivalent to above.
            -  ``labels.env:*`` --> The instance has the label "env".
            -  ``labels.env:dev`` --> The instance has the label "env"
               and the value of the label contains the string "dev".
            -  ``name:howl labels.env:dev`` --> The instance's name
               contains "howl" and it has the label "env" with its value
               containing "dev".
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)

    filter = proto.Field(proto.STRING, number=4)


class ListInstancesResponse(proto.Message):
    r"""The response for
    [ListInstances][google.spanner.admin.instance.v1.InstanceAdmin.ListInstances].

    Attributes:
        instances (Sequence[~.spanner_instance_admin.Instance]):
            The list of requested instances.
        next_page_token (str):
            ``next_page_token`` can be sent in a subsequent
            [ListInstances][google.spanner.admin.instance.v1.InstanceAdmin.ListInstances]
            call to fetch more of the matching instances.
    """

    @property
    def raw_page(self):
        return self

    instances = proto.RepeatedField(proto.MESSAGE, number=1, message="Instance",)

    next_page_token = proto.Field(proto.STRING, number=2)


class UpdateInstanceRequest(proto.Message):
    r"""The request for
    [UpdateInstance][google.spanner.admin.instance.v1.InstanceAdmin.UpdateInstance].

    Attributes:
        instance (~.spanner_instance_admin.Instance):
            Required. The instance to update, which must always include
            the instance name. Otherwise, only fields mentioned in
            [field_mask][google.spanner.admin.instance.v1.UpdateInstanceRequest.field_mask]
            need be included.
        field_mask (~.gp_field_mask.FieldMask):
            Required. A mask specifying which fields in
            [Instance][google.spanner.admin.instance.v1.Instance] should
            be updated. The field mask must always be specified; this
            prevents any future fields in
            [Instance][google.spanner.admin.instance.v1.Instance] from
            being erased accidentally by clients that do not know about
            them.
    """

    instance = proto.Field(proto.MESSAGE, number=1, message="Instance",)

    field_mask = proto.Field(proto.MESSAGE, number=2, message=gp_field_mask.FieldMask,)


class DeleteInstanceRequest(proto.Message):
    r"""The request for
    [DeleteInstance][google.spanner.admin.instance.v1.InstanceAdmin.DeleteInstance].

    Attributes:
        name (str):
            Required. The name of the instance to be deleted. Values are
            of the form ``projects/<project>/instances/<instance>``
    """

    name = proto.Field(proto.STRING, number=1)


class CreateInstanceMetadata(proto.Message):
    r"""Metadata type for the operation returned by
    [CreateInstance][google.spanner.admin.instance.v1.InstanceAdmin.CreateInstance].

    Attributes:
        instance (~.spanner_instance_admin.Instance):
            The instance being created.
        start_time (~.timestamp.Timestamp):
            The time at which the
            [CreateInstance][google.spanner.admin.instance.v1.InstanceAdmin.CreateInstance]
            request was received.
        cancel_time (~.timestamp.Timestamp):
            The time at which this operation was
            cancelled. If set, this operation is in the
            process of undoing itself (which is guaranteed
            to succeed) and cannot be cancelled again.
        end_time (~.timestamp.Timestamp):
            The time at which this operation failed or
            was completed successfully.
    """

    instance = proto.Field(proto.MESSAGE, number=1, message="Instance",)

    start_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)

    cancel_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)

    end_time = proto.Field(proto.MESSAGE, number=4, message=timestamp.Timestamp,)


class UpdateInstanceMetadata(proto.Message):
    r"""Metadata type for the operation returned by
    [UpdateInstance][google.spanner.admin.instance.v1.InstanceAdmin.UpdateInstance].

    Attributes:
        instance (~.spanner_instance_admin.Instance):
            The desired end state of the update.
        start_time (~.timestamp.Timestamp):
            The time at which
            [UpdateInstance][google.spanner.admin.instance.v1.InstanceAdmin.UpdateInstance]
            request was received.
        cancel_time (~.timestamp.Timestamp):
            The time at which this operation was
            cancelled. If set, this operation is in the
            process of undoing itself (which is guaranteed
            to succeed) and cannot be cancelled again.
        end_time (~.timestamp.Timestamp):
            The time at which this operation failed or
            was completed successfully.
    """

    instance = proto.Field(proto.MESSAGE, number=1, message="Instance",)

    start_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)

    cancel_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)

    end_time = proto.Field(proto.MESSAGE, number=4, message=timestamp.Timestamp,)


__all__ = tuple(sorted(__protobuf__.manifest))
