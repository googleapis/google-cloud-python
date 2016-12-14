# Copyright 2015 Google Inc.
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

"""The generic Resource class in Google Cloud Platform and used by the
Resource Manager API."""


class Resource(object):
    """A container to reference a Google Cloud Platform resource.

    See:
    https://cloud.google.com/resource-manager/reference/rest/v1/projects#ResourceId

    :type resource_type: str
    :param resource_type: The type of the resource.

    :type resource_id: str
    :param resource_id: The id of the resource.
    """
    def __init__(self, resource_type, resource_id):
        self.resource_type = resource_type
        self.resource_id = resource_id

    def __repr__(self):
        return '<Resource: %r (%r)>' % (self.resource_id, self.resource_type)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory:  construct a resource given its API representation.

        :type resource: dict
        :param resource: resource type and id returned from the API

        :rtype: :class:`google.cloud.resource_manager.resource.Resource`
        :returns: The resource.
        """
        resource = cls(resource_type=resource.get('type'),
                       resource_id=resource.get('id'))
        return resource


class OrganizationResource(Resource):
    """The Organization Resource type/id container.

    :type resource_id: str
    :param resource_id: The id of the organization.
    """

    ORGANIZATION_TYPE = "organization"

    def __init__(self, resource_id):
        super(OrganizationResource, self).__init__(self.ORGANIZATION_TYPE,
                                                   resource_id)
