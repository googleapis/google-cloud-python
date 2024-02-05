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

PROJECT = "PROJECT"
INSTANCE_ID = "instance-id"
DISPLAY_NAME = "display-name"
USER_AGENT = "you-sir-age-int"


def _invoke_client_factory(client_class, **kw):
    from google.cloud.bigtable.client import _create_gapic_client

    return _create_gapic_client(client_class, **kw)


def test___create_gapic_client_wo_emulator():
    client_class = mock.Mock()
    credentials = _make_credentials()
    client = _MockClient(credentials)
    client_info = client._client_info = mock.Mock()
    transport = mock.Mock()

    result = _invoke_client_factory(client_class, transport=transport)(client)

    assert result is client_class.return_value
    client_class.assert_called_once_with(
        credentials=None,
        client_info=client_info,
        client_options=None,
        transport=transport,
    )


def test___create_gapic_client_wo_emulator_w_client_options():
    client_class = mock.Mock()
    credentials = _make_credentials()
    client = _MockClient(credentials)
    client_info = client._client_info = mock.Mock()
    client_options = mock.Mock()
    transport = mock.Mock()

    result = _invoke_client_factory(
        client_class, client_options=client_options, transport=transport
    )(client)

    assert result is client_class.return_value
    client_class.assert_called_once_with(
        credentials=None,
        client_info=client_info,
        client_options=client_options,
        transport=transport,
    )


def test___create_gapic_client_w_emulator():
    client_class = mock.Mock()
    emulator_host = emulator_channel = object()
    credentials = _make_credentials()
    client_options = mock.Mock()
    transport = mock.Mock()

    client = _MockClient(
        credentials, emulator_host=emulator_host, emulator_channel=emulator_channel
    )
    client_info = client._client_info = mock.Mock()
    result = _invoke_client_factory(
        client_class, client_options=client_options, transport=transport
    )(client)

    assert result is client_class.return_value
    client_class.assert_called_once_with(
        credentials=None,
        client_info=client_info,
        client_options=client_options,
        transport=transport,
    )


class _MockClient(object):
    def __init__(self, credentials, emulator_host=None, emulator_channel=None):
        self._credentials = credentials
        self._emulator_host = emulator_host
        self._emulator_channel = emulator_channel


def _make_client(*args, **kwargs):
    from google.cloud.bigtable.client import Client

    return Client(*args, **kwargs)


@mock.patch("os.environ", {})
def test_client_constructor_defaults():
    from google.api_core import client_info
    from google.cloud.bigtable import __version__
    from google.cloud.bigtable.client import DATA_SCOPE

    credentials = _make_credentials()

    with mock.patch("google.auth.default") as mocked:
        mocked.return_value = credentials, PROJECT
        client = _make_client()

    assert client.project == PROJECT
    assert client._credentials is credentials.with_scopes.return_value
    assert not client._read_only
    assert not client._admin
    assert isinstance(client._client_info, client_info.ClientInfo)
    assert client._client_info.client_library_version == __version__
    assert client._channel is None
    assert client._emulator_host is None
    assert client.SCOPE == (DATA_SCOPE,)


def test_client_constructor_explicit():
    import warnings
    from google.cloud.bigtable.client import ADMIN_SCOPE
    from google.cloud.bigtable.client import DATA_SCOPE

    credentials = _make_credentials()
    client_info = mock.Mock()

    with warnings.catch_warnings(record=True) as warned:
        client = _make_client(
            project=PROJECT,
            credentials=credentials,
            read_only=False,
            admin=True,
            client_info=client_info,
            channel=mock.sentinel.channel,
        )

    assert len(warned) == 1

    assert client.project == PROJECT
    assert client._credentials is credentials.with_scopes.return_value
    assert not client._read_only
    assert client._admin
    assert client._client_info is client_info
    assert client._channel is mock.sentinel.channel
    assert client.SCOPE == (DATA_SCOPE, ADMIN_SCOPE)


