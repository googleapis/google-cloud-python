# Copyright 2018, Google LLC All rights reserved.
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
import threading

import grpc
import mock
import pytest
from six.moves import queue

from google.api_core import bidi
from google.api_core import exceptions


class Test_RequestQueueGenerator(object):

    def test_bounded_consume(self):
        call = mock.create_autospec(grpc.Call, instance=True)
        call.is_active.return_value = True

        def queue_generator(rpc):
            yield mock.sentinel.A
            yield queue.Empty()
            yield mock.sentinel.B
            rpc.is_active.return_value = False
            yield mock.sentinel.C

        q = mock.create_autospec(queue.Queue, instance=True)
        q.get.side_effect = queue_generator(call)

        generator = bidi._RequestQueueGenerator(q)
        generator.call = call

        items = list(generator)

        assert items == [mock.sentinel.A, mock.sentinel.B]

    def test_yield_initial_and_exit(self):
        q = mock.create_autospec(queue.Queue, instance=True)
        q.get.side_effect = queue.Empty()
        call = mock.create_autospec(grpc.Call, instance=True)
        call.is_active.return_value = False

        generator = bidi._RequestQueueGenerator(
            q, initial_request=mock.sentinel.A)
        generator.call = call

        items = list(generator)

        assert items == [mock.sentinel.A]

    def test_yield_initial_callable_and_exit(self):
        q = mock.create_autospec(queue.Queue, instance=True)
        q.get.side_effect = queue.Empty()
        call = mock.create_autospec(grpc.Call, instance=True)
        call.is_active.return_value = False

        generator = bidi._RequestQueueGenerator(
            q, initial_request=lambda: mock.sentinel.A)
        generator.call = call

        items = list(generator)

        assert items == [mock.sentinel.A]

    def test_exit_when_inactive_with_item(self):
        q = mock.create_autospec(queue.Queue, instance=True)
        q.get.side_effect = [mock.sentinel.A, queue.Empty()]
        call = mock.create_autospec(grpc.Call, instance=True)
        call.is_active.return_value = False

        generator = bidi._RequestQueueGenerator(q)
        generator.call = call

        items = list(generator)

        assert items == []
        # Make sure it put the item back.
        q.put.assert_called_once_with(mock.sentinel.A)

    def test_exit_when_inactive_empty(self):
        q = mock.create_autospec(queue.Queue, instance=True)
        q.get.side_effect = queue.Empty()
        call = mock.create_autospec(grpc.Call, instance=True)
        call.is_active.return_value = False

        generator = bidi._RequestQueueGenerator(q)
        generator.call = call

        items = list(generator)

        assert items == []

    def test_exit_with_stop(self):
        q = mock.create_autospec(queue.Queue, instance=True)
        q.get.side_effect = [None, queue.Empty()]
        call = mock.create_autospec(grpc.Call, instance=True)
        call.is_active.return_value = True

        generator = bidi._RequestQueueGenerator(q)
        generator.call = call

        items = list(generator)

        assert items == []


class _CallAndFuture(grpc.Call, grpc.Future):
    pass


def make_rpc():
    """Makes a mock RPC used to test Bidi classes."""
    call = mock.create_autospec(_CallAndFuture, instance=True)
    rpc = mock.create_autospec(grpc.StreamStreamMultiCallable, instance=True)

    def rpc_side_effect(request):
        call.is_active.return_value = True
        call.request = request
        return call

    rpc.side_effect = rpc_side_effect

    def cancel_side_effect():
        call.is_active.return_value = False

    call.cancel.side_effect = cancel_side_effect

    return rpc, call


class ClosedCall(object):
    # NOTE: This is needed because defining `.next` on an **instance**
    #       rather than the **class** will not be iterable in Python 2.
    #       This is problematic since a `Mock` just sets members.

    def __init__(self, exception):
        self.exception = exception

    def __next__(self):
        raise self.exception

    next = __next__  # Python 2

    def is_active(self):
        return False


