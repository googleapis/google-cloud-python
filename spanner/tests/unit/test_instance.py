# Copyright 2016 Google LLC All rights reserved.
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

import mock


class TestInstance(unittest.TestCase):

    PROJECT = "project"
    PARENT = "projects/" + PROJECT
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = PARENT + "/instances/" + INSTANCE_ID
    CONFIG_NAME = "configuration-name"
    LOCATION = "projects/" + PROJECT + "/locations/" + CONFIG_NAME
    DISPLAY_NAME = "display_name"
    NODE_COUNT = 5
    OP_ID = 8915
    OP_NAME = "operations/projects/%s/instances/%soperations/%d" % (
        PROJECT,
        INSTANCE_ID,
        OP_ID,
    )
    TABLE_ID = "table_id"
    TABLE_NAME = INSTANCE_NAME + "/tables/" + TABLE_ID
    TIMEOUT_SECONDS = 1
    DATABASE_ID = "database_id"
    DATABASE_NAME = "%s/databases/%s" % (INSTANCE_NAME, DATABASE_ID)

    def _getTargetClass(self):
        from google.cloud.spanner_v1.instance import Instance

        return Instance

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor_defaults(self):
        from google.cloud.spanner_v1.instance import DEFAULT_NODE_COUNT

        client = object()
        instance = self._make_one(self.INSTANCE_ID, client)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertIs(instance._client, client)
        self.assertIs(instance.configuration_name, None)
        self.assertEqual(instance.node_count, DEFAULT_NODE_COUNT)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)

    def test_constructor_non_default(self):
        DISPLAY_NAME = "display_name"
        client = object()

        instance = self._make_one(
            self.INSTANCE_ID,
            client,
            configuration_name=self.CONFIG_NAME,
            node_count=self.NODE_COUNT,
            display_name=DISPLAY_NAME,
        )
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertIs(instance._client, client)
        self.assertEqual(instance.configuration_name, self.CONFIG_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertEqual(instance.display_name, DISPLAY_NAME)

    def test_copy(self):
        DISPLAY_NAME = "display_name"

        client = _Client(self.PROJECT)
        instance = self._make_one(
            self.INSTANCE_ID, client, self.CONFIG_NAME, display_name=DISPLAY_NAME
        )
        new_instance = instance.copy()

        # Make sure the client copy succeeded.
        self.assertIsNot(new_instance._client, client)
        self.assertEqual(new_instance._client, client)
        # Make sure the client got copied to a new instance.
        self.assertIsNot(instance, new_instance)
        self.assertEqual(instance, new_instance)

    def test__update_from_pb_success(self):
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2 as admin_v1_pb2,
        )

        display_name = "display_name"
        instance_pb = admin_v1_pb2.Instance(display_name=display_name)

        instance = self._make_one(None, None, None, None)
        self.assertEqual(instance.display_name, None)
        instance._update_from_pb(instance_pb)
        self.assertEqual(instance.display_name, display_name)

    def test__update_from_pb_no_display_name(self):
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2 as admin_v1_pb2,
        )

        instance_pb = admin_v1_pb2.Instance()
        instance = self._make_one(None, None, None, None)
        self.assertEqual(instance.display_name, None)
        with self.assertRaises(ValueError):
            instance._update_from_pb(instance_pb)
        self.assertEqual(instance.display_name, None)

    def test_from_pb_bad_instance_name(self):
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2 as admin_v1_pb2,
        )

        instance_name = "INCORRECT_FORMAT"
        instance_pb = admin_v1_pb2.Instance(name=instance_name)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(instance_pb, None)

    def test_from_pb_project_mistmatch(self):
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2 as admin_v1_pb2,
        )

        ALT_PROJECT = "ALT_PROJECT"
        client = _Client(project=ALT_PROJECT)

        self.assertNotEqual(self.PROJECT, ALT_PROJECT)

        instance_pb = admin_v1_pb2.Instance(name=self.INSTANCE_NAME)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(instance_pb, client)

    def test_from_pb_success(self):
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2 as admin_v1_pb2,
        )

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
        comparison_val = instance1 != instance2
        self.assertFalse(comparison_val)

    def test___ne__(self):
        instance1 = self._make_one("instance_id1", "client1", self.CONFIG_NAME)
        instance2 = self._make_one("instance_id2", "client2", self.CONFIG_NAME)
        self.assertNotEqual(instance1, instance2)

    def test_create_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client(self.PROJECT)
        client.instance_admin_api = _FauxInstanceAdminAPI(_rpc_error=True)
        instance = self._make_one(
            self.INSTANCE_ID, client, configuration_name=self.CONFIG_NAME
        )

        with self.assertRaises(Unknown):
            instance.create()

    def test_create_already_exists(self):
        from google.cloud.exceptions import Conflict

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _create_instance_conflict=True
        )
        instance = self._make_one(
            self.INSTANCE_ID, client, configuration_name=self.CONFIG_NAME
        )

        with self.assertRaises(Conflict):
            instance.create()

        (parent, instance_id, instance, metadata) = api._created_instance
        self.assertEqual(parent, self.PARENT)
        self.assertEqual(instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.config, self.CONFIG_NAME)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertEqual(instance.node_count, 1)
        self.assertEqual(metadata, [("google-cloud-resource-prefix", instance.name)])

    def test_create_success(self):
        op_future = _FauxOperationFuture()
        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _create_instance_response=op_future
        )
        instance = self._make_one(
            self.INSTANCE_ID,
            client,
            configuration_name=self.CONFIG_NAME,
            display_name=self.DISPLAY_NAME,
            node_count=self.NODE_COUNT,
        )

        future = instance.create()

        self.assertIs(future, op_future)

        (parent, instance_id, instance, metadata) = api._created_instance
        self.assertEqual(parent, self.PARENT)
        self.assertEqual(instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.config, self.CONFIG_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertEqual(metadata, [("google-cloud-resource-prefix", instance.name)])

    def test_exists_instance_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client(self.PROJECT)
        client.instance_admin_api = _FauxInstanceAdminAPI(_rpc_error=True)
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)

        with self.assertRaises(Unknown):
            instance.exists()

    def test_exists_instance_not_found(self):
        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _instance_not_found=True
        )
        api._instance_not_found = True
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)

        self.assertFalse(instance.exists())

        name, metadata = api._got_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(metadata, [("google-cloud-resource-prefix", instance.name)])

    def test_exists_success(self):
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2 as admin_v1_pb2,
        )

        client = _Client(self.PROJECT)
        instance_pb = admin_v1_pb2.Instance(
            name=self.INSTANCE_NAME,
            config=self.CONFIG_NAME,
            display_name=self.DISPLAY_NAME,
            node_count=self.NODE_COUNT,
        )
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _get_instance_response=instance_pb
        )
        instance = self._make_one(self.INSTANCE_ID, client)

        self.assertTrue(instance.exists())

        name, metadata = api._got_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(metadata, [("google-cloud-resource-prefix", instance.name)])

    def test_reload_instance_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client(self.PROJECT)
        client.instance_admin_api = _FauxInstanceAdminAPI(_rpc_error=True)
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)

        with self.assertRaises(Unknown):
            instance.reload()

    def test_reload_instance_not_found(self):
        from google.cloud.exceptions import NotFound

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _instance_not_found=True
        )
        api._instance_not_found = True
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)

        with self.assertRaises(NotFound):
            instance.reload()

        name, metadata = api._got_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(metadata, [("google-cloud-resource-prefix", instance.name)])

    def test_reload_success(self):
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2 as admin_v1_pb2,
        )

        client = _Client(self.PROJECT)
        instance_pb = admin_v1_pb2.Instance(
            name=self.INSTANCE_NAME,
            config=self.CONFIG_NAME,
            display_name=self.DISPLAY_NAME,
            node_count=self.NODE_COUNT,
        )
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _get_instance_response=instance_pb
        )
        instance = self._make_one(self.INSTANCE_ID, client)

        instance.reload()

        self.assertEqual(instance.configuration_name, self.CONFIG_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)

        name, metadata = api._got_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(metadata, [("google-cloud-resource-prefix", instance.name)])

    def test_update_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client(self.PROJECT)
        client.instance_admin_api = _FauxInstanceAdminAPI(_rpc_error=True)
        instance = self._make_one(
            self.INSTANCE_ID, client, configuration_name=self.CONFIG_NAME
        )

        with self.assertRaises(Unknown):
            instance.update()

    def test_update_not_found(self):
        from google.cloud.exceptions import NotFound
        from google.cloud.spanner_v1.instance import DEFAULT_NODE_COUNT

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _instance_not_found=True
        )
        instance = self._make_one(
            self.INSTANCE_ID, client, configuration_name=self.CONFIG_NAME
        )

        with self.assertRaises(NotFound):
            instance.update()

        instance, field_mask, metadata = api._updated_instance
        self.assertEqual(field_mask.paths, ["config", "display_name", "node_count"])
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.config, self.CONFIG_NAME)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertEqual(instance.node_count, DEFAULT_NODE_COUNT)
        self.assertEqual(metadata, [("google-cloud-resource-prefix", instance.name)])

    def test_update_success(self):
        op_future = _FauxOperationFuture()
        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _update_instance_response=op_future
        )
        instance = self._make_one(
            self.INSTANCE_ID,
            client,
            configuration_name=self.CONFIG_NAME,
            node_count=self.NODE_COUNT,
            display_name=self.DISPLAY_NAME,
        )

        future = instance.update()

        self.assertIs(future, op_future)

        instance, field_mask, metadata = api._updated_instance
        self.assertEqual(field_mask.paths, ["config", "display_name", "node_count"])
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.config, self.CONFIG_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertEqual(metadata, [("google-cloud-resource-prefix", instance.name)])

    def test_delete_grpc_error(self):
        from google.api_core.exceptions import Unknown

        client = _Client(self.PROJECT)
        client.instance_admin_api = _FauxInstanceAdminAPI(_rpc_error=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        with self.assertRaises(Unknown):
            instance.delete()

    def test_delete_not_found(self):
        from google.cloud.exceptions import NotFound

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _instance_not_found=True
        )
        instance = self._make_one(self.INSTANCE_ID, client)

        with self.assertRaises(NotFound):
            instance.delete()

        name, metadata = api._deleted_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(metadata, [("google-cloud-resource-prefix", instance.name)])

    def test_delete_success(self):
        from google.protobuf.empty_pb2 import Empty

        client = _Client(self.PROJECT)
        api = client.instance_admin_api = _FauxInstanceAdminAPI(
            _delete_instance_response=Empty()
        )
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)

        instance.delete()

        name, metadata = api._deleted_instance
        self.assertEqual(name, self.INSTANCE_NAME)
        self.assertEqual(metadata, [("google-cloud-resource-prefix", instance.name)])

    def test_database_factory_defaults(self):
        from google.cloud.spanner_v1.database import Database
        from google.cloud.spanner_v1.pool import BurstyPool

        client = _Client(self.PROJECT)
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)
        DATABASE_ID = "database-id"

        database = instance.database(DATABASE_ID)

        self.assertTrue(isinstance(database, Database))
        self.assertEqual(database.database_id, DATABASE_ID)
        self.assertIs(database._instance, instance)
        self.assertEqual(list(database.ddl_statements), [])
        self.assertIsInstance(database._pool, BurstyPool)
        pool = database._pool
        self.assertIs(pool._database, database)

    def test_database_factory_explicit(self):
        from google.cloud.spanner_v1.database import Database
        from tests._fixtures import DDL_STATEMENTS

        client = _Client(self.PROJECT)
        instance = self._make_one(self.INSTANCE_ID, client, self.CONFIG_NAME)
        DATABASE_ID = "database-id"
        pool = _Pool()

        database = instance.database(
            DATABASE_ID, ddl_statements=DDL_STATEMENTS, pool=pool
        )

        self.assertTrue(isinstance(database, Database))
        self.assertEqual(database.database_id, DATABASE_ID)
        self.assertIs(database._instance, instance)
        self.assertEqual(list(database.ddl_statements), DDL_STATEMENTS)
        self.assertIs(database._pool, pool)
        self.assertIs(pool._bound, database)

    def test_list_databases(self):
        from google.cloud.spanner_admin_database_v1.gapic import database_admin_client
        from google.cloud.spanner_admin_database_v1.proto import (
            spanner_database_admin_pb2,
        )
        from google.cloud.spanner_v1.database import Database

        api = database_admin_client.DatabaseAdminClient(mock.Mock())
        client = _Client(self.PROJECT)
        client.database_admin_api = api
        instance = self._make_one(self.INSTANCE_ID, client)

        databases_pb = spanner_database_admin_pb2.ListDatabasesResponse(
            databases=[
                spanner_database_admin_pb2.Database(
                    name="{}/databases/aa".format(self.INSTANCE_NAME)
                ),
                spanner_database_admin_pb2.Database(
                    name="{}/databases/bb".format(self.INSTANCE_NAME)
                ),
            ]
        )

        ld_api = api._inner_api_calls["list_databases"] = mock.Mock(
            return_value=databases_pb
        )

        response = instance.list_databases()
        databases = list(response)

        self.assertIsInstance(databases[0], Database)
        self.assertTrue(databases[0].name.endswith("/aa"))
        self.assertTrue(databases[1].name.endswith("/bb"))

        ld_api.assert_called_once_with(
            spanner_database_admin_pb2.ListDatabasesRequest(parent=self.INSTANCE_NAME),
            metadata=[("google-cloud-resource-prefix", instance.name)],
            retry=mock.ANY,
            timeout=mock.ANY,
        )

    def test_list_databases_w_options(self):
        from google.cloud.spanner_admin_database_v1.gapic import database_admin_client
        from google.cloud.spanner_admin_database_v1.proto import (
            spanner_database_admin_pb2,
        )

        api = database_admin_client.DatabaseAdminClient(mock.Mock())
        client = _Client(self.PROJECT)
        client.database_admin_api = api
        instance = self._make_one(self.INSTANCE_ID, client)

        databases_pb = spanner_database_admin_pb2.ListDatabasesResponse(databases=[])

        ld_api = api._inner_api_calls["list_databases"] = mock.Mock(
            return_value=databases_pb
        )

        page_size = 42
        page_token = "token"
        response = instance.list_databases(page_size=page_size, page_token=page_token)
        databases = list(response)

        self.assertEqual(databases, [])

        ld_api.assert_called_once_with(
            spanner_database_admin_pb2.ListDatabasesRequest(
                parent=self.INSTANCE_NAME, page_size=page_size, page_token=page_token
            ),
            metadata=[("google-cloud-resource-prefix", instance.name)],
            retry=mock.ANY,
            timeout=mock.ANY,
        )


