# Copyright 2018 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unittest

import mock

from ._testing import _make_credentials


class MultiCallableStub(object):
    """Stub for the grpc.UnaryUnaryMultiCallable interface."""

    def __init__(self, method, channel_stub):
        self.method = method
        self.channel_stub = channel_stub

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        self.channel_stub.requests.append((self.method, request))
        return self.channel_stub.responses.pop()


class ChannelStub(object):
    """Stub for the grpc.Channel interface."""

    def __init__(self, responses=[]):
        self.responses = responses
        self.requests = []

    def unary_unary(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)


class TestAppProfile(unittest.TestCase):

    PROJECT = "project"
    INSTANCE_ID = "instance-id"
    APP_PROFILE_ID = "app-profile-id"
    APP_PROFILE_NAME = "projects/{}/instances/{}/appProfiles/{}".format(
        PROJECT, INSTANCE_ID, APP_PROFILE_ID
    )
    CLUSTER_ID = "cluster-id"
    OP_ID = 8765
    OP_NAME = "operations/projects/{}/instances/{}/appProfiles/{}/operations/{}".format(
        PROJECT, INSTANCE_ID, APP_PROFILE_ID, OP_ID
    )

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.app_profile import AppProfile

        return AppProfile

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @staticmethod
    def _get_target_client_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_client(self, *args, **kwargs):
        return self._get_target_client_class()(*args, **kwargs)

    def test_constructor_defaults(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        app_profile = self._make_one(self.APP_PROFILE_ID, instance)
        self.assertIsInstance(app_profile, self._get_target_class())
        self.assertEqual(app_profile._instance, instance)
        self.assertIsNone(app_profile.routing_policy_type)
        self.assertIsNone(app_profile.description)
        self.assertIsNone(app_profile.cluster_id)
        self.assertIsNone(app_profile.allow_transactional_writes)

    def test_constructor_non_defaults(self):
        from google.cloud.bigtable.enums import RoutingPolicyType

        ANY = RoutingPolicyType.ANY
        DESCRIPTION_1 = "routing policy any"
        APP_PROFILE_ID_2 = "app-profile-id-2"
        SINGLE = RoutingPolicyType.SINGLE
        DESCRIPTION_2 = "routing policy single"
        ALLOW_WRITES = True
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        app_profile1 = self._make_one(
            self.APP_PROFILE_ID,
            instance,
            routing_policy_type=ANY,
            description=DESCRIPTION_1,
        )
        app_profile2 = self._make_one(
            APP_PROFILE_ID_2,
            instance,
            routing_policy_type=SINGLE,
            description=DESCRIPTION_2,
            cluster_id=self.CLUSTER_ID,
            allow_transactional_writes=ALLOW_WRITES,
        )
        self.assertEqual(app_profile1.app_profile_id, self.APP_PROFILE_ID)
        self.assertIs(app_profile1._instance, instance)
        self.assertEqual(app_profile1.routing_policy_type, ANY)
        self.assertEqual(app_profile1.description, DESCRIPTION_1)
        self.assertEqual(app_profile2.app_profile_id, APP_PROFILE_ID_2)
        self.assertIs(app_profile2._instance, instance)
        self.assertEqual(app_profile2.routing_policy_type, SINGLE)
        self.assertEqual(app_profile2.description, DESCRIPTION_2)
        self.assertEqual(app_profile2.cluster_id, self.CLUSTER_ID)
        self.assertEqual(app_profile2.allow_transactional_writes, ALLOW_WRITES)

    def test_name_property(self):
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = _Instance(self.INSTANCE_ID, client)

        app_profile = self._make_one(self.APP_PROFILE_ID, instance)
        self.assertEqual(app_profile.name, self.APP_PROFILE_NAME)

    def test___eq__(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        app_profile1 = self._make_one(self.APP_PROFILE_ID, instance)
        app_profile2 = self._make_one(self.APP_PROFILE_ID, instance)
        self.assertTrue(app_profile1 == app_profile2)

    def test___eq__type_instance_differ(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        alt_instance = _Instance("other-instance", client)
        other_object = _Other(self.APP_PROFILE_ID, instance)
        app_profile1 = self._make_one(self.APP_PROFILE_ID, instance)
        app_profile2 = self._make_one(self.APP_PROFILE_ID, alt_instance)
        self.assertFalse(app_profile1 == other_object)
        self.assertFalse(app_profile1 == app_profile2)

    def test___ne__same_value(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        app_profile1 = self._make_one(self.APP_PROFILE_ID, instance)
        app_profile2 = self._make_one(self.APP_PROFILE_ID, instance)
        self.assertFalse(app_profile1 != app_profile2)

    def test___ne__(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        app_profile1 = self._make_one("app_profile_id1", instance)
        app_profile2 = self._make_one("app_profile_id2", instance)
        self.assertTrue(app_profile1 != app_profile2)

    def test_from_pb_success_routing_any(self):
        from google.cloud.bigtable_admin_v2.types import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable.enums import RoutingPolicyType

        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        desctiption = "routing any"
        routing = RoutingPolicyType.ANY
        multi_cluster_routing_use_any = (
            data_v2_pb2.AppProfile.MultiClusterRoutingUseAny()
        )

        app_profile_pb = data_v2_pb2.AppProfile(
            name=self.APP_PROFILE_NAME,
            description=desctiption,
            multi_cluster_routing_use_any=multi_cluster_routing_use_any,
        )

        klass = self._get_target_class()
        app_profile = klass.from_pb(app_profile_pb, instance)
        self.assertIsInstance(app_profile, klass)
        self.assertIs(app_profile._instance, instance)
        self.assertEqual(app_profile.app_profile_id, self.APP_PROFILE_ID)
        self.assertEqual(app_profile.description, desctiption)
        self.assertEqual(app_profile.routing_policy_type, routing)
        self.assertIsNone(app_profile.cluster_id)
        self.assertEqual(app_profile.allow_transactional_writes, False)

    def test_from_pb_success_routing_single(self):
        from google.cloud.bigtable_admin_v2.types import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable.enums import RoutingPolicyType

        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        desctiption = "routing single"
        allow_transactional_writes = True
        routing = RoutingPolicyType.SINGLE
        single_cluster_routing = data_v2_pb2.AppProfile.SingleClusterRouting(
            cluster_id=self.CLUSTER_ID,
            allow_transactional_writes=allow_transactional_writes,
        )

        app_profile_pb = data_v2_pb2.AppProfile(
            name=self.APP_PROFILE_NAME,
            description=desctiption,
            single_cluster_routing=single_cluster_routing,
        )

        klass = self._get_target_class()
        app_profile = klass.from_pb(app_profile_pb, instance)
        self.assertIsInstance(app_profile, klass)
        self.assertIs(app_profile._instance, instance)
        self.assertEqual(app_profile.app_profile_id, self.APP_PROFILE_ID)
        self.assertEqual(app_profile.description, desctiption)
        self.assertEqual(app_profile.routing_policy_type, routing)
        self.assertEqual(app_profile.cluster_id, self.CLUSTER_ID)
        self.assertEqual(
            app_profile.allow_transactional_writes, allow_transactional_writes
        )

    def test_from_pb_bad_app_profile_name(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2

        bad_app_profile_name = "BAD_NAME"

        app_profile_pb = data_v2_pb2.AppProfile(name=bad_app_profile_name)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(app_profile_pb, None)

    def test_from_pb_instance_id_mistmatch(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2

        ALT_INSTANCE_ID = "ALT_INSTANCE_ID"
        client = _Client(self.PROJECT)
        instance = _Instance(ALT_INSTANCE_ID, client)
        self.assertEqual(instance.instance_id, ALT_INSTANCE_ID)

        app_profile_pb = data_v2_pb2.AppProfile(name=self.APP_PROFILE_NAME)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(app_profile_pb, instance)

    def test_from_pb_project_mistmatch(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2

        ALT_PROJECT = "ALT_PROJECT"
        client = _Client(project=ALT_PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        self.assertEqual(client.project, ALT_PROJECT)

        app_profile_pb = data_v2_pb2.AppProfile(name=self.APP_PROFILE_NAME)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(app_profile_pb, instance)

    def test_reload_routing_any(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable.enums import RoutingPolicyType

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = _Instance(self.INSTANCE_ID, client)

        routing = RoutingPolicyType.ANY
        description = "routing policy any"

        app_profile = self._make_one(
            self.APP_PROFILE_ID,
            instance,
            routing_policy_type=routing,
            description=description,
        )

        # Create response_pb
        description_from_server = "routing policy switched to single"
        cluster_id_from_server = self.CLUSTER_ID
        allow_transactional_writes = True
        single_cluster_routing = data_v2_pb2.AppProfile.SingleClusterRouting(
            cluster_id=cluster_id_from_server,
            allow_transactional_writes=allow_transactional_writes,
        )

        response_pb = data_v2_pb2.AppProfile(
            name=app_profile.name,
            single_cluster_routing=single_cluster_routing,
            description=description_from_server,
        )

        # Patch the stub used by the API method.
        client._instance_admin_client = api
        instance_stub = client._instance_admin_client.transport
        instance_stub.get_app_profile.side_effect = [response_pb]

        # Create expected_result.
        expected_result = None  # reload() has no return value.

        # Check app_profile config values before.
        self.assertEqual(app_profile.routing_policy_type, routing)
        self.assertEqual(app_profile.description, description)
        self.assertIsNone(app_profile.cluster_id)
        self.assertIsNone(app_profile.allow_transactional_writes)

        # Perform the method and check the result.
        result = app_profile.reload()
        self.assertEqual(result, expected_result)
        self.assertEqual(app_profile.routing_policy_type, RoutingPolicyType.SINGLE)
        self.assertEqual(app_profile.description, description_from_server)
        self.assertEqual(app_profile.cluster_id, cluster_id_from_server)
        self.assertEqual(
            app_profile.allow_transactional_writes, allow_transactional_writes
        )

    def test_exists(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.api_core import exceptions

        instance_api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock()
        )
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = client.instance(self.INSTANCE_ID)

        # Create response_pb
        response_pb = data_v2_pb2.AppProfile(name=self.APP_PROFILE_NAME)
        client._instance_admin_client = instance_api

        # Patch the stub used by the API method.
        client._instance_admin_client = instance_api
        instance_stub = client._instance_admin_client.transport
        instance_stub.get_app_profile.side_effect = [
            response_pb,
            exceptions.NotFound("testing"),
            exceptions.BadRequest("testing"),
        ]

        # Perform the method and check the result.
        non_existing_app_profile_id = "other-app-profile-id"
        app_profile = self._make_one(self.APP_PROFILE_ID, instance)
        alt_app_profile = self._make_one(non_existing_app_profile_id, instance)
        self.assertTrue(app_profile.exists())
        self.assertFalse(alt_app_profile.exists())
        with self.assertRaises(exceptions.BadRequest):
            alt_app_profile.exists()

    def test_create_routing_any(self):
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2,
        )
        from google.cloud.bigtable.enums import RoutingPolicyType
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = client.instance(self.INSTANCE_ID)

        routing = RoutingPolicyType.ANY
        description = "routing policy any"
        ignore_warnings = True

        app_profile = self._make_one(
            self.APP_PROFILE_ID,
            instance,
            routing_policy_type=routing,
            description=description,
        )
        expected_request_app_profile = app_profile._to_pb()
        expected_request = messages_v2_pb2.CreateAppProfileRequest(
            parent=instance.name,
            app_profile_id=self.APP_PROFILE_ID,
            app_profile=expected_request_app_profile,
            ignore_warnings=ignore_warnings,
        )

        # Patch the stub used by the API method.
        channel = ChannelStub(responses=[expected_request_app_profile])
        instance_api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            channel=channel
        )
        client._instance_admin_client = instance_api
        # Perform the method and check the result.
        result = app_profile.create(ignore_warnings)
        actual_request = channel.requests[0][1]

        self.assertEqual(actual_request, expected_request)
        self.assertIsInstance(result, self._get_target_class())
        self.assertEqual(result.app_profile_id, self.APP_PROFILE_ID)
        self.assertIs(result._instance, instance)
        self.assertEqual(result.routing_policy_type, routing)
        self.assertEqual(result.description, description)
        self.assertEqual(result.allow_transactional_writes, False)
        self.assertIsNone(result.cluster_id)

    def test_create_routing_single(self):
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2,
        )
        from google.cloud.bigtable.enums import RoutingPolicyType
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = client.instance(self.INSTANCE_ID)

        routing = RoutingPolicyType.SINGLE
        description = "routing policy single"
        allow_writes = False
        ignore_warnings = True

        app_profile = self._make_one(
            self.APP_PROFILE_ID,
            instance,
            routing_policy_type=routing,
            description=description,
            cluster_id=self.CLUSTER_ID,
            allow_transactional_writes=allow_writes,
        )
        expected_request_app_profile = app_profile._to_pb()
        expected_request = messages_v2_pb2.CreateAppProfileRequest(
            parent=instance.name,
            app_profile_id=self.APP_PROFILE_ID,
            app_profile=expected_request_app_profile,
            ignore_warnings=ignore_warnings,
        )

        # Patch the stub used by the API method.
        channel = ChannelStub(responses=[expected_request_app_profile])
        instance_api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            channel=channel
        )
        client._instance_admin_client = instance_api
        # Perform the method and check the result.
        result = app_profile.create(ignore_warnings)
        actual_request = channel.requests[0][1]

        self.assertEqual(actual_request, expected_request)
        self.assertIsInstance(result, self._get_target_class())
        self.assertEqual(result.app_profile_id, self.APP_PROFILE_ID)
        self.assertIs(result._instance, instance)
        self.assertEqual(result.routing_policy_type, routing)
        self.assertEqual(result.description, description)
        self.assertEqual(result.allow_transactional_writes, allow_writes)
        self.assertEqual(result.cluster_id, self.CLUSTER_ID)

    def test_create_app_profile_with_wrong_routing_policy(self):
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = client.instance(self.INSTANCE_ID)
        app_profile = self._make_one(
            self.APP_PROFILE_ID, instance, routing_policy_type=None
        )
        with self.assertRaises(ValueError):
            app_profile.create()

    def test_update_app_profile_routing_any(self):
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2,
        )
        from google.cloud.bigtable.enums import RoutingPolicyType
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.protobuf import field_mask_pb2

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = client.instance(self.INSTANCE_ID)

        routing = RoutingPolicyType.SINGLE
        description = "to routing policy single"
        allow_writes = True
        app_profile = self._make_one(
            self.APP_PROFILE_ID,
            instance,
            routing_policy_type=routing,
            description=description,
            cluster_id=self.CLUSTER_ID,
            allow_transactional_writes=allow_writes,
        )

        # Create response_pb
        metadata = messages_v2_pb2.UpdateAppProfileMetadata()
        type_url = "type.googleapis.com/{}".format(
            messages_v2_pb2.UpdateAppProfileMetadata.DESCRIPTOR.full_name
        )
        response_pb = operations_pb2.Operation(
            name=self.OP_NAME,
            metadata=Any(type_url=type_url, value=metadata.SerializeToString()),
        )

        # Patch the stub used by the API method.
        channel = ChannelStub(responses=[response_pb])
        instance_api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            channel=channel
        )
        # Mock api calls
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        ignore_warnings = True
        expected_request_update_mask = field_mask_pb2.FieldMask(
            paths=["description", "single_cluster_routing"]
        )
        expected_request = messages_v2_pb2.UpdateAppProfileRequest(
            app_profile=app_profile._to_pb(),
            update_mask=expected_request_update_mask,
            ignore_warnings=ignore_warnings,
        )

        result = app_profile.update(ignore_warnings=ignore_warnings)
        actual_request = channel.requests[0][1]

        self.assertEqual(actual_request, expected_request)
        self.assertIsInstance(result, operation.Operation)
        self.assertEqual(result.operation.name, self.OP_NAME)
        self.assertIsInstance(result.metadata, messages_v2_pb2.UpdateAppProfileMetadata)

    def test_update_app_profile_routing_single(self):
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2,
        )
        from google.cloud.bigtable.enums import RoutingPolicyType
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.protobuf import field_mask_pb2

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = client.instance(self.INSTANCE_ID)

        routing = RoutingPolicyType.ANY
        app_profile = self._make_one(
            self.APP_PROFILE_ID, instance, routing_policy_type=routing
        )

        # Create response_pb
        metadata = messages_v2_pb2.UpdateAppProfileMetadata()
        type_url = "type.googleapis.com/{}".format(
            messages_v2_pb2.UpdateAppProfileMetadata.DESCRIPTOR.full_name
        )
        response_pb = operations_pb2.Operation(
            name=self.OP_NAME,
            metadata=Any(type_url=type_url, value=metadata.SerializeToString()),
        )

        # Patch the stub used by the API method.
        channel = ChannelStub(responses=[response_pb])
        instance_api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            channel=channel
        )
        # Mock api calls
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        ignore_warnings = True
        expected_request_update_mask = field_mask_pb2.FieldMask(
            paths=["multi_cluster_routing_use_any"]
        )
        expected_request = messages_v2_pb2.UpdateAppProfileRequest(
            app_profile=app_profile._to_pb(),
            update_mask=expected_request_update_mask,
            ignore_warnings=ignore_warnings,
        )

        result = app_profile.update(ignore_warnings=ignore_warnings)
        actual_request = channel.requests[0][1]

        self.assertEqual(actual_request, expected_request)
        self.assertIsInstance(result, operation.Operation)
        self.assertEqual(result.operation.name, self.OP_NAME)
        self.assertIsInstance(result.metadata, messages_v2_pb2.UpdateAppProfileMetadata)

    def test_update_app_profile_with_wrong_routing_policy(self):
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = client.instance(self.INSTANCE_ID)
        app_profile = self._make_one(
            self.APP_PROFILE_ID, instance, routing_policy_type=None
        )
        with self.assertRaises(ValueError):
            app_profile.update()

    def test_delete(self):
        from google.protobuf import empty_pb2
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client

        instance_api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock()
        )

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = client.instance(self.INSTANCE_ID)
        app_profile = self._make_one(self.APP_PROFILE_ID, instance)

        # Create response_pb
        response_pb = empty_pb2.Empty()

        # Patch the stub used by the API method.
        client._instance_admin_client = instance_api
        instance_stub = client._instance_admin_client.transport
        instance_stub.delete_cluster.side_effect = [response_pb]

        # Create expected_result.
        expected_result = None  # delete() has no return value.

        # Perform the method and check the result.
        result = app_profile.delete()

        self.assertEqual(result, expected_result)


class _Client(object):
    def __init__(self, project):
        self.project = project
        self.project_name = "projects/" + self.project
        self._operations_stub = mock.sentinel.operations_stub

    def __eq__(self, other):
        return other.project == self.project and other.project_name == self.project_name


class _Instance(object):
    def __init__(self, instance_id, client):
        self.instance_id = instance_id
        self._client = client

    def __eq__(self, other):
        return other.instance_id == self.instance_id and other._client == self._client


class _Other(object):
    def __init__(self, app_profile_id, instance):
        self.app_profile_id = app_profile_id
        self._instance = instance
