# Copyright 2026 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
from unittest import mock

from google.protobuf import descriptor_pb2, descriptor_pool


def test_operations_descriptor_name():
    """Validates the canonical proto name registered in the descriptor pool."""
    from google.longrunning import operations_pb2

    # The descriptor name MUST be the canonical path 'google/longrunning/operations.proto'.
    # If named 'google/longrunning/operations_proto.proto', any downstream proto that
    # imports 'google/longrunning/operations.proto' will fail to resolve.
    assert operations_pb2.DESCRIPTOR.name == "google/longrunning/operations.proto"

    # Verify lookup by canonical path succeeds in the global descriptor pool
    pool = descriptor_pool.Default()
    file_desc = pool.FindFileByName("google/longrunning/operations.proto")
    assert file_desc is not None
    assert file_desc.name == "google/longrunning/operations.proto"


def test_operations_message_instantiation():
    """Validates message instantiation from both public module entry points."""
    from google.longrunning import operations_pb2, operations_proto_pb2

    op1 = operations_pb2.Operation(name="operations/123", done=True)
    assert op1.name == "operations/123"
    assert op1.done is True

    op2 = operations_proto_pb2.Operation(name="operations/456", done=False)
    assert op2.name == "operations/456"
    assert op2.done is False


def test_downstream_dependency_resolution():
    """Regression test for b/566222096.

    Downstream clients compile protos containing:
        import "google/longrunning/operations.proto";

    When their generated *_pb2 modules load, protobuf calls:

    ```
        _descriptor_pool.Default().AddSerializedFile(...)
    ```

    which checks that 'google/longrunning/operations.proto' exists in the pool.
    """
    # Ensure operations_pb2 is imported and registered
    from google.longrunning import operations_pb2  # noqa: F401

    pool = descriptor_pool.Default()

    # Create a uniquely named proto to avoid collision during repeated test runs
    unique_name = f"google/test/downstream_{uuid.uuid4().hex}.proto"

    downstream_file = descriptor_pb2.FileDescriptorProto()
    downstream_file.name = unique_name
    downstream_file.package = "google.test"
    downstream_file.dependency.append("google/longrunning/operations.proto")

    # 1. This step will throw the TypeError if operations.proto is missing (under C++ runtime).
    file_descriptor = pool.Add(downstream_file)

    # 2. Retrieve the descriptor from the pool (required because pool.Add() returns None).
    file_descriptor = pool.FindFileByName(unique_name)
    assert file_descriptor is not None
    assert file_descriptor.name == unique_name
    assert "google/longrunning/operations.proto" in [
        dep.name for dep in file_descriptor.dependencies
    ]


def test_grpc_stubs_coverage():
    """Exercises gRPC stubs to achieve 100% coverage."""
    from google.longrunning import operations_pb2_grpc

    servicer = operations_pb2_grpc.OperationsServicer()
    for method in [
        servicer.ListOperations,
        servicer.GetOperation,
        servicer.DeleteOperation,
        servicer.CancelOperation,
        servicer.WaitOperation,
    ]:
        try:
            method(mock.Mock(), mock.Mock())
        except NotImplementedError:
            pass

    mock_server = mock.Mock()
    operations_pb2_grpc.add_OperationsServicer_to_server(servicer, mock_server)
    assert mock_server.add_generic_rpc_handlers.called

    mock_channel = mock.Mock()
    dummy_callable = mock.Mock(return_value=mock.Mock())
    mock_channel.unary_unary = mock.Mock(return_value=dummy_callable)
    mock_channel.unary_stream = mock.Mock(return_value=dummy_callable)

    stub = operations_pb2_grpc.OperationsStub(mock_channel)
    stub.ListOperations(mock.Mock())
    stub.GetOperation(mock.Mock())
    stub.DeleteOperation(mock.Mock())
    stub.CancelOperation(mock.Mock())
    stub.WaitOperation(mock.Mock())

    with mock.patch("grpc.experimental.unary_unary", return_value=mock.Mock()):
        operations_pb2_grpc.Operations.ListOperations(mock.Mock(), "target")
        operations_pb2_grpc.Operations.GetOperation(mock.Mock(), "target")
        operations_pb2_grpc.Operations.DeleteOperation(mock.Mock(), "target")
        operations_pb2_grpc.Operations.CancelOperation(mock.Mock(), "target")
        operations_pb2_grpc.Operations.WaitOperation(mock.Mock(), "target")