class _Client(object):
    def __init__(self, project, timeout_seconds=None):
        self.project = project
        self.project_name = "projects/" + self.project
        self.timeout_seconds = timeout_seconds

    def copy(self):
        from copy import deepcopy

        return deepcopy(self)

    def __eq__(self, other):
        return (
            other.project == self.project
            and other.project_name == self.project_name
            and other.timeout_seconds == self.timeout_seconds
        )


class _FauxInstanceAdminAPI(object):

    _create_instance_conflict = False
    _instance_not_found = False
    _rpc_error = False

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def create_instance(self, parent, instance_id, instance, metadata=None):
        from google.api_core.exceptions import AlreadyExists, Unknown

        self._created_instance = (parent, instance_id, instance, metadata)
        if self._rpc_error:
            raise Unknown("error")
        if self._create_instance_conflict:
            raise AlreadyExists("conflict")
        return self._create_instance_response

    def get_instance(self, name, metadata=None):
        from google.api_core.exceptions import NotFound, Unknown

        self._got_instance = (name, metadata)
        if self._rpc_error:
            raise Unknown("error")
        if self._instance_not_found:
            raise NotFound("error")
        return self._get_instance_response

    def update_instance(self, instance, field_mask, metadata=None):
        from google.api_core.exceptions import NotFound, Unknown

        self._updated_instance = (instance, field_mask, metadata)
        if self._rpc_error:
            raise Unknown("error")
        if self._instance_not_found:
            raise NotFound("error")
        return self._update_instance_response

    def delete_instance(self, name, metadata=None):
        from google.api_core.exceptions import NotFound, Unknown

        self._deleted_instance = name, metadata
        if self._rpc_error:
            raise Unknown("error")
        if self._instance_not_found:
            raise NotFound("error")
        return self._delete_instance_response


class _FauxOperationFuture(object):
    pass


class _Pool(object):
    _bound = None

    def bind(self, database):
        self._bound = database
