# -*- coding: utf-8 -*-
# Copyright 2016 Google LLC
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

from google.cloud import translate


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """

    CLIENT = None


def setUpModule():
    Config.CLIENT = translate.Client()


class TestTranslate(unittest.TestCase):
    def test_get_languages(self):
        result = Config.CLIENT.get_languages()
        # There are **many** more than 10 languages.
        self.assertGreater(len(result), 10)

        lang_map = {val["language"]: val["name"] for val in result}
        self.assertEqual(lang_map["en"], "English")
        self.assertEqual(lang_map["ja"], "Japanese")
        self.assertEqual(lang_map["lv"], "Latvian")
        self.assertEqual(lang_map["zu"], "Zulu")

    def test_detect_language(self):
        values = ["takoy", u"fa\xe7ade", "s'il vous plait"]
        detections = Config.CLIENT.detect_language(values)
        self.assertEqual(len(values), len(detections))
        self.assertEqual(detections[0]["language"], "ru")
        self.assertEqual(detections[1]["language"], "fr")
        self.assertEqual(detections[2]["language"], "fr")

    def test_translate(self):
        values = ["petnaest", "dek kvin", "Me llamo Jeff", "My name is Jeff"]
        translations = Config.CLIENT.translate(
            values, target_language="de", model="nmt"
        )
        self.assertEqual(len(values), len(translations))

        self.assertEqual(translations[0]["detectedSourceLanguage"].lower(), "hr")
        self.assertEqual(translations[0]["translatedText"].lower(), u"fünfzehn")

        self.assertEqual(translations[1]["detectedSourceLanguage"], "eo")
        self.assertEqual(translations[1]["translatedText"].lower(), u"fünfzehn")

        self.assertEqual(translations[2]["detectedSourceLanguage"], "es")
        self.assertEqual(translations[2]["translatedText"].lower(), u"ich heiße jeff")

        self.assertEqual(translations[3]["detectedSourceLanguage"], "en")
        self.assertEqual(
            translations[3]["translatedText"].lower(), "mein name ist jeff"
        )
