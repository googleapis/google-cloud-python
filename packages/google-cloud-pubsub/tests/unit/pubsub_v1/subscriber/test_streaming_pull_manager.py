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

import functools
import logging
import threading
import time
import types as stdlib_types

import mock
import pytest

from google.api_core import bidi
from google.api_core import exceptions
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import client
from google.cloud.pubsub_v1.subscriber import message
from google.cloud.pubsub_v1.subscriber import scheduler
from google.cloud.pubsub_v1.subscriber._protocol import dispatcher
from google.cloud.pubsub_v1.subscriber._protocol import heartbeater
from google.cloud.pubsub_v1.subscriber._protocol import leaser
from google.cloud.pubsub_v1.subscriber._protocol import messages_on_hold
from google.cloud.pubsub_v1.subscriber._protocol import requests
from google.cloud.pubsub_v1.subscriber._protocol import streaming_pull_manager
from google.pubsub_v1 import types as gapic_types
import grpc


@pytest.mark.parametrize(
    "exception,expected_cls",
    [
        (ValueError("meep"), ValueError),
        (
            mock.create_autospec(grpc.RpcError, instance=True),
            exceptions.GoogleAPICallError,
        ),
        ({"error": "RPC terminated"}, Exception),
        ("something broke", Exception),
    ],
)
def test__wrap_as_exception(exception, expected_cls):
    assert isinstance(
        streaming_pull_manager._wrap_as_exception(exception), expected_cls
    )


def test__wrap_callback_errors_no_error():
    msg = mock.create_autospec(message.Message, instance=True)
    callback = mock.Mock()
    on_callback_error = mock.Mock()

    streaming_pull_manager._wrap_callback_errors(callback, on_callback_error, msg)

    callback.assert_called_once_with(msg)
    msg.nack.assert_not_called()
    on_callback_error.assert_not_called()


def test__wrap_callback_errors_error():
    callback_error = ValueError("meep")

    msg = mock.create_autospec(message.Message, instance=True)
    callback = mock.Mock(side_effect=callback_error)
    on_callback_error = mock.Mock()

    streaming_pull_manager._wrap_callback_errors(callback, on_callback_error, msg)

    msg.nack.assert_called_once()
    on_callback_error.assert_called_once_with(callback_error)


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
    assert manager._messages_on_hold is not None
    assert manager._client_id is not None


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


def fake_leaser_add(leaser, init_msg_count=0, assumed_msg_size=10):
    """Add a simplified fake add() method to a leaser instance.

    The fake add() method actually increases the leaser's internal message count
    by one for each message, and the total bytes by ``assumed_msg_size`` for
    each message (regardless of the actual message size).
    """

    def fake_add(self, items):
        self.message_count += len(items)
        self.bytes += len(items) * assumed_msg_size

    leaser.message_count = init_msg_count
    leaser.bytes = init_msg_count * assumed_msg_size
    leaser.add = stdlib_types.MethodType(fake_add, leaser)


def test__obtain_ack_deadline_no_custom_flow_control_setting():
    from google.cloud.pubsub_v1.subscriber._protocol import histogram

    manager = make_manager()

    # Make sure that max_duration_per_lease_extension is disabled.
    manager._flow_control = types.FlowControl(max_duration_per_lease_extension=0)

    deadline = manager._obtain_ack_deadline(maybe_update=True)
    assert deadline == histogram.MIN_ACK_DEADLINE

    # When we get some historical data, the deadline is adjusted.
    manager.ack_histogram.add(histogram.MIN_ACK_DEADLINE * 2)
    deadline = manager._obtain_ack_deadline(maybe_update=True)
    assert deadline == histogram.MIN_ACK_DEADLINE * 2

    # Adding just a single additional data point does not yet change the deadline.
    manager.ack_histogram.add(histogram.MIN_ACK_DEADLINE)
    deadline = manager._obtain_ack_deadline(maybe_update=True)
    assert deadline == histogram.MIN_ACK_DEADLINE * 2


def test__obtain_ack_deadline_with_max_duration_per_lease_extension():
    from google.cloud.pubsub_v1.subscriber._protocol import histogram

    manager = make_manager()
    manager._flow_control = types.FlowControl(
        max_duration_per_lease_extension=histogram.MIN_ACK_DEADLINE + 1
    )
    manager.ack_histogram.add(histogram.MIN_ACK_DEADLINE * 3)  # make p99 value large

    # The deadline configured in flow control should prevail.
    deadline = manager._obtain_ack_deadline(maybe_update=True)
    assert deadline == histogram.MIN_ACK_DEADLINE + 1


