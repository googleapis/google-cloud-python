from unittest import TestCase
from google.cloud.firestore_v1beta1 import db, SERVER_TIMESTAMP
import json
from datetime import datetime, date


class TestDB(TestCase):
    def test_fields(self):
        # String Field
        string_field = db.StringField(default="test", required=True, length=6)
        self.assertEqual(string_field.validate("roast"), "roast")
        # The default value is set on an empty field
        self.assertEqual(string_field.validate(None), "test")
        # The string requires a maximum length of 6
        self.assertRaises(db.InvalidValueError, string_field.validate, "01234567")
        #  String field should only accept strings
        self.assertRaises(db.InvalidValueError, string_field.validate, 123)
        # Create a field without a default value
        string_field = db.StringField(required=True)
        # This is a required field, None is not a valid value
        self.assertRaises(db.InvalidValueError, string_field.validate, None)

        # Integer field
        integer_field = db.IntegerField()
        self.assertEqual(integer_field.validate(1), 1)
        self.assertEqual(integer_field.validate(0), 0)
        # Float is not a valid value of an integer field
        self.assertRaises(db.InvalidValueError, integer_field.validate, 1.36)
        # String is not a valid integer
        self.assertRaises(db.InvalidValueError, integer_field.validate, "0")
        # None required field defaults to None
        self.assertIsNone(integer_field.validate(None))

        # Float field
        float_field = db.FloatingPointNumberField()
        # Should accept both float and integer values
        self.assertEqual(float_field.validate(0), 0)
        self.assertEqual(float_field.validate(1), 1)
        self.assertEqual(float_field.validate(0.6667), 0.6667)
        self.assertEqual(float_field.validate(3.142), 3.142)
        self.assertRaises(db.InvalidValueError, float_field.validate, "10234")

        # List Field
        list_field = db.ListField(field_type=db.IntegerField())
        self.assertEqual(list_field.validate([1, 2, 3, 4]), [1, 2, 3, 4])
        # An invalid data type is not accepted as part of the child fields
        self.assertRaises(db.InvalidValueError, list_field.validate, [1, 2, ""])

        # Dict Field
        dict_field = db.DictField()
        valid_dict = dict(name="John doe", age=24)
        # A dict, a list, or a valid json string are valid values
        self.assertEqual(dict_field.validate(valid_dict), valid_dict)
        self.assertEqual(dict_field.validate(json.dumps(valid_dict)), valid_dict)
        # A list is not a valid input of dict field
        self.assertRaises(db.InvalidValueError, dict_field.validate, [1, 2, 3])

        # Date time Field
        dt_field = db.DateTimeField(auto_add_now=True)
        now = datetime.now()
        self.assertEqual(dt_field.validate(now), now)
        # Confirm that default is set to server timestamp
        self.assertEqual(dt_field.validate(None), SERVER_TIMESTAMP)
        # A string is not a date time object
        self.assertRaises(db.InvalidValueError, dt_field.validate, "12-may-2019")
        today = date.fromtimestamp(now.timestamp())
        # A date item is a valid entry
        self.assertEqual(dt_field.validate(today), today)
        dt_field = db.DateTimeField(auto_now=True)
        # This value is always updated to current time stamp on every update
        self.assertEqual(dt_field.validate(now), SERVER_TIMESTAMP)

        # Boolean field
        bool_field = db.BooleanField(required=True)
        self.assertTrue(bool_field.validate(True))
        self.assertFalse(bool_field.validate(False))
        self.assertRaises(db.InvalidValueError, bool_field.validate, "some string")
        self.assertRaises(db.InvalidValueError, bool_field.validate, None)  # None is not a valid boolean value
        bool_field = db.BooleanField()
        self.assertIsNone(bool_field.validate(None))

