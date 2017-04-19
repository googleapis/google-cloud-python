# Copyright 2016 Google Inc.
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

"""Testable usage examples for Google Cloud Pubsub API wrapper

Each example function takes a ``client`` argument (which must be an instance
of :class:`google.cloud.pubsub.client.Client`) and uses it to perform a task
with the API.

To facilitate running the examples as system tests, each example is also passed
a ``to_delete`` list;  the function adds to the list any objects created which
need to be deleted during teardown.
"""

import time

from google.cloud.pubsub.client import Client


def snippet(func):
    """Mark ``func`` as a snippet example function."""
    func._snippet = True
    return func


def _millis():
    return time.time() * 1000


@snippet
def client_list_topics(client, to_delete):  # pylint: disable=unused-argument
    """List topics for a project."""

    def do_something_with(sub):  # pylint: disable=unused-argument
        pass

    # [START client_list_topics]
    for topic in client.list_topics():   # API request(s)
        do_something_with(topic)
    # [END client_list_topics]


@snippet
def client_list_subscriptions(client,
                              to_delete):  # pylint: disable=unused-argument
    """List all subscriptions for a project."""

    def do_something_with(sub):  # pylint: disable=unused-argument
        pass

    # [START client_list_subscriptions]
    for subscription in client.list_subscriptions():  # API request(s)
        do_something_with(subscription)
    # [END client_list_subscriptions]


@snippet
def topic_create(client, to_delete):
    """Create a topic."""
    TOPIC_NAME = 'topic_create-%d' % (_millis(),)

    # [START topic_create]
    topic = client.topic(TOPIC_NAME)
    topic.create()              # API request
    # [END topic_create]

    to_delete.append(topic)


@snippet
def topic_exists(client, to_delete):
    """Test existence of a topic."""
    TOPIC_NAME = 'topic_exists-%d' % (_millis(),)
    topic = client.topic(TOPIC_NAME)
    to_delete.append(topic)

    # [START topic_exists]
    assert not topic.exists()   # API request
    topic.create()              # API request
    assert topic.exists()       # API request
    # [END topic_exists]


@snippet
def topic_delete(client, to_delete):  # pylint: disable=unused-argument
    """Delete a topic."""
    TOPIC_NAME = 'topic_delete-%d' % (_millis(),)
    topic = client.topic(TOPIC_NAME)
    topic.create()              # API request

    # [START topic_delete]
    assert topic.exists()       # API request
    topic.delete()
    assert not topic.exists()   # API request
    # [END topic_delete]


@snippet
def topic_iam_policy(client, to_delete):
    """Fetch / set a topic's IAM policy."""
    TOPIC_NAME = 'topic_iam_policy-%d' % (_millis(),)
    topic = client.topic(TOPIC_NAME)
    topic.create()
    to_delete.append(topic)

    # [START topic_get_iam_policy]
    policy = topic.get_iam_policy()             # API request
    # [END topic_get_iam_policy]

    assert len(policy.viewers) == 0
    assert len(policy.editors) == 0
    assert len(policy.owners) == 0

    # [START topic_set_iam_policy]
    ALL_USERS = policy.all_users()
    policy.viewers = [ALL_USERS]
    LOGS_GROUP = policy.group('cloud-logs@google.com')
    policy.editors = [LOGS_GROUP]
    new_policy = topic.set_iam_policy(policy)   # API request
    # [END topic_set_iam_policy]

    assert ALL_USERS in new_policy.viewers
    assert LOGS_GROUP in new_policy.editors


# @snippet   # Disabled due to #1687
def topic_check_iam_permissions(client, to_delete):
    """Check topic IAM permissions."""
    TOPIC_NAME = 'topic_check_iam_permissions-%d' % (_millis(),)
    topic = client.topic(TOPIC_NAME)
    topic.create()
    to_delete.append(topic)

    # [START topic_check_iam_permissions]
    from google.cloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
    TO_CHECK = [OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE]
    ALLOWED = topic.check_iam_permissions(TO_CHECK)
    assert set(ALLOWED) == set(TO_CHECK)
    # [END topic_check_iam_permissions]


@snippet
def topic_publish_messages(client, to_delete):
    """Publish messages to a topic."""
    TOPIC_NAME = 'topic_publish_messages-%d' % (_millis(),)
    topic = client.topic(TOPIC_NAME)
    topic.create()
    to_delete.append(topic)

    # [START topic_publish_simple_message]
    topic.publish(b'This is the message payload')               # API request
    # [END topic_publish_simple_message]

    # [START topic_publish_message_with_attrs]
    topic.publish(b'Another message payload', extra='EXTRA')    # API request
    # [END topic_publish_message_with_attrs]


