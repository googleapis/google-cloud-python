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


import datetime
import warnings

import six

from gcloud.bigtable.client import Client
from gcloud.bigtable.column_family import GCRuleIntersection
from gcloud.bigtable.column_family import MaxAgeGCRule
from gcloud.bigtable.column_family import MaxVersionsGCRule
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
_DISABLE_DELETE_MSG = ('The disable argument should not be used in '
                       'delete_table(). Cloud Bigtable has no concept '
                       'of enabled / disabled tables.')


def _get_cluster(timeout=None):
    """Gets cluster for the default project.

    Creates a client with the inferred credentials and project ID from
    the local environment. Then uses
    :meth:`.bigtable.client.Client.list_clusters` to
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
        :class:`Client <gcloud.bigtable.client.Client>` that created the
        :class:`Cluster <gcloud.bigtable.cluster.Cluster>` instance and the
        :class:`Credentials <oauth2client.client.Credentials>` stored on the
        client.

    The arguments ``host``, ``port``, ``compat``, ``transport`` and
    ``protocol`` are allowed (as keyword arguments) for compatibility with
    HappyBase. However, they will not be used in any way, and will cause a
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

    :type cluster: :class:`Cluster <gcloud.bigtable.cluster.Cluster>`
    :param cluster: (Optional) A Cloud Bigtable cluster. The instance also
                    owns a client for making gRPC requests to the Cloud
                    Bigtable API. If not passed in, defaults to creating client
                    with ``admin=True`` and using the ``timeout`` here for the
                    ``timeout_seconds`` argument to the
                    :class:`Client <gcloud.bigtable.client.Client>`
                    constructor. The credentials for the client
                    will be the implicit ones loaded from the environment.
                    Then that client is used to retrieve all the clusters
                    owned by the client's project.

    :type kwargs: dict
    :param kwargs: Remaining keyword arguments. Provided for HappyBase
                   compatibility.
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
        :class:`Client <gcloud.bigtable.client.Client>` bound to the
        :class:`Cluster <gcloud.bigtable.cluster.Cluster>` owned by
        this connection.
        """
        self._cluster._client.start()

    def close(self):
        """Close the underlying transport to Cloud Bigtable.

        This method closes the underlying HTTP/2 gRPC connection using a
        :class:`Client <gcloud.bigtable.client.Client>` bound to the
        :class:`Cluster <gcloud.bigtable.cluster.Cluster>` owned by
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

        :rtype: :class:`Table <gcloud.bigtable.happybase.table.Table>`
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

    def create_table(self, name, families):
        """Create a table.

        .. warning::

            The only column family options from HappyBase that are able to be
            used with Cloud Bigtable are ``max_versions`` and ``time_to_live``.

        .. note::

            This method is **not** atomic. The Cloud Bigtable API separates
            the creation of a table from the creation of column families. Thus
            this method needs to send 1 request for the table creation and 1
            request for each column family. If any of these fails, the method
            will fail, but the progress made towards completion cannot be
            rolled back.

        Values in ``families`` represent column family options. In HappyBase,
        these are dictionaries, corresponding to the ``ColumnDescriptor``
        structure in the Thrift API. The accepted keys are:

        * ``max_versions`` (``int``)
        * ``compression`` (``str``)
        * ``in_memory`` (``bool``)
        * ``bloom_filter_type`` (``str``)
        * ``bloom_filter_vector_size`` (``int``)
        * ``bloom_filter_nb_hashes`` (``int``)
        * ``block_cache_enabled`` (``bool``)
        * ``time_to_live`` (``int``)

        :type name: str
        :param name: The name of the table to be created.

        :type families: dict
        :param families: Dictionary with column family names as keys and column
                         family options as the values. The options can be among

                         * :class:`dict`
                         * :class:`.GarbageCollectionRule`

        :raises: :class:`TypeError <exceptions.TypeError>` if ``families`` is
                 not a dictionary,
                 :class:`ValueError <exceptions.ValueError>` if ``families``
                 has no entries
        """
        if not isinstance(families, dict):
            raise TypeError('families arg must be a dictionary')

        if not families:
            raise ValueError('Cannot create table %r (no column '
                             'families specified)' % (name,))

        # Parse all keys before making any API requests.
        gc_rule_dict = {}
        for column_family_name, option in families.items():
            if isinstance(column_family_name, six.binary_type):
                column_family_name = column_family_name.decode('utf-8')
            if column_family_name.endswith(':'):
                column_family_name = column_family_name[:-1]
            gc_rule_dict[column_family_name] = _parse_family_option(option)

        # Create table instance and then make API calls.
        name = self._table_name(name)
        low_level_table = _LowLevelTable(name, self._cluster)
        low_level_table.create()

        for column_family_name, gc_rule in gc_rule_dict.items():
            column_family = low_level_table.column_family(
                column_family_name, gc_rule=gc_rule)
            column_family.create()

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
        """
        if disable:
            _WARN(_DISABLE_DELETE_MSG)

        name = self._table_name(name)
        _LowLevelTable(name, self._cluster).delete()

    def enable_table(self, name):
        """Enable the specified table.

        .. warning::

            Cloud Bigtable has no concept of enabled / disabled tables so this
            method does not work. It is provided simply for compatibility.

        :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
                 always
        """
        raise NotImplementedError('The Cloud Bigtable API has no concept of '
                                  'enabled or disabled tables.')

    def disable_table(self, name):
        """Disable the specified table.

        .. warning::

            Cloud Bigtable has no concept of enabled / disabled tables so this
            method does not work. It is provided simply for compatibility.

        :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
                 always
        """
        raise NotImplementedError('The Cloud Bigtable API has no concept of '
                                  'enabled or disabled tables.')

    def is_table_enabled(self, name):
        """Return whether the specified table is enabled.

        .. warning::

            Cloud Bigtable has no concept of enabled / disabled tables so this
            method does not work. It is provided simply for compatibility.

        :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
                 always
        """
        raise NotImplementedError('The Cloud Bigtable API has no concept of '
                                  'enabled or disabled tables.')

    def compact_table(self, name, major=False):
        """Compact the specified table.

        .. warning::

            Cloud Bigtable does not support compacting a table, so this
            method does not work. It is provided simply for compatibility.

        :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
                 always
        """
        raise NotImplementedError('The Cloud Bigtable API does not support '
                                  'compacting a table.')


