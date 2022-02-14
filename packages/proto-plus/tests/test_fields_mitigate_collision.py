# Copyright 2022 Google LLC
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

import proto


# Underscores may be appended to field names
# that collide with python or proto-plus keywords.
# In case a key only exists with a `_` suffix, coerce the key
# to include the `_` suffix. Is not possible to
# natively define the same field with a trailing underscore in protobuf.
# See related issue
# https://github.com/googleapis/python-api-core/issues/227
def test_fields_mitigate_collision():
    class TestMessage(proto.Message):
        spam_ = proto.Field(proto.STRING, number=1)
        eggs = proto.Field(proto.STRING, number=2)

    obj = TestMessage(spam_="has_spam")
    obj.eggs = "has_eggs"
    assert obj.spam_ == "has_spam"

    # Test that `spam` is coerced to `spam_`
    modified_obj = TestMessage({"spam": "has_spam", "eggs": "has_eggs"})
    assert modified_obj.spam_ == "has_spam"