@snippet
def topic_subscription(client, to_delete):
    """Create subscriptions to a topic."""
    TOPIC_NAME = 'topic_subscription-%d' % (_millis(),)
    SUB_DEFAULTS = 'topic_subscription-defaults-%d' % (_millis(),)
    SUB_ACK90 = 'topic_subscription-ack90-%d' % (_millis(),)
    topic = client.topic(TOPIC_NAME)
    topic.create()
    to_delete.append(topic)

    # [START topic_subscription_defaults]
    sub_defaults = topic.subscription(SUB_DEFAULTS)
    # [END topic_subscription_defaults]

    sub_defaults.create()                               # API request
    to_delete.append(sub_defaults)
    expected_names = set()
    expected_names.add(sub_defaults.full_name)

    # [START topic_subscription_ack90]
    sub_ack90 = topic.subscription(SUB_ACK90, ack_deadline=90)
    # [END topic_subscription_ack90]

    sub_ack90.create()                                  # API request
    to_delete.append(sub_ack90)
    expected_names.add(sub_ack90.full_name)

    sub_names = set()

    def do_something_with(sub):
        sub_names.add(sub.full_name)

    # [START topic_list_subscriptions]
    for subscription in topic.list_subscriptions():   # API request(s)
        do_something_with(subscription)
    # [END topic_list_subscriptions]

    assert sub_names.issuperset(expected_names)


# @snippet:  disabled, because push-mode requires a validated endpoint URL
def topic_subscription_push(client, to_delete):
    """Create subscriptions to a topic."""
    TOPIC_NAME = 'topic_subscription_push-%d' % (_millis(),)
    SUB_PUSH = 'topic_subscription_push-sub-%d' % (_millis(),)
    PUSH_URL = 'https://api.example.com/push-endpoint'
    topic = client.topic(TOPIC_NAME)
    topic.create()
    to_delete.append(topic)

    # [START topic_subscription_push]
    subscription = topic.subscription(SUB_PUSH, push_endpoint=PUSH_URL)
    subscription.create()               # API request
    # [END topic_subscription_push]

    # [START subscription_push_pull]
    subscription.modify_push_configuration(push_endpoint=None)  # API request
    # [END subscription_push_pull]

    # [START subscription_pull_push]
    subscription.modify_push_configuration(
        push_endpoint=PUSH_URL)                                 # API request
    # [END subscription_pull_push]


@snippet
def subscription_lifecycle(client, to_delete):
    """Test lifecycle of a subscription."""
    TOPIC_NAME = 'subscription_lifecycle-%d' % (_millis(),)
    SUB_NAME = 'subscription_lifecycle-defaults-%d' % (_millis(),)
    topic = client.topic(TOPIC_NAME)
    topic.create()
    to_delete.append(topic)

    # [START subscription_create]
    subscription = topic.subscription(SUB_NAME)
    subscription.create()                               # API request
    # [END subscription_create]

    # [START subscription_exists]
    assert subscription.exists()                        # API request
    # [END subscription_exists]

    # [START subscription_reload]
    subscription.reload()                               # API request
    # [END subscription_reload]

    # [START subscription_delete]
    subscription.delete()                               # API request
    # [END subscription_delete]


@snippet
def subscription_pull(client, to_delete):
    """Pull messges from a subscribed topic."""
    TOPIC_NAME = 'subscription_pull-%d' % (_millis(),)
    SUB_NAME = 'subscription_pull-defaults-%d' % (_millis(),)
    PAYLOAD1 = b'PAYLOAD1'
    PAYLOAD2 = b'PAYLOAD2'
    EXTRA = 'EXTRA'
    topic = client.topic(TOPIC_NAME)
    topic.create()
    to_delete.append(topic)

    subscription = topic.subscription(SUB_NAME)
    subscription.create()
    to_delete.append(subscription)

    # [START subscription_pull_return_immediately]
    pulled = subscription.pull(return_immediately=True)
    # [END subscription_pull_return_immediately]
    assert len(pulled) == 0, "unexpected message"

    topic.publish(PAYLOAD1)
    topic.publish(PAYLOAD2, extra=EXTRA)

    time.sleep(1)  # eventually-consistent

    # [START subscription_pull]
    pulled = subscription.pull(max_messages=2)
    # [END subscription_pull]

    assert len(pulled) == 2, "eventual consistency"

    # [START subscription_modify_ack_deadline]
    for ack_id, _ in pulled:
        subscription.modify_ack_deadline(ack_id, 90)    # API request
    # [END subscription_modify_ack_deadline]

    payloads = []
    extras = []

    def do_something_with(message):  # pylint: disable=unused-argument
        payloads.append(message.data)
        if message.attributes:
            extras.append(message.attributes)

    class ApplicationException(Exception):
        pass

    def log_exception(_):
        pass

    # [START subscription_acknowledge]
    for ack_id, message in pulled:
        try:
            do_something_with(message)
        except ApplicationException as e:
            log_exception(e)
        else:
            subscription.acknowledge([ack_id])
    # [END subscription_acknowledge]

    assert set(payloads) == set([PAYLOAD1, PAYLOAD2]), 'payloads: %s' % (
        (payloads,))
    assert extras == [{'extra': EXTRA}], 'extras: %s' % (
        (extras,))


