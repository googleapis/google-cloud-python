# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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
#

import proto  # type: ignore


from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from grafeas.grafeas_v1.types import attestation as g_attestation
from grafeas.grafeas_v1.types import build as g_build
from grafeas.grafeas_v1.types import common
from grafeas.grafeas_v1.types import deployment as g_deployment
from grafeas.grafeas_v1.types import discovery as g_discovery
from grafeas.grafeas_v1.types import image as g_image
from grafeas.grafeas_v1.types import package as g_package
from grafeas.grafeas_v1.types import upgrade as g_upgrade
from grafeas.grafeas_v1.types import vulnerability as g_vulnerability


__protobuf__ = proto.module(
    package="grafeas.v1",
    manifest={
        "Occurrence",
        "Note",
        "GetOccurrenceRequest",
        "ListOccurrencesRequest",
        "ListOccurrencesResponse",
        "DeleteOccurrenceRequest",
        "CreateOccurrenceRequest",
        "UpdateOccurrenceRequest",
        "GetNoteRequest",
        "GetOccurrenceNoteRequest",
        "ListNotesRequest",
        "ListNotesResponse",
        "DeleteNoteRequest",
        "CreateNoteRequest",
        "UpdateNoteRequest",
        "ListNoteOccurrencesRequest",
        "ListNoteOccurrencesResponse",
        "BatchCreateNotesRequest",
        "BatchCreateNotesResponse",
        "BatchCreateOccurrencesRequest",
        "BatchCreateOccurrencesResponse",
    },
)


class Occurrence(proto.Message):
    r"""An instance of an analysis type that has been found on a
    resource.

    Attributes:
        name (str):
            Output only. The name of the occurrence in the form of
            ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.
        resource_uri (str):
            Required. Immutable. A URI that represents the resource for
            which the occurrence applies. For example,
            ``https://gcr.io/project/image@sha256:123abc`` for a Docker
            image.
        note_name (str):
            Required. Immutable. The analysis note associated with this
            occurrence, in the form of
            ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``. This field can
            be used as a filter in list requests.
        kind (~.common.NoteKind):
            Output only. This explicitly denotes which of
            the occurrence details are specified. This field
            can be used as a filter in list requests.
        remediation (str):
            A description of actions that can be taken to
            remedy the note.
        create_time (~.timestamp.Timestamp):
            Output only. The time this occurrence was
            created.
        update_time (~.timestamp.Timestamp):
            Output only. The time this occurrence was
            last updated.
        vulnerability (~.g_vulnerability.VulnerabilityOccurrence):
            Describes a security vulnerability.
        build (~.g_build.BuildOccurrence):
            Describes a verifiable build.
        image (~.g_image.ImageOccurrence):
            Describes how this resource derives from the
            basis in the associated note.
        package (~.g_package.PackageOccurrence):
            Describes the installation of a package on
            the linked resource.
        deployment (~.g_deployment.DeploymentOccurrence):
            Describes the deployment of an artifact on a
            runtime.
        discovery (~.g_discovery.DiscoveryOccurrence):
            Describes when a resource was discovered.
        attestation (~.g_attestation.AttestationOccurrence):
            Describes an attestation of an artifact.
        upgrade (~.g_upgrade.UpgradeOccurrence):
            Describes an available package upgrade on the
            linked resource.
    """

    name = proto.Field(proto.STRING, number=1)

    resource_uri = proto.Field(proto.STRING, number=2)

    note_name = proto.Field(proto.STRING, number=3)

    kind = proto.Field(proto.ENUM, number=4, enum=common.NoteKind,)

    remediation = proto.Field(proto.STRING, number=5)

    create_time = proto.Field(proto.MESSAGE, number=6, message=timestamp.Timestamp,)

    update_time = proto.Field(proto.MESSAGE, number=7, message=timestamp.Timestamp,)

    vulnerability = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="details",
        message=g_vulnerability.VulnerabilityOccurrence,
    )

    build = proto.Field(
        proto.MESSAGE, number=9, oneof="details", message=g_build.BuildOccurrence,
    )

    image = proto.Field(
        proto.MESSAGE, number=10, oneof="details", message=g_image.ImageOccurrence,
    )

    package = proto.Field(
        proto.MESSAGE, number=11, oneof="details", message=g_package.PackageOccurrence,
    )

    deployment = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="details",
        message=g_deployment.DeploymentOccurrence,
    )

    discovery = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof="details",
        message=g_discovery.DiscoveryOccurrence,
    )

    attestation = proto.Field(
        proto.MESSAGE,
        number=14,
        oneof="details",
        message=g_attestation.AttestationOccurrence,
    )

    upgrade = proto.Field(
        proto.MESSAGE, number=15, oneof="details", message=g_upgrade.UpgradeOccurrence,
    )


