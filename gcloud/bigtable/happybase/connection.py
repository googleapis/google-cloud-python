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

        self.autoconnect = autoconnect
        self.table_prefix = table_prefix
        self.table_prefix_separator = table_prefix_separator

        if cluster is None:
            self._cluster = _get_cluster(timeout=timeout)
        else:
            if timeout is not None:
                raise ValueError('Timeout cannot be used when an existing '
                                 'cluster is passed')
            self._cluster = cluster.copy()

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
