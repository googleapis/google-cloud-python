#!/bin/sh

ORIGWD=$(pwd)
# If no SPANNER_TEST_DB is set, generate a unique one
# so that we can have multiple tests running without
# conflicting which changes and constraints. We'll always
# cleanup the created database.
TEST_DBNAME=${SPANNER_TEST_DB:-testdb-$(date +%F%H%M%S)}
TEST_DBNAME_OTHER="$TEST_DBNAME-other"
TEST_APPS=${DJANGO_TEST_APPS:-basic}
INSTANCE_NAME=${SPANNER_TEST_INSTANCE:-django-tests}
PROJECT=${SPANNER_TEST_PROJECT:-appdev-soda-spanner-staging}
SETTINGS_FILE="$TEST_DBNAME-settings"
DROPDB_ON_EXIT=${SPANNER_DROP_DB_ON_EXIT:-true}

# Use "regional-us-east4" to reduce latency to Travis CI, as per:
# https://devops.stackexchange.com/questions/2488/geographically-where-are-the-travis-ci-jobs-run
REGION=${SPANNER_TEST_REGION:-regional-us-east4}
INSTANCE_CONFIG="projects/$PROJECT/instanceConfigs/$REGION"

DBs=($TEST_DBNAME $TEST_DBNAME_OTHER)

function create_db() {
    for DB in ${DBs[*]}
    do
        echo "
from google.cloud import spanner_v1 as sp
ins = sp.Client(project='$PROJECT').instance('$INSTANCE_NAME')
if not ins.exists():
    ins.configuration_name = '$INSTANCE_CONFIG'
    lro = ins.create()
    _ = lro.result()
    print('Created instance: $INSTANCE_NAME at $INSTANCE_CONFIG')

db = ins.database('$DB')
if not db.exists():
    lro = db.create()
    _ = lro.result()
    print('Created database: $DB')
else:
    print('$DB already exists')
" | python3 -
        code=$?
        if [[ $code -ne 0 ]]
        then
            return $code
        fi
    done
}

function checkout_django() {
    mkdir -p django_tests && cd django_tests
    git clone --depth 1 --single-branch --branch spanner-2.2.x https://github.com/timgraham/django.git
    cd django && pip3 install -e .
    pip3 install -r tests/requirements/py3.txt
    return $?
}

function create_settings() {
    cat << ! > "$SETTINGS_FILE.py"
DATABASES = {
   'default': {
       'ENGINE': 'spanner.django',
       'SPANNER_URL': "cloudspanner:/projects/$PROJECT/instances/$INSTANCE_NAME/databases/$TEST_DBNAME?instance_config=$INSTANCE_CONFIG",
        'TEST': {
            'NAME': "$TEST_DBNAME",
        },
   },
   'other': {
       'ENGINE': 'spanner.django',
       'SPANNER_URL': "cloudspanner:/projects/$PROJECT/instances/$INSTANCE_NAME/databases/$TEST_DBNAME_OTHER?instance_config=$INSTANCE_CONFIG",
        'TEST': {
            'NAME': "$TEST_DBNAME_OTHER",
        },
   },
}
SECRET_KEY = 'spanner_tests_secret_key'
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
!
}

function drop_db() {
    echo "
from google.cloud import spanner_v1 as sp
ins = sp.Client(project='$PROJECT').instance('$INSTANCE_NAME')
if not ins.exists():
    print('Instance $INSTANCE_NAME does not exist anyways')
else:
    db = ins.database('$TEST_DBNAME')
    if db.exists():
        db.drop()
        print('Dropped $TEST_DBNAME')
" | python3 -
    return $?
}

function run_django_tests() {
    cd tests
    create_settings
    echo -e "\033[32mRunning Django tests $TEST_APPS\033[00m"
    # Using --keepdb here because Django's test suite tries to invoke `DROP DATABASE`
    # using the Cursor if --keepdb isn't set, yet only the Spanner.Database instance
    # can drop the database, which we do manually in function `drop_db`.
    python3 runtests.py $TEST_APPS --verbosity=2 --keepdb --noinput --settings $SETTINGS_FILE
    return $?
}

function install_spanner_django() {
    pip3 install .
    return $?
}

function cleanup_and_exit() {
    exitCode=$?
    msg=$1
    echo $msg
    if [[ $DROPDB_ON_EXIT = "true" ]]
    then
        drop_db
    fi
    cd $ORIGWD
    exit $exitCode
}

install_spanner_django || cleanup_and_exit
create_db || cleanup_and_exit "INSTANCE: $INSTANCE_NAME DB: $TEST_DBNAME and $TEST_DBNAME_OTHER could not be created"
checkout_django || cleanup_and_exit
run_django_tests || cleanup_and_exit
# Unconditionally clean up before exit.
cleanup_and_exit
