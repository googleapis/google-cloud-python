# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import google.api_core.grpc_helpers

from google.cloud.datacatalog_v1beta1.proto import datacatalog_pb2_grpc


class DataCatalogGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.datacatalog.v1beta1 DataCatalog API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="datacatalog.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "data_catalog_stub": datacatalog_pb2_grpc.DataCatalogStub(channel)
        }

    @classmethod
    def create_channel(
        cls, address="datacatalog.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def search_catalog(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.search_catalog`.

        Searches Data Catalog for multiple resources like entries, tags that
        match a query.

        This is a custom method
        (https://cloud.google.com/apis/design/custom\_methods) and does not
        return the complete resource, only the resource identifier and high
        level fields. Clients can subsequentally call ``Get`` methods.

        Note that Data Catalog search queries do not guarantee full recall.
        Query results that match your query may not be returned, even in
        subsequent result pages. Also note that results returned (and not
        returned) can vary across repeated search queries.

        See `Data Catalog Search
        Syntax <https://cloud.google.com/data-catalog/docs/how-to/search-reference>`__
        for more information.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].SearchCatalog

    @property
    def create_entry_group(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.create_entry_group`.

        Creates an EntryGroup.

        An entry group contains logically related entries together with Cloud
        Identity and Access Management policies that specify the users who can
        create, edit, and view entries within the entry group.

        Data Catalog automatically creates an entry group for BigQuery entries
        ("@bigquery") and Pub/Sub topics ("@pubsub"). Users create their own
        entry group to contain Cloud Storage fileset entries or custom type
        entries, and the IAM policies associated with those entries. Entry
        groups, like entries, can be searched.

        A maximum of 10,000 entry groups may be created per organization across
        all locations.

        Users should enable the Data Catalog API in the project identified by
        the ``parent`` parameter (see [Data Catalog Resource Project]
        (/data-catalog/docs/concepts/resource-project) for more information).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].CreateEntryGroup

    @property
    def get_entry_group(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.get_entry_group`.

        Gets an EntryGroup.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].GetEntryGroup

    @property
    def delete_entry_group(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.delete_entry_group`.

        Deletes an EntryGroup. Only entry groups that do not contain entries can
        be deleted. Users should enable the Data Catalog API in the project
        identified by the ``name`` parameter (see [Data Catalog Resource
        Project] (/data-catalog/docs/concepts/resource-project) for more
        information).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].DeleteEntryGroup

    @property
    def create_entry(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.create_entry`.

        Creates an entry. Only entries of 'FILESET' type or user-specified type
        can be created.

        Users should enable the Data Catalog API in the project identified by
        the ``parent`` parameter (see [Data Catalog Resource Project]
        (/data-catalog/docs/concepts/resource-project) for more information).

        A maximum of 100,000 entries may be created per entry group.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].CreateEntry

    @property
    def update_entry(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.update_entry`.

        Updates an existing entry. Users should enable the Data Catalog API in
        the project identified by the ``entry.name`` parameter (see [Data
        Catalog Resource Project] (/data-catalog/docs/concepts/resource-project)
        for more information).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].UpdateEntry

    @property
    def delete_entry(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.delete_entry`.

        Deletes an existing entry. Only entries created through ``CreateEntry``
        method can be deleted. Users should enable the Data Catalog API in the
        project identified by the ``name`` parameter (see [Data Catalog Resource
        Project] (/data-catalog/docs/concepts/resource-project) for more
        information).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].DeleteEntry

    @property
    def get_entry(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.get_entry`.

        Gets an entry.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].GetEntry

    @property
    def lookup_entry(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.lookup_entry`.

        Get an entry by target resource name. This method allows clients to use
        the resource name from the source Google Cloud Platform service to get the
        Data Catalog Entry.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].LookupEntry

    @property
    def list_entry_groups(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.list_entry_groups`.

        Lists entry groups.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].ListEntryGroups

    @property
    def list_entries(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.list_entries`.

        Lists entries.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].ListEntries

    @property
    def update_entry_group(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.update_entry_group`.

        Updates an EntryGroup. The user should enable the Data Catalog API in
        the project identified by the ``entry_group.name`` parameter (see [Data
        Catalog Resource Project] (/data-catalog/docs/concepts/resource-project)
        for more information).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].UpdateEntryGroup

    @property
    def create_tag_template(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.create_tag_template`.

        Creates a tag template. The user should enable the Data Catalog API in
        the project identified by the ``parent`` parameter (see `Data Catalog
        Resource
        Project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__
        for more information).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].CreateTagTemplate

    @property
    def get_tag_template(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.get_tag_template`.

        Gets a tag template.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].GetTagTemplate

    @property
    def update_tag_template(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.update_tag_template`.

        Updates a tag template. This method cannot be used to update the fields
        of a template. The tag template fields are represented as separate
        resources and should be updated using their own create/update/delete
        methods. Users should enable the Data Catalog API in the project
        identified by the ``tag_template.name`` parameter (see [Data Catalog
        Resource Project] (/data-catalog/docs/concepts/resource-project) for
        more information).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].UpdateTagTemplate

    @property
    def delete_tag_template(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.delete_tag_template`.

        Deletes a tag template and all tags using the template. Users should
        enable the Data Catalog API in the project identified by the ``name``
        parameter (see [Data Catalog Resource Project]
        (/data-catalog/docs/concepts/resource-project) for more information).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].DeleteTagTemplate

    @property
    def create_tag_template_field(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.create_tag_template_field`.

        Creates a field in a tag template. The user should enable the Data
        Catalog API in the project identified by the ``parent`` parameter (see
        `Data Catalog Resource
        Project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__
        for more information).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].CreateTagTemplateField

    @property
    def update_tag_template_field(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.update_tag_template_field`.

        Updates a field in a tag template. This method cannot be used to update
        the field type. Users should enable the Data Catalog API in the project
        identified by the ``name`` parameter (see [Data Catalog Resource
        Project] (/data-catalog/docs/concepts/resource-project) for more
        information).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].UpdateTagTemplateField

    @property
    def rename_tag_template_field(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.rename_tag_template_field`.

        Renames a field in a tag template. The user should enable the Data
        Catalog API in the project identified by the ``name`` parameter (see
        `Data Catalog Resource
        Project <https://cloud.google.com/data-catalog/docs/concepts/resource-project>`__
        for more information).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].RenameTagTemplateField

    @property
    def delete_tag_template_field(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.delete_tag_template_field`.

        Deletes a field in a tag template and all uses of that field. Users
        should enable the Data Catalog API in the project identified by the
        ``name`` parameter (see [Data Catalog Resource Project]
        (/data-catalog/docs/concepts/resource-project) for more information).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].DeleteTagTemplateField

    @property
    def create_tag(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.create_tag`.

        Creates a tag on an ``Entry``. Note: The project identified by the
        ``parent`` parameter for the
        `tag <https://cloud.google.com/data-catalog/docs/reference/rest/v1beta1/projects.locations.entryGroups.entries.tags/create#path-parameters>`__
        and the `tag
        template <https://cloud.google.com/data-catalog/docs/reference/rest/v1beta1/projects.locations.tagTemplates/create#path-parameters>`__
        used to create the tag must be from the same organization.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].CreateTag

    @property
    def update_tag(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.update_tag`.

        Updates an existing tag.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].UpdateTag

    @property
    def delete_tag(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.delete_tag`.

        Deletes a tag.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].DeleteTag

    @property
    def list_tags(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.list_tags`.

        Lists the tags on an ``Entry``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].ListTags

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.set_iam_policy`.

        Sets the access control policy for a resource. Replaces any existing
        policy. Supported resources are:

        -  Tag templates.
        -  Entries.
        -  Entry groups. Note, this method cannot be used to manage policies for
           BigQuery, Cloud Pub/Sub and any external Google Cloud Platform
           resources synced to Cloud Data Catalog.

        Callers must have following Google IAM permission

        -  ``datacatalog.tagTemplates.setIamPolicy`` to set policies on tag
           templates.
        -  ``datacatalog.entries.setIamPolicy`` to set policies on entries.
        -  ``datacatalog.entryGroups.setIamPolicy`` to set policies on entry
           groups.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].SetIamPolicy

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.get_iam_policy`.

        Gets the access control policy for a resource. A ``NOT_FOUND`` error is
        returned if the resource does not exist. An empty policy is returned if
        the resource exists but does not have a policy set on it.

        Supported resources are:

        -  Tag templates.
        -  Entries.
        -  Entry groups. Note, this method cannot be used to manage policies for
           BigQuery, Cloud Pub/Sub and any external Google Cloud Platform
           resources synced to Cloud Data Catalog.

        Callers must have following Google IAM permission

        -  ``datacatalog.tagTemplates.getIamPolicy`` to get policies on tag
           templates.
        -  ``datacatalog.entries.getIamPolicy`` to get policies on entries.
        -  ``datacatalog.entryGroups.getIamPolicy`` to get policies on entry
           groups.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].GetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.test_iam_permissions`.

        Returns the caller's permissions on a resource. If the resource does not
        exist, an empty set of permissions is returned (We don't return a
        ``NOT_FOUND`` error).

        Supported resources are:

        -  Tag templates.
        -  Entries.
        -  Entry groups. Note, this method cannot be used to manage policies for
           BigQuery, Cloud Pub/Sub and any external Google Cloud Platform
           resources synced to Cloud Data Catalog.

        A caller is not required to have Google IAM permission to make this
        request.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].TestIamPermissions
