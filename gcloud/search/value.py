# Copyright 2015 Google Inc. All rights reserved.
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

"""Define Cloud Search Values."""


class Value(object):
    """Value objects hold search values and tokenization parameters.

    See:
    https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions

    :type value: string
    :param value: the string value

    :type tokenization: string
    :param tokenization: the tokenization format for string values.
    """
    def __init__(self, value, tokenization=None):
        self.value = value
        self.tokenization = tokenization

    @classmethod
    def from_api_repr(cls, resource):
        """Factory:  construct a topic given its API representation

        :type resource: dict
        :param resource: topic resource representation returned from the API

        :rtype: :class:`gcloud.search.value.Value`
        :returns: Value parsed from ``resource``.
        """
        return cls(value=resource['value'])