def test_client_constructor_w_both_admin_and_read_only():
    credentials = _make_credentials()
    with pytest.raises(ValueError):
        _make_client(
            project=PROJECT,
            credentials=credentials,
            admin=True,
            read_only=True,
        )


def test_client_constructor_w_emulator_host():
    from google.cloud.environment_vars import BIGTABLE_EMULATOR
    from google.cloud.bigtable.client import _DEFAULT_BIGTABLE_EMULATOR_CLIENT
    from google.cloud.bigtable.client import _GRPC_CHANNEL_OPTIONS

    emulator_host = "localhost:8081"
    with mock.patch("os.environ", {BIGTABLE_EMULATOR: emulator_host}):
        with mock.patch("grpc.secure_channel") as factory:
            client = _make_client()
            # don't test local_composite_credentials
            # client._local_composite_credentials = lambda: credentials
            # channels are formed when needed, so access a client
            # create a gapic channel
            client.table_data_client

    assert client._emulator_host == emulator_host
    assert client.project == _DEFAULT_BIGTABLE_EMULATOR_CLIENT
    factory.assert_called_once_with(
        emulator_host,
        mock.ANY,  # test of creds wrapping in '_emulator_host' below
        options=_GRPC_CHANNEL_OPTIONS,
    )


def test_client_constructor_w_emulator_host_w_project():
    from google.cloud.environment_vars import BIGTABLE_EMULATOR
    from google.cloud.bigtable.client import _GRPC_CHANNEL_OPTIONS

    emulator_host = "localhost:8081"
    with mock.patch("os.environ", {BIGTABLE_EMULATOR: emulator_host}):
        with mock.patch("grpc.secure_channel") as factory:
            client = _make_client(project=PROJECT)
            # channels are formed when needed, so access a client
            # create a gapic channel
            client.table_data_client

    assert client._emulator_host == emulator_host
    assert client.project == PROJECT
    factory.assert_called_once_with(
        emulator_host,
        mock.ANY,  # test of creds wrapping in '_emulator_host' below
        options=_GRPC_CHANNEL_OPTIONS,
    )


def test_client_constructor_w_emulator_host_w_credentials():
    from google.cloud.environment_vars import BIGTABLE_EMULATOR
    from google.cloud.bigtable.client import _DEFAULT_BIGTABLE_EMULATOR_CLIENT
    from google.cloud.bigtable.client import _GRPC_CHANNEL_OPTIONS

    emulator_host = "localhost:8081"
    credentials = _make_credentials()
    with mock.patch("os.environ", {BIGTABLE_EMULATOR: emulator_host}):
        with mock.patch("grpc.secure_channel") as factory:
            client = _make_client(credentials=credentials)
            # channels are formed when needed, so access a client
            # create a gapic channel
            client.table_data_client

    assert client._emulator_host == emulator_host
    assert client.project == _DEFAULT_BIGTABLE_EMULATOR_CLIENT
    factory.assert_called_once_with(
        emulator_host,
        mock.ANY,  # test of creds wrapping in '_emulator_host' below
        options=_GRPC_CHANNEL_OPTIONS,
    )


def test_client__get_scopes_default():
    from google.cloud.bigtable.client import DATA_SCOPE

    client = _make_client(project=PROJECT, credentials=_make_credentials())
    assert client._get_scopes() == (DATA_SCOPE,)


def test_client__get_scopes_w_admin():
    from google.cloud.bigtable.client import ADMIN_SCOPE
    from google.cloud.bigtable.client import DATA_SCOPE

    client = _make_client(project=PROJECT, credentials=_make_credentials(), admin=True)
    expected_scopes = (DATA_SCOPE, ADMIN_SCOPE)
    assert client._get_scopes() == expected_scopes


def test_client__get_scopes_w_read_only():
    from google.cloud.bigtable.client import READ_ONLY_SCOPE

    client = _make_client(
        project=PROJECT, credentials=_make_credentials(), read_only=True
    )
    assert client._get_scopes() == (READ_ONLY_SCOPE,)


