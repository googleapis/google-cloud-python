# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import code_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.eventarc.v1",
    manifest={
        "Trigger",
        "EventFilter",
        "StateCondition",
        "Destination",
        "Transport",
        "CloudRun",
        "GKE",
        "Pubsub",
    },
)


class Trigger(proto.Message):
    r"""A representation of the trigger resource.

    Attributes:
        name (str):
            Required. The resource name of the trigger. Must be unique
            within the location of the project and must be in
            ``projects/{project}/locations/{location}/triggers/{trigger}``
            format.
        uid (str):
            Output only. Server-assigned unique
            identifier for the trigger. The value is a UUID4
            string and guaranteed to remain unchanged until
            the resource is deleted.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last-modified time.
        event_filters (MutableSequence[google.cloud.eventarc_v1.types.EventFilter]):
            Required. Unordered list. The list of filters
            that applies to event attributes. Only events
            that match all the provided filters are sent to
            the destination.
        service_account (str):
            Optional. The IAM service account email associated with the
            trigger. The service account represents the identity of the
            trigger.

            The principal who calls this API must have the
            ``iam.serviceAccounts.actAs`` permission in the service
            account. See
            https://cloud.google.com/iam/docs/understanding-service-accounts?hl=en#sa_common
            for more information.

            For Cloud Run destinations, this service account is used to
            generate identity tokens when invoking the service. See
            https://cloud.google.com/run/docs/triggering/pubsub-push#create-service-account
            for information on how to invoke authenticated Cloud Run
            services. To create Audit Log triggers, the service account
            should also have the ``roles/eventarc.eventReceiver`` IAM
            role.
        destination (google.cloud.eventarc_v1.types.Destination):
            Required. Destination specifies where the
            events should be sent to.
        transport (google.cloud.eventarc_v1.types.Transport):
            Optional. To deliver messages, Eventarc might
            use other GCP products as a transport
            intermediary. This field contains a reference to
            that transport intermediary. This information
            can be used for debugging purposes.
        labels (MutableMapping[str, str]):
            Optional. User labels attached to the
            triggers that can be used to group resources.
        channel (str):
            Optional. The name of the channel associated with the
            trigger in
            ``projects/{project}/locations/{location}/channels/{channel}``
            format. You must provide a channel to receive events from
            Eventarc SaaS partners.
        conditions (MutableMapping[str, google.cloud.eventarc_v1.types.StateCondition]):
            Output only. The reason(s) why a trigger is
            in FAILED state.
        etag (str):
            Output only. This checksum is computed by the
            server based on the value of other fields, and
            might be sent only on create requests to ensure
            that the client has an up-to-date value before
            proceeding.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    event_filters: MutableSequence["EventFilter"] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="EventFilter",
    )
    service_account: str = proto.Field(
        proto.STRING,
        number=9,
    )
    destination: "Destination" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="Destination",
    )
    transport: "Transport" = proto.Field(
        proto.MESSAGE,
        number=11,
        message="Transport",
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=12,
    )
    channel: str = proto.Field(
        proto.STRING,
        number=13,
    )
    conditions: MutableMapping[str, "StateCondition"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=15,
        message="StateCondition",
    )
    etag: str = proto.Field(
        proto.STRING,
        number=99,
    )


class EventFilter(proto.Message):
    r"""Filters events based on exact matches on the CloudEvents
    attributes.

    Attributes:
        attribute (str):
            Required. The name of a CloudEvents
            attribute. Currently, only a subset of
            attributes are supported for filtering.
            All triggers MUST provide a filter for the
            'type' attribute.
        value (str):
            Required. The value for the attribute.
        operator (str):
            Optional. The operator used for matching the events with the
            value of the filter. If not specified, only events that have
            an exact key-value pair specified in the filter are matched.
            The only allowed value is ``match-path-pattern``.
    """

    attribute: str = proto.Field(
        proto.STRING,
        number=1,
    )
    value: str = proto.Field(
        proto.STRING,
        number=2,
    )
    operator: str = proto.Field(
        proto.STRING,
        number=3,
    )


class StateCondition(proto.Message):
    r"""A condition that is part of the trigger state computation.

    Attributes:
        code (google.rpc.code_pb2.Code):
            The canonical code of the condition.
        message (str):
            Human-readable message.
    """

    code: code_pb2.Code = proto.Field(
        proto.ENUM,
        number=1,
        enum=code_pb2.Code,
    )
    message: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Destination(proto.Message):
    r"""Represents a target of an invocation over HTTP.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        cloud_run (google.cloud.eventarc_v1.types.CloudRun):
            Cloud Run fully-managed resource that
            receives the events. The resource should be in
            the same project as the trigger.

            This field is a member of `oneof`_ ``descriptor``.
        cloud_function (str):
            The Cloud Function resource name. Only Cloud Functions V2 is
            supported. Format:
            ``projects/{project}/locations/{location}/functions/{function}``

            This field is a member of `oneof`_ ``descriptor``.
        gke (google.cloud.eventarc_v1.types.GKE):
            A GKE service capable of receiving events.
            The service should be running in the same
            project as the trigger.

            This field is a member of `oneof`_ ``descriptor``.
        workflow (str):
            The resource name of the Workflow whose Executions are
            triggered by the events. The Workflow resource should be
            deployed in the same project as the trigger. Format:
            ``projects/{project}/locations/{location}/workflows/{workflow}``

            This field is a member of `oneof`_ ``descriptor``.
    """

    cloud_run: "CloudRun" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="descriptor",
        message="CloudRun",
    )
    cloud_function: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="descriptor",
    )
    gke: "GKE" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="descriptor",
        message="GKE",
    )
    workflow: str = proto.Field(
        proto.STRING,
        number=4,
        oneof="descriptor",
    )


class Transport(proto.Message):
    r"""Represents the transport intermediaries created for the
    trigger to deliver events.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        pubsub (google.cloud.eventarc_v1.types.Pubsub):
            The Pub/Sub topic and subscription used by
            Eventarc as a transport intermediary.

            This field is a member of `oneof`_ ``intermediary``.
    """

    pubsub: "Pubsub" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="intermediary",
        message="Pubsub",
    )


class CloudRun(proto.Message):
    r"""Represents a Cloud Run destination.

    Attributes:
        service (str):
            Required. The name of the Cloud Run service
            being addressed. See
            https://cloud.google.com/run/docs/reference/rest/v1/namespaces.services.
            Only services located in the same project as the
            trigger object can be addressed.
        path (str):
            Optional. The relative path on the Cloud Run
            service the events should be sent to.
            The value must conform to the definition of a
            URI path segment (section 3.3 of RFC2396).
            Examples: "/route", "route", "route/subroute".
        region (str):
            Required. The region the Cloud Run service is
            deployed in.
    """

    service: str = proto.Field(
        proto.STRING,
        number=1,
    )
    path: str = proto.Field(
        proto.STRING,
        number=2,
    )
    region: str = proto.Field(
        proto.STRING,
        number=3,
    )


class GKE(proto.Message):
    r"""Represents a GKE destination.

    Attributes:
        cluster (str):
            Required. The name of the cluster the GKE
            service is running in. The cluster must be
            running in the same project as the trigger being
            created.
        location (str):
            Required. The name of the Google Compute
            Engine in which the cluster resides, which can
            either be compute zone (for example,
            us-central1-a) for the zonal clusters or region
            (for example, us-central1) for regional
            clusters.
        namespace (str):
            Required. The namespace the GKE service is
            running in.
        service (str):
            Required. Name of the GKE service.
        path (str):
            Optional. The relative path on the GKE
            service the events should be sent to.
            The value must conform to the definition of a
            URI path segment (section 3.3 of RFC2396).
            Examples: "/route", "route", "route/subroute".
    """

    cluster: str = proto.Field(
        proto.STRING,
        number=1,
    )
    location: str = proto.Field(
        proto.STRING,
        number=2,
    )
    namespace: str = proto.Field(
        proto.STRING,
        number=3,
    )
    service: str = proto.Field(
        proto.STRING,
        number=4,
    )
    path: str = proto.Field(
        proto.STRING,
        number=5,
    )


class Pubsub(proto.Message):
    r"""Represents a Pub/Sub transport.

    Attributes:
        topic (str):
            Optional. The name of the Pub/Sub topic created and managed
            by Eventarc as a transport for the event delivery. Format:
            ``projects/{PROJECT_ID}/topics/{TOPIC_NAME}``.

            You can set an existing topic for triggers of the type
            ``google.cloud.pubsub.topic.v1.messagePublished``. The topic
            you provide here is not deleted by Eventarc at trigger
            deletion.
        subscription (str):
            Output only. The name of the Pub/Sub subscription created
            and managed by Eventarc as a transport for the event
            delivery. Format:
            ``projects/{PROJECT_ID}/subscriptions/{SUBSCRIPTION_NAME}``.
    """

    topic: str = proto.Field(
        proto.STRING,
        number=1,
    )
    subscription: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
