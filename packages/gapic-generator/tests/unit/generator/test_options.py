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

import pytest
from unittest import mock
import warnings

from gapic.generator import options
from gapic.samplegen_utils import types


def test_options_empty():
    opts = options.Options.build('')
    assert len(opts.templates) == 1
    assert opts.templates[0].endswith('gapic/templates')
    assert not opts.lazy_import


def test_options_replace_templates():
    opts = options.Options.build('python-gapic-templates=/foo/')
    assert len(opts.templates) == 1
    assert opts.templates[0] == '/foo/'


def test_options_unrecognized():
    with mock.patch.object(warnings, 'warn') as warn:
        options.Options.build('python-gapic-abc=xyz')
    warn.assert_called_once_with('Unrecognized option: `python-gapic-abc`.')


def test_flags_unrecognized():
    with mock.patch.object(warnings, 'warn') as warn:
        options.Options.build('python-gapic-abc')
    warn.assert_called_once_with('Unrecognized option: `python-gapic-abc`.')


def test_options_unrecognized_likely_typo():
    with mock.patch.object(warnings, 'warn') as warn:
        options.Options.build('go-gapic-abc=xyz')
    assert len(warn.mock_calls) == 0


def test_options_no_valid_sample_config(fs):
    fs.create_file("sampledir/not_a_config.yaml")
    with pytest.raises(types.InvalidConfig):
        options.Options.build("samples=sampledir/")


def test_options_service_config(fs):
    opts = options.Options.build("")
    assert opts.retry is None

    # Default of None is okay, verify build can read a config.
    service_config_fpath = "service_config.json"
    fs.create_file(service_config_fpath, contents="""{
    "methodConfig": [
        {
            "name": [
                {
                  "service": "animalia.mollusca.v1beta1.Cephalopod",
                  "method": "IdentifySquid"
                }
            ],
            "retryPolicy": {
                "maxAttempts": 5,
                "maxBackoff": "3s",
                "initialBackoff": "0.2s",
                "backoffMultiplier": 2,
                "retryableStatusCodes": [
                    "UNAVAILABLE",
                    "UNKNOWN"
                ]
            },
            "timeout": "5s"
        }
      ]
    }""")

    opt_string = f"retry-config={service_config_fpath}"
    opts = options.Options.build(opt_string)

    # Verify the config was read in correctly.
    expected_cfg = {
        "methodConfig": [
            {
                "name": [
                    {
                        "service": "animalia.mollusca.v1beta1.Cephalopod",
                        "method": "IdentifySquid",
                    }
                ],
                "retryPolicy": {
                    "maxAttempts": 5,
                    "maxBackoff": "3s",
                    "initialBackoff": "0.2s",
                    "backoffMultiplier": 2,
                    "retryableStatusCodes":
                    [
                        "UNAVAILABLE",
                        "UNKNOWN"
                    ]
                },
                "timeout":"5s"
            }
        ]
    }
    assert opts.retry == expected_cfg


def test_options_lazy_import():
    opts = options.Options.build('lazy-import')
    assert opts.lazy_import
