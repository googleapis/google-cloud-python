import os
import re

from test_utils.system import EmulatorCreds, unique_resource_id

from google.cloud.firestore_v1.base_client import _FIRESTORE_EMULATOR_HOST

FIRESTORE_CREDS = os.environ.get("FIRESTORE_APPLICATION_CREDENTIALS")
FIRESTORE_PROJECT = os.environ.get("GCLOUD_PROJECT")
RANDOM_ID_REGEX = re.compile("^[a-zA-Z0-9]{20}$")
MISSING_DOCUMENT = "No document to update: "
DOCUMENT_EXISTS = "Document already exists: "
UNIQUE_RESOURCE_ID = unique_resource_id("-")
EMULATOR_CREDS = EmulatorCreds()
FIRESTORE_EMULATOR = os.environ.get(_FIRESTORE_EMULATOR_HOST) is not None
FIRESTORE_OTHER_DB = os.environ.get("SYSTEM_TESTS_DATABASE", "system-tests-named-db")
