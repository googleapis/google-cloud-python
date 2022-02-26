# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from grafeas.grafeas_v1.services.grafeas.client import GrafeasClient
from grafeas.grafeas_v1.services.grafeas.async_client import GrafeasAsyncClient

from grafeas.grafeas_v1.types.attestation import AttestationNote
from grafeas.grafeas_v1.types.attestation import AttestationOccurrence
from grafeas.grafeas_v1.types.attestation import Jwt
from grafeas.grafeas_v1.types.build import BuildNote
from grafeas.grafeas_v1.types.build import BuildOccurrence
from grafeas.grafeas_v1.types.common import Envelope
from grafeas.grafeas_v1.types.common import EnvelopeSignature
from grafeas.grafeas_v1.types.common import RelatedUrl
from grafeas.grafeas_v1.types.common import Signature
from grafeas.grafeas_v1.types.common import NoteKind
from grafeas.grafeas_v1.types.compliance import ComplianceNote
from grafeas.grafeas_v1.types.compliance import ComplianceOccurrence
from grafeas.grafeas_v1.types.compliance import ComplianceVersion
from grafeas.grafeas_v1.types.compliance import NonCompliantFile
from grafeas.grafeas_v1.types.cvss import CVSS
from grafeas.grafeas_v1.types.cvss import CVSSv3
from grafeas.grafeas_v1.types.deployment import DeploymentNote
from grafeas.grafeas_v1.types.deployment import DeploymentOccurrence
from grafeas.grafeas_v1.types.discovery import DiscoveryNote
from grafeas.grafeas_v1.types.discovery import DiscoveryOccurrence
from grafeas.grafeas_v1.types.dsse_attestation import DSSEAttestationNote
from grafeas.grafeas_v1.types.dsse_attestation import DSSEAttestationOccurrence
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
from grafeas.grafeas_v1.types.intoto_provenance import BuilderConfig
from grafeas.grafeas_v1.types.intoto_provenance import Completeness
from grafeas.grafeas_v1.types.intoto_provenance import InTotoProvenance
from grafeas.grafeas_v1.types.intoto_provenance import Metadata
from grafeas.grafeas_v1.types.intoto_provenance import Recipe
from grafeas.grafeas_v1.types.intoto_statement import InTotoStatement
from grafeas.grafeas_v1.types.intoto_statement import Subject
from grafeas.grafeas_v1.types.package import Distribution
from grafeas.grafeas_v1.types.package import Location
from grafeas.grafeas_v1.types.package import PackageNote
from grafeas.grafeas_v1.types.package import PackageOccurrence
from grafeas.grafeas_v1.types.package import Version
from grafeas.grafeas_v1.types.package import Architecture
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
from grafeas.grafeas_v1.types.severity import Severity
from grafeas.grafeas_v1.types.slsa_provenance import SlsaProvenance
from grafeas.grafeas_v1.types.upgrade import UpgradeDistribution
from grafeas.grafeas_v1.types.upgrade import UpgradeNote
from grafeas.grafeas_v1.types.upgrade import UpgradeOccurrence
from grafeas.grafeas_v1.types.upgrade import WindowsUpdate
from grafeas.grafeas_v1.types.vulnerability import VulnerabilityNote
from grafeas.grafeas_v1.types.vulnerability import VulnerabilityOccurrence

__all__ = (
    "GrafeasClient",
    "GrafeasAsyncClient",
    "AttestationNote",
    "AttestationOccurrence",
    "Jwt",
    "BuildNote",
    "BuildOccurrence",
    "Envelope",
    "EnvelopeSignature",
    "RelatedUrl",
    "Signature",
    "NoteKind",
    "ComplianceNote",
    "ComplianceOccurrence",
    "ComplianceVersion",
    "NonCompliantFile",
    "CVSS",
    "CVSSv3",
    "DeploymentNote",
    "DeploymentOccurrence",
    "DiscoveryNote",
    "DiscoveryOccurrence",
    "DSSEAttestationNote",
    "DSSEAttestationOccurrence",
    "BatchCreateNotesRequest",
    "BatchCreateNotesResponse",
    "BatchCreateOccurrencesRequest",
    "BatchCreateOccurrencesResponse",
    "CreateNoteRequest",
    "CreateOccurrenceRequest",
    "DeleteNoteRequest",
    "DeleteOccurrenceRequest",
    "GetNoteRequest",
    "GetOccurrenceNoteRequest",
    "GetOccurrenceRequest",
    "ListNoteOccurrencesRequest",
    "ListNoteOccurrencesResponse",
    "ListNotesRequest",
    "ListNotesResponse",
    "ListOccurrencesRequest",
    "ListOccurrencesResponse",
    "Note",
    "Occurrence",
    "UpdateNoteRequest",
    "UpdateOccurrenceRequest",
    "Fingerprint",
    "ImageNote",
    "ImageOccurrence",
    "Layer",
    "BuilderConfig",
    "Completeness",
    "InTotoProvenance",
    "Metadata",
    "Recipe",
    "InTotoStatement",
    "Subject",
    "Distribution",
    "Location",
    "PackageNote",
    "PackageOccurrence",
    "Version",
    "Architecture",
    "AliasContext",
    "Artifact",
    "BuildProvenance",
    "CloudRepoSourceContext",
    "Command",
    "FileHashes",
    "GerritSourceContext",
    "GitSourceContext",
    "Hash",
    "ProjectRepoId",
    "RepoId",
    "Source",
    "SourceContext",
    "Severity",
    "SlsaProvenance",
    "UpgradeDistribution",
    "UpgradeNote",
    "UpgradeOccurrence",
    "WindowsUpdate",
    "VulnerabilityNote",
    "VulnerabilityOccurrence",
)
