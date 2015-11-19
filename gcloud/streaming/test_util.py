import unittest2


class Test_calculate_wait_for_retry(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.streaming.util import calculate_wait_for_retry
        return calculate_wait_for_retry(*args, **kw)

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


class Test_acceptable_mime_type(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.streaming.util import acceptable_mime_type
        return acceptable_mime_type(*args, **kw)

    def test_pattern_wo_slash(self):
        with self.assertRaises(ValueError) as err:
            self._callFUT(['text/*'], 'BOGUS')
        self.assertEqual(
            err.exception.args,
            ('Invalid MIME type: "BOGUS"',))

    def test_accept_pattern_w_semicolon(self):
        with self.assertRaises(ValueError) as err:
            self._callFUT(['text/*;charset=utf-8'], 'text/plain')
        self.assertEqual(
            err.exception.args,
            ('MIME patterns with parameter unsupported: '
             '"text/*;charset=utf-8"',))

    def test_miss(self):
        self.assertFalse(self._callFUT(['image/*'], 'text/plain'))

    def test_hit(self):
        self.assertTrue(self._callFUT(['text/*'], 'text/plain'))
