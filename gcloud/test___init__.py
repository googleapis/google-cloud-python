# Copyright 2014 Google Inc. All rights reserved.
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

import unittest2


class Test__UserAgentReifyProperty(unittest2.TestCase):

    def setUp(self):
        from gcloud.connection import Connection
        self._original_connection_user_agent = Connection.user_agent
        Connection.user_agent = self._makeOne(_NamedObject('user_agent'))

    def tearDown(self):
        from gcloud.connection import Connection
        Connection.user_agent = self._original_connection_user_agent

    def _getTargetClass(self):
        from gcloud import _UserAgentReifyProperty
        return _UserAgentReifyProperty

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        ua_prop = self._makeOne(_NamedObject())
        self.assertEqual(ua_prop._property_name, _NamedObject.NAME_VAL)
        self.assertEqual(ua_prop._curr_environ, None)
        self.assertEqual(ua_prop._user_agent, None)

    def test_ctor_appengine_loaded(self):
        import gcloud
        from gcloud._testing import _Monkey

        NON_NULL = object()
        with _Monkey(gcloud, appengine=NON_NULL):
            ua_prop = self._makeOne(_NamedObject())
        self.assertEqual(ua_prop._property_name, _NamedObject.NAME_VAL)
        self.assertEqual(ua_prop._curr_environ, '-GAE')
        self.assertEqual(ua_prop._user_agent, None)

    def _check_compute_engine_helper(self, status, result):
        import gcloud
        from gcloud._testing import _Monkey

        if status == 'RAISE':
            CONNECTION = _TimeoutHTTPConnection()
        else:
            CONNECTION = _HTTPConnection(status)

        CONNECTION.created = 0

        def _factory(host, timeout):
            CONNECTION.created += 1
            CONNECTION.host = host
            CONNECTION.timeout = timeout
            return CONNECTION

        klass = self._getTargetClass()
        with _Monkey(gcloud, HTTPConnection=_factory):
            gce_str = klass.check_compute_engine()
        self.assertEqual(gce_str, result)

        self.assertEqual(CONNECTION.created, 1)
        self.assertEqual(CONNECTION.host, '169.254.169.254')
        self.assertEqual(CONNECTION.timeout, 0.1)
        self.assertEqual(
            CONNECTION._called_args,
            [('GET', '/computeMetadata/v1/project/project-id')])
        expected_kwargs = {
            'headers': {
                'Metadata-Flavor': 'Google',
            },
        }
        self.assertEqual(CONNECTION._called_kwargs, [expected_kwargs])
        self.assertEqual(CONNECTION._close_count, 1)

    def test_check_compute_engine_fail(self):
        self._check_compute_engine_helper(404, None)

    def test_check_compute_engine_raise(self):
        self._check_compute_engine_helper('RAISE', None)

    def test_check_compute_engine_success(self):
        self._check_compute_engine_helper(200, '-GCE')

    def test_class_property_on_connection(self):
        from gcloud.connection import Connection

        klass = self._getTargetClass()
        self.assertTrue(isinstance(Connection.user_agent, klass))

    def test_instance_property_on_connection_default(self):
        import gcloud
        from gcloud.connection import Connection

        cnxn = Connection()
        expected_ua = 'gcloud-python/{0}'.format(gcloud.__version__)
        self.assertEqual(cnxn.user_agent, expected_ua)

    def test___get___access_twice(self):
        import gcloud
        from gcloud.connection import Connection

        expected_ua = 'gcloud-python/{0}'.format(gcloud.__version__)

        self.assertEqual(Connection.user_agent._user_agent, None)
        value = Connection.user_agent.__get__(_NamedObject())
        self.assertEqual(value, expected_ua)

        # Now test using it a second time.
        self.assertEqual(Connection.user_agent._user_agent, expected_ua)
        value_again = Connection.user_agent.__get__(_NamedObject())
        self.assertEqual(value_again, expected_ua)

    def test_instance_property_connection_with_appengine(self):
        import gcloud
        from gcloud._testing import _Monkey
        from gcloud.connection import Connection

        NON_NULL = object()
        with _Monkey(gcloud, appengine=NON_NULL):
            local_prop = self._makeOne(_NamedObject('user_agent'))
            with _Monkey(Connection, user_agent=local_prop):
                cnxn = Connection()
                value = cnxn.user_agent

        expected_ua = 'gcloud-python/{0}-GAE'.format(gcloud.__version__)
        self.assertEqual(value, expected_ua)

    def test_instance_property_connection_with_compute_engine(self):
        import gcloud
        from gcloud._testing import _Monkey
        from gcloud.connection import Connection

        CONNECTION = _HTTPConnection(200)
        CONNECTION.created = 0

        def _factory(host, timeout):
            CONNECTION.created += 1
            CONNECTION.host = host
            CONNECTION.timeout = timeout
            return CONNECTION

        with _Monkey(gcloud, HTTPConnection=_factory):
            local_prop = self._makeOne(_NamedObject('user_agent'))
            with _Monkey(Connection, user_agent=local_prop):
                cnxn = Connection()
                value = cnxn.user_agent

        expected_ua = 'gcloud-python/{0}-GCE'.format(gcloud.__version__)
        self.assertEqual(value, expected_ua)


class _NamedObject(object):

    NAME_VAL = object()

    def __init__(self, name=None):
        self.__name__ = name or self.NAME_VAL


class _HTTPResponse(object):

    def __init__(self, status):
        self.status = status


class _BaseHTTPConnection(object):

    host = timeout = None

    def __init__(self):
        self._close_count = 0
        self._called_args = []
        self._called_kwargs = []

    def request(self, method, uri, **kwargs):
        self._called_args.append((method, uri))
        self._called_kwargs.append(kwargs)

    def close(self):
        self._close_count += 1


class _HTTPConnection(_BaseHTTPConnection):

    def __init__(self, status):
        super(_HTTPConnection, self).__init__()
        self.status = status

    def getresponse(self):
        return _HTTPResponse(self.status)


class _TimeoutHTTPConnection(_BaseHTTPConnection):

    def getresponse(self):
        import socket
        raise socket.timeout('timed out')
