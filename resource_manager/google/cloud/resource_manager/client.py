# Copyright 2015 Google LLC
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

"""A Client for interacting with the Resource Manager API."""

import six

import google.api_core.client_options
from google.api_core import page_iterator
from google.cloud.client import Client as BaseClient

from google.cloud.resource_manager._http import Connection
from google.cloud.resource_manager.project import Project


class Client(BaseClient):
    """Client to bundle configuration needed for API requests.

    See
    https://cloud.google.com/resource-manager/reference/rest/
    for more information on this API.

    Automatically get credentials::

        >>> from google.cloud import resource_manager
        >>> client = resource_manager.Client()

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed (and if no ``_http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type _http: :class:`~requests.Session`
    :param _http: (Optional) HTTP object to make requests. Can be any object
                  that defines ``request()`` with the same interface as
                  :meth:`requests.Session.request`. If not passed, an
                  ``_http`` object is created that is bound to the
                  ``credentials`` for the current object.
                  This parameter should be considered private, and could
                  change in the future.

    :type client_info: :class:`~google.api_core.client_info.ClientInfo`
    :param client_info:
        The client info used to send a user-agent string along with API
        requests. If ``None``, then default info will be used. Generally,
        you only need to set this if you're developing your own library
        or partner tool.
    :type client_options: :class:`~google.api_core.client_options.ClientOptions`
        or :class:`dict`
    :param client_options: (Optional) Client options used to set user options
        on the client. API Endpoint should be set through client_options.
    """

    SCOPE = ("https://www.googleapis.com/auth/cloud-platform",)
    """The scopes required for authenticating as a Resouce Manager consumer."""

    def __init__(
        self, credentials=None, _http=None, client_info=None, client_options=None
    ):
        super(Client, self).__init__(credentials=credentials, _http=_http)

        kw_args = {"client_info": client_info}
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint
                kw_args["api_endpoint"] = api_endpoint

        self._connection = Connection(self, **kw_args)

    def new_project(self, project_id, name=None, labels=None):
        """Create a project bound to the current client.

        Use :meth:`Project.reload() \
        <google.cloud.resource_manager.project.Project.reload>` to retrieve
        project metadata after creating a
        :class:`~google.cloud.resource_manager.project.Project` instance.

        .. note:

            This does not make an API call.

        :type project_id: str
        :param project_id: The ID for this project.

        :type name: str
        :param name: The display name of the project.

        :type labels: dict
        :param labels: A list of labels associated with the project.

        :rtype: :class:`~google.cloud.resource_manager.project.Project`
        :returns: A new instance of a
                  :class:`~google.cloud.resource_manager.project.Project`
                  **without** any metadata loaded.
        """
        return Project(project_id=project_id, client=self, name=name, labels=labels)

    def fetch_project(self, project_id):
        """Fetch an existing project and it's relevant metadata by ID.

        .. note::

            If the project does not exist, this will raise a
            :class:`NotFound <google.cloud.exceptions.NotFound>` error.

        :type project_id: str
        :param project_id: The ID for this project.

        :rtype: :class:`~google.cloud.resource_manager.project.Project`
        :returns: A :class:`~google.cloud.resource_manager.project.Project`
                  with metadata fetched from the API.
        """
        project = self.new_project(project_id)
        project.reload()
        return project

    def list_projects(self, filter_params=None, page_size=None):
        """List the projects visible to this client.

        Example::

            >>> from google.cloud import resource_manager
            >>> client = resource_manager.Client()
            >>> for project in client.list_projects():
            ...     print(project.project_id)

        List all projects with label ``'environment'`` set to ``'prod'``
        (filtering by labels)::

            >>> from google.cloud import resource_manager
            >>> client = resource_manager.Client()
            >>> env_filter = {'labels.environment': 'prod'}
            >>> for project in client.list_projects(env_filter):
            ...     print(project.project_id)

        See
        https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/list

        Complete filtering example::

            >>> project_filter = {  # Return projects with...
            ...     'name': 'My Project',  # name set to 'My Project'.
            ...     'id': 'my-project-id',  # id set to 'my-project-id'.
            ...     'labels.stage': 'prod',  # the label 'stage' set to 'prod'
            ...     'labels.color': '*'  # a label 'color' set to anything.
            ... }
            >>> client.list_projects(project_filter)

        :type filter_params: dict
        :param filter_params: (Optional) A dictionary of filter options where
                              each key is a property to filter on, and each
                              value is the (case-insensitive) value to check
                              (or the glob ``*`` to check for existence of the
                              property). See the example above for more
                              details.

        :type page_size: int
        :param page_size: (Optional) The maximum number of projects in each
                          page of results from this request. Non-positive
                          values are ignored. Defaults to a sensible value
                          set by the API.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of all
                  :class:`~google.cloud.resource_manager.project.Project`.
                  that the current user has access to.
        """
        extra_params = {}

        if page_size is not None:
            extra_params["pageSize"] = page_size

        if filter_params is not None:
            extra_params["filter"] = [
                "{}:{}".format(key, value)
                for key, value in six.iteritems(filter_params)
            ]

        return page_iterator.HTTPIterator(
            client=self,
            api_request=self._connection.api_request,
            path="/projects",
            item_to_value=_item_to_project,
            items_key="projects",
            extra_params=extra_params,
        )


def _item_to_project(iterator, resource):
    """Convert a JSON project to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that has retrieved the item.

    :type resource: dict
    :param resource: A resource to be converted to a project.

    :rtype: :class:`.Project`
    :returns: The next project in the page.
    """
    return Project.from_api_repr(resource, client=iterator.client)
