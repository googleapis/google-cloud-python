# Copyright 2017, Google LLC All rights reserved.
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

import logging
import time

from google.api_core import exceptions
from google.auth import credentials
import grpc
import mock

from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.gapic import subscriber_client_config
from google.cloud.pubsub_v1.subscriber.policy import base
from google.cloud.pubsub_v1.subscriber.policy import thread


def create_policy(flow_control=types.FlowControl()):
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    return thread.Policy(client, 'sub_name_d', flow_control=flow_control)


def test_idempotent_retry_codes():
    # Make sure the config matches our hard-coded tuple of exceptions.
    interfaces = subscriber_client_config.config['interfaces']
    retry_codes = interfaces['google.pubsub.v1.Subscriber']['retry_codes']
    idempotent = retry_codes['idempotent']

    status_codes = tuple(
        getattr(grpc.StatusCode, name, None)
        for name in idempotent
    )
    expected = tuple(
        exceptions.exception_class_for_grpc_status(status_code)
        for status_code in status_codes
    )
    assert base.BasePolicy._RETRYABLE_STREAM_ERRORS == expected


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
    policy._consumer._stopped.clear()
    with mock.patch.object(policy._consumer, 'send_request') as send_request:
        policy.ack([
            base.AckRequest(
                ack_id='ack_id_string', time_to_ack=20, byte_size=0)])
        send_request.assert_called_once_with(types.StreamingPullRequest(
            ack_ids=['ack_id_string'],
        ))
    assert len(policy.histogram) == 1
    assert 20 in policy.histogram


def test_ack_no_time():
    policy = create_policy()
    policy._consumer._stopped.clear()
    with mock.patch.object(policy._consumer, 'send_request') as send_request:
        policy.ack([base.AckRequest(
            'ack_id_string', time_to_ack=None, byte_size=0)])
        send_request.assert_called_once_with(types.StreamingPullRequest(
            ack_ids=['ack_id_string'],
        ))
    assert len(policy.histogram) == 0


def test_ack_paused():
    policy = create_policy()
    consumer = policy._consumer
    consumer._stopped.set()
    assert consumer.paused is True

    policy.ack([base.AckRequest('ack_id_string', 0, 0)])

    assert consumer.paused is False
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
    policy.drop([base.DropRequest(ack_id='ack_id_string', byte_size=20)])
    assert len(policy.managed_ack_ids) == 0
    assert policy._bytes == 0

    # Do this again to establish idempotency.
    policy.drop([base.DropRequest(ack_id='ack_id_string', byte_size=20)])
    assert len(policy.managed_ack_ids) == 0
    assert policy._bytes == 0


@mock.patch.object(base, '_LOGGER', spec=logging.Logger)
def test_drop_unexpected_negative(_LOGGER):
    policy = create_policy()
    policy.managed_ack_ids.add('ack_id_string')
    policy._bytes = 0
    policy.drop([base.DropRequest(ack_id='ack_id_string', byte_size=20)])
    assert len(policy.managed_ack_ids) == 0
    assert policy._bytes == 0
    _LOGGER.debug.assert_called_once_with(
        'Bytes was unexpectedly negative: %d', -20)


def test_drop_below_threshold():
    """Establish that we resume a paused subscription.

    If the subscription is paused, and we drop sufficiently below
    the flow control thresholds, it should resume.
    """
    policy = create_policy()
    policy.managed_ack_ids.add('ack_id_string')
    num_bytes = 20
    policy._bytes = num_bytes
    consumer = policy._consumer
    assert consumer.paused is True

    policy.drop([
        base.DropRequest(ack_id='ack_id_string', byte_size=num_bytes)])

    assert consumer.paused is False


def test_on_request_below_threshold():
    """Establish that we resume a paused subscription when the pending
    requests count is below threshold."""
    flow_control = types.FlowControl(max_requests=100)
    policy = create_policy(flow_control=flow_control)
    consumer = policy._consumer

    assert consumer.paused is True

    pending_requests_patch = mock.patch.object(
        consumer.__class__, 'pending_requests', new_callable=mock.PropertyMock)
    with pending_requests_patch as pending_requests:
        # should still be paused, not under the threshold.
        pending_requests.return_value = 90
        policy.on_request(None)
        assert consumer.paused is True

        # should unpause, we're under the resume threshold
        pending_requests.return_value = 50
        policy.on_request(None)
        assert consumer.paused is False