def test_client__emulator_channel_w_sync():
    emulator_host = "localhost:8081"
    transport_name = "GrpcTransportTesting"
    transport = mock.Mock(spec=["__name__"], __name__=transport_name)
    options = mock.Mock(spec=[])
    client = _make_client(
        project=PROJECT, credentials=_make_credentials(), read_only=True
    )
    client._emulator_host = emulator_host
    lcc = client._local_composite_credentials = mock.Mock(spec=[])

    with mock.patch("grpc.secure_channel") as patched:
        channel = client._emulator_channel(transport, options)

    assert channel is patched.return_value
    patched.assert_called_once_with(
        emulator_host,
        lcc.return_value,
        options=options,
    )


def test_client__emulator_channel_w_async():
    emulator_host = "localhost:8081"
    transport_name = "GrpcAsyncIOTransportTesting"
    transport = mock.Mock(spec=["__name__"], __name__=transport_name)
    options = mock.Mock(spec=[])
    client = _make_client(
        project=PROJECT, credentials=_make_credentials(), read_only=True
    )
    client._emulator_host = emulator_host
    lcc = client._local_composite_credentials = mock.Mock(spec=[])

    with mock.patch("grpc.aio.secure_channel") as patched:
        channel = client._emulator_channel(transport, options)

    assert channel is patched.return_value
    patched.assert_called_once_with(
        emulator_host,
        lcc.return_value,
        options=options,
    )


def test_client__local_composite_credentials():
    client = _make_client(
        project=PROJECT, credentials=_make_credentials(), read_only=True
    )

    wsir_patch = mock.patch("google.auth.credentials.with_scopes_if_required")
    request_patch = mock.patch("google.auth.transport.requests.Request")
    amp_patch = mock.patch("google.auth.transport.grpc.AuthMetadataPlugin")
    grpc_patches = mock.patch.multiple(
        "grpc",
        metadata_call_credentials=mock.DEFAULT,
        local_channel_credentials=mock.DEFAULT,
        composite_channel_credentials=mock.DEFAULT,
    )
    with wsir_patch as wsir_patched:
        with request_patch as request_patched:
            with amp_patch as amp_patched:
                with grpc_patches as grpc_patched:
                    credentials = client._local_composite_credentials()

    grpc_mcc = grpc_patched["metadata_call_credentials"]
    grpc_lcc = grpc_patched["local_channel_credentials"]
    grpc_ccc = grpc_patched["composite_channel_credentials"]

    assert credentials is grpc_ccc.return_value

    wsir_patched.assert_called_once_with(client._credentials, None)
    request_patched.assert_called_once_with()
    amp_patched.assert_called_once_with(
        wsir_patched.return_value,
        request_patched.return_value,
    )
    grpc_mcc.assert_called_once_with(amp_patched.return_value)
    grpc_lcc.assert_called_once_with()
    grpc_ccc.assert_called_once_with(grpc_lcc.return_value, grpc_mcc.return_value)


def _create_gapic_client_channel_helper(endpoint=None, emulator_host=None):
    from google.cloud.bigtable.client import _GRPC_CHANNEL_OPTIONS

    client_class = mock.Mock(spec=["DEFAULT_ENDPOINT"])
    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials)

    if endpoint is not None:
        client._client_options = mock.Mock(
            spec=["api_endpoint"],
            api_endpoint=endpoint,
        )
        expected_host = endpoint
    else:
        expected_host = client_class.DEFAULT_ENDPOINT

    if emulator_host is not None:
        client._emulator_host = emulator_host
        client._emulator_channel = mock.Mock(spec=[])
        expected_host = emulator_host

    grpc_transport = mock.Mock(spec=["create_channel"])

    transport = client._create_gapic_client_channel(client_class, grpc_transport)

    assert transport is grpc_transport.return_value

    if emulator_host is not None:
        client._emulator_channel.assert_called_once_with(
            transport=grpc_transport,
            options=_GRPC_CHANNEL_OPTIONS,
        )
        grpc_transport.assert_called_once_with(
            channel=client._emulator_channel.return_value,
            host=expected_host,
        )
    else:
        grpc_transport.create_channel.assert_called_once_with(
            host=expected_host,
            credentials=client._credentials,
            options=_GRPC_CHANNEL_OPTIONS,
        )
        grpc_transport.assert_called_once_with(
            channel=grpc_transport.create_channel.return_value,
            host=expected_host,
        )


