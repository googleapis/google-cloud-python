# Copyright 2018 Google LLC
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

from unittest import mock

from api_factory.generator.loader import TemplateLoader


def test_service_templates():
    loader = TemplateLoader(searchpath='<<< IRRELEVANT >>>')
    with mock.patch.object(loader, 'list_templates') as list_templates:
        list_templates.return_value = [
            '_base.j2', 'foo.j2', 'bar.j2',
            'service/spam.j2', 'service/eggs.j2', 'service/py/spameggs.j2',
        ]
        assert loader.service_templates == {
            'service/spam.j2', 'service/eggs.j2', 'service/py/spameggs.j2',
        }


def test_api_templates():
    loader = TemplateLoader(searchpath='<<< IRRELEVANT >>>')
    with mock.patch.object(loader, 'list_templates') as list_templates:
        list_templates.return_value = [
            '_base.j2', 'foo.j2', 'bar.j2',
            'service/spam.j2', 'service/eggs.j2', 'service/py/spameggs.j2',
        ]
        assert loader.api_templates == {'foo.j2', 'bar.j2'}
