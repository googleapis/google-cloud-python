# Copyright 2015 Google LLC
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


import mock
import pytest

from ._testing import _make_credentials

PROJECT = "project"
INSTANCE_ID = "instance-id"
LOCATION_ID = "location-id"
CLUSTER_ID = "cluster-id"
LOCATION_ID = "location-id"
CLUSTER_NAME = (
    "projects/" + PROJECT + "/instances/" + INSTANCE_ID + "/clusters/" + CLUSTER_ID
)
LOCATION_PATH = "projects/" + PROJECT + "/locations/"
SERVE_NODES = 5
OP_ID = 5678
OP_NAME = "operations/projects/{}/instances/{}/clusters/{}/operations/{}".format(
    PROJECT, INSTANCE_ID, CLUSTER_ID, OP_ID
)
KEY_RING_ID = "key-ring-id"
CRYPTO_KEY_ID = "crypto-key-id"
KMS_KEY_NAME = f"{LOCATION_PATH}/keyRings/{KEY_RING_ID}/cryptoKeys/{CRYPTO_KEY_ID}"


def _make_cluster(*args, **kwargs):
    from google.cloud.bigtable.cluster import Cluster

    return Cluster(*args, **kwargs)


def _make_client(*args, **kwargs):
    from google.cloud.bigtable.client import Client

    return Client(*args, **kwargs)


def test_cluster_constructor_defaults():
    client = _Client(PROJECT)
    instance = _Instance(INSTANCE_ID, client)

    cluster = _make_cluster(CLUSTER_ID, instance)

    assert cluster.cluster_id == CLUSTER_ID
    assert cluster._instance is instance
    assert cluster.location_id is None
    assert cluster.state is None
    assert cluster.serve_nodes is None
    assert cluster.default_storage_type is None
    assert cluster.kms_key_name is None


def test_cluster_constructor_explicit():
    from google.cloud.bigtable.enums import StorageType
    from google.cloud.bigtable.enums import Cluster

    STATE = Cluster.State.READY
    STORAGE_TYPE_SSD = StorageType.SSD
    client = _Client(PROJECT)
    instance = _Instance(INSTANCE_ID, client)

    cluster = _make_cluster(
        CLUSTER_ID,
        instance,
        location_id=LOCATION_ID,
        _state=STATE,
        serve_nodes=SERVE_NODES,
        default_storage_type=STORAGE_TYPE_SSD,
        kms_key_name=KMS_KEY_NAME,
    )
    assert cluster.cluster_id == CLUSTER_ID
    assert cluster._instance is instance
    assert cluster.location_id == LOCATION_ID
    assert cluster.state == STATE
    assert cluster.serve_nodes == SERVE_NODES
    assert cluster.default_storage_type == STORAGE_TYPE_SSD
    assert cluster.kms_key_name == KMS_KEY_NAME


def test_cluster_name():
    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)
    instance = _Instance(INSTANCE_ID, client)
    cluster = _make_cluster(CLUSTER_ID, instance)

    assert cluster.name == CLUSTER_NAME


def test_cluster_kms_key_name():
    client = _Client(PROJECT)
    instance = _Instance(INSTANCE_ID, client)
    cluster = _make_cluster(CLUSTER_ID, instance, kms_key_name=KMS_KEY_NAME)

    assert cluster.kms_key_name == KMS_KEY_NAME


def test_cluster_kms_key_name_setter():
    client = _Client(PROJECT)
    instance = _Instance(INSTANCE_ID, client)
    cluster = _make_cluster(CLUSTER_ID, instance, kms_key_name=KMS_KEY_NAME)

    with pytest.raises(AttributeError):
        cluster.kms_key_name = "I'm read only"


def test_cluster_from_pb_success():
    from google.cloud.bigtable_admin_v2.types import instance as data_v2_pb2
    from google.cloud.bigtable.cluster import Cluster
    from google.cloud.bigtable import enums

    client = _Client(PROJECT)
    instance = _Instance(INSTANCE_ID, client)

    location = LOCATION_PATH + LOCATION_ID
    state = enums.Cluster.State.RESIZING
    storage_type = enums.StorageType.SSD
    cluster_pb = data_v2_pb2.Cluster(
        name=CLUSTER_NAME,
        location=location,
        state=state,
        serve_nodes=SERVE_NODES,
        default_storage_type=storage_type,
        encryption_config=data_v2_pb2.Cluster.EncryptionConfig(
            kms_key_name=KMS_KEY_NAME,
        ),
    )

    cluster = Cluster.from_pb(cluster_pb, instance)
    assert isinstance(cluster, Cluster)
    assert cluster._instance == instance
    assert cluster.cluster_id == CLUSTER_ID
    assert cluster.location_id == LOCATION_ID
    assert cluster.state == state
    assert cluster.serve_nodes == SERVE_NODES
    assert cluster.default_storage_type == storage_type
    assert cluster.kms_key_name == KMS_KEY_NAME


