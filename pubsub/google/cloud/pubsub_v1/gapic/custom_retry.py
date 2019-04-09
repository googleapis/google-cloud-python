# -*- coding: utf-8 -*-
#
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

from google.api_core import exceptions as core_exceptions


def patch_retry_predicate(method_config):
    """Patch method config to *not* retry on service accout missing errors.

    If Retry is None in the config, the config is returned unmodified.

    Args:
        method_config (:class:`google.api_core.gapic_v1.config.MethodConfig`):
            The method config to patch.

    Returns:
        :class:`google.api_core.gapic_v1.config.MethodConfig`: The modified config.
    """
    if method_config.retry is None:
        return method_config  # there's nothing to patch

    orig_predicate = method_config.retry._predicate

    def should_retry(exc):
        if isinstance(exc, core_exceptions.ServiceUnavailable):
            return "invalid_grant" not in exc.message
        return orig_predicate(exc)

    new_retry = method_config.retry.with_predicate(should_retry)
    return method_config._replace(retry=new_retry)
