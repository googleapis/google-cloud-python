# Copyright 2016 Google Inc. All rights reserved.
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

import unittest


class Test__compute_type_url(unittest.TestCase):

    def _callFUT(self, klass, prefix=None):
        from gcloud.operation import _compute_type_url
        if prefix is None:
            return _compute_type_url(klass)
        return _compute_type_url(klass, prefix)

    def test_wo_prefix(self):
        from google.protobuf.struct_pb2 import Struct
        from gcloud.operation import _GOOGLE_APIS_PREFIX

        type_url = self._callFUT(Struct)

        self.assertEqual(
            type_url,
            '%s/%s' % (_GOOGLE_APIS_PREFIX, Struct.DESCRIPTOR.full_name))

    def test_w_prefix(self):
        from google.protobuf.struct_pb2 import Struct
        PREFIX = 'test.gcloud-python.com'

        type_url = self._callFUT(Struct, PREFIX)

        self.assertEqual(
            type_url,
            '%s/%s' % (PREFIX, Struct.DESCRIPTOR.full_name))


class Test__register_type_url(unittest.TestCase):

    def _callFUT(self, type_url, klass):
        from gcloud.operation import _register_type_url
        _register_type_url(type_url, klass)

    def test_simple(self):
        from gcloud import operation as MUT
        from unit_tests._testing import _Monkey
        TYPE_URI = 'testing.gcloud-python.com/testing'
        klass = object()
        type_url_map = {}

        with _Monkey(MUT, _TYPE_URL_MAP=type_url_map):
            self._callFUT(TYPE_URI, klass)

        self.assertEqual(type_url_map, {TYPE_URI: klass})

    def test_w_same_class(self):
        from gcloud import operation as MUT
        from unit_tests._testing import _Monkey
        TYPE_URI = 'testing.gcloud-python.com/testing'
        klass = object()
        type_url_map = {TYPE_URI: klass}

        with _Monkey(MUT, _TYPE_URL_MAP=type_url_map):
            self._callFUT(TYPE_URI, klass)

        self.assertEqual(type_url_map, {TYPE_URI: klass})

    def test_w_conflict(self):
        from gcloud import operation as MUT
        from unit_tests._testing import _Monkey
        TYPE_URI = 'testing.gcloud-python.com/testing'
        klass, other = object(), object()
        type_url_map = {TYPE_URI: other}

        with _Monkey(MUT, _TYPE_URL_MAP=type_url_map):
            with self.assertRaises(ValueError):
                self._callFUT(TYPE_URI, klass)

        self.assertEqual(type_url_map, {TYPE_URI: other})


