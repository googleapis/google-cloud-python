# Copyright 2014 Google LLC
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

import os
import tempfile
import re
import time
import unittest

import requests
import six

from google.cloud import exceptions
from google.cloud import storage
from google.cloud.storage._helpers import _base64_md5hash
from google.cloud.storage.bucket import LifecycleRuleDelete
from google.cloud.storage.bucket import LifecycleRuleSetStorageClass
from google.cloud import kms
import google.oauth2

from test_utils.retry import RetryErrors
from test_utils.system import unique_resource_id


USER_PROJECT = os.environ.get("GOOGLE_CLOUD_TESTS_USER_PROJECT")
RUNNING_IN_VPCSC = os.getenv("GOOGLE_CLOUD_TESTS_IN_VPCSC", "").lower() == "true"


def _bad_copy(bad_request):
    """Predicate: pass only exceptions for a failed copyTo."""
    err_msg = bad_request.message
    return err_msg.startswith("No file found in request. (POST") and "copyTo" in err_msg


retry_429 = RetryErrors(exceptions.TooManyRequests)
retry_429_503 = RetryErrors([exceptions.TooManyRequests, exceptions.ServiceUnavailable])
retry_bad_copy = RetryErrors(exceptions.BadRequest, error_predicate=_bad_copy)


def _empty_bucket(bucket):
    """Empty a bucket of all existing blobs.

    This accounts (partially) for the eventual consistency of the
    list blobs API call.
    """
    for blob in bucket.list_blobs():
        try:
            blob.delete()
        except exceptions.NotFound:  # eventual consistency
            pass


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """

    CLIENT = None
    TEST_BUCKET = None


def setUpModule():
    Config.CLIENT = storage.Client()
    bucket_name = "new" + unique_resource_id()
    # In the **very** rare case the bucket name is reserved, this
    # fails with a ConnectionError.
    Config.TEST_BUCKET = Config.CLIENT.bucket(bucket_name)
    retry_429(Config.TEST_BUCKET.create)()


def tearDownModule():
    errors = (exceptions.Conflict, exceptions.TooManyRequests)
    retry = RetryErrors(errors, max_tries=6)
    retry(Config.TEST_BUCKET.delete)(force=True)


class TestClient(unittest.TestCase):
    def test_get_service_account_email(self):
        domain = "gs-project-accounts.iam.gserviceaccount.com"

        email = Config.CLIENT.get_service_account_email()

        new_style = re.compile(r"service-(?P<projnum>[^@]+)@" + domain)
        old_style = re.compile(r"{}@{}".format(Config.CLIENT.project, domain))
        patterns = [new_style, old_style]
        matches = [pattern.match(email) for pattern in patterns]

        self.assertTrue(any(match for match in matches if match is not None))


class TestStorageBuckets(unittest.TestCase):
    def setUp(self):
        self.case_buckets_to_delete = []

    def tearDown(self):
        for bucket_name in self.case_buckets_to_delete:
            bucket = Config.CLIENT.bucket(bucket_name)
            retry_429(bucket.delete)()

    def test_create_bucket(self):
        new_bucket_name = "a-new-bucket" + unique_resource_id("-")
        self.assertRaises(
            exceptions.NotFound, Config.CLIENT.get_bucket, new_bucket_name
        )
        created = retry_429(Config.CLIENT.create_bucket)(new_bucket_name)
        self.case_buckets_to_delete.append(new_bucket_name)
        self.assertEqual(created.name, new_bucket_name)

    def test_lifecycle_rules(self):
        new_bucket_name = "w-lifcycle-rules" + unique_resource_id("-")
        self.assertRaises(
            exceptions.NotFound, Config.CLIENT.get_bucket, new_bucket_name
        )
        bucket = Config.CLIENT.bucket(new_bucket_name)
        bucket.add_lifecycle_delete_rule(age=42)
        bucket.add_lifecycle_set_storage_class_rule(
            "COLDLINE", is_live=False, matches_storage_class=["NEARLINE"]
        )

        expected_rules = [
            LifecycleRuleDelete(age=42),
            LifecycleRuleSetStorageClass(
                "COLDLINE", is_live=False, matches_storage_class=["NEARLINE"]
            ),
        ]

        retry_429(bucket.create)(location="us")

        self.case_buckets_to_delete.append(new_bucket_name)
        self.assertEqual(bucket.name, new_bucket_name)
        self.assertEqual(list(bucket.lifecycle_rules), expected_rules)

        bucket.clear_lifecyle_rules()
        bucket.patch()

        self.assertEqual(list(bucket.lifecycle_rules), [])

    def test_list_buckets(self):
        buckets_to_create = [
            "new" + unique_resource_id(),
            "newer" + unique_resource_id(),
            "newest" + unique_resource_id(),
        ]
        created_buckets = []
        for bucket_name in buckets_to_create:
            bucket = Config.CLIENT.bucket(bucket_name)
            retry_429(bucket.create)()
            self.case_buckets_to_delete.append(bucket_name)

        # Retrieve the buckets.
        all_buckets = Config.CLIENT.list_buckets()
        created_buckets = [
            bucket for bucket in all_buckets if bucket.name in buckets_to_create
        ]
        self.assertEqual(len(created_buckets), len(buckets_to_create))

    def test_bucket_update_labels(self):
        bucket_name = "update-labels" + unique_resource_id("-")
        bucket = retry_429(Config.CLIENT.create_bucket)(bucket_name)
        self.case_buckets_to_delete.append(bucket_name)
        self.assertTrue(bucket.exists())

        updated_labels = {"test-label": "label-value"}
        bucket.labels = updated_labels
        bucket.update()
        self.assertEqual(bucket.labels, updated_labels)

        new_labels = {"another-label": "another-value"}
        bucket.labels = new_labels
        bucket.patch()
        self.assertEqual(bucket.labels, new_labels)

        bucket.labels = {}
        bucket.update()
        self.assertEqual(bucket.labels, {})

    @unittest.skipUnless(USER_PROJECT, "USER_PROJECT not set in environment.")
    def test_crud_bucket_with_requester_pays(self):
        new_bucket_name = "w-requester-pays" + unique_resource_id("-")
        created = retry_429(Config.CLIENT.create_bucket)(
            new_bucket_name, requester_pays=True
        )
        self.case_buckets_to_delete.append(new_bucket_name)
        self.assertEqual(created.name, new_bucket_name)
        self.assertTrue(created.requester_pays)

        with_user_project = Config.CLIENT.bucket(
            new_bucket_name, user_project=USER_PROJECT
        )

        # Bucket will be deleted in-line below.
        self.case_buckets_to_delete.remove(new_bucket_name)

        try:
            # Exercise 'buckets.get' w/ userProject.
            self.assertTrue(with_user_project.exists())
            with_user_project.reload()
            self.assertTrue(with_user_project.requester_pays)

            # Exercise 'buckets.patch' w/ userProject.
            with_user_project.configure_website(
                main_page_suffix="index.html", not_found_page="404.html"
            )
            with_user_project.patch()
            self.assertEqual(
                with_user_project._properties["website"],
                {"mainPageSuffix": "index.html", "notFoundPage": "404.html"},
            )

            # Exercise 'buckets.update' w/ userProject.
            new_labels = {"another-label": "another-value"}
            with_user_project.labels = new_labels
            with_user_project.update()
            self.assertEqual(with_user_project.labels, new_labels)

        finally:
            # Exercise 'buckets.delete' w/ userProject.
            with_user_project.delete()

    @unittest.skipUnless(USER_PROJECT, "USER_PROJECT not set in environment.")
    def test_bucket_acls_iam_with_user_project(self):
        new_bucket_name = "acl-w-user-project" + unique_resource_id("-")
        retry_429(Config.CLIENT.create_bucket)(new_bucket_name, requester_pays=True)
        self.case_buckets_to_delete.append(new_bucket_name)

        with_user_project = Config.CLIENT.bucket(
            new_bucket_name, user_project=USER_PROJECT
        )

        # Exercise bucket ACL w/ userProject
        acl = with_user_project.acl
        acl.reload()
        acl.all().grant_read()
        acl.save()
        self.assertIn("READER", acl.all().get_roles())
        del acl.entities["allUsers"]
        acl.save()
        self.assertFalse(acl.has_entity("allUsers"))

        # Exercise default object ACL w/ userProject
        doa = with_user_project.default_object_acl
        doa.reload()
        doa.all().grant_read()
        doa.save()
        self.assertIn("READER", doa.all().get_roles())

        # Exercise IAM w/ userProject
        test_permissions = ["storage.buckets.get"]
        self.assertEqual(
            with_user_project.test_iam_permissions(test_permissions), test_permissions
        )

        policy = with_user_project.get_iam_policy()
        viewers = policy.setdefault("roles/storage.objectViewer", set())
        viewers.add(policy.all_users())
        with_user_project.set_iam_policy(policy)

    @unittest.skipUnless(USER_PROJECT, "USER_PROJECT not set in environment.")
    def test_copy_existing_file_with_user_project(self):
        new_bucket_name = "copy-w-requester-pays" + unique_resource_id("-")
        created = retry_429(Config.CLIENT.create_bucket)(
            new_bucket_name, requester_pays=True
        )
        self.case_buckets_to_delete.append(new_bucket_name)
        self.assertEqual(created.name, new_bucket_name)
        self.assertTrue(created.requester_pays)

        to_delete = []
        blob = storage.Blob("simple", bucket=created)
        blob.upload_from_string(b"DEADBEEF")
        to_delete.append(blob)
        try:
            with_user_project = Config.CLIENT.bucket(
                new_bucket_name, user_project=USER_PROJECT
            )

            new_blob = retry_bad_copy(with_user_project.copy_blob)(
                blob, with_user_project, "simple-copy"
            )
            to_delete.append(new_blob)

            base_contents = blob.download_as_string()
            copied_contents = new_blob.download_as_string()
            self.assertEqual(base_contents, copied_contents)
        finally:
            for blob in to_delete:
                retry_429(blob.delete)()

    @unittest.skipUnless(USER_PROJECT, "USER_PROJECT not set in environment.")
    def test_bucket_get_blob_with_user_project(self):
        new_bucket_name = "w-requester-pays" + unique_resource_id("-")
        data = b"DEADBEEF"
        created = retry_429(Config.CLIENT.create_bucket)(
            new_bucket_name, requester_pays=True
        )
        self.case_buckets_to_delete.append(new_bucket_name)
        self.assertEqual(created.name, new_bucket_name)
        self.assertTrue(created.requester_pays)

        with_user_project = Config.CLIENT.bucket(
            new_bucket_name, user_project=USER_PROJECT
        )

        self.assertIsNone(with_user_project.get_blob("nonesuch"))
        to_add = created.blob("blob-name")
        to_add.upload_from_string(data)
        try:
            found = with_user_project.get_blob("blob-name")
            self.assertEqual(found.download_as_string(), data)
        finally:
            to_add.delete()


class TestStorageFiles(unittest.TestCase):

    DIRNAME = os.path.realpath(os.path.dirname(__file__))
    FILES = {
        "logo": {"path": DIRNAME + "/data/CloudPlatform_128px_Retina.png"},
        "big": {"path": DIRNAME + "/data/five-point-one-mb-file.zip"},
        "simple": {"path": DIRNAME + "/data/simple.txt"},
    }

    @classmethod
    def setUpClass(cls):
        super(TestStorageFiles, cls).setUpClass()
        for file_data in cls.FILES.values():
            with open(file_data["path"], "rb") as file_obj:
                file_data["hash"] = _base64_md5hash(file_obj)
        cls.bucket = Config.TEST_BUCKET

    def setUp(self):
        self.case_blobs_to_delete = []

    def tearDown(self):
        errors = (exceptions.TooManyRequests, exceptions.ServiceUnavailable)
        retry = RetryErrors(errors, max_tries=6)
        for blob in self.case_blobs_to_delete:
            retry(blob.delete)()


class TestStorageWriteFiles(TestStorageFiles):
    ENCRYPTION_KEY = "b23ff11bba187db8c37077e6af3b25b8"

    def test_large_file_write_from_stream(self):
        blob = self.bucket.blob("LargeFile")

        file_data = self.FILES["big"]
        with open(file_data["path"], "rb") as file_obj:
            blob.upload_from_file(file_obj)
            self.case_blobs_to_delete.append(blob)

        md5_hash = blob.md5_hash
        if not isinstance(md5_hash, six.binary_type):
            md5_hash = md5_hash.encode("utf-8")
        self.assertEqual(md5_hash, file_data["hash"])

    def test_large_encrypted_file_write_from_stream(self):
        blob = self.bucket.blob("LargeFile", encryption_key=self.ENCRYPTION_KEY)

        file_data = self.FILES["big"]
        with open(file_data["path"], "rb") as file_obj:
            blob.upload_from_file(file_obj)
            self.case_blobs_to_delete.append(blob)

        md5_hash = blob.md5_hash
        if not isinstance(md5_hash, six.binary_type):
            md5_hash = md5_hash.encode("utf-8")
        self.assertEqual(md5_hash, file_data["hash"])

        temp_filename = tempfile.mktemp()
        with open(temp_filename, "wb") as file_obj:
            blob.download_to_file(file_obj)

        with open(temp_filename, "rb") as file_obj:
            md5_temp_hash = _base64_md5hash(file_obj)

        self.assertEqual(md5_temp_hash, file_data["hash"])

    def test_small_file_write_from_filename(self):
        blob = self.bucket.blob("SmallFile")

        file_data = self.FILES["simple"]
        blob.upload_from_filename(file_data["path"])
        self.case_blobs_to_delete.append(blob)

        md5_hash = blob.md5_hash
        if not isinstance(md5_hash, six.binary_type):
            md5_hash = md5_hash.encode("utf-8")
        self.assertEqual(md5_hash, file_data["hash"])

    @unittest.skipUnless(USER_PROJECT, "USER_PROJECT not set in environment.")
    def test_crud_blob_w_user_project(self):
        with_user_project = Config.CLIENT.bucket(
            self.bucket.name, user_project=USER_PROJECT
        )
        blob = with_user_project.blob("SmallFile")

        file_data = self.FILES["simple"]
        with open(file_data["path"], mode="rb") as to_read:
            file_contents = to_read.read()

        # Exercise 'objects.insert' w/ userProject.
        blob.upload_from_filename(file_data["path"])

        try:
            # Exercise 'objects.get' (metadata) w/ userProject.
            self.assertTrue(blob.exists())
            blob.reload()

            # Exercise 'objects.get' (media) w/ userProject.
            downloaded = blob.download_as_string()
            self.assertEqual(downloaded, file_contents)

            # Exercise 'objects.patch' w/ userProject.
            blob.content_language = "en"
            blob.patch()
            self.assertEqual(blob.content_language, "en")

            # Exercise 'objects.update' w/ userProject.
            metadata = {"foo": "Foo", "bar": "Bar"}
            blob.metadata = metadata
            blob.update()
            self.assertEqual(blob.metadata, metadata)
        finally:
            # Exercise 'objects.delete' (metadata) w/ userProject.
            blob.delete()

    @unittest.skipUnless(USER_PROJECT, "USER_PROJECT not set in environment.")
    def test_blob_acl_w_user_project(self):
        with_user_project = Config.CLIENT.bucket(
            self.bucket.name, user_project=USER_PROJECT
        )
        blob = with_user_project.blob("SmallFile")

        file_data = self.FILES["simple"]

        blob.upload_from_filename(file_data["path"])
        self.case_blobs_to_delete.append(blob)

        # Exercise bucket ACL w/ userProject
        acl = blob.acl
        acl.reload()
        acl.all().grant_read()
        acl.save()
        self.assertIn("READER", acl.all().get_roles())
        del acl.entities["allUsers"]
        acl.save()
        self.assertFalse(acl.has_entity("allUsers"))

    def test_upload_blob_acl(self):
        control = self.bucket.blob("logo")
        control_data = self.FILES["logo"]

        blob = self.bucket.blob("SmallFile")
        file_data = self.FILES["simple"]

        try:
            control.upload_from_filename(control_data["path"])
            blob.upload_from_filename(file_data["path"], predefined_acl="publicRead")
        finally:
            self.case_blobs_to_delete.append(blob)
            self.case_blobs_to_delete.append(control)

        control_acl = control.acl
        self.assertNotIn("READER", control_acl.all().get_roles())
        acl = blob.acl
        self.assertIn("READER", acl.all().get_roles())
        acl.all().revoke_read()
        self.assertSequenceEqual(acl.all().get_roles(), set([]))
        self.assertEqual(control_acl.all().get_roles(), acl.all().get_roles())

    def test_write_metadata(self):
        filename = self.FILES["logo"]["path"]
        blob_name = os.path.basename(filename)

        blob = storage.Blob(blob_name, bucket=self.bucket)
        blob.upload_from_filename(filename)
        self.case_blobs_to_delete.append(blob)

        # NOTE: This should not be necessary. We should be able to pass
        #       it in to upload_file and also to upload_from_string.
        blob.content_type = "image/png"
        self.assertEqual(blob.content_type, "image/png")

    def test_direct_write_and_read_into_file(self):
        blob = self.bucket.blob("MyBuffer")
        file_contents = b"Hello World"
        blob.upload_from_string(file_contents)
        self.case_blobs_to_delete.append(blob)

        same_blob = self.bucket.blob("MyBuffer")
        same_blob.reload()  # Initialize properties.
        temp_filename = tempfile.mktemp()
        with open(temp_filename, "wb") as file_obj:
            same_blob.download_to_file(file_obj)

        with open(temp_filename, "rb") as file_obj:
            stored_contents = file_obj.read()

        self.assertEqual(file_contents, stored_contents)

    def test_copy_existing_file(self):
        filename = self.FILES["logo"]["path"]
        blob = storage.Blob("CloudLogo", bucket=self.bucket)
        blob.upload_from_filename(filename)
        self.case_blobs_to_delete.append(blob)

        new_blob = retry_bad_copy(self.bucket.copy_blob)(
            blob, self.bucket, "CloudLogoCopy"
        )
        self.case_blobs_to_delete.append(new_blob)

        base_contents = blob.download_as_string()
        copied_contents = new_blob.download_as_string()
        self.assertEqual(base_contents, copied_contents)


class TestUnicode(unittest.TestCase):
    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_fetch_object_and_check_content(self):
        client = storage.Client()
        bucket = client.bucket("storage-library-test-bucket")

        # Note: These files are public.
        # Normalization form C: a single character for e-acute;
        # URL should end with Cafe%CC%81
        # Normalization Form D: an ASCII e followed by U+0301 combining
        # character; URL should end with Caf%C3%A9
        test_data = {
            u"Caf\u00e9": b"Normalization Form C",
            u"Cafe\u0301": b"Normalization Form D",
        }
        for blob_name, file_contents in test_data.items():
            blob = bucket.blob(blob_name)
            self.assertEqual(blob.name, blob_name)
            self.assertEqual(blob.download_as_string(), file_contents)


class TestStorageListFiles(TestStorageFiles):

    FILENAMES = ("CloudLogo1", "CloudLogo2", "CloudLogo3")

    @classmethod
    def setUpClass(cls):
        super(TestStorageListFiles, cls).setUpClass()
        # Make sure bucket empty before beginning.
        _empty_bucket(cls.bucket)

        logo_path = cls.FILES["logo"]["path"]
        blob = storage.Blob(cls.FILENAMES[0], bucket=cls.bucket)
        blob.upload_from_filename(logo_path)
        cls.suite_blobs_to_delete = [blob]

        # Copy main blob onto remaining in FILENAMES.
        for filename in cls.FILENAMES[1:]:
            new_blob = retry_bad_copy(cls.bucket.copy_blob)(blob, cls.bucket, filename)
            cls.suite_blobs_to_delete.append(new_blob)

    @classmethod
    def tearDownClass(cls):
        errors = (exceptions.TooManyRequests, exceptions.ServiceUnavailable)
        retry = RetryErrors(errors, max_tries=6)
        for blob in cls.suite_blobs_to_delete:
            retry(blob.delete)()

    @RetryErrors(unittest.TestCase.failureException)
    def test_list_files(self):
        all_blobs = list(self.bucket.list_blobs())
        self.assertEqual(
            sorted(blob.name for blob in all_blobs), sorted(self.FILENAMES)
        )

    @unittest.skipUnless(USER_PROJECT, "USER_PROJECT not set in environment.")
    @RetryErrors(unittest.TestCase.failureException)
    def test_list_files_with_user_project(self):
        with_user_project = Config.CLIENT.bucket(
            self.bucket.name, user_project=USER_PROJECT
        )
        all_blobs = list(with_user_project.list_blobs())
        self.assertEqual(
            sorted(blob.name for blob in all_blobs), sorted(self.FILENAMES)
        )

    @RetryErrors(unittest.TestCase.failureException)
    def test_paginate_files(self):
        truncation_size = 1
        count = len(self.FILENAMES) - truncation_size
        iterator = self.bucket.list_blobs(max_results=count)
        page_iter = iterator.pages

        page1 = six.next(page_iter)
        blobs = list(page1)
        self.assertEqual(len(blobs), count)
        self.assertIsNotNone(iterator.next_page_token)
        # Technically the iterator is exhausted.
        self.assertEqual(iterator.num_results, iterator.max_results)
        # But we modify the iterator to continue paging after
        # articially stopping after ``count`` items.
        iterator.max_results = None

        page2 = six.next(page_iter)
        last_blobs = list(page2)
        self.assertEqual(len(last_blobs), truncation_size)


class TestStoragePseudoHierarchy(TestStorageFiles):

    FILENAMES = (
        "file01.txt",
        "parent/file11.txt",
        "parent/child/file21.txt",
        "parent/child/file22.txt",
        "parent/child/grand/file31.txt",
        "parent/child/other/file32.txt",
    )

    @classmethod
    def setUpClass(cls):
        super(TestStoragePseudoHierarchy, cls).setUpClass()
        # Make sure bucket empty before beginning.
        _empty_bucket(cls.bucket)

        cls.suite_blobs_to_delete = []
        simple_path = cls.FILES["simple"]["path"]
        for filename in cls.FILENAMES:
            blob = storage.Blob(filename, bucket=cls.bucket)
            blob.upload_from_filename(simple_path)
            cls.suite_blobs_to_delete.append(blob)

    @classmethod
    def tearDownClass(cls):
        errors = (exceptions.TooManyRequests, exceptions.ServiceUnavailable)
        retry = RetryErrors(errors, max_tries=6)
        for blob in cls.suite_blobs_to_delete:
            retry(blob.delete)()

    @RetryErrors(unittest.TestCase.failureException)
    def test_blob_get_w_delimiter(self):
        for filename in self.FILENAMES:
            blob = self.bucket.blob(filename)
            self.assertTrue(blob.exists(), filename)

    @RetryErrors(unittest.TestCase.failureException)
    def test_root_level_w_delimiter(self):
        iterator = self.bucket.list_blobs(delimiter="/")
        page = six.next(iterator.pages)
        blobs = list(page)
        self.assertEqual([blob.name for blob in blobs], ["file01.txt"])
        self.assertIsNone(iterator.next_page_token)
        self.assertEqual(iterator.prefixes, set(["parent/"]))

    @RetryErrors(unittest.TestCase.failureException)
    def test_first_level(self):
        iterator = self.bucket.list_blobs(delimiter="/", prefix="parent/")
        page = six.next(iterator.pages)
        blobs = list(page)
        self.assertEqual([blob.name for blob in blobs], ["parent/file11.txt"])
        self.assertIsNone(iterator.next_page_token)
        self.assertEqual(iterator.prefixes, set(["parent/child/"]))

    @RetryErrors(unittest.TestCase.failureException)
    def test_second_level(self):
        expected_names = ["parent/child/file21.txt", "parent/child/file22.txt"]

        iterator = self.bucket.list_blobs(delimiter="/", prefix="parent/child/")
        page = six.next(iterator.pages)
        blobs = list(page)
        self.assertEqual([blob.name for blob in blobs], expected_names)
        self.assertIsNone(iterator.next_page_token)
        self.assertEqual(
            iterator.prefixes, set(["parent/child/grand/", "parent/child/other/"])
        )

    @RetryErrors(unittest.TestCase.failureException)
    def test_third_level(self):
        # Pseudo-hierarchy can be arbitrarily deep, subject to the limit
        # of 1024 characters in the UTF-8 encoded name:
        # https://cloud.google.com/storage/docs/bucketnaming#objectnames
        # Exercise a layer deeper to illustrate this.
        iterator = self.bucket.list_blobs(delimiter="/", prefix="parent/child/grand/")
        page = six.next(iterator.pages)
        blobs = list(page)
        self.assertEqual(
            [blob.name for blob in blobs], ["parent/child/grand/file31.txt"]
        )
        self.assertIsNone(iterator.next_page_token)
        self.assertEqual(iterator.prefixes, set())


class TestStorageSignURLs(TestStorageFiles):
    def setUp(self):
        super(TestStorageSignURLs, self).setUp()

        if (
            type(Config.CLIENT._credentials)
            is not google.oauth2.service_account.credentials
        ):
            self.skipTest("Signing tests requires a service account credential")

        logo_path = self.FILES["logo"]["path"]
        with open(logo_path, "rb") as file_obj:
            self.LOCAL_FILE = file_obj.read()

        blob = self.bucket.blob("LogoToSign.jpg")
        blob.upload_from_string(self.LOCAL_FILE)
        self.case_blobs_to_delete.append(blob)

    def tearDown(self):
        errors = (exceptions.TooManyRequests, exceptions.ServiceUnavailable)
        retry = RetryErrors(errors, max_tries=6)
        for blob in self.case_blobs_to_delete:
            if blob.exists():
                retry(blob.delete)()

    def test_create_signed_read_url(self):
        blob = self.bucket.blob("LogoToSign.jpg")
        expiration = int(time.time() + 10)
        signed_url = blob.generate_signed_url(
            expiration, method="GET", client=Config.CLIENT
        )

        response = requests.get(signed_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.LOCAL_FILE)

    def test_create_signed_read_url_lowercase_method(self):
        blob = self.bucket.blob("LogoToSign.jpg")
        expiration = int(time.time() + 10)
        signed_url = blob.generate_signed_url(
            expiration, method="get", client=Config.CLIENT
        )

        response = requests.get(signed_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.LOCAL_FILE)

    def test_create_signed_read_url_w_non_ascii_name(self):
        blob = self.bucket.blob(u"Caf\xe9.txt")
        payload = b"Test signed URL for blob w/ non-ASCII name"
        blob.upload_from_string(payload)
        self.case_blobs_to_delete.append(blob)

        expiration = int(time.time() + 10)
        signed_url = blob.generate_signed_url(
            expiration, method="GET", client=Config.CLIENT
        )

        response = requests.get(signed_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, payload)

    def test_create_signed_delete_url(self):
        blob = self.bucket.blob("LogoToSign.jpg")
        expiration = int(time.time() + 283473274)
        signed_delete_url = blob.generate_signed_url(
            expiration, method="DELETE", client=Config.CLIENT
        )

        response = requests.request("DELETE", signed_delete_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")

        # Check that the blob has actually been deleted.
        self.assertFalse(blob.exists())


class TestStorageCompose(TestStorageFiles):

    FILES = {}

    def test_compose_create_new_blob(self):
        SOURCE_1 = b"AAA\n"
        source_1 = self.bucket.blob("source-1")
        source_1.upload_from_string(SOURCE_1)
        self.case_blobs_to_delete.append(source_1)

        SOURCE_2 = b"BBB\n"
        source_2 = self.bucket.blob("source-2")
        source_2.upload_from_string(SOURCE_2)
        self.case_blobs_to_delete.append(source_2)

        destination = self.bucket.blob("destination")
        destination.content_type = "text/plain"
        destination.compose([source_1, source_2])
        self.case_blobs_to_delete.append(destination)

        composed = destination.download_as_string()
        self.assertEqual(composed, SOURCE_1 + SOURCE_2)

    def test_compose_create_new_blob_wo_content_type(self):
        SOURCE_1 = b"AAA\n"
        source_1 = self.bucket.blob("source-1")
        source_1.upload_from_string(SOURCE_1)
        self.case_blobs_to_delete.append(source_1)

        SOURCE_2 = b"BBB\n"
        source_2 = self.bucket.blob("source-2")
        source_2.upload_from_string(SOURCE_2)
        self.case_blobs_to_delete.append(source_2)

        destination = self.bucket.blob("destination")

        destination.compose([source_1, source_2])
        self.case_blobs_to_delete.append(destination)

        self.assertIsNone(destination.content_type)
        composed = destination.download_as_string()
        self.assertEqual(composed, SOURCE_1 + SOURCE_2)

    def test_compose_replace_existing_blob(self):
        BEFORE = b"AAA\n"
        original = self.bucket.blob("original")
        original.content_type = "text/plain"
        original.upload_from_string(BEFORE)
        self.case_blobs_to_delete.append(original)

        TO_APPEND = b"BBB\n"
        to_append = self.bucket.blob("to_append")
        to_append.upload_from_string(TO_APPEND)
        self.case_blobs_to_delete.append(to_append)

        original.compose([original, to_append])

        composed = original.download_as_string()
        self.assertEqual(composed, BEFORE + TO_APPEND)

    @unittest.skipUnless(USER_PROJECT, "USER_PROJECT not set in environment.")
    def test_compose_with_user_project(self):
        new_bucket_name = "compose-user-project" + unique_resource_id("-")
        created = retry_429(Config.CLIENT.create_bucket)(
            new_bucket_name, requester_pays=True
        )
        try:
            SOURCE_1 = b"AAA\n"
            source_1 = created.blob("source-1")
            source_1.upload_from_string(SOURCE_1)

            SOURCE_2 = b"BBB\n"
            source_2 = created.blob("source-2")
            source_2.upload_from_string(SOURCE_2)

            with_user_project = Config.CLIENT.bucket(
                new_bucket_name, user_project=USER_PROJECT
            )

            destination = with_user_project.blob("destination")
            destination.content_type = "text/plain"
            destination.compose([source_1, source_2])

            composed = destination.download_as_string()
            self.assertEqual(composed, SOURCE_1 + SOURCE_2)
        finally:
            retry_429(created.delete)(force=True)


class TestStorageRewrite(TestStorageFiles):

    FILENAMES = ("file01.txt",)

    def test_rewrite_create_new_blob_add_encryption_key(self):
        file_data = self.FILES["simple"]

        source = self.bucket.blob("source")
        source.upload_from_filename(file_data["path"])
        self.case_blobs_to_delete.append(source)
        source_data = source.download_as_string()

        KEY = os.urandom(32)
        dest = self.bucket.blob("dest", encryption_key=KEY)
        token, rewritten, total = dest.rewrite(source)
        self.case_blobs_to_delete.append(dest)

        self.assertEqual(token, None)
        self.assertEqual(rewritten, len(source_data))
        self.assertEqual(total, len(source_data))

        self.assertEqual(source.download_as_string(), dest.download_as_string())

    def test_rewrite_rotate_encryption_key(self):
        BLOB_NAME = "rotating-keys"
        file_data = self.FILES["simple"]

        SOURCE_KEY = os.urandom(32)
        source = self.bucket.blob(BLOB_NAME, encryption_key=SOURCE_KEY)
        source.upload_from_filename(file_data["path"])
        self.case_blobs_to_delete.append(source)
        source_data = source.download_as_string()

        DEST_KEY = os.urandom(32)
        dest = self.bucket.blob(BLOB_NAME, encryption_key=DEST_KEY)
        token, rewritten, total = dest.rewrite(source)
        # Not adding 'dest' to 'self.case_blobs_to_delete':  it is the
        # same object as 'source'.

        self.assertIsNone(token)
        self.assertEqual(rewritten, len(source_data))
        self.assertEqual(total, len(source_data))

        self.assertEqual(dest.download_as_string(), source_data)

    @unittest.skipUnless(USER_PROJECT, "USER_PROJECT not set in environment.")
    def test_rewrite_add_key_with_user_project(self):
        file_data = self.FILES["simple"]
        new_bucket_name = "rewrite-key-up" + unique_resource_id("-")
        created = retry_429(Config.CLIENT.create_bucket)(
            new_bucket_name, requester_pays=True
        )
        try:
            with_user_project = Config.CLIENT.bucket(
                new_bucket_name, user_project=USER_PROJECT
            )

            source = with_user_project.blob("source")
            source.upload_from_filename(file_data["path"])
            source_data = source.download_as_string()

            KEY = os.urandom(32)
            dest = with_user_project.blob("dest", encryption_key=KEY)
            token, rewritten, total = dest.rewrite(source)

            self.assertEqual(token, None)
            self.assertEqual(rewritten, len(source_data))
            self.assertEqual(total, len(source_data))

            self.assertEqual(source.download_as_string(), dest.download_as_string())
        finally:
            retry_429(created.delete)(force=True)

    @unittest.skipUnless(USER_PROJECT, "USER_PROJECT not set in environment.")
    def test_rewrite_rotate_with_user_project(self):
        BLOB_NAME = "rotating-keys"
        file_data = self.FILES["simple"]
        new_bucket_name = "rewrite-rotate-up" + unique_resource_id("-")
        created = retry_429(Config.CLIENT.create_bucket)(
            new_bucket_name, requester_pays=True
        )
        try:
            with_user_project = Config.CLIENT.bucket(
                new_bucket_name, user_project=USER_PROJECT
            )

            SOURCE_KEY = os.urandom(32)
            source = with_user_project.blob(BLOB_NAME, encryption_key=SOURCE_KEY)
            source.upload_from_filename(file_data["path"])
            source_data = source.download_as_string()

            DEST_KEY = os.urandom(32)
            dest = with_user_project.blob(BLOB_NAME, encryption_key=DEST_KEY)
            token, rewritten, total = dest.rewrite(source)

            self.assertEqual(token, None)
            self.assertEqual(rewritten, len(source_data))
            self.assertEqual(total, len(source_data))

            self.assertEqual(dest.download_as_string(), source_data)
        finally:
            retry_429(created.delete)(force=True)


class TestStorageUpdateStorageClass(TestStorageFiles):
    def test_update_storage_class_small_file(self):
        blob = self.bucket.blob("SmallFile")

        file_data = self.FILES["simple"]
        blob.upload_from_filename(file_data["path"])
        self.case_blobs_to_delete.append(blob)

        blob.update_storage_class("NEARLINE")
        blob.reload()
        self.assertEqual(blob.storage_class, "NEARLINE")

        blob.update_storage_class("COLDLINE")
        blob.reload()
        self.assertEqual(blob.storage_class, "COLDLINE")

    def test_update_storage_class_large_file(self):
        blob = self.bucket.blob("BigFile")

        file_data = self.FILES["big"]
        blob.upload_from_filename(file_data["path"])
        self.case_blobs_to_delete.append(blob)

        blob.update_storage_class("NEARLINE")
        blob.reload()
        self.assertEqual(blob.storage_class, "NEARLINE")

        blob.update_storage_class("COLDLINE")
        blob.reload()
        self.assertEqual(blob.storage_class, "COLDLINE")


class TestStorageNotificationCRUD(unittest.TestCase):

    topic = None
    TOPIC_NAME = "notification" + unique_resource_id("-")
    CUSTOM_ATTRIBUTES = {"attr1": "value1", "attr2": "value2"}
    BLOB_NAME_PREFIX = "blob-name-prefix/"

    @property
    def topic_path(self):
        return "projects/{}/topics/{}".format(Config.CLIENT.project, self.TOPIC_NAME)

    def _initialize_topic(self):
        try:
            from google.cloud.pubsub_v1 import PublisherClient
        except ImportError:
            raise unittest.SkipTest("Cannot import pubsub")
        self.publisher_client = PublisherClient()
        retry_429(self.publisher_client.create_topic)(self.topic_path)
        policy = self.publisher_client.get_iam_policy(self.topic_path)
        binding = policy.bindings.add()
        binding.role = "roles/pubsub.publisher"
        binding.members.append(
            "serviceAccount:{}".format(Config.CLIENT.get_service_account_email())
        )
        self.publisher_client.set_iam_policy(self.topic_path, policy)

    def setUp(self):
        self.case_buckets_to_delete = []
        self._initialize_topic()

    def tearDown(self):
        retry_429(self.publisher_client.delete_topic)(self.topic_path)
        with Config.CLIENT.batch():
            for bucket_name in self.case_buckets_to_delete:
                bucket = Config.CLIENT.bucket(bucket_name)
                retry_429(bucket.delete)()

    @staticmethod
    def event_types():
        from google.cloud.storage.notification import (
            OBJECT_FINALIZE_EVENT_TYPE,
            OBJECT_DELETE_EVENT_TYPE,
        )

        return [OBJECT_FINALIZE_EVENT_TYPE, OBJECT_DELETE_EVENT_TYPE]

    @staticmethod
    def payload_format():
        from google.cloud.storage.notification import JSON_API_V1_PAYLOAD_FORMAT

        return JSON_API_V1_PAYLOAD_FORMAT

    def test_notification_minimal(self):
        new_bucket_name = "notification-minimal" + unique_resource_id("-")
        bucket = retry_429(Config.CLIENT.create_bucket)(new_bucket_name)
        self.case_buckets_to_delete.append(new_bucket_name)
        self.assertEqual(list(bucket.list_notifications()), [])
        notification = bucket.notification(self.TOPIC_NAME)
        retry_429_503(notification.create)()
        try:
            self.assertTrue(notification.exists())
            self.assertIsNotNone(notification.notification_id)
            notifications = list(bucket.list_notifications())
            self.assertEqual(len(notifications), 1)
            self.assertEqual(notifications[0].topic_name, self.TOPIC_NAME)
        finally:
            notification.delete()

    def test_notification_explicit(self):
        new_bucket_name = "notification-explicit" + unique_resource_id("-")
        bucket = retry_429(Config.CLIENT.create_bucket)(new_bucket_name)
        self.case_buckets_to_delete.append(new_bucket_name)
        notification = bucket.notification(
            self.TOPIC_NAME,
            custom_attributes=self.CUSTOM_ATTRIBUTES,
            event_types=self.event_types(),
            blob_name_prefix=self.BLOB_NAME_PREFIX,
            payload_format=self.payload_format(),
        )
        retry_429_503(notification.create)()
        try:
            self.assertTrue(notification.exists())
            self.assertIsNotNone(notification.notification_id)
            self.assertEqual(notification.custom_attributes, self.CUSTOM_ATTRIBUTES)
            self.assertEqual(notification.event_types, self.event_types())
            self.assertEqual(notification.blob_name_prefix, self.BLOB_NAME_PREFIX)
            self.assertEqual(notification.payload_format, self.payload_format())
        finally:
            notification.delete()

    @unittest.skipUnless(USER_PROJECT, "USER_PROJECT not set in environment.")
    def test_notification_w_user_project(self):
        new_bucket_name = "notification-minimal" + unique_resource_id("-")
        retry_429(Config.CLIENT.create_bucket)(new_bucket_name, requester_pays=True)
        self.case_buckets_to_delete.append(new_bucket_name)
        with_user_project = Config.CLIENT.bucket(
            new_bucket_name, user_project=USER_PROJECT
        )
        self.assertEqual(list(with_user_project.list_notifications()), [])
        notification = with_user_project.notification(self.TOPIC_NAME)
        retry_429(notification.create)()
        try:
            self.assertTrue(notification.exists())
            self.assertIsNotNone(notification.notification_id)
            notifications = list(with_user_project.list_notifications())
            self.assertEqual(len(notifications), 1)
            self.assertEqual(notifications[0].topic_name, self.TOPIC_NAME)
        finally:
            notification.delete()


class TestAnonymousClient(unittest.TestCase):

    PUBLIC_BUCKET = "gcp-public-data-landsat"

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_access_to_public_bucket(self):
        anonymous = storage.Client.create_anonymous_client()
        bucket = anonymous.bucket(self.PUBLIC_BUCKET)
        blob, = bucket.list_blobs(max_results=1)
        with tempfile.TemporaryFile() as stream:
            blob.download_to_file(stream)


class TestKMSIntegration(TestStorageFiles):

    FILENAMES = ("file01.txt",)

    KEYRING_NAME = "gcs-test"
    KEY_NAME = "gcs-test"
    ALT_KEY_NAME = "gcs-test-alternate"

    def _kms_key_name(self, key_name=None):
        if key_name is None:
            key_name = self.KEY_NAME

        return ("projects/{}/" "locations/{}/" "keyRings/{}/" "cryptoKeys/{}").format(
            Config.CLIENT.project,
            self.bucket.location.lower(),
            self.KEYRING_NAME,
            key_name,
        )

    @classmethod
    def setUpClass(cls):
        super(TestKMSIntegration, cls).setUpClass()

    def setUp(self):
        super(TestKMSIntegration, self).setUp()
        client = kms.KeyManagementServiceClient()
        project = Config.CLIENT.project
        location = self.bucket.location.lower()
        keyring_name = self.KEYRING_NAME
        purpose = kms.enums.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT

        # If the keyring doesn't exist create it.
        keyring_path = client.key_ring_path(project, location, keyring_name)

        try:
            client.get_key_ring(keyring_path)
        except exceptions.NotFound:
            parent = client.location_path(project, location)
            client.create_key_ring(parent, keyring_name, {})

            # Mark this service account as an owner of the new keyring
            service_account = Config.CLIENT.get_service_account_email()
            policy = {
                "bindings": [
                    {
                        "role": "roles/cloudkms.cryptoKeyEncrypterDecrypter",
                        "members": ["serviceAccount:" + service_account],
                    }
                ]
            }
            client.set_iam_policy(keyring_path, policy)

        # Populate the keyring with the keys we use in the tests
        key_names = [
            "gcs-test",
            "gcs-test-alternate",
            "explicit-kms-key-name",
            "default-kms-key-name",
            "override-default-kms-key-name",
            "alt-default-kms-key-name",
        ]
        for key_name in key_names:
            key_path = client.crypto_key_path(project, location, keyring_name, key_name)
            try:
                client.get_crypto_key(key_path)
            except exceptions.NotFound:
                key = {"purpose": purpose}
                client.create_crypto_key(keyring_path, key_name, key)

    def test_blob_w_explicit_kms_key_name(self):
        BLOB_NAME = "explicit-kms-key-name"
        file_data = self.FILES["simple"]
        kms_key_name = self._kms_key_name()
        blob = self.bucket.blob(BLOB_NAME, kms_key_name=kms_key_name)
        blob.upload_from_filename(file_data["path"])
        self.case_blobs_to_delete.append(blob)
        with open(file_data["path"], "rb") as _file_data:
            self.assertEqual(blob.download_as_string(), _file_data.read())
        # We don't know the current version of the key.
        self.assertTrue(blob.kms_key_name.startswith(kms_key_name))

        listed, = list(self.bucket.list_blobs())
        self.assertTrue(listed.kms_key_name.startswith(kms_key_name))

    def test_bucket_w_default_kms_key_name(self):
        BLOB_NAME = "default-kms-key-name"
        OVERRIDE_BLOB_NAME = "override-default-kms-key-name"
        ALT_BLOB_NAME = "alt-default-kms-key-name"
        CLEARTEXT_BLOB_NAME = "cleartext"

        file_data = self.FILES["simple"]

        with open(file_data["path"], "rb") as _file_data:
            contents = _file_data.read()

        kms_key_name = self._kms_key_name()
        self.bucket.default_kms_key_name = kms_key_name
        self.bucket.patch()
        self.assertEqual(self.bucket.default_kms_key_name, kms_key_name)

        defaulted_blob = self.bucket.blob(BLOB_NAME)
        defaulted_blob.upload_from_filename(file_data["path"])
        self.case_blobs_to_delete.append(defaulted_blob)

        self.assertEqual(defaulted_blob.download_as_string(), contents)
        # We don't know the current version of the key.
        self.assertTrue(defaulted_blob.kms_key_name.startswith(kms_key_name))

        alt_kms_key_name = self._kms_key_name(self.ALT_KEY_NAME)

        override_blob = self.bucket.blob(
            OVERRIDE_BLOB_NAME, kms_key_name=alt_kms_key_name
        )
        override_blob.upload_from_filename(file_data["path"])
        self.case_blobs_to_delete.append(override_blob)

        self.assertEqual(override_blob.download_as_string(), contents)
        # We don't know the current version of the key.
        self.assertTrue(override_blob.kms_key_name.startswith(alt_kms_key_name))

        self.bucket.default_kms_key_name = alt_kms_key_name
        self.bucket.patch()

        alt_blob = self.bucket.blob(ALT_BLOB_NAME)
        alt_blob.upload_from_filename(file_data["path"])
        self.case_blobs_to_delete.append(alt_blob)

        self.assertEqual(alt_blob.download_as_string(), contents)
        # We don't know the current version of the key.
        self.assertTrue(alt_blob.kms_key_name.startswith(alt_kms_key_name))

        self.bucket.default_kms_key_name = None
        self.bucket.patch()

        cleartext_blob = self.bucket.blob(CLEARTEXT_BLOB_NAME)
        cleartext_blob.upload_from_filename(file_data["path"])
        self.case_blobs_to_delete.append(cleartext_blob)

        self.assertEqual(cleartext_blob.download_as_string(), contents)
        self.assertIsNone(cleartext_blob.kms_key_name)

    def test_rewrite_rotate_csek_to_cmek(self):
        BLOB_NAME = "rotating-keys"
        file_data = self.FILES["simple"]

        SOURCE_KEY = os.urandom(32)
        source = self.bucket.blob(BLOB_NAME, encryption_key=SOURCE_KEY)
        source.upload_from_filename(file_data["path"])
        self.case_blobs_to_delete.append(source)
        source_data = source.download_as_string()

        kms_key_name = self._kms_key_name()

        # We can't verify it, but ideally we would check that the following
        # URL was resolvable with our credentials
        # KEY_URL = 'https://cloudkms.googleapis.com/v1/{}'.format(
        #     kms_key_name)

        dest = self.bucket.blob(BLOB_NAME, kms_key_name=kms_key_name)
        token, rewritten, total = dest.rewrite(source)

        while token is not None:
            token, rewritten, total = dest.rewrite(source, token=token)

        # Not adding 'dest' to 'self.case_blobs_to_delete':  it is the
        # same object as 'source'.

        self.assertIsNone(token)
        self.assertEqual(rewritten, len(source_data))
        self.assertEqual(total, len(source_data))

        self.assertEqual(dest.download_as_string(), source_data)


class TestRetentionPolicy(unittest.TestCase):
    def setUp(self):
        self.case_buckets_to_delete = []

    def tearDown(self):
        for bucket_name in self.case_buckets_to_delete:
            bucket = Config.CLIENT.bucket(bucket_name)
            retry_429(bucket.delete)()

    def test_bucket_w_retention_period(self):
        import datetime
        from google.api_core import exceptions

        period_secs = 10

        new_bucket_name = "w-retention-period" + unique_resource_id("-")
        bucket = retry_429(Config.CLIENT.create_bucket)(new_bucket_name)
        self.case_buckets_to_delete.append(new_bucket_name)

        bucket.retention_period = period_secs
        bucket.default_event_based_hold = False
        bucket.patch()

        self.assertEqual(bucket.retention_period, period_secs)
        self.assertIsInstance(bucket.retention_policy_effective_time, datetime.datetime)
        self.assertFalse(bucket.default_event_based_hold)
        self.assertFalse(bucket.retention_policy_locked)

        blob_name = "test-blob"
        payload = b"DEADBEEF"
        blob = bucket.blob(blob_name)
        blob.upload_from_string(payload)

        other = bucket.get_blob(blob_name)

        self.assertFalse(other.event_based_hold)
        self.assertFalse(other.temporary_hold)
        self.assertIsInstance(other.retention_expiration_time, datetime.datetime)

        with self.assertRaises(exceptions.Forbidden):
            other.delete()

        bucket.retention_period = None
        bucket.patch()

        self.assertIsNone(bucket.retention_period)
        self.assertIsNone(bucket.retention_policy_effective_time)
        self.assertFalse(bucket.default_event_based_hold)
        self.assertFalse(bucket.retention_policy_locked)

        other.reload()

        self.assertFalse(other.event_based_hold)
        self.assertFalse(other.temporary_hold)
        self.assertIsNone(other.retention_expiration_time)

        other.delete()

    def test_bucket_w_default_event_based_hold(self):
        from google.api_core import exceptions

        new_bucket_name = "w-def-ebh" + unique_resource_id("-")
        self.assertRaises(
            exceptions.NotFound, Config.CLIENT.get_bucket, new_bucket_name
        )
        bucket = retry_429(Config.CLIENT.create_bucket)(new_bucket_name)
        self.case_buckets_to_delete.append(new_bucket_name)

        bucket.default_event_based_hold = True
        bucket.patch()

        self.assertTrue(bucket.default_event_based_hold)
        self.assertIsNone(bucket.retention_period)
        self.assertIsNone(bucket.retention_policy_effective_time)
        self.assertFalse(bucket.retention_policy_locked)

        blob_name = "test-blob"
        payload = b"DEADBEEF"
        blob = bucket.blob(blob_name)
        blob.upload_from_string(payload)

        other = bucket.get_blob(blob_name)

        self.assertTrue(other.event_based_hold)
        self.assertFalse(other.temporary_hold)
        self.assertIsNone(other.retention_expiration_time)

        with self.assertRaises(exceptions.Forbidden):
            other.delete()

        other.event_based_hold = False
        other.patch()

        other.delete()

        bucket.default_event_based_hold = False
        bucket.patch()

        self.assertFalse(bucket.default_event_based_hold)
        self.assertIsNone(bucket.retention_period)
        self.assertIsNone(bucket.retention_policy_effective_time)
        self.assertFalse(bucket.retention_policy_locked)

        blob.upload_from_string(payload)
        self.assertFalse(other.event_based_hold)
        self.assertFalse(other.temporary_hold)
        self.assertIsNone(other.retention_expiration_time)

        blob.delete()

    def test_blob_w_temporary_hold(self):
        from google.api_core import exceptions

        new_bucket_name = "w-tmp-hold" + unique_resource_id("-")
        self.assertRaises(
            exceptions.NotFound, Config.CLIENT.get_bucket, new_bucket_name
        )
        bucket = retry_429(Config.CLIENT.create_bucket)(new_bucket_name)
        self.case_buckets_to_delete.append(new_bucket_name)

        blob_name = "test-blob"
        payload = b"DEADBEEF"
        blob = bucket.blob(blob_name)
        blob.upload_from_string(payload)

        other = bucket.get_blob(blob_name)
        other.temporary_hold = True
        other.patch()

        self.assertTrue(other.temporary_hold)
        self.assertFalse(other.event_based_hold)
        self.assertIsNone(other.retention_expiration_time)

        with self.assertRaises(exceptions.Forbidden):
            other.delete()

        other.temporary_hold = False
        other.patch()

        other.delete()

    def test_bucket_lock_retention_policy(self):
        import datetime
        from google.api_core import exceptions

        period_secs = 10

        new_bucket_name = "loc-ret-policy" + unique_resource_id("-")
        self.assertRaises(
            exceptions.NotFound, Config.CLIENT.get_bucket, new_bucket_name
        )
        bucket = retry_429(Config.CLIENT.create_bucket)(new_bucket_name)
        self.case_buckets_to_delete.append(new_bucket_name)

        bucket.retention_period = period_secs
        bucket.patch()

        self.assertEqual(bucket.retention_period, period_secs)
        self.assertIsInstance(bucket.retention_policy_effective_time, datetime.datetime)
        self.assertFalse(bucket.default_event_based_hold)
        self.assertFalse(bucket.retention_policy_locked)

        bucket.lock_retention_policy()

        bucket.reload()
        self.assertTrue(bucket.retention_policy_locked)

        bucket.retention_period = None
        with self.assertRaises(exceptions.Forbidden):
            bucket.patch()