def _parse_family_option(option):
    """Parses a column family option into a garbage collection rule.

    .. note::

        If ``option`` is not a dictionary, the type is not checked.
        If ``option`` is :data:`None`, there is nothing to do, since this
        is the correct output.

    :type option: :class:`dict`,
                  :data:`NoneType <types.NoneType>`,
                  :class:`.GarbageCollectionRule`
    :param option: A column family option passes as a dictionary value in
                   :meth:`Connection.create_table`.

    :rtype: :class:`.GarbageCollectionRule`
    :returns: A garbage collection rule parsed from the input.
    """
    result = option
    if isinstance(result, dict):
        if not set(result.keys()) <= set(['max_versions', 'time_to_live']):
            all_keys = ', '.join(repr(key) for key in result.keys())
            warning_msg = ('Cloud Bigtable only supports max_versions and '
                           'time_to_live column family settings. '
                           'Received: %s' % (all_keys,))
            _WARN(warning_msg)

        max_num_versions = result.get('max_versions')
        max_age = None
        if 'time_to_live' in result:
            max_age = datetime.timedelta(seconds=result['time_to_live'])

        versions_rule = age_rule = None
        if max_num_versions is not None:
            versions_rule = MaxVersionsGCRule(max_num_versions)
        if max_age is not None:
            age_rule = MaxAgeGCRule(max_age)

        if versions_rule is None:
            result = age_rule
        else:
            if age_rule is None:
                result = versions_rule
            else:
                result = GCRuleIntersection(rules=[age_rule, versions_rule])

    return result