class Note(proto.Message):
    r"""A type of analysis that can be done for a resource.

    Attributes:
        name (str):
            Output only. The name of the note in the form of
            ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.
        short_description (str):
            A one sentence description of this note.
        long_description (str):
            A detailed description of this note.
        kind (~.common.NoteKind):
            Output only. The type of analysis. This field
            can be used as a filter in list requests.
        related_url (Sequence[~.common.RelatedUrl]):
            URLs associated with this note.
        expiration_time (~.timestamp.Timestamp):
            Time of expiration for this note. Empty if
            note does not expire.
        create_time (~.timestamp.Timestamp):
            Output only. The time this note was created.
            This field can be used as a filter in list
            requests.
        update_time (~.timestamp.Timestamp):
            Output only. The time this note was last
            updated. This field can be used as a filter in
            list requests.
        related_note_names (Sequence[str]):
            Other notes related to this note.
        vulnerability (~.g_vulnerability.VulnerabilityNote):
            A note describing a package vulnerability.
        build (~.g_build.BuildNote):
            A note describing build provenance for a
            verifiable build.
        image (~.g_image.ImageNote):
            A note describing a base image.
        package (~.g_package.PackageNote):
            A note describing a package hosted by various
            package managers.
        deployment (~.g_deployment.DeploymentNote):
            A note describing something that can be
            deployed.
        discovery (~.g_discovery.DiscoveryNote):
            A note describing the initial analysis of a
            resource.
        attestation (~.g_attestation.AttestationNote):
            A note describing an attestation role.
        upgrade (~.g_upgrade.UpgradeNote):
            A note describing available package upgrades.
    """

    name = proto.Field(proto.STRING, number=1)

    short_description = proto.Field(proto.STRING, number=2)

    long_description = proto.Field(proto.STRING, number=3)

    kind = proto.Field(proto.ENUM, number=4, enum=common.NoteKind,)

    related_url = proto.RepeatedField(
        proto.MESSAGE, number=5, message=common.RelatedUrl,
    )

    expiration_time = proto.Field(proto.MESSAGE, number=6, message=timestamp.Timestamp,)

    create_time = proto.Field(proto.MESSAGE, number=7, message=timestamp.Timestamp,)

    update_time = proto.Field(proto.MESSAGE, number=8, message=timestamp.Timestamp,)

    related_note_names = proto.RepeatedField(proto.STRING, number=9)

    vulnerability = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="type",
        message=g_vulnerability.VulnerabilityNote,
    )

    build = proto.Field(
        proto.MESSAGE, number=11, oneof="type", message=g_build.BuildNote,
    )

    image = proto.Field(
        proto.MESSAGE, number=12, oneof="type", message=g_image.ImageNote,
    )

    package = proto.Field(
        proto.MESSAGE, number=13, oneof="type", message=g_package.PackageNote,
    )

    deployment = proto.Field(
        proto.MESSAGE, number=14, oneof="type", message=g_deployment.DeploymentNote,
    )

    discovery = proto.Field(
        proto.MESSAGE, number=15, oneof="type", message=g_discovery.DiscoveryNote,
    )

    attestation = proto.Field(
        proto.MESSAGE, number=16, oneof="type", message=g_attestation.AttestationNote,
    )

    upgrade = proto.Field(
        proto.MESSAGE, number=17, oneof="type", message=g_upgrade.UpgradeNote,
    )


class GetOccurrenceRequest(proto.Message):
    r"""Request to get an occurrence.

    Attributes:
        name (str):
            The name of the occurrence in the form of
            ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.
    """

    name = proto.Field(proto.STRING, number=1)