class TestBidiRpc(object):
    def test_initial_state(self):
        bidi_rpc = bidi.BidiRpc(None)

        assert bidi_rpc.is_active is False

    def test_done_callbacks(self):
        bidi_rpc = bidi.BidiRpc(None)
        callback = mock.Mock(spec=['__call__'])

        bidi_rpc.add_done_callback(callback)
        bidi_rpc._on_call_done(mock.sentinel.future)

        callback.assert_called_once_with(mock.sentinel.future)

    def test_open(self):
        rpc, call = make_rpc()
        bidi_rpc = bidi.BidiRpc(rpc)

        bidi_rpc.open()

        assert bidi_rpc.call == call
        assert bidi_rpc.is_active
        call.add_done_callback.assert_called_once_with(bidi_rpc._on_call_done)

    def test_open_error_already_open(self):
        rpc, _ = make_rpc()
        bidi_rpc = bidi.BidiRpc(rpc)

        bidi_rpc.open()

        with pytest.raises(ValueError):
            bidi_rpc.open()

    def test_close(self):
        rpc, call = make_rpc()
        bidi_rpc = bidi.BidiRpc(rpc)
        bidi_rpc.open()

        bidi_rpc.close()

        call.cancel.assert_called_once()
        assert bidi_rpc.call == call
        assert bidi_rpc.is_active is False
        # ensure the request queue was signaled to stop.
        assert bidi_rpc.pending_requests == 1
        assert bidi_rpc._request_queue.get() is None

    def test_close_no_rpc(self):
        bidi_rpc = bidi.BidiRpc(None)
        bidi_rpc.close()

    def test_send(self):
        rpc, call = make_rpc()
        bidi_rpc = bidi.BidiRpc(rpc)
        bidi_rpc.open()

        bidi_rpc.send(mock.sentinel.request)

        assert bidi_rpc.pending_requests == 1
        assert bidi_rpc._request_queue.get() is mock.sentinel.request

    def test_send_not_open(self):
        rpc, call = make_rpc()
        bidi_rpc = bidi.BidiRpc(rpc)

        with pytest.raises(ValueError):
            bidi_rpc.send(mock.sentinel.request)

    def test_send_dead_rpc(self):
        error = ValueError()
        bidi_rpc = bidi.BidiRpc(None)
        bidi_rpc.call = ClosedCall(error)

        with pytest.raises(ValueError) as exc_info:
            bidi_rpc.send(mock.sentinel.request)

        assert exc_info.value == error

    def test_recv(self):
        bidi_rpc = bidi.BidiRpc(None)
        bidi_rpc.call = iter([mock.sentinel.response])

        response = bidi_rpc.recv()

        assert response == mock.sentinel.response

    def test_recv_not_open(self):
        rpc, call = make_rpc()
        bidi_rpc = bidi.BidiRpc(rpc)

        with pytest.raises(ValueError):
            bidi_rpc.recv()


class CallStub(object):
    def __init__(self, values, active=True):
        self.values = iter(values)
        self._is_active = active
        self.cancelled = False

    def __next__(self):
        item = next(self.values)
        if isinstance(item, Exception):
            self._is_active = False
            raise item
        return item

    next = __next__  # Python 2

    def is_active(self):
        return self._is_active

    def add_done_callback(self, callback):
        pass

    def cancel(self):
        self.cancelled = True