@snippet
def subscription_pull_w_autoack(client, to_delete):
    """Pull messges from a topic, auto-acknowldging them"""
    TOPIC_NAME = 'subscription_pull_autoack-%d' % (_millis(),)
    SUB_NAME = 'subscription_pull_autoack-defaults-%d' % (_millis(),)
    PAYLOAD1 = b'PAYLOAD1'
    PAYLOAD2 = b'PAYLOAD2'
    EXTRA = 'EXTRA'
    topic = client.topic(TOPIC_NAME)
    topic.create()
    to_delete.append(topic)

    subscription = topic.subscription(SUB_NAME)
    subscription.create()
    to_delete.append(subscription)

    # [START topic_batch]
    with topic.batch() as batch:
        batch.publish(PAYLOAD1)
        batch.publish(PAYLOAD2, extra=EXTRA)
    # [END topic_batch]

    time.sleep(1)  # eventually-consistent

    payloads = []
    extras = []

    def do_something_with(message):  # pylint: disable=unused-argument
        payloads.append(message.data)
        if message.attributes:
            extras.append(message.attributes)

    # [START subscription_pull_autoack]
    from google.cloud.pubsub.subscription import AutoAck
    with AutoAck(subscription, max_messages=10) as ack:
        for ack_id, message in list(ack.items()):
            try:
                do_something_with(message)
            except Exception:  # pylint: disable=broad-except
                del ack[ack_id]
    # [END subscription_pull_autoack]

    assert set(payloads) == set(PAYLOAD1, PAYLOAD1), "eventual consistency"
    assert extras == [{'extra': EXTRA}], "eventual consistency"


@snippet
def subscription_iam_policy(client, to_delete):
    """Fetch / set a subscription's IAM policy."""
    TOPIC_NAME = 'subscription_iam_policy-%d' % (_millis(),)
    SUB_NAME = 'subscription_iam_policy-defaults-%d' % (_millis(),)
    topic = client.topic(TOPIC_NAME)
    topic.create()
    to_delete.append(topic)

    subscription = topic.subscription(SUB_NAME)
    subscription.create()
    to_delete.append(subscription)

    # [START subscription_get_iam_policy]
    policy = subscription.get_iam_policy()             # API request
    # [END subscription_get_iam_policy]

    assert len(policy.viewers) == 0
    assert len(policy.editors) == 0
    assert len(policy.owners) == 0

    # [START subscription_set_iam_policy]
    ALL_USERS = policy.all_users()
    policy.viewers = [ALL_USERS]
    LOGS_GROUP = policy.group('cloud-logs@google.com')
    policy.editors = [LOGS_GROUP]
    new_policy = subscription.set_iam_policy(policy)   # API request
    # [END subscription_set_iam_policy]

    assert ALL_USERS in new_policy.viewers
    assert LOGS_GROUP in new_policy.editors


# @snippet   # Disabled due to #1687
def subscription_check_iam_permissions(client, to_delete):
    """Check subscription IAM permissions."""
    TOPIC_NAME = 'subscription_check_iam_permissions-%d' % (_millis(),)
    SUB_NAME = 'subscription_check_iam_permissions-defaults-%d' % (_millis(),)
    topic = client.topic(TOPIC_NAME)
    topic.create()
    to_delete.append(topic)

    subscription = topic.subscription(SUB_NAME)
    subscription.create()
    to_delete.append(subscription)

    # [START subscription_check_iam_permissions]
    from google.cloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
    TO_CHECK = [OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE]
    ALLOWED = subscription.check_iam_permissions(TO_CHECK)
    assert set(ALLOWED) == set(TO_CHECK)
    # [END subscription_check_iam_permissions]


def _line_no(func):
    code = getattr(func, '__code__', None) or getattr(func, 'func_code')
    return code.co_firstlineno


def _find_examples():
    funcs = [obj for obj in globals().values()
             if getattr(obj, '_snippet', False)]
    for func in sorted(funcs, key=_line_no):
        yield func


def _name_and_doc(func):
    return func.__name__, func.__doc__


def main():
    client = Client()
    for example in _find_examples():
        to_delete = []
        print('%-25s: %s' % _name_and_doc(example))
        try:
            example(client, to_delete)
        except AssertionError as e:
            print('   FAIL: %s' % (e,))
        except Exception as e:  # pylint: disable=broad-except
            print('  ERROR: %r' % (e,))
        for item in to_delete:
            item.delete()


if __name__ == '__main__':
    main()
