#!/bin/sh

# Copyright (c) 2020 Google LLC. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# exit when any command fails
set -e

# If no SPANNER_TEST_DB is set, generate a unique one
# so that we can have multiple tests running without
# conflicting which changes and constraints. We'll always
# cleanup the created database.
TEST_DBNAME=${SPANNER_TEST_DB:-$(python3 -c 'import os, time; print(chr(ord("a") + time.time_ns() % 26)+os.urandom(10).hex())')}
TEST_DBNAME_OTHER="$TEST_DBNAME-ot"
TEST_APPS=${DJANGO_TEST_APPS:-basic}
INSTANCE=${SPANNER_TEST_INSTANCE:-django-tests}
PROJECT=${PROJECT_ID:-appdev-soda-spanner-staging}
SETTINGS_FILE="$TEST_DBNAME-settings"

checkout_django() {
    mkdir -p django_tests && cd django_tests
    git clone --depth 1 --single-branch --branch spanner-2.2.x https://github.com/timgraham/django.git
    cd django && pip3 install -e .
    # pip3 install -r tests/requirements/py3.txt
}

create_settings() {
    cat << ! > "$SETTINGS_FILE.py"
DATABASES = {
   'default': {
       'ENGINE': 'django_spanner',
       'PROJECT': "$PROJECT",
       'INSTANCE': "$INSTANCE",
       'NAME': "$TEST_DBNAME",
   },
   'other': {
       'ENGINE': 'django_spanner',
       'PROJECT': "$PROJECT",
       'INSTANCE': "$INSTANCE",
       'NAME': "$TEST_DBNAME_OTHER",
   },
}
SECRET_KEY = 'spanner_tests_secret_key'
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
!
}

run_django_tests() {
    cd tests
    create_settings
    echo -e "\033[32mRunning Django tests $TEST_APPS\033[00m"
    python3 runtests.py $TEST_APPS --verbosity=2 --noinput --settings $SETTINGS_FILE
}

install_django_spanner() {
    pip3 install .
}

install_django_spanner
checkout_django
run_django_tests
