# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.policysimulator_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.simulator import SimulatorClient
from .services.simulator import SimulatorAsyncClient

from .types.explanations import AccessTuple
from .types.explanations import BindingExplanation
from .types.explanations import ExplainedPolicy
from .types.explanations import AccessState
from .types.explanations import HeuristicRelevance
from .types.simulator import AccessStateDiff
from .types.simulator import CreateReplayRequest
from .types.simulator import ExplainedAccess
from .types.simulator import GetReplayRequest
from .types.simulator import ListReplayResultsRequest
from .types.simulator import ListReplayResultsResponse
from .types.simulator import Replay
from .types.simulator import ReplayConfig
from .types.simulator import ReplayDiff
from .types.simulator import ReplayOperationMetadata
from .types.simulator import ReplayResult

__all__ = (
    'SimulatorAsyncClient',
'AccessState',
'AccessStateDiff',
'AccessTuple',
'BindingExplanation',
'CreateReplayRequest',
'ExplainedAccess',
'ExplainedPolicy',
'GetReplayRequest',
'HeuristicRelevance',
'ListReplayResultsRequest',
'ListReplayResultsResponse',
'Replay',
'ReplayConfig',
'ReplayDiff',
'ReplayOperationMetadata',
'ReplayResult',
'SimulatorClient',
)
