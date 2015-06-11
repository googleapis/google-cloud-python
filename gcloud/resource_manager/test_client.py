# Copyright 2015 Google Inc. All rights reserved.
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

"""Tests for resouce_manager.client.Client."""

import unittest2


class TestClient(unittest2.TestCase):
    """Main test case for resource_manager.client.Client."""

    def _getTargetClass(self):
        from gcloud.resource_manager.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_list_projects_returns_iterator(self):
        from gcloud.iterator import Iterator
        CREDS = _Credentials()
        CLIENT_OBJ = self._makeOne(credentials=CREDS)

        RETURNED = {'projects': [{'projectId': 'project-id',
                                  'projectNumber': 1,
                                  'lifecycleState': 'ACTIVE'}]}
        CLIENT_OBJ.connection = _Connection(RETURNED)

        results = CLIENT_OBJ.list_projects()
        self.assertIsInstance(results, Iterator)

    def test_list_projects_no_paging(self):
        CREDS = _Credentials()
        CLIENT_OBJ = self._makeOne(credentials=CREDS)

        RETURNED = {'projects': [{'projectId': 'project-id',
                                  'projectNumber': 1,
                                  'lifecycleState': 'ACTIVE'}]}
        CLIENT_OBJ.connection = _Connection(RETURNED)

        results = list(CLIENT_OBJ.list_projects())
        self.assertEqual(len(results), 1)
        project = results[0]
        self.assertEqual(project.project_id, 'project-id')
        self.assertEqual(project.number, 1)
        self.assertEqual(project.status, 'ACTIVE')

    def test_list_projects_with_paging(self):
        CREDS = _Credentials()
        CLIENT_OBJ = self._makeOne(credentials=CREDS)
        TOKEN = 'next-page-token'
        RETURNED = [{'projects': [{'projectId': 'project-id',
                                   'projectNumber': 1,
                                   'lifecycleState': 'ACTIVE'}],
                     'nextPageToken': TOKEN},
                    {'projects': [{'projectId': 'project-id-2',
                                   'projectNumber': 2,
                                   'lifecycleState': 'ACTIVE'}]}]
        CONN = _Connection(*RETURNED)
        CLIENT_OBJ.connection = CONN

        # Get all the projects and verify the requests did as expected.
        results = list(CLIENT_OBJ.list_projects(page_size=1))
        requests = CONN._requested
        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0]['path'], '/projects')
        self.assertEqual(requests[0]['method'], 'GET')
        self.assertEqual(requests[0]['query_params'], {'pageSize': 1})
        self.assertEqual(requests[1]['path'], '/projects')
        self.assertEqual(requests[1]['method'], 'GET')
        self.assertEqual(requests[1]['query_params'], {'pageToken': TOKEN,
                                                       'pageSize': 1})

        # The results should be the two projects defined in RETURNED.
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].project_id, 'project-id')
        self.assertEqual(results[0].number, 1)
        self.assertEqual(results[0].status, 'ACTIVE')
        self.assertEqual(results[1].project_id, 'project-id-2')
        self.assertEqual(results[1].number, 2)
        self.assertEqual(results[1].status, 'ACTIVE')

    def test_list_projects_passes_filter(self):
        CREDS = _Credentials()
        CLIENT_OBJ = self._makeOne(credentials=CREDS)
        FILTER_PARAMS = {'id': 'project-id'}
        RETURNED = [{'projects': [{'projectId': 'project-id',
                                   'projectNumber': 1,
                                   'lifecycleState': 'ACTIVE'}]}]
        CONN = _Connection(*RETURNED)
        CLIENT_OBJ.connection = CONN

        # Get all the projects and verify the requests did as expected.
        results = list(CLIENT_OBJ.list_projects(filter_params=FILTER_PARAMS))
        self.assertEqual(len(results), 1)
        requests = CONN._requested
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0]['path'], '/projects')
        self.assertEqual(requests[0]['method'], 'GET')
        self.assertEqual(requests[0]['query_params'],
                         {'filter': FILTER_PARAMS})

    def test_get_project(self):
        CREDS = _Credentials()
        CLIENT_OBJ = self._makeOne(credentials=CREDS)
        PROJECT_ID = 'project-id'
        RETURNED = [{'projectId': PROJECT_ID,
                     'projectNumber': 1,
                     'lifecycleState': 'ACTIVE'}]
        CONN = _Connection(*RETURNED)
        CLIENT_OBJ.connection = CONN

        project = CLIENT_OBJ.get_project(PROJECT_ID)
        requests = CONN._requested
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0]['path'], '/projects/%s' % (PROJECT_ID,))
        self.assertEqual(requests[0]['method'], 'GET')
        self.assertEqual(project.project_id, PROJECT_ID)
        self.assertEqual(project.number, 1)
        self.assertEqual(project.status, 'ACTIVE')

    def test_get_project_not_found(self):
        CREDS = _Credentials()
        CLIENT_OBJ = self._makeOne(credentials=CREDS)
        PROJECT_ID = 'project-id'
        RETURNED = []
        CONN = _Connection(*RETURNED)
        CLIENT_OBJ.connection = CONN

        project = CLIENT_OBJ.get_project(PROJECT_ID)
        self.assertEqual(project, None)
        requests = CONN._requested
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0]['path'], '/projects/%s' % (PROJECT_ID,))
        self.assertEqual(requests[0]['method'], 'GET')


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _Connection(object):
    """A mock Connection object which accepts a list of responses to return.

    This also let's you check the requests passed through the connection.
    """

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from gcloud.exceptions import NotFound
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFound('miss')
        else:
            return response