def test_client__create_gapic_client_channel_w_defaults():
    _create_gapic_client_channel_helper()


def test_client__create_gapic_client_channel_w_endpoint():
    endpoint = "api.example.com"
    _create_gapic_client_channel_helper(endpoint=endpoint)


def test_client__create_gapic_client_channel_w_emulator_host():
    host = "api.example.com:1234"
    _create_gapic_client_channel_helper(emulator_host=host)


def test_client__create_gapic_client_channel_w_endpoint_w_emulator_host():
    endpoint = "api.example.com"
    host = "other.example.com:1234"
    _create_gapic_client_channel_helper(endpoint=endpoint, emulator_host=host)


def test_client_project_path():
    credentials = _make_credentials()
    project = "PROJECT"
    client = _make_client(project=project, credentials=credentials, admin=True)
    project_name = "projects/" + project
    assert client.project_path == project_name


def test_client_table_data_client_not_initialized():
    from google.cloud.bigtable_v2 import BigtableClient

    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials)

    table_data_client = client.table_data_client
    assert isinstance(table_data_client, BigtableClient)
    assert client._table_data_client is table_data_client


def test_client_table_data_client_not_initialized_w_client_info():
    from google.cloud.bigtable_v2 import BigtableClient

    credentials = _make_credentials()
    client_info = mock.Mock()
    client = _make_client(
        project=PROJECT, credentials=credentials, client_info=client_info
    )

    table_data_client = client.table_data_client
    assert isinstance(table_data_client, BigtableClient)
    assert client._client_info is client_info
    assert client._table_data_client is table_data_client


def test_client_table_data_client_not_initialized_w_client_options():
    from google.api_core.client_options import ClientOptions

    credentials = _make_credentials()
    client_options = ClientOptions(quota_project_id="QUOTA-PROJECT", api_endpoint="xyz")
    client = _make_client(
        project=PROJECT, credentials=credentials, client_options=client_options
    )

    patch = mock.patch("google.cloud.bigtable_v2.BigtableClient")
    with patch as mocked:
        table_data_client = client.table_data_client

    assert table_data_client is mocked.return_value
    assert client._table_data_client is table_data_client

    mocked.assert_called_once_with(
        client_info=client._client_info,
        credentials=None,
        transport=mock.ANY,
        client_options=client_options,
    )


def test_client_table_data_client_initialized():
    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)

    already = client._table_data_client = object()
    assert client.table_data_client is already


def test_client_table_admin_client_not_initialized_no_admin_flag():
    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials)

    with pytest.raises(ValueError):
        client.table_admin_client()


def test_client_table_admin_client_not_initialized_w_admin_flag():
    from google.cloud.bigtable_admin_v2 import BigtableTableAdminClient

    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)

    table_admin_client = client.table_admin_client
    assert isinstance(table_admin_client, BigtableTableAdminClient)
    assert client._table_admin_client is table_admin_client


def test_client_table_admin_client_not_initialized_w_client_info():
    from google.cloud.bigtable_admin_v2 import BigtableTableAdminClient

    credentials = _make_credentials()
    client_info = mock.Mock()
    client = _make_client(
        project=PROJECT,
        credentials=credentials,
        admin=True,
        client_info=client_info,
    )

    table_admin_client = client.table_admin_client
    assert isinstance(table_admin_client, BigtableTableAdminClient)
    assert client._client_info is client_info
    assert client._table_admin_client is table_admin_client


