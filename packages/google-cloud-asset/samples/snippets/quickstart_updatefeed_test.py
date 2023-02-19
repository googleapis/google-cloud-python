#!/usr/bin/env python

# Copyright 2018 Google LLC.
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

import pytest

import quickstart_updatefeed


@pytest.mark.parametrize("transport", ["grpc", "rest"])
def test_update_feed(transport, capsys, test_feed, another_topic):
    quickstart_updatefeed.update_feed(
        feed_name=test_feed.name,
        topic=another_topic.name,
        transport=transport,
    )
    out, _ = capsys.readouterr()

    assert "updated_feed" in out
