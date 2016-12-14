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


class TestResource(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.resource_manager.resource import Resource
        return Resource

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        RESOURCE_ID = 'resource-123'
        RESOURCE_TYPE = 'project'
        resource = self._make_one(RESOURCE_TYPE, RESOURCE_ID)
        self.assertEqual(resource.resource_id, RESOURCE_ID)
        self.assertEqual(resource.resource_type, RESOURCE_TYPE)

    def test_from_api_repr(self):
        RESOURCE_ID = 'resource-123'
        RESOURCE_TYPE = 'project'
        resource_dict = {'type': RESOURCE_TYPE,
                         'id': RESOURCE_ID}
        resource = self._get_target_class().from_api_repr(resource_dict)
        self.assertEqual(resource.resource_id, RESOURCE_ID)
        self.assertEqual(resource.resource_type, RESOURCE_TYPE)

    def test_create_organization_resource(self):
        RESOURCE_ID = 'resource-123'
        from google.cloud.resource_manager.resource import OrganizationResource
        organization = OrganizationResource(RESOURCE_ID)
        self.assertEqual(organization.resource_type, 'organization')
        self.assertEqual(organization.resource_id, RESOURCE_ID)
