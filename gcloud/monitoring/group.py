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

"""Groups for the `Google Stackdriver Monitoring API (V3)`_.

.. _Google Stackdriver Monitoring API (V3):
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
    projects.groups
"""

import re

from gcloud._helpers import _name_from_project_path
from gcloud.monitoring._helpers import _format_timestamp
from gcloud.monitoring.resource import Resource


_GROUP_TEMPLATE = re.compile(r"""
    projects/            # static prefix
    (?P<project>[^/]+)   # initial letter, wordchars + hyphen
    /groups/             # static midfix
    (?P<name>[^/]+)      # initial letter, wordchars + allowed punc
""", re.VERBOSE)


def group_id_from_path(path, project=None):
    """Validate a group URI path and get the group ID.

    :type path: string
    :param path: URI path for a group API request.

    :type project: string or None
    :param project: The project associated with the request. It is
                    included for validation purposes.

    :rtype: string
    :returns: Group ID parsed from ``path``.
    :raises: :class:`ValueError` if the ``path`` is ill-formed or if
             the project from the ``path`` does not agree with the
             ``project`` passed in.
    """
    if not path:
        return ''
    return _name_from_project_path(path, project, _GROUP_TEMPLATE)


class Group(object):
    """A dynamic collection of monitored resources.

    :type client: :class:`gcloud.monitoring.client.Client`
    :param client: A client for operating on the metric descriptor.

    :type name: string
    :param name:
          The fully qualified name of the group in the format
          "projects/<project>/groups/<id>". This is a read-only property.

    :type display_name: string
    :param display_name:
        A user-assigned name for this group, used only for display purposes.

    :type parent_name: string
    :param parent_name:
        The fully qualified name of the group's parent, if it has one.

    :type filter_string: string
    :param filter_string:
        The filter string used to determine which monitored resources belong to
        this group.

    :type is_cluster: boolean
    :param is_cluster:
        If true, the members of this group are considered to be a cluster. The
        system can perform additional analysis on groups that are clusters.
    """
    def __init__(self, client, name=None, display_name='', parent_name='',
                 filter_string='', is_cluster=False):
        self.client = client
        self.name = name
        self.display_name = display_name
        self.parent_name = parent_name
        self.filter = filter_string
        self.is_cluster = is_cluster

    @property
    def id(self):
        """Retrieve the ID of the group."""
        return group_id_from_path(self.name, self.client.project)

    @property
    def parent_id(self):
        """The ID of  the parent group."""
        return group_id_from_path(self.parent_name, self.client.project)

    def parent(self):
        """Returns the parent group of this group.

        :rtype: :class:`Group` or None
        :returns: The parent of the group.
        """
        if not self.parent_name:
            return None
        return self._fetch(self.client, self.parent_id)

    def children(self):
        """Lists all children of this group.

        Returns groups whose parent_name field contains the group name. If no
        groups have this parent, the results are empty.

        :rtype: list of :class:`~gcloud.monitoring.group.Group`
        :returns: A list of group instances.
        """
        return self._list(self.client, children_of_group=self.name)

    def ancestors(self):
        """Lists all ancestors of this group.

        The groups are returned in order, starting with the immediate parent
        and ending with the most distant ancestor. If the specified group has
        no immediate parent, the results are empty.

        :rtype: list of :class:`~gcloud.monitoring.group.Group`
        :returns: A list of group instances.
        """
        return self._list(self.client, ancestors_of_group=self.name)

    def descendants(self):
        """Lists all descendants of this group.

        This returns a superset of the results returned by the :meth:`children`
        method, and includes children-of-children, and so forth.

        :rtype: list of :class:`~gcloud.monitoring.group.Group`
        :returns: A list of group instances.
        """
        return self._list(self.client, descendants_of_group=self.name)

    def members(self, filter_string=None, end_time=None, start_time=None):
        """Lists all monitored resources that are members of this group.

        If no end_time and start_time is provided then the group membership
        over the last minute is returned.

        Examples::

            To get current members that are Compute Engine VM instances:

                group.members('resource.type = "gce_instance"')

            To get historical members that existed between 4 and 5 hours ago:

                import datetime
                t1 = datetime.datetime.utcnow() - datetime.timedelta(hours=4)
                t0 = t1 - datetime.timedelta(hours=1)
                group.members(end_time=t1, start_time=t0)


        :type filter_string: string or None
        :param filter_string:
            An optional list filter describing the members to be returned. The
            filter may reference the type, labels, and metadata of monitored
            resources that comprise the group. See the `filter documentation`_.

        :type end_time: :class:`datetime.datetime` or None
        :param end_time:
            The end time (inclusive) of the time interval for which results
            should be returned, as a datetime object.

        :type start_time: :class:`datetime.datetime` or None
        :param start_time:
            The start time (exclusive) of the time interval for which results
            should be returned, as a datetime object.  If not specified, the
            interval is a point in time.

        :rtype: list of :class:`~gcloud.monitoring.resource.Resource`
        :returns: A list of resource instances.

        :raises:
            :exc:`ValueError` if the ``start_time`` is specified, but the
            ``end_time`` is missing.

        .. _filter documentation:
            https://cloud.google.com/monitoring/api/v3/filters#group-filter
        """
        if start_time is not None and end_time is None:
            raise ValueError('If "start_time" is specified, "end_time" must '
                             'also be specified')

        path = '/%s/members' % self.name
        resources = []
        page_token = None

        while True:
            params = {}

            if filter_string is not None:
                params['filter'] = filter_string

            if end_time is not None:
                params['interval.endTime'] = _format_timestamp(end_time)

            if start_time is not None:
                params['interval.startTime'] = _format_timestamp(start_time)

            if page_token is not None:
                params['pageToken'] = page_token

            response = self.client.connection.api_request(
                method='GET', path=path, query_params=params)
            for info in response.get('members', []):
                resources.append(Resource._from_dict(info))

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        return resources

    @staticmethod
    def path_helper(project, group_id=''):
        """Returns the path to the group API.

        :type project: string
        :param project: The project ID or number to use.

        :type group_id: string
        :param group_id: The group ID.

        :rtype: string
        :returns: The relative URL path for the specific group.
        """
        return '/projects/{project}/groups/{group_id}'.format(
            project=project, group_id=group_id)

    @classmethod
    def _fetch(cls, client, group_id):
        """Look up a group by ID.

        :type client: :class:`gcloud.monitoring.client.Client`
        :param client: The client to use.

        :type group_id: string
        :param group_id: The group ID.

        :rtype: :class:`Group`
        :returns: The group instance.

        :raises: :class:`gcloud.exceptions.NotFound` if the group
            is not found.
        """
        path = cls.path_helper(client.project, group_id)
        info = client.connection.api_request(method='GET', path=path)
        return cls._from_dict(client, info)

    @classmethod
    def _list(cls, client, children_of_group=None, ancestors_of_group=None,
              descendants_of_group=None):
        """Lists all groups in the project.

        :type client: :class:`gcloud.monitoring.client.Client`
        :param client: The client to use.

        :type children_of_group: string or None
        :param children_of_group:
            Returns groups whose parent_name field contains the group name. If
            no groups have this parent, the results are empty.

        :type ancestors_of_group: string or None
        :param ancestors_of_group:
            Returns groups that are ancestors of the specified group. If the
            specified group has no immediate parent, the results are empty.

        :type descendants_of_group: string or None
        :param descendants_of_group:
            Returns the descendants of the specified group. This is a superset
            of the results returned by the children_of_group filter, and
            includes children-of-children, and so forth.

        :rtype: list of :class:`~gcloud.monitoring.group.Group`
        :returns: A list of group instances.
        """
        path = cls.path_helper(client.project)
        groups = []
        page_token = None

        while True:
            params = {}

            if children_of_group is not None:
                params['childrenOfGroup'] = children_of_group

            if ancestors_of_group is not None:
                params['ancestorsOfGroup'] = ancestors_of_group

            if descendants_of_group is not None:
                params['descendantsOfGroup'] = descendants_of_group

            if page_token is not None:
                params['pageToken'] = page_token

            response = client.connection.api_request(
                method='GET', path=path, query_params=params)
            for info in response.get('group', []):
                groups.append(cls._from_dict(client, info))

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        return groups

    @classmethod
    def _from_dict(cls, client, info):
        """Constructs a Group instance from the parsed JSON representation.

        :type client: :class:`gcloud.monitoring.client.Client`
        :param client: A client to be included in the returned object.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`Group`
        :returns: A group.
        """
        group = cls(client)
        group._init_from_dict(info)
        return group

    def _init_from_dict(self, info):
        """Initialize attributes from the parsed JSON representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.
        """
        self.name = info['name']
        self.display_name = info['displayName']
        self.parent_name = info.get('parentName', '')
        self.filter = info['filter']
        self.is_cluster = info.get('isCluster', False)

    def __repr__(self):
        return (
            '<Group: \n'
            ' name={name!r},\n'
            ' display_name={display_name!r},\n'
            ' parent_name={parent_name!r},\n'
            ' filter={filter!r},\n'
            ' is_cluster={is_cluster!r}>'
        ).format(**self.__dict__)
