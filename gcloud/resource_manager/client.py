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

"""A Client for interacting with the Resource Manager API.

Overview
~~~~~~~~

There are three main methods in the ``Client`` class:

- :func:`gcloud.resource_manager.client.Client.list_projects`
- :func:`gcloud.resource_manager.client.Client.project`
- :func:`gcloud.resource_manager.client.Client.get_project`

``project()`` versus ``get_project()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The difference between ``project`` and ``get_project`` is subtle,
so it might be worthwhile to make a quick distinction.

If you want to simply "get a hold of a Project" object,
but **don't** want to actually retrieve any metadata about that project
(for example, when you want to create a new project, or delete a project
in a single API request), ``project()`` is the best method to use::

    >>> from gcloud import resource_manager
    >>> client = resource_manager.Client()
    >>> project = client.project('purple-spaceship-123')
    >>> project.number is None
    True

The ``project`` referenced above has no extra metadata associated with it,
however you can still operate on it (ie, ``project.create()`` or
``project.delete()``).

If you want to retrieve a project and all of it's metadata, the best method
to use is ``get_project()``, which will return ``None`` if the project
doesn't exist::

    >>> from gcloud import resource_manager
    >>> client = resource_manager.Client()
    >>> project = client.get_project('purple-spaceship-123')
    >>> project.number is None
    False
    >>> project = client.get_project('doesnt-exist')
    >>> project is None
    True
"""


from gcloud.client import Client as BaseClient
from gcloud.exceptions import NotFound
from gcloud.iterator import Iterator
from gcloud.resource_manager.connection import Connection
from gcloud.resource_manager.project import Project


class Client(BaseClient):
    """Client to bundle configuration needed for API requests.

    See
    https://cloud.google.com/resource-manager/reference/rest/
    for more information on this API.

    Automatically get credentials::

        >>> from gcloud.resource_manager import Client
        >>> client = Client()

    .. note::

        Chances are you want to use either the constructor with no arguments,
        or one of the factory methods (like
        :func:`gcloud.resource_manager.client.Client.from_service_account_json`
        or similar).

        Even more likely is that you want to use the Cloud SDK to get
        credentials for these API calls (that is, run ``gcloud auth login``).

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def list_projects(self, filter_params=None, page_size=None):
        """List the projects visible to this client.

        Example::

            >>> from gcloud import resource_manager
            >>> client = resource_manager.Client()
            >>> for project in client.list_projects():
            ...     print project.project_id

        List all projects with label ``'environment'`` set to ``'prod'``
        (filtering by labels)::

            >>> from gcloud import resource_manager
            >>> client = resource_manager.Client()
            >>> env_filter = {'labels.environment': 'prod'}
            >>> for project in client.list_projects(env_filter):
            ...     print project.project_id

        See:
        https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/list

        Complete filtering example::

            >>> project_filter = {  # Return projects with...
            ...     'name': 'My Project',  # name set to 'My Project'.
            ...     'id': 'my-project-id',  # id set to 'my-project-id'.
            ...     'labels.stage': 'prod',  # the label 'stage' set to 'prod'
            ...                           # set to prod.
            ...     'labels.color': '*'  # a label 'color' set to anything.
            ... }
            >>> client.list_projects(project_filter)

        :type filter_params: dict
        :param filter_params: A dictionary of filter options where the keys are
                              the property to filter on, and the value is the
                              case-insensitive value to check (or * to check
                              for existence of the property). See the example
                              above for more details.
                              Note that property values are case-insensitive.

        :type page_size: int
        :param page_size: maximum number of projects to return in a single
                          page. If not passed, defaults to a value set by the
                          API.

        :rtype: :class:`gcloud.resource_manager.iterator.ProjectIterator`
        :returns: A ProjectIterator class, which allows you to iterate through
                  all of the results without thinking about pagination.
                  Each item will be a :class:`.project.Project` object.
        """
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if filter_params is not None:
            params['filter'] = filter_params

        client = self

        class ProjectIterator(Iterator):
            """An iterator over a list of Project resources."""

            def get_items_from_response(self, response):
                """Yield :class:`.resource_manager.project.Project` items
                from response.

                :type response: dict
                :param response: The JSON API response for a page of projects.
                """
                for resource in response.get('projects', []):
                    item = Project.from_api_repr(resource, client=client)
                    yield item

        return ProjectIterator(connection=self.connection, extra_params=params,
                               path='/projects')

    def project(self, project_id):
        """Get a Project instance without making an API call.

        Typically used when creating a new project.

        See :func:`gcloud.resource_manager.client.Client.get_project` if you
        want to load a project and its metadata using an API call.

        Example::

            >>> client = Client()
            >>> project = client.project('purple-spaceship-123')
            >>> print project.name
            None
            >>> print project.project_id
            purple-spaceship-123

        :type project_id: str
        :param project_id: The ID for this project.

        :rtype: :class:`gcloud.resource_manager.project.Project`
        :returns: A new instance of a :class:`.project.Project` **without**
                  any metadata loaded.
        """
        return Project(project_id=project_id, client=self)

    def get_project(self, project_id):
        """Get a Project instance and its metadata via an API call.

        Example::

            >>> client = Client()
            >>> project = client.get_project('purple-spaceship-123')
            >>> print project.name
            Purple Spaceship 123
            >>> print project.project_id
            purple-spaceship-123

        See :func:`gcloud.resource_manager.client.Client.project` if you
        want to load a project **without** its metadata (aka, without an
        API call).

        :type project_id: str
        :param project_id: The ID for this project.

        :rtype: :class:`gcloud.resource_manager.project.Project`
        :returns: A new instance of a :class:`.project.Project` with all
                  its metadata loaded.
        """
        try:
            project = self.project(project_id)
            project.reload()
        except NotFound:
            project = None
        return project
