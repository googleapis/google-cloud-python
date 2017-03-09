# Copyright 2014 Google Inc.
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
import time
import unittest

import httplib2
import six

from google.cloud import exceptions
from google.cloud import storage
from google.cloud.storage._helpers import _base64_md5hash

from test_utils.retry import RetryErrors
from test_utils.system import unique_resource_id


HTTP = httplib2.Http()


def _bad_copy(bad_request):
    """Predicate: pass only exceptions for a failed copyTo."""
    err_msg = bad_request.message
    return (err_msg.startswith('No file found in request. (POST') and
            'copyTo' in err_msg)


retry_429 = RetryErrors(exceptions.TooManyRequests)
retry_bad_copy = RetryErrors(exceptions.BadRequest,
                             error_predicate=_bad_copy)


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
    bucket_name = 'new' + unique_resource_id()
    # In the **very** rare case the bucket name is reserved, this
    # fails with a ConnectionError.
    Config.TEST_BUCKET = Config.CLIENT.bucket(bucket_name)
    retry_429(Config.TEST_BUCKET.create)()


def tearDownModule():
    retry = RetryErrors(exceptions.Conflict)
    retry(Config.TEST_BUCKET.delete)(force=True)


class TestStorageBuckets(unittest.TestCase):

    def setUp(self):
        self.case_buckets_to_delete = []

    def tearDown(self):
        with Config.CLIENT.batch():
            for bucket_name in self.case_buckets_to_delete:
                bucket = Config.CLIENT.bucket(bucket_name)
                retry_429(bucket.delete)()

    def test_create_bucket(self):
        new_bucket_name = 'a-new-bucket' + unique_resource_id('-')
        self.assertRaises(exceptions.NotFound,
                          Config.CLIENT.get_bucket, new_bucket_name)
        created = Config.CLIENT.create_bucket(new_bucket_name)
        self.case_buckets_to_delete.append(new_bucket_name)
        self.assertEqual(created.name, new_bucket_name)

    def test_list_buckets(self):
        buckets_to_create = [
            'new' + unique_resource_id(),
            'newer' + unique_resource_id(),
            'newest' + unique_resource_id(),
        ]
        created_buckets = []
        for bucket_name in buckets_to_create:
            bucket = Config.CLIENT.bucket(bucket_name)
            retry_429(bucket.create)()
            self.case_buckets_to_delete.append(bucket_name)

        # Retrieve the buckets.
        all_buckets = Config.CLIENT.list_buckets()
        created_buckets = [bucket for bucket in all_buckets
                           if bucket.name in buckets_to_create]
        self.assertEqual(len(created_buckets), len(buckets_to_create))


class TestStorageFiles(unittest.TestCase):

    DIRNAME = os.path.realpath(os.path.dirname(__file__))
    FILES = {
        'logo': {
            'path': DIRNAME + '/data/CloudPlatform_128px_Retina.png',
        },
        'big': {
            'path': DIRNAME + '/data/five-point-one-mb-file.zip',
        },
        'simple': {
            'path': DIRNAME + '/data/simple.txt',
        }
    }

    @classmethod
    def setUpClass(cls):
        super(TestStorageFiles, cls).setUpClass()
        for file_data in cls.FILES.values():
            with open(file_data['path'], 'rb') as file_obj:
                file_data['hash'] = _base64_md5hash(file_obj)
        cls.bucket = Config.TEST_BUCKET

    def setUp(self):
        self.case_blobs_to_delete = []

    def tearDown(self):
        for blob in self.case_blobs_to_delete:
            blob.delete()


