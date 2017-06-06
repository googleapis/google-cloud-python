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

"""Parent client for calling the Cloud Spanner API.

This is the base from which all interactions with the API occur.

In the hierarchy of API concepts

* a :class:`~google.cloud.spanner.client.Client` owns an
  :class:`~google.cloud.spanner.instance.Instance`
* a :class:`~google.cloud.spanner.instance.Instance` owns a
  :class:`~google.cloud.spanner.database.Database`
"""

import google.auth.credentials
from google.gax import INITIAL_PAGE
# pylint: disable=line-too-long
from google.cloud.gapic.spanner_admin_database.v1.database_admin_client import (  # noqa
    DatabaseAdminClient)
from google.cloud.gapic.spanner_admin_instance.v1.instance_admin_client import (  # noqa
    InstanceAdminClient)
# pylint: enable=line-too-long

from google.cloud._http import DEFAULT_USER_AGENT
from google.cloud.client import _ClientFactoryMixin
from google.cloud.client import _ClientProjectMixin
from google.cloud.credentials import get_credentials
from google.cloud.iterator import GAXIterator
from google.cloud.spanner import __version__
from google.cloud.spanner._helpers import _options_with_prefix
from google.cloud.spanner.instance import DEFAULT_NODE_COUNT
from google.cloud.spanner.instance import Instance

SPANNER_ADMIN_SCOPE = 'https://www.googleapis.com/auth/spanner.admin'


class InstanceConfig(object):
    """Named configurations for Spanner instances.

    :type name: str
    :param name: ID of the instance configuration

    :type display_name: str
    :param display_name: Name of the instance configuration
    """
    def __init__(self, name, display_name):
        self.name = name
        self.display_name = display_name

    @classmethod
    def from_pb(cls, config_pb):
        """Construct an instance from the equvalent protobuf.

        :type config_pb:
          :class:`~google.spanner.v1.spanner_instance_admin_pb2.InstanceConfig`
        :param config_pb: the protobuf to parse

        :rtype: :class:`InstanceConfig`
        :returns: an instance of this class
        """
        return cls(config_pb.name, config_pb.display_name)