class TestResumableBidiRpc(object):
    def test_initial_state(self):
        callback = mock.Mock()
        callback.return_value = True
        bidi_rpc = bidi.ResumableBidiRpc(None, callback)

        assert bidi_rpc.is_active is False

    def test_done_callbacks_recoverable(self):
        start_rpc = mock.create_autospec(
            grpc.StreamStreamMultiCallable, instance=True)
        bidi_rpc = bidi.ResumableBidiRpc(start_rpc, lambda _: True)
        callback = mock.Mock(spec=['__call__'])

        bidi_rpc.add_done_callback(callback)
        bidi_rpc._on_call_done(mock.sentinel.future)

        callback.assert_not_called()
        start_rpc.assert_called_once()
        assert bidi_rpc.is_active

    def test_done_callbacks_non_recoverable(self):
        bidi_rpc = bidi.ResumableBidiRpc(None, lambda _: False)
        callback = mock.Mock(spec=['__call__'])

        bidi_rpc.add_done_callback(callback)
        bidi_rpc._on_call_done(mock.sentinel.future)

        callback.assert_called_once_with(mock.sentinel.future)

    def test_send_recover(self):
        error = ValueError()
        call_1 = CallStub([error], active=False)
        call_2 = CallStub([])
        start_rpc = mock.create_autospec(
            grpc.StreamStreamMultiCallable,
            instance=True,
            side_effect=[call_1, call_2])
        should_recover = mock.Mock(spec=['__call__'], return_value=True)
        bidi_rpc = bidi.ResumableBidiRpc(start_rpc, should_recover)

        bidi_rpc.open()

        bidi_rpc.send(mock.sentinel.request)

        assert bidi_rpc.pending_requests == 1
        assert bidi_rpc._request_queue.get() is mock.sentinel.request

        should_recover.assert_called_once_with(error)
        assert bidi_rpc.call == call_2
        assert bidi_rpc.is_active is True

    def test_send_failure(self):
        error = ValueError()
        call = CallStub([error], active=False)
        start_rpc = mock.create_autospec(
            grpc.StreamStreamMultiCallable,
            instance=True,
            return_value=call)
        should_recover = mock.Mock(spec=['__call__'], return_value=False)
        bidi_rpc = bidi.ResumableBidiRpc(start_rpc, should_recover)

        bidi_rpc.open()

        with pytest.raises(ValueError) as exc_info:
            bidi_rpc.send(mock.sentinel.request)

        assert exc_info.value == error
        should_recover.assert_called_once_with(error)
        assert bidi_rpc.call == call
        assert bidi_rpc.is_active is False
        assert call.cancelled is True
        assert bidi_rpc.pending_requests == 1
        assert bidi_rpc._request_queue.get() is None

    def test_recv_recover(self):
        error = ValueError()
        call_1 = CallStub([1, error])
        call_2 = CallStub([2, 3])
        start_rpc = mock.create_autospec(
            grpc.StreamStreamMultiCallable,
            instance=True,
            side_effect=[call_1, call_2])
        should_recover = mock.Mock(spec=['__call__'], return_value=True)
        bidi_rpc = bidi.ResumableBidiRpc(start_rpc, should_recover)

        bidi_rpc.open()

        values = []
        for n in range(3):
            values.append(bidi_rpc.recv())

        assert values == [1, 2, 3]
        should_recover.assert_called_once_with(error)
        assert bidi_rpc.call == call_2
        assert bidi_rpc.is_active is True

    def test_recv_recover_already_recovered(self):
        call_1 = CallStub([])
        call_2 = CallStub([])
        start_rpc = mock.create_autospec(
            grpc.StreamStreamMultiCallable,
            instance=True,
            side_effect=[call_1, call_2])
        callback = mock.Mock()
        callback.return_value = True
        bidi_rpc = bidi.ResumableBidiRpc(start_rpc, callback)

        bidi_rpc.open()

        bidi_rpc._reopen()

        assert bidi_rpc.call is call_1
        assert bidi_rpc.is_active is True

    def test_recv_failure(self):
        error = ValueError()
        call = CallStub([error])
        start_rpc = mock.create_autospec(
            grpc.StreamStreamMultiCallable,
            instance=True,
            return_value=call)
        should_recover = mock.Mock(spec=['__call__'], return_value=False)
        bidi_rpc = bidi.ResumableBidiRpc(start_rpc, should_recover)

        bidi_rpc.open()

        with pytest.raises(ValueError) as exc_info:
            bidi_rpc.recv()

        assert exc_info.value == error
        should_recover.assert_called_once_with(error)
        assert bidi_rpc.call == call
        assert bidi_rpc.is_active is False
        assert call.cancelled is True

    def test_reopen_failure_on_rpc_restart(self):
        error1 = ValueError('1')
        error2 = ValueError('2')
        call = CallStub([error1])
        # Invoking start RPC a second time will trigger an error.
        start_rpc = mock.create_autospec(
            grpc.StreamStreamMultiCallable,
            instance=True,
            side_effect=[call, error2])
        should_recover = mock.Mock(spec=['__call__'], return_value=True)
        callback = mock.Mock(spec=['__call__'])

        bidi_rpc = bidi.ResumableBidiRpc(start_rpc, should_recover)
        bidi_rpc.add_done_callback(callback)

        bidi_rpc.open()

        with pytest.raises(ValueError) as exc_info:
            bidi_rpc.recv()

        assert exc_info.value == error2
        should_recover.assert_called_once_with(error1)
        assert bidi_rpc.call is None
        assert bidi_rpc.is_active is False
        callback.assert_called_once_with(error2)

    def test_send_not_open(self):
        bidi_rpc = bidi.ResumableBidiRpc(None, lambda _: False)

        with pytest.raises(ValueError):
            bidi_rpc.send(mock.sentinel.request)

    def test_recv_not_open(self):
        bidi_rpc = bidi.ResumableBidiRpc(None, lambda _: False)

        with pytest.raises(ValueError):
            bidi_rpc.recv()

    def test_finalize_idempotent(self):
        error1 = ValueError('1')
        error2 = ValueError('2')
        callback = mock.Mock(spec=['__call__'])
        should_recover = mock.Mock(spec=['__call__'], return_value=False)

        bidi_rpc = bidi.ResumableBidiRpc(
            mock.sentinel.start_rpc, should_recover)

        bidi_rpc.add_done_callback(callback)

        bidi_rpc._on_call_done(error1)
        bidi_rpc._on_call_done(error2)

        callback.assert_called_once_with(error1)


