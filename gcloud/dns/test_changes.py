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


class TestChanges(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.dns.changes import Changes
        return Changes

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        zone = _Zone()

        changes = self._makeOne(zone)

        self.assertTrue(changes.zone is zone)
        self.assertEqual(changes.name, None)
        self.assertEqual(changes.status, None)
        self.assertEqual(changes.started, None)
        self.assertEqual(list(changes.additions), [])
        self.assertEqual(list(changes.deletions), [])

    def test_from_api_repr_missing_additions_deletions(self):
        from gcloud._helpers import UTC
        from gcloud._helpers import _NOW
        from gcloud._helpers import _RFC3339_MICROS
        zone = _Zone()
        NAME = 'CHANGES_ID'
        WHEN = _NOW().replace(tzinfo=UTC)
        WHEN_STR = WHEN.strftime(_RFC3339_MICROS)
        RESOURCE = {
            'kind': 'dns#change',
            'id': NAME,
            'status': 'pending',
            'startTime': WHEN_STR,
        }
        zone = _Zone()
        klass = self._getTargetClass()
        changes = klass.from_api_repr(RESOURCE, zone=zone)

        self.assertEqual(changes.name, NAME)
        self.assertEqual(changes.started, WHEN)
        self.assertEqual(changes.status, 'pending')

        self.assertEqual(len(changes.additions), 0)
        self.assertEqual(len(changes.deletions), 0)

    def test_from_api_repr(self):
        from gcloud._helpers import UTC
        from gcloud._helpers import _NOW
        from gcloud._helpers import _RFC3339_MICROS
        NAME = 'CHANGES_ID'
        WHEN = _NOW().replace(tzinfo=UTC)
        WHEN_STR = WHEN.strftime(_RFC3339_MICROS)
        RESOURCE = {
            'kind': 'dns#change',
            'id': NAME,
            'startTime': WHEN_STR,
            'status': 'done',
            'additions' : [
                {'name': 'test.example.com',
                 'type': 'CNAME',
                 'ttl': '3600',
                 'rrdatas': ['www.example.com']},
            ],
            'deletions': [
                {'name': 'test.example.com',
                 'type': 'CNAME',
                 'ttl': '86400',
                 'rrdatas': ['other.example.com']},
            ],
        }
        zone = _Zone()
        klass = self._getTargetClass()
        changes = klass.from_api_repr(RESOURCE, zone=zone)

        self.assertEqual(changes.name, NAME)
        self.assertEqual(changes.started, WHEN)
        self.assertEqual(changes.status, 'done')

        self.assertEqual(len(changes.additions), 1)
        rrs = changes.additions[0]
        self.assertEqual(rrs.name, 'test.example.com')
        self.assertEqual(rrs.record_type, 'CNAME')
        self.assertEqual(rrs.ttl, 3600)
        self.assertEqual(rrs.rrdatas, ['www.example.com'])
        self.assertTrue(rrs.zone is zone)

        self.assertEqual(len(changes.deletions), 1)
        rrs = changes.deletions[0]
        self.assertEqual(rrs.name, 'test.example.com')
        self.assertEqual(rrs.record_type, 'CNAME')
        self.assertEqual(rrs.ttl, 86400)
        self.assertEqual(rrs.rrdatas, ['other.example.com'])
        self.assertTrue(rrs.zone is zone)

    def test_add_record_set_invalid_value(self):
        zone = _Zone()
        changes = self._makeOne(zone)

        with self.assertRaises(ValueError):
            changes.add_record_set(object())

    def test_add_record_set(self):
        from gcloud.dns.resource_record_set import ResourceRecordSet
        zone = _Zone()
        changes = self._makeOne(zone)
        rrs = ResourceRecordSet('test.example.com', 'CNAME', 3600,
                                ['www.example.com'], zone)
        changes.add_record_set(rrs)
        self.assertEqual(list(changes.additions), [rrs])

    def test_delete_record_set_invalid_value(self):
        zone = _Zone()
        changes = self._makeOne(zone)

        with self.assertRaises(ValueError):
            changes.delete_record_set(object())

    def test_delete_record_set(self):
        from gcloud.dns.resource_record_set import ResourceRecordSet
        zone = _Zone()
        changes = self._makeOne(zone)
        rrs = ResourceRecordSet('test.example.com', 'CNAME', 3600,
                                ['www.example.com'], zone)
        changes.delete_record_set(rrs)
        self.assertEqual(list(changes.deletions), [rrs])


class _Zone(object):
    pass
