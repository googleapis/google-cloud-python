# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/monitoring/v3/group_service.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
# Manual additions are allowed because the refresh process performs
# a 3-way merge in order to preserve those manual additions. In order to not
# break the refresh process, only certain types of modifications are
# allowed.
#
# Allowed modifications:
# 1. New methods (these should be added to the end of the class)
#
# Happy editing!

from google.gax import PageDescriptor
from google.gax import api_callable
from google.gax import config
from google.gax.path_template import PathTemplate
from google.monitoring.v3 import group_service_pb2
from google.api import monitored_resource_pb2
from google.monitoring.v3 import common_pb2
from google.monitoring.v3 import group_pb2


class GroupServiceApi(object):
    """
    The Group API lets you inspect and manage your
    [groups](google.monitoring.v3.Group).

    A group is a named filter that is used to identify
    a collection of monitored resources. Groups are typically used to
    mirror the physical and/or logical topology of the environment.
    Because group membership is computed dynamically, monitored
    resources that are started in the future are automatically placed
    in matching groups. By using a group to name monitored resources in,
    for example, an alert policy, the target of that alert policy is
    updated automatically as monitored resources are added and removed
    from the infrastructure.
    """

    # The default address of the logging service.
    _SERVICE_ADDRESS = 'monitoring.googleapis.com'

    # The default port of the logging service.
    _DEFAULT_SERVICE_PORT = 443

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = (
        'https://www.googleapis.com/auth/monitoring',
        'https://www.googleapis.com/auth/monitoring.write',
        'https://www.googleapis.com/auth/monitoring.read',
        'https://www.googleapis.com/auth/cloud-platform',
    )

    _LIST_GROUPS_DESCRIPTOR = PageDescriptor(
        'page_token',
        'next_page_token',
        'group',
    )
    _LIST_GROUPS_FOR_RESOURCE_DESCRIPTOR = PageDescriptor(
        'page_token',
        'next_page_token',
        'group',
    )
    _LIST_GROUP_MEMBERS_DESCRIPTOR = PageDescriptor(
        'page_token',
        'next_page_token',
        'members',
    )

    class Templates(object):
        """PathTemplates for resources used by GroupServiceApi."""
        PROJECT = PathTemplate.from_string(
            'projects/{project}')
        GROUP = PathTemplate.from_string(
            'projects/{project}/groups/{group}')

    def __init__(
            self,
            service_path=_SERVICE_ADDRESS,
            port=_DEFAULT_SERVICE_PORT,
            channel=None,
            ssl_creds=None,
            scopes=_ALL_SCOPES,
            is_idempotent_retrying=True,
            max_attempts=3,
            timeout=30):
        self.defaults = api_callable.ApiCallableDefaults(
            timeout=timeout,
            max_attempts=max_attempts,
            is_idempotent_retrying=is_idempotent_retrying)

        self.stub = config.create_stub(
            group_service_pb2.beta_create_GroupService_stub,
            service_path,
            port,
            ssl_creds=ssl_creds,
            channel=channel,
            scopes=scopes)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        del self.stub

    # Service calls
    def list_groups(
            self,
            name='',
            children_of_group='',
            ancestors_of_group='',
            descendants_of_group='',
            **kwargs):
        """
        Lists the existing groups.

        :type name: string
        :type children_of_group: string
        :type ancestors_of_group: string
        :type descendants_of_group: string
        """

        list_groups_request = group_service_pb2.ListGroupsRequest(
            name=name,
            children_of_group=children_of_group,
            ancestors_of_group=ancestors_of_group,
            descendants_of_group=descendants_of_group,
            **kwargs)
        return self.list_groups_callable()(list_groups_request)

    def list_groups_callable(
            self,
            is_retrying=None,
            max_attempts=None,
            page_streaming=_LIST_GROUPS_DESCRIPTOR):
        return api_callable.idempotent_callable(
            self.stub.ListGroups,
            page_streaming=page_streaming,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def list_groups_for_resource(
            self,
            name='',
            monitored_resource=None,
            **kwargs):
        """
        Lists the groups containing a specific monitored resource.

        :type name: string
        :type monitored_resource: monitored_resource_pb2.MonitoredResource
        """
        if monitored_resource is None:
            monitored_resource = monitored_resource_pb2.MonitoredResource()
        list_groups_for_resource_request = group_service_pb2.ListGroupsForResourceRequest(
            name=name,
            monitored_resource=monitored_resource,
            **kwargs)
        return self.list_groups_for_resource_callable()(list_groups_for_resource_request)

    def list_groups_for_resource_callable(
            self,
            is_retrying=None,
            max_attempts=None,
            page_streaming=_LIST_GROUPS_FOR_RESOURCE_DESCRIPTOR):
        return api_callable.idempotent_callable(
            self.stub.ListGroupsForResource,
            page_streaming=page_streaming,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def get_group(
            self,
            name='',
            **kwargs):
        """
        Gets a single group.

        :type name: string
        """

        get_group_request = group_service_pb2.GetGroupRequest(
            name=name,
            **kwargs)
        return self.get_group_callable()(get_group_request)

    def get_group_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.GetGroup,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def create_group(
            self,
            name='',
            group=None,
            validate_only=False,
            **kwargs):
        """
        Creates a new group.

        :type name: string
        :type group: group_pb2.Group
        :type validate_only: bool
        """
        if group is None:
            group = group_pb2.Group()
        create_group_request = group_service_pb2.CreateGroupRequest(
            name=name,
            group=group,
            validate_only=validate_only,
            **kwargs)
        return self.create_group_callable()(create_group_request)

    def create_group_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.CreateGroup,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def update_group(
            self,
            group=None,
            validate_only=False,
            **kwargs):
        """
        Updates an existing group.
        You can change any group attributes except `name`.

        :type group: group_pb2.Group
        :type validate_only: bool
        """
        if group is None:
            group = group_pb2.Group()
        update_group_request = group_service_pb2.UpdateGroupRequest(
            group=group,
            validate_only=validate_only,
            **kwargs)
        return self.update_group_callable()(update_group_request)

    def update_group_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.UpdateGroup,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def delete_group(
            self,
            name='',
            **kwargs):
        """
        Deletes an existing group.

        :type name: string
        """

        delete_group_request = group_service_pb2.DeleteGroupRequest(
            name=name,
            **kwargs)
        return self.delete_group_callable()(delete_group_request)

    def delete_group_callable(
            self,
            is_retrying=None,
            max_attempts=None):
        return api_callable.idempotent_callable(
            self.stub.DeleteGroup,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    def list_group_members(
            self,
            name='',
            filter_='',
            interval=None,
            **kwargs):
        """
        Lists the monitored resources that are members of a group.

        :type name: string
        :type filter: string
        :type interval: common_pb2.TimeInterval
        """
        if interval is None:
            interval = common_pb2.TimeInterval()
        list_group_members_request = group_service_pb2.ListGroupMembersRequest(
            name=name,
            filter=filter_,
            interval=interval,
            **kwargs)
        return self.list_group_members_callable()(list_group_members_request)

    def list_group_members_callable(
            self,
            is_retrying=None,
            max_attempts=None,
            page_streaming=_LIST_GROUP_MEMBERS_DESCRIPTOR):
        return api_callable.idempotent_callable(
            self.stub.ListGroupMembers,
            page_streaming=page_streaming,
            is_retrying=is_retrying,
            max_attempts=max_attempts,
            defaults=self.defaults)

    # ========
    # Manually-added methods: add custom (non-generated) methods after this point.
    # ========