def test_client_table_admin_client_not_initialized_w_client_options():
    credentials = _make_credentials()
    admin_client_options = mock.Mock()
    client = _make_client(
        project=PROJECT,
        credentials=credentials,
        admin=True,
        admin_client_options=admin_client_options,
    )

    client._create_gapic_client_channel = mock.Mock()
    patch = mock.patch("google.cloud.bigtable_admin_v2.BigtableTableAdminClient")
    with patch as mocked:
        table_admin_client = client.table_admin_client

    assert table_admin_client is mocked.return_value
    assert client._table_admin_client is table_admin_client
    mocked.assert_called_once_with(
        client_info=client._client_info,
        credentials=None,
        transport=mock.ANY,
        client_options=admin_client_options,
    )


def test_client_table_admin_client_initialized():
    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)

    already = client._table_admin_client = object()
    assert client.table_admin_client is already


def test_client_instance_admin_client_not_initialized_no_admin_flag():
    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials)

    with pytest.raises(ValueError):
        client.instance_admin_client()


def test_client_instance_admin_client_not_initialized_w_admin_flag():
    from google.cloud.bigtable_admin_v2 import BigtableInstanceAdminClient

    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)

    instance_admin_client = client.instance_admin_client
    assert isinstance(instance_admin_client, BigtableInstanceAdminClient)
    assert client._instance_admin_client is instance_admin_client


def test_client_instance_admin_client_not_initialized_w_client_info():
    from google.cloud.bigtable_admin_v2 import BigtableInstanceAdminClient

    credentials = _make_credentials()
    client_info = mock.Mock()
    client = _make_client(
        project=PROJECT,
        credentials=credentials,
        admin=True,
        client_info=client_info,
    )

    instance_admin_client = client.instance_admin_client
    assert isinstance(instance_admin_client, BigtableInstanceAdminClient)
    assert client._client_info is client_info
    assert client._instance_admin_client is instance_admin_client


def test_client_instance_admin_client_not_initialized_w_client_options():
    credentials = _make_credentials()
    admin_client_options = mock.Mock()
    client = _make_client(
        project=PROJECT,
        credentials=credentials,
        admin=True,
        admin_client_options=admin_client_options,
    )

    client._create_gapic_client_channel = mock.Mock()
    patch = mock.patch("google.cloud.bigtable_admin_v2.BigtableInstanceAdminClient")
    with patch as mocked:
        instance_admin_client = client.instance_admin_client

    assert instance_admin_client is mocked.return_value
    assert client._instance_admin_client is instance_admin_client
    mocked.assert_called_once_with(
        client_info=client._client_info,
        credentials=None,
        transport=mock.ANY,
        client_options=admin_client_options,
    )


def test_client_instance_admin_client_initialized():
    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)

    already = client._instance_admin_client = object()
    assert client.instance_admin_client is already


def test_client_instance_factory_defaults():
    from google.cloud.bigtable.instance import Instance

    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials)

    instance = client.instance(INSTANCE_ID)

    assert isinstance(instance, Instance)
    assert instance.instance_id == INSTANCE_ID
    assert instance.display_name == INSTANCE_ID
    assert instance.type_ is None
    assert instance.labels is None
    assert instance._client is client


def test_client_instance_factory_non_defaults():
    from google.cloud.bigtable.instance import Instance
    from google.cloud.bigtable import enums

    instance_type = enums.Instance.Type.DEVELOPMENT
    labels = {"foo": "bar"}
    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials)

    instance = client.instance(
        INSTANCE_ID,
        display_name=DISPLAY_NAME,
        instance_type=instance_type,
        labels=labels,
    )

    assert isinstance(instance, Instance)
    assert instance.instance_id == INSTANCE_ID
    assert instance.display_name == DISPLAY_NAME
    assert instance.type_ == instance_type
    assert instance.labels == labels
    assert instance._client is client


