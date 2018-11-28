# Copyright 2018, Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

import mock
import pytest

from google.api_core import bidi
from google.api_core import exceptions
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.gapic import subscriber_client_config
from google.cloud.pubsub_v1.subscriber import client
from google.cloud.pubsub_v1.subscriber import message
from google.cloud.pubsub_v1.subscriber import scheduler
from google.cloud.pubsub_v1.subscriber._protocol import dispatcher
from google.cloud.pubsub_v1.subscriber._protocol import heartbeater
from google.cloud.pubsub_v1.subscriber._protocol import leaser
from google.cloud.pubsub_v1.subscriber._protocol import requests
from google.cloud.pubsub_v1.subscriber._protocol import streaming_pull_manager
import grpc


@pytest.mark.parametrize(
    "exception,expected_cls",
    [
        (ValueError("meep"), ValueError),
        (
            mock.create_autospec(grpc.RpcError, instance=True),
            exceptions.GoogleAPICallError,
        ),
    ],
)
def test__maybe_wrap_exception(exception, expected_cls):
    assert isinstance(
        streaming_pull_manager._maybe_wrap_exception(exception), expected_cls
    )


def test__wrap_callback_errors_no_error():
    msg = mock.create_autospec(message.Message, instance=True)
    callback = mock.Mock()

    streaming_pull_manager._wrap_callback_errors(callback, msg)

    callback.assert_called_once_with(msg)
    msg.nack.assert_not_called()


def test__wrap_callback_errors_error():
    msg = mock.create_autospec(message.Message, instance=True)
    callback = mock.Mock(side_effect=ValueError("meep"))

    streaming_pull_manager._wrap_callback_errors(callback, msg)

    msg.nack.assert_called_once()


def test_constructor_and_default_state():
    manager = streaming_pull_manager.StreamingPullManager(
        mock.sentinel.client, mock.sentinel.subscription
    )

    # Public state
    assert manager.is_active is False
    assert manager.flow_control == types.FlowControl()
    assert manager.dispatcher is None
    assert manager.leaser is None
    assert manager.ack_histogram is not None
    assert manager.ack_deadline == 10
    assert manager.load == 0

    # Private state
    assert manager._client == mock.sentinel.client
    assert manager._subscription == mock.sentinel.subscription
    assert manager._scheduler is not None


def test_constructor_with_options():
    manager = streaming_pull_manager.StreamingPullManager(
        mock.sentinel.client,
        mock.sentinel.subscription,
        flow_control=mock.sentinel.flow_control,
        scheduler=mock.sentinel.scheduler,
    )

    assert manager.flow_control == mock.sentinel.flow_control
    assert manager._scheduler == mock.sentinel.scheduler


def make_manager(**kwargs):
    client_ = mock.create_autospec(client.Client, instance=True)
    scheduler_ = mock.create_autospec(scheduler.Scheduler, instance=True)
    return streaming_pull_manager.StreamingPullManager(
        client_, "subscription-name", scheduler=scheduler_, **kwargs
    )


def test_ack_deadline():
    manager = make_manager()
    assert manager.ack_deadline == 10
    manager.ack_histogram.add(20)
    assert manager.ack_deadline == 20
    manager.ack_histogram.add(10)
    assert manager.ack_deadline == 20


def test_maybe_pause_consumer_wo_consumer_set():
    manager = make_manager(
        flow_control=types.FlowControl(max_messages=10, max_bytes=1000)
    )
    manager.maybe_pause_consumer()  # no raise
    # Ensure load > 1
    _leaser = manager._leaser = mock.create_autospec(leaser.Leaser)
    _leaser.message_count = 100
    _leaser.bytes = 10000
    manager.maybe_pause_consumer()  # no raise


