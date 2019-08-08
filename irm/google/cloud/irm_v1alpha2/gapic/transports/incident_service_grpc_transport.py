# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

from google.cloud.irm_v1alpha2.proto import incidents_service_pb2_grpc


class IncidentServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.irm.v1alpha2 IncidentService API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="irm.googleapis.com:443"
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
            "incident_service_stub": incidents_service_pb2_grpc.IncidentServiceStub(
                channel
            )
        }

    @classmethod
    def create_channel(
        cls, address="irm.googleapis.com:443", credentials=None, **kwargs
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
    def create_incident(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.create_incident`.

        Creates a new incident.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].CreateIncident

    @property
    def get_incident(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.get_incident`.

        Returns an incident by name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].GetIncident

    @property
    def search_incidents(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.search_incidents`.

        Returns a list of incidents.
        Incidents are ordered by start time, with the most recent incidents first.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].SearchIncidents

    @property
    def update_incident(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.update_incident`.

        Updates an existing incident.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].UpdateIncident

    @property
    def search_similar_incidents(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.search_similar_incidents`.

        Returns a list of incidents that are "similar" to the specified incident
        or signal. This functionality is provided on a best-effort basis and the
        definition of "similar" is subject to change.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].SearchSimilarIncidents

    @property
    def create_annotation(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.create_annotation`.

        Creates an annotation on an existing incident. Only 'text/plain' and
        'text/markdown' annotations can be created via this method.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].CreateAnnotation

    @property
    def list_annotations(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.list_annotations`.

        Lists annotations that are part of an incident. No assumptions should be
        made on the content-type of the annotation returned.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].ListAnnotations

    @property
    def create_tag(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.create_tag`.

        Creates a tag on an existing incident.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].CreateTag

    @property
    def delete_tag(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.delete_tag`.

        Deletes an existing tag.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].DeleteTag

    @property
    def list_tags(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.list_tags`.

        Lists tags that are part of an incident.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].ListTags

    @property
    def create_signal(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.create_signal`.

        Creates a new signal.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].CreateSignal

    @property
    def search_signals(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.search_signals`.

        Lists signals that are part of an incident.
        Signals are returned in reverse chronological order.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].SearchSignals

    @property
    def get_signal(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.get_signal`.

        Returns a signal by name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].GetSignal

    @property
    def lookup_signal(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.lookup_signal`.

        Finds a signal by other unique IDs.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].LookupSignal

    @property
    def update_signal(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.update_signal`.

        Updates an existing signal (for example, to assign/unassign it to an
        incident).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].UpdateSignal

    @property
    def escalate_incident(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.escalate_incident`.

        Escalates an incident.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].EscalateIncident

    @property
    def create_artifact(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.create_artifact`.

        Creates a new artifact.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].CreateArtifact

    @property
    def list_artifacts(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.list_artifacts`.

        Returns a list of artifacts for an incident.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].ListArtifacts

    @property
    def update_artifact(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.update_artifact`.

        Updates an existing artifact.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].UpdateArtifact

    @property
    def delete_artifact(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.delete_artifact`.

        Deletes an existing artifact.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].DeleteArtifact

    @property
    def send_shift_handoff(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.send_shift_handoff`.

        Sends a summary of the shift for oncall handoff.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].SendShiftHandoff

    @property
    def create_subscription(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.create_subscription`.

        Creates a new subscription.
        This will fail if:
           a. there are too many (50) subscriptions in the incident already
           b. a subscription using the given channel already exists

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].CreateSubscription

    @property
    def update_subscription(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.update_subscription`.

        Updates a subscription.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].UpdateSubscription

    @property
    def list_subscriptions(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.list_subscriptions`.

        Returns a list of subscriptions for an incident.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].ListSubscriptions

    @property
    def delete_subscription(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.delete_subscription`.

        Deletes an existing subscription.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].DeleteSubscription

    @property
    def create_incident_role_assignment(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.create_incident_role_assignment`.

        Creates a role assignment on an existing incident. Normally, the user field
        will be set when assigning a role to oneself, and the next field will be
        set when proposing another user as the assignee. Setting the next field
        directly to a user other than oneself is equivalent to proposing and
        force-assigning the role to the user.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].CreateIncidentRoleAssignment

    @property
    def delete_incident_role_assignment(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.delete_incident_role_assignment`.

        Deletes an existing role assignment.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].DeleteIncidentRoleAssignment

    @property
    def list_incident_role_assignments(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.list_incident_role_assignments`.

        Lists role assignments that are part of an incident.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].ListIncidentRoleAssignments

    @property
    def request_incident_role_handover(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.request_incident_role_handover`.

        Starts a role handover. The proposed assignee will receive an email
        notifying them of the assignment. This will fail if a role handover is
        already pending.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].RequestIncidentRoleHandover

    @property
    def confirm_incident_role_handover(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.confirm_incident_role_handover`.

        Confirms a role handover. This will fail if the 'proposed_assignee'
        field of the IncidentRoleAssignment is not equal to the 'new_assignee'
        field of the request. If the caller is not the new_assignee,
        ForceIncidentRoleHandover should be used instead.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].ConfirmIncidentRoleHandover

    @property
    def force_incident_role_handover(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.force_incident_role_handover`.

        Forces a role handover. This will fail if the 'proposed_assignee' field
        of the IncidentRoleAssignment is not equal to the 'new_assignee' field
        of the request. If the caller is the new_assignee,
        ConfirmIncidentRoleHandover should be used instead.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].ForceIncidentRoleHandover

    @property
    def cancel_incident_role_handover(self):
        """Return the gRPC stub for :meth:`IncidentServiceClient.cancel_incident_role_handover`.

        Cancels a role handover. This will fail if the 'proposed_assignee'
        field of the IncidentRoleAssignment is not equal to the 'new_assignee'
        field of the request.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["incident_service_stub"].CancelIncidentRoleHandover
