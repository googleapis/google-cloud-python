# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import google.protobuf.field_mask_pb2 as field_mask_pb2  # type: ignore
import google.protobuf.timestamp_pb2 as timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.blockchainnodeengine.v1",
    manifest={
        "BlockchainNode",
        "ListBlockchainNodesRequest",
        "ListBlockchainNodesResponse",
        "GetBlockchainNodeRequest",
        "CreateBlockchainNodeRequest",
        "UpdateBlockchainNodeRequest",
        "DeleteBlockchainNodeRequest",
        "OperationMetadata",
    },
)


class BlockchainNode(proto.Message):
    r"""A representation of a blockchain node.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        ethereum_details (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.EthereumDetails):
            Ethereum-specific blockchain node details.

            This field is a member of `oneof`_ ``blockchain_type_details``.
        name (str):
            Output only. The fully qualified name of the blockchain
            node. e.g.
            ``projects/my-project/locations/us-central1/blockchainNodes/my-node``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp at which the
            blockchain node was first created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp at which the
            blockchain node was last updated.
        labels (MutableMapping[str, str]):
            User-provided key-value pairs.
        blockchain_type (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.BlockchainType):
            Immutable. The blockchain type of the node.

            This field is a member of `oneof`_ ``_blockchain_type``.
        connection_info (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.ConnectionInfo):
            Output only. The connection information used
            to interact with a blockchain node.
        state (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.State):
            Output only. A status representing the state
            of the node.
        private_service_connect_enabled (bool):
            Optional. When true, the node is only
            accessible via Private Service Connect; no
            public endpoints are exposed. Otherwise, the
            node is only accessible via public endpoints.
            Warning: These nodes are deprecated, please use
            public endpoints instead.
    """

    class BlockchainType(proto.Enum):
        r"""The blockchain type of the node.

        Values:
            BLOCKCHAIN_TYPE_UNSPECIFIED (0):
                Blockchain type has not been specified, but
                should be.
            ETHEREUM (1):
                The blockchain type is Ethereum.
        """

        BLOCKCHAIN_TYPE_UNSPECIFIED = 0
        ETHEREUM = 1

    class State(proto.Enum):
        r"""All possible states for a given blockchain node.

        Values:
            STATE_UNSPECIFIED (0):
                The state has not been specified.
            CREATING (1):
                The node has been requested and is in the
                process of being created.
            DELETING (2):
                The existing node is undergoing deletion, but
                is not yet finished.
            RUNNING (4):
                The node is running and ready for use.
            ERROR (5):
                The node is in an unexpected or errored
                state.
            UPDATING (6):
                The node is currently being updated.
            REPAIRING (7):
                The node is currently being repaired.
            RECONCILING (8):
                The node is currently being reconciled.
            SYNCING (9):
                The node is syncing, which is the process by
                which it obtains the latest block and current
                global state.
        """

        STATE_UNSPECIFIED = 0
        CREATING = 1
        DELETING = 2
        RUNNING = 4
        ERROR = 5
        UPDATING = 6
        REPAIRING = 7
        RECONCILING = 8
        SYNCING = 9

    class ConnectionInfo(proto.Message):
        r"""The connection information through which to interact with a
        blockchain node.

        Attributes:
            endpoint_info (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.ConnectionInfo.EndpointInfo):
                Output only. The endpoint information through
                which to interact with a blockchain node.
            service_attachment (str):
                Output only. A service attachment that exposes a node, and
                has the following format:
                projects/{project}/regions/{region}/serviceAttachments/{service_attachment_name}
        """

        class EndpointInfo(proto.Message):
            r"""Contains endpoint information through which to interact with
            a blockchain node.

            Attributes:
                json_rpc_api_endpoint (str):
                    Output only. The assigned URL for the node
                    JSON-RPC API endpoint.
                websockets_api_endpoint (str):
                    Output only. The assigned URL for the node
                    WebSockets API endpoint.
            """

            json_rpc_api_endpoint: str = proto.Field(
                proto.STRING,
                number=1,
            )
            websockets_api_endpoint: str = proto.Field(
                proto.STRING,
                number=2,
            )

        endpoint_info: "BlockchainNode.ConnectionInfo.EndpointInfo" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="BlockchainNode.ConnectionInfo.EndpointInfo",
        )
        service_attachment: str = proto.Field(
            proto.STRING,
            number=3,
        )

    class EthereumDetails(proto.Message):
        r"""Ethereum-specific blockchain node details.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            geth_details (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.EthereumDetails.GethDetails):
                Details for the Geth execution client.

                This field is a member of `oneof`_ ``execution_client_details``.
            network (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.EthereumDetails.Network):
                Immutable. The Ethereum environment being
                accessed.

                This field is a member of `oneof`_ ``_network``.
            node_type (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.EthereumDetails.NodeType):
                Immutable. The type of Ethereum node.

                This field is a member of `oneof`_ ``_node_type``.
            execution_client (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.EthereumDetails.ExecutionClient):
                Immutable. The execution client

                This field is a member of `oneof`_ ``_execution_client``.
            consensus_client (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.EthereumDetails.ConsensusClient):
                Immutable. The consensus client.

                This field is a member of `oneof`_ ``_consensus_client``.
            api_enable_admin (bool):
                Immutable. Enables JSON-RPC access to functions in the
                ``admin`` namespace. Defaults to ``false``.

                This field is a member of `oneof`_ ``_api_enable_admin``.
            api_enable_debug (bool):
                Immutable. Enables JSON-RPC access to functions in the
                ``debug`` namespace. Defaults to ``false``.

                This field is a member of `oneof`_ ``_api_enable_debug``.
            additional_endpoints (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.EthereumDetails.EthereumEndpoints):
                Output only. Ethereum-specific endpoint
                information.

                This field is a member of `oneof`_ ``_additional_endpoints``.
            validator_config (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.EthereumDetails.ValidatorConfig):
                Configuration for validator-related
                parameters on the beacon client, and for any
                GCP-managed validator client.

                This field is a member of `oneof`_ ``_validator_config``.
        """

        class Network(proto.Enum):
            r"""The Ethereum environment being accessed.

            See `Networks <https://ethereum.org/en/developers/docs/networks>`__
            for more details.

            Values:
                NETWORK_UNSPECIFIED (0):
                    The network has not been specified, but
                    should be.
                MAINNET (1):
                    The Ethereum Mainnet.
                TESTNET_GOERLI_PRATER (2):
                    Deprecated: The Ethereum Testnet based on
                    Goerli protocol. Please use another test
                    network.
                TESTNET_SEPOLIA (3):
                    The Ethereum Testnet based on Sepolia/Bepolia
                    protocol. See
                    https://github.com/eth-clients/sepolia.
                TESTNET_HOLESKY (4):
                    The Ethereum Testnet based on Holesky
                    specification. See
                    https://github.com/eth-clients/holesky.
            """

            NETWORK_UNSPECIFIED = 0
            MAINNET = 1
            TESTNET_GOERLI_PRATER = 2
            TESTNET_SEPOLIA = 3
            TESTNET_HOLESKY = 4

        class NodeType(proto.Enum):
            r"""The type of Ethereum node.

            See `Node
            Types <https://ethereum.org/en/developers/docs/nodes-and-clients/#node-types>`__
            for more details.

            Values:
                NODE_TYPE_UNSPECIFIED (0):
                    Node type has not been specified, but should
                    be.
                LIGHT (1):
                    An Ethereum node that only downloads Ethereum
                    block headers.
                FULL (2):
                    Keeps a complete copy of the blockchain data,
                    and contributes to the network by receiving,
                    validating, and forwarding transactions.
                ARCHIVE (3):
                    Holds the same data as full node as well as
                    all of the blockchain's history state data
                    dating back to the Genesis Block.
            """

            NODE_TYPE_UNSPECIFIED = 0
            LIGHT = 1
            FULL = 2
            ARCHIVE = 3

        class ExecutionClient(proto.Enum):
            r"""The execution client (i.e., Execution Engine or EL client) listens
            to new transactions broadcast in the network, executes them in EVM,
            and holds the latest state and database of all current Ethereum
            data.

            See `What are nodes and
            clients? <https://ethereum.org/en/developers/docs/nodes-and-clients/#what-are-nodes-and-clients>`__
            for more details.

            Values:
                EXECUTION_CLIENT_UNSPECIFIED (0):
                    Execution client has not been specified, but
                    should be.
                GETH (1):
                    Official Go implementation of the Ethereum protocol. See
                    `go-ethereum <https://geth.ethereum.org/>`__ for details.
                ERIGON (2):
                    An implementation of Ethereum (execution client), on the
                    efficiency frontier, written in Go. See `Erigon on
                    GitHub <https://github.com/ledgerwatch/erigon>`__ for
                    details.
            """

            EXECUTION_CLIENT_UNSPECIFIED = 0
            GETH = 1
            ERIGON = 2

        class ConsensusClient(proto.Enum):
            r"""The consensus client (also referred to as beacon node or CL client)
            implements the proof-of-stake consensus algorithm, which enables the
            network to achieve agreement based on validated data from the
            execution client.

            See `What are nodes and
            clients? <https://ethereum.org/en/developers/docs/nodes-and-clients/#what-are-nodes-and-clients>`__
            for more details.

            Values:
                CONSENSUS_CLIENT_UNSPECIFIED (0):
                    Consensus client has not been specified, but
                    should be.
                LIGHTHOUSE (1):
                    Consensus client implementation written in Rust, maintained
                    by Sigma Prime. See `Lighthouse - Sigma
                    Prime <https://lighthouse.sigmaprime.io/>`__ for details.
            """

            CONSENSUS_CLIENT_UNSPECIFIED = 0
            LIGHTHOUSE = 1

        class GethDetails(proto.Message):
            r"""Options for the Geth execution client.

            See `Command-line
            Options <https://geth.ethereum.org/docs/fundamentals/command-line-options>`__
            for more details.


            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                garbage_collection_mode (google.cloud.blockchainnodeengine_v1.types.BlockchainNode.EthereumDetails.GethDetails.GarbageCollectionMode):
                    Immutable. Blockchain garbage collection
                    mode.

                    This field is a member of `oneof`_ ``_garbage_collection_mode``.
            """

            class GarbageCollectionMode(proto.Enum):
                r"""Blockchain garbage collection modes. Only applicable when
                ``NodeType`` is ``FULL`` or ``ARCHIVE``.

                Values:
                    GARBAGE_COLLECTION_MODE_UNSPECIFIED (0):
                        The garbage collection has not been
                        specified.
                    FULL (1):
                        Configures Geth's garbage collection so that
                        older data not needed for a full node is
                        deleted. This is the default mode when creating
                        a full node.
                    ARCHIVE (2):
                        Configures Geth's garbage collection so that old data is
                        never deleted. This is the default mode when creating an
                        archive node. This value can also be chosen when creating a
                        full node in order to create a partial/recent archive node.
                        See `Sync
                        modes <https://geth.ethereum.org/docs/fundamentals/sync-modes>`__
                        for more details.
                """

                GARBAGE_COLLECTION_MODE_UNSPECIFIED = 0
                FULL = 1
                ARCHIVE = 2

            garbage_collection_mode: "BlockchainNode.EthereumDetails.GethDetails.GarbageCollectionMode" = proto.Field(
                proto.ENUM,
                number=1,
                optional=True,
                enum="BlockchainNode.EthereumDetails.GethDetails.GarbageCollectionMode",
            )

        class EthereumEndpoints(proto.Message):
            r"""Contains endpoint information specific to Ethereum nodes.

            Attributes:
                beacon_api_endpoint (str):
                    Output only. The assigned URL for the node's
                    Beacon API endpoint.
                beacon_prometheus_metrics_api_endpoint (str):
                    Output only. The assigned URL for the node's Beacon
                    Prometheus metrics endpoint. See `Prometheus
                    Metrics <https://lighthouse-book.sigmaprime.io/advanced_metrics.html>`__
                    for more details.
                execution_client_prometheus_metrics_api_endpoint (str):
                    Output only. The assigned URL for the node's
                    execution client's Prometheus metrics endpoint.
            """

            beacon_api_endpoint: str = proto.Field(
                proto.STRING,
                number=1,
            )
            beacon_prometheus_metrics_api_endpoint: str = proto.Field(
                proto.STRING,
                number=2,
            )
            execution_client_prometheus_metrics_api_endpoint: str = proto.Field(
                proto.STRING,
                number=3,
            )

        class ValidatorConfig(proto.Message):
            r"""Configuration for validator-related parameters on the beacon
            client, and for any GCP-managed validator client.


            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                mev_relay_urls (MutableSequence[str]):
                    URLs for MEV-relay services to use for block
                    building. When set, a GCP-managed MEV-boost
                    service is configured on the beacon client.
                managed_validator_client (bool):
                    Immutable. When true, deploys a GCP-managed
                    validator client alongside the beacon client.
                beacon_fee_recipient (str):
                    An Ethereum address which the beacon client
                    will send fee rewards to if no recipient is
                    configured in the validator client.

                    See
                    https://lighthouse-book.sigmaprime.io/suggested-fee-recipient.html
                    or
                    https://docs.prylabs.network/docs/execution-node/fee-recipient
                    for examples of how this is used.

                    Note that while this is often described as
                    "suggested", as we run the execution node we can
                    trust the execution node, and therefore this is
                    considered enforced.

                    This field is a member of `oneof`_ ``_beacon_fee_recipient``.
            """

            mev_relay_urls: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=1,
            )
            managed_validator_client: bool = proto.Field(
                proto.BOOL,
                number=2,
            )
            beacon_fee_recipient: str = proto.Field(
                proto.STRING,
                number=3,
                optional=True,
            )

        geth_details: "BlockchainNode.EthereumDetails.GethDetails" = proto.Field(
            proto.MESSAGE,
            number=8,
            oneof="execution_client_details",
            message="BlockchainNode.EthereumDetails.GethDetails",
        )
        network: "BlockchainNode.EthereumDetails.Network" = proto.Field(
            proto.ENUM,
            number=1,
            optional=True,
            enum="BlockchainNode.EthereumDetails.Network",
        )
        node_type: "BlockchainNode.EthereumDetails.NodeType" = proto.Field(
            proto.ENUM,
            number=2,
            optional=True,
            enum="BlockchainNode.EthereumDetails.NodeType",
        )
        execution_client: "BlockchainNode.EthereumDetails.ExecutionClient" = (
            proto.Field(
                proto.ENUM,
                number=3,
                optional=True,
                enum="BlockchainNode.EthereumDetails.ExecutionClient",
            )
        )
        consensus_client: "BlockchainNode.EthereumDetails.ConsensusClient" = (
            proto.Field(
                proto.ENUM,
                number=4,
                optional=True,
                enum="BlockchainNode.EthereumDetails.ConsensusClient",
            )
        )
        api_enable_admin: bool = proto.Field(
            proto.BOOL,
            number=5,
            optional=True,
        )
        api_enable_debug: bool = proto.Field(
            proto.BOOL,
            number=6,
            optional=True,
        )
        additional_endpoints: "BlockchainNode.EthereumDetails.EthereumEndpoints" = (
            proto.Field(
                proto.MESSAGE,
                number=7,
                optional=True,
                message="BlockchainNode.EthereumDetails.EthereumEndpoints",
            )
        )
        validator_config: "BlockchainNode.EthereumDetails.ValidatorConfig" = (
            proto.Field(
                proto.MESSAGE,
                number=10,
                optional=True,
                message="BlockchainNode.EthereumDetails.ValidatorConfig",
            )
        )

    ethereum_details: EthereumDetails = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="blockchain_type_details",
        message=EthereumDetails,
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    blockchain_type: BlockchainType = proto.Field(
        proto.ENUM,
        number=5,
        optional=True,
        enum=BlockchainType,
    )
    connection_info: ConnectionInfo = proto.Field(
        proto.MESSAGE,
        number=6,
        message=ConnectionInfo,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=8,
        enum=State,
    )
    private_service_connect_enabled: bool = proto.Field(
        proto.BOOL,
        number=12,
    )


