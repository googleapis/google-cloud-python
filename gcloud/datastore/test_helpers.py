from datetime import datetime
import time

import unittest2

from gcloud.datastore import helpers
from gcloud.datastore.key import Key


class TestHelpers(unittest2.TestCase):

  def test_get_protobuf_attribute(self):
    mapping = (
        (str(), 'string_value'),
        (unicode(), 'string_value'),
        (int(), 'integer_value'),
        (long(), 'integer_value'),
        (float(), 'double_value'),
        (bool(), 'boolean_value'),
        (datetime.now(), 'timestamp_microseconds_value'),
        (Key(), 'key_value'),
        )

    for test_value, expected_name in mapping:
      actual_name, _ = helpers.get_protobuf_attribute_and_value(test_value)
      self.assertEqual(expected_name, actual_name,
          'Test value "%s" expected %s, got %s' % (
            test_value, expected_name, actual_name))

  def test_get_protobuf_value(self):
    now = datetime.now()

    mapping = (
        (str('string'), 'string'),
        (unicode('string'), 'string'),
        (int(), int()),
        (long(), int()),
        (float(), float()),
        (bool(), bool()),
        (now, time.mktime(now.timetuple())),
        (Key(), Key().to_protobuf()),
        )

    for test_value, expected_value in mapping:
      _, actual_value = helpers.get_protobuf_attribute_and_value(test_value)
      self.assertEqual(expected_value, actual_value,
          'Test value "%s" expected %s, got %s.' % (
            test_value, expected_value, actual_value))
