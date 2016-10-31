# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Helper functions for logging handlers."""

import math
import json


def format_stackdriver_json(record, message):
    """Helper to format a LogRecord in in Stackdriver fluentd format.

        :rtype: str
        :returns: JSON str to be written to the log file.
    """
    subsecond, second = math.modf(record.created)

    payload = {
        'message': message,
        'timestamp': {
            'seconds': int(second),
            'nanos': int(subsecond * 1e9),
        },
        'thread': record.thread,
        'severity': record.levelname,
    }

    return json.dumps(payload)
