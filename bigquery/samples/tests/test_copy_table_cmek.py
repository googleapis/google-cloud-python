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


from .. import copy_table_cmek


def test_copy_table_cmek(capsys, client, dataset_id, table_w_data):

    copy_table_cmek.copy_table_cmek(client, dataset_id, table_w_data)
    out, err = capsys.readouterr()
    assert "The process completed" in out
    assert "A copy of the table created" in out
