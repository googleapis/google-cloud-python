# Copyright 2014 Google Inc.
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

import os
import unittest


class Test__LocalStack(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud._helpers import _LocalStack

        return _LocalStack

    def _make_one(self):
        return self._get_target_class()()

    def test_it(self):
        batch1, batch2 = object(), object()
        batches = self._make_one()
        self.assertEqual(list(batches), [])
        self.assertIsNone(batches.top)
        batches.push(batch1)
        self.assertIs(batches.top, batch1)
        batches.push(batch2)
        self.assertIs(batches.top, batch2)
        popped = batches.pop()
        self.assertIs(popped, batch2)
        self.assertIs(batches.top, batch1)
        self.assertEqual(list(batches), [batch1])
        popped = batches.pop()
        self.assertIsNone(batches.top)
        self.assertEqual(list(batches), [])


class Test__UTC(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud._helpers import _UTC
        return _UTC

    def _make_one(self):
        return self._get_target_class()()

    def test_module_property(self):
        from google.cloud import _helpers as MUT
        klass = self._get_target_class()
        try:
            import pytz
        except ImportError:
            self.assertIsInstance(MUT.UTC, klass)
        else:
            self.assertIs(MUT.UTC, pytz.UTC)  # pragma: NO COVER

    def test_dst(self):
        import datetime

        tz = self._make_one()
        self.assertEqual(tz.dst(None), datetime.timedelta(0))

    def test_fromutc(self):
        import datetime

        naive_epoch = datetime.datetime.utcfromtimestamp(0)
        self.assertIsNone(naive_epoch.tzinfo)
        tz = self._make_one()
        epoch = tz.fromutc(naive_epoch)
        self.assertEqual(epoch.tzinfo, tz)

    def test_tzname(self):
        tz = self._make_one()
        self.assertEqual(tz.tzname(None), 'UTC')

    def test_utcoffset(self):
        import datetime

        tz = self._make_one()
        self.assertEqual(tz.utcoffset(None), datetime.timedelta(0))

    def test___repr__(self):
        tz = self._make_one()
        self.assertEqual(repr(tz), '<UTC>')

    def test___str__(self):
        tz = self._make_one()
        self.assertEqual(str(tz), 'UTC')


class Test__ensure_tuple_or_list(unittest.TestCase):

    def _call_fut(self, arg_name, tuple_or_list):
        from google.cloud._helpers import _ensure_tuple_or_list
        return _ensure_tuple_or_list(arg_name, tuple_or_list)

    def test_valid_tuple(self):
        valid_tuple_or_list = ('a', 'b', 'c', 'd')
        result = self._call_fut('ARGNAME', valid_tuple_or_list)
        self.assertEqual(result, ['a', 'b', 'c', 'd'])

    def test_valid_list(self):
        valid_tuple_or_list = ['a', 'b', 'c', 'd']
        result = self._call_fut('ARGNAME', valid_tuple_or_list)
        self.assertEqual(result, valid_tuple_or_list)

    def test_invalid(self):
        invalid_tuple_or_list = object()
        with self.assertRaises(TypeError):
            self._call_fut('ARGNAME', invalid_tuple_or_list)

    def test_invalid_iterable(self):
        invalid_tuple_or_list = 'FOO'
        with self.assertRaises(TypeError):
            self._call_fut('ARGNAME', invalid_tuple_or_list)


class Test__app_engine_id(unittest.TestCase):

    def _call_fut(self):
        from google.cloud._helpers import _app_engine_id
        return _app_engine_id()

    def test_no_value(self):
        from google.cloud._testing import _Monkey
        from google.cloud import _helpers

        with _Monkey(_helpers, app_identity=None):
            dataset_id = self._call_fut()
            self.assertIsNone(dataset_id)

    def test_value_set(self):
        from google.cloud._testing import _Monkey
        from google.cloud import _helpers

        APP_ENGINE_ID = object()
        APP_IDENTITY = _AppIdentity(APP_ENGINE_ID)
        with _Monkey(_helpers, app_identity=APP_IDENTITY):
            dataset_id = self._call_fut()
            self.assertEqual(dataset_id, APP_ENGINE_ID)


class Test__file_project_id(unittest.TestCase):

    def _call_fut(self):
        from google.cloud._helpers import _file_project_id
        return _file_project_id()

    def test_success(self):
        from google.cloud.environment_vars import CREDENTIALS
        from google.cloud._testing import _Monkey
        from google.cloud._testing import _NamedTemporaryFile

        project_id = 'test-project-id'
        payload = '{"%s":"%s"}' % ('project_id', project_id)
        with _NamedTemporaryFile() as temp:
            with open(temp.name, 'w') as creds_file:
                creds_file.write(payload)

            environ = {CREDENTIALS: temp.name}
            with _Monkey(os, getenv=environ.get):
                result = self._call_fut()

            self.assertEqual(result, project_id)

    def test_no_environment_variable_set(self):
        from google.cloud._testing import _Monkey

        environ = {}
        with _Monkey(os, getenv=environ.get):
            result = self._call_fut()

        self.assertIsNone(result)


class Test__get_nix_config_path(unittest.TestCase):

    def _call_fut(self):
        from google.cloud._helpers import _get_nix_config_path
        return _get_nix_config_path()

    def test_it(self):
        from google.cloud import _helpers as MUT
        from google.cloud._testing import _Monkey

        user_root = 'a'
        config_file = 'b'
        with _Monkey(MUT, _USER_ROOT=user_root,
                     _GCLOUD_CONFIG_FILE=config_file):
            result = self._call_fut()

        expected = os.path.join(user_root, '.config', config_file)
        self.assertEqual(result, expected)


class Test__get_windows_config_path(unittest.TestCase):

    def _call_fut(self):
        from google.cloud._helpers import _get_windows_config_path
        return _get_windows_config_path()

    def test_it(self):
        from google.cloud import _helpers as MUT
        from google.cloud._testing import _Monkey

        appdata_dir = 'a'
        environ = {'APPDATA': appdata_dir}
        config_file = 'b'
        with _Monkey(os, getenv=environ.get):
            with _Monkey(MUT, _GCLOUD_CONFIG_FILE=config_file):
                result = self._call_fut()

        expected = os.path.join(appdata_dir, config_file)
        self.assertEqual(result, expected)


class Test__default_service_project_id(unittest.TestCase):

    CONFIG_TEMPLATE = '[%s]\n%s = %s\n'

    def _call_fut(self):
        from google.cloud._helpers import _default_service_project_id
        return _default_service_project_id()

    def test_nix(self):
        from google.cloud import _helpers as MUT
        from google.cloud._testing import _Monkey
        from google.cloud._testing import _NamedTemporaryFile

        project_id = 'test-project-id'
        with _NamedTemporaryFile() as temp:
            config_value = self.CONFIG_TEMPLATE % (
                MUT._GCLOUD_CONFIG_SECTION,
                MUT._GCLOUD_CONFIG_KEY, project_id)
            with open(temp.name, 'w') as config_file:
                config_file.write(config_value)

            def mock_get_path():
                return temp.name

            with _Monkey(os, name='not-nt'):
                with _Monkey(MUT, _get_nix_config_path=mock_get_path,
                             _USER_ROOT='not-None'):
                    result = self._call_fut()

            self.assertEqual(result, project_id)

    def test_nix_missing_prject_key(self):
        from google.cloud import _helpers as MUT
        from google.cloud._testing import _Monkey
        from google.cloud._testing import _NamedTemporaryFile

        with _NamedTemporaryFile() as temp:
            config_value = '[%s]' % (MUT._GCLOUD_CONFIG_SECTION,)
            with open(temp.name, 'w') as config_file:
                config_file.write(config_value)

            def mock_get_path():
                return temp.name

            with _Monkey(os, name='not-nt'):
                with _Monkey(MUT, _get_nix_config_path=mock_get_path,
                             _USER_ROOT='not-None'):
                    result = self._call_fut()

            self.assertEqual(result, None)

    def test_windows(self):
        from google.cloud import _helpers as MUT
        from google.cloud._testing import _Monkey
        from google.cloud._testing import _NamedTemporaryFile

        project_id = 'test-project-id'
        with _NamedTemporaryFile() as temp:
            config_value = self.CONFIG_TEMPLATE % (
                MUT._GCLOUD_CONFIG_SECTION,
                MUT._GCLOUD_CONFIG_KEY, project_id)
            with open(temp.name, 'w') as config_file:
                config_file.write(config_value)

            def mock_get_path():
                return temp.name

            with _Monkey(os, name='nt'):
                with _Monkey(MUT, _get_windows_config_path=mock_get_path,
                             _USER_ROOT=None):
                    result = self._call_fut()

            self.assertEqual(result, project_id)

    def test_gae(self):
        from google.cloud import _helpers as MUT
        from google.cloud._testing import _Monkey

        with _Monkey(os, name='not-nt'):
            with _Monkey(MUT, _USER_ROOT=None):
                result = self._call_fut()

        self.assertIsNone(result)


class Test__compute_engine_id(unittest.TestCase):

    def _call_fut(self):
        from google.cloud._helpers import _compute_engine_id
        return _compute_engine_id()

    def _monkeyConnection(self, connection):
        from six.moves import http_client
        from google.cloud._testing import _Monkey

        def _connection_factory(host, timeout):
            connection.host = host
            connection.timeout = timeout
            return connection

        return _Monkey(http_client, HTTPConnection=_connection_factory)

    def test_bad_status(self):
        connection = _HTTPConnection(404, None)
        with self._monkeyConnection(connection):
            dataset_id = self._call_fut()
            self.assertIsNone(dataset_id)

    def test_success(self):
        COMPUTE_ENGINE_ID = object()
        connection = _HTTPConnection(200, COMPUTE_ENGINE_ID)
        with self._monkeyConnection(connection):
            dataset_id = self._call_fut()
            self.assertEqual(dataset_id, COMPUTE_ENGINE_ID)

    def test_socket_raises(self):
        connection = _TimeoutHTTPConnection()
        with self._monkeyConnection(connection):
            dataset_id = self._call_fut()
            self.assertIsNone(dataset_id)


class Test__get_production_project(unittest.TestCase):

    def _call_fut(self):
        from google.cloud._helpers import _get_production_project
        return _get_production_project()

    def test_no_value(self):
        from google.cloud._testing import _Monkey

        environ = {}
        with _Monkey(os, getenv=environ.get):
            project = self._call_fut()
            self.assertIsNone(project)

    def test_value_set(self):
        from google.cloud._testing import _Monkey
        from google.cloud._helpers import PROJECT

        MOCK_PROJECT = object()
        environ = {PROJECT: MOCK_PROJECT}
        with _Monkey(os, getenv=environ.get):
            project = self._call_fut()
            self.assertEqual(project, MOCK_PROJECT)


class Test__determine_default_project(unittest.TestCase):

    def _call_fut(self, project=None):
        from google.cloud._helpers import _determine_default_project
        return _determine_default_project(project=project)

    def _determine_default_helper(self, prod=None, gae=None, gce=None,
                                  file_id=None, srv_id=None, project=None):
        from google.cloud._testing import _Monkey
        from google.cloud import _helpers

        _callers = []

        def prod_mock():
            _callers.append('prod_mock')
            return prod

        def file_id_mock():
            _callers.append('file_id_mock')
            return file_id

        def srv_id_mock():
            _callers.append('srv_id_mock')
            return srv_id

        def gae_mock():
            _callers.append('gae_mock')
            return gae

        def gce_mock():
            _callers.append('gce_mock')
            return gce

        patched_methods = {
            '_get_production_project': prod_mock,
            '_file_project_id': file_id_mock,
            '_default_service_project_id': srv_id_mock,
            '_app_engine_id': gae_mock,
            '_compute_engine_id': gce_mock,
        }

        with _Monkey(_helpers, **patched_methods):
            returned_project = self._call_fut(project)

        return returned_project, _callers

    def test_no_value(self):
        project, callers = self._determine_default_helper()
        self.assertIsNone(project)
        self.assertEqual(callers, ['prod_mock', 'file_id_mock', 'srv_id_mock',
                                   'gae_mock', 'gce_mock'])

    def test_explicit(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(project=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, [])

    def test_prod(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(prod=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, ['prod_mock'])

    def test_gae(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(gae=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, ['prod_mock', 'file_id_mock',
                                   'srv_id_mock', 'gae_mock'])

    def test_gce(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(gce=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, ['prod_mock', 'file_id_mock', 'srv_id_mock',
                                   'gae_mock', 'gce_mock'])


class Test__millis(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud._helpers import _millis
        return _millis(value)

    def test_one_second_from_epoch(self):
        import datetime
        from google.cloud._helpers import UTC

        WHEN = datetime.datetime(1970, 1, 1, 0, 0, 1, tzinfo=UTC)
        self.assertEqual(self._call_fut(WHEN), 1000)


class Test__microseconds_from_datetime(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud._helpers import _microseconds_from_datetime
        return _microseconds_from_datetime(value)

    def test_it(self):
        import datetime

        microseconds = 314159
        timestamp = datetime.datetime(1970, 1, 1, hour=0,
                                      minute=0, second=0,
                                      microsecond=microseconds)
        result = self._call_fut(timestamp)
        self.assertEqual(result, microseconds)


class Test__millis_from_datetime(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud._helpers import _millis_from_datetime
        return _millis_from_datetime(value)

    def test_w_none(self):
        self.assertIsNone(self._call_fut(None))

    def test_w_utc_datetime(self):
        import datetime
        import six
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _microseconds_from_datetime

        NOW = datetime.datetime.utcnow().replace(tzinfo=UTC)
        NOW_MICROS = _microseconds_from_datetime(NOW)
        MILLIS = NOW_MICROS // 1000
        result = self._call_fut(NOW)
        self.assertIsInstance(result, six.integer_types)
        self.assertEqual(result, MILLIS)

    def test_w_non_utc_datetime(self):
        import datetime
        import six
        from google.cloud._helpers import _UTC
        from google.cloud._helpers import _microseconds_from_datetime

        class CET(_UTC):
            _tzname = 'CET'
            _utcoffset = datetime.timedelta(hours=-1)

        zone = CET()
        NOW = datetime.datetime(2015, 7, 28, 16, 34, 47, tzinfo=zone)
        NOW_MICROS = _microseconds_from_datetime(NOW)
        MILLIS = NOW_MICROS // 1000
        result = self._call_fut(NOW)
        self.assertIsInstance(result, six.integer_types)
        self.assertEqual(result, MILLIS)

    def test_w_naive_datetime(self):
        import datetime
        import six
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _microseconds_from_datetime

        NOW = datetime.datetime.utcnow()
        UTC_NOW = NOW.replace(tzinfo=UTC)
        UTC_NOW_MICROS = _microseconds_from_datetime(UTC_NOW)
        MILLIS = UTC_NOW_MICROS // 1000
        result = self._call_fut(NOW)
        self.assertIsInstance(result, six.integer_types)
        self.assertEqual(result, MILLIS)


class Test__datetime_from_microseconds(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud._helpers import _datetime_from_microseconds
        return _datetime_from_microseconds(value)

    def test_it(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _microseconds_from_datetime

        NOW = datetime.datetime(2015, 7, 29, 17, 45, 21, 123456,
                                tzinfo=UTC)
        NOW_MICROS = _microseconds_from_datetime(NOW)
        self.assertEqual(self._call_fut(NOW_MICROS), NOW)


class Test___date_from_iso8601_date(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud._helpers import _date_from_iso8601_date
        return _date_from_iso8601_date(value)

    def test_todays_date(self):
        import datetime
        TODAY = datetime.date.today()
        self.assertEqual(self._call_fut(TODAY.strftime("%Y-%m-%d")), TODAY)


class Test__rfc3339_to_datetime(unittest.TestCase):

    def _call_fut(self, dt_str):
        from google.cloud._helpers import _rfc3339_to_datetime
        return _rfc3339_to_datetime(dt_str)

    def test_w_bogus_zone(self):
        year = 2009
        month = 12
        day = 17
        hour = 12
        minute = 44
        seconds = 32
        micros = 123456789

        dt_str = '%d-%02d-%02dT%02d:%02d:%02d.%06dBOGUS' % (
            year, month, day, hour, minute, seconds, micros)
        with self.assertRaises(ValueError):
            self._call_fut(dt_str)

    def test_w_microseconds(self):
        import datetime
        from google.cloud._helpers import UTC

        year = 2009
        month = 12
        day = 17
        hour = 12
        minute = 44
        seconds = 32
        micros = 123456

        dt_str = '%d-%02d-%02dT%02d:%02d:%02d.%06dZ' % (
            year, month, day, hour, minute, seconds, micros)
        result = self._call_fut(dt_str)
        expected_result = datetime.datetime(
            year, month, day, hour, minute, seconds, micros, UTC)
        self.assertEqual(result, expected_result)

    def test_w_naonseconds(self):
        year = 2009
        month = 12
        day = 17
        hour = 12
        minute = 44
        seconds = 32
        nanos = 123456789

        dt_str = '%d-%02d-%02dT%02d:%02d:%02d.%09dZ' % (
            year, month, day, hour, minute, seconds, nanos)
        with self.assertRaises(ValueError):
            self._call_fut(dt_str)


class Test__rfc3339_nanos_to_datetime(unittest.TestCase):

    def _call_fut(self, dt_str):
        from google.cloud._helpers import _rfc3339_nanos_to_datetime
        return _rfc3339_nanos_to_datetime(dt_str)

    def test_w_bogus_zone(self):
        year = 2009
        month = 12
        day = 17
        hour = 12
        minute = 44
        seconds = 32
        micros = 123456789

        dt_str = '%d-%02d-%02dT%02d:%02d:%02d.%06dBOGUS' % (
            year, month, day, hour, minute, seconds, micros)
        with self.assertRaises(ValueError):
            self._call_fut(dt_str)

    def test_w_truncated_nanos(self):
        import datetime
        from google.cloud._helpers import UTC

        year = 2009
        month = 12
        day = 17
        hour = 12
        minute = 44
        seconds = 32
        truncateds_and_micros = [
            ('12345678', 123456),
            ('1234567', 123456),
            ('123456', 123456),
            ('12345', 123450),
            ('1234', 123400),
            ('123', 123000),
            ('12', 120000),
            ('1', 100000),
        ]

        for truncated, micros in truncateds_and_micros:
            dt_str = '%d-%02d-%02dT%02d:%02d:%02d.%sZ' % (
                year, month, day, hour, minute, seconds, truncated)
            result = self._call_fut(dt_str)
            expected_result = datetime.datetime(
                year, month, day, hour, minute, seconds, micros, UTC)
            self.assertEqual(result, expected_result)

    def test_without_nanos(self):
        import datetime
        from google.cloud._helpers import UTC

        year = 1988
        month = 4
        day = 29
        hour = 12
        minute = 12
        seconds = 12

        dt_str = '%d-%02d-%02dT%02d:%02d:%02dZ' % (
            year, month, day, hour, minute, seconds)
        result = self._call_fut(dt_str)
        expected_result = datetime.datetime(
            year, month, day, hour, minute, seconds, 0, UTC)
        self.assertEqual(result, expected_result)

    def test_w_naonseconds(self):
        import datetime
        from google.cloud._helpers import UTC

        year = 2009
        month = 12
        day = 17
        hour = 12
        minute = 44
        seconds = 32
        nanos = 123456789
        micros = nanos // 1000

        dt_str = '%d-%02d-%02dT%02d:%02d:%02d.%09dZ' % (
            year, month, day, hour, minute, seconds, nanos)
        result = self._call_fut(dt_str)
        expected_result = datetime.datetime(
            year, month, day, hour, minute, seconds, micros, UTC)
        self.assertEqual(result, expected_result)


class Test__datetime_to_rfc3339(unittest.TestCase):

    def _call_fut(self, *args, **kwargs):
        from google.cloud._helpers import _datetime_to_rfc3339
        return _datetime_to_rfc3339(*args, **kwargs)

    @staticmethod
    def _make_timezone(offset):
        from google.cloud._helpers import _UTC

        class CET(_UTC):
            _tzname = 'CET'
            _utcoffset = offset

        return CET()

    def test_w_utc_datetime(self):
        import datetime
        from google.cloud._helpers import UTC

        TIMESTAMP = datetime.datetime(2016, 4, 5, 13, 30, 0, tzinfo=UTC)
        result = self._call_fut(TIMESTAMP, ignore_zone=False)
        self.assertEqual(result, '2016-04-05T13:30:00.000000Z')

    def test_w_non_utc_datetime(self):
        import datetime

        zone = self._make_timezone(offset=datetime.timedelta(hours=-1))
        TIMESTAMP = datetime.datetime(2016, 4, 5, 13, 30, 0, tzinfo=zone)
        result = self._call_fut(TIMESTAMP, ignore_zone=False)
        self.assertEqual(result, '2016-04-05T14:30:00.000000Z')

    def test_w_non_utc_datetime_and_ignore_zone(self):
        import datetime

        zone = self._make_timezone(offset=datetime.timedelta(hours=-1))
        TIMESTAMP = datetime.datetime(2016, 4, 5, 13, 30, 0, tzinfo=zone)
        result = self._call_fut(TIMESTAMP)
        self.assertEqual(result, '2016-04-05T13:30:00.000000Z')

    def test_w_naive_datetime(self):
        import datetime

        TIMESTAMP = datetime.datetime(2016, 4, 5, 13, 30, 0)
        result = self._call_fut(TIMESTAMP)
        self.assertEqual(result, '2016-04-05T13:30:00.000000Z')


class Test__to_bytes(unittest.TestCase):

    def _call_fut(self, *args, **kwargs):
        from google.cloud._helpers import _to_bytes
        return _to_bytes(*args, **kwargs)

    def test_with_bytes(self):
        value = b'bytes-val'
        self.assertEqual(self._call_fut(value), value)

    def test_with_unicode(self):
        value = u'string-val'
        encoded_value = b'string-val'
        self.assertEqual(self._call_fut(value), encoded_value)

    def test_unicode_non_ascii(self):
        value = u'\u2013'  # Long hyphen
        encoded_value = b'\xe2\x80\x93'
        self.assertRaises(UnicodeEncodeError, self._call_fut, value)
        self.assertEqual(self._call_fut(value, encoding='utf-8'),
                         encoded_value)

    def test_with_nonstring_type(self):
        value = object()
        self.assertRaises(TypeError, self._call_fut, value)


class Test__bytes_to_unicode(unittest.TestCase):

    def _call_fut(self, *args, **kwargs):
        from google.cloud._helpers import _bytes_to_unicode
        return _bytes_to_unicode(*args, **kwargs)

    def test_with_bytes(self):
        value = b'bytes-val'
        encoded_value = 'bytes-val'
        self.assertEqual(self._call_fut(value), encoded_value)

    def test_with_unicode(self):
        value = u'string-val'
        encoded_value = 'string-val'
        self.assertEqual(self._call_fut(value), encoded_value)

    def test_with_nonstring_type(self):
        value = object()
        self.assertRaises(ValueError, self._call_fut, value)


class Test__pb_timestamp_to_datetime(unittest.TestCase):

    def _call_fut(self, timestamp):
        from google.cloud._helpers import _pb_timestamp_to_datetime
        return _pb_timestamp_to_datetime(timestamp)

    def test_it(self):
        import datetime
        from google.protobuf.timestamp_pb2 import Timestamp
        from google.cloud._helpers import UTC

        # Epoch is midnight on January 1, 1970 ...
        dt_stamp = datetime.datetime(1970, month=1, day=1, hour=0,
                                     minute=1, second=1, microsecond=1234,
                                     tzinfo=UTC)
        # ... so 1 minute and 1 second after is 61 seconds and 1234
        # microseconds is 1234000 nanoseconds.
        timestamp = Timestamp(seconds=61, nanos=1234000)
        self.assertEqual(self._call_fut(timestamp), dt_stamp)


class Test__pb_timestamp_to_rfc3339(unittest.TestCase):

    def _call_fut(self, timestamp):
        from google.cloud._helpers import _pb_timestamp_to_rfc3339
        return _pb_timestamp_to_rfc3339(timestamp)

    def test_it(self):
        from google.protobuf.timestamp_pb2 import Timestamp

        # Epoch is midnight on January 1, 1970 ...
        # ... so 1 minute and 1 second after is 61 seconds and 1234
        # microseconds is 1234000 nanoseconds.
        timestamp = Timestamp(seconds=61, nanos=1234000)
        self.assertEqual(self._call_fut(timestamp),
                         '1970-01-01T00:01:01.001234Z')


class Test__datetime_to_pb_timestamp(unittest.TestCase):

    def _call_fut(self, when):
        from google.cloud._helpers import _datetime_to_pb_timestamp
        return _datetime_to_pb_timestamp(when)

    def test_it(self):
        import datetime
        from google.protobuf.timestamp_pb2 import Timestamp
        from google.cloud._helpers import UTC

        # Epoch is midnight on January 1, 1970 ...
        dt_stamp = datetime.datetime(1970, month=1, day=1, hour=0,
                                     minute=1, second=1, microsecond=1234,
                                     tzinfo=UTC)
        # ... so 1 minute and 1 second after is 61 seconds and 1234
        # microseconds is 1234000 nanoseconds.
        timestamp = Timestamp(seconds=61, nanos=1234000)
        self.assertEqual(self._call_fut(dt_stamp), timestamp)


class Test__name_from_project_path(unittest.TestCase):

    PROJECT = 'PROJECT'
    THING_NAME = 'THING_NAME'
    TEMPLATE = r'projects/(?P<project>\w+)/things/(?P<name>\w+)'

    def _call_fut(self, path, project, template):
        from google.cloud._helpers import _name_from_project_path
        return _name_from_project_path(path, project, template)

    def test_w_invalid_path_length(self):
        PATH = 'projects/foo'
        with self.assertRaises(ValueError):
            self._call_fut(PATH, None, self.TEMPLATE)

    def test_w_invalid_path_segments(self):
        PATH = 'foo/%s/bar/%s' % (self.PROJECT, self.THING_NAME)
        with self.assertRaises(ValueError):
            self._call_fut(PATH, self.PROJECT, self.TEMPLATE)

    def test_w_mismatched_project(self):
        PROJECT1 = 'PROJECT1'
        PROJECT2 = 'PROJECT2'
        PATH = 'projects/%s/things/%s' % (PROJECT1, self.THING_NAME)
        with self.assertRaises(ValueError):
            self._call_fut(PATH, PROJECT2, self.TEMPLATE)

    def test_w_valid_data_w_compiled_regex(self):
        import re
        template = re.compile(self.TEMPLATE)
        PATH = 'projects/%s/things/%s' % (self.PROJECT, self.THING_NAME)
        name = self._call_fut(PATH, self.PROJECT, template)
        self.assertEqual(name, self.THING_NAME)

    def test_w_project_passed_as_none(self):
        PROJECT1 = 'PROJECT1'
        PATH = 'projects/%s/things/%s' % (PROJECT1, self.THING_NAME)
        self._call_fut(PATH, None, self.TEMPLATE)
        name = self._call_fut(PATH, None, self.TEMPLATE)
        self.assertEqual(name, self.THING_NAME)


class TestMetadataPlugin(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud._helpers import MetadataPlugin
        return MetadataPlugin

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        credentials = object()
        plugin = self._make_one(credentials)
        self.assertIs(plugin._credentials, credentials)

    def test___call__(self):
        access_token_expected = 'FOOBARBAZ'
        credentials = _Credentials(access_token=access_token_expected)
        callback_args = []

        def callback(*args):
            callback_args.append(args)

        transformer = self._make_one(credentials)
        result = transformer(None, callback)
        cb_headers = [
            ('authorization', 'Bearer ' + access_token_expected),
        ]
        self.assertIsNone(result)
        self.assertEqual(callback_args, [(cb_headers, None)])
        self.assertEqual(len(credentials._tokens), 1)


class Test_make_secure_channel(unittest.TestCase):

    def _call_fut(self, *args, **kwargs):
        from google.cloud._helpers import make_secure_channel
        return make_secure_channel(*args, **kwargs)

    def test_it(self):
        from six.moves import http_client
        from google.cloud._testing import _Monkey
        from google.cloud import _helpers as MUT

        SSL_CREDS = object()
        METADATA_CREDS = object()
        COMPOSITE_CREDS = object()
        CHANNEL = object()

        class _GRPCModule(object):

            def __init__(self):
                self.ssl_channel_credentials_args = None
                self.metadata_call_credentials_args = None
                self.composite_channel_credentials_args = None
                self.secure_channel_args = None

            def ssl_channel_credentials(self, *args):
                self.ssl_channel_credentials_args = args
                return SSL_CREDS

            def metadata_call_credentials(self, *args, **kwargs):
                self.metadata_call_credentials_args = (args, kwargs)
                return METADATA_CREDS

            def composite_channel_credentials(self, *args):
                self.composite_channel_credentials_args = args
                return COMPOSITE_CREDS

            def secure_channel(self, *args, **kwargs):
                self.secure_channel_args = (args, kwargs)
                return CHANNEL

        grpc_mod = _GRPCModule()
        metadata_plugin = object()
        plugin_args = []

        def mock_plugin(*args):
            plugin_args.append(args)
            return metadata_plugin

        host = 'HOST'
        credentials = object()
        user_agent = 'USER_AGENT'
        with _Monkey(MUT, grpc=grpc_mod,
                     MetadataPlugin=mock_plugin):
            result = self._call_fut(credentials, user_agent, host)

        self.assertIs(result, CHANNEL)
        self.assertEqual(plugin_args, [(credentials,)])
        self.assertEqual(grpc_mod.ssl_channel_credentials_args, ())
        self.assertEqual(grpc_mod.metadata_call_credentials_args,
                         ((metadata_plugin,), {'name': 'google_creds'}))
        self.assertEqual(
            grpc_mod.composite_channel_credentials_args,
            (SSL_CREDS, METADATA_CREDS))
        target = '%s:%d' % (host, http_client.HTTPS_PORT)
        secure_args = (target, COMPOSITE_CREDS)
        secure_kwargs = {
            'options': (('grpc.primary_user_agent', user_agent),)
        }
        self.assertEqual(grpc_mod.secure_channel_args,
                         (secure_args, secure_kwargs))


class Test_make_secure_stub(unittest.TestCase):

    def _call_fut(self, *args, **kwargs):
        from google.cloud._helpers import make_secure_stub
        return make_secure_stub(*args, **kwargs)

    def test_it(self):
        from google.cloud._testing import _Monkey
        from google.cloud import _helpers as MUT

        result = object()
        channel_obj = object()
        channels = []
        channel_args = []

        def stub_class(channel):
            channels.append(channel)
            return result

        def mock_channel(*args):
            channel_args.append(args)
            return channel_obj

        credentials = object()
        user_agent = 'you-sir-age-int'
        host = 'localhost'
        with _Monkey(MUT, make_secure_channel=mock_channel):
            stub = self._call_fut(credentials, user_agent,
                                  stub_class, host)

        self.assertIs(stub, result)
        self.assertEqual(channels, [channel_obj])
        self.assertEqual(channel_args,
                         [(credentials, user_agent, host)])


class Test_make_insecure_stub(unittest.TestCase):

    def _call_fut(self, *args, **kwargs):
        from google.cloud._helpers import make_insecure_stub
        return make_insecure_stub(*args, **kwargs)

    def _helper(self, target, host, port=None):
        from google.cloud._testing import _Monkey
        from google.cloud import _helpers as MUT

        mock_result = object()
        stub_inputs = []
        CHANNEL = object()

        class _GRPCModule(object):

            def insecure_channel(self, *args):
                self.insecure_channel_args = args
                return CHANNEL

        grpc_mod = _GRPCModule()

        def mock_stub_class(channel):
            stub_inputs.append(channel)
            return mock_result

        with _Monkey(MUT, grpc=grpc_mod):
            result = self._call_fut(mock_stub_class, host, port=port)

        self.assertIs(result, mock_result)
        self.assertEqual(stub_inputs, [CHANNEL])
        self.assertEqual(grpc_mod.insecure_channel_args, (target,))

    def test_with_port_argument(self):
        host = 'HOST'
        port = 1025
        target = '%s:%d' % (host, port)
        self._helper(target, host, port=port)

    def test_without_port_argument(self):
        host = 'HOST:1114'
        self._helper(host, host)


class _AppIdentity(object):

    def __init__(self, app_id):
        self.app_id = app_id

    def get_application_id(self):
        return self.app_id


class _HTTPResponse(object):

    def __init__(self, status, data):
        self.status = status
        self.data = data

    def read(self):
        return self.data


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

    def __init__(self, status, project):
        super(_HTTPConnection, self).__init__()
        self.status = status
        self.project = project

    def getresponse(self):
        return _HTTPResponse(self.status, self.project)


class _TimeoutHTTPConnection(_BaseHTTPConnection):

    def getresponse(self):
        import socket
        raise socket.timeout('timed out')


class _Credentials(object):

    def __init__(self, access_token=None):
        self._access_token = access_token
        self._tokens = []

    def get_access_token(self):
        from oauth2client.client import AccessTokenInfo
        token = AccessTokenInfo(access_token=self._access_token,
                                expires_in=None)
        self._tokens.append(token)
        return token
