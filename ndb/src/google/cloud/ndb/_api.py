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

"""Functions that interact with Datastore backend."""

import grpc

from google.cloud import _helpers
from google.cloud import _http
from google.cloud.datastore_v1.proto import datastore_pb2_grpc

from google.cloud.ndb import _runstate


def stub():
    """Get the stub for the `Google Datastore` API.

    Gets the stub from the current context, creating one if there isn't one
    already.

    Returns:
        :class:`~google.cloud.datastore_v1.proto.datastore_pb2_grpc.DatastoreStub`:
            The stub instance.
    """
    state = _runstate.current()

    if state.stub is None:
        client = state.client
        if client.secure:
            channel = _helpers.make_secure_channel(
                client._credentials, _http.DEFAULT_USER_AGENT, client.host
            )
        else:
            channel = grpc.insecure_channel(client.host)

        state.stub = datastore_pb2_grpc.DatastoreStub(channel)

    return state.stub
