# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.cloud.documentai_toolbox.wrappers import EntityWrapper
from google.cloud import documentai


def test_from_documentai_entity():
    test_entity = documentai.Document.Entity(
        mention_text="20,868", type_="vat", id="0", mention_id="", redacted=False
    )

    actual = EntityWrapper.from_documentai_entity(test_entity)

    assert actual.mention_text == "20,868"
    assert actual.type_ == "vat"
