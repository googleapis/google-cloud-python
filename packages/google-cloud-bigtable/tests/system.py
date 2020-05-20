# Copyright 2016 Google LLC
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

import datetime
import operator
import os
import unittest

from google.api_core.exceptions import TooManyRequests
from google.cloud.environment_vars import BIGTABLE_EMULATOR
from test_utils.retry import RetryErrors
from test_utils.retry import RetryResult
from test_utils.system import EmulatorCreds
from test_utils.system import unique_resource_id

from google.cloud._helpers import _datetime_from_microseconds
from google.cloud._helpers import _microseconds_from_datetime
from google.cloud._helpers import UTC
from google.cloud.bigtable.client import Client
from google.cloud.bigtable.column_family import MaxVersionsGCRule
from google.cloud.bigtable.policy import Policy
from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE
from google.cloud.bigtable.row_filters import ApplyLabelFilter
from google.cloud.bigtable.row_filters import ColumnQualifierRegexFilter
from google.cloud.bigtable.row_filters import RowFilterChain
from google.cloud.bigtable.row_filters import RowFilterUnion
from google.cloud.bigtable.row_data import Cell
from google.cloud.bigtable.row_data import PartialRowData
from google.cloud.bigtable.row_set import RowSet
from google.cloud.bigtable.row_set import RowRange
from google.cloud.bigtable_admin_v2.gapic import (
    bigtable_table_admin_client_config as table_admin_config,
)

