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

from .services.grafeas import GrafeasClient
from .types.attestation import AttestationNote
from .types.attestation import AttestationOccurrence
from .types.build import BuildNote
from .types.build import BuildOccurrence
from .types.common import NoteKind
from .types.common import RelatedUrl
from .types.common import Signature
from .types.cvss import CVSSv3
from .types.deployment import DeploymentNote
from .types.deployment import DeploymentOccurrence
from .types.discovery import DiscoveryNote
from .types.discovery import DiscoveryOccurrence
from .types.grafeas import BatchCreateNotesRequest
from .types.grafeas import BatchCreateNotesResponse
from .types.grafeas import BatchCreateOccurrencesRequest
from .types.grafeas import BatchCreateOccurrencesResponse
from .types.grafeas import CreateNoteRequest
from .types.grafeas import CreateOccurrenceRequest
from .types.grafeas import DeleteNoteRequest
from .types.grafeas import DeleteOccurrenceRequest
from .types.grafeas import GetNoteRequest
from .types.grafeas import GetOccurrenceNoteRequest
from .types.grafeas import GetOccurrenceRequest
from .types.grafeas import ListNoteOccurrencesRequest
from .types.grafeas import ListNoteOccurrencesResponse
from .types.grafeas import ListNotesRequest
from .types.grafeas import ListNotesResponse
from .types.grafeas import ListOccurrencesRequest
from .types.grafeas import ListOccurrencesResponse
from .types.grafeas import Note
from .types.grafeas import Occurrence
from .types.grafeas import UpdateNoteRequest
from .types.grafeas import UpdateOccurrenceRequest
from .types.image import Fingerprint
from .types.image import ImageNote
from .types.image import ImageOccurrence
from .types.image import Layer
from .types.package import Architecture
from .types.package import Distribution
from .types.package import Location
from .types.package import PackageNote
from .types.package import PackageOccurrence
from .types.package import Version
from .types.provenance import AliasContext
from .types.provenance import Artifact
from .types.provenance import BuildProvenance
from .types.provenance import CloudRepoSourceContext
from .types.provenance import Command
from .types.provenance import FileHashes
from .types.provenance import GerritSourceContext
from .types.provenance import GitSourceContext
from .types.provenance import Hash
from .types.provenance import ProjectRepoId
from .types.provenance import RepoId
from .types.provenance import Source
from .types.provenance import SourceContext
from .types.upgrade import UpgradeDistribution
from .types.upgrade import UpgradeNote
from .types.upgrade import UpgradeOccurrence
from .types.upgrade import WindowsUpdate
from .types.vulnerability import Severity
from .types.vulnerability import VulnerabilityNote
from .types.vulnerability import VulnerabilityOccurrence


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
    "GrafeasClient",
)
