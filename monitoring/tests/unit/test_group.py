# Copyright 2016 Google Inc.
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

import unittest


class Test_group_id_from_name(unittest.TestCase):

    def _call_fut(self, path, project):
        from google.cloud.monitoring.group import _group_id_from_name

        return _group_id_from_name(path, project)

    def test_w_empty_name(self):
        PROJECT = 'my-project-1234'
        PATH = ''
        with self.assertRaises(ValueError):
            self._call_fut(PATH, PROJECT)

    def test_w_simple_name(self):
        GROUP_ID = 'GROUP_ID'
        PROJECT = 'my-project-1234'
        PATH = 'projects/%s/groups/%s' % (PROJECT, GROUP_ID)
        group_id = self._call_fut(PATH, PROJECT)
        self.assertEqual(group_id, GROUP_ID)

    def test_w_name_w_all_extras(self):
        GROUP_ID = 'GROUP_ID-part.one~part.two%part-three'
        PROJECT = 'my-project-1234'
        PATH = 'projects/%s/groups/%s' % (PROJECT, GROUP_ID)
        group_id = self._call_fut(PATH, PROJECT)
        self.assertEqual(group_id, GROUP_ID)


class TestGroup(unittest.TestCase):

    def setUp(self):
        self.PROJECT = 'PROJECT'
        self.GROUP_ID = 'group_id'
        self.PARENT_ID = 'parent_id'
        self.DISPLAY_NAME = 'My Group'

        self.PATH = 'projects/%s/groups/' % self.PROJECT
        self.GROUP_NAME = self.PATH + self.GROUP_ID
        self.PARENT_NAME = self.PATH + self.PARENT_ID

        FILTER_TEMPLATE = 'resource.metadata.tag."color"="%s"'
        self.FILTER = FILTER_TEMPLATE % ('blue',)

        self.JSON_GROUP = {
            'name': self.GROUP_NAME,
            'displayName': self.DISPLAY_NAME,
            'parentName': self.PARENT_NAME,
            'filter': self.FILTER,
            'isCluster': True,
        }
        self.JSON_PARENT = {
            'name': self.PARENT_NAME,
            'displayName': 'Parent group',
            'filter': FILTER_TEMPLATE % 'red',
            'isCluster': False,
        }
        self.JSON_SIBLING = {
            'name': self.PATH + 'sibling_id',
            'displayName': 'Sibling group',
            'parentName': self.PARENT_NAME,
            'filter': FILTER_TEMPLATE % 'orange',
            'isCluster': True,
        }
        self.JSON_CHILD = {
            'name': self.PATH + 'child_id',
            'displayName': 'Child group',
            'parentName': self.PARENT_NAME,
            'filter': FILTER_TEMPLATE % 'purple',
            'isCluster': False,
        }

    def _setUpResources(self):
        from google.cloud.monitoring.resource import Resource

        info1 = {
            'type': 'gce_instance',
            'labels': {
                'project_id': 'my-project',
                'instance_id': '1234567890123456788',
                'zone': 'us-central1-a',
            }
        }
        info2 = {
            'type': 'gce_instance',
            'labels': {
                'project_id': 'my-project',
                'instance_id': '1234567890123456789',
                'zone': 'us-central1-a',
            }
        }
        self.RESOURCE1 = Resource._from_dict(info1)
        self.RESOURCE2 = Resource._from_dict(info2)
        self.MEMBERS = [info1, info2]

    @staticmethod
    def _get_target_class():
        from google.cloud.monitoring.group import Group

        return Group

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def _make_oneFromJSON(self, info, client=None):
        return self._get_target_class()._from_dict(client=client, info=info)

    def _validateGroup(self, actual_group, expected_group_json):
        expected_group = self._make_oneFromJSON(expected_group_json)
        self.assertEqual(actual_group.id, expected_group.id)
        self.assertEqual(actual_group.display_name,
                         expected_group.display_name)
        self.assertEqual(actual_group.parent_id, expected_group.parent_id)
        self.assertEqual(actual_group.filter, expected_group.filter)
        self.assertEqual(actual_group.is_cluster, expected_group.is_cluster)

    def _validateGroupList(self, client, actual_groups, expected_groups_json):
        self.assertEqual(len(actual_groups), len(expected_groups_json))
        for i, group in enumerate(actual_groups):
            self.assertIs(group.client, client)
            self._validateGroup(group, expected_groups_json[i])

    def test_constructor(self):
        client = _Client(project=self.PROJECT)
        group = self._make_one(
            client=client,
            group_id=self.GROUP_ID,
            display_name=self.DISPLAY_NAME,
            parent_id=self.PARENT_ID,
            filter_string=self.FILTER,
            is_cluster=True,
        )

        self.assertIs(group.client, client)

        self.assertEqual(group.id, self.GROUP_ID)
        self.assertEqual(group.name, self.GROUP_NAME)
        self.assertEqual(group.display_name, self.DISPLAY_NAME)
        self.assertEqual(group.parent_id, self.PARENT_ID)
        self.assertEqual(group.parent_name, self.PARENT_NAME)
        self.assertEqual(group.filter, self.FILTER)
        self.assertTrue(group.is_cluster)

    def test_constructor_defaults(self):
        client = _Client(project=self.PROJECT)
        group = self._make_one(client=client)

        self.assertIs(group.client, client)

        self.assertIsNone(group.id)
        self.assertIsNone(group.name)
        self.assertIsNone(group.display_name)
        self.assertIsNone(group.parent_id)
        self.assertIsNone(group.parent_name)
        self.assertIsNone(group.filter)
        self.assertFalse(group.is_cluster)

    def test_path_no_id(self):
        group = self._make_one(client=None)
        self.assertRaises(ValueError, getattr, group, 'path')

    def test_path_w_id(self):
        client = _Client(project=self.PROJECT)
        group = self._make_one(client=client, group_id=self.GROUP_ID)
        self.assertEqual(group.path, '/%s' % self.GROUP_NAME)

    def test_from_dict(self):
        client = _Client(project=self.PROJECT)
        group = self._get_target_class()._from_dict(client, self.JSON_GROUP)

        self.assertIs(group.client, client)

        self.assertEqual(group.name, self.GROUP_NAME)
        self.assertEqual(group.display_name, self.DISPLAY_NAME)
        self.assertEqual(group.parent_name, self.PARENT_NAME)
        self.assertEqual(group.filter, self.FILTER)
        self.assertTrue(group.is_cluster)

    def test_from_dict_defaults(self):
        client = _Client(project=self.PROJECT)
        info = {
            'name': self.GROUP_NAME,
            'displayName': self.DISPLAY_NAME,
            'filter': self.FILTER,
        }
        group = self._get_target_class()._from_dict(client, info)

        self.assertIs(group.client, client)

        self.assertEqual(group.id, self.GROUP_ID)
        self.assertEqual(group.display_name, self.DISPLAY_NAME)
        self.assertIsNone(group.parent_id)
        self.assertEqual(group.filter, self.FILTER)
        self.assertFalse(group.is_cluster)

    def test_to_dict(self):
        client = _Client(project=self.PROJECT)
        group = self._make_oneFromJSON(self.JSON_GROUP, client)
        self.assertEqual(group._to_dict(), self.JSON_GROUP)

    def test_to_dict_defaults(self):
        client = _Client(project=self.PROJECT)
        group = self._make_one(
            client=client, group_id=self.GROUP_ID,
            display_name=self.DISPLAY_NAME,
            filter_string=self.FILTER)
        expected_dict = {
            'name': self.GROUP_NAME,
            'displayName': self.DISPLAY_NAME,
            'filter': self.FILTER,
            'isCluster': False,
        }
        self.assertEqual(group._to_dict(), expected_dict)

    def test_create(self):
        RESPONSE = self.JSON_GROUP

        REQUEST = RESPONSE.copy()
        REQUEST.pop('name')

        connection = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=connection)
        group = self._make_one(
            client=client,
            display_name=self.DISPLAY_NAME,
            parent_id=self.PARENT_ID,
            filter_string=self.FILTER,
            is_cluster=True
        )
        group.create()

        self._validateGroup(group, RESPONSE)

        request, = connection._requested
        expected_request = {'method': 'POST', 'path': '/' + self.PATH,
                            'data': REQUEST}
        self.assertEqual(request, expected_request)

    def test_exists_hit(self):
        connection = _Connection(self.JSON_GROUP)
        client = _Client(project=self.PROJECT, connection=connection)
        group = self._make_one(client=client, group_id=self.GROUP_ID)

        self.assertTrue(group.exists())

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + self.GROUP_NAME,
                            'query_params': {'fields': 'name'}}
        self.assertEqual(request, expected_request)

    def test_exists_miss(self):
        connection = _Connection()
        client = _Client(project=self.PROJECT, connection=connection)
        group = self._make_one(client=client, group_id=self.GROUP_ID)

        self.assertFalse(group.exists())

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + self.GROUP_NAME,
                            'query_params': {'fields': 'name'}}
        self.assertEqual(request, expected_request)

    def test_reload(self):
        connection = _Connection(self.JSON_GROUP)
        client = _Client(project=self.PROJECT, connection=connection)
        group = self._make_one(client, group_id=self.GROUP_ID)
        group.reload()

        self.assertIs(group.client, client)
        self._validateGroup(group, self.JSON_GROUP)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + self.GROUP_NAME}
        self.assertEqual(request, expected_request)

    def test_update(self):
        REQUEST = self.JSON_GROUP
        RESPONSE = REQUEST

        connection = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=connection)
        group = self._make_oneFromJSON(REQUEST, client)
        group.update()

        self._validateGroup(group, RESPONSE)

        request, = connection._requested
        expected_request = {'method': 'PUT', 'path': '/' + self.GROUP_NAME,
                            'data': REQUEST}
        self.assertEqual(request, expected_request)

    def test_delete(self):
        connection = _Connection(self.JSON_GROUP)
        client = _Client(project=self.PROJECT, connection=connection)
        group = self._make_oneFromJSON(self.JSON_GROUP, client)
        group.delete()

        request, = connection._requested
        expected_request = {'method': 'DELETE', 'path': group.path}
        self.assertEqual(request, expected_request)

    def test_fetch_parent(self):
        connection = _Connection(self.JSON_PARENT)
        client = _Client(project=self.PROJECT, connection=connection)
        group = self._make_oneFromJSON(self.JSON_GROUP, client)

        actual_parent = group.fetch_parent()

        self.assertIs(actual_parent.client, client)
        self._validateGroup(actual_parent, self.JSON_PARENT)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + self.PARENT_NAME}
        self.assertEqual(request, expected_request)

    def test_fetch_parent_empty(self):
        connection = _Connection()
        client = _Client(project=self.PROJECT, connection=connection)
        group = self._make_one(client=client)
        actual_parent = group.fetch_parent()

        self.assertIsNone(actual_parent)
        self.assertEqual(connection._requested, [])

    def test_list(self):
        LIST_OF_GROUPS = [self.JSON_GROUP, self.JSON_PARENT]
        RESPONSE = {
            'group': LIST_OF_GROUPS,
        }
        connection = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=connection)
        groups = self._get_target_class()._list(client)
        self._validateGroupList(client, groups, LIST_OF_GROUPS)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + self.PATH,
                            'query_params': {}}
        self.assertEqual(request, expected_request)

    def test_list_paged(self):
        from google.cloud.exceptions import NotFound

        LIST_OF_GROUPS = [self.JSON_GROUP, self.JSON_PARENT]
        TOKEN = 'second-page-please'
        RESPONSE1 = {
            'group': [LIST_OF_GROUPS[0]],
            'nextPageToken': TOKEN,
        }
        RESPONSE2 = {
            'group': [LIST_OF_GROUPS[1]],
        }

        connection = _Connection(RESPONSE1, RESPONSE2)
        client = _Client(project=self.PROJECT, connection=connection)
        groups = self._get_target_class()._list(client)
        self._validateGroupList(client, groups, LIST_OF_GROUPS)

        request1, request2 = connection._requested
        expected_request1 = {'method': 'GET', 'path': '/' + self.PATH,
                             'query_params': {}}
        expected_request2 = {'method': 'GET', 'path': '/' + self.PATH,
                             'query_params': {'pageToken': TOKEN}}
        self.assertEqual(request1, expected_request1)
        self.assertEqual(request2, expected_request2)

        with self.assertRaises(NotFound):
            self._get_target_class()._list(client)

    def test_list_children(self):
        CHILDREN = [self.JSON_GROUP, self.JSON_SIBLING]
        RESPONSE = {
            'group': CHILDREN,
        }
        connection = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=connection)
        parent_group = self._make_oneFromJSON(self.JSON_PARENT, client)
        groups = parent_group.list_children()
        self._validateGroupList(client, groups, CHILDREN)

        request, = connection._requested
        expected_request = {
            'method': 'GET', 'path': '/' + self.PATH,
            'query_params': {'childrenOfGroup': self.PARENT_NAME}
        }
        self.assertEqual(request, expected_request)

    def test_list_ancestors(self):
        ANCESTORS = [self.JSON_GROUP, self.JSON_PARENT]
        RESPONSE = {
            'group': ANCESTORS,
        }
        connection = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=connection)
        child_group = self._make_oneFromJSON(self.JSON_CHILD, client)
        groups = child_group.list_ancestors()
        self._validateGroupList(client, groups, ANCESTORS)

        request, = connection._requested
        expected_request = {
            'method': 'GET', 'path': '/' + self.PATH,
            'query_params': {'ancestorsOfGroup': child_group.name}
        }
        self.assertEqual(request, expected_request)

    def test_list_descendants(self):
        DESCENDANTS = [self.JSON_GROUP, self.JSON_SIBLING, self.JSON_CHILD]
        RESPONSE = {
            'group': DESCENDANTS,
        }
        connection = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=connection)
        parent_group = self._make_oneFromJSON(self.JSON_PARENT, client)
        groups = parent_group.list_descendants()
        self._validateGroupList(client, groups, DESCENDANTS)

        request, = connection._requested
        expected_request = {
            'method': 'GET', 'path': '/' + self.PATH,
            'query_params': {'descendantsOfGroup': self.PARENT_NAME}
        }
        self.assertEqual(request, expected_request)

    def test_list_members(self):
        self._setUpResources()
        RESPONSE = {
            'members': self.MEMBERS,
        }
        connection = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=connection)
        group = self._make_oneFromJSON(self.JSON_GROUP, client)
        members = group.list_members()

        self.assertEqual(members, [self.RESOURCE1, self.RESOURCE2])

        request, = connection._requested
        expected_request = {
            'method': 'GET', 'path': '/%s/members' % self.GROUP_NAME,
            'query_params': {},
        }
        self.assertEqual(request, expected_request)

    def test_list_members_paged(self):
        self._setUpResources()
        TOKEN = 'second-page-please'
        RESPONSE1 = {
            'members': [self.MEMBERS[0]],
            'nextPageToken': TOKEN,
        }
        RESPONSE2 = {
            'members': [self.MEMBERS[1]],
        }

        connection = _Connection(RESPONSE1, RESPONSE2)
        client = _Client(project=self.PROJECT, connection=connection)
        group = self._make_oneFromJSON(self.JSON_GROUP, client)
        members = group.list_members()

        self.assertEqual(members, [self.RESOURCE1, self.RESOURCE2])

        request1, request2 = connection._requested
        expected_request1 = {
            'method': 'GET', 'path': '/%s/members' % self.GROUP_NAME,
            'query_params': {},
        }
        expected_request2 = {
            'method': 'GET', 'path': '/%s/members' % self.GROUP_NAME,
            'query_params': {'pageToken': TOKEN},
        }
        self.assertEqual(request1, expected_request1)
        self.assertEqual(request2, expected_request2)

    def test_list_members_w_all_arguments(self):
        import datetime
        from google.cloud._helpers import _datetime_to_rfc3339

        self._setUpResources()

        T0 = datetime.datetime(2016, 4, 6, 22, 5, 0)
        T1 = datetime.datetime(2016, 4, 6, 22, 10, 0)
        MEMBER_FILTER = 'resource.zone = "us-central1-a"'

        RESPONSE = {
            'members': self.MEMBERS,
        }
        connection = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=connection)
        group = self._make_oneFromJSON(self.JSON_GROUP, client)
        members = group.list_members(
            start_time=T0, end_time=T1, filter_string=MEMBER_FILTER)

        self.assertEqual(members, [self.RESOURCE1, self.RESOURCE2])

        request, = connection._requested
        expected_request = {
            'method': 'GET', 'path': '/%s/members' % self.GROUP_NAME,
            'query_params': {
                'interval.startTime': _datetime_to_rfc3339(T0),
                'interval.endTime': _datetime_to_rfc3339(T1),
                'filter': MEMBER_FILTER,
            },
        }
        self.assertEqual(request, expected_request)

    def test_list_members_w_missing_end_time(self):
        import datetime

        T0 = datetime.datetime(2016, 4, 6, 22, 5, 0)

        connection = _Connection()
        client = _Client(project=self.PROJECT, connection=connection)
        group = self._make_oneFromJSON(self.JSON_GROUP, client)
        with self.assertRaises(ValueError):
            group.list_members(start_time=T0)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = list(responses)
        self._requested = []

    def api_request(self, **kwargs):
        from google.cloud.exceptions import NotFound

        self._requested.append(kwargs)
        try:
            return self._responses.pop(0)
        except IndexError:
            raise NotFound('miss')


class _Client(object):

    def __init__(self, project, connection=None):
        self.project = project
        self._connection = connection