def test_load_w_lease():
    flow_control = types.FlowControl(max_messages=10, max_bytes=1000)
    policy = create_policy(flow_control=flow_control)
    consumer = policy._consumer

    with mock.patch.object(consumer, 'pause') as pause:
        # This should mean that our messages count is at 10%, and our bytes
        # are at 15%; the ._load property should return the higher (0.15).
        policy.lease([base.LeaseRequest(ack_id='one', byte_size=150)])
        assert policy._load == 0.15
        pause.assert_not_called()
        # After this message is added, the messages should be higher at 20%
        # (versus 16% for bytes).
        policy.lease([base.LeaseRequest(ack_id='two', byte_size=10)])
        assert policy._load == 0.2
        pause.assert_not_called()
        # Returning a number above 100% is fine.
        policy.lease([base.LeaseRequest(ack_id='three', byte_size=1000)])
        assert policy._load == 1.16
        pause.assert_called_once_with()


def test_load_w_requests():
    flow_control = types.FlowControl(max_bytes=100, max_requests=100)
    policy = create_policy(flow_control=flow_control)
    consumer = policy._consumer

    pending_requests_patch = mock.patch.object(
        consumer.__class__, 'pending_requests', new_callable=mock.PropertyMock)
    with pending_requests_patch as pending_requests:
        pending_requests.return_value = 0
        assert policy._load == 0

        pending_requests.return_value = 100
        assert policy._load == 1

        # If bytes count is higher, it should return that.
        policy._bytes = 110
        assert policy._load == 1.1


def test_modify_ack_deadline():
    policy = create_policy()
    with mock.patch.object(policy._consumer, 'send_request') as send_request:
        policy.modify_ack_deadline([
            base.ModAckRequest(ack_id='ack_id_string', seconds=60)])
        send_request.assert_called_once_with(types.StreamingPullRequest(
            modify_deadline_ack_ids=['ack_id_string'],
            modify_deadline_seconds=[60],
        ))


def test_maintain_leases_inactive_consumer():
    policy = create_policy()
    policy._consumer._stopped.set()
    assert policy.maintain_leases() is None


def test_maintain_leases_ack_ids():
    policy = create_policy()
    policy._consumer._stopped.clear()
    policy.lease([base.LeaseRequest(ack_id='my ack id', byte_size=50)])

    # Mock the sleep object.
    with mock.patch.object(time, 'sleep', autospec=True) as sleep:
        def trigger_inactive(seconds):
            assert 0 < seconds < 10
            policy._consumer._stopped.set()

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
    policy._consumer._stopped.clear()
    with mock.patch.object(time, 'sleep', autospec=True) as sleep:
        def trigger_inactive(seconds):
            assert 0 < seconds < 10
            policy._consumer._stopped.set()

        sleep.side_effect = trigger_inactive
        policy.maintain_leases()
        sleep.assert_called()


def test_lease():
    policy = create_policy()
    policy.lease([base.LeaseRequest(ack_id='ack_id_string', byte_size=20)])
    assert len(policy.managed_ack_ids) == 1
    assert policy._bytes == 20

    # Do this again to prove idempotency.
    policy.lease([base.LeaseRequest(ack_id='ack_id_string', byte_size=20)])
    assert len(policy.managed_ack_ids) == 1
    assert policy._bytes == 20


def test_lease_above_threshold():
    flow_control = types.FlowControl(max_messages=2)
    policy = create_policy(flow_control=flow_control)
    consumer = policy._consumer

    with mock.patch.object(consumer, 'pause') as pause:
        policy.lease([base.LeaseRequest(ack_id='first_ack_id', byte_size=20)])
        pause.assert_not_called()
        policy.lease([base.LeaseRequest(ack_id='second_ack_id', byte_size=25)])
        pause.assert_called_once_with()


def test_nack():
    policy = create_policy()
    with mock.patch.object(policy, 'modify_ack_deadline') as mad:
        with mock.patch.object(policy, 'drop') as drop:
            items = [base.NackRequest(ack_id='ack_id_string', byte_size=10)]
            policy.nack(items)
            drop.assert_called_once_with(
                [base.DropRequest(ack_id='ack_id_string', byte_size=10)])
        mad.assert_called_once_with(
            [base.ModAckRequest(ack_id='ack_id_string', seconds=0)])
