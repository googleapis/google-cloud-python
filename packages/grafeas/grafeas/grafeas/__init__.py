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

from grafeas.grafeas_v1.services.grafeas.async_client import GrafeasAsyncClient
from grafeas.grafeas_v1.services.grafeas.client import GrafeasClient
from grafeas.grafeas_v1.types.attestation import AttestationNote
from grafeas.grafeas_v1.types.attestation import AttestationOccurrence
from grafeas.grafeas_v1.types.build import BuildNote
from grafeas.grafeas_v1.types.build import BuildOccurrence
from grafeas.grafeas_v1.types.common import NoteKind
from grafeas.grafeas_v1.types.common import RelatedUrl
from grafeas.grafeas_v1.types.common import Signature
from grafeas.grafeas_v1.types.cvss import CVSSv3
from grafeas.grafeas_v1.types.deployment import DeploymentNote
from grafeas.grafeas_v1.types.deployment import DeploymentOccurrence
from grafeas.grafeas_v1.types.discovery import DiscoveryNote
from grafeas.grafeas_v1.types.discovery import DiscoveryOccurrence
from grafeas.grafeas_v1.types.grafeas import BatchCreateNotesRequest
from grafeas.grafeas_v1.types.grafeas import BatchCreateNotesResponse
from grafeas.grafeas_v1.types.grafeas import BatchCreateOccurrencesRequest
from grafeas.grafeas_v1.types.grafeas import BatchCreateOccurrencesResponse
from grafeas.grafeas_v1.types.grafeas import CreateNoteRequest
from grafeas.grafeas_v1.types.grafeas import CreateOccurrenceRequest
from grafeas.grafeas_v1.types.grafeas import DeleteNoteRequest
from grafeas.grafeas_v1.types.grafeas import DeleteOccurrenceRequest
from grafeas.grafeas_v1.types.grafeas import GetNoteRequest
from grafeas.grafeas_v1.types.grafeas import GetOccurrenceNoteRequest
from grafeas.grafeas_v1.types.grafeas import GetOccurrenceRequest
from grafeas.grafeas_v1.types.grafeas import ListNoteOccurrencesRequest
from grafeas.grafeas_v1.types.grafeas import ListNoteOccurrencesResponse
from grafeas.grafeas_v1.types.grafeas import ListNotesRequest
from grafeas.grafeas_v1.types.grafeas import ListNotesResponse
from grafeas.grafeas_v1.types.grafeas import ListOccurrencesRequest
from grafeas.grafeas_v1.types.grafeas import ListOccurrencesResponse
from grafeas.grafeas_v1.types.grafeas import Note
from grafeas.grafeas_v1.types.grafeas import Occurrence
from grafeas.grafeas_v1.types.grafeas import UpdateNoteRequest
from grafeas.grafeas_v1.types.grafeas import UpdateOccurrenceRequest
from grafeas.grafeas_v1.types.image import Fingerprint
from grafeas.grafeas_v1.types.image import ImageNote
from grafeas.grafeas_v1.types.image import ImageOccurrence
from grafeas.grafeas_v1.types.image import Layer
from grafeas.grafeas_v1.types.package import Architecture
from grafeas.grafeas_v1.types.package import Distribution
from grafeas.grafeas_v1.types.package import Location
from grafeas.grafeas_v1.types.package import PackageNote
from grafeas.grafeas_v1.types.package import PackageOccurrence
from grafeas.grafeas_v1.types.package import Version
from grafeas.grafeas_v1.types.provenance import AliasContext
from grafeas.grafeas_v1.types.provenance import Artifact
from grafeas.grafeas_v1.types.provenance import BuildProvenance
from grafeas.grafeas_v1.types.provenance import CloudRepoSourceContext
from grafeas.grafeas_v1.types.provenance import Command
from grafeas.grafeas_v1.types.provenance import FileHashes
from grafeas.grafeas_v1.types.provenance import GerritSourceContext
from grafeas.grafeas_v1.types.provenance import GitSourceContext
from grafeas.grafeas_v1.types.provenance import Hash
from grafeas.grafeas_v1.types.provenance import ProjectRepoId
from grafeas.grafeas_v1.types.provenance import RepoId
from grafeas.grafeas_v1.types.provenance import Source
from grafeas.grafeas_v1.types.provenance import SourceContext
from grafeas.grafeas_v1.types.upgrade import UpgradeDistribution
from grafeas.grafeas_v1.types.upgrade import UpgradeNote
from grafeas.grafeas_v1.types.upgrade import UpgradeOccurrence
from grafeas.grafeas_v1.types.upgrade import WindowsUpdate
from grafeas.grafeas_v1.types.vulnerability import Severity
from grafeas.grafeas_v1.types.vulnerability import VulnerabilityNote
from grafeas.grafeas_v1.types.vulnerability import VulnerabilityOccurrence

__all__ = (
    "AliasContext",
    "Architecture",
    "Artifact",
    "AttestationNote",
    "AttestationOccurrence",
    "BatchCreateNotesRequest",
    "BatchCreateNotesResponse",
    "BatchCreateOccurrencesRequest",
    "BatchCreateOccurrencesResponse",
    "BuildNote",
    "BuildOccurrence",
    "BuildProvenance",
    "CVSSv3",
    "CloudRepoSourceContext",
    "Command",
    "CreateNoteRequest",
    "CreateOccurrenceRequest",
    "DeleteNoteRequest",
    "DeleteOccurrenceRequest",
    "DeploymentNote",
    "DeploymentOccurrence",
    "DiscoveryNote",
    "DiscoveryOccurrence",
    "Distribution",
    "FileHashes",
    "Fingerprint",
    "GerritSourceContext",
    "GetNoteRequest",
    "GetOccurrenceNoteRequest",
    "GetOccurrenceRequest",
    "GitSourceContext",
    "GrafeasAsyncClient",
    "GrafeasClient",
    "Hash",
    "ImageNote",
    "ImageOccurrence",
    "Layer",
    "ListNoteOccurrencesRequest",
    "ListNoteOccurrencesResponse",
    "ListNotesRequest",
    "ListNotesResponse",
    "ListOccurrencesRequest",
    "ListOccurrencesResponse",
    "Location",
    "Note",
    "NoteKind",
    "Occurrence",
    "PackageNote",
    "PackageOccurrence",
    "ProjectRepoId",
    "RelatedUrl",
    "RepoId",
    "Severity",
    "Signature",
    "Source",
    "SourceContext",
    "UpdateNoteRequest",
    "UpdateOccurrenceRequest",
    "UpgradeDistribution",
    "UpgradeNote",
    "UpgradeOccurrence",
    "Version",
    "VulnerabilityNote",
    "VulnerabilityOccurrence",
    "WindowsUpdate",
)