def test_cluster_from_pb_w_bad_cluster_name():
    from google.cloud.bigtable_admin_v2.types import instance as data_v2_pb2
    from google.cloud.bigtable.cluster import Cluster

    bad_cluster_name = "BAD_NAME"

    cluster_pb = data_v2_pb2.Cluster(name=bad_cluster_name)

    with pytest.raises(ValueError):
        Cluster.from_pb(cluster_pb, None)


def test_cluster_from_pb_w_instance_id_mistmatch():
    from google.cloud.bigtable_admin_v2.types import instance as data_v2_pb2
    from google.cloud.bigtable.cluster import Cluster

    ALT_INSTANCE_ID = "ALT_INSTANCE_ID"
    client = _Client(PROJECT)
    instance = _Instance(ALT_INSTANCE_ID, client)

    assert INSTANCE_ID != ALT_INSTANCE_ID
    cluster_pb = data_v2_pb2.Cluster(name=CLUSTER_NAME)

    with pytest.raises(ValueError):
        Cluster.from_pb(cluster_pb, instance)


def test_cluster_from_pb_w_project_mistmatch():
    from google.cloud.bigtable_admin_v2.types import instance as data_v2_pb2
    from google.cloud.bigtable.cluster import Cluster

    ALT_PROJECT = "ALT_PROJECT"
    client = _Client(project=ALT_PROJECT)
    instance = _Instance(INSTANCE_ID, client)

    assert PROJECT != ALT_PROJECT
    cluster_pb = data_v2_pb2.Cluster(name=CLUSTER_NAME)

    with pytest.raises(ValueError):
        Cluster.from_pb(cluster_pb, instance)


def test_cluster___eq__():
    client = _Client(PROJECT)
    instance = _Instance(INSTANCE_ID, client)
    cluster1 = _make_cluster(CLUSTER_ID, instance, LOCATION_ID)
    cluster2 = _make_cluster(CLUSTER_ID, instance, LOCATION_ID)
    assert cluster1 == cluster2


def test_cluster___eq___w_type_differ():
    client = _Client(PROJECT)
    instance = _Instance(INSTANCE_ID, client)
    cluster1 = _make_cluster(CLUSTER_ID, instance, LOCATION_ID)
    cluster2 = object()
    assert cluster1 != cluster2


def test_cluster___ne___w_same_value():
    client = _Client(PROJECT)
    instance = _Instance(INSTANCE_ID, client)
    cluster1 = _make_cluster(CLUSTER_ID, instance, LOCATION_ID)
    cluster2 = _make_cluster(CLUSTER_ID, instance, LOCATION_ID)
    assert not (cluster1 != cluster2)


def test_cluster___ne__():
    client = _Client(PROJECT)
    instance = _Instance(INSTANCE_ID, client)
    cluster1 = _make_cluster("cluster_id1", instance, LOCATION_ID)
    cluster2 = _make_cluster("cluster_id2", instance, LOCATION_ID)
    assert cluster1 != cluster2


def _make_instance_admin_client():
    from google.cloud.bigtable_admin_v2.services.bigtable_instance_admin import (
        BigtableInstanceAdminClient,
    )

    return mock.create_autospec(BigtableInstanceAdminClient)


def test_cluster_reload():
    from google.cloud.bigtable_admin_v2.types import instance as data_v2_pb2
    from google.cloud.bigtable.enums import StorageType
    from google.cloud.bigtable.enums import Cluster

    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)
    STORAGE_TYPE_SSD = StorageType.SSD
    instance = _Instance(INSTANCE_ID, client)
    cluster = _make_cluster(
        CLUSTER_ID,
        instance,
        location_id=LOCATION_ID,
        serve_nodes=SERVE_NODES,
        default_storage_type=STORAGE_TYPE_SSD,
        kms_key_name=KMS_KEY_NAME,
    )

    # Create response_pb
    LOCATION_ID_FROM_SERVER = "new-location-id"
    STATE = Cluster.State.READY
    SERVE_NODES_FROM_SERVER = 10
    STORAGE_TYPE_FROM_SERVER = StorageType.HDD

    response_pb = data_v2_pb2.Cluster(
        name=cluster.name,
        location=LOCATION_PATH + LOCATION_ID_FROM_SERVER,
        state=STATE,
        serve_nodes=SERVE_NODES_FROM_SERVER,
        default_storage_type=STORAGE_TYPE_FROM_SERVER,
    )

    # Patch the stub used by the API method.
    api = client._instance_admin_client = _make_instance_admin_client()
    api.get_cluster.side_effect = [response_pb]

    # Create expected_result.
    expected_result = None  # reload() has no return value.

    # Check Cluster optional config values before.
    assert cluster.location_id == LOCATION_ID
    assert cluster.state is None
    assert cluster.serve_nodes == SERVE_NODES
    assert cluster.default_storage_type == STORAGE_TYPE_SSD

    # Perform the method and check the result.
    result = cluster.reload()
    assert result == expected_result
    assert cluster.location_id == LOCATION_ID_FROM_SERVER
    assert cluster.state == STATE
    assert cluster.serve_nodes == SERVE_NODES_FROM_SERVER
    assert cluster.default_storage_type == STORAGE_TYPE_FROM_SERVER
    assert cluster.kms_key_name is None

    api.get_cluster.assert_called_once_with(request={"name": cluster.name})


