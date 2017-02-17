# Copyright 2016 Google Inc. All rights reserved.
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

import unittest

from google.cloud._testing import _GAXBaseAPI


class TestInstance(unittest.TestCase):

    PROJECT = 'project'
    PARENT = 'projects/' + PROJECT
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = PARENT + '/instances/' + INSTANCE_ID
    CONFIG_NAME = 'configuration-name'
    LOCATION = 'projects/' + PROJECT + '/locations/' + CONFIG_NAME
    DISPLAY_NAME = 'display_name'
    NODE_COUNT = 5
    OP_ID = 8915
    OP_NAME = ('operations/projects/%s/instances/%soperations/%d' %
               (PROJECT, INSTANCE_ID, OP_ID))
    TABLE_ID = 'table_id'
    TABLE_NAME = INSTANCE_NAME + '/tables/' + TABLE_ID
    TIMEOUT_SECONDS = 1
    DATABASE_ID = 'database_id'
    DATABASE_NAME = '%s/databases/%s' % (INSTANCE_NAME, DATABASE_ID)

    def _getTargetClass(self):
        from google.cloud.spanner.instance import Instance

        return Instance

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor_defaults(self):
        from google.cloud.spanner.instance import DEFAULT_NODE_COUNT

        client = object()
        instance = self._make_one(self.INSTANCE_ID, client)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertTrue(instance._client is client)
        self.assertTrue(instance.configuration_name is None)
        self.assertEqual(instance.node_count, DEFAULT_NODE_COUNT)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)

    def test_constructor_non_default(self):
        DISPLAY_NAME = 'display_name'
        client = object()

        instance = self._make_one(self.INSTANCE_ID, client,
                                  configuration_name=self.CONFIG_NAME,
                                  node_count=self.NODE_COUNT,
                                  display_name=DISPLAY_NAME)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertTrue(instance._client is client)
        self.assertEqual(instance.configuration_name, self.CONFIG_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertEqual(instance.display_name, DISPLAY_NAME)

    def test_copy(self):
        DISPLAY_NAME = 'display_name'

        client = _Client(self.PROJECT)
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME,
                                  display_name=DISPLAY_NAME)
        new_instance = instance.copy()

        # Make sure the client copy succeeded.
        self.assertFalse(new_instance._client is client)
        self.assertEqual(new_instance._client, client)
        # Make sure the client got copied to a new instance.
        self.assertFalse(instance is new_instance)
        self.assertEqual(instance, new_instance)

    def test__update_from_pb_success(self):
        from google.cloud.proto.spanner.admin.instance.v1 import (
            spanner_instance_admin_pb2 as admin_v1_pb2)

        display_name = 'display_name'
        instance_pb = admin_v1_pb2.Instance(
            display_name=display_name,
        )

        instance = self._make_one(None, None, None, None)
        self.assertEqual(instance.display_name, None)
        instance._update_from_pb(instance_pb)
        self.assertEqual(instance.display_name, display_name)

    def test__update_from_pb_no_display_name(self):
        from google.cloud.proto.spanner.admin.instance.v1 import (
            spanner_instance_admin_pb2 as admin_v1_pb2)

        instance_pb = admin_v1_pb2.Instance()
        instance = self._make_one(None, None, None, None)
        self.assertEqual(instance.display_name, None)
        with self.assertRaises(ValueError):
            instance._update_from_pb(instance_pb)
        self.assertEqual(instance.display_name, None)

    def test_from_pb_bad_instance_name(self):
        from google.cloud.proto.spanner.admin.instance.v1 import (
            spanner_instance_admin_pb2 as admin_v1_pb2)

        instance_name = 'INCORRECT_FORMAT'
        instance_pb = admin_v1_pb2.Instance(name=instance_name)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(instance_pb, None)

    def test_from_pb_project_mistmatch(self):
        from google.cloud.proto.spanner.admin.instance.v1 import (
            spanner_instance_admin_pb2 as admin_v1_pb2)

        ALT_PROJECT = 'ALT_PROJECT'
        client = _Client(project=ALT_PROJECT)

        self.assertNotEqual(self.PROJECT, ALT_PROJECT)

        instance_pb = admin_v1_pb2.Instance(name=self.INSTANCE_NAME)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(instance_pb, client)

    def test_from_pb_success(self):
        from google.cloud.proto.spanner.admin.instance.v1 import (
            spanner_instance_admin_pb2 as admin_v1_pb2)

        client = _Client(project=self.PROJECT)

        instance_pb = admin_v1_pb2.Instance(
            name=self.INSTANCE_NAME,
            config=self.CONFIG_NAME,
            display_name=self.INSTANCE_ID,
        )

        klass = self._getTargetClass()
        instance = klass.from_pb(instance_pb, client)
        self.assertTrue(isinstance(instance, klass))
        self.assertEqual(instance._client, client)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.configuration_name, self.CONFIG_NAME)

    def test_name_property(self):
        client = _Client(project=self.PROJECT)

        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)
        self.assertEqual(instance.name, self.INSTANCE_NAME)

    def test___eq__(self):
        client = object()
        instance1 = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)
        instance2 = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)
        self.assertEqual(instance1, instance2)

    def test___eq__type_differ(self):
        client = object()
        instance1 = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)
        instance2 = object()
        self.assertNotEqual(instance1, instance2)

    def test___ne__same_value(self):
        client = object()
        instance1 = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)
        instance2 = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)
        comparison_val = (instance1 != instance2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        instance1 = self._make_one('instance_id1', 'client1', self.CONFIG_NAME)
        instance2 = self._make_one('instance_id2', 'client2', self.CONFIG_NAME)
        self.assertNotEqual(instance1, instance2)

    def test_create_grpc_error(self):
        from google.gax.errors import GaxError

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _random_gax_error=True)
        instance = self._make_one(self.INSTANCE_ID, client,
                                  configuration_name=self.CONFIG_NAME)

        with self.assertRaises(GaxError):
            instance.create()

        (parent, instance_id, instance, options) = api._created_instance
        self.assertEqual(parent, self.PARENT)
        self.assertEqual(instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.config, self.CONFIG_NAME)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertEqual(instance.node_count, 1)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_create_already_exists(self):
        from google.cloud.exceptions import Conflict

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _create_instance_conflict=True)
        instance = self._make_one(self.INSTANCE_ID, client,
                                  configuration_name=self.CONFIG_NAME)

        with self.assertRaises(Conflict):
            instance.create()

        (parent, instance_id, instance, options) = api._created_instance
        self.assertEqual(parent, self.PARENT)
        self.assertEqual(instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.config, self.CONFIG_NAME)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertEqual(instance.node_count, 1)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_create_success(self):
        op_future = _FauxOperationFuture()
        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _create_instance_response=op_future)
        instance = self._make_one(self.INSTANCE_ID, client,
                                  configuration_name=self.CONFIG_NAME,
                                  display_name=self.DISPLAY_NAME,
                                  node_count=self.NODE_COUNT)

        future = instance.create()

        self.assertIs(future, op_future)
        self.assertEqual(future.caller_metadata,
                         {'request_type': 'CreateInstance'})

        (parent, instance_id, instance, options) = api._created_instance
        self.assertEqual(parent, self.PARENT)
        self.assertEqual(instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.config, self.CONFIG_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_exists_instance_grpc_error(self):
        from google.gax.errors import GaxError

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _random_gax_error=True)
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)

        with self.assertRaises(GaxError):
            instance.exists()

        name, options = api._got_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_exists_instance_not_found(self):
        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _instance_not_found=True)
        api._instance_not_found = True
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)

        self.assertFalse(instance.exists())

        name, options = api._got_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_exists_success(self):
        from google.cloud.proto.spanner.admin.instance.v1 import (
            spanner_instance_admin_pb2 as admin_v1_pb2)

        client = _Client(self.PROJECT)
        instance_pb = admin_v1_pb2.Instance(
            name=self.INSTANCE_NAME,
            config=self.CONFIG_NAME,
            display_name=self.DISPLAY_NAME,
            node_count=self.NODE_COUNT,
        )
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _get_instance_response=instance_pb)
        instance = self._make_one(self.INSTANCE_ID, client)

        self.assertTrue(instance.exists())

        name, options = api._got_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_reload_instance_grpc_error(self):
        from google.gax.errors import GaxError

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _random_gax_error=True)
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)

        with self.assertRaises(GaxError):
            instance.reload()

        name, options = api._got_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_reload_instance_not_found(self):
        from google.cloud.exceptions import NotFound

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _instance_not_found=True)
        api._instance_not_found = True
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)

        with self.assertRaises(NotFound):
            instance.reload()

        name, options = api._got_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_reload_success(self):
        from google.cloud.proto.spanner.admin.instance.v1 import (
            spanner_instance_admin_pb2 as admin_v1_pb2)

        client = _Client(self.PROJECT)
        instance_pb = admin_v1_pb2.Instance(
            name=self.INSTANCE_NAME,
            config=self.CONFIG_NAME,
            display_name=self.DISPLAY_NAME,
            node_count=self.NODE_COUNT,
        )
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _get_instance_response=instance_pb)
        instance = self._make_one(self.INSTANCE_ID, client)

        instance.reload()

        self.assertEqual(instance.configuration_name, self.CONFIG_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)

        name, options = api._got_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_update_grpc_error(self):
        from google.gax.errors import GaxError
        from google.cloud.spanner.instance import DEFAULT_NODE_COUNT

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _random_gax_error=True)
        instance = self._make_one(self.INSTANCE_ID, client,
                                  configuration_name=self.CONFIG_NAME)

        with self.assertRaises(GaxError):
            instance.update()

        instance, field_mask, options = api._updated_instance
        self.assertEqual(field_mask.paths,
                         ['config', 'display_name', 'node_count'])
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.config, self.CONFIG_NAME)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertEqual(instance.node_count, DEFAULT_NODE_COUNT)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_update_not_found(self):
        from google.cloud.exceptions import NotFound
        from google.cloud.spanner.instance import DEFAULT_NODE_COUNT

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _instance_not_found=True)
        instance = self._make_one(self.INSTANCE_ID, client,
                                  configuration_name=self.CONFIG_NAME)

        with self.assertRaises(NotFound):
            instance.update()

        instance, field_mask, options = api._updated_instance
        self.assertEqual(field_mask.paths,
                         ['config', 'display_name', 'node_count'])
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.config, self.CONFIG_NAME)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertEqual(instance.node_count, DEFAULT_NODE_COUNT)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_update_success(self):
        op_future = _FauxOperationFuture()
        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _update_instance_response=op_future)
        instance = self._make_one(self.INSTANCE_ID, client,
                                  configuration_name=self.CONFIG_NAME,
                                  node_count=self.NODE_COUNT,
                                  display_name=self.DISPLAY_NAME)

        future = instance.update()

        self.assertIs(future, op_future)
        self.assertEqual(future.caller_metadata,
                         {'request_type': 'UpdateInstance'})

        instance, field_mask, options = api._updated_instance
        self.assertEqual(field_mask.paths,
                         ['config', 'display_name', 'node_count'])
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.config, self.CONFIG_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_delete_grpc_error(self):
        from google.gax.errors import GaxError

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _random_gax_error=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        with self.assertRaises(GaxError):
            instance.delete()

        name, options = api._deleted_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_delete_not_found(self):
        from google.cloud.exceptions import NotFound

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _instance_not_found=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        with self.assertRaises(NotFound):
            instance.delete()

        name, options = api._deleted_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_delete_success(self):
        from google.protobuf.empty_pb2 import Empty

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _delete_instance_response=Empty())
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)

        instance.delete()

        name, options = api._deleted_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_database_factory_defaults(self):
        from google.cloud.spanner.database import Database
        from google.cloud.spanner.pool import BurstyPool

        client = _Client(self.PROJECT)
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)
        DATABASE_ID = 'database-id'

        database = instance.database(DATABASE_ID)

        self.assertTrue(isinstance(database, Database))
        self.assertEqual(database.database_id, DATABASE_ID)
        self.assertTrue(database._instance is instance)
        self.assertEqual(list(database.ddl_statements), [])
        self.assertIsInstance(database._pool, BurstyPool)
        pool = database._pool
        self.assertIs(pool._database, database)

    def test_database_factory_explicit(self):
        from google.cloud.spanner._fixtures import DDL_STATEMENTS
        from google.cloud.spanner.database import Database

        client = _Client(self.PROJECT)
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)
        DATABASE_ID = 'database-id'
        pool = _Pool()

        database = instance.database(
            DATABASE_ID, ddl_statements=DDL_STATEMENTS, pool=pool)

        self.assertTrue(isinstance(database, Database))
        self.assertEqual(database.database_id, DATABASE_ID)
        self.assertTrue(database._instance is instance)
        self.assertEqual(list(database.ddl_statements), DDL_STATEMENTS)
        self.assertIs(database._pool, pool)
        self.assertIs(pool._bound, database)

    def test_list_databases_wo_paging(self):
        from google.cloud._testing import _GAXPageIterator
        from google.gax import INITIAL_PAGE
        from google.cloud.spanner.database import Database

        NEXT_TOKEN = 'TOKEN'
        database_pb = _DatabasePB(name=self.DATABASE_NAME)
        response = _GAXPageIterator([database_pb], page_token=NEXT_TOKEN)
        client = _Client(self.PROJECT)
        api = client.database_admin_api = _FauxDatabaseAdminAPI()
        api._list_databases_response = response
        instance = self._make_one(self.INSTANCE_ID, client)

        iterator = instance.list_databases()
        next_token = iterator.next_page_token
        databases = list(iterator)

        self.assertEqual(len(databases), 1)
        database = databases[0]
        self.assertTrue(isinstance(database, Database))
        self.assertEqual(database.name, self.DATABASE_NAME)
        self.assertEqual(next_token, NEXT_TOKEN)

        instance_name, page_size, options = api._listed_databases
        self.assertEqual(instance_name, self.INSTANCE_NAME)
        self.assertEqual(page_size, None)
        self.assertTrue(options.page_token is INITIAL_PAGE)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])

    def test_list_databases_w_paging(self):
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.spanner.database import Database

        SIZE = 15
        TOKEN = 'TOKEN'
        database_pb = _DatabasePB(name=self.DATABASE_NAME)
        response = _GAXPageIterator([database_pb])
        client = _Client(self.PROJECT)
        api = client.database_admin_api = _FauxDatabaseAdminAPI()
        api._list_databases_response = response
        instance = self._make_one(self.INSTANCE_ID, client)

        iterator = instance.list_databases(
            page_size=SIZE, page_token=TOKEN)
        next_token = iterator.next_page_token
        databases = list(iterator)

        self.assertEqual(len(databases), 1)
        database = databases[0]
        self.assertTrue(isinstance(database, Database))
        self.assertEqual(database.name, self.DATABASE_NAME)
        self.assertEqual(next_token, None)

        instance_name, page_size, options = api._listed_databases
        self.assertEqual(instance_name, self.INSTANCE_NAME)
        self.assertEqual(page_size, SIZE)
        self.assertEqual(options.page_token, TOKEN)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', instance.name)])


