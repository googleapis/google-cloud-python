# Copyright 2016 Google Inc.
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

SYNC_RECOGNIZE_RESPONSE = {
    'results': [
        {
            'alternatives': [
                {
                    'transcript': 'hello',
                    'confidence': 0.784919,
                },
            ],
        },
    ],
}

SYNC_RECOGNIZE_EMPTY_RESPONSE = {
    'results': [],
}

ASYNC_RECOGNIZE_RESPONSE = {
    'name': '123456789',
}

OPERATION_COMPLETE_RESPONSE = {
    'name': '123456789',
    'metadata': {
        '@type': ('type.googleapis.com/'
                  'google.cloud.speech.v1beta1.AsyncRecognizeMetadata'),
        'progressPercent': 100,
        'startTime': '2016-09-22T17:52:25.536964Z',
        'lastUpdateTime': '2016-09-22T17:52:27.802902Z',
    },
    'done': True,
    'response': {
        '@type': ('type.googleapis.com/'
                  'google.cloud.speech.v1beta1.AsyncRecognizeResponse'),
        'results': [
            {
                'alternatives': [
                    {
                        'transcript': 'how old is the Brooklyn Bridge',
                        'confidence': 0.98267895,
                    },
                ],
            },
        ],
    },
}

OPERATION_INCOMPLETE_RESPONSE = {
    'name': '123456789',
    'metadata': {
        '@type': ('type.googleapis.com/'
                  'google.cloud.speech.v1beta1.AsyncRecognizeMetadata'),
        'progressPercent': 27,
        'startTime': '2016-09-22T17:52:25.536964Z',
        'lastUpdateTime': '2016-09-22T17:52:27.802902Z',
    },
    'done': False,
}
