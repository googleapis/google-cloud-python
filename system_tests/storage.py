# Copyright 2014 Google Inc. All rights reserved.
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

import httplib2
import os
import six
import tempfile
import time
import unittest2

from gcloud import _helpers
from gcloud.environment_vars import TESTS_PROJECT
from gcloud import exceptions
from gcloud import storage
from gcloud.storage._helpers import _base64_md5hash


HTTP = httplib2.Http()
SHARED_BUCKETS = {}

_helpers.PROJECT = TESTS_PROJECT
CLIENT = storage.Client()


def setUpModule():
    if 'test_bucket' not in SHARED_BUCKETS:
        # %d rounds milliseconds to nearest integer.
        bucket_name = 'new%d' % (1000 * time.time(),)
        # In the **very** rare case the bucket name is reserved, this
        # fails with a ConnectionError.
        SHARED_BUCKETS['test_bucket'] = CLIENT.create_bucket(bucket_name)


def tearDownModule():
    for bucket in SHARED_BUCKETS.values():
        bucket.delete(force=True)


class TestStorageBuckets(unittest2.TestCase):

    def setUp(self):
        self.case_buckets_to_delete = []

    def tearDown(self):
        with CLIENT.batch():
            for bucket_name in self.case_buckets_to_delete:
                CLIENT.bucket(bucket_name).delete()

    def test_create_bucket(self):
        new_bucket_name = 'a-new-bucket'
        self.assertRaises(exceptions.NotFound,
                          CLIENT.get_bucket, new_bucket_name)
        created = CLIENT.create_bucket(new_bucket_name)
        self.case_buckets_to_delete.append(new_bucket_name)
        self.assertEqual(created.name, new_bucket_name)

    def test_list_buckets(self):
        buckets_to_create = [
            'new%d' % (1000 * time.time(),),
            'newer%d' % (1000 * time.time(),),
            'newest%d' % (1000 * time.time(),),
        ]
        created_buckets = []
        for bucket_name in buckets_to_create:
            bucket = CLIENT.create_bucket(bucket_name)
            self.case_buckets_to_delete.append(bucket_name)

        # Retrieve the buckets.
        all_buckets = CLIENT.list_buckets()
        created_buckets = [bucket for bucket in all_buckets
                           if bucket.name in buckets_to_create]
        self.assertEqual(len(created_buckets), len(buckets_to_create))


class TestStorageFiles(unittest2.TestCase):

    FILES = {
        'logo': {
            'path': 'system_tests/data/CloudPlatform_128px_Retina.png',
        },
        'big': {
            'path': 'system_tests/data/five-point-one-mb-file.zip',
        },
        'simple': {
            'path': 'system_tests/data/simple.txt',
        }
    }

    @classmethod
    def setUpClass(cls):
        super(TestStorageFiles, cls).setUpClass()
        for file_data in cls.FILES.values():
            with open(file_data['path'], 'rb') as file_obj:
                file_data['hash'] = _base64_md5hash(file_obj)
        cls.bucket = SHARED_BUCKETS['test_bucket']

    def setUp(self):
        self.case_blobs_to_delete = []

    def tearDown(self):
        for blob in self.case_blobs_to_delete:
            blob.delete()


class TestStorageWriteFiles(TestStorageFiles):

    def test_large_file_write_from_stream(self):
        blob = self.bucket.blob('LargeFile')
        self.assertEqual(blob._properties, {})

        file_data = self.FILES['big']
        with open(file_data['path'], 'rb') as file_obj:
            blob.upload_from_file(file_obj)
            self.case_blobs_to_delete.append(blob)

        md5_hash = blob.md5_hash
        if not isinstance(md5_hash, six.binary_type):
            md5_hash = md5_hash.encode('utf-8')
        self.assertEqual(md5_hash, file_data['hash'])

    def test_small_file_write_from_filename(self):
        blob = self.bucket.blob('SmallFile')
        self.assertEqual(blob._properties, {})

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

        new_blob = self.bucket.copy_blob(blob, self.bucket, 'CloudLogoCopy')
        self.case_blobs_to_delete.append(new_blob)

        base_contents = blob.download_as_string()
        copied_contents = new_blob.download_as_string()
        self.assertEqual(base_contents, copied_contents)


