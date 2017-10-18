# Copyright 2017 Google Inc.
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

import mock

from google.api_core import operations_v1
from google.api_core import page_iterator
from google.longrunning import operations_pb2


def make_operations_stub(channel):
    return mock.Mock(
        spec=[
            'GetOperation', 'DeleteOperation', 'ListOperations',
            'CancelOperation'])


operations_stub_patch = mock.patch(
    'google.longrunning.operations_pb2.OperationsStub',
    autospec=True,
    side_effect=make_operations_stub)


@operations_stub_patch
def test_constructor(operations_stub):
    stub = make_operations_stub(None)
    operations_stub.side_effect = None
    operations_stub.return_value = stub

    client = operations_v1.OperationsClient(mock.sentinel.channel)

    assert client.operations_stub == stub
    operations_stub.assert_called_once_with(mock.sentinel.channel)


@operations_stub_patch
def test_get_operation(operations_stub):
    client = operations_v1.OperationsClient(mock.sentinel.channel)
    client.operations_stub.GetOperation.return_value = mock.sentinel.operation

    response = client.get_operation('name')

    request = client.operations_stub.GetOperation.call_args[0][0]
    assert isinstance(request, operations_pb2.GetOperationRequest)
    assert request.name == 'name'

    assert response == mock.sentinel.operation


@operations_stub_patch
def test_list_operations(operations_stub):
    client = operations_v1.OperationsClient(mock.sentinel.channel)
    operations = [
        operations_pb2.Operation(name='1'),
        operations_pb2.Operation(name='2')]
    list_response = operations_pb2.ListOperationsResponse(
        operations=operations)
    client.operations_stub.ListOperations.return_value = list_response

    response = client.list_operations('name', 'filter')

    assert isinstance(response, page_iterator.Iterator)
    assert list(response) == operations

    request = client.operations_stub.ListOperations.call_args[0][0]
    assert isinstance(request, operations_pb2.ListOperationsRequest)
    assert request.name == 'name'
    assert request.filter == 'filter'


@operations_stub_patch
def test_delete_operation(operations_stub):
    client = operations_v1.OperationsClient(mock.sentinel.channel)

    client.delete_operation('name')

    request = client.operations_stub.DeleteOperation.call_args[0][0]
    assert isinstance(request, operations_pb2.DeleteOperationRequest)
    assert request.name == 'name'


@operations_stub_patch
def test_cancel_operation(operations_stub):
    client = operations_v1.OperationsClient(mock.sentinel.channel)

    client.cancel_operation('name')

    request = client.operations_stub.CancelOperation.call_args[0][0]
    assert isinstance(request, operations_pb2.CancelOperationRequest)
    assert request.name == 'name'
