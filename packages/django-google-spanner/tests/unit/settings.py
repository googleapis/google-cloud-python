# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import time
import os

DEBUG = True
USE_TZ = True

INSTALLED_APPS = [
    "django_spanner",  # Must be the first entry
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tests",
]

TIME_ZONE = "UTC"

ENGINE = "django_spanner"
PROJECT = os.getenv(
    "GOOGLE_CLOUD_PROJECT", os.getenv("PROJECT_ID", "emulator-test-project"),
)

INSTANCE = "django-test-instance"
NAME = "spanner-django-test-{}".format(str(int(time.time())))

DATABASES = {
    "default": {
        "ENGINE": ENGINE,
        "PROJECT": PROJECT,
        "INSTANCE": INSTANCE,
        "NAME": NAME,
    }
}
SECRET_KEY = "spanner emulator secret key"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

SITE_ID = 1

CONN_MAX_AGE = 60

ENGINE = "django_spanner"
PROJECT = "emulator-local"
INSTANCE = "django-test-instance"
NAME = "django-test-db"
OPTIONS = {}
AUTOCOMMIT = True