class Client(_ClientFactoryMixin, _ClientProjectMixin):
    """Client for interacting with Cloud Spanner API.

    .. note::

        Since the Cloud Spanner API requires the gRPC transport, no
        ``http`` argument is accepted by this class.

    :type project: :class:`str` or :func:`unicode <unicode>`
    :param project: (Optional) The ID of the project which owns the
                    instances, tables and data. If not provided, will
                    attempt to determine from the environment.

    :type credentials:
        :class:`OAuth2Credentials <oauth2client.client.OAuth2Credentials>` or
        :data:`NoneType <types.NoneType>`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not provided, defaults to the Google
                        Application Default Credentials.

    :type user_agent: str
    :param user_agent: (Optional) The user agent to be used with API request.
                       Defaults to :const:`DEFAULT_USER_AGENT`.

    :raises: :class:`ValueError <exceptions.ValueError>` if both ``read_only``
             and ``admin`` are :data:`True`
    """
    _instance_admin_api = None
    _database_admin_api = None
    _SET_PROJECT = True  # Used by from_service_account_json()

    def __init__(self, project=None, credentials=None,
                 user_agent=DEFAULT_USER_AGENT):

        _ClientProjectMixin.__init__(self, project=project)
        if credentials is None:
            credentials = get_credentials()

        scopes = [
            SPANNER_ADMIN_SCOPE,
        ]

        credentials = google.auth.credentials.with_scopes_if_required(
            credentials, scopes)

        self._credentials = credentials
        self.user_agent = user_agent

    @property
    def credentials(self):
        """Getter for client's credentials.

        :rtype:
            :class:`OAuth2Credentials <oauth2client.client.OAuth2Credentials>`
        :returns: The credentials stored on the client.
        """
        return self._credentials

    @property
    def project_name(self):
        """Project name to be used with Spanner APIs.

        .. note::

            This property will not change if ``project`` does not, but the
            return value is not cached.

        The project name is of the form

            ``"projects/{project}"``

        :rtype: str
        :returns: The project name to be used with the Cloud Spanner Admin
                  API RPC service.
        """
        return 'projects/' + self.project

    @property
    def instance_admin_api(self):
        """Helper for session-related API calls."""
        if self._instance_admin_api is None:
            self._instance_admin_api = InstanceAdminClient(
                credentials=self.credentials,
                lib_name='gccl',
                lib_version=__version__,
            )
        return self._instance_admin_api

    @property
    def database_admin_api(self):
        """Helper for session-related API calls."""
        if self._database_admin_api is None:
            self._database_admin_api = DatabaseAdminClient(
                credentials=self.credentials,
                lib_name='gccl',
                lib_version=__version__,
            )
        return self._database_admin_api

    def copy(self):
        """Make a copy of this client.

        Copies the local data stored as simple types but does not copy the
        current state of any open connections with the Cloud Bigtable API.

        :rtype: :class:`.Client`
        :returns: A copy of the current client.
        """
        credentials = self._credentials
        copied_creds = credentials.create_scoped(credentials.scopes)
        return self.__class__(
            self.project,
            copied_creds,
            self.user_agent,
        )

    def list_instance_configs(self, page_size=None, page_token=None):
        """List available instance configurations for the client's project.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.database.v1#google.spanner.admin.database.v1.InstanceAdmin.ListInstanceConfigs

        :type page_size: int
        :param page_size: (Optional) Maximum number of results to return.

        :type page_token: str
        :param page_token: (Optional) Token for fetching next page of results.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns:
            Iterator of
            :class:`~google.cloud.spanner.instance.InstanceConfig`
            resources within the client's project.
        """
        if page_token is None:
            page_token = INITIAL_PAGE
        options = _options_with_prefix(self.project_name,
                                       page_token=page_token)
        path = 'projects/%s' % (self.project,)
        page_iter = self.instance_admin_api.list_instance_configs(
            path, page_size=page_size, options=options)
        return GAXIterator(self, page_iter, _item_to_instance_config)

    def instance(self, instance_id,
                 configuration_name=None,
                 display_name=None,
                 node_count=DEFAULT_NODE_COUNT):
        """Factory to create a instance associated with this client.

        :type instance_id: str
        :param instance_id: The ID of the instance.

        :type configuration_name: string
        :param configuration_name:
           (Optional) Name of the instance configuration used to set up the
           instance's cluster, in the form:
           ``projects/<project>/instanceConfigs/<config>``.
           **Required** for instances which do not yet exist.

        :type display_name: str
        :param display_name: (Optional) The display name for the instance in
                             the Cloud Console UI. (Must be between 4 and 30
                             characters.) If this value is not set in the
                             constructor, will fall back to the instance ID.

        :type node_count: int
        :param node_count: (Optional) The number of nodes in the instance's
                            cluster; used to set up the instance's cluster.

        :rtype: :class:`~google.cloud.spanner.instance.Instance`
        :returns: an instance owned by this client.
        """
        return Instance(
            instance_id, self, configuration_name, node_count, display_name)

    def list_instances(self, filter_='', page_size=None, page_token=None):
        """List instances for the client's project.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.database.v1#google.spanner.admin.database.v1.InstanceAdmin.ListInstances

        :type filter_: string
        :param filter_: (Optional) Filter to select instances listed.  See
                        the ``ListInstancesRequest`` docs above for examples.

        :type page_size: int
        :param page_size: (Optional) Maximum number of results to return.

        :type page_token: str
        :param page_token: (Optional) Token for fetching next page of results.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns:
            Iterator of :class:`~google.cloud.spanner.instance.Instance`
            resources within the client's project.
        """
        if page_token is None:
            page_token = INITIAL_PAGE
        options = _options_with_prefix(self.project_name,
                                       page_token=page_token)
        path = 'projects/%s' % (self.project,)
        page_iter = self.instance_admin_api.list_instances(
            path, filter_=filter_, page_size=page_size, options=options)
        return GAXIterator(self, page_iter, _item_to_instance)


def _item_to_instance_config(
        iterator, config_pb):  # pylint: disable=unused-argument
    """Convert an instance config protobuf to the native object.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type config_pb:
        :class:`~google.spanner.admin.instance.v1.InstanceConfig`
    :param config_pb: An instance config returned from the API.

    :rtype: :class:`~google.cloud.spanner.instance.InstanceConfig`
    :returns: The next instance config in the page.
    """
    return InstanceConfig.from_pb(config_pb)


def _item_to_instance(iterator, instance_pb):
    """Convert an instance protobuf to the native object.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type instance_pb: :class:`~google.spanner.admin.instance.v1.Instance`
    :param instance_pb: An instance returned from the API.

    :rtype: :class:`~google.cloud.spanner.instance.Instance`
    :returns: The next instance in the page.
    """
    return Instance.from_pb(instance_pb, iterator.client)
