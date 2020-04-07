# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

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
from .utils import check_django_compatability

__version__ = '2.2a0'

check_django_compatability()
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