class TestStorageWriteFiles(TestStorageFiles):
    ENCRYPTION_KEY = 'b23ff11bba187db8c37077e6af3b25b8'

    def test_large_file_write_from_stream(self):
        blob = self.bucket.blob('LargeFile')

        file_data = self.FILES['big']
        with open(file_data['path'], 'rb') as file_obj:
            blob.upload_from_file(file_obj)
            self.case_blobs_to_delete.append(blob)

        md5_hash = blob.md5_hash
        if not isinstance(md5_hash, six.binary_type):
            md5_hash = md5_hash.encode('utf-8')
        self.assertEqual(md5_hash, file_data['hash'])

    def test_large_encrypted_file_write_from_stream(self):
        blob = self.bucket.blob('LargeFile',
                                encryption_key=self.ENCRYPTION_KEY)

        file_data = self.FILES['big']
        with open(file_data['path'], 'rb') as file_obj:
            blob.upload_from_file(file_obj)
            self.case_blobs_to_delete.append(blob)

        md5_hash = blob.md5_hash
        if not isinstance(md5_hash, six.binary_type):
            md5_hash = md5_hash.encode('utf-8')
        self.assertEqual(md5_hash, file_data['hash'])

        temp_filename = tempfile.mktemp()
        with open(temp_filename, 'wb') as file_obj:
            blob.download_to_file(file_obj)

        with open(temp_filename, 'rb') as file_obj:
            md5_temp_hash = _base64_md5hash(file_obj)

        self.assertEqual(md5_temp_hash, file_data['hash'])

    def test_small_file_write_from_filename(self):
        blob = self.bucket.blob('SmallFile')

        file_data = self.FILES['simple']
        blob.upload_from_filename(file_data['path'])
        self.case_blobs_to_delete.append(blob)

        md5_hash = blob.md5_hash
        if not isinstance(md5_hash, six.binary_type):
            md5_hash = md5_hash.encode('utf-8')
        self.assertEqual(md5_hash, file_data['hash'])

    def test_write_metadata(self):
        filename = self.FILES['logo']['path']
        blob_name = os.path.basename(filename)

        blob = storage.Blob(blob_name, bucket=self.bucket)
        blob.upload_from_filename(filename)
        self.case_blobs_to_delete.append(blob)

        # NOTE: This should not be necessary. We should be able to pass
        #       it in to upload_file and also to upload_from_string.
        blob.content_type = 'image/png'
        self.assertEqual(blob.content_type, 'image/png')

    def test_direct_write_and_read_into_file(self):
        blob = self.bucket.blob('MyBuffer')
        file_contents = b'Hello World'
        blob.upload_from_string(file_contents)
        self.case_blobs_to_delete.append(blob)

        same_blob = self.bucket.blob('MyBuffer')
        same_blob.reload()  # Initialize properties.
        temp_filename = tempfile.mktemp()
        with open(temp_filename, 'wb') as file_obj:
            same_blob.download_to_file(file_obj)

        with open(temp_filename, 'rb') as file_obj:
            stored_contents = file_obj.read()

        self.assertEqual(file_contents, stored_contents)

    def test_copy_existing_file(self):
        filename = self.FILES['logo']['path']
        blob = storage.Blob('CloudLogo', bucket=self.bucket)
        blob.upload_from_filename(filename)
        self.case_blobs_to_delete.append(blob)

        new_blob = retry_bad_copy(self.bucket.copy_blob)(
            blob, self.bucket, 'CloudLogoCopy')
        self.case_blobs_to_delete.append(new_blob)

        base_contents = blob.download_as_string()
        copied_contents = new_blob.download_as_string()
        self.assertEqual(base_contents, copied_contents)


