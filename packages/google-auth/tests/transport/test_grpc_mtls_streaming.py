import pytest
from unittest import mock
import grpc
import threading
import time

from google.auth.transport.grpc import (
    _ReplayableIterator,
    _MTLSRefreshingChannel,
    _MTLSCallInterceptor,
)
from google.auth.transport import _mtls_helper

class TestReplayableIterator:
    def test_buffer_and_replay(self):
        source = iter([1, 2, 3])
        replayable = _ReplayableIterator(source, max_items=2)
        
        # Read two items
        reader = iter(replayable)
        assert next(reader) == 1
        assert next(reader) == 2
        
        # Reader is preempted/dies, we should be able to start another reader
        # since it fits in the buffer
        assert replayable.can_replay()
        
        reader2 = iter(replayable)
        assert next(reader2) == 1
        assert next(reader2) == 2
        assert next(reader2) == 3
        
        # Since it exceeded max_items=2 during reading 3, can_replay becomes False
        assert not replayable.can_replay()

    def test_concurrent_handoff(self):
        def slow_source():
            yield 1
            yield 2
            time.sleep(0.5)
            yield 3

        replayable = _ReplayableIterator(slow_source())
        reader1 = iter(replayable)
        
        # start first reader in a thread
        values1 = []
        def read_thread():
            try:
                for v in reader1:
                    values1.append(v)
            except Exception:
                pass
                
        t = threading.Thread(target=read_thread)
        t.start()
        
        # let it read 1, 2
        time.sleep(0.1)
        
        # Now start second reader. First reader should abort when it wakes up.
        reader2 = iter(replayable)
        values2 = [v for v in reader2]
        
        t.join()
        
        # Reader 1 should only have read 1, 2 before being aborted
        assert values1 == [1, 2]
        # Reader 2 should get everything
        assert values2 == [1, 2, 3]


class _MockCall(grpc.Call):
    def __init__(self, code, should_fail=True):
        self._code = code
        self._should_fail = should_fail
        self._count = 0

    def code(self):
        return self._code

    def is_active(self):
        return True

    def __iter__(self):
        return self

    def __next__(self):
        if self._count == 0 and self._should_fail:
            self._count += 1
            err = grpc.RpcError()
            err.code = lambda: self._code
            raise err
        self._count += 1
        return "success"


class TestMTLSRefreshingChannel:
    @mock.patch("google.auth.transport._mtls_helper.check_parameters_for_unauthorized_response")
    @mock.patch("google.auth.transport.grpc.secure_authorized_channel")
    def test_refresh_logic(self, mock_secure_channel, mock_check_params):
        # mock fingerprint differences indicating rotation is needed
        mock_check_params.return_value = (None, None, b"old", b"new")
        mock_secure_channel.return_value = mock.Mock(spec=grpc.Channel)
        
        initial_channel = mock.Mock(spec=grpc.Channel)
        wrapper = _MTLSRefreshingChannel(
            target="target",
            factory_args={},
            initial_channel=initial_channel,
            initial_cert=b"old_cert"
        )
        
        # Subscribing adds to the initial channel
        mock_callback = mock.Mock()
        wrapper.subscribe(mock_callback)
        initial_channel.subscribe.assert_called_with(mock_callback, try_to_connect=False)
        
        wrapper.refresh_logic(1)
        
        initial_channel.unsubscribe.assert_called_with(mock_callback)
        mock_secure_channel.return_value.subscribe.assert_called_with(mock_callback)

