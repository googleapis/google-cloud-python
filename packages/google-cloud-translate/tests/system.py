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


import os
import pytest
import unittest

from google.cloud import translate_v2
from google.cloud import translate


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """

    CLIENT_V2 = None
    CLIENT_V3 = None
    location = "global"
    project_id = os.environ["PROJECT_ID"]
    use_mtls = os.environ.get("GOOGLE_API_USE_MTLS_ENDPOINT", "never")


def setUpModule():
    Config.CLIENT_V2 = translate_v2.Client()
    Config.CLIENT_V3 = translate.TranslationServiceClient()


# Only v3/v3beta1 clients have mTLS support, so we need to skip all the
# v2 client tests for mTLS testing.
skip_for_mtls = pytest.mark.skipif(
    Config.use_mtls == "always", reason="Skip the v2 client test for mTLS testing"
)


class TestTranslate(unittest.TestCase):
    @skip_for_mtls
    def test_get_languages(self):
        result = Config.CLIENT_V2.get_languages()
        # There are **many** more than 10 languages.
        self.assertGreater(len(result), 10)

        lang_map = {val["language"]: val["name"] for val in result}
        self.assertEqual(lang_map["en"], "English")
        self.assertEqual(lang_map["ja"], "Japanese")
        self.assertEqual(lang_map["lv"], "Latvian")
        self.assertEqual(lang_map["zu"], "Zulu")

    @skip_for_mtls
    def test_detect_language(self):
        values = ["takoy", "fa\xe7ade", "s'il vous plait"]
        detections = Config.CLIENT_V2.detect_language(values)
        self.assertEqual(len(values), len(detections))
        self.assertEqual(detections[0]["language"], "ru")
        self.assertEqual(detections[1]["language"], "fr")
        self.assertEqual(detections[2]["language"], "fr")

    @skip_for_mtls
    def test_translate(self):
        values = ["petnaest", "dek kvin", "Me llamo Jeff", "My name is Jeff"]
        translations = Config.CLIENT_V2.translate(
            values, target_language="de", model="nmt"
        )
        self.assertEqual(len(values), len(translations))

        self.assertEqual(translations[0]["detectedSourceLanguage"].lower(), "hr")
        self.assertEqual(translations[0]["translatedText"].lower(), "fünfzehn")

        self.assertEqual(translations[1]["detectedSourceLanguage"], "eo")
        self.assertEqual(translations[1]["translatedText"].lower(), "fünfzehn")

        self.assertEqual(translations[2]["detectedSourceLanguage"], "es")
        es_translation = translations[2]["translatedText"].lower()
        self.assertTrue(
            es_translation == "ich heiße jeff" or es_translation == "mein name ist jeff"
        )

        self.assertEqual(translations[3]["detectedSourceLanguage"], "en")
        self.assertEqual(
            translations[3]["translatedText"].lower(), "mein name ist jeff"
        )

    def test_get_languages_v3(self):
        parent = f"projects/{Config.project_id}/locations/{Config.location}"
        result = Config.CLIENT_V3.get_supported_languages(parent=parent)
        languages = [lang.language_code for lang in result.languages]
        self.assertGreater(
            len(languages), 10
        )  # There are **many** more than 10 languages.
        self.assertIn("zu", languages)  # Zulu is supported
        self.assertIn("fr", languages)  # English is supported
        self.assertIn("ga", languages)  # Irish is supported

    def test_detect_language_v3(self):
        parent = f"projects/{Config.project_id}/locations/{Config.location}"
        value = "s'il vous plait"
        response = Config.CLIENT_V3.detect_language(
            request={"parent": parent, "content": value, "mime_type": "text/plain"}
        )
        languages = [detection.language_code for detection in response.languages]
        self.assertEqual(languages[0], "fr")

    def test_translate_v3(self):
        parent = f"projects/{Config.project_id}/locations/{Config.location}"
        values = ["petnaest", "dek kvin", "Me llamo Jeff", "My name is Jeff"]
        translations = Config.CLIENT_V3.translate_text(
            parent=parent, contents=values, target_language_code="de"
        )

        results_map = {
            result.detected_language_code: result.translated_text
            for result in translations.translations
        }
        self.assertEqual(len(values), len(results_map))

        self.assertIn("hr", results_map.keys())
        self.assertIn("eo", results_map.keys())
        self.assertIn("es", results_map.keys())
        self.assertIn("en", results_map.keys())

        self.assertEqual(results_map["hr"].lower(), "fünfzehn")
        self.assertEqual(results_map["eo"].lower(), "fünfzehn")

        es_translation = results_map["es"].lower()
        self.assertTrue(
            es_translation == "ich heiße jeff" or es_translation == "mein name ist jeff"
        )

        self.assertEqual(results_map["en"].lower(), "mein name ist jeff")