def test__obtain_ack_deadline_with_max_duration_per_lease_extension_too_low():
    from google.cloud.pubsub_v1.subscriber._protocol import histogram

    manager = make_manager()
    manager._flow_control = types.FlowControl(
        max_duration_per_lease_extension=histogram.MIN_ACK_DEADLINE - 1
    )
    manager.ack_histogram.add(histogram.MIN_ACK_DEADLINE * 3)  # make p99 value large

    # The deadline configured in flow control should be adjusted to the minimum allowed.
    deadline = manager._obtain_ack_deadline(maybe_update=True)
    assert deadline == histogram.MIN_ACK_DEADLINE


def test__obtain_ack_deadline_no_value_update():
    manager = make_manager()

    # Make sure that max_duration_per_lease_extension is disabled.
    manager._flow_control = types.FlowControl(max_duration_per_lease_extension=0)

    manager.ack_histogram.add(21)
    deadline = manager._obtain_ack_deadline(maybe_update=True)
    assert deadline == 21

    for _ in range(5):
        manager.ack_histogram.add(35)  # Gather some new ACK data.

    deadline = manager._obtain_ack_deadline(maybe_update=False)
    assert deadline == 21  # still the same

    # Accessing the value through the ack_deadline property has no side effects either.
    assert manager.ack_deadline == 21

    # Updating the ack deadline is reflected on ack_deadline wrapper, too.
    deadline = manager._obtain_ack_deadline(maybe_update=True)
    assert manager.ack_deadline == deadline == 35


def test_client_id():
    manager1 = make_manager()
    request1 = manager1._get_initial_request(stream_ack_deadline_seconds=10)
    client_id_1 = request1.client_id
    assert client_id_1

    manager2 = make_manager()
    request2 = manager2._get_initial_request(stream_ack_deadline_seconds=10)
    client_id_2 = request2.client_id
    assert client_id_2

    assert client_id_1 != client_id_2


def test_streaming_flow_control():
    manager = make_manager(
        flow_control=types.FlowControl(max_messages=10, max_bytes=1000)
    )
    request = manager._get_initial_request(stream_ack_deadline_seconds=10)
    assert request.max_outstanding_messages == 10
    assert request.max_outstanding_bytes == 1000


def test_streaming_flow_control_use_legacy_flow_control():
    manager = make_manager(
        flow_control=types.FlowControl(max_messages=10, max_bytes=1000),
        use_legacy_flow_control=True,
    )
    request = manager._get_initial_request(stream_ack_deadline_seconds=10)
    assert request.max_outstanding_messages == 0
    assert request.max_outstanding_bytes == 0


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
    manager.leaser.add(
        [requests.LeaseRequest(ack_id="one", byte_size=150, ordering_key="")]
    )
    assert manager.load == 0.15
    manager.maybe_pause_consumer()
    manager._consumer.pause.assert_not_called()

    # After this message is added, the messages should be higher at 20%
    # (versus 16% for bytes).
    manager.leaser.add(
        [requests.LeaseRequest(ack_id="two", byte_size=10, ordering_key="")]
    )
    assert manager.load == 0.2

    # Returning a number above 100% is fine, and it should cause this to pause.
    manager.leaser.add(
        [requests.LeaseRequest(ack_id="three", byte_size=1000, ordering_key="")]
    )
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
            requests.LeaseRequest(ack_id="one", byte_size=750, ordering_key=""),
            requests.LeaseRequest(ack_id="two", byte_size=250, ordering_key=""),
        ]
    )

    assert manager.load == 1.0

    # Trying to resume now should have no effect as we're over the threshold.
    manager.maybe_resume_consumer()
    manager._consumer.resume.assert_not_called()

    # Drop the 200 byte message, which should put us under the resume
    # threshold.
    manager.leaser.remove(
        [requests.DropRequest(ack_id="two", byte_size=250, ordering_key="")]
    )
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


