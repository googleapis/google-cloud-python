# -*- coding: utf-8 -*-
# Copyright 2018 Google LLC
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

import unittest

import mock


class Test__tokenize_field_path(unittest.TestCase):
    @staticmethod
    def _call_fut(path):
        from google.cloud.firestore_v1beta1 import field_path

        return field_path._tokenize_field_path(path)

    def _expect(self, path, split_path):
        self.assertEqual(list(self._call_fut(path)), split_path)

    def test_w_empty(self):
        self._expect("", [])

    def test_w_single_dot(self):
        self._expect(".", ["."])

    def test_w_single_simple(self):
        self._expect("abc", ["abc"])

    def test_w_single_quoted(self):
        self._expect("`c*de`", ["`c*de`"])

    def test_w_quoted_embedded_dot(self):
        self._expect("`c*.de`", ["`c*.de`"])

    def test_w_quoted_escaped_backtick(self):
        self._expect(r"`c*\`de`", [r"`c*\`de`"])

    def test_w_dotted_quoted(self):
        self._expect("`*`.`~`", ["`*`", ".", "`~`"])

    def test_w_dotted(self):
        self._expect("a.b.`c*de`", ["a", ".", "b", ".", "`c*de`"])

    def test_w_dotted_escaped(self):
        self._expect("_0.`1`.`+2`", ["_0", ".", "`1`", ".", "`+2`"])

    def test_w_unconsumed_characters(self):
        path = "a~b"
        with self.assertRaises(ValueError):
            list(self._call_fut(path))


class Test_split_field_path(unittest.TestCase):
    @staticmethod
    def _call_fut(path):
        from google.cloud.firestore_v1beta1 import field_path

        return field_path.split_field_path(path)

    def test_w_single_dot(self):
        with self.assertRaises(ValueError):
            self._call_fut(".")

    def test_w_leading_dot(self):
        with self.assertRaises(ValueError):
            self._call_fut(".a.b.c")

    def test_w_trailing_dot(self):
        with self.assertRaises(ValueError):
            self._call_fut("a.b.")

    def test_w_missing_dot(self):
        with self.assertRaises(ValueError):
            self._call_fut("a`c*de`f")

    def test_w_half_quoted_field(self):
        with self.assertRaises(ValueError):
            self._call_fut("`c*de")

    def test_w_empty(self):
        self.assertEqual(self._call_fut(""), [])

    def test_w_simple_field(self):
        self.assertEqual(self._call_fut("a"), ["a"])

    def test_w_dotted_field(self):
        self.assertEqual(self._call_fut("a.b.cde"), ["a", "b", "cde"])

    def test_w_quoted_field(self):
        self.assertEqual(self._call_fut("a.b.`c*de`"), ["a", "b", "`c*de`"])

    def test_w_quoted_field_escaped_backtick(self):
        self.assertEqual(self._call_fut(r"`c*\`de`"), [r"`c*\`de`"])


class Test_parse_field_path(unittest.TestCase):
    @staticmethod
    def _call_fut(path):
        from google.cloud.firestore_v1beta1 import field_path

        return field_path.parse_field_path(path)

    def test_wo_escaped_names(self):
        self.assertEqual(self._call_fut("a.b.c"), ["a", "b", "c"])

    def test_w_escaped_backtick(self):
        self.assertEqual(self._call_fut("`a\\`b`.c.d"), ["a`b", "c", "d"])

    def test_w_escaped_backslash(self):
        self.assertEqual(self._call_fut("`a\\\\b`.c.d"), ["a\\b", "c", "d"])

    def test_w_first_name_escaped_wo_closing_backtick(self):
        with self.assertRaises(ValueError):
            self._call_fut("`a\\`b.c.d")


class Test_render_field_path(unittest.TestCase):
    @staticmethod
    def _call_fut(field_names):
        from google.cloud.firestore_v1beta1 import field_path

        return field_path.render_field_path(field_names)

    def test_w_empty(self):
        self.assertEqual(self._call_fut([]), "")

    def test_w_one_simple(self):
        self.assertEqual(self._call_fut(["a"]), "a")

    def test_w_one_starts_w_digit(self):
        self.assertEqual(self._call_fut(["0abc"]), "`0abc`")

    def test_w_one_w_non_alphanum(self):
        self.assertEqual(self._call_fut(["a b c"]), "`a b c`")

    def test_w_one_w_backtick(self):
        self.assertEqual(self._call_fut(["a`b"]), "`a\\`b`")

    def test_w_one_w_backslash(self):
        self.assertEqual(self._call_fut(["a\\b"]), "`a\\\\b`")

    def test_multiple(self):
        self.assertEqual(self._call_fut(["a", "b", "c"]), "a.b.c")


