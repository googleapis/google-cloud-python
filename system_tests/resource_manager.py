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

import os
import time
import unittest

from google.cloud import exceptions
from google.cloud import resource_manager
from google.cloud.resource_manager.resource import OrganizationResource

from system_test_utils import unique_resource_id
from retry import RetryErrors


class Config(object):
    CLIENT = None
    TEST_PROJECT = None
    PROJECT_DELIMITER = '-'
    TEST_ORGANIZATION = None


def setUpModule():
    project_id = 'new' + unique_resource_id(Config.PROJECT_DELIMITER)
    org_id = os.getenv('GOOGLE_CLOUD_ORGANIZATION_ID')
    Config.CLIENT = resource_manager.Client()
    if org_id:
        Config.TEST_ORGANIZATION = OrganizationResource(org_id)
    Config.TEST_PROJECT = Config.CLIENT.new_project(
        project_id,
        name=project_id,
        parent=Config.TEST_ORGANIZATION)
    retry_429 = RetryErrors(exceptions.TooManyRequests)
    retry_429(Config.TEST_PROJECT.create)()
    print 'Project id: %s' % project_id
    waitForProjectCreation(Config.TEST_PROJECT)


def tearDownModule():
    project_retry = RetryErrors(
        (exceptions.TooManyRequests, exceptions.Conflict))
    project_retry(Config.TEST_PROJECT.delete)()


def waitForProjectCreation(project):
    while True:
        time.sleep(2)
        op = project.create_operation
        op.get()
        is_done = op.done
        print 'Check whether create operation is done... %s' % is_done
        if op.error:
            print op.error
            break

        if is_done and op.response:
            print 'Created project %s' % project
            project.reload()
            break


class TestProject(unittest.TestCase):

    def setUp(self):
        self.project_ids_to_delete = []

    def tearDown(self):
        retry_429 = RetryErrors(exceptions.TooManyRequests)
        for project_id in self.project_ids_to_delete:
            project = Config.CLIENT.fetch_project(project_id)
            retry_429(project.delete)()

    def test_new_project(self):
        new_project_id = 'new' + unique_resource_id(Config.PROJECT_DELIMITER)
        self.assertRaises(exceptions.Forbidden,
                          Config.CLIENT.fetch_project, new_project_id)
        created = Config.CLIENT.new_project(project_id=new_project_id,
                                            parent=Config.TEST_ORGANIZATION)
        created.create()
        waitForProjectCreation(created)
        self.assertEqual(new_project_id, created.project_id)
        time.sleep(1)
        self.project_ids_to_delete.append(created.project_id)

    def test_fetch_project(self):
        project = Config.TEST_PROJECT
        fetched_project = Config.CLIENT.fetch_project(project.project_id)
        self.assertEqual(repr(project), repr(fetched_project))

    def test_project_exists(self):
        project = Config.TEST_PROJECT
        self.assertTrue(project.exists())

    def test_update_project(self):
        project = Config.TEST_PROJECT
        orig_name = project.name
        project_name = 'My new project'
        project.name = project_name
        project.update()
        self.assertEqual(project_name, project.name)
        time.sleep(2)
        project.name = orig_name
        project.update()
        self.assertEqual(orig_name, project.name)

    def test_delete_project(self):
        project = Config.TEST_PROJECT
        retry_429 = RetryErrors(exceptions.TooManyRequests)
        retry_429(project.delete)(reload_data=True)
        self.assertEqual('DELETE_REQUESTED', project.status)
        time.sleep(2)
        retry_429(project.undelete)(reload_data=True)

    def test_undelete_project(self):
        project = Config.TEST_PROJECT
        retry_429 = RetryErrors(exceptions.TooManyRequests)
        retry_429(project.delete)(reload_data=True)
        time.sleep(2)
        retry_429(project.undelete)(reload_data=True)
        self.assertEqual('ACTIVE', project.status)