def test_lease_load_and_pause():
    manager = make_manager(
        flow_control=types.FlowControl(max_messages=10, max_bytes=1000)
    )
    manager._leaser = leaser.Leaser(manager)
    manager._consumer = mock.create_autospec(bidi.BackgroundConsumer, instance=True)
    manager._consumer.is_paused = False

    # This should mean that our messages count is at 10%, and our bytes
    # are at 15%; load should return the higher (0.15), and shouldn't cause
    # the consumer to pause.
    manager.leaser.add([requests.LeaseRequest(ack_id="one", byte_size=150)])
    assert manager.load == 0.15
    manager.maybe_pause_consumer()
    manager._consumer.pause.assert_not_called()

    # After this message is added, the messages should be higher at 20%
    # (versus 16% for bytes).
    manager.leaser.add([requests.LeaseRequest(ack_id="two", byte_size=10)])
    assert manager.load == 0.2

    # Returning a number above 100% is fine, and it should cause this to pause.
    manager.leaser.add([requests.LeaseRequest(ack_id="three", byte_size=1000)])
    assert manager.load == 1.16
    manager.maybe_pause_consumer()
    manager._consumer.pause.assert_called_once()


def test_drop_and_resume():
    manager = make_manager(
        flow_control=types.FlowControl(max_messages=10, max_bytes=1000)
    )
    manager._leaser = leaser.Leaser(manager)
    manager._consumer = mock.create_autospec(bidi.BackgroundConsumer, instance=True)
    manager._consumer.is_paused = True

    # Add several messages until we're over the load threshold.
    manager.leaser.add(
        [
            requests.LeaseRequest(ack_id="one", byte_size=750),
            requests.LeaseRequest(ack_id="two", byte_size=250),
        ]
    )

    assert manager.load == 1.0

    # Trying to resume now should have no effect as we're over the threshold.
    manager.maybe_resume_consumer()
    manager._consumer.resume.assert_not_called()

    # Drop the 200 byte message, which should put us under the resume
    # threshold.
    manager.leaser.remove([requests.DropRequest(ack_id="two", byte_size=250)])
    manager.maybe_resume_consumer()
    manager._consumer.resume.assert_called_once()


def test_resume_not_paused():
    manager = make_manager()
    manager._consumer = mock.create_autospec(bidi.BackgroundConsumer, instance=True)
    manager._consumer.is_paused = False

    # Resuming should have no effect is the consumer is not actually paused.
    manager.maybe_resume_consumer()
    manager._consumer.resume.assert_not_called()


def test_maybe_resume_consumer_wo_consumer_set():
    manager = make_manager(
        flow_control=types.FlowControl(max_messages=10, max_bytes=1000)
    )
    manager.maybe_resume_consumer()  # no raise


def test_send_unary():
    manager = make_manager()
    manager._UNARY_REQUESTS = True

    manager.send(
        types.StreamingPullRequest(
            ack_ids=["ack_id1", "ack_id2"],
            modify_deadline_ack_ids=["ack_id3", "ack_id4", "ack_id5"],
            modify_deadline_seconds=[10, 20, 20],
        )
    )

    manager._client.acknowledge.assert_called_once_with(
        subscription=manager._subscription, ack_ids=["ack_id1", "ack_id2"]
    )

    manager._client.modify_ack_deadline.assert_has_calls(
        [
            mock.call(
                subscription=manager._subscription,
                ack_ids=["ack_id3"],
                ack_deadline_seconds=10,
            ),
            mock.call(
                subscription=manager._subscription,
                ack_ids=["ack_id4", "ack_id5"],
                ack_deadline_seconds=20,
            ),
        ],
        any_order=True,
    )


def test_send_unary_empty():
    manager = make_manager()
    manager._UNARY_REQUESTS = True

    manager.send(types.StreamingPullRequest())

    manager._client.acknowledge.assert_not_called()
    manager._client.modify_ack_deadline.assert_not_called()


def test_send_unary_error(caplog):
    caplog.set_level(logging.DEBUG)

    manager = make_manager()
    manager._UNARY_REQUESTS = True

    error = exceptions.GoogleAPICallError("The front fell off")
    manager._client.acknowledge.side_effect = error

    manager.send(types.StreamingPullRequest(ack_ids=["ack_id1", "ack_id2"]))

    assert "The front fell off" in caplog.text


