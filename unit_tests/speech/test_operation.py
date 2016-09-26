import unittest


class OperationTests(unittest.TestCase):

    OPERATION_NAME = '123456789'

    def _getTargetClass(self):
        from google.cloud.speech.operation import Operation
        return Operation

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor_defaults(self):
        client = _Client()
        operation = self._makeOne(client, self.OPERATION_NAME)
        self.assertEqual('123456789', operation.name)
        self.assertFalse(operation.complete)
        self.assertIsNone(operation.last_updated)
        self.assertEqual(0, operation.progress_percent)
        self.assertIsNone(operation.results)
        self.assertIsNone(operation.start_time)

    def test_from_api_repr(self):
        from unit_tests.speech._fixtures import OPERATION_COMPLETE_RESPONSE
        RESPONSE = OPERATION_COMPLETE_RESPONSE

        client = _Client()
        connection = _Connection(OPERATION_COMPLETE_RESPONSE)
        client.connection = connection
        operation = self._getTargetClass().from_api_repr(client, RESPONSE)

        self.assertEqual('123456789', operation.name)
        self.assertTrue(operation.complete)

        alternatives = operation.results[0]['alternatives']

        self.assertEqual('how old is the Brooklyn Bridge',
                         alternatives[0]['transcript'])
        self.assertEqual(0.98267895, alternatives[0]['confidence'])
        self.assertTrue(operation.complete)

    def test_update_response(self):
        from unit_tests.speech._fixtures import ASYNC_RECOGNIZE_RESPONSE
        from unit_tests.speech._fixtures import OPERATION_COMPLETE_RESPONSE
        RESPONSE = ASYNC_RECOGNIZE_RESPONSE

        client = _Client()
        connection = _Connection(OPERATION_COMPLETE_RESPONSE)
        client.connection = connection
        operation = self._getTargetClass().from_api_repr(client, RESPONSE)
        self.assertEqual('123456789', operation.name)

        operation._update(OPERATION_COMPLETE_RESPONSE)
        self.assertTrue(operation.complete)

    def test_poll(self):
        from unit_tests.speech._fixtures import ASYNC_RECOGNIZE_RESPONSE
        from unit_tests.speech._fixtures import OPERATION_COMPLETE_RESPONSE
        RESPONSE = ASYNC_RECOGNIZE_RESPONSE
        client = _Client()
        connection = _Connection(OPERATION_COMPLETE_RESPONSE)
        client.connection = connection

        operation = self._getTargetClass().from_api_repr(client, RESPONSE)
        self.assertFalse(operation.complete)
        operation.poll()
        self.assertTrue(operation.complete)

    def test_poll_complete(self):
        from unit_tests.speech._fixtures import OPERATION_COMPLETE_RESPONSE
        RESPONSE = OPERATION_COMPLETE_RESPONSE
        client = _Client()
        connection = _Connection(OPERATION_COMPLETE_RESPONSE)
        client.connection = connection

        operation = self._getTargetClass().from_api_repr(client, RESPONSE)
        self.assertTrue(operation.complete)
        with self.assertRaises(ValueError):
            operation.poll()


class _Connection(object):
    def __init__(self, response):
        self.response = response

    def api_request(self, method, path):
        return self.response


class _Client(object):
    connection = None
