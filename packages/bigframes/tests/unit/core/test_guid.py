import types
import unittest

from bigframes.core.guid import SequentialUIDGenerator


class TestSequentialUIDGenerator(unittest.TestCase):
    def test_get_uid_stream_returns_generator(self):
        generator = SequentialUIDGenerator()
        stream = generator.get_uid_stream("prefix")
        self.assertIsInstance(stream, types.GeneratorType)

    def test_generator_yields_correct_uids(self):
        generator = SequentialUIDGenerator()
        stream = generator.get_uid_stream("prefix")
        self.assertEqual(next(stream), "prefix0")
        self.assertEqual(next(stream), "prefix1")
        self.assertEqual(next(stream), "prefix2")

    def test_generator_yields_different_uids_for_different_prefixes(self):
        generator = SequentialUIDGenerator()
        stream_a = generator.get_uid_stream("prefixA")
        stream_b = generator.get_uid_stream("prefixB")
        self.assertEqual(next(stream_a), "prefixA0")
        self.assertEqual(next(stream_b), "prefixB0")
        self.assertEqual(next(stream_a), "prefixA1")
        self.assertEqual(next(stream_b), "prefixB1")

    def test_multiple_calls_continue_generation(self):
        generator = SequentialUIDGenerator()
        stream1 = generator.get_uid_stream("prefix")
        self.assertEqual(next(stream1), "prefix0")
        self.assertEqual(next(stream1), "prefix1")

        stream2 = generator.get_uid_stream("prefix")
        self.assertEqual(next(stream2), "prefix2")
        self.assertEqual(next(stream2), "prefix3")


if __name__ == "__main__":
    unittest.main()