def test_send_streaming():
    manager = make_manager()
    manager._UNARY_REQUESTS = False
    manager._rpc = mock.create_autospec(bidi.BidiRpc, instance=True)

    manager.send(mock.sentinel.request)

    manager._rpc.send.assert_called_once_with(mock.sentinel.request)


def test_heartbeat():
    manager = make_manager()
    manager._rpc = mock.create_autospec(bidi.BidiRpc, instance=True)
    manager._rpc.is_active = True

    manager.heartbeat()

    manager._rpc.send.assert_called_once_with(types.StreamingPullRequest())


def test_heartbeat_inactive():
    manager = make_manager()
    manager._rpc = mock.create_autospec(bidi.BidiRpc, instance=True)
    manager._rpc.is_active = False

    manager.heartbeat()

    manager._rpc.send.assert_not_called()


@mock.patch("google.api_core.bidi.ResumableBidiRpc", autospec=True)
@mock.patch("google.api_core.bidi.BackgroundConsumer", autospec=True)
@mock.patch("google.cloud.pubsub_v1.subscriber._protocol.leaser.Leaser", autospec=True)
@mock.patch(
    "google.cloud.pubsub_v1.subscriber._protocol.dispatcher.Dispatcher", autospec=True
)
@mock.patch(
    "google.cloud.pubsub_v1.subscriber._protocol.heartbeater.Heartbeater", autospec=True
)
def test_open(heartbeater, dispatcher, leaser, background_consumer, resumable_bidi_rpc):
    manager = make_manager()

    manager.open(mock.sentinel.callback)

    heartbeater.assert_called_once_with(manager)
    heartbeater.return_value.start.assert_called_once()
    assert manager._heartbeater == heartbeater.return_value

    dispatcher.assert_called_once_with(manager, manager._scheduler.queue)
    dispatcher.return_value.start.assert_called_once()
    assert manager._dispatcher == dispatcher.return_value

    leaser.assert_called_once_with(manager)
    leaser.return_value.start.assert_called_once()
    assert manager.leaser == leaser.return_value

    background_consumer.assert_called_once_with(manager._rpc, manager._on_response)
    background_consumer.return_value.start.assert_called_once()
    assert manager._consumer == background_consumer.return_value

    resumable_bidi_rpc.assert_called_once_with(
        start_rpc=manager._client.api.streaming_pull,
        initial_request=manager._get_initial_request,
        should_recover=manager._should_recover,
    )
    resumable_bidi_rpc.return_value.add_done_callback.assert_called_once_with(
        manager._on_rpc_done
    )
    assert manager._rpc == resumable_bidi_rpc.return_value

    manager._consumer.is_active = True
    assert manager.is_active is True


def test_open_already_active():
    manager = make_manager()
    manager._consumer = mock.create_autospec(bidi.BackgroundConsumer, instance=True)
    manager._consumer.is_active = True

    with pytest.raises(ValueError, match="already open"):
        manager.open(mock.sentinel.callback)


def test_open_has_been_closed():
    manager = make_manager()
    manager._closed = True

    with pytest.raises(ValueError, match="closed"):
        manager.open(mock.sentinel.callback)


def make_running_manager():
    manager = make_manager()
    manager._consumer = mock.create_autospec(bidi.BackgroundConsumer, instance=True)
    manager._consumer.is_active = True
    manager._dispatcher = mock.create_autospec(dispatcher.Dispatcher, instance=True)
    manager._leaser = mock.create_autospec(leaser.Leaser, instance=True)
    manager._heartbeater = mock.create_autospec(heartbeater.Heartbeater, instance=True)

    return (
        manager,
        manager._consumer,
        manager._dispatcher,
        manager._leaser,
        manager._heartbeater,
        manager._scheduler,
    )


def test_close():
    manager, consumer, dispatcher, leaser, heartbeater, scheduler = (
        make_running_manager()
    )

    manager.close()

    consumer.stop.assert_called_once()
    leaser.stop.assert_called_once()
    dispatcher.stop.assert_called_once()
    heartbeater.stop.assert_called_once()
    scheduler.shutdown.assert_called_once()

    assert manager.is_active is False