def test_cluster_exists_hit():
    from google.cloud.bigtable_admin_v2.types import instance as data_v2_pb2
    from google.cloud.bigtable.instance import Instance

    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)
    instance = Instance(INSTANCE_ID, client)

    cluster_name = client.instance_admin_client.cluster_path(
        PROJECT, INSTANCE_ID, CLUSTER_ID
    )
    response_pb = data_v2_pb2.Cluster(name=cluster_name)

    api = client._instance_admin_client = _make_instance_admin_client()
    api.get_cluster.return_value = response_pb

    cluster = _make_cluster(CLUSTER_ID, instance)

    assert cluster.exists()

    api.get_cluster.assert_called_once_with(request={"name": cluster.name})


def test_cluster_exists_miss():
    from google.cloud.bigtable.instance import Instance
    from google.api_core import exceptions

    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)
    instance = Instance(INSTANCE_ID, client)

    api = client._instance_admin_client = _make_instance_admin_client()
    api.get_cluster.side_effect = exceptions.NotFound("testing")

    non_existing_cluster_id = "nonesuch-cluster-2"
    cluster = _make_cluster(non_existing_cluster_id, instance)

    assert not cluster.exists()

    api.get_cluster.assert_called_once_with(request={"name": cluster.name})


def test_cluster_exists_w_error():
    from google.cloud.bigtable.instance import Instance
    from google.api_core import exceptions

    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)
    instance = Instance(INSTANCE_ID, client)

    api = client._instance_admin_client = _make_instance_admin_client()
    api.get_cluster.side_effect = exceptions.BadRequest("testing")

    cluster = _make_cluster(CLUSTER_ID, instance)

    with pytest.raises(exceptions.BadRequest):
        cluster.exists()

    api.get_cluster.assert_called_once_with(request={"name": cluster.name})


def test_cluster_create():
    import datetime
    from google.longrunning import operations_pb2
    from google.protobuf.any_pb2 import Any
    from google.cloud.bigtable_admin_v2.types import (
        bigtable_instance_admin as messages_v2_pb2,
    )
    from google.cloud._helpers import _datetime_to_pb_timestamp
    from google.cloud.bigtable.instance import Instance
    from google.cloud.bigtable_admin_v2.types import instance as instance_v2_pb2
    from google.cloud.bigtable.enums import StorageType

    NOW = datetime.datetime.utcnow()
    NOW_PB = _datetime_to_pb_timestamp(NOW)
    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)
    STORAGE_TYPE_SSD = StorageType.SSD
    LOCATION = LOCATION_PATH + LOCATION_ID
    instance = Instance(INSTANCE_ID, client)
    cluster = _make_cluster(
        CLUSTER_ID,
        instance,
        location_id=LOCATION_ID,
        serve_nodes=SERVE_NODES,
        default_storage_type=STORAGE_TYPE_SSD,
    )
    metadata = messages_v2_pb2.CreateClusterMetadata(request_time=NOW_PB)
    type_url = "type.googleapis.com/{}".format(
        messages_v2_pb2.CreateClusterMetadata._meta._pb.DESCRIPTOR.full_name
    )
    response_pb = operations_pb2.Operation(
        name=OP_NAME,
        metadata=Any(type_url=type_url, value=metadata._pb.SerializeToString()),
    )

    api = client._instance_admin_client = _make_instance_admin_client()
    api.common_location_path.return_value = LOCATION
    api.instance_path.return_value = instance.name
    api.create_cluster.return_value = response_pb

    cluster.create()

    expected_request_cluster = instance_v2_pb2.Cluster(
        location=LOCATION,
        serve_nodes=cluster.serve_nodes,
        default_storage_type=cluster.default_storage_type,
    )
    expected_request = {
        "parent": instance.name,
        "cluster_id": CLUSTER_ID,
        "cluster": expected_request_cluster,
    }
    api.create_cluster.assert_called_once_with(request=expected_request)