class TestBackgroundConsumer(object):
    def test_consume_once_then_exit(self):
        bidi_rpc = mock.create_autospec(bidi.BidiRpc, instance=True)
        bidi_rpc.is_active = True
        bidi_rpc.recv.side_effect = [mock.sentinel.response_1]
        recved = threading.Event()

        def on_response(response):
            assert response == mock.sentinel.response_1
            bidi_rpc.is_active = False
            recved.set()

        consumer = bidi.BackgroundConsumer(bidi_rpc, on_response)

        consumer.start()

        recved.wait()

        bidi_rpc.recv.assert_called_once()
        assert bidi_rpc.is_active is False

        consumer.stop()

        bidi_rpc.close.assert_called_once()
        assert consumer.is_active is False

    def test_pause_resume_and_close(self):
        # This test is relatively complex. It attempts to start the consumer,
        # consume one item, pause the consumer, check the state of the world,
        # then resume the consumer. Doing this in a deterministic fashion
        # requires a bit more mocking and patching than usual.

        bidi_rpc = mock.create_autospec(bidi.BidiRpc, instance=True)
        bidi_rpc.is_active = True

        def close_side_effect():
            bidi_rpc.is_active = False

        bidi_rpc.close.side_effect = close_side_effect

        # These are used to coordinate the two threads to ensure deterministic
        # execution.
        should_continue = threading.Event()
        responses_and_events = {
            mock.sentinel.response_1: threading.Event(),
            mock.sentinel.response_2: threading.Event()
        }
        bidi_rpc.recv.side_effect = [
            mock.sentinel.response_1, mock.sentinel.response_2]

        recved_responses = []
        consumer = None

        def on_response(response):
            if response == mock.sentinel.response_1:
                consumer.pause()

            recved_responses.append(response)
            responses_and_events[response].set()
            should_continue.wait()

        consumer = bidi.BackgroundConsumer(bidi_rpc, on_response)

        consumer.start()

        # Wait for the first response to be recved.
        responses_and_events[mock.sentinel.response_1].wait()

        # Ensure only one item has been recved and that the consumer is paused.
        assert recved_responses == [mock.sentinel.response_1]
        assert consumer.is_paused is True
        assert consumer.is_active is True

        # Unpause the consumer, wait for the second item, then close the
        # consumer.
        should_continue.set()
        consumer.resume()

        responses_and_events[mock.sentinel.response_2].wait()

        assert recved_responses == [
            mock.sentinel.response_1, mock.sentinel.response_2]

        consumer.stop()

        assert consumer.is_active is False

    def test_wake_on_error(self):
        should_continue = threading.Event()

        bidi_rpc = mock.create_autospec(bidi.BidiRpc, instance=True)
        bidi_rpc.is_active = True
        bidi_rpc.add_done_callback.side_effect = (
            lambda _: should_continue.set())

        consumer = bidi.BackgroundConsumer(bidi_rpc, mock.sentinel.on_response)

        # Start the consumer paused, which should immediately put it into wait
        # state.
        consumer.pause()
        consumer.start()

        # Wait for add_done_callback to be called
        should_continue.wait()
        bidi_rpc.add_done_callback.assert_called_once_with(
            consumer._on_call_done)

        # The consumer should now be blocked on waiting to be unpaused.
        assert consumer.is_active
        assert consumer.is_paused

        # Trigger the done callback, it should unpause the consumer and cause
        # it to exit.
        bidi_rpc.is_active = False
        consumer._on_call_done(bidi_rpc)

        # It may take a few cycles for the thread to exit.
        while consumer.is_active:
            pass

    def test_consumer_expected_error(self, caplog):
        caplog.set_level(logging.DEBUG)

        bidi_rpc = mock.create_autospec(bidi.BidiRpc, instance=True)
        bidi_rpc.is_active = True
        bidi_rpc.recv.side_effect = exceptions.ServiceUnavailable('Gone away')

        on_response = mock.Mock(spec=['__call__'])

        consumer = bidi.BackgroundConsumer(bidi_rpc, on_response)

        consumer.start()

        # Wait for the consumer's thread to exit.
        while consumer.is_active:
            pass

        on_response.assert_not_called()
        bidi_rpc.recv.assert_called_once()
        assert 'caught error' in caplog.text

    def test_consumer_unexpected_error(self, caplog):
        caplog.set_level(logging.DEBUG)

        bidi_rpc = mock.create_autospec(bidi.BidiRpc, instance=True)
        bidi_rpc.is_active = True
        bidi_rpc.recv.side_effect = ValueError()

        on_response = mock.Mock(spec=['__call__'])

        consumer = bidi.BackgroundConsumer(bidi_rpc, on_response)

        consumer.start()

        # Wait for the consumer's thread to exit.
        while consumer.is_active:
            pass

        on_response.assert_not_called()
        bidi_rpc.recv.assert_called_once()
        assert 'caught unexpected exception' in caplog.text

    def test_double_stop(self, caplog):
        caplog.set_level(logging.DEBUG)
        bidi_rpc = mock.create_autospec(bidi.BidiRpc, instance=True)
        bidi_rpc.is_active = True
        on_response = mock.Mock(spec=['__call__'])

        def close_side_effect():
            bidi_rpc.is_active = False

        bidi_rpc.close.side_effect = close_side_effect

        consumer = bidi.BackgroundConsumer(bidi_rpc, on_response)

        consumer.start()
        assert consumer.is_active is True

        consumer.stop()
        assert consumer.is_active is False

        # calling stop twice should not result in an error.
        consumer.stop()
