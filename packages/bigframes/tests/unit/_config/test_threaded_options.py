# Copyright 2023 Google LLC
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

import threading

import bigframes._config


def test_mutate_options_threaded():
    options = bigframes._config.Options()
    options.display.max_rows = 50
    result_dict = {"this_before": options.display.max_rows}

    def mutate_options_threaded(options, result_dict):
        result_dict["other_before"] = options.display.max_rows

        options.display.max_rows = 100
        result_dict["other_after"] = options.display.max_rows

    thread = threading.Thread(
        target=(lambda: mutate_options_threaded(options, result_dict))
    )
    thread.start()
    thread.join(1)
    result_dict["this_after"] = options.display.max_rows

    assert result_dict["this_before"] == 50
    assert result_dict["this_after"] == 50
    assert result_dict["other_before"] == 25
    assert result_dict["other_after"] == 100
