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

from unittest import mock

from google.cloud.ndb import _api


class TestStub:
    @staticmethod
    @mock.patch("google.cloud.ndb._api._helpers")
    @mock.patch("google.cloud.ndb._api.datastore_pb2_grpc")
    def test_secure_channel(datastore_pb2_grpc, _helpers):
        channel = _helpers.make_secure_channel.return_value
        client = mock.Mock(
            _credentials="creds",
            secure=True,
            host="thehost",
            spec=("_credentials", "secure", "host"),
        )
        stub = _api.stub(client)
        assert stub is datastore_pb2_grpc.DatastoreStub.return_value
        datastore_pb2_grpc.DatastoreStub.assert_called_once_with(channel)
        _helpers.make_secure_channel.assert_called_once_with(
            "creds", "gcloud-python/ndb", "thehost"
        )

    @staticmethod
    @mock.patch("google.cloud.ndb._api.grpc")
    @mock.patch("google.cloud.ndb._api.datastore_pb2_grpc")
    def test_insecure_channel(datastore_pb2_grpc, grpc):
        channel = grpc.insecure_channel.return_value
        client = mock.Mock(
            secure=False, host="thehost", spec=("secure", "host")
        )
        stub = _api.stub(client)
        assert stub is datastore_pb2_grpc.DatastoreStub.return_value
        datastore_pb2_grpc.DatastoreStub.assert_called_once_with(channel)
        grpc.insecure_channel.assert_called_once_with("thehost")