class TestStorageListFiles(TestStorageFiles):

    FILENAMES = ('CloudLogo1', 'CloudLogo2', 'CloudLogo3')

    @classmethod
    def setUpClass(cls):
        super(TestStorageListFiles, cls).setUpClass()
        # Make sure bucket empty before beginning.
        _empty_bucket(cls.bucket)

        logo_path = cls.FILES['logo']['path']
        blob = storage.Blob(cls.FILENAMES[0], bucket=cls.bucket)
        blob.upload_from_filename(logo_path)
        cls.suite_blobs_to_delete = [blob]

        # Copy main blob onto remaining in FILENAMES.
        for filename in cls.FILENAMES[1:]:
            new_blob = retry_bad_copy(cls.bucket.copy_blob)(
                blob, cls.bucket, filename)
            cls.suite_blobs_to_delete.append(new_blob)

    @classmethod
    def tearDownClass(cls):
        for blob in cls.suite_blobs_to_delete:
            blob.delete()

    @RetryErrors(unittest.TestCase.failureException)
    def test_list_files(self):
        all_blobs = list(self.bucket.list_blobs())
        self.assertEqual(sorted(blob.name for blob in all_blobs),
                         sorted(self.FILENAMES))

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
        'file01.txt',
        'parent/file11.txt',
        'parent/child/file21.txt',
        'parent/child/file22.txt',
        'parent/child/grand/file31.txt',
        'parent/child/other/file32.txt',
    )

    @classmethod
    def setUpClass(cls):
        super(TestStoragePseudoHierarchy, cls).setUpClass()
        # Make sure bucket empty before beginning.
        _empty_bucket(cls.bucket)

        simple_path = cls.FILES['simple']['path']
        blob = storage.Blob(cls.FILENAMES[0], bucket=cls.bucket)
        blob.upload_from_filename(simple_path)
        cls.suite_blobs_to_delete = [blob]
        for filename in cls.FILENAMES[1:]:
            new_blob = retry_bad_copy(cls.bucket.copy_blob)(
                blob, cls.bucket, filename)
            cls.suite_blobs_to_delete.append(new_blob)

    @classmethod
    def tearDownClass(cls):
        for blob in cls.suite_blobs_to_delete:
            blob.delete()

    @RetryErrors(unittest.TestCase.failureException)
    def test_root_level_w_delimiter(self):
        iterator = self.bucket.list_blobs(delimiter='/')
        page = six.next(iterator.pages)
        blobs = list(page)
        self.assertEqual([blob.name for blob in blobs], ['file01.txt'])
        self.assertIsNone(iterator.next_page_token)
        self.assertEqual(iterator.prefixes, set(['parent/']))

    @RetryErrors(unittest.TestCase.failureException)
    def test_first_level(self):
        iterator = self.bucket.list_blobs(delimiter='/', prefix='parent/')
        page = six.next(iterator.pages)
        blobs = list(page)
        self.assertEqual([blob.name for blob in blobs], ['parent/file11.txt'])
        self.assertIsNone(iterator.next_page_token)
        self.assertEqual(iterator.prefixes, set(['parent/child/']))

    @RetryErrors(unittest.TestCase.failureException)
    def test_second_level(self):
        expected_names = [
            'parent/child/file21.txt',
            'parent/child/file22.txt',
        ]

        iterator = self.bucket.list_blobs(delimiter='/',
                                          prefix='parent/child/')
        page = six.next(iterator.pages)
        blobs = list(page)
        self.assertEqual([blob.name for blob in blobs],
                         expected_names)
        self.assertIsNone(iterator.next_page_token)
        self.assertEqual(iterator.prefixes,
                         set(['parent/child/grand/', 'parent/child/other/']))

    @RetryErrors(unittest.TestCase.failureException)
    def test_third_level(self):
        # Pseudo-hierarchy can be arbitrarily deep, subject to the limit
        # of 1024 characters in the UTF-8 encoded name:
        # https://cloud.google.com/storage/docs/bucketnaming#objectnames
        # Exercise a layer deeper to illustrate this.
        iterator = self.bucket.list_blobs(delimiter='/',
                                          prefix='parent/child/grand/')
        page = six.next(iterator.pages)
        blobs = list(page)
        self.assertEqual([blob.name for blob in blobs],
                         ['parent/child/grand/file31.txt'])
        self.assertIsNone(iterator.next_page_token)
        self.assertEqual(iterator.prefixes, set())


