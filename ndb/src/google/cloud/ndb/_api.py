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
from google.cloud.datastore_v1.proto import datastore_pb2
from google.cloud.datastore_v1.proto import datastore_pb2_grpc

from google.cloud.ndb import _runstate

USER_AGENT = "gcloud-python/ndb"


def stub():
    """Get a stub for the `Google Datastore` API.

    Returns:
        :class:`~google.cloud.datastore_v1.proto.datastore_pb2_grpc.DatastoreStub`:
            The stub instance.
    """
    state = _runstate.current()
    if state.stub is None:
        if state.secure:
            channel = _helpers.make_secure_channel(
                state.credentials, USER_AGENT, state.host
            )
        else:
            channel = grpc.insecure_channel(state.host)
        state.stub = datastore_pb2_grpc.DatastoreStub(channel)
    return state.stub


def lookup(key):
    """Lookup one NDB entity by key."""
    state = _runstate.current()
    request = datastore_pb2.LookupRequest(project_id=state.project)
    key_pb = request.keys.add()
    key_pb.CopyFrom(key._key.to_protobuf())

    api = stub()
    return api.Lookup.future(request)
