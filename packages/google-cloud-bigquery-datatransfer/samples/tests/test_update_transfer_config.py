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

from .. import create_scheduled_query, update_transfer_config


def test_update_config_sample(project_id, dataset_id, capsys, to_delete):
    config_name = create_scheduled_query.sample_create_transfer_config(
        project_id, dataset_id
    )

    display_name = "Transfer config updated"
    config = update_transfer_config.sample_update_transfer_config(config_name, display_name)
    to_delete.append(config.name)
    out, err = capsys.readouterr()
    assert config.name in out
    assert config.display_name == display_name
