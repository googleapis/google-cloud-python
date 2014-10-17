import unittest2


class TestConnectionError(unittest2.TestCase):

    @staticmethod
    def _getTargetClass():
        from gcloud.storage.exceptions import ConnectionError
        return ConnectionError

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_no_headers(self):
        e = self._makeOne({}, '')
        self.assertEqual(str(e), '{}')
        self.assertEqual(e.message, '{}')


class TestNotFoundError(unittest2.TestCase):

    @staticmethod
    def _getTargetClass():
        from gcloud.storage.exceptions import NotFoundError
        return NotFoundError

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_no_headers(self):
        e = self._makeOne({})
        self.assertEqual(str(e), '')
        self.assertEqual(e.message, 'Request returned a 404. Headers: {}')
