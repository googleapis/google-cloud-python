import unittest2


class TestConnection(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.connection import Connection
        return Connection

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        conn = self._makeOne()
        self.assertEqual(conn.credentials, None)

    def test_ctor_explicit(self):
        creds = object()
        conn = self._makeOne(creds)
        self.assertTrue(conn.credentials is creds)

    def test_http_w_existing(self):
        conn = self._makeOne()
        conn._http = http = object()
        self.assertTrue(conn.http is http)

    def test_http_wo_creds(self):
        from httplib2 import Http
        conn = self._makeOne()
        self.assertTrue(isinstance(conn.http, Http))

    def test_http_w_creds(self):
        from httplib2 import Http

        authorized = object()

        class Creds(object):
            def authorize(self, http):
                self._called_with = http
                return authorized
        creds = Creds()
        conn = self._makeOne(creds)
        self.assertTrue(conn.http is authorized)
        self.assertTrue(isinstance(creds._called_with, Http))

    def test_user_agent_format(self):
        from pkg_resources import get_distribution
        expected_ua = 'gcloud-python/{0}'.format(
            get_distribution('gcloud').version)
        conn = self._makeOne()
        self.assertEqual(conn.USER_AGENT, expected_ua)
