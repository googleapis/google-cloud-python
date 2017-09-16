# Copyright 2017 Google Inc.
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

"""Support for bucket notification resources."""

OBJECT_FINALIZE_EVENT_TYPE = 'OBJECT_FINALIZE'
OBJECT_METADATA_UPDATE_EVENT_TYPE = 'OBJECT_METADATA_UPDATE'
OBJECT_DELETE_EVENT_TYPE = 'OBJECT_DELETE'
OBJECT_ARCHIVE_EVENT_TYPE = 'OBJECT_ARCHIVE'

JSON_API_V1_PAYLOAD_FORMAT = 'JSON_API_V1'
NONE_PAYLOAD_FORMAT = 'NONE'

_TOPIC_REF = '//pubsub.googleapis.com/projects/{}/topics/{}'


class BucketNotification(object):
    """Represent a single notification resource for a bucket.

    See: https://cloud.google.com/storage/docs/json_api/v1/notifications

    :type bucket: :class:`google.cloud.storage.bucket.Bucket`
    :param bucket: Bucket to which the notification is bound.

    :type topic_name: str
    :param topic_name: Topic name to which notifications are published.

    :type topic_project: str
    :param topic_project:
        (Optional) project ID of topic to which notifications are published.
        If not passed, uses the project ID of the bucket's client.

    :type custom_attributes: dict
    :param custom_attributes:
        (Optional) additional attributes passed with notification events.

    :type event_types: list(str)
    :param event_types:
        (Optional) event types for which notificatin events are published.

    :type blob_name_prefix: str
    :param blob_name_prefix:
        (Optional) prefix of blob names for which notification events are
        published..

    :type payload_format: str
    :param payload_format:
        (Optional) format of payload for notification events.
    """
    def __init__(self, bucket, topic_name,
                 topic_project=None, custom_attributes=None, event_types=None,
                 blob_name_prefix=None, payload_format=None):
        self._bucket = bucket
        self._topic_name = topic_name

        if topic_project is None:
            topic_project = bucket.client.project
        self._topic_project = topic_project

        self._properties = {}

        if custom_attributes is not None:
            self._properties['custom_attributes'] = custom_attributes

        if event_types is not None:
            self._properties['event_types'] = event_types

        if blob_name_prefix is not None:
            self._properties['blob_name_prefix'] = blob_name_prefix

        if payload_format is not None:
            self._properties['payload_format'] = payload_format

    @property
    def bucket(self):
        """Bucket to which the notification is bound."""
        return self._bucket

    @property
    def topic_name(self):
        """Topic name to which notifications are published."""
        return self._topic_name

    @property
    def topic_project(self):
        """Project ID of topic to which notifications are published.
        """
        return self._topic_project

    @property
    def custom_attributes(self):
        """Custom attributes passed with notification events.
        """
        return self._properties.get('custom_attributes')

    @property
    def event_types(self):
        """Event types for which notification events are published.
        """
        return self._properties.get('event_types')

    @property
    def blob_name_prefix(self):
        """Prefix of blob names for which notification events are published.
        """
        return self._properties.get('blob_name_prefix')

    @property
    def payload_format(self):
        """Format of payload of notification events."""
        return self._properties.get('payload_format')

    @property
    def notification_id(self):
        """Server-set ID of notification resource."""
        return self._properties.get('id')

    @property
    def etag(self):
        """Server-set ETag of notification resource."""
        return self._properties.get('etag')

    @property
    def self_link(self):
        """Server-set ETag of notification resource."""
        return self._properties.get('selfLink')

    @property
    def client(self):
        """The client bound to this notfication."""
        return self.bucket.client

    @property
    def path(self):
        """The URL path for this notification."""
        return '/b/{}/notificationConfigs/{}'.format(
            self.bucket.name, self.notification_id)

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: the client to use.

        :rtype: :class:`google.cloud.storage.client.Client`
        :returns: The client passed in or the bucket's client.
        """
        if client is None:
            client = self.client
        return client

    def create(self, client=None):
        """API wrapper: create the notification.

        See:
        https://cloud.google.com/storage/docs/json_api/v1/notifications/insert

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) the client to use.  If not passed, falls back
                       to the ``client`` stored on the notification's bucket.
        """
        if self.notification_id is not None:
            raise ValueError("Notification already exists w/ id: {}".format(
                self.notification_id))

        client = self._require_client(client)

        path = '/b/{}/notificationConfigs'.format(self.bucket.name)
        properties = self._properties.copy()
        properties['topic'] = _TOPIC_REF.format(
            self.topic_project, self.topic_name)
        self._properties = client._connection.api_request(
            method='POST',
            path=path,
            data=properties,
        )

    def delete(self, client=None):
        """Delete this notification.

        See:
        https://cloud.google.com/storage/docs/json_api/v1/notifications/delete

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :raises: :class:`google.api.core.exceptions.NotFound`:
            if the notification does not exist.
        """
        if self.notification_id is None:
            raise ValueError("Notification not intialized by server")

        client = self._require_client(client)
        client._connection.api_request(method='DELETE', path=self.path)
