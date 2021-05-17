# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

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

DATABASES = {
    "default": {
        "ENGINE": "django_spanner",
        "PROJECT": "emulator-local",
        "INSTANCE": "django-test-instance",
        "NAME": "django-test-db",
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