def test_close_inactive_consumer():
    manager, consumer, dispatcher, leaser, heartbeater, scheduler = (
        make_running_manager()
    )
    consumer.is_active = False

    manager.close()

    consumer.stop.assert_not_called()
    leaser.stop.assert_called_once()
    dispatcher.stop.assert_called_once()
    heartbeater.stop.assert_called_once()
    scheduler.shutdown.assert_called_once()


def test_close_idempotent():
    manager, _, _, _, _, scheduler = make_running_manager()

    manager.close()
    manager.close()

    assert scheduler.shutdown.call_count == 1


def test_close_callbacks():
    manager, _, _, _, _, _ = make_running_manager()

    callback = mock.Mock()

    manager.add_close_callback(callback)
    manager.close(reason="meep")

    callback.assert_called_once_with(manager, "meep")


def test__get_initial_request():
    manager = make_manager()
    manager._leaser = mock.create_autospec(leaser.Leaser, instance=True)
    manager._leaser.ack_ids = ["1", "2"]

    initial_request = manager._get_initial_request()

    assert isinstance(initial_request, types.StreamingPullRequest)
    assert initial_request.subscription == "subscription-name"
    assert initial_request.stream_ack_deadline_seconds == 10
    assert initial_request.modify_deadline_ack_ids == ["1", "2"]
    assert initial_request.modify_deadline_seconds == [10, 10]


def test__get_initial_request_wo_leaser():
    manager = make_manager()
    manager._leaser = None

    initial_request = manager._get_initial_request()

    assert isinstance(initial_request, types.StreamingPullRequest)
    assert initial_request.subscription == "subscription-name"
    assert initial_request.stream_ack_deadline_seconds == 10
    assert initial_request.modify_deadline_ack_ids == []
    assert initial_request.modify_deadline_seconds == []


def test_on_response():
    manager, _, dispatcher, _, _, scheduler = make_running_manager()
    manager._callback = mock.sentinel.callback

    # Set up the messages.
    response = types.StreamingPullResponse(
        received_messages=[
            types.ReceivedMessage(
                ack_id="fack", message=types.PubsubMessage(data=b"foo", message_id="1")
            ),
            types.ReceivedMessage(
                ack_id="back", message=types.PubsubMessage(data=b"bar", message_id="2")
            ),
        ]
    )

    # Actually run the method and prove that modack and schedule
    # are called in the expected way.
    manager._on_response(response)

    dispatcher.modify_ack_deadline.assert_called_once_with(
        [requests.ModAckRequest("fack", 10), requests.ModAckRequest("back", 10)]
    )

    schedule_calls = scheduler.schedule.mock_calls
    assert len(schedule_calls) == 2
    for call in schedule_calls:
        assert call[1][0] == mock.sentinel.callback
        assert isinstance(call[1][1], message.Message)


def test_retryable_stream_errors():
    # Make sure the config matches our hard-coded tuple of exceptions.
    interfaces = subscriber_client_config.config["interfaces"]
    retry_codes = interfaces["google.pubsub.v1.Subscriber"]["retry_codes"]
    idempotent = retry_codes["idempotent"]

    status_codes = tuple(getattr(grpc.StatusCode, name, None) for name in idempotent)
    expected = tuple(
        exceptions.exception_class_for_grpc_status(status_code)
        for status_code in status_codes
    )
    assert set(expected).issubset(set(streaming_pull_manager._RETRYABLE_STREAM_ERRORS))


def test__should_recover_true():
    manager = make_manager()

    details = "UNAVAILABLE. Service taking nap."
    exc = exceptions.ServiceUnavailable(details)

    assert manager._should_recover(exc) is True


def test__should_recover_false():
    manager = make_manager()

    exc = TypeError("wahhhhhh")

    assert manager._should_recover(exc) is False


@mock.patch("threading.Thread", autospec=True)
def test__on_rpc_done(thread):
    manager = make_manager()

    manager._on_rpc_done(mock.sentinel.error)

    thread.assert_called_once_with(
        name=mock.ANY, target=manager.close, kwargs={"reason": mock.sentinel.error}
    )
