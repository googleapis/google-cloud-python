# Copyright 2017, Google Inc. All rights reserved.
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

import time

import mock

from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber.policy import thread


def create_policy():
    client = subscriber.Client()
    return thread.Policy(client, 'sub_name')


def test_ack_deadline():
    policy = create_policy()
    assert policy.ack_deadline == 10
    policy.histogram.add(20)
    assert policy.ack_deadline == 20
    policy.histogram.add(10)
    assert policy.ack_deadline == 20


def test_initial_request():
    policy = create_policy()
    initial_request = policy.initial_request
    assert isinstance(initial_request, types.StreamingPullRequest)
    assert initial_request.subscription == 'sub_name'
    assert initial_request.stream_ack_deadline_seconds == 10


def test_managed_ack_ids():
    policy = create_policy()

    # Ensure we always get a set back, even if the property is not yet set.
    managed_ack_ids = policy.managed_ack_ids
    assert isinstance(managed_ack_ids, set)

    # Ensure that multiple calls give the same actual object back.
    assert managed_ack_ids is policy.managed_ack_ids


def test_subscription():
    policy = create_policy()
    assert policy.subscription == 'sub_name'


def test_ack():
    policy = create_policy()
    with mock.patch.object(policy._consumer, 'send_request') as send_request:
        policy.ack('ack_id_string', 20)
        send_request.assert_called_once_with(types.StreamingPullRequest(
            ack_ids=['ack_id_string'],
        ))
    assert len(policy.histogram) == 1
    assert 20 in policy.histogram


def test_ack_no_time():
    policy = create_policy()
    with mock.patch.object(policy._consumer, 'send_request') as send_request:
        policy.ack('ack_id_string')
        send_request.assert_called_once_with(types.StreamingPullRequest(
            ack_ids=['ack_id_string'],
        ))
    assert len(policy.histogram) == 0


def test_call_rpc():
    policy = create_policy()
    with mock.patch.object(policy._client.api, 'streaming_pull') as pull:
        policy.call_rpc(mock.sentinel.GENERATOR)
        pull.assert_called_once_with(mock.sentinel.GENERATOR)


def test_drop():
    policy = create_policy()
    policy.managed_ack_ids.add('ack_id_string')
    policy.drop('ack_id_string')
    assert len(policy.managed_ack_ids) == 0


def test_modify_ack_deadline():
    policy = create_policy()
    with mock.patch.object(policy._consumer, 'send_request') as send_request:
        policy.modify_ack_deadline('ack_id_string', 60)
        send_request.assert_called_once_with(types.StreamingPullRequest(
            modify_deadline_ack_ids=['ack_id_string'],
            modify_deadline_seconds=[60],
        ))


def test_maintain_leases_inactive_consumer():
    policy = create_policy()
    policy._consumer.active = False
    assert policy.maintain_leases() is None


def test_maintain_leases_ack_ids():
    policy = create_policy()
    policy._consumer.active = True
    policy.lease('my ack id')

    # Mock the sleep object.
    with mock.patch.object(time, 'sleep', autospec=True) as sleep:
        def trigger_inactive(seconds):
            assert 0 < seconds < 10
            policy._consumer.active = False
        sleep.side_effect = trigger_inactive

        # Also mock the consumer, which sends the request.
        with mock.patch.object(policy._consumer, 'send_request') as send:
            policy.maintain_leases()
            send.assert_called_once_with(types.StreamingPullRequest(
                modify_deadline_ack_ids=['my ack id'],
                modify_deadline_seconds=[10],
            ))
        sleep.assert_called()


def test_maintain_leases_no_ack_ids():
    policy = create_policy()
    policy._consumer.active = True
    with mock.patch.object(time, 'sleep', autospec=True) as sleep:
        def trigger_inactive(seconds):
            assert 0 < seconds < 10
            policy._consumer.active = False
        sleep.side_effect = trigger_inactive
        policy.maintain_leases()
        sleep.assert_called()


def test_nack():
    policy = create_policy()
    with mock.patch.object(policy, 'modify_ack_deadline') as mad:
        policy.nack('ack_id_string')
        mad.assert_called_once_with(ack_id='ack_id_string', seconds=0)
