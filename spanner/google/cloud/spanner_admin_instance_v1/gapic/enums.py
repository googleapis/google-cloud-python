# Copyright 2017, Google LLC All rights reserved.
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
"""Wrappers for protocol buffer enum types."""


class Instance(object):
    class State(object):
        """
        Indicates the current state of the instance.

        Attributes:
          STATE_UNSPECIFIED (int): Not specified.
          CREATING (int): The instance is still being created. Resources may not be
          available yet, and operations such as database creation may not
          work.
          READY (int): The instance is fully created and ready to do work such as
          creating databases.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