def test_client_list_instances():
    from google.cloud.bigtable_admin_v2.types import instance as data_v2_pb2
    from google.cloud.bigtable_admin_v2.types import (
        bigtable_instance_admin as messages_v2_pb2,
    )
    from google.cloud.bigtable_admin_v2.services.bigtable_instance_admin import (
        BigtableInstanceAdminClient,
    )
    from google.cloud.bigtable.instance import Instance

    FAILED_LOCATION = "FAILED"
    INSTANCE_ID1 = "instance-id1"
    INSTANCE_ID2 = "instance-id2"
    INSTANCE_NAME1 = "projects/" + PROJECT + "/instances/" + INSTANCE_ID1
    INSTANCE_NAME2 = "projects/" + PROJECT + "/instances/" + INSTANCE_ID2

    api = mock.create_autospec(BigtableInstanceAdminClient)
    credentials = _make_credentials()

    client = _make_client(project=PROJECT, credentials=credentials, admin=True)

    # Create response_pb
    response_pb = messages_v2_pb2.ListInstancesResponse(
        failed_locations=[FAILED_LOCATION],
        instances=[
            data_v2_pb2.Instance(name=INSTANCE_NAME1, display_name=INSTANCE_NAME1),
            data_v2_pb2.Instance(name=INSTANCE_NAME2, display_name=INSTANCE_NAME2),
        ],
    )

    # Patch the stub used by the API method.
    client._instance_admin_client = api
    instance_stub = client._instance_admin_client

    instance_stub.list_instances.side_effect = [response_pb]

    # Perform the method and check the result.
    instances, failed_locations = client.list_instances()

    instance_1, instance_2 = instances

    assert isinstance(instance_1, Instance)
    assert instance_1.instance_id == INSTANCE_ID1
    assert instance_1._client is client

    assert isinstance(instance_2, Instance)
    assert instance_2.instance_id == INSTANCE_ID2
    assert instance_2._client is client

    assert failed_locations == [FAILED_LOCATION]


def test_client_list_clusters():
    from google.cloud.bigtable_admin_v2.services.bigtable_instance_admin import (
        BigtableInstanceAdminClient,
    )
    from google.cloud.bigtable_admin_v2.types import (
        bigtable_instance_admin as messages_v2_pb2,
    )
    from google.cloud.bigtable_admin_v2.types import instance as data_v2_pb2
    from google.cloud.bigtable.instance import Cluster

    instance_api = mock.create_autospec(BigtableInstanceAdminClient)

    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials, admin=True)

    INSTANCE_ID1 = "instance-id1"
    INSTANCE_ID2 = "instance-id2"

    failed_location = "FAILED"
    cluster_id1 = "{}-cluster".format(INSTANCE_ID1)
    cluster_id2 = "{}-cluster-1".format(INSTANCE_ID2)
    cluster_id3 = "{}-cluster-2".format(INSTANCE_ID2)
    cluster_name1 = client.instance_admin_client.cluster_path(
        PROJECT, INSTANCE_ID1, cluster_id1
    )
    cluster_name2 = client.instance_admin_client.cluster_path(
        PROJECT, INSTANCE_ID2, cluster_id2
    )
    cluster_name3 = client.instance_admin_client.cluster_path(
        PROJECT, INSTANCE_ID2, cluster_id3
    )

    # Create response_pb
    response_pb = messages_v2_pb2.ListClustersResponse(
        failed_locations=[failed_location],
        clusters=[
            data_v2_pb2.Cluster(name=cluster_name1),
            data_v2_pb2.Cluster(name=cluster_name2),
            data_v2_pb2.Cluster(name=cluster_name3),
        ],
    )

    # Patch the stub used by the API method.
    client._instance_admin_client = instance_api
    instance_stub = client._instance_admin_client

    instance_stub.list_clusters.side_effect = [response_pb]

    # Perform the method and check the result.
    clusters, failed_locations = client.list_clusters()

    cluster_1, cluster_2, cluster_3 = clusters

    assert isinstance(cluster_1, Cluster)
    assert cluster_1.cluster_id == cluster_id1
    assert cluster_1._instance.instance_id == INSTANCE_ID1

    assert isinstance(cluster_2, Cluster)
    assert cluster_2.cluster_id == cluster_id2
    assert cluster_2._instance.instance_id == INSTANCE_ID2

    assert isinstance(cluster_3, Cluster)
    assert cluster_3.cluster_id == cluster_id3
    assert cluster_3._instance.instance_id == INSTANCE_ID2

    assert failed_locations == [failed_location]
