# Copyright 2016 Google Inc. All rights reserved.
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

"""GAX wrapper for Pubsub API requests."""

try:
    # pylint: disable=no-name-in-module
    from google.gax import CallOptions
    from google.gax.errors import GaxError
    from google.pubsub.v1.pubsub_pb2 import PubsubMessage
    # pylint: enable=no-name-in-module
except ImportError:  # pragma: NO COVER
    _HAVE_GAX = False
else:
    _HAVE_GAX = True

    from gcloud.exceptions import Conflict
    from gcloud.exceptions import NotFound
    from gcloud._helpers import _to_bytes

    class _PublisherAPI(object):
        """Helper mapping publisher-related APIs.

        :type gax_api: :class:`google.pubsub.v1.publisher_api.PublisherApi`
        :param gax_api: API object used to make GAX requests.
        """
        def __init__(self, gax_api):
            self._gax_api = gax_api

        def list_topics(self, project):
            """List topics for the project associated with this API.

            See:
            https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/list

            :type project: string
            :param project: project ID

            :rtype: tuple, (list, str)
            :returns: list of ``Topic`` resource dicts, plus a
                    "next page token" string:  if not None, indicates that
                    more topics can be retrieved with another call (pass that
                    value as ``page_token``).
            """
            options = CallOptions(is_page_streaming=False)
            path = 'projects/%s' % (project,)
            response = self._gax_api.list_topics(path, options)
            topics = [{'name': topic_pb.name} for topic_pb in response.topics]
            return topics, response.next_page_token

        def topic_create(self, topic_path):
            """API call:  create a topic

            See:
            https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/create

            :type topic_path: string
            :param topic_path: fully-qualified path of the new topic, in format
                               ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

            :rtype: dict
            :returns: ``Topic`` resource returned from the API.
            :raises: :exc:`gcloud.exceptions.Conflict` if the topic already
                     exists
            """
            try:
                topic_pb = self._gax_api.create_topic(topic_path)
            except GaxError:
                raise Conflict(topic_path)
            return {'name': topic_pb.name}

        def topic_get(self, topic_path):
            """API call:  retrieve a topic

            See:
            https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/get

            :type topic_path: string
            :param topic_path: fully-qualified path of the topic, in format
                            ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

            :rtype: dict
            :returns: ``Topic`` resource returned from the API.
            :raises: :exc:`gcloud.exceptions.NotFound` if the topic does not
                     exist
            """
            try:
                topic_pb = self._gax_api.get_topic(topic_path)
            except GaxError:
                raise NotFound(topic_path)
            return {'name': topic_pb.name}

        def topic_delete(self, topic_path):
            """API call:  delete a topic

            See:
            https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/create

            :type topic_path: string
            :param topic_path: fully-qualified path of the new topic, in format
                               ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

            :rtype: dict
            :returns: ``Topic`` resource returned from the API.
            """
            try:
                self._gax_api.delete_topic(topic_path)
            except GaxError:
                raise NotFound(topic_path)

        def topic_publish(self, topic_path, messages):
            """API call:  publish one or more messages to a topic

            See:
            https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/publish

            :type topic_path: string
            :param topic_path: fully-qualified path of the topic, in format
                               ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

            :type messages: list of dict
            :param messages: messages to be published.

            :rtype: list of string
            :returns: list of opaque IDs for published messages.
            :raises: :exc:`gcloud.exceptions.NotFound` if the topic does not
                     exist
            """
            message_pbs = [_message_pb_from_dict(message)
                           for message in messages]
            try:
                response = self._gax_api.publish(topic_path, message_pbs)
            except GaxError:
                raise NotFound(topic_path)
            return response.message_ids

        def topic_list_subscriptions(self, topic_path):
            """API call:  list subscriptions bound to a topic

            See:
            https://cloud.google.com/pubsub/reference/rest/v1/projects.topics.subscriptions/list

            :type topic_path: string
            :param topic_path: fully-qualified path of the topic, in format
                               ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

            :rtype: list of strings
            :returns: fully-qualified names of subscriptions for the supplied
                    topic.
            :raises: :exc:`gcloud.exceptions.NotFound` if the topic does not
                     exist
            """
            options = CallOptions(is_page_streaming=False)
            try:
                response = self._gax_api.list_topic_subscriptions(
                    topic_path, options)
            except GaxError:
                raise NotFound(topic_path)
            subs = [{'topic': topic_path, 'name': subscription}
                    for subscription in response.subscriptions]
            return subs, response.next_page_token


def _message_pb_from_dict(message):
    """Helper for :meth:`_PublisherAPI.topic_publish`."""
    return PubsubMessage(data=_to_bytes(message['data']),
                         attributes=message['attributes'])
