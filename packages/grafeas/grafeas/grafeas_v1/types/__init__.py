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

from .common import (
    RelatedUrl,
    Signature,
)
from .attestation import (
    AttestationNote,
    AttestationOccurrence,
)
from .provenance import (
    BuildProvenance,
    Source,
    FileHashes,
    Hash,
    Command,
    Artifact,
    SourceContext,
    AliasContext,
    CloudRepoSourceContext,
    GerritSourceContext,
    GitSourceContext,
    RepoId,
    ProjectRepoId,
)
from .build import (
    BuildNote,
    BuildOccurrence,
)
from .cvss import CVSSv3
from .deployment import (
    DeploymentNote,
    DeploymentOccurrence,
)
from .discovery import (
    DiscoveryNote,
    DiscoveryOccurrence,
)
from .image import (
    Layer,
    Fingerprint,
    ImageNote,
    ImageOccurrence,
)
from .package import (
    Distribution,
    Location,
    PackageNote,
    PackageOccurrence,
    Version,
)
from .upgrade import (
    UpgradeNote,
    UpgradeDistribution,
    WindowsUpdate,
    UpgradeOccurrence,
)
from .vulnerability import (
    VulnerabilityNote,
    VulnerabilityOccurrence,
)
from .grafeas import (
    Occurrence,
    Note,
    GetOccurrenceRequest,
    ListOccurrencesRequest,
    ListOccurrencesResponse,
    DeleteOccurrenceRequest,
    CreateOccurrenceRequest,
    UpdateOccurrenceRequest,
    GetNoteRequest,
    GetOccurrenceNoteRequest,
    ListNotesRequest,
    ListNotesResponse,
    DeleteNoteRequest,
    CreateNoteRequest,
    UpdateNoteRequest,
    ListNoteOccurrencesRequest,
    ListNoteOccurrencesResponse,
    BatchCreateNotesRequest,
    BatchCreateNotesResponse,
    BatchCreateOccurrencesRequest,
    BatchCreateOccurrencesResponse,
)


__all__ = (
    "RelatedUrl",
    "Signature",
    "AttestationNote",
    "AttestationOccurrence",
    "BuildProvenance",
    "Source",
    "FileHashes",
    "Hash",
    "Command",
    "Artifact",
    "SourceContext",
    "AliasContext",
    "CloudRepoSourceContext",
    "GerritSourceContext",
    "GitSourceContext",
    "RepoId",
    "ProjectRepoId",
    "BuildNote",
    "BuildOccurrence",
    "CVSSv3",
    "DeploymentNote",
    "DeploymentOccurrence",
    "DiscoveryNote",
    "DiscoveryOccurrence",
    "Layer",
    "Fingerprint",
    "ImageNote",
    "ImageOccurrence",
    "Distribution",
    "Location",
    "PackageNote",
    "PackageOccurrence",
    "Version",
    "UpgradeNote",
    "UpgradeDistribution",
    "WindowsUpdate",
    "UpgradeOccurrence",
    "VulnerabilityNote",
    "VulnerabilityOccurrence",
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
)
