# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from .attestation import (
    AttestationNote,
    AttestationOccurrence,
    Jwt,
)
from .build import (
    BuildNote,
    BuildOccurrence,
)
from .common import (
    Digest,
    Envelope,
    EnvelopeSignature,
    FileLocation,
    License,
    RelatedUrl,
    Signature,
    NoteKind,
)
from .compliance import (
    ComplianceNote,
    ComplianceOccurrence,
    ComplianceVersion,
    NonCompliantFile,
)
from .cvss import (
    CVSS,
    CVSSv3,
    CVSSVersion,
)
from .deployment import (
    DeploymentNote,
    DeploymentOccurrence,
)
from .discovery import (
    DiscoveryNote,
    DiscoveryOccurrence,
)
from .dsse_attestation import (
    DSSEAttestationNote,
    DSSEAttestationOccurrence,
)
from .grafeas import (
    BatchCreateNotesRequest,
    BatchCreateNotesResponse,
    BatchCreateOccurrencesRequest,
    BatchCreateOccurrencesResponse,
    CreateNoteRequest,
    CreateOccurrenceRequest,
    DeleteNoteRequest,
    DeleteOccurrenceRequest,
    GetNoteRequest,
    GetOccurrenceNoteRequest,
    GetOccurrenceRequest,
    ListNoteOccurrencesRequest,
    ListNoteOccurrencesResponse,
    ListNotesRequest,
    ListNotesResponse,
    ListOccurrencesRequest,
    ListOccurrencesResponse,
    Note,
    Occurrence,
    UpdateNoteRequest,
    UpdateOccurrenceRequest,
)
from .image import (
    Fingerprint,
    ImageNote,
    ImageOccurrence,
    Layer,
)
from .intoto_provenance import (
    BuilderConfig,
    Completeness,
    InTotoProvenance,
    Metadata,
    Recipe,
)
from .intoto_statement import (
    InTotoSlsaProvenanceV1,
    InTotoStatement,
    Subject,
)
from .package import (
    Distribution,
    Location,
    PackageNote,
    PackageOccurrence,
    Version,
    Architecture,
)
from .provenance import (
    AliasContext,
    Artifact,
    BuildProvenance,
    CloudRepoSourceContext,
    Command,
    FileHashes,
    GerritSourceContext,
    GitSourceContext,
    Hash,
    ProjectRepoId,
    RepoId,
    Source,
    SourceContext,
)
from .sbom import (
    SbomReferenceIntotoPayload,
    SbomReferenceIntotoPredicate,
    SBOMReferenceNote,
    SBOMReferenceOccurrence,
)
from .severity import (
    Severity,
)
from .slsa_provenance import (
    SlsaProvenance,
)
from .slsa_provenance_zero_two import (
    SlsaProvenanceZeroTwo,
)
from .upgrade import (
    UpgradeDistribution,
    UpgradeNote,
    UpgradeOccurrence,
    WindowsUpdate,
)
from .vex import (
    VulnerabilityAssessmentNote,
)
from .vulnerability import (
    VulnerabilityNote,
    VulnerabilityOccurrence,
)

__all__ = (
    'AttestationNote',
    'AttestationOccurrence',
    'Jwt',
    'BuildNote',
    'BuildOccurrence',
    'Digest',
    'Envelope',
    'EnvelopeSignature',
    'FileLocation',
    'License',
    'RelatedUrl',
    'Signature',
    'NoteKind',
    'ComplianceNote',
    'ComplianceOccurrence',
    'ComplianceVersion',
    'NonCompliantFile',
    'CVSS',
    'CVSSv3',
    'CVSSVersion',
    'DeploymentNote',
    'DeploymentOccurrence',
    'DiscoveryNote',
    'DiscoveryOccurrence',
    'DSSEAttestationNote',
    'DSSEAttestationOccurrence',
    'BatchCreateNotesRequest',
    'BatchCreateNotesResponse',
    'BatchCreateOccurrencesRequest',
    'BatchCreateOccurrencesResponse',
    'CreateNoteRequest',
    'CreateOccurrenceRequest',
    'DeleteNoteRequest',
    'DeleteOccurrenceRequest',
    'GetNoteRequest',
    'GetOccurrenceNoteRequest',
    'GetOccurrenceRequest',
    'ListNoteOccurrencesRequest',
    'ListNoteOccurrencesResponse',
    'ListNotesRequest',
    'ListNotesResponse',
    'ListOccurrencesRequest',
    'ListOccurrencesResponse',
    'Note',
    'Occurrence',
    'UpdateNoteRequest',
    'UpdateOccurrenceRequest',
    'Fingerprint',
    'ImageNote',
    'ImageOccurrence',
    'Layer',
    'BuilderConfig',
    'Completeness',
    'InTotoProvenance',
    'Metadata',
    'Recipe',
    'InTotoSlsaProvenanceV1',
    'InTotoStatement',
    'Subject',
    'Distribution',
    'Location',
    'PackageNote',
    'PackageOccurrence',
    'Version',
    'Architecture',
    'AliasContext',
    'Artifact',
    'BuildProvenance',
    'CloudRepoSourceContext',
    'Command',
    'FileHashes',
    'GerritSourceContext',
    'GitSourceContext',
    'Hash',
    'ProjectRepoId',
    'RepoId',
    'Source',
    'SourceContext',
    'SbomReferenceIntotoPayload',
    'SbomReferenceIntotoPredicate',
    'SBOMReferenceNote',
    'SBOMReferenceOccurrence',
    'Severity',
    'SlsaProvenance',
    'SlsaProvenanceZeroTwo',
    'UpgradeDistribution',
    'UpgradeNote',
    'UpgradeOccurrence',
    'WindowsUpdate',
    'VulnerabilityAssessmentNote',
    'VulnerabilityNote',
    'VulnerabilityOccurrence',
)
