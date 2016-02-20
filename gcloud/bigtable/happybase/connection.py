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

"""Google Cloud Bigtable HappyBase connection module."""


import warnings

import six

from gcloud.bigtable.client import Client
from gcloud.bigtable.happybase.table import Table
from gcloud.bigtable.table import Table as _LowLevelTable


# Constants reproduced here for HappyBase compatibility, though values
# are all null.
COMPAT_MODES = None
THRIFT_TRANSPORTS = None
THRIFT_PROTOCOLS = None
DEFAULT_HOST = None
DEFAULT_PORT = None
DEFAULT_TRANSPORT = None
DEFAULT_COMPAT = None
DEFAULT_PROTOCOL = None

_LEGACY_ARGS = frozenset(('host', 'port', 'compat', 'transport', 'protocol'))
_WARN = warnings.warn


def _get_cluster(timeout=None):
    """Gets cluster for the default project.

    Creates a client with the inferred credentials and project ID from
    the local environment. Then uses :meth:`.Client.list_clusters` to
    get the unique cluster owned by the project.

    If the request fails for any reason, or if there isn't exactly one cluster
    owned by the project, then this function will fail.

    :type timeout: int
    :param timeout: (Optional) The socket timeout in milliseconds.

    :rtype: :class:`gcloud.bigtable.cluster.Cluster`
    :returns: The unique cluster owned by the project inferred from
              the environment.
    :raises: :class:`ValueError <exceptions.ValueError>` if there is a failed
             zone or any number of clusters other than one.
    """
    client_kwargs = {'admin': True}
    if timeout is not None:
        client_kwargs['timeout_seconds'] = timeout / 1000.0
    client = Client(**client_kwargs)
    try:
        client.start()
        clusters, failed_zones = client.list_clusters()
    finally:
        client.stop()

    if len(failed_zones) != 0:
        raise ValueError('Determining cluster via ListClusters encountered '
                         'failed zones.')
    if len(clusters) == 0:
        raise ValueError('This client doesn\'t have access to any clusters.')
    if len(clusters) > 1:
        raise ValueError('This client has access to more than one cluster. '
                         'Please directly pass the cluster you\'d '
                         'like to use.')
    return clusters[0]


