# Copyright 2016 Google LLC
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

from google.cloud._helpers import _datetime_to_rfc3339
from google.cloud._helpers import _name_from_project_path
from google.cloud.exceptions import NotFound
from google.cloud.monitoring.resource import Resource


_GROUP_TEMPLATE = re.compile(r"""
    projects/            # static prefix
    (?P<project>[^/]+)   # initial letter, wordchars + hyphen
    /groups/             # static midfix
    (?P<name>[^/]+)      # initial letter, wordchars + allowed punc
""", re.VERBOSE)


def _group_id_from_name(path, project=None):
    """Validate a group URI path and get the group ID.

    :type path: str
    :param path: URI path for a group API request.

    :type project: str
    :param project: (Optional) The project associated with the request. It is
                    included for validation purposes.

    :rtype: str
    :returns: Group ID parsed from ``path``.
    :raises: :class:`ValueError` if the ``path`` is ill-formed or if
             the project from the ``path`` does not agree with the
             ``project`` passed in.
    """
    return _name_from_project_path(path, project, _GROUP_TEMPLATE)


def _group_name_from_id(project, group_id):
    """Build the group name given the project and group ID.

    :type project: str
    :param project: The project associated with the group.

    :type group_id: str
    :param group_id: The group ID.

    :rtype: str
    :returns: The fully qualified name of the group.
    """
    return 'projects/{project}/groups/{group_id}'.format(
        project=project, group_id=group_id)


