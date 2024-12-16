# Copyright 2024 Google LLC
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


import os.path


def test_template_notebook_exists():
    # This notebook is meant for being used as a BigFrames usage template and
    # could be dynamically linked in places such as BQ Studio and IDE extensions.
    # Let's make sure it exists in the well known path.
    assert os.path.exists("notebooks/getting_started/bq_dataframes_template.ipynb")