class OperationTests(unittest.TestCase):

    OPERATION_NAME = 'operations/projects/foo/instances/bar/operations/123'

    def _getTargetClass(self):
        from gcloud.operation import Operation
        return Operation

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        client = _Client()
        operation = self._makeOne(
            self.OPERATION_NAME, client)
        self.assertEqual(operation.name, self.OPERATION_NAME)
        self.assertTrue(operation.client is client)
        self.assertTrue(operation.target is None)
        self.assertTrue(operation.pb_metadata is None)
        self.assertEqual(operation.metadata, {})

    def test_ctor_explicit(self):
        client = _Client()
        pb_metadata = object()
        operation = self._makeOne(
            self.OPERATION_NAME, client, pb_metadata, foo='bar')
        self.assertEqual(operation.name, self.OPERATION_NAME)
        self.assertTrue(operation.client is client)
        self.assertTrue(operation.target is None)
        self.assertTrue(operation.pb_metadata is pb_metadata)
        self.assertEqual(operation.metadata, {'foo': 'bar'})

    def test_from_pb_wo_metadata_or_kw(self):
        from google.longrunning import operations_pb2
        client = _Client()
        operation_pb = operations_pb2.Operation(name=self.OPERATION_NAME)
        klass = self._getTargetClass()

        operation = klass.from_pb(operation_pb, client)

        self.assertEqual(operation.name, self.OPERATION_NAME)
        self.assertTrue(operation.client is client)
        self.assertTrue(operation.pb_metadata is None)
        self.assertEqual(operation.metadata, {})

    def test_from_pb_w_unknown_metadata(self):
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.protobuf.struct_pb2 import Struct, Value
        TYPE_URI = 'type.googleapis.com/%s' % (Struct.DESCRIPTOR.full_name,)

        client = _Client()
        meta = Struct(fields={'foo': Value(string_value=u'Bar')})
        metadata_pb = Any(type_url=TYPE_URI, value=meta.SerializeToString())
        operation_pb = operations_pb2.Operation(
            name=self.OPERATION_NAME, metadata=metadata_pb)
        klass = self._getTargetClass()

        operation = klass.from_pb(operation_pb, client)

        self.assertEqual(operation.name, self.OPERATION_NAME)
        self.assertTrue(operation.client is client)
        self.assertTrue(operation.pb_metadata is None)
        self.assertEqual(operation.metadata, {})

    def test_from_pb_w_metadata_and_kwargs(self):
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.protobuf.struct_pb2 import Struct, Value
        from gcloud import operation as MUT
        from unit_tests._testing import _Monkey
        TYPE_URI = 'type.googleapis.com/%s' % (Struct.DESCRIPTOR.full_name,)
        type_url_map = {TYPE_URI: Struct}

        client = _Client()
        meta = Struct(fields={'foo': Value(string_value=u'Bar')})
        metadata_pb = Any(type_url=TYPE_URI, value=meta.SerializeToString())
        operation_pb = operations_pb2.Operation(
            name=self.OPERATION_NAME, metadata=metadata_pb)
        klass = self._getTargetClass()

        with _Monkey(MUT, _TYPE_URL_MAP=type_url_map):
            operation = klass.from_pb(operation_pb, client, baz='qux')

        self.assertEqual(operation.name, self.OPERATION_NAME)
        self.assertTrue(operation.client is client)
        pb_metadata = operation.pb_metadata
        self.assertTrue(isinstance(pb_metadata, Struct))
        self.assertEqual(list(pb_metadata.fields), ['foo'])
        self.assertEqual(pb_metadata.fields['foo'].string_value, 'Bar')
        self.assertEqual(operation.metadata, {'baz': 'qux'})

    def test_complete_property(self):
        client = _Client()
        operation = self._makeOne(self.OPERATION_NAME, client)
        self.assertFalse(operation.complete)
        operation._complete = True
        self.assertTrue(operation.complete)
        with self.assertRaises(AttributeError):
            operation.complete = False

    def test_poll_already_complete(self):
        client = _Client()
        operation = self._makeOne(self.OPERATION_NAME, client)
        operation._complete = True

        with self.assertRaises(ValueError):
            operation.poll()

    def test_poll_false(self):
        from google.longrunning.operations_pb2 import GetOperationRequest
        response_pb = _GetOperationResponse(False)
        client = _Client()
        stub = client._operations_stub
        stub._get_operation_response = response_pb
        operation = self._makeOne(self.OPERATION_NAME, client)

        self.assertFalse(operation.poll())

        request_pb = stub._get_operation_requested
        self.assertTrue(isinstance(request_pb, GetOperationRequest))
        self.assertEqual(request_pb.name, self.OPERATION_NAME)

    def test_poll_true(self):
        from google.longrunning.operations_pb2 import GetOperationRequest
        response_pb = _GetOperationResponse(True)
        client = _Client()
        stub = client._operations_stub
        stub._get_operation_response = response_pb
        operation = self._makeOne(self.OPERATION_NAME, client)

        self.assertTrue(operation.poll())

        request_pb = stub._get_operation_requested
        self.assertTrue(isinstance(request_pb, GetOperationRequest))
        self.assertEqual(request_pb.name, self.OPERATION_NAME)


class _GetOperationResponse(object):
    def __init__(self, done):
        self.done = done


class _OperationsStub(object):

    def GetOperation(self, request_pb):
        self._get_operation_requested = request_pb
        return self._get_operation_response


class _Client(object):

    def __init__(self):
        self._operations_stub = _OperationsStub()