class ListOccurrencesRequest(proto.Message):
    r"""Request to list occurrences.

    Attributes:
        parent (str):
            The name of the project to list occurrences for in the form
            of ``projects/[PROJECT_ID]``.
        filter (str):
            The filter expression.
        page_size (int):
            Number of occurrences to return in the list.
            Must be positive. Max allowed page size is 1000.
            If not specified, page size defaults to 20.
        page_token (str):
            Token to provide to skip to a particular spot
            in the list.
    """

    parent = proto.Field(proto.STRING, number=1)

    filter = proto.Field(proto.STRING, number=2)

    page_size = proto.Field(proto.INT32, number=3)

    page_token = proto.Field(proto.STRING, number=4)


class ListOccurrencesResponse(proto.Message):
    r"""Response for listing occurrences.

    Attributes:
        occurrences (Sequence[~.grafeas.Occurrence]):
            The occurrences requested.
        next_page_token (str):
            The next pagination token in the list response. It should be
            used as ``page_token`` for the following request. An empty
            value means no more results.
    """

    @property
    def raw_page(self):
        return self

    occurrences = proto.RepeatedField(proto.MESSAGE, number=1, message=Occurrence,)

    next_page_token = proto.Field(proto.STRING, number=2)


class DeleteOccurrenceRequest(proto.Message):
    r"""Request to delete an occurrence.

    Attributes:
        name (str):
            The name of the occurrence in the form of
            ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.
    """

    name = proto.Field(proto.STRING, number=1)


class CreateOccurrenceRequest(proto.Message):
    r"""Request to create a new occurrence.

    Attributes:
        parent (str):
            The name of the project in the form of
            ``projects/[PROJECT_ID]``, under which the occurrence is to
            be created.
        occurrence (~.grafeas.Occurrence):
            The occurrence to create.
    """

    parent = proto.Field(proto.STRING, number=1)

    occurrence = proto.Field(proto.MESSAGE, number=2, message=Occurrence,)


class UpdateOccurrenceRequest(proto.Message):
    r"""Request to update an occurrence.

    Attributes:
        name (str):
            The name of the occurrence in the form of
            ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.
        occurrence (~.grafeas.Occurrence):
            The updated occurrence.
        update_mask (~.field_mask.FieldMask):
            The fields to update.
    """

    name = proto.Field(proto.STRING, number=1)

    occurrence = proto.Field(proto.MESSAGE, number=2, message=Occurrence,)

    update_mask = proto.Field(proto.MESSAGE, number=3, message=field_mask.FieldMask,)


class GetNoteRequest(proto.Message):
    r"""Request to get a note.

    Attributes:
        name (str):
            The name of the note in the form of
            ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.
    """

    name = proto.Field(proto.STRING, number=1)


class GetOccurrenceNoteRequest(proto.Message):
    r"""Request to get the note to which the specified occurrence is
    attached.

    Attributes:
        name (str):
            The name of the occurrence in the form of
            ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.
    """

    name = proto.Field(proto.STRING, number=1)


class ListNotesRequest(proto.Message):
    r"""Request to list notes.

    Attributes:
        parent (str):
            The name of the project to list notes for in the form of
            ``projects/[PROJECT_ID]``.
        filter (str):
            The filter expression.
        page_size (int):
            Number of notes to return in the list. Must
            be positive. Max allowed page size is 1000. If
            not specified, page size defaults to 20.
        page_token (str):
            Token to provide to skip to a particular spot
            in the list.
    """

    parent = proto.Field(proto.STRING, number=1)

    filter = proto.Field(proto.STRING, number=2)

    page_size = proto.Field(proto.INT32, number=3)

    page_token = proto.Field(proto.STRING, number=4)


class ListNotesResponse(proto.Message):
    r"""Response for listing notes.

    Attributes:
        notes (Sequence[~.grafeas.Note]):
            The notes requested.
        next_page_token (str):
            The next pagination token in the list response. It should be
            used as ``page_token`` for the following request. An empty
            value means no more results.
    """

    @property
    def raw_page(self):
        return self

    notes = proto.RepeatedField(proto.MESSAGE, number=1, message=Note,)

    next_page_token = proto.Field(proto.STRING, number=2)