class Connection(object):
    """Connection to Cloud Bigtable backend.

    .. note::

        If you pass a ``cluster``, it will be :meth:`.Cluster.copy`-ed before
        being stored on the new connection. This also copies the
        :class:`.Client` that created the :class:`.Cluster` instance and the
        :class:`Credentials <oauth2client.client.Credentials>` stored on the
        client.

    The arguments ``host``, ``port``, ``compat``, ``transport`` and
    ``protocol`` are allowed (as keyword arguments) for compatibility with
    HappyBase. However, they will not be used in anyway, and will cause a
    warning if passed.

    :type timeout: int
    :param timeout: (Optional) The socket timeout in milliseconds.

    :type autoconnect: bool
    :param autoconnect: (Optional) Whether the connection should be
                        :meth:`open`-ed during construction.

    :type table_prefix: str
    :param table_prefix: (Optional) Prefix used to construct table names.

    :type table_prefix_separator: str
    :param table_prefix_separator: (Optional) Separator used with
                                   ``table_prefix``. Defaults to ``_``.

    :type cluster: :class:`gcloud.bigtable.cluster.Cluster`
    :param cluster: (Optional) A Cloud Bigtable cluster. The instance also
                    owns a client for making gRPC requests to the Cloud
                    Bigtable API. If not passed in, defaults to creating client
                    with ``admin=True`` and using the ``timeout`` here for the
                    ``timeout_seconds`` argument to the :class:`.Client``
                    constructor. The credentials for the client
                    will be the implicit ones loaded from the environment.
                    Then that client is used to retrieve all the clusters
                    owned by the client's project.

    :type kwargs: dict
    :param kwargs: Remaining keyword arguments. Provided for HappyBase
                   compatibility.

    :raises: :class:`ValueError <exceptions.ValueError>` if any of the unused
             parameters are specified with a value other than the defaults.
    """

    _cluster = None

    def __init__(self, timeout=None, autoconnect=True, table_prefix=None,
                 table_prefix_separator='_', cluster=None, **kwargs):
        self._handle_legacy_args(kwargs)
        if table_prefix is not None:
            if not isinstance(table_prefix, six.string_types):
                raise TypeError('table_prefix must be a string', 'received',
                                table_prefix, type(table_prefix))

        if not isinstance(table_prefix_separator, six.string_types):
            raise TypeError('table_prefix_separator must be a string',
                            'received', table_prefix_separator,
                            type(table_prefix_separator))

        self.table_prefix = table_prefix
        self.table_prefix_separator = table_prefix_separator

        if cluster is None:
            self._cluster = _get_cluster(timeout=timeout)
        else:
            if timeout is not None:
                raise ValueError('Timeout cannot be used when an existing '
                                 'cluster is passed')
            self._cluster = cluster.copy()

        if autoconnect:
            self.open()

        self._initialized = True

    @staticmethod
    def _handle_legacy_args(arguments_dict):
        """Check legacy HappyBase arguments and warn if set.

        :type arguments_dict: dict
        :param arguments_dict: Unused keyword arguments.

        :raises: :class:`TypeError <exceptions.TypeError>` if a keyword other
                 than ``host``, ``port``, ``compat``, ``transport`` or
                 ``protocol`` is used.
        """
        common_args = _LEGACY_ARGS.intersection(six.iterkeys(arguments_dict))
        if common_args:
            all_args = ', '.join(common_args)
            message = ('The HappyBase legacy arguments %s were used. These '
                       'arguments are unused by gcloud.' % (all_args,))
            _WARN(message)
        for arg_name in common_args:
            arguments_dict.pop(arg_name)
        if arguments_dict:
            unexpected_names = arguments_dict.keys()
            raise TypeError('Received unexpected arguments', unexpected_names)

    def open(self):
        """Open the underlying transport to Cloud Bigtable.

        This method opens the underlying HTTP/2 gRPC connection using a
        :class:`.Client` bound to the :class:`.Cluster` owned by
        this connection.
        """
        self._cluster._client.start()

    def close(self):
        """Close the underlying transport to Cloud Bigtable.

        This method closes the underlying HTTP/2 gRPC connection using a
        :class:`.Client` bound to the :class:`.Cluster` owned by
        this connection.
        """
        self._cluster._client.stop()

    def __del__(self):
        if self._cluster is not None:
            self.close()

    def _table_name(self, name):
        """Construct a table name by optionally adding a table name prefix.

        :type name: str
        :param name: The name to have a prefix added to it.

        :rtype: str
        :returns: The prefixed name, if the current connection has a table
                  prefix set.
        """
        if self.table_prefix is None:
            return name

        return self.table_prefix + self.table_prefix_separator + name

    def table(self, name, use_prefix=True):
        """Table factory.

        :type name: str
        :param name: The name of the table to be created.

        :type use_prefix: bool
        :param use_prefix: Whether to use the table prefix (if any).

        :rtype: `Table <gcloud.bigtable.happybase.table.Table>`
        :returns: Table instance owned by this connection.
        """
        if use_prefix:
            name = self._table_name(name)
        return Table(name, self)

    def tables(self):
        """Return a list of table names available to this connection.

        .. note::

            This lists every table in the cluster owned by this connection,
            **not** every table that a given user may have access to.

        .. note::

            If ``table_prefix`` is set on this connection, only returns the
            table names which match that prefix.

        :rtype: list
        :returns: List of string table names.
        """
        low_level_table_instances = self._cluster.list_tables()
        table_names = [table_instance.table_id
                       for table_instance in low_level_table_instances]

        # Filter using prefix, and strip prefix from names
        if self.table_prefix is not None:
            prefix = self._table_name('')
            offset = len(prefix)
            table_names = [name[offset:] for name in table_names
                           if name.startswith(prefix)]

        return table_names

    def delete_table(self, name, disable=False):
        """Delete the specified table.

        :type name: str
        :param name: The name of the table to be deleted. If ``table_prefix``
                     is set, a prefix will be added to the ``name``.

        :type disable: bool
        :param disable: Whether to first disable the table if needed. This
                        is provided for compatibility with HappyBase, but is
                        not relevant for Cloud Bigtable since it has no concept
                        of enabled / disabled tables.

        :raises: :class:`ValueError <exceptions.ValueError>`
                 if ``disable=True``.
        """
        if disable:
            raise ValueError('The disable argument should not be used in '
                             'delete_table(). Cloud Bigtable has no concept '
                             'of enabled / disabled tables.')

        name = self._table_name(name)
        _LowLevelTable(name, self._cluster).delete()

    def enable_table(self, name):
        """Enable the specified table.

        Cloud Bigtable has no concept of enabled / disabled tables so this
        method does not work. It is provided simply for compatibility.

        :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
                 always
        """
        raise NotImplementedError('The Cloud Bigtable API has no concept of '
                                  'enabled or disabled tables.')

    def disable_table(self, name):
        """Disable the specified table.

        Cloud Bigtable has no concept of enabled / disabled tables so this
        method does not work. It is provided simply for compatibility.

        :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
                 always
        """
        raise NotImplementedError('The Cloud Bigtable API has no concept of '
                                  'enabled or disabled tables.')

    def is_table_enabled(self, name):
        """Return whether the specified table is enabled.

        Cloud Bigtable has no concept of enabled / disabled tables so this
        method does not work. It is provided simply for compatibility.

        :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
                 always
        """
        raise NotImplementedError('The Cloud Bigtable API has no concept of '
                                  'enabled or disabled tables.')

    def compact_table(self, name, major=False):
        """Compact the specified table.

        Cloud Bigtable does not support compacting a table, so this
        method does not work. It is provided simply for compatibility.

        :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
                 always
        """
        raise NotImplementedError('The Cloud Bigtable API does not support '
                                  'compacting a table.')