class _Client(object):

    def __init__(self, project, timeout_seconds=None):
        self.project = project
        self.project_name = 'projects/' + self.project
        self.timeout_seconds = timeout_seconds

    def copy(self):
        from copy import deepcopy

        return deepcopy(self)

    def __eq__(self, other):
        return (other.project == self.project and
                other.project_name == self.project_name and
                other.timeout_seconds == self.timeout_seconds)


class _DatabasePB(object):

    def __init__(self, name):
        self.name = name


class _FauxInstanceAdminAPI(_GAXBaseAPI):

    _create_instance_conflict = False
    _instance_not_found = False

    def _make_grpc_already_exists(self):
        from grpc.beta.interfaces import StatusCode

        return self._make_grpc_error(StatusCode.ALREADY_EXISTS)

    def create_instance(self, parent, instance_id, instance, options=None):
        from google.gax.errors import GaxError

        self._created_instance = (parent, instance_id, instance, options)
        if self._random_gax_error:
            raise GaxError('error')
        if self._create_instance_conflict:
            raise GaxError('conflict', self._make_grpc_already_exists())
        return self._create_instance_response

    def get_instance(self, name, options=None):
        from google.gax.errors import GaxError

        self._got_instance = (name, options)
        if self._random_gax_error:
            raise GaxError('error')
        if self._instance_not_found:
            raise GaxError('not found', self._make_grpc_not_found())
        return self._get_instance_response

    def update_instance(self, instance, field_mask, options=None):
        from google.gax.errors import GaxError

        self._updated_instance = (instance, field_mask, options)
        if self._random_gax_error:
            raise GaxError('error')
        if self._instance_not_found:
            raise GaxError('not found', self._make_grpc_not_found())
        return self._update_instance_response

    def delete_instance(self, name, options=None):
        from google.gax.errors import GaxError

        self._deleted_instance = name, options
        if self._random_gax_error:
            raise GaxError('error')
        if self._instance_not_found:
            raise GaxError('not found', self._make_grpc_not_found())
        return self._delete_instance_response


class _FauxDatabaseAdminAPI(object):

    def list_databases(self, name, page_size, options):
        self._listed_databases = (name, page_size, options)
        return self._list_databases_response


class _FauxOperationFuture(object):
    pass


class _Pool(object):
    _bound = None

    def bind(self, database):
        self._bound = database