class ListBlockchainNodesRequest(proto.Message):
    r"""Message for requesting list of blockchain nodes.

    Attributes:
        parent (str):
            Required. Parent value for ``ListNodesRequest``.
        page_size (int):
            Requested page size. Server may return fewer
            items than requested. If unspecified, server
            will pick an appropriate default.
        page_token (str):
            A token identifying a page of results the
            server should return.
        filter (str):
            Filtering results.
        order_by (str):
            Hint for how to order the results.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListBlockchainNodesResponse(proto.Message):
    r"""Message for response to listing blockchain nodes.

    Attributes:
        blockchain_nodes (MutableSequence[google.cloud.blockchainnodeengine_v1.types.BlockchainNode]):
            The list of nodes
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    blockchain_nodes: MutableSequence["BlockchainNode"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="BlockchainNode",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetBlockchainNodeRequest(proto.Message):
    r"""Message for getting a blockchain node.

    Attributes:
        name (str):
            Required. The fully qualified name of the blockchain node to
            fetch. e.g.
            ``projects/my-project/locations/us-central1/blockchainNodes/my-node``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateBlockchainNodeRequest(proto.Message):
    r"""Message for creating a blockchain node.

    Attributes:
        parent (str):
            Required. Value for parent.
        blockchain_node_id (str):
            Required. ID of the requesting object.
        blockchain_node (google.cloud.blockchainnodeengine_v1.types.BlockchainNode):
            Required. The resource being created.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    blockchain_node_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    blockchain_node: "BlockchainNode" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="BlockchainNode",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateBlockchainNodeRequest(proto.Message):
    r"""Message for updating a blockchain node.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the Blockchain node resource by the update.
            The fields specified in the ``update_mask`` are relative to
            the resource, not the full request. A field will be
            overwritten if it is in the mask. If the user does not
            provide a mask then all fields will be overwritten.
        blockchain_node (google.cloud.blockchainnodeengine_v1.types.BlockchainNode):
            Required. The resource being updated.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    blockchain_node: "BlockchainNode" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="BlockchainNode",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteBlockchainNodeRequest(proto.Message):
    r"""Message for deleting a blockchain node.

    Attributes:
        name (str):
            Required. The fully qualified name of the blockchain node to
            delete. e.g.
            ``projects/my-project/locations/us-central1/blockchainNodes/my-node``.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have been
            cancelled successfully have ``[Operation.error][]`` value
            with a ``[google.rpc.Status.code][google.rpc.Status.code]``
            of ``1``, corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
