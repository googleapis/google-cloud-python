# Copyright 2016 Google Inc. All Rights Reserved.
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

import unittest


class TestSentiment(unittest.TestCase):

    def _getTargetClass(self):
        from gcloud.language.sentiment import Sentiment
        return Sentiment

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_constructor(self):
        polarity = 1
        magnitude = 2.3
        sentiment = self._makeOne(polarity, magnitude)
        self.assertEqual(sentiment.polarity, polarity)
        self.assertEqual(sentiment.magnitude, magnitude)

    def test_from_api_repr(self):
        klass = self._getTargetClass()
        polarity = -1
        magnitude = 5.55
        payload = {
            'polarity': polarity,
            'magnitude': magnitude,
        }
        sentiment = klass.from_api_repr(payload)
        self.assertEqual(sentiment.polarity, polarity)
        self.assertEqual(sentiment.magnitude, magnitude)
