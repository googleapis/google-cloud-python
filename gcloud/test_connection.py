# This is test code, globally disable docstrings.
# pylint: disable=missing-docstring
import unittest2


class TestConnection(unittest2.TestCase):  # pylint: disable=R0904

    def _getTargetClass(self):  # pylint: disable=invalid-name,no-self-use
        from gcloud.connection import Connection
        return Connection

    def _makeOne(self, *args, **kw):  # pylint: disable=invalid-name
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
        conn._http = http = object()  # pylint: disable=protected-access
        self.assertTrue(conn.http is http)

    def test_http_wo_creds(self):
        from httplib2 import Http
        conn = self._makeOne()
        self.assertTrue(isinstance(conn.http, Http))

    def test_http_w_creds(self):
        from httplib2 import Http

        authorized = object()

        class Creds(object):  # pylint: disable=too-few-public-methods
            def authorize(self, http):
                # pylint: disable=attribute-defined-outside-init
                self._called_with = http
                # pylint: enable=attribute-defined-outside-init
                return authorized
        creds = Creds()
        conn = self._makeOne(creds)
        self.assertTrue(conn.http is authorized)
        # pylint: disable=protected-access
        self.assertTrue(isinstance(creds._called_with, Http))
        # pylint: enable=protected-access

    def test_user_agent_format(self):
        from pkg_resources import get_distribution
        expected_ua = 'gcloud-python/{0}'.format(
            get_distribution('gcloud').version)
        conn = self._makeOne()
        self.assertEqual(conn.USER_AGENT, expected_ua)
