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

"""Utility for managing projects via the Cloud Resource Manager API."""


class Project(object):
    """Projects are containers for your work on Google Cloud Platform.

    .. note::

        A :class:`Project` can also be created via
        :meth:`Client.project() \
        <gcloud.resource_manager.client.Client.project>`

    To manage labels on a :class:`Project`::

        >>> from gcloud import resource_manager
        >>> client = resource_manager.Client()
        >>> project = client.project('purple-spaceship-123')
        >>> project.labels = {'color': 'purple'}
        >>> project.labels['environment'] = 'production'
        >>> project.update()

    See:
    https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects

    :type project_id: string
    :param project_id: The globally unique ID of the project.

    :type client: :class:`gcloud.resource_manager.client.Client`
    :param client: The Client used with this project.

    :type name: string
    :param name: The display name of the project.

    :type labels: dict
    :param labels: A list of labels associated with the project.
    """
    def __init__(self, project_id, client, name=None, labels=None):
        self._client = client
        self.project_id = project_id
        self.name = name
        self.number = None
        self.labels = labels or {}
        self.status = None

    def __repr__(self):
        return '<Project: %r (%r)>' % (self.name, self.project_id)

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a project given its API representation.

        :type resource: dict
        :param resource: project resource representation returned from the API

        :type client: :class:`gcloud.resource_manager.client.Client`
        :param client: The Client used with this project.

        :rtype: :class:`gcloud.resource_manager.project.Project`
        """
        project = cls(project_id=resource['projectId'], client=client)
        project.set_properties_from_api_repr(resource)
        return project

    def set_properties_from_api_repr(self, resource):
        """Update specific properties from its API representation."""
        self.name = resource.get('name')
        self.number = resource['projectNumber']
        self.labels = resource.get('labels', {})
        self.status = resource['lifecycleState']

    @property
    def full_name(self):
        """Fully-qualified name (ie, ``'projects/purple-spaceship-123'``)."""
        if not self.project_id:
            raise ValueError('Missing project ID.')
        return 'projects/%s' % (self.project_id)

    @property
    def path(self):
        """URL for the project (ie, ``'/projects/purple-spaceship-123'``)."""
        return '/%s' % (self.full_name)
