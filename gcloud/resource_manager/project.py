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


from gcloud.exceptions import NotFound


class Project(object):
    """Projects are containers for your work on Google Cloud Platform.

    .. note::

        A :class:`Project` can also be created via
        :meth:`Client.new_project() \
        <gcloud.resource_manager.client.Client.new_project>`

    To manage labels on a :class:`Project`::

        >>> from gcloud import resource_manager
        >>> client = resource_manager.Client()
        >>> project = client.new_project('purple-spaceship-123')
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

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`gcloud.resource_manager.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current project.

        :rtype: :class:`gcloud.resource_manager.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    def create(self, client=None):
        """API call:  create the project via a ``POST`` request.

        See
        https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/create

        :type client: :class:`gcloud.resource_manager.client.Client` or
                      :data:`NoneType <types.NoneType>`
        :param client: the client to use.  If not passed, falls back to
                       the client stored on the current project.
        """
        client = self._require_client(client)

        data = {
            'projectId': self.project_id,
            'name': self.name,
            'labels': self.labels,
        }
        resp = client.connection.api_request(method='POST', path='/projects',
                                             data=data)
        self.set_properties_from_api_repr(resource=resp)

    def reload(self, client=None):
        """API call:  reload the project via a ``GET`` request.

        This method will reload the newest metadata for the project. If you've
        created a new :class:`Project` instance via
        :meth:`Client.new_project() \
        <gcloud.resource_manager.client.Client.new_project>`,
        this method will retrieve project metadata.

        .. warning::

            This will overwrite any local changes you've made and not saved
            via :meth:`update`.

        See
        https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/get

        :type client: :class:`gcloud.resource_manager.client.Client` or
                      :data:`NoneType <types.NoneType>`
        :param client: the client to use.  If not passed, falls back to
                       the client stored on the current project.
        """
        client = self._require_client(client)

        # We assume the project exists. If it doesn't it will raise a NotFound
        # exception.
        resp = client.connection.api_request(method='GET', path=self.path)
        self.set_properties_from_api_repr(resource=resp)

    def exists(self, client=None):
        """API call:  test the existence of a project via a ``GET`` request.

        See
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/projects/get

        :type client: :class:`gcloud.resource_manager.client.Client` or
                      :data:`NoneType <types.NoneType>`
        :param client: the client to use.  If not passed, falls back to
                       the client stored on the current project.
        """
        client = self._require_client(client)

        try:
            # Note that we have to request the entire resource as the API
            # doesn't provide a way tocheck for existence only.
            client.connection.api_request(method='GET', path=self.path)
        except NotFound:
            return False
        else:
            return True

    def update(self, client=None):
        """API call:  update the project via a ``PUT`` request.

        See
        https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/update

        :type client: :class:`gcloud.resource_manager.client.Client` or
                      :data:`NoneType <types.NoneType>`
        :param client: the client to use.  If not passed, falls back to
                       the client stored on the current project.
        """
        client = self._require_client(client)

        data = {'name': self.name, 'labels': self.labels}
        resp = client.connection.api_request(method='PUT', path=self.path,
                                             data=data)
        self.set_properties_from_api_repr(resp)

    def delete(self, client=None, reload_data=False):
        """API call:  delete the project via a ``DELETE`` request.

        See:
        https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/delete

        This actually changes the status (``lifecycleState``) from ``ACTIVE``
        to ``DELETE_REQUESTED``.
        Later (it's not specified when), the project will move into the
        ``DELETE_IN_PROGRESS`` state, which means the deleting has actually
        begun.

        :type client: :class:`gcloud.resource_manager.client.Client` or
                      :data:`NoneType <types.NoneType>`
        :param client: the client to use.  If not passed, falls back to
                       the client stored on the current project.

        :type reload_data: bool
        :param reload_data: Whether to reload the project with the latest
                            state. If you want to get the updated status,
                            you'll want this set to :data:`True` as the DELETE
                            method doesn't send back the updated project.
                            Default: :data:`False`.
        """
        client = self._require_client(client)
        client.connection.api_request(method='DELETE', path=self.path)

        # If the reload flag is set, reload the project.
        if reload_data:
            self.reload()

    def undelete(self, client=None, reload_data=False):
        """API call:  undelete the project via a ``POST`` request.

        See
        https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/undelete

        This actually changes the project status (``lifecycleState``) from
        ``DELETE_REQUESTED`` to ``ACTIVE``.
        If the project has already reached a status of ``DELETE_IN_PROGRESS``,
        this request will fail and the project cannot be restored.

        :type client: :class:`gcloud.resource_manager.client.Client` or
                      :data:`NoneType <types.NoneType>`
        :param client: the client to use.  If not passed, falls back to
                       the client stored on the current project.

        :type reload_data: bool
        :param reload_data: Whether to reload the project with the latest
                            state. If you want to get the updated status,
                            you'll want this set to :data:`True` as the DELETE
                            method doesn't send back the updated project.
                            Default: :data:`False`.
        """
        client = self._require_client(client)
        client.connection.api_request(method='POST',
                                      path=self.path + ':undelete')

        # If the reload flag is set, reload the project.
        if reload_data:
            self.reload()