def test__maybe_release_messages_on_overload():
    manager = make_manager(
        flow_control=types.FlowControl(max_messages=10, max_bytes=1000)
    )

    msg = mock.create_autospec(message.Message, instance=True, ack_id="ack", size=11)
    manager._messages_on_hold.put(msg)
    manager._on_hold_bytes = msg.size

    # Ensure load is exactly 1.0 (to verify that >= condition is used)
    _leaser = manager._leaser = mock.create_autospec(leaser.Leaser)
    _leaser.message_count = 10
    _leaser.bytes = 1000 + msg.size

    manager._maybe_release_messages()

    assert manager._messages_on_hold.size == 1
    manager._leaser.add.assert_not_called()
    manager._scheduler.schedule.assert_not_called()


def test__maybe_release_messages_below_overload():
    manager = make_manager(
        flow_control=types.FlowControl(max_messages=10, max_bytes=1000)
    )
    manager._callback = mock.sentinel.callback

    # Init leaser message count to 11, so that when subtracting the 3 messages
    # that are on hold, there is still room for another 2 messages before the
    # max load is hit.
    _leaser = manager._leaser = mock.create_autospec(leaser.Leaser)
    fake_leaser_add(_leaser, init_msg_count=11, assumed_msg_size=10)

    messages = [
        mock.create_autospec(message.Message, instance=True, ack_id="ack_foo", size=10),
        mock.create_autospec(message.Message, instance=True, ack_id="ack_bar", size=10),
        mock.create_autospec(message.Message, instance=True, ack_id="ack_baz", size=10),
    ]
    for msg in messages:
        manager._messages_on_hold.put(msg)
        manager._on_hold_bytes = 3 * 10

    # the actual call of MUT
    manager._maybe_release_messages()

    assert manager._messages_on_hold.size == 1
    msg = manager._messages_on_hold.get()
    assert msg.ack_id == "ack_baz"

    schedule_calls = manager._scheduler.schedule.mock_calls
    assert len(schedule_calls) == 2
    for _, call_args, _ in schedule_calls:
        assert call_args[0] == mock.sentinel.callback
        assert isinstance(call_args[1], message.Message)
        assert call_args[1].ack_id in ("ack_foo", "ack_bar")


def test__maybe_release_messages_negative_on_hold_bytes_warning(caplog):
    manager = make_manager(
        flow_control=types.FlowControl(max_messages=10, max_bytes=1000)
    )

    msg = mock.create_autospec(message.Message, instance=True, ack_id="ack", size=17)
    manager._messages_on_hold.put(msg)
    manager._on_hold_bytes = 5  # too low for some reason

    _leaser = manager._leaser = mock.create_autospec(leaser.Leaser)
    _leaser.message_count = 3
    _leaser.bytes = 150

    with caplog.at_level(logging.WARNING):
        manager._maybe_release_messages()

    expected_warnings = [
        record.message.lower()
        for record in caplog.records
        if "unexpectedly negative" in record.message
    ]
    assert len(expected_warnings) == 1
    assert "on hold bytes" in expected_warnings[0]
    assert "-12" in expected_warnings[0]

    assert manager._on_hold_bytes == 0  # should be auto-corrected


