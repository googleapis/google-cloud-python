# pylint: skip-file
import unittest2


class Test_TypeCheck(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud._apitools.util import Typecheck
        return Typecheck(*args, **kw)

    def test_pass(self):
        self.assertEqual(self._callFUT(123, int), 123)

    def test_fail_w_explicit_msg(self):
        from gcloud._apitools.exceptions import TypecheckError
        with self.assertRaises(TypecheckError) as err:
            self._callFUT(123, str, 'foo')
        self.assertEqual(err.exception.args, ('foo',))

    def test_fail_w_single_type_no_msg(self):
        from gcloud._apitools.exceptions import TypecheckError
        with self.assertRaises(TypecheckError) as err:
            self._callFUT(123, str)

    def test_fail_w_tuple_no_msg(self):
        from gcloud._apitools.exceptions import TypecheckError
        with self.assertRaises(TypecheckError) as err:
            self._callFUT(123, (list, tuple))


class Test_CalculateWaitForRetry(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud._apitools.util import CalculateWaitForRetry
        return CalculateWaitForRetry(*args, **kw)

    def test_w_negative_jitter_lt_max_wait(self):
        import random
        from gcloud._testing import _Monkey
        with _Monkey(random, uniform=lambda lower, upper: lower):
            self.assertEqual(self._callFUT(1, 60), 1.5)

    def test_w_positive_jitter_gt_max_wait(self):
        import random
        from gcloud._testing import _Monkey
        with _Monkey(random, uniform=lambda lower, upper: upper):
            self.assertEqual(self._callFUT(4, 10), 10)


class Test_AcceptableMimeType(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud._apitools.util import AcceptableMimeType
        return AcceptableMimeType(*args, **kw)

    def test_pattern_wo_slash(self):
        from gcloud._apitools.exceptions import InvalidUserInputError
        with self.assertRaises(InvalidUserInputError) as err:
            self._callFUT(['text/*'], 'BOGUS')
        self.assertEqual(
            err.exception.args,
            ('Invalid MIME type: "BOGUS"',))

    def test_accept_pattern_w_semicolon(self):
        from gcloud._apitools.exceptions import GeneratedClientError
        with self.assertRaises(GeneratedClientError) as err:
            self._callFUT(['text/*;charset=utf-8'], 'text/plain')
        self.assertEqual(
            err.exception.args,
            ('MIME patterns with parameter unsupported: '
             '"text/*;charset=utf-8"',))

    def test_miss(self):
        self.assertFalse(self._callFUT(['image/*'], 'text/plain'))

    def test_hit(self):
        self.assertTrue(self._callFUT(['text/*'], 'text/plain'))
