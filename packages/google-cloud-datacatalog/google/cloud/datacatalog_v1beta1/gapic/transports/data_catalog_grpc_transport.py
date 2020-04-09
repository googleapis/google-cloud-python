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

        Output only. Resource name of this policy tag, whose format is:
        "projects/{project_number}/locations/{location_id}/taxonomies/{taxonomy_id}/policyTags/{id}".

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].SearchCatalog

    @property
    def create_entry_group(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.create_entry_group`.

        Request message for ``LookupEntry``.

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

        Request message for ``GetEntry``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].DeleteEntryGroup

    @property
    def create_entry(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.create_entry`.

        For extensions, this is the name of the type being extended. It is
        resolved in the same manner as type_name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].CreateEntry

    @property
    def update_entry(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.update_entry`.

        A ``TagTemplate``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].UpdateEntry

    @property
    def delete_entry(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.delete_entry`.

        The full name of the Google Cloud Platform resource the Data Catalog
        entry represents. See:
        https://cloud.google.com/apis/design/resource_names#full_resource_name.
        Full names are case-sensitive.

        Examples:

        -  //bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId
        -  //pubsub.googleapis.com/projects/projectId/topics/topicId

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

        An ``Entry``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].UpdateEntryGroup

    @property
    def create_tag_template(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.create_tag_template`.

        The set of permissions to check for the ``resource``. Permissions
        with wildcards (such as '*' or 'storage.*') are not allowed. For more
        information see `IAM
        Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.

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

        An annotation that describes a resource definition, see
        ``ResourceDescriptor``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].UpdateTagTemplate

    @property
    def delete_tag_template(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.delete_tag_template`.

        The relative resource name of the resource in URL format. Examples:

        -  ``projects/{project_id}/locations/{location_id}/entryGroups/{entry_group_id}/entries/{entry_id}``
        -  ``projects/{project_id}/tagTemplates/{tag_template_id}``

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].DeleteTagTemplate

    @property
    def create_tag_template_field(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.create_tag_template_field`.

        An ``EntryGroup``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].CreateTagTemplateField

    @property
    def update_tag_template_field(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.update_tag_template_field`.

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
        return self._stubs["data_catalog_stub"].UpdateTagTemplateField

    @property
    def rename_tag_template_field(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.rename_tag_template_field`.

        The SQL name of the entry. SQL names are case-sensitive.

        Examples:

        -  ``cloud_pubsub.project_id.topic_id``
        -  :literal:`pubsub.project_id.`topic.id.with.dots\``
        -  ``bigquery.table.project_id.dataset_id.table_id``
        -  ``bigquery.dataset.project_id.dataset_id``
        -  ``datacatalog.entry.project_id.location_id.entry_group_id.entry_id``

        ``*_id``\ s shoud satisfy the standard SQL rules for identifiers.
        https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].RenameTagTemplateField

    @property
    def delete_tag_template_field(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.delete_tag_template_field`.

        A simple descriptor of a resource type.

        ResourceDescriptor annotates a resource message (either by means of a
        protobuf annotation or use in the service config), and associates the
        resource's schema, the resource type, and the pattern of the resource
        name.

        Example:

        ::

            message Topic {
              // Indicates this message defines a resource schema.
              // Declares the resource type in the format of {service}/{kind}.
              // For Kubernetes resources, the format is {api group}/{kind}.
              option (google.api.resource) = {
                type: "pubsub.googleapis.com/Topic"
                name_descriptor: {
                  pattern: "projects/{project}/topics/{topic}"
                  parent_type: "cloudresourcemanager.googleapis.com/Project"
                  parent_name_extractor: "projects/{project}"
                }
              };
            }

        The ResourceDescriptor Yaml config will look like:

        ::

            resources:
            - type: "pubsub.googleapis.com/Topic"
              name_descriptor:
                - pattern: "projects/{project}/topics/{topic}"
                  parent_type: "cloudresourcemanager.googleapis.com/Project"
                  parent_name_extractor: "projects/{project}"

        Sometimes, resources have multiple patterns, typically because they can
        live under multiple parents.

        Example:

        ::

            message LogEntry {
              option (google.api.resource) = {
                type: "logging.googleapis.com/LogEntry"
                name_descriptor: {
                  pattern: "projects/{project}/logs/{log}"
                  parent_type: "cloudresourcemanager.googleapis.com/Project"
                  parent_name_extractor: "projects/{project}"
                }
                name_descriptor: {
                  pattern: "folders/{folder}/logs/{log}"
                  parent_type: "cloudresourcemanager.googleapis.com/Folder"
                  parent_name_extractor: "folders/{folder}"
                }
                name_descriptor: {
                  pattern: "organizations/{organization}/logs/{log}"
                  parent_type: "cloudresourcemanager.googleapis.com/Organization"
                  parent_name_extractor: "organizations/{organization}"
                }
                name_descriptor: {
                  pattern: "billingAccounts/{billing_account}/logs/{log}"
                  parent_type: "billing.googleapis.com/BillingAccount"
                  parent_name_extractor: "billingAccounts/{billing_account}"
                }
              };
            }

        The ResourceDescriptor Yaml config will look like:

        ::

            resources:
            - type: 'logging.googleapis.com/LogEntry'
              name_descriptor:
                - pattern: "projects/{project}/logs/{log}"
                  parent_type: "cloudresourcemanager.googleapis.com/Project"
                  parent_name_extractor: "projects/{project}"
                - pattern: "folders/{folder}/logs/{log}"
                  parent_type: "cloudresourcemanager.googleapis.com/Folder"
                  parent_name_extractor: "folders/{folder}"
                - pattern: "organizations/{organization}/logs/{log}"
                  parent_type: "cloudresourcemanager.googleapis.com/Organization"
                  parent_name_extractor: "organizations/{organization}"
                - pattern: "billingAccounts/{billing_account}/logs/{log}"
                  parent_type: "billing.googleapis.com/BillingAccount"
                  parent_name_extractor: "billingAccounts/{billing_account}"

        For flexible resources, the resource name doesn't contain parent names,
        but the resource itself has parents for policy evaluation.

        Example:

        ::

            message Shelf {
              option (google.api.resource) = {
                type: "library.googleapis.com/Shelf"
                name_descriptor: {
                  pattern: "shelves/{shelf}"
                  parent_type: "cloudresourcemanager.googleapis.com/Project"
                }
                name_descriptor: {
                  pattern: "shelves/{shelf}"
                  parent_type: "cloudresourcemanager.googleapis.com/Folder"
                }
              };
            }

        The ResourceDescriptor Yaml config will look like:

        ::

            resources:
            - type: 'library.googleapis.com/Shelf'
              name_descriptor:
                - pattern: "shelves/{shelf}"
                  parent_type: "cloudresourcemanager.googleapis.com/Project"
                - pattern: "shelves/{shelf}"
                  parent_type: "cloudresourcemanager.googleapis.com/Folder"

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].DeleteTagTemplateField

    @property
    def create_tag(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.create_tag`.

        Response message for ``ListTags``.

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

        Request message for ``ExportTaxonomies``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].ListTags

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.set_iam_policy`.

        Response message for ``TestIamPermissions`` method.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].SetIamPolicy

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.get_iam_policy`.

        Entry Metadata. A Data Catalog Entry resource represents another
        resource in Google Cloud Platform (such as a BigQuery dataset or a Cloud
        Pub/Sub topic), or outside of Google Cloud Platform. Clients can use the
        ``linked_resource`` field in the Entry resource to refer to the original
        resource ID of the source system.

        An Entry resource contains resource details, such as its schema. An
        Entry can also be used to attach flexible metadata, such as a ``Tag``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].GetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`DataCatalogClient.test_iam_permissions`.

        If set, gives the index of a oneof in the containing type's
        oneof_decl list. This field is a member of that oneof.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_catalog_stub"].TestIamPermissions
