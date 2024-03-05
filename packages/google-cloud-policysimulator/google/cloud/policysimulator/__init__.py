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
from google.cloud.policysimulator import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.policysimulator_v1.services.simulator.async_client import (
    SimulatorAsyncClient,
)
from google.cloud.policysimulator_v1.services.simulator.client import SimulatorClient
from google.cloud.policysimulator_v1.types.explanations import (
    AccessState,
    AccessTuple,
    BindingExplanation,
    ExplainedPolicy,
    HeuristicRelevance,
)
from google.cloud.policysimulator_v1.types.simulator import (
    AccessStateDiff,
    CreateReplayRequest,
    ExplainedAccess,
    GetReplayRequest,
    ListReplayResultsRequest,
    ListReplayResultsResponse,
    Replay,
    ReplayConfig,
    ReplayDiff,
    ReplayOperationMetadata,
    ReplayResult,
)

__all__ = (
    "SimulatorClient",
    "SimulatorAsyncClient",
    "AccessTuple",
    "BindingExplanation",
    "ExplainedPolicy",
    "AccessState",
    "HeuristicRelevance",
    "AccessStateDiff",
    "CreateReplayRequest",
    "ExplainedAccess",
    "GetReplayRequest",
    "ListReplayResultsRequest",
    "ListReplayResultsResponse",
    "Replay",
    "ReplayConfig",
    "ReplayDiff",
    "ReplayOperationMetadata",
    "ReplayResult",
)
