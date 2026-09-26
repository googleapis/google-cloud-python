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


from google.protobuf import descriptor_pb2
from google.protobuf import descriptor_pool

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
    from google.longrunning import operations_pb2
    from google.longrunning import operations_proto_pb2

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

    # Construct a synthetic downstream FileDescriptorProto depending on operations.proto
    downstream_file = descriptor_pb2.FileDescriptorProto()
    downstream_file.name = "google/test/downstream_operations_test.proto"
    downstream_file.package = "google.test"
    downstream_file.dependency.append("google/longrunning/operations.proto")

    # Add to pool: raises TypeError if 'google/longrunning/operations.proto' is missing
    file_descriptor = pool.Add(downstream_file)
    assert file_descriptor is not None
    assert "google/longrunning/operations.proto" in [
        dep.name for dep in file_descriptor.dependencies
    ]
