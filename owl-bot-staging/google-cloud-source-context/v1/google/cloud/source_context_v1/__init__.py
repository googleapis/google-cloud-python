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
from google.cloud.source_context_v1 import gapic_version as package_version

__version__ = package_version.__version__



from .types.source_context import AliasContext
from .types.source_context import CloudRepoSourceContext
from .types.source_context import CloudWorkspaceId
from .types.source_context import CloudWorkspaceSourceContext
from .types.source_context import ExtendedSourceContext
from .types.source_context import GerritSourceContext
from .types.source_context import GitSourceContext
from .types.source_context import ProjectRepoId
from .types.source_context import RepoId
from .types.source_context import SourceContext

__all__ = (
'AliasContext',
'CloudRepoSourceContext',
'CloudWorkspaceId',
'CloudWorkspaceSourceContext',
'ExtendedSourceContext',
'GerritSourceContext',
'GitSourceContext',
'ProjectRepoId',
'RepoId',
'SourceContext',
)
