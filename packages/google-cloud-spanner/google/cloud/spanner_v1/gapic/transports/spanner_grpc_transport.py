# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

import pkg_resources
import grpc_gcp

import google.api_core.grpc_helpers

from google.cloud.spanner_v1.proto import spanner_pb2_grpc


_SPANNER_GRPC_CONFIG = "spanner.grpc.config"


class SpannerGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.spanner.v1 Spanner API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/spanner.data",
    )

    def __init__(
        self, channel=None, credentials=None, address="spanner.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(address=address, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {"spanner_stub": spanner_pb2_grpc.SpannerStub(channel)}

    @classmethod
    def create_channel(cls, address="spanner.googleapis.com:443", credentials=None):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        grpc_gcp_config = grpc_gcp.api_config_from_text_pb(
            pkg_resources.resource_string(__name__, _SPANNER_GRPC_CONFIG)
        )
        options = [(grpc_gcp.API_CONFIG_CHANNEL_ARG, grpc_gcp_config)]
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def create_session(self):
        """Return the gRPC stub for :meth:`SpannerClient.create_session`.

        Creates a new session. A session can be used to perform transactions
        that read and/or modify data in a Cloud Spanner database. Sessions are
        meant to be reused for many consecutive transactions.

        Sessions can only execute one transaction at a time. To execute multiple
        concurrent read-write/write-only transactions, create multiple sessions.
        Note that standalone reads and queries use a transaction internally, and
        count toward the one transaction limit.

        Cloud Spanner limits the number of sessions that can exist at any given
        time; thus, it is a good idea to delete idle and/or unneeded sessions.
        Aside from explicit deletes, Cloud Spanner can delete sessions for which
        no operations are sent for more than an hour. If a session is deleted,
        requests to it return ``NOT_FOUND``.

        Idle sessions can be kept alive by sending a trivial SQL query
        periodically, e.g., ``"SELECT 1"``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].CreateSession

    @property
    def get_session(self):
        """Return the gRPC stub for :meth:`SpannerClient.get_session`.

        Gets a session. Returns ``NOT_FOUND`` if the session does not exist.
        This is mainly useful for determining whether a session is still alive.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].GetSession

    @property
    def list_sessions(self):
        """Return the gRPC stub for :meth:`SpannerClient.list_sessions`.

        Lists all sessions in a given database.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].ListSessions

    @property
    def delete_session(self):
        """Return the gRPC stub for :meth:`SpannerClient.delete_session`.

        Ends a session, releasing server resources associated with it.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].DeleteSession

    @property
    def execute_sql(self):
        """Return the gRPC stub for :meth:`SpannerClient.execute_sql`.

        Executes an SQL statement, returning all results in a single reply. This
        method cannot be used to return a result set larger than 10 MiB; if the
        query yields more data than that, the query fails with a
        ``FAILED_PRECONDITION`` error.

        Operations inside read-write transactions might return ``ABORTED``. If
        this occurs, the application should restart the transaction from the
        beginning. See ``Transaction`` for more details.

        Larger result sets can be fetched in streaming fashion by calling
        ``ExecuteStreamingSql`` instead.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].ExecuteSql

    @property
    def execute_streaming_sql(self):
        """Return the gRPC stub for :meth:`SpannerClient.execute_streaming_sql`.

        Like ``ExecuteSql``, except returns the result set as a stream. Unlike
        ``ExecuteSql``, there is no limit on the size of the returned result
        set. However, no individual row in the result set can exceed 100 MiB,
        and no column value can exceed 10 MiB.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].ExecuteStreamingSql

    @property
    def read(self):
        """Return the gRPC stub for :meth:`SpannerClient.read`.

        Reads rows from the database using key lookups and scans, as a simple
        key/value style alternative to ``ExecuteSql``. This method cannot be
        used to return a result set larger than 10 MiB; if the read matches more
        data than that, the read fails with a ``FAILED_PRECONDITION`` error.

        Reads inside read-write transactions might return ``ABORTED``. If this
        occurs, the application should restart the transaction from the
        beginning. See ``Transaction`` for more details.

        Larger result sets can be yielded in streaming fashion by calling
        ``StreamingRead`` instead.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].Read

    @property
    def streaming_read(self):
        """Return the gRPC stub for :meth:`SpannerClient.streaming_read`.

        Like ``Read``, except returns the result set as a stream. Unlike
        ``Read``, there is no limit on the size of the returned result set.
        However, no individual row in the result set can exceed 100 MiB, and no
        column value can exceed 10 MiB.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].StreamingRead

    @property
    def begin_transaction(self):
        """Return the gRPC stub for :meth:`SpannerClient.begin_transaction`.

        Begins a new transaction. This step can often be skipped: ``Read``,
        ``ExecuteSql`` and ``Commit`` can begin a new transaction as a
        side-effect.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].BeginTransaction

    @property
    def commit(self):
        """Return the gRPC stub for :meth:`SpannerClient.commit`.

        Commits a transaction. The request includes the mutations to be applied
        to rows in the database.

        ``Commit`` might return an ``ABORTED`` error. This can occur at any
        time; commonly, the cause is conflicts with concurrent transactions.
        However, it can also happen for a variety of other reasons. If
        ``Commit`` returns ``ABORTED``, the caller should re-attempt the
        transaction from the beginning, re-using the same session.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].Commit

    @property
    def rollback(self):
        """Return the gRPC stub for :meth:`SpannerClient.rollback`.

        Rolls back a transaction, releasing any locks it holds. It is a good
        idea to call this for any transaction that includes one or more ``Read``
        or ``ExecuteSql`` requests and ultimately decides not to commit.

        ``Rollback`` returns ``OK`` if it successfully aborts the transaction,
        the transaction was already aborted, or the transaction is not found.
        ``Rollback`` never returns ``ABORTED``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].Rollback

    @property
    def partition_query(self):
        """Return the gRPC stub for :meth:`SpannerClient.partition_query`.

        Creates a set of partition tokens that can be used to execute a query
        operation in parallel. Each of the returned partition tokens can be used
        by ``ExecuteStreamingSql`` to specify a subset of the query result to
        read. The same session and read-only transaction must be used by the
        PartitionQueryRequest used to create the partition tokens and the
        ExecuteSqlRequests that use the partition tokens.

        Partition tokens become invalid when the session used to create them is
        deleted, is idle for too long, begins a new transaction, or becomes too
        old. When any of these happen, it is not possible to resume the query,
        and the whole operation must be restarted from the beginning.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].PartitionQuery

    @property
    def partition_read(self):
        """Return the gRPC stub for :meth:`SpannerClient.partition_read`.

        Creates a set of partition tokens that can be used to execute a read
        operation in parallel. Each of the returned partition tokens can be used
        by ``StreamingRead`` to specify a subset of the read result to read. The
        same session and read-only transaction must be used by the
        PartitionReadRequest used to create the partition tokens and the
        ReadRequests that use the partition tokens. There are no ordering
        guarantees on rows returned among the returned partition tokens, or even
        within each individual StreamingRead call issued with a
        partition\_token.

        Partition tokens become invalid when the session used to create them is
        deleted, is idle for too long, begins a new transaction, or becomes too
        old. When any of these happen, it is not possible to resume the read,
        and the whole operation must be restarted from the beginning.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["spanner_stub"].PartitionRead