UNIQUE_SUFFIX = unique_resource_id("-")
LOCATION_ID = "us-central1-c"
INSTANCE_ID = "g-c-p" + UNIQUE_SUFFIX
INSTANCE_ID_DATA = "g-c-p-d" + UNIQUE_SUFFIX
TABLE_ID = "google-cloud-python-test-table"
CLUSTER_ID = INSTANCE_ID + "-cluster"
CLUSTER_ID_DATA = INSTANCE_ID_DATA + "-cluster"
SERVE_NODES = 3
COLUMN_FAMILY_ID1 = u"col-fam-id1"
COLUMN_FAMILY_ID2 = u"col-fam-id2"
COL_NAME1 = b"col-name1"
COL_NAME2 = b"col-name2"
COL_NAME3 = b"col-name3-but-other-fam"
CELL_VAL1 = b"cell-val"
CELL_VAL2 = b"cell-val-newer"
CELL_VAL3 = b"altcol-cell-val"
CELL_VAL4 = b"foo"
ROW_KEY = b"row-key"
ROW_KEY_ALT = b"row-key-alt"
EXISTING_INSTANCES = []
LABEL_KEY = u"python-system"
label_stamp = (
    datetime.datetime.utcnow()
    .replace(microsecond=0, tzinfo=UTC)
    .strftime("%Y-%m-%dt%H-%M-%S")
)
LABELS = {LABEL_KEY: str(label_stamp)}


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """

    CLIENT = None
    INSTANCE = None
    INSTANCE_DATA = None
    CLUSTER = None
    CLUSTER_DATA = None
    IN_EMULATOR = False


def _retry_on_unavailable(exc):
    """Retry only errors whose status code is 'UNAVAILABLE'."""
    from grpc import StatusCode

    return exc.code() == StatusCode.UNAVAILABLE


retry_429 = RetryErrors(TooManyRequests, max_tries=9)


def setUpModule():
    from google.cloud.exceptions import GrpcRendezvous
    from google.cloud.bigtable.enums import Instance

    # See: https://github.com/googleapis/google-cloud-python/issues/5928
    interfaces = table_admin_config.config["interfaces"]
    iface_config = interfaces["google.bigtable.admin.v2.BigtableTableAdmin"]
    methods = iface_config["methods"]
    create_table = methods["CreateTable"]
    create_table["timeout_millis"] = 90000

    Config.IN_EMULATOR = os.getenv(BIGTABLE_EMULATOR) is not None

    if Config.IN_EMULATOR:
        credentials = EmulatorCreds()
        Config.CLIENT = Client(admin=True, credentials=credentials)
    else:
        Config.CLIENT = Client(admin=True)

    Config.INSTANCE = Config.CLIENT.instance(INSTANCE_ID, labels=LABELS)
    Config.CLUSTER = Config.INSTANCE.cluster(
        CLUSTER_ID, location_id=LOCATION_ID, serve_nodes=SERVE_NODES
    )
    Config.INSTANCE_DATA = Config.CLIENT.instance(
        INSTANCE_ID_DATA, instance_type=Instance.Type.DEVELOPMENT, labels=LABELS
    )
    Config.CLUSTER_DATA = Config.INSTANCE_DATA.cluster(
        CLUSTER_ID_DATA, location_id=LOCATION_ID
    )

    if not Config.IN_EMULATOR:
        retry = RetryErrors(GrpcRendezvous, error_predicate=_retry_on_unavailable)
        instances, failed_locations = retry(Config.CLIENT.list_instances)()

        if len(failed_locations) != 0:
            raise ValueError("List instances failed in module set up.")

        EXISTING_INSTANCES[:] = instances

        # After listing, create the test instances.
        admin_op = Config.INSTANCE.create(clusters=[Config.CLUSTER])
        admin_op.result(timeout=10)
        data_op = Config.INSTANCE_DATA.create(clusters=[Config.CLUSTER_DATA])
        data_op.result(timeout=10)


def tearDownModule():
    if not Config.IN_EMULATOR:
        retry_429(Config.INSTANCE.delete)()
        retry_429(Config.INSTANCE_DATA.delete)()


class TestInstanceAdminAPI(unittest.TestCase):
    def setUp(self):
        if Config.IN_EMULATOR:
            self.skipTest("Instance Admin API not supported in emulator")
        self.instances_to_delete = []

    def tearDown(self):
        for instance in self.instances_to_delete:
            retry_429(instance.delete)()

    def test_list_instances(self):
        instances, failed_locations = Config.CLIENT.list_instances()

        self.assertEqual(failed_locations, [])

        found = set([instance.name for instance in instances])
        self.assertTrue(Config.INSTANCE.name in found)

    def test_reload(self):
        from google.cloud.bigtable import enums

        # Use same arguments as Config.INSTANCE (created in `setUpModule`)
        # so we can use reload() on a fresh instance.
        alt_instance = Config.CLIENT.instance(INSTANCE_ID)
        # Make sure metadata unset before reloading.
        alt_instance.display_name = None

        alt_instance.reload()
        self.assertEqual(alt_instance.display_name, Config.INSTANCE.display_name)
        self.assertEqual(alt_instance.labels, Config.INSTANCE.labels)
        self.assertEqual(alt_instance.type_, enums.Instance.Type.PRODUCTION)

    def test_create_instance_defaults(self):
        from google.cloud.bigtable import enums

        ALT_INSTANCE_ID = "ndef" + UNIQUE_SUFFIX
        instance = Config.CLIENT.instance(ALT_INSTANCE_ID, labels=LABELS)
        ALT_CLUSTER_ID = ALT_INSTANCE_ID + "-cluster"
        cluster = instance.cluster(
            ALT_CLUSTER_ID, location_id=LOCATION_ID, serve_nodes=SERVE_NODES
        )
        operation = instance.create(clusters=[cluster])

        # Make sure this instance gets deleted after the test case.
        self.instances_to_delete.append(instance)

        # We want to make sure the operation completes.
        operation.result(timeout=10)

        # Create a new instance instance and make sure it is the same.
        instance_alt = Config.CLIENT.instance(ALT_INSTANCE_ID)
        instance_alt.reload()

        self.assertEqual(instance, instance_alt)
        self.assertEqual(instance.display_name, instance_alt.display_name)
        # Make sure that by default a PRODUCTION type instance is created
        self.assertIsNone(instance.type_)
        self.assertEqual(instance_alt.type_, enums.Instance.Type.PRODUCTION)

    def test_create_instance(self):
        from google.cloud.bigtable import enums

        _DEVELOPMENT = enums.Instance.Type.DEVELOPMENT

        ALT_INSTANCE_ID = "new" + UNIQUE_SUFFIX
        instance = Config.CLIENT.instance(
            ALT_INSTANCE_ID, instance_type=_DEVELOPMENT, labels=LABELS
        )
        ALT_CLUSTER_ID = ALT_INSTANCE_ID + "-cluster"
        cluster = instance.cluster(ALT_CLUSTER_ID, location_id=LOCATION_ID)
        operation = instance.create(clusters=[cluster])

        # Make sure this instance gets deleted after the test case.
        self.instances_to_delete.append(instance)

        # We want to make sure the operation completes.
        operation.result(timeout=10)

        # Create a new instance instance and make sure it is the same.
        instance_alt = Config.CLIENT.instance(ALT_INSTANCE_ID)
        instance_alt.reload()

        self.assertEqual(instance, instance_alt)
        self.assertEqual(instance.display_name, instance_alt.display_name)
        self.assertEqual(instance.type_, instance_alt.type_)
        self.assertEqual(instance_alt.labels, LABELS)
        self.assertEqual(instance_alt.state, enums.Instance.State.READY)

    def test_cluster_exists(self):
        NONEXISTING_CLUSTER_ID = "cluster-id"

        cluster = Config.INSTANCE.cluster(CLUSTER_ID)
        alt_cluster = Config.INSTANCE.cluster(NONEXISTING_CLUSTER_ID)
        self.assertTrue(cluster.exists())
        self.assertFalse(alt_cluster.exists())

    def test_instance_exists(self):
        NONEXISTING_INSTANCE_ID = "instancer-id"

        alt_instance = Config.CLIENT.instance(NONEXISTING_INSTANCE_ID)
        self.assertTrue(Config.INSTANCE.exists())
        self.assertFalse(alt_instance.exists())

    def test_create_instance_w_two_clusters(self):
        from google.cloud.bigtable import enums
        from google.cloud.bigtable.table import ClusterState

        _PRODUCTION = enums.Instance.Type.PRODUCTION
        ALT_INSTANCE_ID = "dif" + UNIQUE_SUFFIX
        instance = Config.CLIENT.instance(
            ALT_INSTANCE_ID, instance_type=_PRODUCTION, labels=LABELS
        )

        ALT_CLUSTER_ID_1 = ALT_INSTANCE_ID + "-c1"
        ALT_CLUSTER_ID_2 = ALT_INSTANCE_ID + "-c2"
        LOCATION_ID_2 = "us-central1-f"
        STORAGE_TYPE = enums.StorageType.HDD
        cluster_1 = instance.cluster(
            ALT_CLUSTER_ID_1,
            location_id=LOCATION_ID,
            serve_nodes=SERVE_NODES,
            default_storage_type=STORAGE_TYPE,
        )
        cluster_2 = instance.cluster(
            ALT_CLUSTER_ID_2,
            location_id=LOCATION_ID_2,
            serve_nodes=SERVE_NODES,
            default_storage_type=STORAGE_TYPE,
        )
        operation = instance.create(clusters=[cluster_1, cluster_2])

        # Make sure this instance gets deleted after the test case.
        self.instances_to_delete.append(instance)

        # We want to make sure the operation completes.
        operation.result(timeout=30)

        # Create a new instance instance and make sure it is the same.
        instance_alt = Config.CLIENT.instance(ALT_INSTANCE_ID)
        instance_alt.reload()

        self.assertEqual(instance, instance_alt)
        self.assertEqual(instance.display_name, instance_alt.display_name)
        self.assertEqual(instance.type_, instance_alt.type_)

        clusters, failed_locations = instance_alt.list_clusters()
        self.assertEqual(failed_locations, [])

        clusters.sort(key=lambda x: x.name)
        alt_cluster_1, alt_cluster_2 = clusters

        self.assertEqual(cluster_1.location_id, alt_cluster_1.location_id)
        self.assertEqual(alt_cluster_1.state, enums.Cluster.State.READY)
        self.assertEqual(cluster_1.serve_nodes, alt_cluster_1.serve_nodes)
        self.assertEqual(
            cluster_1.default_storage_type, alt_cluster_1.default_storage_type
        )
        self.assertEqual(cluster_2.location_id, alt_cluster_2.location_id)
        self.assertEqual(alt_cluster_2.state, enums.Cluster.State.READY)
        self.assertEqual(cluster_2.serve_nodes, alt_cluster_2.serve_nodes)
        self.assertEqual(
            cluster_2.default_storage_type, alt_cluster_2.default_storage_type
        )

        # Test list clusters in project via 'client.list_clusters'
        clusters, failed_locations = Config.CLIENT.list_clusters()
        self.assertFalse(failed_locations)
        found = set([cluster.name for cluster in clusters])
        self.assertTrue(
            {alt_cluster_1.name, alt_cluster_2.name, Config.CLUSTER.name}.issubset(
                found
            )
        )

        temp_table_id = "test-get-cluster-states"
        temp_table = instance.table(temp_table_id)
        temp_table.create()
        result = temp_table.get_cluster_states()
        ReplicationState = enums.Table.ReplicationState
        expected_results = [
            ClusterState(ReplicationState.STATE_NOT_KNOWN),
            ClusterState(ReplicationState.INITIALIZING),
            ClusterState(ReplicationState.PLANNED_MAINTENANCE),
            ClusterState(ReplicationState.UNPLANNED_MAINTENANCE),
            ClusterState(ReplicationState.READY),
        ]
        cluster_id_list = result.keys()
        self.assertEqual(len(cluster_id_list), 2)
        self.assertIn(ALT_CLUSTER_ID_1, cluster_id_list)
        self.assertIn(ALT_CLUSTER_ID_2, cluster_id_list)
        for clusterstate in result.values():
            self.assertIn(clusterstate, expected_results)

        # Test create app profile with multi_cluster_routing policy
        app_profiles_to_delete = []
        description = "routing policy-multy"
        app_profile_id_1 = "app_profile_id_1"
        routing = enums.RoutingPolicyType.ANY
        self._test_create_app_profile_helper(
            app_profile_id_1,
            instance,
            routing_policy_type=routing,
            description=description,
            ignore_warnings=True,
        )
        app_profiles_to_delete.append(app_profile_id_1)

        # Test list app profiles
        self._test_list_app_profiles_helper(instance, [app_profile_id_1])

        # Test modify app profile app_profile_id_1
        # routing policy to single cluster policy,
        # cluster -> ALT_CLUSTER_ID_1,
        # allow_transactional_writes -> disallowed
        # modify description
        description = "to routing policy-single"
        routing = enums.RoutingPolicyType.SINGLE
        self._test_modify_app_profile_helper(
            app_profile_id_1,
            instance,
            routing_policy_type=routing,
            description=description,
            cluster_id=ALT_CLUSTER_ID_1,
            allow_transactional_writes=False,
        )

        # Test modify app profile app_profile_id_1
        # cluster -> ALT_CLUSTER_ID_2,
        # allow_transactional_writes -> allowed
        self._test_modify_app_profile_helper(
            app_profile_id_1,
            instance,
            routing_policy_type=routing,
            description=description,
            cluster_id=ALT_CLUSTER_ID_2,
            allow_transactional_writes=True,
            ignore_warnings=True,
        )

        # Test create app profile with single cluster routing policy
        description = "routing policy-single"
        app_profile_id_2 = "app_profile_id_2"
        routing = enums.RoutingPolicyType.SINGLE
        self._test_create_app_profile_helper(
            app_profile_id_2,
            instance,
            routing_policy_type=routing,
            description=description,
            cluster_id=ALT_CLUSTER_ID_2,
            allow_transactional_writes=False,
        )
        app_profiles_to_delete.append(app_profile_id_2)

        # Test list app profiles
        self._test_list_app_profiles_helper(
            instance, [app_profile_id_1, app_profile_id_2]
        )

        # Test modify app profile app_profile_id_2 to
        # allow transactional writes
        # Note: no need to set ``ignore_warnings`` to True
        # since we are not restrictings anything with this modification.
        self._test_modify_app_profile_helper(
            app_profile_id_2,
            instance,
            routing_policy_type=routing,
            description=description,
            cluster_id=ALT_CLUSTER_ID_2,
            allow_transactional_writes=True,
        )

        # Test modify app profile app_profile_id_2 routing policy
        # to multi_cluster_routing policy
        # modify description
        description = "to routing policy-multy"
        routing = enums.RoutingPolicyType.ANY
        self._test_modify_app_profile_helper(
            app_profile_id_2,
            instance,
            routing_policy_type=routing,
            description=description,
            allow_transactional_writes=False,
            ignore_warnings=True,
        )

        # Test delete app profiles
        for app_profile_id in app_profiles_to_delete:
            self._test_delete_app_profile_helper(app_profile_id, instance)

    def test_update_display_name_and_labels(self):
        OLD_DISPLAY_NAME = Config.INSTANCE.display_name
        NEW_DISPLAY_NAME = "Foo Bar Baz"
        n_label_stamp = (
            datetime.datetime.utcnow()
            .replace(microsecond=0, tzinfo=UTC)
            .strftime("%Y-%m-%dt%H-%M-%S")
        )

        NEW_LABELS = {LABEL_KEY: str(n_label_stamp)}
        Config.INSTANCE.display_name = NEW_DISPLAY_NAME
        Config.INSTANCE.labels = NEW_LABELS
        operation = Config.INSTANCE.update()

        # We want to make sure the operation completes.
        operation.result(timeout=10)

        # Create a new instance instance and reload it.
        instance_alt = Config.CLIENT.instance(INSTANCE_ID, labels=LABELS)
        self.assertEqual(instance_alt.display_name, OLD_DISPLAY_NAME)
        self.assertEqual(instance_alt.labels, LABELS)
        instance_alt.reload()
        self.assertEqual(instance_alt.display_name, NEW_DISPLAY_NAME)
        self.assertEqual(instance_alt.labels, NEW_LABELS)

        # Make sure to put the instance back the way it was for the
        # other test cases.
        Config.INSTANCE.display_name = OLD_DISPLAY_NAME
        Config.INSTANCE.labels = LABELS
        operation = Config.INSTANCE.update()

        # We want to make sure the operation completes.
        operation.result(timeout=10)

    def test_update_type(self):
        from google.cloud.bigtable.enums import Instance

        _DEVELOPMENT = Instance.Type.DEVELOPMENT
        _PRODUCTION = Instance.Type.PRODUCTION
        ALT_INSTANCE_ID = "ndif" + UNIQUE_SUFFIX
        instance = Config.CLIENT.instance(
            ALT_INSTANCE_ID, instance_type=_DEVELOPMENT, labels=LABELS
        )
        operation = instance.create(location_id=LOCATION_ID, serve_nodes=None)

        # Make sure this instance gets deleted after the test case.
        self.instances_to_delete.append(instance)

        # We want to make sure the operation completes.
        operation.result(timeout=10)

        # Unset the display_name
        instance.display_name = None

        instance.type_ = _PRODUCTION
        operation = instance.update()

        # We want to make sure the operation completes.
        operation.result(timeout=10)

        # Create a new instance instance and reload it.
        instance_alt = Config.CLIENT.instance(ALT_INSTANCE_ID)
        self.assertIsNone(instance_alt.type_)
        instance_alt.reload()
        self.assertEqual(instance_alt.type_, _PRODUCTION)

    def test_update_cluster(self):
        NEW_SERVE_NODES = 4

        Config.CLUSTER.serve_nodes = NEW_SERVE_NODES

        operation = Config.CLUSTER.update()

        # We want to make sure the operation completes.
        operation.result(timeout=10)

        # Create a new cluster instance and reload it.
        alt_cluster = Config.INSTANCE.cluster(CLUSTER_ID)
        alt_cluster.reload()
        self.assertEqual(alt_cluster.serve_nodes, NEW_SERVE_NODES)

        # Make sure to put the cluster back the way it was for the
        # other test cases.
        Config.CLUSTER.serve_nodes = SERVE_NODES
        operation = Config.CLUSTER.update()
        operation.result(timeout=10)

    def test_create_cluster(self):
        from google.cloud.bigtable.enums import StorageType
        from google.cloud.bigtable.enums import Cluster

        ALT_CLUSTER_ID = INSTANCE_ID + "-c2"
        ALT_LOCATION_ID = "us-central1-f"
        ALT_SERVE_NODES = 4

        cluster_2 = Config.INSTANCE.cluster(
            ALT_CLUSTER_ID,
            location_id=ALT_LOCATION_ID,
            serve_nodes=ALT_SERVE_NODES,
            default_storage_type=(StorageType.SSD),
        )
        operation = cluster_2.create()

        # We want to make sure the operation completes.
        operation.result(timeout=30)

        # Create a new object instance, reload  and make sure it is the same.
        alt_cluster = Config.INSTANCE.cluster(ALT_CLUSTER_ID)
        alt_cluster.reload()

        self.assertEqual(cluster_2, alt_cluster)
        self.assertEqual(cluster_2.location_id, alt_cluster.location_id)
        self.assertEqual(alt_cluster.state, Cluster.State.READY)
        self.assertEqual(cluster_2.serve_nodes, alt_cluster.serve_nodes)
        self.assertEqual(
            cluster_2.default_storage_type, alt_cluster.default_storage_type
        )

        # Delete the newly created cluster and confirm
        self.assertTrue(cluster_2.exists())
        cluster_2.delete()
        self.assertFalse(cluster_2.exists())

    def _test_create_app_profile_helper(
        self,
        app_profile_id,
        instance,
        routing_policy_type,
        description=None,
        cluster_id=None,
        allow_transactional_writes=None,
        ignore_warnings=None,
    ):

        app_profile = instance.app_profile(
            app_profile_id=app_profile_id,
            routing_policy_type=routing_policy_type,
            description=description,
            cluster_id=cluster_id,
            allow_transactional_writes=allow_transactional_writes,
        )
        self.assertEqual(
            app_profile.allow_transactional_writes, allow_transactional_writes
        )

        app_profile = app_profile.create(ignore_warnings=ignore_warnings)

        # Load a different app_profile objec form the server and
        # verrify that it is the same
        alt_app_profile = instance.app_profile(app_profile_id)
        alt_app_profile.reload()

        self.assertEqual(app_profile.app_profile_id, alt_app_profile.app_profile_id)
        self.assertEqual(app_profile.routing_policy_type, routing_policy_type)
        self.assertEqual(alt_app_profile.routing_policy_type, routing_policy_type)
        self.assertEqual(app_profile.description, alt_app_profile.description)
        self.assertFalse(app_profile.allow_transactional_writes)
        self.assertFalse(alt_app_profile.allow_transactional_writes)

    def _test_list_app_profiles_helper(self, instance, app_profile_ids):
        app_profiles = instance.list_app_profiles()
        found = [app_prof.app_profile_id for app_prof in app_profiles]
        for app_profile_id in app_profile_ids:
            self.assertTrue(app_profile_id in found)

    def _test_modify_app_profile_helper(
        self,
        app_profile_id,
        instance,
        routing_policy_type,
        description=None,
        cluster_id=None,
        allow_transactional_writes=None,
        ignore_warnings=None,
    ):
        app_profile = instance.app_profile(
            app_profile_id=app_profile_id,
            routing_policy_type=routing_policy_type,
            description=description,
            cluster_id=cluster_id,
            allow_transactional_writes=allow_transactional_writes,
        )

        operation = app_profile.update(ignore_warnings)
        operation.result(timeout=30)

        alt_app_profile = instance.app_profile(app_profile_id)
        alt_app_profile.reload()
        self.assertEqual(alt_app_profile.description, description)
        self.assertEqual(alt_app_profile.routing_policy_type, routing_policy_type)
        self.assertEqual(alt_app_profile.cluster_id, cluster_id)
        self.assertEqual(
            alt_app_profile.allow_transactional_writes, allow_transactional_writes
        )

    def _test_delete_app_profile_helper(self, app_profile_id, instance):
        app_profile = instance.app_profile(app_profile_id)
        self.assertTrue(app_profile.exists())
        app_profile.delete(ignore_warnings=True)
        self.assertFalse(app_profile.exists())


class TestTableAdminAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._table = Config.INSTANCE_DATA.table(TABLE_ID)
        cls._table.create()

    @classmethod
    def tearDownClass(cls):
        cls._table.delete()

    def setUp(self):
        self.tables_to_delete = []

    def tearDown(self):
        for table in self.tables_to_delete:
            table.delete()

    def _skip_if_emulated(self, message):
        # NOTE: This method is necessary because ``Config.IN_EMULATOR``
        #       is set at runtime rather than import time, which means we
        #       can't use the @unittest.skipIf decorator.
        if Config.IN_EMULATOR:
            self.skipTest(message)

    def test_list_tables(self):
        # Since `Config.INSTANCE_DATA` is newly created in `setUpModule`, the
        # table created in `setUpClass` here will be the only one.
        tables = Config.INSTANCE_DATA.list_tables()
        self.assertEqual(tables, [self._table])

    def test_exists(self):
        retry_until_true = RetryResult(lambda result: result)
        retry_until_false = RetryResult(lambda result: not result)
        temp_table_id = "test-table_existence"
        temp_table = Config.INSTANCE_DATA.table(temp_table_id)
        self.assertFalse(temp_table.exists())
        temp_table.create()
        self.assertTrue(retry_until_true(temp_table.exists)())
        temp_table.delete()
        self.assertFalse(retry_until_false(temp_table.exists)())

    def test_create_table(self):
        temp_table_id = "test-create-table"
        temp_table = Config.INSTANCE_DATA.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        # First, create a sorted version of our expected result.
        name_attr = operator.attrgetter("name")
        expected_tables = sorted([temp_table, self._table], key=name_attr)

        # Then query for the tables in the instance and sort them by
        # name as well.
        tables = Config.INSTANCE_DATA.list_tables()
        sorted_tables = sorted(tables, key=name_attr)
        self.assertEqual(sorted_tables, expected_tables)

    def test_test_iam_permissions(self):
        self._skip_if_emulated("Method not implemented in bigtable emulator")
        temp_table_id = "test-test-iam-policy-table"
        temp_table = Config.INSTANCE_DATA.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        permissions = ["bigtable.tables.mutateRows", "bigtable.tables.readRows"]
        permissions_allowed = temp_table.test_iam_permissions(permissions)
        self.assertEqual(permissions, permissions_allowed)

    def test_get_iam_policy(self):
        self._skip_if_emulated("Method not implemented in bigtable emulator")
        temp_table_id = "test-get-iam-policy-table"
        temp_table = Config.INSTANCE_DATA.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        policy = temp_table.get_iam_policy().to_api_repr()
        self.assertEqual(policy["etag"], "ACAB")
        self.assertEqual(policy["version"], 0)

    def test_set_iam_policy(self):
        self._skip_if_emulated("Method not implemented in bigtable emulator")
        temp_table_id = "test-set-iam-policy-table"
        temp_table = Config.INSTANCE_DATA.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        new_policy = Policy()
        service_account_email = Config.CLIENT._credentials.service_account_email
        new_policy[BIGTABLE_ADMIN_ROLE] = [
            Policy.service_account(service_account_email)
        ]
        policy_latest = temp_table.set_iam_policy(new_policy).to_api_repr()

        self.assertEqual(policy_latest["bindings"][0]["role"], "roles/bigtable.admin")
        self.assertIn(service_account_email, policy_latest["bindings"][0]["members"][0])

    def test_create_table_with_families(self):
        temp_table_id = "test-create-table-with-failies"
        temp_table = Config.INSTANCE_DATA.table(temp_table_id)
        gc_rule = MaxVersionsGCRule(1)
        temp_table.create(column_families={COLUMN_FAMILY_ID1: gc_rule})
        self.tables_to_delete.append(temp_table)

        col_fams = temp_table.list_column_families()

        self.assertEqual(len(col_fams), 1)
        retrieved_col_fam = col_fams[COLUMN_FAMILY_ID1]
        self.assertIs(retrieved_col_fam._table, temp_table)
        self.assertEqual(retrieved_col_fam.column_family_id, COLUMN_FAMILY_ID1)
        self.assertEqual(retrieved_col_fam.gc_rule, gc_rule)

    def test_create_table_with_split_keys(self):
        self._skip_if_emulated("Split keys are not supported by Bigtable emulator")
        temp_table_id = "foo-bar-baz-split-table"
        initial_split_keys = [b"split_key_1", b"split_key_10", b"split_key_20"]
        temp_table = Config.INSTANCE_DATA.table(temp_table_id)
        temp_table.create(initial_split_keys=initial_split_keys)
        self.tables_to_delete.append(temp_table)

        # Read Sample Row Keys for created splits
        sample_row_keys = temp_table.sample_row_keys()
        actual_keys = [srk.row_key for srk in sample_row_keys]

        expected_keys = initial_split_keys
        expected_keys.append(b"")

        self.assertEqual(actual_keys, expected_keys)

    def test_create_column_family(self):
        temp_table_id = "test-create-column-family"
        temp_table = Config.INSTANCE_DATA.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        self.assertEqual(temp_table.list_column_families(), {})
        gc_rule = MaxVersionsGCRule(1)
        column_family = temp_table.column_family(COLUMN_FAMILY_ID1, gc_rule=gc_rule)
        column_family.create()

        col_fams = temp_table.list_column_families()

        self.assertEqual(len(col_fams), 1)
        retrieved_col_fam = col_fams[COLUMN_FAMILY_ID1]
        self.assertIs(retrieved_col_fam._table, column_family._table)
        self.assertEqual(
            retrieved_col_fam.column_family_id, column_family.column_family_id
        )
        self.assertEqual(retrieved_col_fam.gc_rule, gc_rule)

    def test_update_column_family(self):
        temp_table_id = "test-update-column-family"
        temp_table = Config.INSTANCE_DATA.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        gc_rule = MaxVersionsGCRule(1)
        column_family = temp_table.column_family(COLUMN_FAMILY_ID1, gc_rule=gc_rule)
        column_family.create()

        # Check that our created table is as expected.
        col_fams = temp_table.list_column_families()
        self.assertEqual(col_fams, {COLUMN_FAMILY_ID1: column_family})

        # Update the column family's GC rule and then try to update.
        column_family.gc_rule = None
        column_family.update()

        # Check that the update has propagated.
        col_fams = temp_table.list_column_families()
        self.assertIsNone(col_fams[COLUMN_FAMILY_ID1].gc_rule)

    def test_delete_column_family(self):
        temp_table_id = "test-delete-column-family"
        temp_table = Config.INSTANCE_DATA.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        self.assertEqual(temp_table.list_column_families(), {})
        column_family = temp_table.column_family(COLUMN_FAMILY_ID1)
        column_family.create()

        # Make sure the family is there before deleting it.
        col_fams = temp_table.list_column_families()
        self.assertEqual(list(col_fams.keys()), [COLUMN_FAMILY_ID1])

        column_family.delete()
        # Make sure we have successfully deleted it.
        self.assertEqual(temp_table.list_column_families(), {})


class TestDataAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._table = table = Config.INSTANCE_DATA.table("test-data-api")
        table.create()
        table.column_family(COLUMN_FAMILY_ID1).create()
        table.column_family(COLUMN_FAMILY_ID2).create()

    @classmethod
    def tearDownClass(cls):
        # Will also delete any data contained in the table.
        cls._table.delete()

    def _maybe_emulator_skip(self, message):
        # NOTE: This method is necessary because ``Config.IN_EMULATOR``
        #       is set at runtime rather than import time, which means we
        #       can't use the @unittest.skipIf decorator.
        if Config.IN_EMULATOR:
            self.skipTest(message)

    def setUp(self):
        self.rows_to_delete = []

    def tearDown(self):
        for row in self.rows_to_delete:
            row.clear()
            row.delete()
            row.commit()

    def _write_to_row(self, row1=None, row2=None, row3=None, row4=None):
        timestamp1 = datetime.datetime.utcnow().replace(tzinfo=UTC)
        timestamp1_micros = _microseconds_from_datetime(timestamp1)
        # Truncate to millisecond granularity.
        timestamp1_micros -= timestamp1_micros % 1000
        timestamp1 = _datetime_from_microseconds(timestamp1_micros)
        # 1000 microseconds is a millisecond
        timestamp2 = timestamp1 + datetime.timedelta(microseconds=1000)
        timestamp2_micros = _microseconds_from_datetime(timestamp2)
        timestamp3 = timestamp1 + datetime.timedelta(microseconds=2000)
        timestamp3_micros = _microseconds_from_datetime(timestamp3)
        timestamp4 = timestamp1 + datetime.timedelta(microseconds=3000)
        timestamp4_micros = _microseconds_from_datetime(timestamp4)

        if row1 is not None:
            row1.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL1, timestamp=timestamp1)
        if row2 is not None:
            row2.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL2, timestamp=timestamp2)
        if row3 is not None:
            row3.set_cell(COLUMN_FAMILY_ID1, COL_NAME2, CELL_VAL3, timestamp=timestamp3)
        if row4 is not None:
            row4.set_cell(COLUMN_FAMILY_ID2, COL_NAME3, CELL_VAL4, timestamp=timestamp4)

        # Create the cells we will check.
        cell1 = Cell(CELL_VAL1, timestamp1_micros)
        cell2 = Cell(CELL_VAL2, timestamp2_micros)
        cell3 = Cell(CELL_VAL3, timestamp3_micros)
        cell4 = Cell(CELL_VAL4, timestamp4_micros)
        return cell1, cell2, cell3, cell4

    def test_timestamp_filter_millisecond_granularity(self):
        from google.cloud.bigtable import row_filters

        end = datetime.datetime.now()
        start = end - datetime.timedelta(minutes=60)
        timestamp_range = row_filters.TimestampRange(start=start, end=end)
        timefilter = row_filters.TimestampRangeFilter(timestamp_range)
        row_data = self._table.read_rows(filter_=timefilter)
        row_data.consume_all()

    def test_mutate_rows(self):
        row1 = self._table.row(ROW_KEY)
        row1.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL1)
        row1.commit()
        self.rows_to_delete.append(row1)
        row2 = self._table.row(ROW_KEY_ALT)
        row2.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL2)
        row2.commit()
        self.rows_to_delete.append(row2)

        # Change the contents
        row1.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL3)
        row2.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL4)
        rows = [row1, row2]
        statuses = self._table.mutate_rows(rows)
        result = [status.code for status in statuses]
        expected_result = [0, 0]
        self.assertEqual(result, expected_result)

        # Check the contents
        row1_data = self._table.read_row(ROW_KEY)
        self.assertEqual(
            row1_data.cells[COLUMN_FAMILY_ID1][COL_NAME1][0].value, CELL_VAL3
        )
        row2_data = self._table.read_row(ROW_KEY_ALT)
        self.assertEqual(
            row2_data.cells[COLUMN_FAMILY_ID1][COL_NAME1][0].value, CELL_VAL4
        )

    def test_truncate_table(self):
        row_keys = [
            b"row_key_1",
            b"row_key_2",
            b"row_key_3",
            b"row_key_4",
            b"row_key_5",
            b"row_key_pr_1",
            b"row_key_pr_2",
            b"row_key_pr_3",
            b"row_key_pr_4",
            b"row_key_pr_5",
        ]

        for row_key in row_keys:
            row = self._table.row(row_key)
            row.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL1)
            row.commit()
            self.rows_to_delete.append(row)

        self._table.truncate(timeout=200)

        read_rows = self._table.yield_rows()

        for row in read_rows:
            self.assertNotIn(row.row_key.decode("utf-8"), row_keys)

    def test_drop_by_prefix_table(self):
        row_keys = [
            b"row_key_1",
            b"row_key_2",
            b"row_key_3",
            b"row_key_4",
            b"row_key_5",
            b"row_key_pr_1",
            b"row_key_pr_2",
            b"row_key_pr_3",
            b"row_key_pr_4",
            b"row_key_pr_5",
        ]

        for row_key in row_keys:
            row = self._table.row(row_key)
            row.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL1)
            row.commit()
            self.rows_to_delete.append(row)

        self._table.drop_by_prefix(row_key_prefix="row_key_pr", timeout=200)

        read_rows = self._table.yield_rows()
        expected_rows_count = 5
        read_rows_count = 0

        for row in read_rows:
            if row.row_key in row_keys:
                read_rows_count += 1

        self.assertEqual(expected_rows_count, read_rows_count)

    def test_yield_rows_with_row_set(self):
        row_keys = [
            b"row_key_1",
            b"row_key_2",
            b"row_key_3",
            b"row_key_4",
            b"row_key_5",
            b"row_key_6",
            b"row_key_7",
            b"row_key_8",
            b"row_key_9",
        ]

        rows = []
        for row_key in row_keys:
            row = self._table.row(row_key)
            row.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL1)
            rows.append(row)
            self.rows_to_delete.append(row)
        self._table.mutate_rows(rows)

        row_set = RowSet()
        row_set.add_row_range(RowRange(start_key=b"row_key_3", end_key=b"row_key_7"))
        row_set.add_row_key(b"row_key_1")

        read_rows = self._table.yield_rows(row_set=row_set)

        expected_row_keys = [
            b"row_key_1",
            b"row_key_3",
            b"row_key_4",
            b"row_key_5",
            b"row_key_6",
        ]
        found_row_keys = [row.row_key for row in read_rows]
        self.assertEqual(found_row_keys, expected_row_keys)

    def test_read_large_cell_limit(self):
        self._maybe_emulator_skip(
            "Maximum gRPC received message size for emulator is 4194304 bytes."
        )
        row = self._table.row(ROW_KEY)
        self.rows_to_delete.append(row)

        number_of_bytes = 10 * 1024 * 1024
        data = b"1" * number_of_bytes  # 10MB of 1's.
        row.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, data)
        row.commit()

        # Read back the contents of the row.
        partial_row_data = self._table.read_row(ROW_KEY)
        self.assertEqual(partial_row_data.row_key, ROW_KEY)
        cell = partial_row_data.cells[COLUMN_FAMILY_ID1]
        column = cell[COL_NAME1]
        self.assertEqual(len(column), 1)
        self.assertEqual(column[0].value, data)

    def test_read_row(self):
        row = self._table.row(ROW_KEY)
        self.rows_to_delete.append(row)

        cell1, cell2, cell3, cell4 = self._write_to_row(row, row, row, row)
        row.commit()

        # Read back the contents of the row.
        partial_row_data = self._table.read_row(ROW_KEY)
        self.assertEqual(partial_row_data.row_key, ROW_KEY)

        # Check the cells match.
        ts_attr = operator.attrgetter("timestamp")
        expected_row_contents = {
            COLUMN_FAMILY_ID1: {
                COL_NAME1: sorted([cell1, cell2], key=ts_attr, reverse=True),
                COL_NAME2: [cell3],
            },
            COLUMN_FAMILY_ID2: {COL_NAME3: [cell4]},
        }
        self.assertEqual(partial_row_data.cells, expected_row_contents)

    def test_read_rows(self):
        row = self._table.row(ROW_KEY)
        row_alt = self._table.row(ROW_KEY_ALT)
        self.rows_to_delete.extend([row, row_alt])

        cell1, cell2, cell3, cell4 = self._write_to_row(row, row_alt, row, row_alt)
        row.commit()
        row_alt.commit()

        rows_data = self._table.read_rows()
        self.assertEqual(rows_data.rows, {})
        rows_data.consume_all()

        # NOTE: We should refrain from editing protected data on instances.
        #       Instead we should make the values public or provide factories
        #       for constructing objects with them.
        row_data = PartialRowData(ROW_KEY)
        row_data._chunks_encountered = True
        row_data._committed = True
        row_data._cells = {COLUMN_FAMILY_ID1: {COL_NAME1: [cell1], COL_NAME2: [cell3]}}

        row_alt_data = PartialRowData(ROW_KEY_ALT)
        row_alt_data._chunks_encountered = True
        row_alt_data._committed = True
        row_alt_data._cells = {
            COLUMN_FAMILY_ID1: {COL_NAME1: [cell2]},
            COLUMN_FAMILY_ID2: {COL_NAME3: [cell4]},
        }

        expected_rows = {ROW_KEY: row_data, ROW_KEY_ALT: row_alt_data}
        self.assertEqual(rows_data.rows, expected_rows)

    def test_read_with_label_applied(self):
        self._maybe_emulator_skip("Labels not supported by Bigtable emulator")
        row = self._table.row(ROW_KEY)
        self.rows_to_delete.append(row)

        cell1, _, cell3, _ = self._write_to_row(row, None, row)
        row.commit()

        # Combine a label with column 1.
        label1 = u"label-red"
        label1_filter = ApplyLabelFilter(label1)
        col1_filter = ColumnQualifierRegexFilter(COL_NAME1)
        chain1 = RowFilterChain(filters=[col1_filter, label1_filter])

        # Combine a label with column 2.
        label2 = u"label-blue"
        label2_filter = ApplyLabelFilter(label2)
        col2_filter = ColumnQualifierRegexFilter(COL_NAME2)
        chain2 = RowFilterChain(filters=[col2_filter, label2_filter])

        # Bring our two labeled columns together.
        row_filter = RowFilterUnion(filters=[chain1, chain2])
        partial_row_data = self._table.read_row(ROW_KEY, filter_=row_filter)
        self.assertEqual(partial_row_data.row_key, ROW_KEY)

        cells_returned = partial_row_data.cells
        col_fam1 = cells_returned.pop(COLUMN_FAMILY_ID1)
        # Make sure COLUMN_FAMILY_ID1 was the only key.
        self.assertEqual(len(cells_returned), 0)

        (cell1_new,) = col_fam1.pop(COL_NAME1)
        (cell3_new,) = col_fam1.pop(COL_NAME2)
        # Make sure COL_NAME1 and COL_NAME2 were the only keys.
        self.assertEqual(len(col_fam1), 0)

        # Check that cell1 has matching values and gained a label.
        self.assertEqual(cell1_new.value, cell1.value)
        self.assertEqual(cell1_new.timestamp, cell1.timestamp)
        self.assertEqual(cell1.labels, [])
        self.assertEqual(cell1_new.labels, [label1])

        # Check that cell3 has matching values and gained a label.
        self.assertEqual(cell3_new.value, cell3.value)
        self.assertEqual(cell3_new.timestamp, cell3.timestamp)
        self.assertEqual(cell3.labels, [])
        self.assertEqual(cell3_new.labels, [label2])

    def test_access_with_non_admin_client(self):
        client = Client(admin=False)
        instance = client.instance(INSTANCE_ID_DATA)
        table = instance.table(self._table.table_id)
        self.assertIsNone(table.read_row("nonesuch"))
