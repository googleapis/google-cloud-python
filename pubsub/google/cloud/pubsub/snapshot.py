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

"""Define API Snapshots."""

from google.cloud.pubsub._helpers import topic_name_from_path


class Snapshot(object):

    _DELETED_TOPIC_PATH = '_deleted-topic_'
    """Value of ``projects.snapshots.topic`` when topic has been deleted."""

    def __init__(self, name, subscription=None, topic=None, client=None):

        num_kwargs = len(
            [param for param in (subscription, topic, client) if param])
        if num_kwargs != 1:
            raise TypeError(
                "Pass only one of 'subscription', 'topic', 'client'.")

        self.name = name
        self.topic = topic or getattr(subscription, 'topic', None)
        self._subscription = subscription
        self._client = client or getattr(
            subscription, '_client', None) or topic._client

    @classmethod
    def from_api_repr(cls, resource, client, topics=None):
        """Factory:  construct a subscription given its API representation

        :type resource: dict
        :param resource: snapshot resource representation returned from the
            API.

        :type client: :class:`google.cloud.pubsub.client.Client`
        :param client: Client which holds credentials and project
                       configuration.

        :type subscriptions: dict
        :param subscriptions:
            (Optional) A Subscription to which this snapshot belongs. If not
            passed, the subscription will have a newly-created subscription.
            Must have the same topic as the snapshot.

        :rtype: :class:`google.cloud.pubsub.subscription.Subscription`
        :returns: Subscription parsed from ``resource``.
        """
        if topics is None:
            topics = {}
        topic_path = resource['topic']
        if topic_path == cls._DELETED_TOPIC_PATH:
            topic = None
        else:
            topic = topics.get(topic_path)
            if topic is None:
                # NOTE: This duplicates behavior from Topic.from_api_repr to
                #       avoid an import cycle.
                topic_name = topic_name_from_path(topic_path, client.project)
                topic = topics[topic_path] = client.topic(topic_name)
        _, _, _, name = resource['name'].split('/')
        if topic is None:
            return cls(name, client=client)
        return cls(name, topic=topic)

    @property
    def project(self):
        """Project bound to the subscription."""
        return self._client.project

    @property
    def full_name(self):
        """Fully-qualified name used in subscription APIs"""
        return 'projects/%s/snapshots/%s' % (self.project, self.name)

    @property
    def path(self):
        """URL path for the subscription's APIs"""
        return '/%s' % (self.full_name,)

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the topic of the
                       current subscription.

        :rtype: :class:`google.cloud.pubsub.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    def create(self, client=None):
        """API call:  create the snapshot

        See
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.snapshots/create

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        if not self._subscription:
            raise RuntimeError(
                'Cannot create a snapshot not bound to a subscription')

        client = self._require_client(client)
        api = client.subscriber_api
        api.snapshot_create(self.full_name, self._subscription.full_name)

    def delete(self, client=None):
        """API call:  delete the snapshot

        See
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.snapshots/delete

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        api = client.subscriber_api
        api.snapshot_delete(self.full_name)
