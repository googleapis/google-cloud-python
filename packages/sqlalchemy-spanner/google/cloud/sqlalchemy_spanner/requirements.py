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

from sqlalchemy.testing import exclusions
from sqlalchemy.testing.requirements import SuiteRequirements


class Requirements(SuiteRequirements):
    @property
    def schema_reflection(self):
        return exclusions.open()

    @property
    def implicitly_named_constraints(self):
        return exclusions.open()

    @property
    def autocommit(self):
        return exclusions.open()

    @property
    def order_by_collation(self):
        return exclusions.open()

    @property
    def ctes(self):
        return exclusions.open()

    @property
    def isolation_level(self):
        return exclusions.open()

    def get_order_by_collation(self, _):
        """Get the default collation name.

        Returns:
            str: Collation name.
        """
        return '"unicode"'

    def get_isolation_levels(self, _):
        """Get isolation levels supported by the dialect.

        Returns:
            dict: isolation levels description.
        """
        return {"default": "SERIALIZABLE", "supported": ["SERIALIZABLE", "AUTOCOMMIT"]}
