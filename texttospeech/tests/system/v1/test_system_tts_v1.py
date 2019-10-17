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

from google.cloud import texttospeech_v1


class TestSystemSpeech(object):
    def test_synthesize_speech(self):
        client = texttospeech_v1.TextToSpeechClient()

        synthesis_input = texttospeech_v1.types.SynthesisInput(text="Hello, World!")
        voice = texttospeech_v1.types.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech_v1.enums.SsmlVoiceGender.NEUTRAL,
        )
        audio_config = texttospeech_v1.types.AudioConfig(
            audio_encoding=texttospeech_v1.enums.AudioEncoding.MP3
        )

        response = client.synthesize_speech(synthesis_input, voice, audio_config)
        assert response.audio_content is not None

    def test_list_voices(self):
        client = texttospeech_v1.TextToSpeechClient()

        voices = client.list_voices()
        assert len(voices.voices) > 0
