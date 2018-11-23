# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import imp
from unittest import mock

from google.protobuf import descriptor_pool
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import symbol_database

import proto
from proto.marshal import types
from proto.message import _FileInfo


def pytest_runtest_setup(item):
    _FileInfo.registry.clear()

    # Replace the descriptor pool and symbol database to avoid tests
    # polluting one another.
    pool = descriptor_pool.DescriptorPool()
    sym_db = symbol_database.SymbolDatabase(pool=pool)
    item._mocks = (
        mock.patch.object(descriptor_pool, 'Default', return_value=pool),
        mock.patch.object(symbol_database, 'Default', return_value=sym_db),
    )
    [i.start() for i in item._mocks]

    # Importing a pb2 module registers those messages with the pool.
    # However, our test harness is subbing out the default pool above,
    # which means that all the dependencies that messages may depend on
    # are now absent from the pool.
    #
    # Add any pb2 modules that may have been imported by the test's module to
    # the descriptor pool and symbol database.
    #
    # This is exceptionally tricky in the C implementation because there is
    # no way to add an existing descriptor to a pool; the only acceptable
    # approach is to add a file descriptor proto, which then creates *new*
    # descriptors. We therefore do that and then plop the replacement classes
    # onto the pb2 modules.
    reloaded = set()
    for name in dir(item.module):
        if name.endswith('_pb2') and not name.startswith('test_'):
            module = getattr(item.module, name)
            pool.AddSerializedFile(module.DESCRIPTOR.serialized_pb)
            fd = pool.FindFileByName(module.DESCRIPTOR.name)
            for message_name, descriptor in fd.message_types_by_name.items():
                new_message = reflection.GeneratedProtocolMessageType(
                    message_name,
                    (message.Message,),
                    {'DESCRIPTOR': descriptor, '__module__': None},
                )
                sym_db.RegisterMessage(new_message)
                setattr(module, message_name, new_message)

            # Track which modules had new message classes loaded.
            # This is used below to wire the new classes into the marshal.
            reloaded.add(name)

    # If the marshal had previously registered the old message classes,
    # then reload the appropriate modules so the marshal is using the new ones.
    if 'wrappers_pb2' in reloaded:
        imp.reload(types.wrappers)
    if reloaded.intersection({'timestamp_pb2', 'duration_pb2'}):
        imp.reload(types.dates)
    proto.marshal.reset()


def pytest_runtest_teardown(item):
    [i.stop() for i in item._mocks]
