import unittest2


class Test_StorageError(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.exceptions import StorageError
        return StorageError

    def _makeOne(self, *args):
        return self._getTargetClass()(*args)

    def test_ctor_defaults(self):
        e = self._makeOne('Testing')
        e.code = 600
        self.assertEqual(str(e), '600 Testing')
        self.assertEqual(e.message, 'Testing')
        self.assertEqual(list(e.errors), [])

    def test_ctor_explicit(self):
        ERROR = {
            'domain': 'global',
            'location': 'test',
            'locationType': 'testing',
            'message': 'Testing',
            'reason': 'test',
            }
        e = self._makeOne('Testing', [ERROR])
        e.code = 600
        self.assertEqual(str(e), '600 Testing')
        self.assertEqual(e.message, 'Testing')
        self.assertEqual(list(e.errors), [ERROR])


class Test_make_exception(unittest2.TestCase):

    def _callFUT(self, response, content):
        from gcloud.storage.exceptions import make_exception
        return make_exception(response, content)

    def test_hit_w_content_as_str(self):
        from gcloud.storage.exceptions import NotFound
        response = _Response(404)
        content = '{"message": "Not Found"}'
        exception = self._callFUT(response, content)
        self.assertTrue(isinstance(exception, NotFound))
        self.assertEqual(exception.message, 'Not Found')
        self.assertEqual(list(exception.errors), [])

    def test_miss_w_content_as_dict(self):
        from gcloud.storage.exceptions import StorageError
        ERROR = {
            'domain': 'global',
            'location': 'test',
            'locationType': 'testing',
            'message': 'Testing',
            'reason': 'test',
            }
        response = _Response(600)
        content = {"message": "Unknown Error", "error": {"errors": [ERROR]}}
        exception = self._callFUT(response, content)
        self.assertTrue(isinstance(exception, StorageError))
        self.assertEqual(exception.message, 'Unknown Error')
        self.assertEqual(list(exception.errors), [ERROR])


class _Response(object):
    def __init__(self, status):
        self.status = status
