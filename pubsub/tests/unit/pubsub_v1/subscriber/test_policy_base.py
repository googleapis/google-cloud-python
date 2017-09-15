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

from google.auth import credentials
from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber.policy import thread


def create_policy(flow_control=types.FlowControl()):
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    return thread.Policy(client, 'sub_name_d', flow_control=flow_control)


def test_ack_deadline():
    policy = create_policy()
    assert policy.ack_deadline == 10
    policy.histogram.add(20)
    assert policy.ack_deadline == 20
    policy.histogram.add(10)
    assert policy.ack_deadline == 20


def test_get_initial_request():
    policy = create_policy()
    initial_request = policy.get_initial_request()
    assert isinstance(initial_request, types.StreamingPullRequest)
    assert initial_request.subscription == 'sub_name_d'
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
    assert policy.subscription == 'sub_name_d'


def test_ack():
    policy = create_policy()
    policy._consumer.active = True
    with mock.patch.object(policy._consumer, 'send_request') as send_request:
        policy.ack('ack_id_string', 20)
        send_request.assert_called_once_with(types.StreamingPullRequest(
            ack_ids=['ack_id_string'],
        ))
    assert len(policy.histogram) == 1
    assert 20 in policy.histogram


def test_ack_no_time():
    policy = create_policy()
    policy._consumer.active = True
    with mock.patch.object(policy._consumer, 'send_request') as send_request:
        policy.ack('ack_id_string')
        send_request.assert_called_once_with(types.StreamingPullRequest(
            ack_ids=['ack_id_string'],
        ))
    assert len(policy.histogram) == 0


def test_ack_paused():
    policy = create_policy()
    policy._paused = True
    policy._consumer.active = False
    with mock.patch.object(policy, 'open') as open_:
        policy.ack('ack_id_string')
        open_.assert_called()
    assert 'ack_id_string' in policy._ack_on_resume


def test_call_rpc():
    policy = create_policy()
    with mock.patch.object(policy._client.api, 'streaming_pull') as pull:
        policy.call_rpc(mock.sentinel.GENERATOR)
        pull.assert_called_once_with(mock.sentinel.GENERATOR)


def test_drop():
    policy = create_policy()
    policy.managed_ack_ids.add('ack_id_string')
    policy._bytes = 20
    policy.drop('ack_id_string', 20)
    assert len(policy.managed_ack_ids) == 0
    assert policy._bytes == 0

    # Do this again to establish idempotency.
    policy.drop('ack_id_string', 20)
    assert len(policy.managed_ack_ids) == 0
    assert policy._bytes == 0


def test_drop_below_threshold():
    """Establish that we resume a paused subscription.

    If the subscription is paused, and we drop sufficiently below
    the flow control thresholds, it should resume.
    """
    policy = create_policy()
    policy.managed_ack_ids.add('ack_id_string')
    policy._bytes = 20
    policy._paused = True
    with mock.patch.object(policy, 'open') as open_:
        policy.drop(ack_id='ack_id_string', byte_size=20)
        open_.assert_called_once_with(policy._callback)
    assert policy._paused is False


def test_load():
    flow_control = types.FlowControl(max_messages=10, max_bytes=1000)
    policy = create_policy(flow_control=flow_control)

    # This should mean that our messages count is at 10%, and our bytes
    # are at 15%; the ._load property should return the higher (0.15).
    policy.lease(ack_id='one', byte_size=150)
    assert policy._load == 0.15

    # After this message is added, the messages should be higher at 20%
    # (versus 16% for bytes).
    policy.lease(ack_id='two', byte_size=10)
    assert policy._load == 0.2

    # Returning a number above 100% is fine.
    policy.lease(ack_id='three', byte_size=1000)
    assert policy._load == 1.16


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
    policy.lease('my ack id', 50)

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


def test_lease():
    policy = create_policy()
    policy.lease(ack_id='ack_id_string', byte_size=20)
    assert len(policy.managed_ack_ids) == 1
    assert policy._bytes == 20

    # Do this again to prove idempotency.
    policy.lease(ack_id='ack_id_string', byte_size=20)
    assert len(policy.managed_ack_ids) == 1
    assert policy._bytes == 20


def test_lease_above_threshold():
    flow_control = types.FlowControl(max_messages=2)
    policy = create_policy(flow_control=flow_control)
    with mock.patch.object(policy, 'close') as close:
        policy.lease(ack_id='first_ack_id', byte_size=20)
        assert close.call_count == 0
        policy.lease(ack_id='second_ack_id', byte_size=25)
        close.assert_called_once_with()


def test_nack():
    policy = create_policy()
    with mock.patch.object(policy, 'modify_ack_deadline') as mad:
        with mock.patch.object(policy, 'drop') as drop:
            policy.nack(ack_id='ack_id_string', byte_size=10)
            drop.assert_called_once_with(ack_id='ack_id_string', byte_size=10)
        mad.assert_called_once_with(ack_id='ack_id_string', seconds=0)
