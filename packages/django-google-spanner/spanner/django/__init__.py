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

import datetime
# Monkey-patch AutoField to generate a random value since Cloud Spanner can't
# do that.
from uuid import uuid4

from django.db.models.fields import AutoField, Field
# Monkey-patch google.DatetimeWithNanoseconds's __eq__ compare against datetime.datetime.
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

from .expressions import register_expressions
from .functions import register_functions
from .lookups import register_lookups

register_expressions()
register_functions()
register_lookups()


def gen_rand_int64():
    # Credit to https://stackoverflow.com/a/3530326.
    return uuid4().int & 0x7FFFFFFFFFFFFFFF


def autofield_init(self, *args, **kwargs):
    kwargs['blank'] = True
    Field.__init__(self, *args, **kwargs)
    self.default = gen_rand_int64


AutoField.__init__ = autofield_init

old_datetimewithnanoseconds_eq = getattr(DatetimeWithNanoseconds, '__eq__', None)


def datetimewithnanoseconds_eq(self, other):
    if old_datetimewithnanoseconds_eq:
        equal = old_datetimewithnanoseconds_eq(self, other)
        if equal:
            return True
        elif type(self) is type(other):
            return False

    # Otherwise try to convert them to an equvialent form.
    # See https://github.com/orijtech/spanner-orm/issues/272
    if isinstance(other, datetime.datetime):
        return self.ctime() == other.ctime()

    return False


DatetimeWithNanoseconds.__eq__ = datetimewithnanoseconds_eq

# Sanity check here since tests can't easily be run for this file:
if __name__ == '__main__':
    from django.utils import timezone
    UTC = timezone.utc

    dt = datetime.datetime(2020, 1, 10, 2, 44, 57, 999, UTC)
    dtns = DatetimeWithNanoseconds(2020, 1, 10, 2, 44, 57, 999, UTC)
    equal = dtns == dt
    if not equal:
        raise Exception('%s\n!=\n%s' % (dtns, dt))