def test_send_unary():
    manager = make_manager()

    manager.send(
        gapic_types.StreamingPullRequest(
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

    manager.send(gapic_types.StreamingPullRequest())

    manager._client.acknowledge.assert_not_called()
    manager._client.modify_ack_deadline.assert_not_called()


def test_send_unary_api_call_error(caplog):
    caplog.set_level(logging.DEBUG)

    manager = make_manager()

    error = exceptions.GoogleAPICallError("The front fell off")
    manager._client.acknowledge.side_effect = error

    manager.send(gapic_types.StreamingPullRequest(ack_ids=["ack_id1", "ack_id2"]))

    assert "The front fell off" in caplog.text


def test_send_unary_retry_error(caplog):
    caplog.set_level(logging.DEBUG)

    manager, _, _, _, _, _ = make_running_manager()

    error = exceptions.RetryError(
        "Too long a transient error", cause=Exception("Out of time!")
    )
    manager._client.acknowledge.side_effect = error

    with pytest.raises(exceptions.RetryError):
        manager.send(gapic_types.StreamingPullRequest(ack_ids=["ack_id1", "ack_id2"]))

    assert "RetryError while sending unary RPC" in caplog.text
    assert "signaled streaming pull manager shutdown" in caplog.text


def test_heartbeat():
    manager = make_manager()
    manager._rpc = mock.create_autospec(bidi.BidiRpc, instance=True)
    manager._rpc.is_active = True

    result = manager.heartbeat()

    manager._rpc.send.assert_called_once_with(gapic_types.StreamingPullRequest())
    assert result


def test_heartbeat_inactive():
    manager = make_manager()
    manager._rpc = mock.create_autospec(bidi.BidiRpc, instance=True)
    manager._rpc.is_active = False

    manager.heartbeat()

    result = manager._rpc.send.assert_not_called()
    assert not result


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

    with mock.patch.object(
        type(manager), "ack_deadline", new=mock.PropertyMock(return_value=18)
    ):
        manager.open(mock.sentinel.callback, mock.sentinel.on_callback_error)

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
        initial_request=mock.ANY,
        should_recover=manager._should_recover,
        should_terminate=manager._should_terminate,
        throttle_reopen=True,
    )
    initial_request_arg = resumable_bidi_rpc.call_args.kwargs["initial_request"]
    assert initial_request_arg.func == manager._get_initial_request
    assert initial_request_arg.args[0] == 18
    assert not manager._client.api.get_subscription.called

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
        manager.open(mock.sentinel.callback, mock.sentinel.on_callback_error)


def test_open_has_been_closed():
    manager = make_manager()
    manager._closed = True

    with pytest.raises(ValueError, match="closed"):
        manager.open(mock.sentinel.callback, mock.sentinel.on_callback_error)


def make_running_manager(**kwargs):
    manager = make_manager(**kwargs)
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


def await_manager_shutdown(manager, timeout=None):
    # NOTE: This method should be called after manager.close(), i.e. after the shutdown
    # thread has been created and started.
    shutdown_thread = manager._regular_shutdown_thread

    if shutdown_thread is None:  # pragma: NO COVER
        raise Exception("Shutdown thread does not exist on the manager instance.")

    shutdown_thread.join(timeout=timeout)
    if shutdown_thread.is_alive():  # pragma: NO COVER
        pytest.fail("Shutdown not completed in time.")


def test_close():
    (
        manager,
        consumer,
        dispatcher,
        leaser,
        heartbeater,
        scheduler,
    ) = make_running_manager()

    manager.close()
    await_manager_shutdown(manager, timeout=3)

    consumer.stop.assert_called_once()
    leaser.stop.assert_called_once()
    dispatcher.stop.assert_called_once()
    heartbeater.stop.assert_called_once()
    scheduler.shutdown.assert_called_once()

    assert manager.is_active is False


def test_close_inactive_consumer():
    (
        manager,
        consumer,
        dispatcher,
        leaser,
        heartbeater,
        scheduler,
    ) = make_running_manager()
    consumer.is_active = False

    manager.close()
    await_manager_shutdown(manager, timeout=3)

    consumer.stop.assert_not_called()
    leaser.stop.assert_called_once()
    dispatcher.stop.assert_called_once()
    heartbeater.stop.assert_called_once()
    scheduler.shutdown.assert_called_once()


def test_close_idempotent():
    manager, _, _, _, _, scheduler = make_running_manager()

    manager.close()
    manager.close()
    await_manager_shutdown(manager, timeout=3)

    assert scheduler.shutdown.call_count == 1


class FakeDispatcher(object):
    def __init__(self, manager, error_callback):
        self._manager = manager
        self._error_callback = error_callback
        self._thread = None
        self._stop = False

    def start(self):
        self._thread = threading.Thread(target=self._do_work)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._stop = True
        self._thread.join()
        self._thread = None

    def _do_work(self):
        while not self._stop:
            try:
                self._manager.leaser.add([mock.Mock()])
            except Exception as exc:  # pragma: NO COVER
                self._error_callback(exc)
            time.sleep(0.1)

        # also try to interact with the leaser after the stop flag has been set
        try:
            self._manager.leaser.remove([mock.Mock()])
        except Exception as exc:  # pragma: NO COVER
            self._error_callback(exc)


def test_close_no_dispatcher_error():
    manager, _, _, _, _, _ = make_running_manager()
    error_callback = mock.Mock(name="error_callback")
    dispatcher = FakeDispatcher(manager=manager, error_callback=error_callback)
    manager._dispatcher = dispatcher
    dispatcher.start()

    manager.close()
    await_manager_shutdown(manager, timeout=3)

    error_callback.assert_not_called()


def test_close_callbacks():
    manager, _, _, _, _, _ = make_running_manager()

    callback = mock.Mock()

    manager.add_close_callback(callback)
    manager.close(reason="meep")
    await_manager_shutdown(manager, timeout=3)

    callback.assert_called_once_with(manager, "meep")


def test_close_blocking_scheduler_shutdown():
    manager, _, _, _, _, _ = make_running_manager(await_callbacks_on_shutdown=True)
    scheduler = manager._scheduler

    manager.close()
    await_manager_shutdown(manager, timeout=3)

    scheduler.shutdown.assert_called_once_with(await_msg_callbacks=True)


def test_close_nonblocking_scheduler_shutdown():
    manager, _, _, _, _, _ = make_running_manager(await_callbacks_on_shutdown=False)
    scheduler = manager._scheduler

    manager.close()
    await_manager_shutdown(manager, timeout=3)

    scheduler.shutdown.assert_called_once_with(await_msg_callbacks=False)


def test_close_nacks_internally_queued_messages():
    nacked_messages = []

    def fake_nack(self):
        nacked_messages.append(self.data)

    MockMsg = functools.partial(mock.create_autospec, message.Message, instance=True)
    messages = [MockMsg(data=b"msg1"), MockMsg(data=b"msg2"), MockMsg(data=b"msg3")]
    for msg in messages:
        msg.nack = stdlib_types.MethodType(fake_nack, msg)

    manager, _, _, _, _, _ = make_running_manager()
    dropped_by_scheduler = messages[:2]
    manager._scheduler.shutdown.return_value = dropped_by_scheduler
    manager._messages_on_hold._messages_on_hold.append(messages[2])

    manager.close()
    await_manager_shutdown(manager, timeout=3)

    assert sorted(nacked_messages) == [b"msg1", b"msg2", b"msg3"]


def test__get_initial_request():
    manager = make_manager()
    manager._leaser = mock.create_autospec(leaser.Leaser, instance=True)
    manager._leaser.ack_ids = ["1", "2"]

    initial_request = manager._get_initial_request(123)

    assert isinstance(initial_request, gapic_types.StreamingPullRequest)
    assert initial_request.subscription == "subscription-name"
    assert initial_request.stream_ack_deadline_seconds == 123
    assert initial_request.modify_deadline_ack_ids == ["1", "2"]
    assert initial_request.modify_deadline_seconds == [10, 10]


def test__get_initial_request_wo_leaser():
    manager = make_manager()
    manager._leaser = None

    initial_request = manager._get_initial_request(123)

    assert isinstance(initial_request, gapic_types.StreamingPullRequest)
    assert initial_request.subscription == "subscription-name"
    assert initial_request.stream_ack_deadline_seconds == 123
    assert initial_request.modify_deadline_ack_ids == []
    assert initial_request.modify_deadline_seconds == []


def test__on_response_delivery_attempt():
    manager, _, dispatcher, leaser, _, scheduler = make_running_manager()
    manager._callback = mock.sentinel.callback

    # Set up the messages.
    response = gapic_types.StreamingPullResponse(
        received_messages=[
            gapic_types.ReceivedMessage(
                ack_id="fack",
                message=gapic_types.PubsubMessage(data=b"foo", message_id="1"),
            ),
            gapic_types.ReceivedMessage(
                ack_id="back",
                message=gapic_types.PubsubMessage(data=b"bar", message_id="2"),
                delivery_attempt=6,
            ),
        ]
    )

    # adjust message bookkeeping in leaser
    fake_leaser_add(leaser, init_msg_count=0, assumed_msg_size=42)

    manager._on_response(response)

    schedule_calls = scheduler.schedule.mock_calls
    assert len(schedule_calls) == 2
    msg1 = schedule_calls[0][1][1]
    assert msg1.delivery_attempt is None
    msg2 = schedule_calls[1][1][1]
    assert msg2.delivery_attempt == 6


def test__on_response_modifies_ack_deadline():
    manager, _, dispatcher, leaser, _, scheduler = make_running_manager()
    manager._callback = mock.sentinel.callback

    # Set up the messages.
    response = gapic_types.StreamingPullResponse(
        received_messages=[
            gapic_types.ReceivedMessage(
                ack_id="ack_1",
                message=gapic_types.PubsubMessage(data=b"foo", message_id="1"),
            ),
            gapic_types.ReceivedMessage(
                ack_id="ack_2",
                message=gapic_types.PubsubMessage(data=b"bar", message_id="2"),
            ),
        ]
    )

    # adjust message bookkeeping in leaser
    fake_leaser_add(leaser, init_msg_count=0, assumed_msg_size=80)

    # Actually run the method and chack that correct MODACK value is used.
    with mock.patch.object(
        type(manager), "ack_deadline", new=mock.PropertyMock(return_value=18)
    ):
        manager._on_response(response)

    dispatcher.modify_ack_deadline.assert_called_once_with(
        [requests.ModAckRequest("ack_1", 18), requests.ModAckRequest("ack_2", 18)]
    )


def test__on_response_no_leaser_overload():
    manager, _, dispatcher, leaser, _, scheduler = make_running_manager()
    manager._callback = mock.sentinel.callback

    # Set up the messages.
    response = gapic_types.StreamingPullResponse(
        received_messages=[
            gapic_types.ReceivedMessage(
                ack_id="fack",
                message=gapic_types.PubsubMessage(data=b"foo", message_id="1"),
            ),
            gapic_types.ReceivedMessage(
                ack_id="back",
                message=gapic_types.PubsubMessage(data=b"bar", message_id="2"),
            ),
        ]
    )

    # adjust message bookkeeping in leaser
    fake_leaser_add(leaser, init_msg_count=0, assumed_msg_size=42)

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

    # the leaser load limit not hit, no messages had to be put on hold
    assert manager._messages_on_hold.size == 0


def test__on_response_with_leaser_overload():
    manager, _, dispatcher, leaser, _, scheduler = make_running_manager()
    manager._callback = mock.sentinel.callback

    # Set up the messages.
    response = gapic_types.StreamingPullResponse(
        received_messages=[
            gapic_types.ReceivedMessage(
                ack_id="fack",
                message=gapic_types.PubsubMessage(data=b"foo", message_id="1"),
            ),
            gapic_types.ReceivedMessage(
                ack_id="back",
                message=gapic_types.PubsubMessage(data=b"bar", message_id="2"),
            ),
            gapic_types.ReceivedMessage(
                ack_id="zack",
                message=gapic_types.PubsubMessage(data=b"baz", message_id="3"),
            ),
        ]
    )

    # Adjust message bookkeeping in leaser. Pick 999 messages, which is just below
    # the default FlowControl.max_messages limit.
    fake_leaser_add(leaser, init_msg_count=999, assumed_msg_size=10)

    # Actually run the method and prove that modack and schedule
    # are called in the expected way.
    manager._on_response(response)

    # all messages should be added to the lease management and have their ACK
    # deadline extended, even those not dispatched to callbacks
    dispatcher.modify_ack_deadline.assert_called_once_with(
        [
            requests.ModAckRequest("fack", 10),
            requests.ModAckRequest("back", 10),
            requests.ModAckRequest("zack", 10),
        ]
    )

    # one message should be scheduled, the flow control limits allow for it
    schedule_calls = scheduler.schedule.mock_calls
    assert len(schedule_calls) == 1
    call_args = schedule_calls[0][1]
    assert call_args[0] == mock.sentinel.callback
    assert isinstance(call_args[1], message.Message)
    assert call_args[1].message_id == "1"

    # the rest of the messages should have been put on hold
    assert manager._messages_on_hold.size == 2
    while True:
        msg = manager._messages_on_hold.get()
        if msg is None:
            break
        else:
            assert isinstance(msg, message.Message)
            assert msg.message_id in ("2", "3")


def test__on_response_none_data(caplog):
    caplog.set_level(logging.DEBUG)

    manager, _, dispatcher, leaser, _, scheduler = make_running_manager()
    manager._callback = mock.sentinel.callback

    # adjust message bookkeeping in leaser
    fake_leaser_add(leaser, init_msg_count=0, assumed_msg_size=10)

    manager._on_response(response=None)

    scheduler.schedule.assert_not_called()
    assert "callback invoked with None" in caplog.text


def test__on_response_with_ordering_keys():
    manager, _, dispatcher, leaser, _, scheduler = make_running_manager()
    manager._callback = mock.sentinel.callback

    # Set up the messages.
    response = gapic_types.StreamingPullResponse(
        received_messages=[
            gapic_types.ReceivedMessage(
                ack_id="fack",
                message=gapic_types.PubsubMessage(
                    data=b"foo", message_id="1", ordering_key=""
                ),
            ),
            gapic_types.ReceivedMessage(
                ack_id="back",
                message=gapic_types.PubsubMessage(
                    data=b"bar", message_id="2", ordering_key="key1"
                ),
            ),
            gapic_types.ReceivedMessage(
                ack_id="zack",
                message=gapic_types.PubsubMessage(
                    data=b"baz", message_id="3", ordering_key="key1"
                ),
            ),
        ]
    )

    # Make leaser with zero initial messages, so we don't test lease management
    # behavior.
    fake_leaser_add(leaser, init_msg_count=0, assumed_msg_size=10)

    # Actually run the method and prove that modack and schedule are called in
    # the expected way.
    manager._on_response(response)

    # All messages should be added to the lease management and have their ACK
    # deadline extended, even those not dispatched to callbacks.
    dispatcher.modify_ack_deadline.assert_called_once_with(
        [
            requests.ModAckRequest("fack", 10),
            requests.ModAckRequest("back", 10),
            requests.ModAckRequest("zack", 10),
        ]
    )

    # The first two messages should be scheduled, The third should be put on
    # hold because it's blocked by the completion of the second, which has the
    # same ordering key.
    schedule_calls = scheduler.schedule.mock_calls
    assert len(schedule_calls) == 2
    call_args = schedule_calls[0][1]
    assert call_args[0] == mock.sentinel.callback
    assert isinstance(call_args[1], message.Message)
    assert call_args[1].message_id == "1"

    call_args = schedule_calls[1][1]
    assert call_args[0] == mock.sentinel.callback
    assert isinstance(call_args[1], message.Message)
    assert call_args[1].message_id == "2"

    # Message 3 should have been put on hold.
    assert manager._messages_on_hold.size == 1
    # No messages available because message 2 (with "key1") has not completed yet.
    assert manager._messages_on_hold.get() is None

    # Complete message 2 (with "key1").
    manager.activate_ordering_keys(["key1"])

    # Completing message 2 should release message 3.
    schedule_calls = scheduler.schedule.mock_calls
    assert len(schedule_calls) == 3
    call_args = schedule_calls[2][1]
    assert call_args[0] == mock.sentinel.callback
    assert isinstance(call_args[1], message.Message)
    assert call_args[1].message_id == "3"

    # No messages available in the queue.
    assert manager._messages_on_hold.get() is None


def test__should_recover_true():
    manager = make_manager()

    details = "UNAVAILABLE. Service taking nap."
    exc = exceptions.ServiceUnavailable(details)

    assert manager._should_recover(exc) is True


def test__should_recover_false():
    manager = make_manager()

    exc = TypeError("wahhhhhh")

    assert manager._should_recover(exc) is False


def test__should_terminate_true():
    manager = make_manager()

    details = "Cancelled. Go away, before I taunt you a second time."
    exc = exceptions.Cancelled(details)

    assert manager._should_terminate(exc) is True


def test__should_terminate_false():
    manager = make_manager()

    exc = TypeError("wahhhhhh")

    assert manager._should_terminate(exc) is False


@mock.patch("threading.Thread", autospec=True)
def test__on_rpc_done(thread):
    manager = make_manager()

    manager._on_rpc_done(mock.sentinel.error)

    thread.assert_called_once_with(
        name=mock.ANY, target=manager._shutdown, kwargs={"reason": mock.ANY}
    )
    _, kwargs = thread.call_args
    reason = kwargs["kwargs"]["reason"]
    assert isinstance(reason, Exception)
    assert reason.args == (mock.sentinel.error,)  # Exception wraps the original error


def test_activate_ordering_keys():
    manager = make_manager()
    manager._messages_on_hold = mock.create_autospec(
        messages_on_hold.MessagesOnHold, instance=True
    )

    manager.activate_ordering_keys(["key1", "key2"])

    manager._messages_on_hold.activate_ordering_keys.assert_called_once_with(
        ["key1", "key2"], mock.ANY
    )


def test_activate_ordering_keys_stopped_scheduler():
    manager = make_manager()
    manager._messages_on_hold = mock.create_autospec(
        messages_on_hold.MessagesOnHold, instance=True
    )
    manager._scheduler = None

    manager.activate_ordering_keys(["key1", "key2"])

    manager._messages_on_hold.activate_ordering_keys.assert_not_called()
