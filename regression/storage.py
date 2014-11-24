from Crypto.Hash import MD5
import base64
import httplib2
import tempfile
import time
import unittest2

from gcloud import storage
# This assumes the command is being run via tox hence the
# repository root is the current directory.
from regression import regression_utils


HTTP = httplib2.Http()
SHARED_BUCKETS = {}


def setUpModule():
    if 'test_bucket' not in SHARED_BUCKETS:
        connection = regression_utils.get_storage_connection()
        # %d rounds milliseconds to nearest integer.
        bucket_name = 'new%d' % (1000 * time.time(),)
        # In the **very** rare case the bucket name is reserved, this
        # fails with a ConnectionError.
        SHARED_BUCKETS['test_bucket'] = connection.create_bucket(bucket_name)


def tearDownModule():
    for bucket in SHARED_BUCKETS.values():
        # Passing force=True also deletes all files.
        bucket.delete(force=True)


class TestStorage(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connection = regression_utils.get_storage_connection()


class TestStorageBuckets(TestStorage):

    def setUp(self):
        self.case_buckets_to_delete = []

    def tearDown(self):
        for bucket in self.case_buckets_to_delete:
            bucket.delete()

    def test_create_bucket(self):
        new_bucket_name = 'a-new-bucket'
        self.assertRaises(storage.exceptions.NotFound,
                          self.connection.get_bucket, new_bucket_name)
        created = self.connection.create_bucket(new_bucket_name)
        self.case_buckets_to_delete.append(created)
        self.assertEqual(created.name, new_bucket_name)

    def test_get_buckets(self):
        buckets_to_create = [
            'new%d' % (1000 * time.time(),),
            'newer%d' % (1000 * time.time(),),
            'newest%d' % (1000 * time.time(),),
        ]
        created_buckets = []
        for bucket_name in buckets_to_create:
            bucket = self.connection.create_bucket(bucket_name)
            self.case_buckets_to_delete.append(bucket)

        # Retrieve the buckets.
        all_buckets = self.connection.get_all_buckets()
        created_buckets = [bucket for bucket in all_buckets
                           if bucket.name in buckets_to_create]
        self.assertEqual(len(created_buckets), len(buckets_to_create))


class TestStorageFiles(TestStorage):

    FILES = {
        'logo': {
            'path': 'regression/data/CloudPlatform_128px_Retina.png',
        },
        'big': {
            'path': 'regression/data/five-mb-file.zip',
        },
        'simple': {
            'path': 'regression/data/simple.txt',
        }
    }

    @staticmethod
    def _get_base64_md5hash(filename):
        with open(filename, 'rb') as file_obj:
            hash = MD5.new(data=file_obj.read())
        digest_bytes = hash.digest()
        return base64.b64encode(digest_bytes)

    @classmethod
    def setUpClass(cls):
        super(TestStorageFiles, cls).setUpClass()
        for file_data in cls.FILES.values():
            file_data['hash'] = cls._get_base64_md5hash(file_data['path'])
        cls.bucket = SHARED_BUCKETS['test_bucket']

    def setUp(self):
        self.case_keys_to_delete = []

    def tearDown(self):
        for key in self.case_keys_to_delete:
            key.delete()


class TestStorageWriteFiles(TestStorageFiles):

    def test_large_file_write_from_stream(self):
        key = self.bucket.new_key('LargeFile')
        self.assertEqual(key._properties, {})

        file_data = self.FILES['big']
        with open(file_data['path'], 'rb') as file_obj:
            self.bucket.upload_file_object(file_obj, key=key)
            self.case_keys_to_delete.append(key)

        key._properties.clear()  # force a reload
        self.assertEqual(key.md5_hash, file_data['hash'])

    def test_write_metadata(self):
        key = self.bucket.upload_file(self.FILES['logo']['path'])
        self.case_keys_to_delete.append(key)

        # NOTE: This should not be necessary. We should be able to pass
        #       it in to upload_file and also to upload_from_string.
        key.content_type = 'image/png'
        key._properties.clear()  # force a reload
        self.assertEqual(key.content_type, 'image/png')

    def test_direct_write_and_read_into_file(self):
        key = self.bucket.new_key('MyBuffer')
        file_contents = 'Hello World'
        key.upload_from_string(file_contents)
        self.case_keys_to_delete.append(key)

        same_key = self.bucket.new_key('MyBuffer')
        temp_filename = tempfile.mktemp()
        with open(temp_filename, 'w') as file_obj:
            same_key.get_contents_to_file(file_obj)

        with open(temp_filename, 'rb') as file_obj:
            stored_contents = file_obj.read()

        self.assertEqual(file_contents, stored_contents)

    def test_copy_existing_file(self):
        key = self.bucket.upload_file(self.FILES['logo']['path'],
                                      key='CloudLogo')
        self.case_keys_to_delete.append(key)

        new_key = self.bucket.copy_key(key, self.bucket, 'CloudLogoCopy')
        self.case_keys_to_delete.append(new_key)

        base_contents = key.get_contents_as_string()
        copied_contents = new_key.get_contents_as_string()
        self.assertEqual(base_contents, copied_contents)


class TestStorageListFiles(TestStorageFiles):

    FILENAMES = ['CloudLogo1', 'CloudLogo2', 'CloudLogo3']

    @classmethod
    def setUpClass(cls):
        super(TestStorageListFiles, cls).setUpClass()
        # Make sure bucket empty before beginning.
        for key in cls.bucket:
            key.delete()

        logo_path = cls.FILES['logo']['path']
        key = cls.bucket.upload_file(logo_path, key=cls.FILENAMES[0])
        cls.suite_keys_to_delete = [key]

        # Copy main key onto remaining in FILENAMES.
        for filename in cls.FILENAMES[1:]:
            new_key = cls.bucket.copy_key(key, cls.bucket, filename)
            cls.suite_keys_to_delete.append(new_key)

    @classmethod
    def tearDownClass(cls):
        for key in cls.suite_keys_to_delete:
            key.delete()

    def test_list_files(self):
        all_keys = self.bucket.get_all_keys()
        self.assertEqual(len(all_keys), len(self.FILENAMES))

    def test_paginate_files(self):
        truncation_size = 1
        count = len(self.FILENAMES) - truncation_size
        iterator = self.bucket.iterator(max_results=count)
        response = iterator.get_next_page_response()
        keys = list(iterator.get_items_from_response(response))
        self.assertEqual(len(keys), count)
        self.assertEqual(iterator.page_number, 1)
        self.assertTrue(iterator.next_page_token is not None)

        response = iterator.get_next_page_response()
        last_keys = list(iterator.get_items_from_response(response))
        self.assertEqual(len(last_keys), truncation_size)


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
        for key in cls.bucket:
            key.delete()

        simple_path = cls.FILES['simple']['path']
        key = cls.bucket.upload_file(simple_path, key=cls.FILENAMES[0])
        cls.suite_keys_to_delete = [key]
        for filename in cls.FILENAMES[1:]:
            new_key = cls.bucket.copy_key(key, cls.bucket, filename)
            cls.suite_keys_to_delete.append(new_key)

    @classmethod
    def tearDownClass(cls):
        for key in cls.suite_keys_to_delete:
            key.delete()

    def test_root_level_w_delimiter(self):
        iterator = self.bucket.iterator(delimiter='/')
        response = iterator.get_next_page_response()
        keys = list(iterator.get_items_from_response(response))
        self.assertEqual([key.name for key in keys], ['file01.txt'])
        self.assertEqual(iterator.page_number, 1)
        self.assertTrue(iterator.next_page_token is None)
        self.assertEqual(iterator.prefixes, ('parent/',))

    def test_first_level(self):
        iterator = self.bucket.iterator(delimiter='/', prefix='parent/')
        response = iterator.get_next_page_response()
        keys = list(iterator.get_items_from_response(response))
        self.assertEqual([key.name for key in keys], ['parent/file11.txt'])
        self.assertEqual(iterator.page_number, 1)
        self.assertTrue(iterator.next_page_token is None)
        self.assertEqual(iterator.prefixes, ('parent/child/',))

    def test_second_level(self):
        iterator = self.bucket.iterator(delimiter='/', prefix='parent/child/')
        response = iterator.get_next_page_response()
        keys = list(iterator.get_items_from_response(response))
        self.assertEqual([key.name for key in keys],
                         ['parent/child/file21.txt',
                          'parent/child/file22.txt'])
        self.assertEqual(iterator.page_number, 1)
        self.assertTrue(iterator.next_page_token is None)
        self.assertEqual(iterator.prefixes,
                         ('parent/child/grand/', 'parent/child/other/'))

    def test_third_level(self):
        # Pseudo-hierarchy can be arbitrarily deep, subject to the limit
        # of 1024 characters in the UTF-8 encoded name:
        # https://cloud.google.com/storage/docs/bucketnaming#objectnames
        # Exercise a layer deeper to illustrate this.
        iterator = self.bucket.iterator(delimiter='/',
                                        prefix='parent/child/grand/')
        response = iterator.get_next_page_response()
        keys = list(iterator.get_items_from_response(response))
        self.assertEqual([key.name for key in keys],
                         ['parent/child/grand/file31.txt'])
        self.assertEqual(iterator.page_number, 1)
        self.assertTrue(iterator.next_page_token is None)
        self.assertEqual(iterator.prefixes, ())


class TestStorageSignURLs(TestStorageFiles):

    def setUp(self):
        super(TestStorageSignURLs, self).setUp()

        logo_path = self.FILES['logo']['path']
        with open(logo_path, 'r') as file_obj:
            self.LOCAL_FILE = file_obj.read()

        key = self.bucket.new_key('LogoToSign.jpg')
        key.upload_from_string(self.LOCAL_FILE)
        self.case_keys_to_delete.append(key)

    def tearDown(self):
        for key in self.case_keys_to_delete:
            if key.exists():
                key.delete()

    def test_create_signed_read_url(self):
        key = self.bucket.new_key('LogoToSign.jpg')
        expiration = int(time.time() + 5)
        signed_url = key.generate_signed_url(expiration, method='GET')

        response, content = HTTP.request(signed_url, method='GET')
        self.assertEqual(response.status, 200)
        self.assertEqual(content, self.LOCAL_FILE)

    def test_create_signed_delete_url(self):
        key = self.bucket.new_key('LogoToSign.jpg')
        expiration = int(time.time() + 283473274)
        signed_delete_url = key.generate_signed_url(expiration,
                                                    method='DELETE')

        response, content = HTTP.request(signed_delete_url, method='DELETE')
        self.assertEqual(response.status, 204)
        self.assertEqual(content, '')

        # Check that the key has actually been deleted.
        self.assertFalse(key in self.bucket)
