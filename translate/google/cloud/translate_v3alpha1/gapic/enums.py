# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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


class Glossary(object):
    class GlossaryType(enum.IntEnum):
        """
        Glossary type.

        Attributes:
          GLOSSARY_TYPE_UNSPECIFIED (int): Invalid.
          UNIDIRECTIONAL (int): A single language pair e.g., CSV file with source=>target mapping.
          EQUIVALENT_TERMS_SET (int): Any language pair from a set of supported languages e.g., GTT glossaries.
        """

        GLOSSARY_TYPE_UNSPECIFIED = 0
        UNIDIRECTIONAL = 1
        EQUIVALENT_TERMS_SET = 2
