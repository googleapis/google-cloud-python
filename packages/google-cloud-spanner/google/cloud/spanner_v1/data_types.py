# Copyright 2021 Google LLC
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

"""Custom data types for spanner."""

import json


class JsonObject(dict):
    """
    JsonObject type help format Django JSONField to compatible Cloud Spanner's
    JSON type. Before making queries, it'll help differentiate between
    normal parameters and JSON parameters.
    """

    def __init__(self, *args, **kwargs):
        self._is_null = (args, kwargs) == ((), {}) or args == (None,)
        if not self._is_null:
            super(JsonObject, self).__init__(*args, **kwargs)

    @classmethod
    def from_str(cls, str_repr):
        """Initiate an object from its `str` representation.

        Args:
            str_repr (str): JSON text representation.

        Returns:
            JsonObject: JSON object.
        """
        if str_repr == "null":
            return cls()

        return cls(json.loads(str_repr))

    def serialize(self):
        """Return the object text representation.

        Returns:
            str: JSON object text representation.
        """
        if self._is_null:
            return None

        return json.dumps(self, sort_keys=True, separators=(",", ":"))
