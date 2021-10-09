# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import datetime
import os
import django

# Monkey-patch AutoField to generate a random value since Cloud Spanner can't
# do that.
from uuid import uuid4

import pkg_resources
from google.cloud.spanner_v1 import JsonObject
from django.db.models.fields import (
    AutoField,
    Field,
)

from .expressions import register_expressions
from .functions import register_functions
from .lookups import register_lookups
from .utils import check_django_compatability

# Monkey-patch google.DatetimeWithNanoseconds's __eq__ compare against
# datetime.datetime.
from google.api_core.datetime_helpers import DatetimeWithNanoseconds


USING_DJANGO_3 = False
if django.VERSION[:2] == (3, 2):
    USING_DJANGO_3 = True

if USING_DJANGO_3:
    from django.db.models.fields import (
        SmallAutoField,
        BigAutoField,
    )
    from django.db.models import JSONField

__version__ = pkg_resources.get_distribution("django-google-spanner").version

USE_EMULATOR = os.getenv("SPANNER_EMULATOR_HOST") is not None

# Only active LTS django versions (2.2.*, 3.2.*) are supported by this library right now.
SUPPORTED_DJANGO_VERSIONS = [(2, 2), (3, 2)]

check_django_compatability(SUPPORTED_DJANGO_VERSIONS)
register_expressions(USING_DJANGO_3)
register_functions()
register_lookups()


def gen_rand_int64():
    # Credit to https://stackoverflow.com/a/3530326.
    return uuid4().int & 0x7FFFFFFFFFFFFFFF


def autofield_init(self, *args, **kwargs):
    kwargs["blank"] = True
    Field.__init__(self, *args, **kwargs)
    self.default = gen_rand_int64


AutoField.__init__ = autofield_init
AutoField.db_returning = False
AutoField.validators = []
if USING_DJANGO_3:
    SmallAutoField.__init__ = autofield_init
    BigAutoField.__init__ = autofield_init
    SmallAutoField.db_returning = False
    BigAutoField.db_returning = False
    SmallAutoField.validators = []
    BigAutoField.validators = []

    def get_prep_value(self, value):
        # Json encoding and decoding for spanner is done in python-spanner.
        if not isinstance(value, JsonObject) and isinstance(value, dict):
            return JsonObject(value)

        return value

    JSONField.get_prep_value = get_prep_value


old_datetimewithnanoseconds_eq = getattr(
    DatetimeWithNanoseconds, "__eq__", None
)


def datetimewithnanoseconds_eq(self, other):
    if old_datetimewithnanoseconds_eq:
        equal = old_datetimewithnanoseconds_eq(self, other)
        if equal:
            return True
        elif type(self) is type(other):
            return False

    # Otherwise try to convert them to an equvialent form.
    # See https://github.com/googleapis/python-spanner-django/issues/272
    if isinstance(other, datetime.datetime):
        return self.ctime() == other.ctime()

    return False


DatetimeWithNanoseconds.__eq__ = datetimewithnanoseconds_eq

# Sanity check here since tests can't easily be run for this file:
if __name__ == "__main__":
    from django.utils import timezone

    UTC = timezone.utc

    dt = datetime.datetime(2020, 1, 10, 2, 44, 57, 999, UTC)
    dtns = DatetimeWithNanoseconds(2020, 1, 10, 2, 44, 57, 999, UTC)
    equal = dtns == dt
    if not equal:
        raise Exception("%s\n!=\n%s" % (dtns, dt))
