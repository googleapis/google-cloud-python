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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.eventarc.v1',
    manifest={
        'Trigger',
        'EventFilter',
        'Destination',
        'Transport',
        'CloudRun',
        'Pubsub',
    },
)


class Trigger(proto.Message):
    r"""A representation of the trigger resource.

    Attributes:
        name (str):
            Required. The resource name of the trigger. Must be unique
            within the location on the project and must be in
            ``projects/{project}/locations/{location}/triggers/{trigger}``
            format.
        uid (str):
            Output only. Server assigned unique
            identifier for the trigger. The value is a UUID4
            string and guaranteed to remain unchanged until
            the resource is deleted.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last-modified time.
        event_filters (Sequence[google.cloud.eventarc_v1.types.EventFilter]):
            Required. null The list of filters that
            applies to event attributes. Only events that
            match all the provided filters will be sent to
            the destination.
        service_account (str):
            Optional. The IAM service account email associated with the
            trigger. The service account represents the identity of the
            trigger.

            The principal who calls this API must have
            ``iam.serviceAccounts.actAs`` permission in the service
            account. See
            https://cloud.google.com/iam/docs/understanding-service-accounts?hl=en#sa_common
            for more information.

            For Cloud Run destinations, this service account is used to
            generate identity tokens when invoking the service. See
            https://cloud.google.com/run/docs/triggering/pubsub-push#create-service-account
            for information on how to invoke authenticated Cloud Run
            services. In order to create Audit Log triggers, the service
            account should also have ``roles/eventarc.eventReceiver``
            IAM role.
        destination (google.cloud.eventarc_v1.types.Destination):
            Required. Destination specifies where the
            events should be sent to.
        transport (google.cloud.eventarc_v1.types.Transport):
            Optional. In order to deliver messages,
            Eventarc may use other GCP products as transport
            intermediary. This field contains a reference to
            that transport intermediary. This information
            can be used for debugging purposes.
        labels (Mapping[str, str]):
            Optional. User labels attached to the
            triggers that can be used to group resources.
        etag (str):
            Output only. This checksum is computed by the
            server based on the value of other fields, and
            may be sent only on create requests to ensure
            the client has an up-to-date value before
            proceeding.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    uid = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    event_filters = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message='EventFilter',
    )
    service_account = proto.Field(
        proto.STRING,
        number=9,
    )
    destination = proto.Field(
        proto.MESSAGE,
        number=10,
        message='Destination',
    )
    transport = proto.Field(
        proto.MESSAGE,
        number=11,
        message='Transport',
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=12,
    )
    etag = proto.Field(
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
    """

    attribute = proto.Field(
        proto.STRING,
        number=1,
    )
    value = proto.Field(
        proto.STRING,
        number=2,
    )


class Destination(proto.Message):
    r"""Represents a target of an invocation over HTTP.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        cloud_run (google.cloud.eventarc_v1.types.CloudRun):
            Cloud Run fully-managed service that receives
            the events. The service should be running in the
            same project of the trigger.

            This field is a member of `oneof`_ ``descriptor``.
    """

    cloud_run = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof='descriptor',
        message='CloudRun',
    )


class Transport(proto.Message):
    r"""Represents the transport intermediaries created for the
    trigger in order to deliver events.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        pubsub (google.cloud.eventarc_v1.types.Pubsub):
            The Pub/Sub topic and subscription used by
            Eventarc as delivery intermediary.

            This field is a member of `oneof`_ ``intermediary``.
    """

    pubsub = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof='intermediary',
        message='Pubsub',
    )


class CloudRun(proto.Message):
    r"""Represents a Cloud Run destination.

    Attributes:
        service (str):
            Required. The name of the Cloud Run service
            being addressed. See
            https://cloud.google.com/run/docs/reference/rest/v1/namespaces.services.
            Only services located in the same project of the
            trigger object can be addressed.
        path (str):
            Optional. The relative path on the Cloud Run
            service the events should be sent to.

            The value must conform to the definition of URI
            path segment (section 3.3 of RFC2396). Examples:
            "/route", "route", "route/subroute".
        region (str):
            Required. The region the Cloud Run service is
            deployed in.
    """

    service = proto.Field(
        proto.STRING,
        number=1,
    )
    path = proto.Field(
        proto.STRING,
        number=2,
    )
    region = proto.Field(
        proto.STRING,
        number=3,
    )


class Pubsub(proto.Message):
    r"""Represents a Pub/Sub transport.

    Attributes:
        topic (str):
            Optional. The name of the Pub/Sub topic created and managed
            by Eventarc system as a transport for the event delivery.
            Format: ``projects/{PROJECT_ID}/topics/{TOPIC_NAME}``.

            You may set an existing topic for triggers of the type
            ``google.cloud.pubsub.topic.v1.messagePublished`` only. The
            topic you provide here will not be deleted by Eventarc at
            trigger deletion.
        subscription (str):
            Output only. The name of the Pub/Sub subscription created
            and managed by Eventarc system as a transport for the event
            delivery. Format:
            ``projects/{PROJECT_ID}/subscriptions/{SUBSCRIPTION_NAME}``.
    """

    topic = proto.Field(
        proto.STRING,
        number=1,
    )
    subscription = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
