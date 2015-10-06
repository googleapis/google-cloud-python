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

"""Define API Indexes."""


class Index(object):
    """Indexes are containers for documents.

    See:
    https://cloud.google.com/search/reference/rest/v1/indexes

    :type name: string
    :param name: the name of the index

    :type client: :class:`gcloud.dns.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the index (which requires a project).
    """

    def __init__(self, name, client):
        self.name = name
        self._client = client
        self._properties = {}

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct an index given its API representation

        :type resource: dict
        :param resource: index resource representation returned from the API

        :type client: :class:`gcloud.dns.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the index.

        :rtype: :class:`gcloud.dns.index.Index`
        :returns: Index parsed from ``resource``.
        """
        name = resource.get('indexId')
        if name is None:
            raise KeyError(
                'Resource lacks required identity information: ["indexId"]')
        index = cls(name, client=client)
        index._set_properties(resource)
        return index

    @property
    def project(self):
        """Project bound to the index.

        :rtype: string
        :returns: the project (derived from the client).
        """
        return self._client.project

    @property
    def path(self):
        """URL path for the index's APIs.

        :rtype: string
        :returns: the path based on project and dataste name.
        """
        return '/projects/%s/indexes/%s' % (self.project, self.name)

    def _list_field_names(self, field_type):
        """Helper for 'text_fields', etc.
        """
        fields = self._properties.get('indexedField', {})
        return fields.get(field_type)

    @property
    def text_fields(self):
        """Names of text fields in the index.

        :rtype: list of string, or None
        :returns: names of text fields in the index, or None if no
                  resource information is available.
        """
        return self._list_field_names('textFields')

    @property
    def atom_fields(self):
        """Names of atom fields in the index.

        :rtype: list of string, or None
        :returns: names of atom fields in the index, or None if no
                  resource information is available.
        """
        return self._list_field_names('atomFields')

    @property
    def html_fields(self):
        """Names of html fields in the index.

        :rtype: list of string, or None
        :returns: names of html fields in the index, or None if no
                  resource information is available.
        """
        return self._list_field_names('htmlFields')

    @property
    def date_fields(self):
        """Names of date fields in the index.

        :rtype: list of string, or None
        :returns: names of date fields in the index, or None if no
                  resource information is available.
        """
        return self._list_field_names('dateFields')

    @property
    def number_fields(self):
        """Names of number fields in the index.

        :rtype: list of string, or None
        :returns: names of number fields in the index, or None if no
                  resource information is available.
        """
        return self._list_field_names('numberFields')

    @property
    def geo_fields(self):
        """Names of geo fields in the index.

        :rtype: list of string, or None
        :returns: names of geo fields in the index, or None if no
                  resource information is available.
        """
        return self._list_field_names('geoFields')

    def _set_properties(self, api_response):
        """Update properties from resource in body of ``api_response``

        :type api_response: httplib2.Response
        :param api_response: response returned from an API call
        """
        self._properties.clear()
        self._properties.update(api_response)