class DeleteNoteRequest(proto.Message):
    r"""Request to delete a note.

    Attributes:
        name (str):
            The name of the note in the form of
            ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.
    """

    name = proto.Field(proto.STRING, number=1)


class CreateNoteRequest(proto.Message):
    r"""Request to create a new note.

    Attributes:
        parent (str):
            The name of the project in the form of
            ``projects/[PROJECT_ID]``, under which the note is to be
            created.
        note_id (str):
            The ID to use for this note.
        note (~.grafeas.Note):
            The note to create.
    """

    parent = proto.Field(proto.STRING, number=1)

    note_id = proto.Field(proto.STRING, number=2)

    note = proto.Field(proto.MESSAGE, number=3, message=Note,)


class UpdateNoteRequest(proto.Message):
    r"""Request to update a note.

    Attributes:
        name (str):
            The name of the note in the form of
            ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.
        note (~.grafeas.Note):
            The updated note.
        update_mask (~.field_mask.FieldMask):
            The fields to update.
    """

    name = proto.Field(proto.STRING, number=1)

    note = proto.Field(proto.MESSAGE, number=2, message=Note,)

    update_mask = proto.Field(proto.MESSAGE, number=3, message=field_mask.FieldMask,)


class ListNoteOccurrencesRequest(proto.Message):
    r"""Request to list occurrences for a note.

    Attributes:
        name (str):
            The name of the note to list occurrences for in the form of
            ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.
        filter (str):
            The filter expression.
        page_size (int):
            Number of occurrences to return in the list.
        page_token (str):
            Token to provide to skip to a particular spot
            in the list.
    """

    name = proto.Field(proto.STRING, number=1)

    filter = proto.Field(proto.STRING, number=2)

    page_size = proto.Field(proto.INT32, number=3)

    page_token = proto.Field(proto.STRING, number=4)


class ListNoteOccurrencesResponse(proto.Message):
    r"""Response for listing occurrences for a note.

    Attributes:
        occurrences (Sequence[~.grafeas.Occurrence]):
            The occurrences attached to the specified
            note.
        next_page_token (str):
            Token to provide to skip to a particular spot
            in the list.
    """

    @property
    def raw_page(self):
        return self

    occurrences = proto.RepeatedField(proto.MESSAGE, number=1, message=Occurrence,)

    next_page_token = proto.Field(proto.STRING, number=2)


class BatchCreateNotesRequest(proto.Message):
    r"""Request to create notes in batch.

    Attributes:
        parent (str):
            The name of the project in the form of
            ``projects/[PROJECT_ID]``, under which the notes are to be
            created.
        notes (Sequence[~.grafeas.BatchCreateNotesRequest.NotesEntry]):
            The notes to create. Max allowed length is
            1000.
    """

    parent = proto.Field(proto.STRING, number=1)

    notes = proto.MapField(proto.STRING, proto.MESSAGE, number=2, message=Note,)


class BatchCreateNotesResponse(proto.Message):
    r"""Response for creating notes in batch.

    Attributes:
        notes (Sequence[~.grafeas.Note]):
            The notes that were created.
    """

    notes = proto.RepeatedField(proto.MESSAGE, number=1, message=Note,)


class BatchCreateOccurrencesRequest(proto.Message):
    r"""Request to create occurrences in batch.

    Attributes:
        parent (str):
            The name of the project in the form of
            ``projects/[PROJECT_ID]``, under which the occurrences are
            to be created.
        occurrences (Sequence[~.grafeas.Occurrence]):
            The occurrences to create. Max allowed length
            is 1000.
    """

    parent = proto.Field(proto.STRING, number=1)

    occurrences = proto.RepeatedField(proto.MESSAGE, number=2, message=Occurrence,)


class BatchCreateOccurrencesResponse(proto.Message):
    r"""Response for creating occurrences in batch.

    Attributes:
        occurrences (Sequence[~.grafeas.Occurrence]):
            The occurrences that were created.
    """

    occurrences = proto.RepeatedField(proto.MESSAGE, number=1, message=Occurrence,)


__all__ = tuple(sorted(__protobuf__.manifest))
