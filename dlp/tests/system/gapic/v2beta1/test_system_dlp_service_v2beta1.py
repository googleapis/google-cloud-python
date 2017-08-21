# Copyright 2017, Google Inc. All rights reserved.
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

import time
import unittest

from google.cloud import dlp
from google.cloud.dlp import enums
from google.cloud.proto.privacy.dlp.v2beta1 import dlp_pb2


class TestSystemDlpService(unittest.TestCase):
    def test_inspect_content(self):

        client = dlp.DlpServiceClient()
        min_likelihood = enums.Likelihood.POSSIBLE
        inspect_config = {'min_likelihood': min_likelihood}
        type_ = 'text/plain'
        value = 'my phone number is 215-512-1212'
        items_element = {'type': type_, 'value': value}
        items = [items_element]
        response = client.inspect_content(inspect_config, items)
