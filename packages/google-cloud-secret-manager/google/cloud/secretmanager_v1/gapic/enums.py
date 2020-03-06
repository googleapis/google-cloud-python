# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrappers for protocol buffer enum types."""

import enum


class SecretVersion(object):
    class State(enum.IntEnum):
        """
        The state of a ``SecretVersion``, indicating if it can be accessed.

        Attributes:
          STATE_UNSPECIFIED (int): Not specified. This value is unused and invalid.
          ENABLED (int): The ``SecretVersion`` may be accessed.
          DISABLED (int): The ``SecretVersion`` may not be accessed, but the secret data is
          still available and can be placed back into the ``ENABLED`` state.
          DESTROYED (int): The ``SecretVersion`` is destroyed and the secret data is no longer
          stored. A version may not leave this state once entered.
        """

        STATE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2
        DESTROYED = 3
