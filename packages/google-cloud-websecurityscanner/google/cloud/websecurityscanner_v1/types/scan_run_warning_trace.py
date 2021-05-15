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


__protobuf__ = proto.module(
    package="google.cloud.websecurityscanner.v1", manifest={"ScanRunWarningTrace",},
)


class ScanRunWarningTrace(proto.Message):
    r"""Output only.
    Defines a warning trace message for ScanRun. Warning traces
    provide customers with useful information that helps make the
    scanning process more effective.

    Attributes:
        code (google.cloud.websecurityscanner_v1.types.ScanRunWarningTrace.Code):
            Output only. Indicates the warning code.
    """

    class Code(proto.Enum):
        r"""Output only.
        Defines a warning message code.
        Next id: 6
        """
        CODE_UNSPECIFIED = 0
        INSUFFICIENT_CRAWL_RESULTS = 1
        TOO_MANY_CRAWL_RESULTS = 2
        TOO_MANY_FUZZ_TASKS = 3
        BLOCKED_BY_IAP = 4

    code = proto.Field(proto.ENUM, number=1, enum=Code,)


__all__ = tuple(sorted(__protobuf__.manifest))
