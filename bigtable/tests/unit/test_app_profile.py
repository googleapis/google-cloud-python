# Copyright 2018 Google Inc.
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

    def unary_unary(self,
                    method,
                    request_serializer=None,
                    response_deserializer=None):
        return MultiCallableStub(method, self)


class TestAppProfile(unittest.TestCase):

    PROJECT = 'project'
    INSTANCE_ID = 'instance-id'
    APP_PROFILE_ID = 'app-profile-id'
    APP_PROFILE_NAME = ('projects/{}/instances/{}/appProfiles/{}'
                        .format(PROJECT, INSTANCE_ID, APP_PROFILE_ID))
    CLUSTER_ID = 'cluster-id'

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
        DESCRIPTION_1 = 'routing policy any'
        APP_PROFILE_ID_2 = 'app-profile-id-2'
        SINGLE = RoutingPolicyType.SINGLE
        DESCRIPTION_2 = 'routing policy single'
        ALLOW_WRITES = True
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        app_profile1 = self._make_one(self.APP_PROFILE_ID, instance,
                                      routing_policy_type=ANY,
                                      description=DESCRIPTION_1)
        app_profile2 = self._make_one(APP_PROFILE_ID_2, instance,
                                      routing_policy_type=SINGLE,
                                      description=DESCRIPTION_2,
                                      cluster_id=self.CLUSTER_ID,
                                      allow_transactional_writes=ALLOW_WRITES)
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
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = _Instance(self.INSTANCE_ID, client)

        app_profile = self._make_one(self.APP_PROFILE_ID, instance)
        self.assertEqual(app_profile.name, self.APP_PROFILE_NAME)

    def test___eq__(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        app_profile1 = self._make_one(self.APP_PROFILE_ID, instance)
        app_profile2 = self._make_one(self.APP_PROFILE_ID, instance)
        self.assertEqual(app_profile1, app_profile2)

    def test___eq__type_differ(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        app_profile1 = self._make_one(self.APP_PROFILE_ID, instance)
        app_profile2 = object()
        self.assertNotEqual(app_profile1, app_profile2)

    def test___ne__same_value(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        app_profile1 = self._make_one(self.APP_PROFILE_ID, instance)
        app_profile2 = self._make_one(self.APP_PROFILE_ID, instance)
        self.assertFalse(app_profile1 != app_profile2)

    def test___ne__(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        app_profile1 = self._make_one('app_profile_id1', instance)
        app_profile2 = self._make_one('app_profile_id2', instance)
        self.assertTrue(app_profile1 != app_profile2)

    def test_from_pb_success_routing_any(self):
        from google.cloud.bigtable_admin_v2.types import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable.enums import RoutingPolicyType

        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        desctiption = 'routing any'
        routing = RoutingPolicyType.ANY
        multi_cluster_routing_use_any = (
            data_v2_pb2.AppProfile.MultiClusterRoutingUseAny())

        app_profile_pb = data_v2_pb2.AppProfile(
            name=self.APP_PROFILE_NAME,
            description=desctiption,
            multi_cluster_routing_use_any=multi_cluster_routing_use_any)

        klass = self._get_target_class()
        app_profile = klass.from_pb(app_profile_pb, instance)
        self.assertIsInstance(app_profile, klass)
        self.assertIs(app_profile._instance, instance)
        self.assertEqual(app_profile.app_profile_id, self.APP_PROFILE_ID)
        self.assertEqual(app_profile.description, desctiption)
        self.assertEqual(app_profile.routing_policy_type, routing)
        self.assertEqual(app_profile.allow_transactional_writes, False)

    def test_from_pb_success_routing_single(self):
        from google.cloud.bigtable_admin_v2.types import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable.enums import RoutingPolicyType

        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        desctiption = 'routing single'
        allow_transactional_writes = True
        routing = RoutingPolicyType.SINGLE
        single_cluster_routing = (
                data_v2_pb2.AppProfile.SingleClusterRouting(
                    cluster_id=self.CLUSTER_ID,
                    allow_transactional_writes=allow_transactional_writes))

        app_profile_pb = data_v2_pb2.AppProfile(
            name=self.APP_PROFILE_NAME,
            description=desctiption,
            single_cluster_routing=single_cluster_routing)

        klass = self._get_target_class()
        app_profile = klass.from_pb(app_profile_pb, instance)
        self.assertIsInstance(app_profile, klass)
        self.assertIs(app_profile._instance, instance)
        self.assertEqual(app_profile.app_profile_id, self.APP_PROFILE_ID)
        self.assertEqual(app_profile.description, desctiption)
        self.assertEqual(app_profile.routing_policy_type, routing)
        self.assertEqual(app_profile.cluster_id, self.CLUSTER_ID)
        self.assertEqual(app_profile.allow_transactional_writes,
                         allow_transactional_writes)

    def test_from_pb_bad_app_profile_name(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)

        bad_app_profile_name = 'BAD_NAME'

        app_profile_pb = data_v2_pb2.AppProfile(name=bad_app_profile_name)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(app_profile_pb, None)

    def test_from_pb_instance_id_mistmatch(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)

        ALT_INSTANCE_ID = 'ALT_INSTANCE_ID'
        client = _Client(self.PROJECT)
        instance = _Instance(ALT_INSTANCE_ID, client)
        self.assertEqual(instance.instance_id, ALT_INSTANCE_ID)

        app_profile_pb = data_v2_pb2.AppProfile(name=self.APP_PROFILE_NAME)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(app_profile_pb, instance)

    def test_reload_routing_any(self):
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable.enums import RoutingPolicyType

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = _Instance(self.INSTANCE_ID, client)

        routing = RoutingPolicyType.ANY
        description = 'routing policy any'

        app_profile = self._make_one(self.APP_PROFILE_ID, instance,
                                     routing_policy_type=routing,
                                     description=description)

        # Create response_pb
        description_from_server = 'routing policy switched to single'
        cluster_id_from_server = self.CLUSTER_ID
        allow_transactional_writes = True
        single_cluster_routing = (
                data_v2_pb2.AppProfile.SingleClusterRouting(
                    cluster_id=cluster_id_from_server,
                    allow_transactional_writes=allow_transactional_writes))

        response_pb = data_v2_pb2.AppProfile(
            name=app_profile.name,
            single_cluster_routing=single_cluster_routing,
            description=description_from_server)

        # Patch the stub used by the API method.
        client._instance_admin_client = api
        instance_stub = (
            client._instance_admin_client.bigtable_instance_admin_stub)
        instance_stub.GetCluster.side_effect = [response_pb]

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
        self.assertEqual(app_profile.routing_policy_type,
                         RoutingPolicyType.SINGLE)
        self.assertEqual(app_profile.description, description_from_server)
        self.assertEqual(app_profile.cluster_id, cluster_id_from_server)
        self.assertEqual(app_profile.allow_transactional_writes,
                         allow_transactional_writes)


class _Client(object):

    def __init__(self, project):
        self.project = project
        self.project_name = 'projects/' + self.project
        self._operations_stub = mock.sentinel.operations_stub

    def __eq__(self, other):
        return (other.project == self.project and
                other.project_name == self.project_name)


class _Instance(object):

    def __init__(self, instance_id, client):
        self.instance_id = instance_id
        self._client = client

    def __eq__(self, other):
        return (other.instance_id == self.instance_id and
                other._client == self._client)
