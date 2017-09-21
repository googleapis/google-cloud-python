# Copyright 2017 Google Inc.
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

from google.api.core import exceptions
from google.api.core.gapic_v1 import config


INTERFACE_CONFIG = {
    'retry_codes': {
        'idempotent': ['DEADLINE_EXCEEDED', 'UNAVAILABLE'],
        'other': ['FAILED_PRECONDITION'],
        'non_idempotent': []
    },
    'retry_params': {
        'default': {
            'initial_retry_delay_millis': 1000,
            'retry_delay_multiplier': 2.5,
            'max_retry_delay_millis': 120000,
            'initial_rpc_timeout_millis': 120000,
            'rpc_timeout_multiplier': 1.0,
            'max_rpc_timeout_millis': 120000,
            'total_timeout_millis': 600000
        },
        'other': {
            'initial_retry_delay_millis': 1000,
            'retry_delay_multiplier': 1,
            'max_retry_delay_millis': 1000,
            'initial_rpc_timeout_millis': 1000,
            'rpc_timeout_multiplier': 1,
            'max_rpc_timeout_millis': 1000,
            'total_timeout_millis': 1000
        },
    },
    'methods': {
        'AnnotateVideo': {
            'timeout_millis': 60000,
            'retry_codes_name': 'idempotent',
            'retry_params_name': 'default'
        },
        'Other': {
            'timeout_millis': 60000,
            'retry_codes_name': 'other',
            'retry_params_name': 'other'
        },
        'Plain': {
            'timeout_millis': 30000
        }
    }
}


def test_create_method_configs():
    method_configs = config.create_method_configs(INTERFACE_CONFIG)

    annotate_video_config = method_configs['AnnotateVideo']
    assert isinstance(annotate_video_config, config.RetryableMethodConfig)
    assert annotate_video_config.retry_exceptions == [
        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable]
    assert annotate_video_config.initial_delay == 1.0
    assert annotate_video_config.delay_multiplier == 2.5
    assert annotate_video_config.max_delay == 120.0
    assert annotate_video_config.deadline == 600.0
    assert annotate_video_config.initial_timeout == 120.0
    assert annotate_video_config.timeout_multiplier == 1.0
    assert annotate_video_config.max_timeout == 120.0

    other_config = method_configs['Other']
    assert isinstance(annotate_video_config, config.RetryableMethodConfig)
    assert other_config.retry_exceptions == [
        exceptions.FailedPrecondition]
    assert other_config.initial_delay == 1.0
    assert other_config.delay_multiplier == 1.0
    assert other_config.max_delay == 1.0
    assert other_config.deadline == 1.0
    assert other_config.initial_timeout == 1.0
    assert other_config.timeout_multiplier == 1.0
    assert other_config.max_timeout == 1.0

    plain_config = method_configs['Plain']
    assert isinstance(plain_config, config.MethodConfig)
    assert plain_config.timeout == 30.0