def test_cluster_create_w_cmek():
    import datetime
    from google.longrunning import operations_pb2
    from google.protobuf.any_pb2 import Any
    from google.cloud.bigtable_admin_v2.types import (
        bigtable_instance_admin as messages_v2_pb2,
    )
    from google.cloud._helpers import _datetime_to_pb_timestamp
    from google.cloud.bigtable.instance import Instance
    from google.cloud.bigtable_admin_v2.types import instance as instance_v2_pb2
    from google.cloud.bigtable.enums import StorageType

    NOW = datetime.datetime.utcnow()
    NOW_PB = _datetime_to_pb_timestamp(NOW)
    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)
    STORAGE_TYPE_SSD = StorageType.SSD
    LOCATION = LOCATION_PATH + LOCATION_ID
    instance = Instance(INSTANCE_ID, client)
    cluster = _make_cluster(
        CLUSTER_ID,
        instance,
        location_id=LOCATION_ID,
        serve_nodes=SERVE_NODES,
        default_storage_type=STORAGE_TYPE_SSD,
        kms_key_name=KMS_KEY_NAME,
    )
    name = instance.name
    metadata = messages_v2_pb2.CreateClusterMetadata(request_time=NOW_PB)
    type_url = "type.googleapis.com/{}".format(
        messages_v2_pb2.CreateClusterMetadata._meta._pb.DESCRIPTOR.full_name
    )
    response_pb = operations_pb2.Operation(
        name=OP_NAME,
        metadata=Any(type_url=type_url, value=metadata._pb.SerializeToString()),
    )

    api = client._instance_admin_client = _make_instance_admin_client()
    api.common_location_path.return_value = LOCATION
    api.instance_path.return_value = name
    api.create_cluster.return_value = response_pb

    cluster.create()

    expected_request_cluster = instance_v2_pb2.Cluster(
        location=LOCATION,
        serve_nodes=cluster.serve_nodes,
        default_storage_type=cluster.default_storage_type,
        encryption_config=instance_v2_pb2.Cluster.EncryptionConfig(
            kms_key_name=KMS_KEY_NAME,
        ),
    )
    expected_request = {
        "parent": instance.name,
        "cluster_id": CLUSTER_ID,
        "cluster": expected_request_cluster,
    }
    api.create_cluster.assert_called_once_with(request=expected_request)


def test_cluster_update():
    import datetime
    from google.longrunning import operations_pb2
    from google.protobuf.any_pb2 import Any
    from google.cloud._helpers import _datetime_to_pb_timestamp
    from google.cloud.bigtable_admin_v2.types import (
        bigtable_instance_admin as messages_v2_pb2,
    )
    from google.cloud.bigtable.enums import StorageType

    NOW = datetime.datetime.utcnow()
    NOW_PB = _datetime_to_pb_timestamp(NOW)

    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)
    STORAGE_TYPE_SSD = StorageType.SSD
    instance = _Instance(INSTANCE_ID, client)
    cluster = _make_cluster(
        CLUSTER_ID,
        instance,
        location_id=LOCATION_ID,
        serve_nodes=SERVE_NODES,
        default_storage_type=STORAGE_TYPE_SSD,
    )
    metadata = messages_v2_pb2.UpdateClusterMetadata(request_time=NOW_PB)
    type_url = "type.googleapis.com/{}".format(
        messages_v2_pb2.UpdateClusterMetadata._meta._pb.DESCRIPTOR.full_name
    )
    response_pb = operations_pb2.Operation(
        name=OP_NAME,
        metadata=Any(type_url=type_url, value=metadata._pb.SerializeToString()),
    )

    api = client._instance_admin_client = _make_instance_admin_client()
    api.cluster_path.return_value = (
        "projects/project/instances/instance-id/clusters/cluster-id"
    )
    api.update_cluster.return_value = response_pb

    cluster.update()

    expected_request = {
        "name": "projects/project/instances/instance-id/clusters/cluster-id",
        "serve_nodes": 5,
        "location": None,
    }
    api.update_cluster.assert_called_once_with(request=expected_request)


def test_cluster_delete():
    from google.protobuf import empty_pb2

    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)
    instance = _Instance(INSTANCE_ID, client)
    cluster = _make_cluster(CLUSTER_ID, instance, LOCATION_ID)

    api = client._instance_admin_client = _make_instance_admin_client()
    api.delete_cluster.side_effect = [empty_pb2.Empty()]

    # Perform the method and check the result.
    assert cluster.delete() is None

    api.delete_cluster.assert_called_once_with(request={"name": cluster.name})


class _Instance(object):
    def __init__(self, instance_id, client):
        self.instance_id = instance_id
        self._client = client

    def __eq__(self, other):
        return other.instance_id == self.instance_id and other._client == self._client


class _Client(object):
    def __init__(self, project):
        self.project = project
        self.project_name = "projects/" + self.project
        self._operations_stub = mock.sentinel.operations_stub

    def __eq__(self, other):
        return other.project == self.project and other.project_name == self.project_name
