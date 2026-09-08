"""
Unit tests for `pyutils.immutables`.

Covers:
    * ReadOnlyMeta   - blocks re-assignment of existing attributes
    * ReadOnlyDictWrapper - read-only mapping wrapper
    * imdict         - immutable dict implementation
"""
import unittest

from pyutils_generic.immutables import ReadOnlyMeta, ReadOnlyDictWrapper, imdict


class TestReadOnlyMeta(unittest.TestCase):
    """Tests for the standalone ReadOnlyMeta base."""

    def test_modifying_existing_attribute_raises(self):
        # ReadOnlyMeta blocks re-assigning an attribute already present in the
        # instance's own __dict__.
        class Config(ReadOnlyMeta):
            pass

        instance = Config()
        instance.token = "first"
        with self.assertRaises(AttributeError):
            instance.token = "second"

    def test_setting_new_attribute_is_allowed(self):
        class Config(ReadOnlyMeta):
            CONSTANT = 42

        instance = Config()
        instance.NEW_ATTR = "ok"
        self.assertEqual(instance.NEW_ATTR, "ok")


class TestReadOnlyDictWrapper(unittest.TestCase):
    """Tests for the read-only mapping wrapper."""

    def test_wraps_and_reads_values(self):
        wrapper = ReadOnlyDictWrapper({"a": 1, "b": 2})
        self.assertEqual(wrapper["a"], 1)
        self.assertEqual(wrapper["b"], 2)

    def test_len_and_iter(self):
        wrapper = ReadOnlyDictWrapper({"a": 1, "b": 2})
        self.assertEqual(len(wrapper), 2)
        self.assertEqual(set(iter(wrapper)), {"a", "b"})

    def test_non_dict_input_raises(self):
        with self.assertRaises(Exception):
            ReadOnlyDictWrapper(["not", "a", "dict"])

    def test_does_not_support_item_assignment(self):
        wrapper = ReadOnlyDictWrapper({"a": 1})
        with self.assertRaises(TypeError):
            wrapper["a"] = 2

    def test_is_a_defensive_copy(self):
        source = {"a": 1}
        wrapper = ReadOnlyDictWrapper(source)
        source["a"] = 99
        self.assertEqual(wrapper["a"], 1)


class TestImdict(unittest.TestCase):
    """Tests for the immutable dict implementation."""

    def test_reads_values(self):
        d = imdict({"a": 1})
        self.assertEqual(d["a"], 1)

    def test_setitem_raises(self):
        d = imdict({"a": 1})
        with self.assertRaises(TypeError):
            d["a"] = 2

    def test_delitem_raises(self):
        d = imdict({"a": 1})
        with self.assertRaises(TypeError):
            del d["a"]

    def test_update_raises(self):
        d = imdict({"a": 1})
        with self.assertRaises(TypeError):
            d.update({"b": 2})

    def test_pop_raises(self):
        d = imdict({"a": 1})
        with self.assertRaises(TypeError):
            d.pop("a")

    def test_clear_raises(self):
        d = imdict({"a": 1})
        with self.assertRaises(TypeError):
            d.clear()

    def test_is_hashable(self):
        d = imdict({"a": 1})
        # id-based hashing means it can be used as a dict key / set member.
        self.assertEqual(hash(d), id(d))
        self.assertIn(d, {d: "value"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
