from unittest import TestCase
from google.cloud.firestore_v1beta1 import db
import json


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

