# Copyright 2017, Google Inc. All rights reserved.
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
"""Unit tests."""

import mock
import unittest

from google.gax import errors
from google.rpc import status_pb2

from google.cloud import spanner_admin_instance_v1
from google.cloud.spanner_admin_instance_v1.proto import spanner_instance_admin_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


class CustomException(Exception):
    pass


class TestInstanceAdminClient(unittest.TestCase):
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_instance_configs(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        parent = client.project_path('[PROJECT]')

        # Mock response
        next_page_token = ''
        instance_configs_element = {}
        instance_configs = [instance_configs_element]
        expected_response = {
            'next_page_token': next_page_token,
            'instance_configs': instance_configs
        }
        expected_response = spanner_instance_admin_pb2.ListInstanceConfigsResponse(
            **expected_response)
        grpc_stub.ListInstanceConfigs.return_value = expected_response

        paged_list_response = client.list_instance_configs(parent)
        resources = list(paged_list_response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response.instance_configs[0], resources[0])

        grpc_stub.ListInstanceConfigs.assert_called_once()
        args, kwargs = grpc_stub.ListInstanceConfigs.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_instance_admin_pb2.ListInstanceConfigsRequest(
            parent=parent)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_instance_configs_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        parent = client.project_path('[PROJECT]')

        # Mock exception response
        grpc_stub.ListInstanceConfigs.side_effect = CustomException()

        paged_list_response = client.list_instance_configs(parent)
        self.assertRaises(errors.GaxError, list, paged_list_response)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_instance_config(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        name = client.instance_config_path('[PROJECT]', '[INSTANCE_CONFIG]')

        # Mock response
        name_2 = 'name2-1052831874'
        display_name = 'displayName1615086568'
        expected_response = {'name': name_2, 'display_name': display_name}
        expected_response = spanner_instance_admin_pb2.InstanceConfig(
            **expected_response)
        grpc_stub.GetInstanceConfig.return_value = expected_response

        response = client.get_instance_config(name)
        self.assertEqual(expected_response, response)

        grpc_stub.GetInstanceConfig.assert_called_once()
        args, kwargs = grpc_stub.GetInstanceConfig.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_instance_admin_pb2.GetInstanceConfigRequest(
            name=name)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_instance_config_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        name = client.instance_config_path('[PROJECT]', '[INSTANCE_CONFIG]')

        # Mock exception response
        grpc_stub.GetInstanceConfig.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.get_instance_config, name)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_instances(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        parent = client.project_path('[PROJECT]')

        # Mock response
        next_page_token = ''
        instances_element = {}
        instances = [instances_element]
        expected_response = {
            'next_page_token': next_page_token,
            'instances': instances
        }
        expected_response = spanner_instance_admin_pb2.ListInstancesResponse(
            **expected_response)
        grpc_stub.ListInstances.return_value = expected_response

        paged_list_response = client.list_instances(parent)
        resources = list(paged_list_response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response.instances[0], resources[0])

        grpc_stub.ListInstances.assert_called_once()
        args, kwargs = grpc_stub.ListInstances.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_instance_admin_pb2.ListInstancesRequest(
            parent=parent)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_instances_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        parent = client.project_path('[PROJECT]')

        # Mock exception response
        grpc_stub.ListInstances.side_effect = CustomException()

        paged_list_response = client.list_instances(parent)
        self.assertRaises(errors.GaxError, list, paged_list_response)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_instance(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        name = client.instance_path('[PROJECT]', '[INSTANCE]')

        # Mock response
        name_2 = 'name2-1052831874'
        config = 'config-1354792126'
        display_name = 'displayName1615086568'
        node_count = 1539922066
        expected_response = {
            'name': name_2,
            'config': config,
            'display_name': display_name,
            'node_count': node_count
        }
        expected_response = spanner_instance_admin_pb2.Instance(
            **expected_response)
        grpc_stub.GetInstance.return_value = expected_response

        response = client.get_instance(name)
        self.assertEqual(expected_response, response)

        grpc_stub.GetInstance.assert_called_once()
        args, kwargs = grpc_stub.GetInstance.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_instance_admin_pb2.GetInstanceRequest(
            name=name)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_instance_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        name = client.instance_path('[PROJECT]', '[INSTANCE]')

        # Mock exception response
        grpc_stub.GetInstance.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.get_instance, name)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_create_instance(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        parent = client.project_path('[PROJECT]')
        instance_id = 'instanceId-2101995259'
        instance = {}

        # Mock response
        name = 'name3373707'
        config = 'config-1354792126'
        display_name = 'displayName1615086568'
        node_count = 1539922066
        expected_response = {
            'name': name,
            'config': config,
            'display_name': display_name,
            'node_count': node_count
        }
        expected_response = spanner_instance_admin_pb2.Instance(
            **expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_create_instance', done=True)
        operation.response.Pack(expected_response)
        grpc_stub.CreateInstance.return_value = operation

        response = client.create_instance(parent, instance_id, instance)
        self.assertEqual(expected_response, response.result())

        grpc_stub.CreateInstance.assert_called_once()
        args, kwargs = grpc_stub.CreateInstance.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_instance_admin_pb2.CreateInstanceRequest(
            parent=parent, instance_id=instance_id, instance=instance)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_create_instance_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        parent = client.project_path('[PROJECT]')
        instance_id = 'instanceId-2101995259'
        instance = {}

        # Mock exception response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_create_instance_exception', done=True)
        operation.error.CopyFrom(error)
        grpc_stub.CreateInstance.return_value = operation

        response = client.create_instance(parent, instance_id, instance)
        self.assertEqual(error, response.exception())

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_update_instance(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        instance = {}
        field_mask = {}

        # Mock response
        name = 'name3373707'
        config = 'config-1354792126'
        display_name = 'displayName1615086568'
        node_count = 1539922066
        expected_response = {
            'name': name,
            'config': config,
            'display_name': display_name,
            'node_count': node_count
        }
        expected_response = spanner_instance_admin_pb2.Instance(
            **expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_update_instance', done=True)
        operation.response.Pack(expected_response)
        grpc_stub.UpdateInstance.return_value = operation

        response = client.update_instance(instance, field_mask)
        self.assertEqual(expected_response, response.result())

        grpc_stub.UpdateInstance.assert_called_once()
        args, kwargs = grpc_stub.UpdateInstance.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_instance_admin_pb2.UpdateInstanceRequest(
            instance=instance, field_mask=field_mask)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_update_instance_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        instance = {}
        field_mask = {}

        # Mock exception response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_update_instance_exception', done=True)
        operation.error.CopyFrom(error)
        grpc_stub.UpdateInstance.return_value = operation

        response = client.update_instance(instance, field_mask)
        self.assertEqual(error, response.exception())

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_delete_instance(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        name = client.instance_path('[PROJECT]', '[INSTANCE]')

        client.delete_instance(name)

        grpc_stub.DeleteInstance.assert_called_once()
        args, kwargs = grpc_stub.DeleteInstance.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_instance_admin_pb2.DeleteInstanceRequest(
            name=name)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_delete_instance_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        name = client.instance_path('[PROJECT]', '[INSTANCE]')

        # Mock exception response
        grpc_stub.DeleteInstance.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.delete_instance, name)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_set_iam_policy(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        resource = client.instance_path('[PROJECT]', '[INSTANCE]')
        policy = {}

        # Mock response
        version = 351608024
        etag = b'21'
        expected_response = {'version': version, 'etag': etag}
        expected_response = policy_pb2.Policy(**expected_response)
        grpc_stub.SetIamPolicy.return_value = expected_response

        response = client.set_iam_policy(resource, policy)
        self.assertEqual(expected_response, response)

        grpc_stub.SetIamPolicy.assert_called_once()
        args, kwargs = grpc_stub.SetIamPolicy.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource, policy=policy)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_set_iam_policy_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        resource = client.instance_path('[PROJECT]', '[INSTANCE]')
        policy = {}

        # Mock exception response
        grpc_stub.SetIamPolicy.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.set_iam_policy, resource,
                          policy)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_iam_policy(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        resource = client.instance_path('[PROJECT]', '[INSTANCE]')

        # Mock response
        version = 351608024
        etag = b'21'
        expected_response = {'version': version, 'etag': etag}
        expected_response = policy_pb2.Policy(**expected_response)
        grpc_stub.GetIamPolicy.return_value = expected_response

        response = client.get_iam_policy(resource)
        self.assertEqual(expected_response, response)

        grpc_stub.GetIamPolicy.assert_called_once()
        args, kwargs = grpc_stub.GetIamPolicy.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = iam_policy_pb2.GetIamPolicyRequest(
            resource=resource)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_iam_policy_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        resource = client.instance_path('[PROJECT]', '[INSTANCE]')

        # Mock exception response
        grpc_stub.GetIamPolicy.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.get_iam_policy, resource)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_test_iam_permissions(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        resource = client.instance_path('[PROJECT]', '[INSTANCE]')
        permissions = []

        # Mock response
        expected_response = {}
        expected_response = iam_policy_pb2.TestIamPermissionsResponse(
            **expected_response)
        grpc_stub.TestIamPermissions.return_value = expected_response

        response = client.test_iam_permissions(resource, permissions)
        self.assertEqual(expected_response, response)

        grpc_stub.TestIamPermissions.assert_called_once()
        args, kwargs = grpc_stub.TestIamPermissions.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_test_iam_permissions_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_instance_v1.InstanceAdminClient()

        # Mock request
        resource = client.instance_path('[PROJECT]', '[INSTANCE]')
        permissions = []

        # Mock exception response
        grpc_stub.TestIamPermissions.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.test_iam_permissions,
                          resource, permissions)
