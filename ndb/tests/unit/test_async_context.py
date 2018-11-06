import unittest

from google.cloud.ndb import _eventloop
from google.cloud.ndb import async_context


@unittest.mock.patch("google.cloud.ndb.async_context._eventloop.EventLoop")
def test_async_context(EventLoop):
    one = unittest.mock.Mock()
    two = unittest.mock.Mock()
    EventLoop.return_value = one
    assert _eventloop.contexts.current() is None
    with async_context.async_context():
        assert _eventloop.contexts.current() is one
        one.run.assert_not_called()
        EventLoop.return_value = two
        with async_context.async_context():
            assert _eventloop.contexts.current() is two
            two.run.assert_not_called()
        assert _eventloop.contexts.current() is one
        one.run.assert_not_called()
        two.run.assert_called_once_with()
    assert _eventloop.contexts.current() is None
    one.run.assert_called_once_with()
