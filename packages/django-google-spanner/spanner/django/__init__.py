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

# The first step is to monkey-patch AutoField that
# contains a primary_key=True set and insert in a UUID.

from django.db.models.fields import AutoField
from spanner.dbapi import gen_rand_int64


def with_rand_int64_pre_save(self, model_instance, add):
    if add:
        return gen_rand_int64()
    else:
        return getattr(model_instance, 'id', None)


# Overwrite any pre_save value.
AutoField.pre_save = with_rand_int64_pre_save