class Group(object):
    """A dynamic collection of monitored resources.

    :type client: :class:`google.cloud.monitoring.client.Client`
    :param client: A client for operating on the metric descriptor.

    :type group_id: str
    :param group_id: (Optional) The ID of the group.

    :type display_name: str
    :param display_name:
        (Optional) A user-assigned name for this group, used only for display
        purposes.

    :type parent_id: str
    :param parent_id:
        (Optional) The ID of the group's parent, if it has one.

    :type filter_string: str
    :param filter_string:
        (Optional) The filter string used to determine which monitored
        resources belong to this group.

    :type is_cluster: bool
    :param is_cluster:
        If true, the members of this group are considered to be a cluster. The
        system can perform additional analysis on groups that are clusters.
    """
    def __init__(self, client, group_id=None, display_name=None,
                 parent_id=None, filter_string=None, is_cluster=False):
        self.client = client
        self._id = group_id
        self.display_name = display_name
        self.parent_id = parent_id
        self.filter = filter_string
        self.is_cluster = is_cluster

        if group_id:
            self._name = _group_name_from_id(client.project, group_id)
        else:
            self._name = None

    @property
    def id(self):
        """Returns the group ID.

        :rtype: str or None
        :returns: the ID of the group based on it's name.
        """
        return self._id

    @property
    def name(self):
        """Returns the fully qualified name of the group.

        :rtype: str or None
        :returns:
            The fully qualified name of the group in the format
            "projects/<project>/groups/<id>".
        """
        return self._name

    @property
    def parent_name(self):
        """Returns the fully qualified name of the parent group.

        :rtype: str or None
        :returns:
            The fully qualified name of the parent group.
        """
        if not self.parent_id:
            return None
        return _group_name_from_id(self.client.project, self.parent_id)

    @property
    def path(self):
        """URL path to this group.

        :rtype: str
        :returns: the path based on project and group name.

        :raises: :exc:`ValueError` if :attr:`name` is not specified.
        """
        if not self.id:
            raise ValueError('Cannot determine path without group ID.')
        return '/' + self.name

    def create(self):
        """Create a new group based on this object via a ``POST`` request.

        Example::

            >>> filter_string = 'resource.type = "gce_instance"'
            >>> group = client.group(
            ...     display_name='My group',
            ...     filter_string=filter_string,
            ...     parent_id='5678',
            ...     is_cluster=True)
            >>> group.create()

        The ``name`` attribute is ignored in preparing the creation request.
        All attributes are overwritten by the values received in the response
        (normally affecting only ``name``).
        """
        path = '/projects/%s/groups/' % (self.client.project,)
        info = self.client._connection.api_request(
            method='POST', path=path, data=self._to_dict())
        self._set_properties_from_dict(info)

    def exists(self):
        """Test for the existence of the group via a ``GET`` request.

        :rtype: bool
        :returns: Boolean indicating existence of the group.
        """
        try:
            self.client._connection.api_request(
                method='GET', path=self.path, query_params={'fields': 'name'})
        except NotFound:
            return False
        else:
            return True

    def reload(self):
        """Sync local group information via a ``GET`` request.

        .. warning::

            This will overwrite any local changes you've made and not saved
            via :meth:`update`.
        """
        info = self.client._connection.api_request(
            method='GET', path=self.path)
        self._set_properties_from_dict(info)

    def update(self):
        """Update the group via a ``PUT`` request."""
        info = self.client._connection.api_request(
            method='PUT', path=self.path, data=self._to_dict())
        self._set_properties_from_dict(info)

    def delete(self):
        """Delete the group via a ``DELETE`` request.

        Example::

            >>> group = client.group('1234')
            >>> group.delete()

        Only the ``client`` and ``name`` attributes are used.

        .. warning::

            This method will fail for groups that have one or more children
            groups.
        """
        self.client._connection.api_request(
            method='DELETE', path=self.path)

    def fetch_parent(self):
        """Returns the parent group of this group via a ``GET`` request.

        :rtype: :class:`Group` or None
        :returns: The parent of the group.
        """
        if not self.parent_id:
            return None
        return self._fetch(self.client, self.parent_id)

    def list_children(self):
        """Lists all children of this group via a ``GET`` request.

        Returns groups whose parent_name field contains the group name. If no
        groups have this parent, the results are empty.

        :rtype: list of :class:`~google.cloud.monitoring.group.Group`
        :returns: A list of group instances.
        """
        return self._list(self.client, children_of_group=self.name)

    def list_ancestors(self):
        """Lists all ancestors of this group via a ``GET`` request.

        The groups are returned in order, starting with the immediate parent
        and ending with the most distant ancestor. If the specified group has
        no immediate parent, the results are empty.

        :rtype: list of :class:`~google.cloud.monitoring.group.Group`
        :returns: A list of group instances.
        """
        return self._list(self.client, ancestors_of_group=self.name)

    def list_descendants(self):
        """Lists all descendants of this group via a ``GET`` request.

        This returns a superset of the results returned by the :meth:`children`
        method, and includes children-of-children, and so forth.

        :rtype: list of :class:`~google.cloud.monitoring.group.Group`
        :returns: A list of group instances.
        """
        return self._list(self.client, descendants_of_group=self.name)

    def list_members(self, filter_string=None, end_time=None, start_time=None):
        """Lists all members of this group via a ``GET`` request.

        If no ``end_time`` is provided then the group membership over the last
        minute is returned.

        Example::

            >>> for member in group.list_members():
            ...     print(member)

        List members that are Compute Engine VM instances::

            >>> filter_string = 'resource.type = "gce_instance"'
            >>> for member in group.list_members(filter_string=filter_string):
            ...     print(member)

        List historical members that existed between 4 and 5 hours ago::

            >>> import datetime
            >>> t1 = datetime.datetime.utcnow() - datetime.timedelta(hours=4)
            >>> t0 = t1 - datetime.timedelta(hours=1)
            >>> for member in group.list_members(end_time=t1, start_time=t0):
            ...     print(member)


        :type filter_string: str
        :param filter_string:
            (Optional) An optional list filter describing the members to be
            returned. The filter may reference the type, labels, and metadata
            of monitored resources that comprise the group. See the `filter
            documentation`_.

        :type end_time: :class:`datetime.datetime`
        :param end_time:
            (Optional) The end time (inclusive) of the time interval for which
            results should be returned, as a datetime object. If ``start_time``
            is specified, then this must also be specified.

        :type start_time: :class:`datetime.datetime`
        :param start_time:
            (Optional) The start time (exclusive) of the time interval for
            which results should be returned, as a datetime object.

        :rtype: list of :class:`~google.cloud.monitoring.resource.Resource`
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

        path = '%s/members' % (self.path,)
        resources = []
        page_token = None
        params = {}

        if filter_string is not None:
            params['filter'] = filter_string

        if end_time is not None:
            params['interval.endTime'] = _datetime_to_rfc3339(
                end_time, ignore_zone=False)

        if start_time is not None:
            params['interval.startTime'] = _datetime_to_rfc3339(
                start_time, ignore_zone=False)

        while True:
            if page_token is not None:
                params['pageToken'] = page_token

            response = self.client._connection.api_request(
                method='GET', path=path, query_params=params.copy())
            for info in response.get('members', ()):
                resources.append(Resource._from_dict(info))

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        return resources

    @classmethod
    def _fetch(cls, client, group_id):
        """Fetch a group from the API based on it's ID.

        :type client: :class:`google.cloud.monitoring.client.Client`
        :param client: The client to use.

        :type group_id: str
        :param group_id: The group ID.

        :rtype: :class:`Group`
        :returns: The group instance.

        :raises: :class:`google.cloud.exceptions.NotFound` if the group
            is not found.
        """
        new_group = cls(client, group_id)
        new_group.reload()
        return new_group

    @classmethod
    def _list(cls, client, children_of_group=None, ancestors_of_group=None,
              descendants_of_group=None):
        """Lists all groups in the project.

        :type client: :class:`google.cloud.monitoring.client.Client`
        :param client: The client to use.

        :type children_of_group: str
        :param children_of_group:
            (Optional) Returns groups whose parent_name field contains the
            group name. If no groups have this parent, the results are empty.

        :type ancestors_of_group: str
        :param ancestors_of_group:
            (Optional) Returns groups that are ancestors of the specified
            group. If the specified group has no immediate parent, the results
            are empty.

        :type descendants_of_group: str
        :param descendants_of_group:
            (Optional) Returns the descendants of the specified group. This is
            a superset of the results returned by the children_of_group filter,
            and includes children-of-children, and so forth.

        :rtype: list of :class:`~google.cloud.monitoring.group.Group`
        :returns: A list of group instances.
        """
        path = '/projects/%s/groups/' % (client.project,)
        groups = []
        page_token = None
        params = {}

        if children_of_group is not None:
            params['childrenOfGroup'] = children_of_group

        if ancestors_of_group is not None:
            params['ancestorsOfGroup'] = ancestors_of_group

        if descendants_of_group is not None:
            params['descendantsOfGroup'] = descendants_of_group

        while True:
            if page_token is not None:
                params['pageToken'] = page_token

            response = client._connection.api_request(
                method='GET', path=path, query_params=params.copy())
            for info in response.get('group', ()):
                groups.append(cls._from_dict(client, info))

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        return groups

    @classmethod
    def _from_dict(cls, client, info):
        """Constructs a Group instance from the parsed JSON representation.

        :type client: :class:`google.cloud.monitoring.client.Client`
        :param client: A client to be included in the returned object.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`Group`
        :returns: A group.
        """
        group = cls(client)
        group._set_properties_from_dict(info)
        return group

    def _set_properties_from_dict(self, info):
        """Update the group properties from its API representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.
        """
        self._name = info['name']
        self._id = _group_id_from_name(self._name)
        self.display_name = info['displayName']
        self.filter = info['filter']
        self.is_cluster = info.get('isCluster', False)

        parent_name = info.get('parentName')
        if parent_name is None:
            self.parent_id = None
        else:
            self.parent_id = _group_id_from_name(parent_name)

    def _to_dict(self):
        """Build a dictionary ready to be serialized to the JSON wire format.

        :rtype: dict
        :returns: A dictionary.
        """
        info = {
            'filter': self.filter,
            'displayName': self.display_name,
            'isCluster': self.is_cluster,
        }

        if self.name is not None:
            info['name'] = self.name

        parent_name = self.parent_name
        if parent_name is not None:
            info['parentName'] = parent_name

        return info

    def __repr__(self):
        return '<Group: %s>' % (self.name,)