class TestStorageSignURLs(TestStorageFiles):

    def setUp(self):
        super(TestStorageSignURLs, self).setUp()

        logo_path = self.FILES['logo']['path']
        with open(logo_path, 'rb') as file_obj:
            self.LOCAL_FILE = file_obj.read()

        blob = self.bucket.blob('LogoToSign.jpg')
        blob.upload_from_string(self.LOCAL_FILE)
        self.case_blobs_to_delete.append(blob)

    def tearDown(self):
        for blob in self.case_blobs_to_delete:
            if blob.exists():
                blob.delete()

    def test_create_signed_read_url(self):
        blob = self.bucket.blob('LogoToSign.jpg')
        expiration = int(time.time() + 5)
        signed_url = blob.generate_signed_url(expiration, method='GET',
                                              client=Config.CLIENT)

        response, content = HTTP.request(signed_url, method='GET')
        self.assertEqual(response.status, 200)
        self.assertEqual(content, self.LOCAL_FILE)

    def test_create_signed_delete_url(self):
        blob = self.bucket.blob('LogoToSign.jpg')
        expiration = int(time.time() + 283473274)
        signed_delete_url = blob.generate_signed_url(expiration,
                                                     method='DELETE',
                                                     client=Config.CLIENT)

        response, content = HTTP.request(signed_delete_url, method='DELETE')
        self.assertEqual(response.status, 204)
        self.assertEqual(content, b'')

        # Check that the blob has actually been deleted.
        self.assertFalse(blob.exists())


class TestStorageCompose(TestStorageFiles):

    FILES = {}

    def test_compose_create_new_blob(self):
        SOURCE_1 = b'AAA\n'
        source_1 = self.bucket.blob('source-1')
        source_1.upload_from_string(SOURCE_1)
        self.case_blobs_to_delete.append(source_1)

        SOURCE_2 = b'BBB\n'
        source_2 = self.bucket.blob('source-2')
        source_2.upload_from_string(SOURCE_2)
        self.case_blobs_to_delete.append(source_2)

        destination = self.bucket.blob('destination')
        destination.content_type = 'text/plain'
        destination.compose([source_1, source_2])
        self.case_blobs_to_delete.append(destination)

        composed = destination.download_as_string()
        self.assertEqual(composed, SOURCE_1 + SOURCE_2)

    def test_compose_replace_existing_blob(self):
        BEFORE = b'AAA\n'
        original = self.bucket.blob('original')
        original.content_type = 'text/plain'
        original.upload_from_string(BEFORE)
        self.case_blobs_to_delete.append(original)

        TO_APPEND = b'BBB\n'
        to_append = self.bucket.blob('to_append')
        to_append.upload_from_string(TO_APPEND)
        self.case_blobs_to_delete.append(to_append)

        original.compose([original, to_append])

        composed = original.download_as_string()
        self.assertEqual(composed, BEFORE + TO_APPEND)


class TestStorageRewrite(TestStorageFiles):

    FILENAMES = (
        'file01.txt',
    )

    def test_rewrite_create_new_blob_add_encryption_key(self):
        file_data = self.FILES['simple']

        source = self.bucket.blob('source')
        source.upload_from_filename(file_data['path'])
        self.case_blobs_to_delete.append(source)
        source_data = source.download_as_string()

        KEY = os.urandom(32)
        dest = self.bucket.blob('dest', encryption_key=KEY)
        token, rewritten, total = dest.rewrite(source)
        self.case_blobs_to_delete.append(dest)

        self.assertEqual(token, None)
        self.assertEqual(rewritten, len(source_data))
        self.assertEqual(total, len(source_data))

        self.assertEqual(source.download_as_string(),
                         dest.download_as_string())

    def test_rewrite_rotate_encryption_key(self):
        BLOB_NAME = 'rotating-keys'
        file_data = self.FILES['simple']

        SOURCE_KEY = os.urandom(32)
        source = self.bucket.blob(BLOB_NAME, encryption_key=SOURCE_KEY)
        source.upload_from_filename(file_data['path'])
        self.case_blobs_to_delete.append(source)
        source_data = source.download_as_string()

        DEST_KEY = os.urandom(32)
        dest = self.bucket.blob(BLOB_NAME, encryption_key=DEST_KEY)
        token, rewritten, total = dest.rewrite(source)
        # Not adding 'dest' to 'self.case_blobs_to_delete':  it is the
        # same object as 'source'.

        self.assertEqual(token, None)
        self.assertEqual(rewritten, len(source_data))
        self.assertEqual(total, len(source_data))

        self.assertEqual(dest.download_as_string(), source_data)
