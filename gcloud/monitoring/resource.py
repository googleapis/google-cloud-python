# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Resource Descriptors for the Google Monitoring API."""

import collections

from gcloud.monitoring.label import LabelDescriptor


class ResourceDescriptor(collections.namedtuple(
        'ResourceDescriptor', ('name type display_name description labels'))):
    """Specification of a monitored resource type and its schema.

    Resource descriptor instances are immutable.

    :type name: string
    :param name:
        The "resource name" of the monitored resource descriptor:
        ``"projects/<project_id>/monitoredResourceDescriptors/<type>"``

    :type type: string
    :param type:
        The monitored resource type. For example: ``"gce_instance"``

    :type display_name: string
    :param display_name:
        A concise name that might be displayed in user interfaces.

    :type description: string
    :param description:
        A detailed description that might be used in documentation.

    :type labels: list of :class:`~gcloud.monitoring.label.LabelDescriptor`
    :param labels:
        A sequence of label descriptors specifying the labels used
        to identify a specific instance of this monitored resource.
    """
    __slots__ = ()

    @classmethod
    def _fetch(cls, client, resource_type):
        """Look up a resource descriptor by type.

        :type client: :class:`gcloud.monitoring.client.Client`
        :param client: The client to use.

        :type resource_type: string
        :param resource_type: The resource type name.

        :rtype: :class:`ResourceDescriptor`
        :returns: The resource descriptor instance.

        :raises: :class:`gcloud.exceptions.NotFound`
        """
        path = '/projects/{project}/monitoredResourceDescriptors/{type}' \
            .format(project=client.project,
                    type=resource_type)
        info = client.connection.api_request(method='GET', path=path)
        return cls._from_dict(info)

    @classmethod
    def _list(cls, client, filter=None):
        """List all resource descriptors for the project.

        :type client: :class:`gcloud.monitoring.client.Client`
        :param client: The client to use.

        :type filter: string or None
        :param filter: An optional filter string describing the resource
                       descriptors to be returned.

        :rtype: list of :class:`ResourceDescriptor`
        :returns: A list of resource descriptor instances.
        """
        # Allow "filter" as a parameter name: pylint: disable=redefined-builtin

        path = '/projects/{project}/monitoredResourceDescriptors/'.format(
            project=client.project)

        def _descriptors():
            page_token = None
            while True:
                params = {}

                if filter is not None:
                    params['filter'] = filter

                if page_token is not None:
                    params['pageToken'] = page_token

                response = client.connection.api_request(
                    method='GET', path=path, query_params=params)
                for info in response.get('resourceDescriptors', []):
                    yield cls._from_dict(info)

                page_token = response.get('nextPageToken')
                if not page_token:
                    break

        return list(_descriptors())

    @classmethod
    def _from_dict(cls, info):
        """Construct a resource descriptor from the parsed JSON representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`ResourceDescriptor`
        :returns: A resource descriptor.
        """
        return cls(
            name=info.get('name', ''),
            type=info.get('type', ''),
            display_name=info.get('displayName', ''),
            description=info.get('description', ''),
            labels=tuple(LabelDescriptor._from_dict(label)
                         for label in info.get('labels', [])),
        )


class Resource(collections.namedtuple('Resource', 'type labels')):
    """A monitored resource identified by specifying values for all labels.

    :type type: string
    :param type: The resource type name.

    :type labels: dict
    :param labels: A mapping from label names to values for all labels
                   enumerated in the associated :class:`ResourceDescriptor`.
    """
    __slots__ = ()

    @classmethod
    def _from_dict(cls, info):
        """Construct a resource object from the parsed JSON representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`Resource`
        :returns: A resource object.
        """
        return cls(
            type=info.get('type', ''),
            labels=info.get('labels', {}),
        )
