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

"""Define Projects."""

from gcloud.exceptions import MissingClientError
from gcloud.exceptions import NotFound


class Project(object):
    """Projects are containers for your work on Google Cloud Platform.

    .. note::

        It's unlikely that you'd need to instantiate this outside the context
        of a :class:`.client.Client`, so in general, it's best to get a Project
        from a Resource Manager client.

    To create a new project::

        >>> from gcloud import resource_manager
        >>> client = resource_manager.Client()
        >>> project = client.project('purple-spaceship-123')
        >>> project.name = 'Purple Spaceship Project!'
        >>> project.create()

    To get an existing project::

        >>> from gcloud import resource_manager
        >>> client = resource_manager.Client()
        >>> project = client.get_project('purple-spaceship-123')
        >>> print project.name
        Purple Spaceship Project!

    To manage labels::

        >>> from gcloud import resource_manager
        >>> client = resource_manager.Client()
        >>> project = client.get_project('purple-spaceship-123')
        >>> project.labels = {'color': 'purple'}
        >>> project.labels['environment'] = 'production'
        >>> project.update()

    See:
    https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects

    :type id: string
    :param id: the globally unique id of the project
    """
    def __init__(self, client, id):
        self._client = client
        self.id = id
        self.name = None
        self.number = None
        self.labels = {}
        self.status = None

    def __repr__(self):
        if self.name:
            display_name = '%s (%s)' % (self.name, self.id)
        else:
            display_name = self.id
        return '<Project: %s>' % display_name

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a project given its API representation.

        :type resource: dict
        :param resource: project resource representation returned from the API

        :rtype: :class:`gcloud.resource_manager.project.Project`
        """
        project = cls(id=resource['projectId'], client=client)
        project._set_properties_from_api_repr(resource)
        return project

    def _set_properties_from_api_repr(self, resource):
        """Update specific properties from its API representation."""
        self.name = resource.get('name')
        self.number = resource['projectNumber']
        self.labels = resource.get('labels', {})
        self.status = resource['lifecycleState']

    @property
    def full_name(self):
        """Fully-qualified name (ie, ``'projects/purple-spaceship-123'``)."""
        if not self.id:
            raise ValueError('Missing project ID!')
        return 'projects/%s' % (self.id)

    @property
    def path(self):
        """URL for the project (ie, ``'/projects/purple-spaceship-123'``)."""
        return '/%s' % (self.full_name)

    @property
    def client(self):
        """The :class:`gcloud.resource_manager.client.Client` object."""
        return self._client

    def _require_client(self, client=None):
        """Get either a client or raise an exception.

        We need to use this as the various methods could accept a client as a
        parameter, which we need to evaluate. If the client provided is empty
        and there is no client set as an instance variable, we'll raise a
        :class:`gcloud.exceptions.MissingClientError`.

        :type client: :class:`gcloud.resource_manager.client.Client`
        :param client: An optional client to test for existence.
        """
        client = client or self.client
        if not client:
            raise MissingClientError()
        return client

    def create(self, client=None):
        """API call:  create the project via a ``POST`` request.

        Example::

            >>> from gcloud import resource_manager
            >>> client = resource_manager.Client()
            >>> project = client.project('new-spaceship-123')
            >>> project.name = 'New Spaceship Project!'
            >>> project.create()

        See
        https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/create

        :type client: :class:`gcloud.resource_manager.client.Client` or None
        :param client: the client to use.  If not passed, falls back to
                       the ``client`` attribute.
        """
        client = client or self.client
        data = {'projectId': self.id, 'name': self.name, 'labels': self.labels}
        resp = client.connection.api_request(method='POST', path='/projects',
                data=data)
        self._set_properties_from_api_repr(resource=resp)


    def reload(self, client=None):
        """API call:  reload the project via a ``GET`` request.

        This method will reload the newest metadata for the project.

        .. warning::

            This will overwrite any local changes you've made and not saved!

        Example::

            >>> from gcloud import resource_manager
            >>> client = resource_manager.Client()
            >>> project = client.get_project('purple-spaceship-123')
            >>> project.name = 'Locally changed name'
            >>> print project
            <Project: Locally changed name (purple-spaceship-123)>
            >>> project.reload()
            >>> print project
            <project: Purple Spaceship (purple-spaceship-123)>

        See
        https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/get

        :type client: :class:`gcloud.resource_manager.client.Client` or None
        :param client: the client to use.  If not passed, falls back to
                       the ``client`` attribute.
        """
        client = self._require_client(client=client)

        # We assume the project exists. If it doesn't it will raise a NotFound
        # exception.
        resp = client.connection.api_request(method='GET', path=self.path)
        self._set_properties_from_api_repr(resource=resp)

    def update(self, client=None):
        """API call:  update the project via a ``PUT`` request.

        Example::

            >>> from gcloud import resource_manager
            >>> client = resource_manager.Client()
            >>> project = client.get_project('purple-spaceship-123')
            >>> project.name = 'New Purple Spaceship'
            >>> project.labels['environment'] = 'prod'
            >>> project.update()

        See
        https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/update

        :type client: :class:`gcloud.resource_manager.client.Client` or None
        :param client: the client to use.  If not passed, falls back to
                       the ``client`` attribute.
        """
        client = self._require_client(client=client)

        data = {'name': self.name, 'labels': self.labels}
        resp = client.connection.api_request(method='PUT', path=self.path,
                data=data)
        self._set_properties_from_api_repr(resp)

    def exists(self, client=None):
        """API call:  test the existence of a project via a ``GET`` request.

        Example::

            >>> from gcloud import resource_manager
            >>> client = resource_manager.Client()
            >>> project = client.project('purple-spaceship-456')
            >>> project.exists()
            False

        You can also use the
        :func:`gcloud.resource_manager.client.Client.get_project`
        method to check whether a project exists, as it will return ``None``
        if the project doesn't exist::

            >>> from gcloud import resource_manager
            >>> client = resource_manager.Client()
            >>> print client.get_project('purple-spaceship-456')
            None

        See
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/projects/get

        :type client: :class:`gcloud.resource_manager.client.Client` or None
        :param client: the client to use.  If not passed, falls back to
                       the ``client`` attribute.
        """
        client = self._require_client(client=client)

        try:
            client.connection.api_request(method='GET', path=self.path)
        except NotFound:
            return False
        else:
            return True

    def delete(self, client=None, reload=True):
        """API call:  delete the project via a ``DELETE`` request.

        See:
        https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/delete

        This actually changes the status (``lifecycleState``) from ``ACTIVE``
        to ``DELETE_REQUESTED``.
        Later (it's not specified when), the project will move into the
        ``DELETE_IN_PROGRESS`` state, which means the deleting has actually
        begun.

        Example::

            >>> from gcloud import resource_manager
            >>> client = resource_manager.Client()
            >>> project = client.get_project('purple-spaceship-123')
            >>> project.delete()

        :type client: :class:`gcloud.resource_manager.client.Client` or None
        :param client: the client to use.  If not passed,
                       falls back to the ``client`` attribute.

        :type reload: bool
        :param reload: Whether to reload the project with the latest state.
                       Default: ``True``.
        """
        client = self._require_client(client)
        client.connection.api_request(method='DELETE', path=self.path)

        # If the reload flag is True, reload the project.
        if reload:
            self.reload()

    def undelete(self, client=None, reload=True):
        """API call:  undelete the project via a ``POST`` request.

        See
        https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/undelete

        This actually changes the project status (``lifecycleState``) from
        ``DELETE_REQUESTED`` to ``ACTIVE``.
        If the project has already reached a status of ``DELETE_IN_PROGRESS`,
        this request will fail and the project cannot be restored.

        Example::

            >>> from gcloud import resource_manager
            >>> client = resource_manager.Client()
            >>> project = client.get_project('purple-spaceship-123')
            >>> project.delete()
            >>> print project.status
            DELETE_REQUESTED
            >>> project.undelete()
            >>> print project.status
            ACTIVE

        :type client: :class:`gcloud.resource_manager.client.Client` or None
        :param client: the client to use.  If not passed,
                       falls back to the ``client`` attribute.

        :type reload: bool
        :param reload: Whether to reload the project with the latest state.
                       Default: ``True``.
        """
        client = self._require_client(client)
        client.connection.api_request(method='POST',
                                      path=self.path + ':undelete')

        # If the reload flag is True, reload the project.
        if reload:
            self.reload()
