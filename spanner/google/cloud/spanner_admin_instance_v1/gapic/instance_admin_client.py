# Copyright 2017 Google LLC
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
"""Accesses the google.spanner.admin.instance.v1 InstanceAdmin API."""

import functools
import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template

from google.cloud.spanner_admin_instance_v1.gapic import enums
from google.cloud.spanner_admin_instance_v1.gapic import instance_admin_client_config
from google.cloud.spanner_admin_instance_v1.proto import spanner_instance_admin_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-spanner', ).version


class InstanceAdminClient(object):
    """
    Cloud Spanner Instance Admin API

    The Cloud Spanner Instance Admin API can be used to create, delete,
    modify and list instances. Instances are dedicated Cloud Spanner serving
    and storage resources to be used by Cloud Spanner databases.

    Each instance has a \"configuration\", which dictates where the
    serving resources for the Cloud Spanner instance are located (e.g.,
    US-central, Europe). Configurations are created by Google based on
    resource availability.

    Cloud Spanner billing is based on the instances that exist and their
    sizes. After an instance exists, there are no additional
    per-database or per-operation charges for use of the instance
    (though there may be additional network bandwidth charges).
    Instances offer isolation: problems with databases in one instance
    will not affect other instances. However, within an instance
    databases can affect each other. For example, if one database in an
    instance receives a lot of requests and consumes most of the
    instance resources, fewer resources are available for other
    databases in that instance, and their performance may suffer.
    """

    SERVICE_ADDRESS = 'spanner.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/spanner.admin',
    )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.spanner.admin.instance.v1.InstanceAdmin'

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project,
        )

    @classmethod
    def instance_config_path(cls, project, instance_config):
        """Return a fully-qualified instance_config string."""
        return google.api_core.path_template.expand(
            'projects/{project}/instanceConfigs/{instance_config}',
            project=project,
            instance_config=instance_config,
        )

    @classmethod
    def instance_path(cls, project, instance):
        """Return a fully-qualified instance string."""
        return google.api_core.path_template.expand(
            'projects/{project}/instances/{instance}',
            project=project,
            instance=instance,
        )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=instance_admin_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict): A dictionary of call options for each
                method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                'The `channel` and `credentials` arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__), )

        # Create the channel.
        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES,
            )

        # Create the gRPC stubs.
        self.instance_admin_stub = (
            spanner_instance_admin_pb2.InstanceAdminStub(channel))

        # Operations client for methods that return long-running operations
        # futures.
        self.operations_client = (
            google.api_core.operations_v1.OperationsClient(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)
        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        # Write the "inner API call" methods to the class.
        # These are wrapped versions of the gRPC stub methods, with retry and
        # timeout configuration applied, called by the public methods on
        # this class.
        self._list_instance_configs = google.api_core.gapic_v1.method.wrap_method(
            self.instance_admin_stub.ListInstanceConfigs,
            default_retry=method_configs['ListInstanceConfigs'].retry,
            default_timeout=method_configs['ListInstanceConfigs'].timeout,
            client_info=client_info,
        )
        self._get_instance_config = google.api_core.gapic_v1.method.wrap_method(
            self.instance_admin_stub.GetInstanceConfig,
            default_retry=method_configs['GetInstanceConfig'].retry,
            default_timeout=method_configs['GetInstanceConfig'].timeout,
            client_info=client_info,
        )
        self._list_instances = google.api_core.gapic_v1.method.wrap_method(
            self.instance_admin_stub.ListInstances,
            default_retry=method_configs['ListInstances'].retry,
            default_timeout=method_configs['ListInstances'].timeout,
            client_info=client_info,
        )
        self._get_instance = google.api_core.gapic_v1.method.wrap_method(
            self.instance_admin_stub.GetInstance,
            default_retry=method_configs['GetInstance'].retry,
            default_timeout=method_configs['GetInstance'].timeout,
            client_info=client_info,
        )
        self._create_instance = google.api_core.gapic_v1.method.wrap_method(
            self.instance_admin_stub.CreateInstance,
            default_retry=method_configs['CreateInstance'].retry,
            default_timeout=method_configs['CreateInstance'].timeout,
            client_info=client_info,
        )
        self._update_instance = google.api_core.gapic_v1.method.wrap_method(
            self.instance_admin_stub.UpdateInstance,
            default_retry=method_configs['UpdateInstance'].retry,
            default_timeout=method_configs['UpdateInstance'].timeout,
            client_info=client_info,
        )
        self._delete_instance = google.api_core.gapic_v1.method.wrap_method(
            self.instance_admin_stub.DeleteInstance,
            default_retry=method_configs['DeleteInstance'].retry,
            default_timeout=method_configs['DeleteInstance'].timeout,
            client_info=client_info,
        )
        self._set_iam_policy = google.api_core.gapic_v1.method.wrap_method(
            self.instance_admin_stub.SetIamPolicy,
            default_retry=method_configs['SetIamPolicy'].retry,
            default_timeout=method_configs['SetIamPolicy'].timeout,
            client_info=client_info,
        )
        self._get_iam_policy = google.api_core.gapic_v1.method.wrap_method(
            self.instance_admin_stub.GetIamPolicy,
            default_retry=method_configs['GetIamPolicy'].retry,
            default_timeout=method_configs['GetIamPolicy'].timeout,
            client_info=client_info,
        )
        self._test_iam_permissions = google.api_core.gapic_v1.method.wrap_method(
            self.instance_admin_stub.TestIamPermissions,
            default_retry=method_configs['TestIamPermissions'].retry,
            default_timeout=method_configs['TestIamPermissions'].timeout,
            client_info=client_info,
        )

    # Service calls
    def list_instance_configs(self,
                              parent,
                              page_size=None,
                              retry=google.api_core.gapic_v1.method.DEFAULT,
                              timeout=google.api_core.gapic_v1.method.DEFAULT,
                              metadata=None):
        """
        Lists the supported instance configurations for a given project.

        Example:
            >>> from google.cloud import spanner_admin_instance_v1
            >>>
            >>> client = spanner_admin_instance_v1.InstanceAdminClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_instance_configs(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_instance_configs(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The name of the project for which a list of supported instance
                configurations is requested. Values are of the form
                ``projects/<project>``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.spanner_admin_instance_v1.types.InstanceConfig` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = spanner_instance_admin_pb2.ListInstanceConfigsRequest(
            parent=parent,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_instance_configs, retry=retry, timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='instance_configs',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_instance_config(self,
                            name,
                            retry=google.api_core.gapic_v1.method.DEFAULT,
                            timeout=google.api_core.gapic_v1.method.DEFAULT,
                            metadata=None):
        """
        Gets information about a particular instance configuration.

        Example:
            >>> from google.cloud import spanner_admin_instance_v1
            >>>
            >>> client = spanner_admin_instance_v1.InstanceAdminClient()
            >>>
            >>> name = client.instance_config_path('[PROJECT]', '[INSTANCE_CONFIG]')
            >>>
            >>> response = client.get_instance_config(name)

        Args:
            name (str): Required. The name of the requested instance configuration. Values are of
                the form ``projects/<project>/instanceConfigs/<config>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.spanner_admin_instance_v1.types.InstanceConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = spanner_instance_admin_pb2.GetInstanceConfigRequest(
            name=name, )
        return self._get_instance_config(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def list_instances(self,
                       parent,
                       page_size=None,
                       filter_=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Lists all instances in the given project.

        Example:
            >>> from google.cloud import spanner_admin_instance_v1
            >>>
            >>> client = spanner_admin_instance_v1.InstanceAdminClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_instances(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_instances(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The name of the project for which a list of instances is
                requested. Values are of the form ``projects/<project>``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            filter_ (str): An expression for filtering the results of the request. Filter rules are
                case insensitive. The fields eligible for filtering are:

                  * ``name``
                  * ``display_name``
                  * ``labels.key`` where key is the name of a label

                Some examples of using filters are:

                  * ``name:*`` --> The instance has a name.
                  * ``name:Howl`` --> The instance's name contains the string \"howl\".
                  * ``name:HOWL`` --> Equivalent to above.
                  * ``NAME:howl`` --> Equivalent to above.
                  * ``labels.env:*`` --> The instance has the label \"env\".
                  * ``labels.env:dev`` --> The instance has the label \"env\" and the value of the label contains the string \"dev\".
                  * ``name:howl labels.env:dev`` --> The instance's name contains \"howl\" and it has the label \"env\" with its value containing \"dev\".

            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.spanner_admin_instance_v1.types.Instance` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = spanner_instance_admin_pb2.ListInstancesRequest(
            parent=parent,
            page_size=page_size,
            filter=filter_,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_instances, retry=retry, timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='instances',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def get_instance(self,
                     name,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT,
                     metadata=None):
        """
        Gets information about a particular instance.

        Example:
            >>> from google.cloud import spanner_admin_instance_v1
            >>>
            >>> client = spanner_admin_instance_v1.InstanceAdminClient()
            >>>
            >>> name = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> response = client.get_instance(name)

        Args:
            name (str): Required. The name of the requested instance. Values are of the form
                ``projects/<project>/instances/<instance>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.spanner_admin_instance_v1.types.Instance` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = spanner_instance_admin_pb2.GetInstanceRequest(name=name, )
        return self._get_instance(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def create_instance(self,
                        parent,
                        instance_id,
                        instance,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Creates an instance and begins preparing it to begin serving. The
        returned ``long-running operation``
        can be used to track the progress of preparing the new
        instance. The instance name is assigned by the caller. If the
        named instance already exists, ``CreateInstance`` returns
        ``ALREADY_EXISTS``.

        Immediately upon completion of this request:

        * The instance is readable via the API, with all requested attributes
          but no allocated resources. Its state is `CREATING`.

        Until completion of the returned operation:

        * Cancelling the operation renders the instance immediately unreadable
          via the API.
        * The instance can be deleted.
        * All other attempts to modify the instance are rejected.

        Upon completion of the returned operation:

        * Billing for all successfully-allocated resources begins (some types
          may have lower than the requested levels).
        * Databases can be created in the instance.
        * The instance's allocated resource levels are readable via the API.
        * The instance's state becomes ``READY``.

        The returned ``long-running operation`` will
        have a name of the format ``<instance_name>/operations/<operation_id>`` and
        can be used to track creation of the instance.  The
        ``metadata`` field type is
        ``CreateInstanceMetadata``.
        The ``response`` field type is
        ``Instance``, if successful.

        Example:
            >>> from google.cloud import spanner_admin_instance_v1
            >>>
            >>> client = spanner_admin_instance_v1.InstanceAdminClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>> instance_id = ''
            >>> instance = {}
            >>>
            >>> response = client.create_instance(parent, instance_id, instance)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            parent (str): Required. The name of the project in which to create the instance. Values
                are of the form ``projects/<project>``.
            instance_id (str): Required. The ID of the instance to create.  Valid identifiers are of the
                form ``[a-z][-a-z0-9]*[a-z0-9]`` and must be between 6 and 30 characters in
                length.
            instance (Union[dict, ~google.cloud.spanner_admin_instance_v1.types.Instance]): Required. The instance to create.  The name may be omitted, but if
                specified must be ``<parent>/instances/<instance_id>``.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_admin_instance_v1.types.Instance`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.spanner_admin_instance_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = spanner_instance_admin_pb2.CreateInstanceRequest(
            parent=parent,
            instance_id=instance_id,
            instance=instance,
        )
        operation = self._create_instance(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            spanner_instance_admin_pb2.Instance,
            metadata_type=spanner_instance_admin_pb2.CreateInstanceMetadata,
        )

    def update_instance(self,
                        instance,
                        field_mask,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Updates an instance, and begins allocating or releasing resources
        as requested. The returned [long-running
        operation][google.longrunning.Operation] can be used to track the
        progress of updating the instance. If the named instance does not
        exist, returns ``NOT_FOUND``.

        Immediately upon completion of this request:

        * For resource types for which a decrease in the instance's allocation
          has been requested, billing is based on the newly-requested level.

        Until completion of the returned operation:

        * Cancelling the operation sets its metadata's
          [cancel_time][google.spanner.admin.instance.v1.UpdateInstanceMetadata.cancel_time], and begins
          restoring resources to their pre-request values. The operation
          is guaranteed to succeed at undoing all resource changes,
          after which point it terminates with a `CANCELLED` status.
        * All other attempts to modify the instance are rejected.
        * Reading the instance via the API continues to give the pre-request
          resource levels.

        Upon completion of the returned operation:

        * Billing begins for all successfully-allocated resources (some types
          may have lower than the requested levels).
        * All newly-reserved resources are available for serving the instance's
          tables.
        * The instance's new resource levels are readable via the API.

        The returned ``long-running operation`` will
        have a name of the format ``<instance_name>/operations/<operation_id>`` and
        can be used to track the instance modification.  The
        ``metadata`` field type is
        ``UpdateInstanceMetadata``.
        The ``response`` field type is
        ``Instance``, if successful.

        Authorization requires ``spanner.instances.update`` permission on
        resource ``name``.

        Example:
            >>> from google.cloud import spanner_admin_instance_v1
            >>>
            >>> client = spanner_admin_instance_v1.InstanceAdminClient()
            >>>
            >>> instance = {}
            >>> field_mask = {}
            >>>
            >>> response = client.update_instance(instance, field_mask)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            instance (Union[dict, ~google.cloud.spanner_admin_instance_v1.types.Instance]): Required. The instance to update, which must always include the instance
                name.  Otherwise, only fields mentioned in [][google.spanner.admin.instance.v1.UpdateInstanceRequest.field_mask] need be included.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_admin_instance_v1.types.Instance`
            field_mask (Union[dict, ~google.cloud.spanner_admin_instance_v1.types.FieldMask]): Required. A mask specifying which fields in [][google.spanner.admin.instance.v1.UpdateInstanceRequest.instance] should be updated.
                The field mask must always be specified; this prevents any future fields in
                [][google.spanner.admin.instance.v1.Instance] from being erased accidentally by clients that do not know
                about them.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_admin_instance_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.spanner_admin_instance_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = spanner_instance_admin_pb2.UpdateInstanceRequest(
            instance=instance,
            field_mask=field_mask,
        )
        operation = self._update_instance(
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.operations_client,
            spanner_instance_admin_pb2.Instance,
            metadata_type=spanner_instance_admin_pb2.UpdateInstanceMetadata,
        )

    def delete_instance(self,
                        name,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT,
                        metadata=None):
        """
        Deletes an instance.

        Immediately upon completion of the request:

        * Billing ceases for all of the instance's reserved resources.

        Soon afterward:

        * The instance and *all of its databases* immediately and
          irrevocably disappear from the API. All data in the databases
          is permanently deleted.

        Example:
            >>> from google.cloud import spanner_admin_instance_v1
            >>>
            >>> client = spanner_admin_instance_v1.InstanceAdminClient()
            >>>
            >>> name = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> client.delete_instance(name)

        Args:
            name (str): Required. The name of the instance to be deleted. Values are of the form
                ``projects/<project>/instances/<instance>``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = spanner_instance_admin_pb2.DeleteInstanceRequest(name=name, )
        self._delete_instance(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def set_iam_policy(self,
                       resource,
                       policy,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Sets the access control policy on an instance resource. Replaces any
        existing policy.

        Authorization requires ``spanner.instances.setIamPolicy`` on
        ``resource``.

        Example:
            >>> from google.cloud import spanner_admin_instance_v1
            >>>
            >>> client = spanner_admin_instance_v1.InstanceAdminClient()
            >>>
            >>> resource = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            policy (Union[dict, ~google.cloud.spanner_admin_instance_v1.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The size of
                the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_admin_instance_v1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.spanner_admin_instance_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource,
            policy=policy,
        )
        return self._set_iam_policy(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def get_iam_policy(self,
                       resource,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT,
                       metadata=None):
        """
        Gets the access control policy for an instance resource. Returns an empty
        policy if an instance exists but does not have a policy set.

        Authorization requires ``spanner.instances.getIamPolicy`` on
        ``resource``.

        Example:
            >>> from google.cloud import spanner_admin_instance_v1
            >>>
            >>> client = spanner_admin_instance_v1.InstanceAdminClient()
            >>>
            >>> resource = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.spanner_admin_instance_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = iam_policy_pb2.GetIamPolicyRequest(resource=resource, )
        return self._get_iam_policy(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def test_iam_permissions(self,
                             resource,
                             permissions,
                             retry=google.api_core.gapic_v1.method.DEFAULT,
                             timeout=google.api_core.gapic_v1.method.DEFAULT,
                             metadata=None):
        """
        Returns permissions that the caller has on the specified instance resource.

        Attempting this RPC on a non-existent Cloud Spanner instance resource will
        result in a NOT_FOUND error if the user has ``spanner.instances.list``
        permission on the containing Google Cloud Project. Otherwise returns an
        empty set of permissions.

        Example:
            >>> from google.cloud import spanner_admin_instance_v1
            >>>
            >>> client = spanner_admin_instance_v1.InstanceAdminClient()
            >>>
            >>> resource = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions with
                wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see
                `IAM Overview <https://cloud.google.com/iam/docs/overview#permissions>`_.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.spanner_admin_instance_v1.types.TestIamPermissionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource,
            permissions=permissions,
        )
        return self._test_iam_permissions(
            request, retry=retry, timeout=timeout, metadata=metadata)