class Test_get_nested_value(unittest.TestCase):

    DATA = {
        "top1": {"middle2": {"bottom3": 20, "bottom4": 22}, "middle5": True},
        "top6": b"\x00\x01 foo",
    }

    @staticmethod
    def _call_fut(path, data):
        from google.cloud.firestore_v1beta1 import field_path

        return field_path.get_nested_value(path, data)

    def test_simple(self):
        self.assertIs(self._call_fut("top1", self.DATA), self.DATA["top1"])

    def test_nested(self):
        self.assertIs(
            self._call_fut("top1.middle2", self.DATA), self.DATA["top1"]["middle2"]
        )
        self.assertIs(
            self._call_fut("top1.middle2.bottom3", self.DATA),
            self.DATA["top1"]["middle2"]["bottom3"],
        )

    def test_missing_top_level(self):
        from google.cloud.firestore_v1beta1.field_path import _FIELD_PATH_MISSING_TOP

        field_path = "top8"
        with self.assertRaises(KeyError) as exc_info:
            self._call_fut(field_path, self.DATA)

        err_msg = _FIELD_PATH_MISSING_TOP.format(field_path)
        self.assertEqual(exc_info.exception.args, (err_msg,))

    def test_missing_key(self):
        from google.cloud.firestore_v1beta1.field_path import _FIELD_PATH_MISSING_KEY

        with self.assertRaises(KeyError) as exc_info:
            self._call_fut("top1.middle2.nope", self.DATA)

        err_msg = _FIELD_PATH_MISSING_KEY.format("nope", "top1.middle2")
        self.assertEqual(exc_info.exception.args, (err_msg,))

    def test_bad_type(self):
        from google.cloud.firestore_v1beta1.field_path import _FIELD_PATH_WRONG_TYPE

        with self.assertRaises(KeyError) as exc_info:
            self._call_fut("top6.middle7", self.DATA)

        err_msg = _FIELD_PATH_WRONG_TYPE.format("top6", "middle7")
        self.assertEqual(exc_info.exception.args, (err_msg,))


