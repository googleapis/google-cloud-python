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

"""Wrappers for protocol buffer enum types."""

import enum


class Artifact(object):
    class Type(enum.IntEnum):
        """
        Possible types of an artifact.

        Attributes:
          TYPE_UNSPECIFIED (int): External type is unspecified.
          TYPE_URL (int): URL.
          TYPE_JIRA_ISSUE (int): A JIRA issue.
        """

        TYPE_UNSPECIFIED = 0
        TYPE_URL = 1
        TYPE_JIRA_ISSUE = 4


class Incident(object):
    class EscalationLevel(enum.IntEnum):
        """
        Specifies the escalation level of this incident, within the IRM protocol
        for handling incidents.

        Attributes:
          ESCALATION_LEVEL_UNSPECIFIED (int): The incident has not been escalated. This is the value used by all new
          and legacy incidents.
          ESCALATION_LEVEL_ORGANIZATION (int): The incident has been escalated to the organizational level.
        """

        ESCALATION_LEVEL_UNSPECIFIED = 0
        ESCALATION_LEVEL_ORGANIZATION = 1

    class Severity(enum.IntEnum):
        """
        Severity of an incident.

        Attributes:
          SEVERITY_UNSPECIFIED (int): Severity is not specified.
          SEVERITY_HUGE (int): Huge incident.
          SEVERITY_MAJOR (int): Major incident.
          SEVERITY_MEDIUM (int): Medium incident.
          SEVERITY_MINOR (int): Minor incident.
          SEVERITY_NEGLIGIBLE (int): Negligible incident.
        """

        SEVERITY_UNSPECIFIED = 0
        SEVERITY_HUGE = 1
        SEVERITY_MAJOR = 2
        SEVERITY_MEDIUM = 3
        SEVERITY_MINOR = 4
        SEVERITY_NEGLIGIBLE = 5

    class Stage(enum.IntEnum):
        """
        Stage of an incident.

        Attributes:
          STAGE_UNSPECIFIED (int): This is the default value if no stage has been specified.
          Note: The caller of the API should set the stage to DETECTED.
          STAGE_DETECTED (int): The incident has been detected. This is the initial stage of a new
          incident.
          Note: The caller still has to set the stage manually.
          STAGE_TRIAGED (int): This incident has been formally characterized.
          STAGE_MITIGATED (int): This incident has been mitigated, i.e. does not affect the service level
          anymore.
          STAGE_RESOLVED (int): This incident has been fully resolved, i.e. there are no immediate
          follow-up tasks.
          STAGE_DOCUMENTED (int): Postmortem for the incident was written.
          STAGE_DUPLICATE (int): Stage for an incident with ``duplicate_incident``. This incident is not
          authoritative anymore and the ``duplicate_incident`` should be used to
          determine the stage.
        """

        STAGE_UNSPECIFIED = 0
        STAGE_DETECTED = 4
        STAGE_TRIAGED = 1
        STAGE_MITIGATED = 2
        STAGE_RESOLVED = 3
        STAGE_DOCUMENTED = 5
        STAGE_DUPLICATE = 6

    class CommunicationVenue(object):
        class ChannelType(enum.IntEnum):
            """
            The type of channel/venue for incident communications.

            Attributes:
              CHANNEL_TYPE_UNSPECIFIED (int): An unspecified communication channel.
              CHANNEL_TYPE_URI (int): A communication channel that is represented by a generic URI.
              CHANNEL_TYPE_SLACK (int): A communication channel that represents a Slack channel.
            """

            CHANNEL_TYPE_UNSPECIFIED = 0
            CHANNEL_TYPE_URI = 1
            CHANNEL_TYPE_SLACK = 5


class IncidentRole(object):
    class Type(enum.IntEnum):
        """
        List of possible roles.

        Attributes:
          TYPE_UNSPECIFIED (int): The role is unspecified.
          TYPE_INCIDENT_COMMANDER (int): Incident Commander: Manages response plan, near-term and long-term
          objectives, establishes priorities, and delegates tasks as needed.
          TYPE_COMMUNICATIONS_LEAD (int): Communications Lead: Keeps everybody outside and within the response team
          informed.
          TYPE_OPERATIONS_LEAD (int): Operations Lead: Figures out what to do, and gets it done.
          TYPE_EXTERNAL_CUSTOMER_COMMUNICATIONS_LEAD (int): External Customer Communications Lead: Responsible for communicating
          incident details to customers/public.
          TYPE_PRIMARY_ONCALL (int): Primary Oncall: Responds to the initial page and handles all
          responsibilities for pre-escalated incidents.
          TYPE_SECONDARY_ONCALL (int): Secondary Oncall: Helps the primary oncall if necessary; mostly useful
          for pre-escalated incidents.
          TYPE_OTHER (int): User-specified roles. One example is a Planning Lead, who keeps track of
          the incident. Another is an assistant Incident Commander.
        """

        TYPE_UNSPECIFIED = 0
        TYPE_INCIDENT_COMMANDER = 1
        TYPE_COMMUNICATIONS_LEAD = 2
        TYPE_OPERATIONS_LEAD = 3
        TYPE_EXTERNAL_CUSTOMER_COMMUNICATIONS_LEAD = 4
        TYPE_PRIMARY_ONCALL = 5
        TYPE_SECONDARY_ONCALL = 6
        TYPE_OTHER = 7


class Signal(object):
    class State(enum.IntEnum):
        """
        Describes whether the alerting condition is still firing.

        Attributes:
          STATE_UNSPECIFIED (int): Unspecified
          STATE_OPEN (int): Firing
          STATE_CLOSED (int): Non-firing
        """

        STATE_UNSPECIFIED = 0
        STATE_OPEN = 1
        STATE_CLOSED = 2


class Subscription(object):
    class EventType(enum.IntEnum):
        """
        Types of changes that users can subscribe to in an incident.

        Attributes:
          EVENT_TYPE_UNSPECIFIED (int): An event_type that's not specified is an error.
          EVENT_TYPE_TITLE_CHANGE (int): The incident's title has changed.
          EVENT_TYPE_SYNOPSIS_CHANGE (int): The incident's synopsis has changed.
          EVENT_TYPE_STAGE_CHANGE (int): The incident's stage has changed.
          EVENT_TYPE_SEVERITY_CHANGE (int): The incident's severity has changed.
          EVENT_TYPE_ANNOTATION_ADD (int): A new annotation has been added to the incident.
          EVENT_TYPE_ANNOTATION_CHANGE (int): An annotation has been modified.
        """

        EVENT_TYPE_UNSPECIFIED = 0
        EVENT_TYPE_TITLE_CHANGE = 1
        EVENT_TYPE_SYNOPSIS_CHANGE = 2
        EVENT_TYPE_STAGE_CHANGE = 3
        EVENT_TYPE_SEVERITY_CHANGE = 4
        EVENT_TYPE_ANNOTATION_ADD = 5
        EVENT_TYPE_ANNOTATION_CHANGE = 6
