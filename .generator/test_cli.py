# Copyright 2025 Google LLC
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

from cli import handle_generate, handle_build, handle_configure


def test_handle_configure_dry_run():
    # This is a simple test to ensure that the dry run command succeeds.
    handle_configure(dry_run=True)

def test_handle_generate_dry_run():
    # This is a simple test to ensure that the dry run command succeeds.
    handle_generate(dry_run=True)

def test_handle_build_dry_run():
    # This is a simple test to ensure that the dry run command succeeds.
    handle_build(dry_run=True)
