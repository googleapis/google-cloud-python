# Copyright 2015 Google Inc. All rights reserved.
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

import unittest2


class TestIndex(unittest2.TestCase):
    PROJECT = 'project'
    INDEX_ID = 'index-id'

    def _getTargetClass(self):
        from gcloud.search.index import Index
        return Index

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _setUpConstants(self):
        import datetime
        from gcloud._helpers import UTC

        self.WHEN_TS = 1437767599.006
        self.WHEN = datetime.datetime.utcfromtimestamp(self.WHEN_TS).replace(
            tzinfo=UTC)
        self.ZONE_ID = 12345

    def _makeResource(self):
        self._setUpConstants()
        return {
            'projectId': self.PROJECT,
            'indexId': self.INDEX_ID,
            'indexedField': {
                'textFields': ['text-1', 'text-2'],
                'htmlFields': ['html-1', 'html-2'],
                'atomFields': ['atom-1', 'atom-2'],
                'dateFields': ['date-1', 'date-2'],
                'numberFields': ['number-1', 'number-2'],
                'geoFields': ['geo-1', 'geo-2'],
            }
        }

    def _makeDocumentResource(self, doc_id, rank=None, title=None):
        resource = {'docId': doc_id}
        if rank is not None:
            resource['rank'] = rank
        if title is not None:
            resource['fields'] = {
                'title': {
                    'values': [{
                        'stringValue': title,
                        'stringFormat': 'text',
                        'lang': 'en'}]
                }
            }
        return resource

    def _verifyResourceProperties(self, index, resource):

        self.assertEqual(index.name, resource.get('indexId'))
        field_info = resource.get('indexedField', {})
        self.assertEqual(index.text_fields, field_info.get('textFields'))
        self.assertEqual(index.html_fields, field_info.get('htmlFields'))
        self.assertEqual(index.atom_fields, field_info.get('atomFields'))
        self.assertEqual(index.date_fields, field_info.get('dateFields'))
        self.assertEqual(index.number_fields, field_info.get('numberFields'))
        self.assertEqual(index.geo_fields, field_info.get('geoFields'))

    def _verifyDocumentResource(self, documents, resource):
        from gcloud.search.document import Document
        from gcloud.search.document import StringValue
        self.assertEqual(len(documents), len(resource))
        for found, expected in zip(documents, resource):
            self.assertTrue(isinstance(found, Document))
            self.assertEqual(found.name, expected['docId'])
            self.assertEqual(found.rank, expected.get('rank'))
            e_fields = expected.get('fields', ())
            self.assertEqual(sorted(found.fields), sorted(e_fields))
            for field, f_field in found.fields.items():
                e_field = e_fields[field]
                for f_value, e_value in zip(f_field.values, e_field['values']):
                    self.assertTrue(isinstance(f_value, StringValue))
                    self.assertEqual(f_value.string_value,
                                     e_value['stringValue'])
                    self.assertEqual(f_value.string_format,
                                     e_value['stringFormat'])
                    self.assertEqual(f_value.language,
                                     e_value['lang'])

    def test_ctor(self):
        client = _Client(self.PROJECT)
        index = self._makeOne(self.INDEX_ID, client)
        self.assertEqual(index.name, self.INDEX_ID)
        self.assertTrue(index._client is client)
        self.assertEqual(index.project, client.project)
        self.assertEqual(
            index.path,
            '/projects/%s/indexes/%s' % (self.PROJECT, self.INDEX_ID))
        self.assertEqual(index.text_fields, None)
        self.assertEqual(index.html_fields, None)
        self.assertEqual(index.atom_fields, None)
        self.assertEqual(index.date_fields, None)
        self.assertEqual(index.number_fields, None)
        self.assertEqual(index.geo_fields, None)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {}
        klass = self._getTargetClass()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {
            'indexId': self.INDEX_ID,
        }
        klass = self._getTargetClass()
        index = klass.from_api_repr(RESOURCE, client=client)
        self.assertTrue(index._client is client)
        self._verifyResourceProperties(index, RESOURCE)

    def test_from_api_repr_w_properties(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = self._makeResource()
        klass = self._getTargetClass()
        index = klass.from_api_repr(RESOURCE, client=client)
        self.assertTrue(index._client is client)
        self._verifyResourceProperties(index, RESOURCE)

    def test_list_documents_defaults(self):
        DOCID_1 = 'docid-one'
        DOCID_2 = 'docid-two'
        PATH = 'projects/%s/indexes/%s/documents' % (
            self.PROJECT, self.INDEX_ID)
        TOKEN = 'TOKEN'
        DOC_1 = self._makeDocumentResource(DOCID_1)
        DOC_2 = self._makeDocumentResource(DOCID_2)
        RESPONSE = {
            'nextPageToken': TOKEN,
            'documents': [DOC_1, DOC_2],
        }
        client = _Client(self.PROJECT)
        conn = client.connection = _Connection(RESPONSE)
        index = self._makeOne(self.INDEX_ID, client)

        documents, token = index.list_documents()

        self._verifyDocumentResource(documents, RESPONSE['documents'])
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {})

    def test_list_documents_explicit(self):
        DOCID_1 = 'docid-one'
        RANK_1 = 2345
        TITLE_1 = 'Title One'
        DOCID_2 = 'docid-two'
        RANK_2 = 1234
        TITLE_2 = 'Title Two'
        PATH = 'projects/%s/indexes/%s/documents' % (
            self.PROJECT, self.INDEX_ID)
        TOKEN = 'TOKEN'
        DOC_1 = self._makeDocumentResource(DOCID_1, RANK_1, TITLE_1)
        DOC_2 = self._makeDocumentResource(DOCID_2, RANK_2, TITLE_2)
        RESPONSE = {'documents': [DOC_1, DOC_2]}
        client = _Client(self.PROJECT)
        conn = client.connection = _Connection(RESPONSE)
        index = self._makeOne(self.INDEX_ID, client)

        documents, token = index.list_documents(
            max_results=3, page_token=TOKEN, view='FULL')

        self._verifyDocumentResource(documents, RESPONSE['documents'])
        self.assertEqual(token, None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'pageSize': 3,
                          'pageToken': TOKEN,
                          'view': 'FULL'})

    def test_document_defaults(self):
        from gcloud.search.document import Document
        DOCUMENT_ID = 'document-id'
        client = _Client(self.PROJECT)
        index = self._makeOne(self.INDEX_ID, client)

        document = index.document(DOCUMENT_ID)

        self.assertTrue(isinstance(document, Document))
        self.assertEqual(document.name, DOCUMENT_ID)
        self.assertEqual(document.rank, None)
        self.assertTrue(document.index is index)

    def test_document_explicit(self):
        from gcloud.search.document import Document
        DOCUMENT_ID = 'document-id'
        RANK = 1234
        client = _Client(self.PROJECT)
        index = self._makeOne(self.INDEX_ID, client)

        document = index.document(DOCUMENT_ID, rank=RANK)

        self.assertTrue(isinstance(document, Document))
        self.assertEqual(document.name, DOCUMENT_ID)
        self.assertEqual(document.rank, RANK)
        self.assertTrue(document.index is index)

    def test_search_defaults(self):
        DOCID_1 = 'docid-one'
        TITLE_1 = 'Title One'
        DOCID_2 = 'docid-two'
        TITLE_2 = 'Title Two'
        PATH = 'projects/%s/indexes/%s/search' % (
            self.PROJECT, self.INDEX_ID)
        TOKEN = 'TOKEN'
        DOC_1 = self._makeDocumentResource(DOCID_1, title=TITLE_1)
        DOC_2 = self._makeDocumentResource(DOCID_2, title=TITLE_2)
        QUERY = 'query string'
        RESPONSE = {
            'nextPageToken': TOKEN,
            'matchedCount': 2,
            'results': [DOC_1, DOC_2],
        }
        client = _Client(self.PROJECT)
        conn = client.connection = _Connection(RESPONSE)
        index = self._makeOne(self.INDEX_ID, client)

        documents, token, matched_count = index.search(QUERY)

        self._verifyDocumentResource(documents, RESPONSE['results'])
        self.assertEqual(token, TOKEN)
        self.assertEqual(matched_count, 2)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {'query': QUERY})

    def test_search_explicit(self):
        DOCID_1 = 'docid-one'
        TITLE_1 = 'Title One'
        FUNKY_1 = 'this is a funky show'
        RANK_1 = 2345
        DOCID_2 = 'docid-two'
        TITLE_2 = 'Title Two'
        FUNKY_2 = 'delighfully funky ambiance'
        RANK_2 = 1234
        PATH = 'projects/%s/indexes/%s/search' % (
            self.PROJECT, self.INDEX_ID)
        TOKEN = 'TOKEN'

        def _makeFunky(text):
            return {
                'values': [{
                    'stringValue': text,
                    'stringFormat': 'text',
                    'lang': 'en',
                }]
            }

        DOC_1 = self._makeDocumentResource(DOCID_1, RANK_1, TITLE_1)
        DOC_1['fields']['funky'] = _makeFunky(FUNKY_1)
        DOC_2 = self._makeDocumentResource(DOCID_2, RANK_2, TITLE_2)
        DOC_2['fields']['funky'] = _makeFunky(FUNKY_2)
        EXPRESSIONS = {'funky': 'snippet("funky", content)'}
        QUERY = 'query string'
        RESPONSE = {
            'matchedCount': 2,
            'results': [DOC_1, DOC_2],
        }
        client = _Client(self.PROJECT)
        conn = client.connection = _Connection(RESPONSE)
        index = self._makeOne(self.INDEX_ID, client)

        documents, token, matched_count = index.search(
            query=QUERY,
            max_results=3,
            page_token=TOKEN,
            field_expressions=EXPRESSIONS,
            order_by=['title'],
            matched_count_accuracy=100,
            scorer='generic',
            scorer_size=20,
            return_fields=['_rank', 'title', 'funky'],
            )

        self._verifyDocumentResource(documents, RESPONSE['results'])
        self.assertEqual(token, None)
        self.assertEqual(matched_count, 2)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        expected_params = {
            'query': QUERY,
            'pageSize': 3,
            'pageToken': TOKEN,
            'fieldExpressions': EXPRESSIONS,
            'orderBy': ['title'],
            'matchedCountAccuracy': 100,
            'scorer': 'generic',
            'scorerSize': 20,
            'returnFields': ['_rank', 'title', 'funky'],
        }
        self.assertEqual(req['query_params'], expected_params)


class _Client(object):

    def __init__(self, project='project', connection=None):
        self.project = project
        self.connection = connection


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from gcloud.exceptions import NotFound
        self._requested.append(kw)

        response, self._responses = self._responses[0], self._responses[1:]
        return response