class TestStorageListFiles(TestStorageFiles):

    FILENAMES = ['CloudLogo1', 'CloudLogo2', 'CloudLogo3']

    @classmethod
    def setUpClass(cls):
        super(TestStorageListFiles, cls).setUpClass()
        # Make sure bucket empty before beginning.
        for blob in cls.bucket.list_blobs():
            blob.delete()

        logo_path = cls.FILES['logo']['path']
        blob = storage.Blob(cls.FILENAMES[0], bucket=cls.bucket)
        blob.upload_from_filename(logo_path)
        cls.suite_blobs_to_delete = [blob]

        # Copy main blob onto remaining in FILENAMES.
        for filename in cls.FILENAMES[1:]:
            new_blob = cls.bucket.copy_blob(blob, cls.bucket, filename)
            cls.suite_blobs_to_delete.append(new_blob)

    @classmethod
    def tearDownClass(cls):
        for blob in cls.suite_blobs_to_delete:
            blob.delete()

    def test_list_files(self):
        all_blobs = list(self.bucket.list_blobs())
        self.assertEqual(len(all_blobs), len(self.FILENAMES))

    def test_paginate_files(self):
        truncation_size = 1
        count = len(self.FILENAMES) - truncation_size
        iterator = self.bucket.list_blobs(max_results=count)
        response = iterator.get_next_page_response()
        blobs = list(iterator.get_items_from_response(response))
        self.assertEqual(len(blobs), count)
        self.assertEqual(iterator.page_number, 1)
        self.assertTrue(iterator.next_page_token is not None)

        response = iterator.get_next_page_response()
        last_blobs = list(iterator.get_items_from_response(response))
        self.assertEqual(len(last_blobs), truncation_size)


class TestStoragePseudoHierarchy(TestStorageFiles):

    FILENAMES = [
        'file01.txt',
        'parent/file11.txt',
        'parent/child/file21.txt',
        'parent/child/file22.txt',
        'parent/child/grand/file31.txt',
        'parent/child/other/file32.txt',
        ]

    @classmethod
    def setUpClass(cls):
        super(TestStoragePseudoHierarchy, cls).setUpClass()
        # Make sure bucket empty before beginning.
        for blob in cls.bucket.list_blobs():
            blob.delete()

        simple_path = cls.FILES['simple']['path']
        blob = storage.Blob(cls.FILENAMES[0], bucket=cls.bucket)
        blob.upload_from_filename(simple_path)
        cls.suite_blobs_to_delete = [blob]
        for filename in cls.FILENAMES[1:]:
            new_blob = cls.bucket.copy_blob(blob, cls.bucket, filename)
            cls.suite_blobs_to_delete.append(new_blob)

    @classmethod
    def tearDownClass(cls):
        for blob in cls.suite_blobs_to_delete:
            blob.delete()

    def test_root_level_w_delimiter(self):
        iterator = self.bucket.list_blobs(delimiter='/')
        response = iterator.get_next_page_response()
        blobs = list(iterator.get_items_from_response(response))
        self.assertEqual([blob.name for blob in blobs], ['file01.txt'])
        self.assertEqual(iterator.page_number, 1)
        self.assertTrue(iterator.next_page_token is None)
        self.assertEqual(iterator.prefixes, set(['parent/']))

    def test_first_level(self):
        iterator = self.bucket.list_blobs(delimiter='/', prefix='parent/')
        response = iterator.get_next_page_response()
        blobs = list(iterator.get_items_from_response(response))
        self.assertEqual([blob.name for blob in blobs], ['parent/file11.txt'])
        self.assertEqual(iterator.page_number, 1)
        self.assertTrue(iterator.next_page_token is None)
        self.assertEqual(iterator.prefixes, set(['parent/child/']))

    def test_second_level(self):
        iterator = self.bucket.list_blobs(delimiter='/',
                                          prefix='parent/child/')
        response = iterator.get_next_page_response()
        blobs = list(iterator.get_items_from_response(response))
        self.assertEqual([blob.name for blob in blobs],
                         ['parent/child/file21.txt',
                          'parent/child/file22.txt'])
        self.assertEqual(iterator.page_number, 1)
        self.assertTrue(iterator.next_page_token is None)
        self.assertEqual(iterator.prefixes,
                         set(['parent/child/grand/', 'parent/child/other/']))

    def test_third_level(self):
        # Pseudo-hierarchy can be arbitrarily deep, subject to the limit
        # of 1024 characters in the UTF-8 encoded name:
        # https://cloud.google.com/storage/docs/bucketnaming#objectnames
        # Exercise a layer deeper to illustrate this.
        iterator = self.bucket.list_blobs(delimiter='/',
                                          prefix='parent/child/grand/')
        response = iterator.get_next_page_response()
        blobs = list(iterator.get_items_from_response(response))
        self.assertEqual([blob.name for blob in blobs],
                         ['parent/child/grand/file31.txt'])
        self.assertEqual(iterator.page_number, 1)
        self.assertTrue(iterator.next_page_token is None)
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
                                              client=CLIENT)

        response, content = HTTP.request(signed_url, method='GET')
        self.assertEqual(response.status, 200)
        self.assertEqual(content, self.LOCAL_FILE)

    def test_create_signed_delete_url(self):
        blob = self.bucket.blob('LogoToSign.jpg')
        expiration = int(time.time() + 283473274)
        signed_delete_url = blob.generate_signed_url(expiration,
                                                     method='DELETE',
                                                     client=CLIENT)

        response, content = HTTP.request(signed_delete_url, method='DELETE')
        self.assertEqual(response.status, 204)
        self.assertEqual(content, b'')

        # Check that the blob has actually been deleted.
        self.assertFalse(blob.exists())
