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


class TestPartOfSpeech(unittest.TestCase):

    def _getTargetClass(self):
        from gcloud.language.token import PartOfSpeech
        return PartOfSpeech

    def test_reverse(self):
        klass = self._getTargetClass()
        for attr in dir(klass):
            if attr.startswith('_'):
                continue
            if attr.islower():
                continue
            value = getattr(klass, attr)
            result = klass.reverse(value)
            self.assertEqual(result, attr)


class TestToken(unittest.TestCase):

    def _getTargetClass(self):
        from gcloud.language.token import Token
        return Token

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_constructor(self):
        from gcloud.language.token import PartOfSpeech

        text_content = 'All'
        text_begin = -1
        part_of_speech = PartOfSpeech.DETERMINER
        edge_index = 3
        edge_label = 'PREDET'
        lemma = 'All'
        token = self._makeOne(text_content, text_begin, part_of_speech,
                              edge_index, edge_label, lemma)
        self.assertEqual(token.text_content, text_content)
        self.assertEqual(token.text_begin, text_begin)
        self.assertEqual(token.part_of_speech, part_of_speech)
        self.assertEqual(token.edge_index, edge_index)
        self.assertEqual(token.edge_label, edge_label)
        self.assertEqual(token.lemma, lemma)
