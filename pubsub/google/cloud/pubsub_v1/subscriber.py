# Copyright 2017, Google Inc. All rights reserved.
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

from __future__ import absolute_import

import functools
import pkg_resources

from google.cloud.gapic.pubsub.v1 import subscriber_client


__VERSION__ = pkg_resources.get_distribution('google-cloud-pubsub').version


class SubscriberClient(subscriber_client.SubscriberClient):
    @functools.wraps(subscriber_client.SubscriberClient.__init__)
    def __init__(self, *args, **kwargs):
        kwargs['lib_name'] = 'gccl'
        kwargs['lib_version'] = __VERSION__
        super(SubscriberClient, self).__init__(*args, **kwargs)

    def get_subscription(self, subscription, options=None):
        """Return the """