class TestFieldPath(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1beta1 import field_path

        return field_path.FieldPath

    def _make_one(self, *args):
        klass = self._get_target_class()
        return klass(*args)

    def test_ctor_w_none_in_part(self):
        with self.assertRaises(ValueError):
            self._make_one("a", None, "b")

    def test_ctor_w_empty_string_in_part(self):
        with self.assertRaises(ValueError):
            self._make_one("a", "", "b")

    def test_ctor_w_integer_part(self):
        with self.assertRaises(ValueError):
            self._make_one("a", 3, "b")

    def test_ctor_w_list(self):
        parts = ["a", "b", "c"]
        with self.assertRaises(ValueError):
            self._make_one(parts)

    def test_ctor_w_tuple(self):
        parts = ("a", "b", "c")
        with self.assertRaises(ValueError):
            self._make_one(parts)

    def test_ctor_w_iterable_part(self):
        with self.assertRaises(ValueError):
            self._make_one("a", ["a"], "b")

    def test_constructor_w_single_part(self):
        field_path = self._make_one("a")
        self.assertEqual(field_path.parts, ("a",))

    def test_constructor_w_multiple_parts(self):
        field_path = self._make_one("a", "b", "c")
        self.assertEqual(field_path.parts, ("a", "b", "c"))

    def test_ctor_w_invalid_chars_in_part(self):
        invalid_parts = ("~", "*", "/", "[", "]", ".")
        for invalid_part in invalid_parts:
            field_path = self._make_one(invalid_part)
            self.assertEqual(field_path.parts, (invalid_part,))

    def test_ctor_w_double_dots(self):
        field_path = self._make_one("a..b")
        self.assertEqual(field_path.parts, ("a..b",))

    def test_ctor_w_unicode(self):
        field_path = self._make_one("一", "二", "三")
        self.assertEqual(field_path.parts, ("一", "二", "三"))

    def test_from_api_repr_w_empty_string(self):
        api_repr = ""
        with self.assertRaises(ValueError):
            self._get_target_class().from_api_repr(api_repr)

    def test_from_api_repr_w_empty_field_name(self):
        api_repr = "a..b"
        with self.assertRaises(ValueError):
            self._get_target_class().from_api_repr(api_repr)

    def test_from_api_repr_w_invalid_chars(self):
        invalid_parts = ("~", "*", "/", "[", "]", ".")
        for invalid_part in invalid_parts:
            with self.assertRaises(ValueError):
                self._get_target_class().from_api_repr(invalid_part)

    def test_from_api_repr_w_ascii_single(self):
        api_repr = "a"
        field_path = self._get_target_class().from_api_repr(api_repr)
        self.assertEqual(field_path.parts, ("a",))

    def test_from_api_repr_w_ascii_dotted(self):
        api_repr = "a.b.c"
        field_path = self._get_target_class().from_api_repr(api_repr)
        self.assertEqual(field_path.parts, ("a", "b", "c"))

    def test_from_api_repr_w_non_ascii_dotted_non_quoted(self):
        api_repr = "a.一"
        with self.assertRaises(ValueError):
            self._get_target_class().from_api_repr(api_repr)

    def test_from_api_repr_w_non_ascii_dotted_quoted(self):
        api_repr = "a.`一`"
        field_path = self._get_target_class().from_api_repr(api_repr)
        self.assertEqual(field_path.parts, ("a", "一"))

    def test_from_string_w_empty_string(self):
        path_string = ""
        with self.assertRaises(ValueError):
            self._get_target_class().from_string(path_string)

    def test_from_string_w_empty_field_name(self):
        path_string = "a..b"
        with self.assertRaises(ValueError):
            self._get_target_class().from_string(path_string)

    def test_from_string_w_leading_dot(self):
        path_string = ".b.c"
        with self.assertRaises(ValueError):
            self._get_target_class().from_string(path_string)

    def test_from_string_w_trailing_dot(self):
        path_string = "a.b."
        with self.assertRaises(ValueError):
            self._get_target_class().from_string(path_string)

    def test_from_string_w_leading_invalid_chars(self):
        invalid_paths = ("~", "*", "/", "[", "]")
        for invalid_path in invalid_paths:
            field_path = self._get_target_class().from_string(invalid_path)
            self.assertEqual(field_path.parts, (invalid_path,))

    def test_from_string_w_embedded_invalid_chars(self):
        invalid_paths = ("a~b", "x*y", "f/g", "h[j", "k]l")
        for invalid_path in invalid_paths:
            with self.assertRaises(ValueError):
                self._get_target_class().from_string(invalid_path)

    def test_from_string_w_ascii_single(self):
        path_string = "a"
        field_path = self._get_target_class().from_string(path_string)
        self.assertEqual(field_path.parts, ("a",))

    def test_from_string_w_ascii_dotted(self):
        path_string = "a.b.c"
        field_path = self._get_target_class().from_string(path_string)
        self.assertEqual(field_path.parts, ("a", "b", "c"))

    def test_from_string_w_non_ascii_dotted(self):
        path_string = "a.一"
        field_path = self._get_target_class().from_string(path_string)
        self.assertEqual(field_path.parts, ("a", "一"))

    def test___hash___w_single_part(self):
        field_path = self._make_one("a")
        self.assertEqual(hash(field_path), hash("a"))

    def test___hash___w_multiple_parts(self):
        field_path = self._make_one("a", "b")
        self.assertEqual(hash(field_path), hash("a.b"))

    def test___hash___w_escaped_parts(self):
        field_path = self._make_one("a", "3")
        self.assertEqual(hash(field_path), hash("a.`3`"))

    def test___eq___w_matching_type(self):
        field_path = self._make_one("a", "b")
        string_path = self._get_target_class().from_string("a.b")
        self.assertEqual(field_path, string_path)

    def test___eq___w_non_matching_type(self):
        field_path = self._make_one("a", "c")
        other = mock.Mock()
        other.parts = "a", "b"
        self.assertNotEqual(field_path, other)

    def test___lt___w_matching_type(self):
        field_path = self._make_one("a", "b")
        string_path = self._get_target_class().from_string("a.c")
        self.assertTrue(field_path < string_path)

    def test___lt___w_non_matching_type(self):
        field_path = self._make_one("a", "b")
        other = object()
        # Python 2 doesn't raise TypeError here, but Python3 does.
        self.assertIs(field_path.__lt__(other), NotImplemented)

    def test___add__(self):
        path1 = "a123", "b456"
        path2 = "c789", "d012"
        path3 = "c789.d012"
        field_path1 = self._make_one(*path1)
        field_path1_string = self._make_one(*path1)
        field_path2 = self._make_one(*path2)
        field_path1 += field_path2
        field_path1_string += path3
        field_path2 = field_path2 + self._make_one(*path1)
        self.assertEqual(field_path1, self._make_one(*(path1 + path2)))
        self.assertEqual(field_path2, self._make_one(*(path2 + path1)))
        self.assertEqual(field_path1_string, field_path1)
        self.assertNotEqual(field_path1, field_path2)
        with self.assertRaises(TypeError):
            field_path1 + 305

    def test_to_api_repr_a(self):
        parts = "a"
        field_path = self._make_one(parts)
        self.assertEqual(field_path.to_api_repr(), "a")

    def test_to_api_repr_backtick(self):
        parts = "`"
        field_path = self._make_one(parts)
        self.assertEqual(field_path.to_api_repr(), r"`\``")

    def test_to_api_repr_dot(self):
        parts = "."
        field_path = self._make_one(parts)
        self.assertEqual(field_path.to_api_repr(), "`.`")

    def test_to_api_repr_slash(self):
        parts = "\\"
        field_path = self._make_one(parts)
        self.assertEqual(field_path.to_api_repr(), r"`\\`")

    def test_to_api_repr_double_slash(self):
        parts = r"\\"
        field_path = self._make_one(parts)
        self.assertEqual(field_path.to_api_repr(), r"`\\\\`")

    def test_to_api_repr_underscore(self):
        parts = "_33132"
        field_path = self._make_one(parts)
        self.assertEqual(field_path.to_api_repr(), "_33132")

    def test_to_api_repr_unicode_non_simple(self):
        parts = "一"
        field_path = self._make_one(parts)
        self.assertEqual(field_path.to_api_repr(), "`一`")

    def test_to_api_repr_number_non_simple(self):
        parts = "03"
        field_path = self._make_one(parts)
        self.assertEqual(field_path.to_api_repr(), "`03`")

    def test_to_api_repr_simple_with_dot(self):
        field_path = self._make_one("a.b")
        self.assertEqual(field_path.to_api_repr(), "`a.b`")

    def test_to_api_repr_non_simple_with_dot(self):
        parts = "a.一"
        field_path = self._make_one(parts)
        self.assertEqual(field_path.to_api_repr(), "`a.一`")

    def test_to_api_repr_simple(self):
        parts = "a0332432"
        field_path = self._make_one(parts)
        self.assertEqual(field_path.to_api_repr(), "a0332432")

    def test_to_api_repr_chain(self):
        parts = "a", "`", "\\", "_3", "03", "a03", "\\\\", "a0332432", "一"
        field_path = self._make_one(*parts)
        self.assertEqual(
            field_path.to_api_repr(), r"a.`\``.`\\`._3.`03`.a03.`\\\\`.a0332432.`一`"
        )

    def test_eq_or_parent_same(self):
        field_path = self._make_one("a", "b")
        other = self._make_one("a", "b")
        self.assertTrue(field_path.eq_or_parent(other))

    def test_eq_or_parent_prefix(self):
        field_path = self._make_one("a", "b")
        other = self._make_one("a", "b", "c")
        self.assertTrue(field_path.eq_or_parent(other))
        self.assertTrue(other.eq_or_parent(field_path))

    def test_eq_or_parent_no_prefix(self):
        field_path = self._make_one("a", "b")
        other = self._make_one("d", "e", "f")
        self.assertFalse(field_path.eq_or_parent(other))
        self.assertFalse(other.eq_or_parent(field_path))

    def test_lineage_empty(self):
        field_path = self._make_one()
        expected = set()
        self.assertEqual(field_path.lineage(), expected)

    def test_lineage_single(self):
        field_path = self._make_one("a")
        expected = set()
        self.assertEqual(field_path.lineage(), expected)

    def test_lineage_nested(self):
        field_path = self._make_one("a", "b", "c")
        expected = set([self._make_one("a"), self._make_one("a", "b")])
        self.assertEqual(field_path.lineage(), expected)
