import unittest

import jsonmerge


class TestDictzipLongest(unittest.TestCase):
    def test_single_dict_results_in_dicts_items(self):
        d = {1: 2, 3: 4, 5: 6}

        self.assertEqual(
            jsonmerge.dictzip_longest(d),
            list(d.items()))

    def test_empy_dicts_yield_empty_list(self):
        self.assertEqual(
            jsonmerge.dictzip_longest({}, {}, {}, {}),
            [])

    def test_missing_values_are_replaced_by_fillvalue(self):
        x = dict(a=1, b=2, c=3)
        y = dict(a=True, b="hi")
        z = dict(a=None)
        self.assertEqual(
            sorted(jsonmerge.dictzip_longest(x, y, z, fillvalue="MISSING")),
            [("a", 1, True, None),
             ("b", 2, "hi", "MISSING"),
             ("c", 3, "MISSING", "MISSING")])


class TestJsonMerge(unittest.TestCase):
    def test_merging_2_scalar_values_yields_second(self):
        self.assertEqual(jsonmerge.json_merge(123, 456), 456)
        self.assertEqual(jsonmerge.json_merge(123, "foo"), "foo")
        self.assertEqual(jsonmerge.json_merge(123, None), None)

    def test_merging_dict_with_scalar_yields_second(self):
        self.assertEqual(jsonmerge.json_merge({1: 2}, 123), 123)
        self.assertEqual(jsonmerge.json_merge(True, {1: 2}), {1: 2})

    def test_merging_list_with_scalar_yields_second(self):
        self.assertEqual(jsonmerge.json_merge([1, 2], 123), 123)
        self.assertEqual(jsonmerge.json_merge(True, [1, 2]), [1, 2])

    def test_merging_list_with_dict_yields_second(self):
        self.assertEqual(jsonmerge.json_merge([1, 2], {1: 2}), {1: 2})
        self.assertEqual(jsonmerge.json_merge({1: 2}, [1, 2]), [1, 2])

    def test_merging_2_lists_yields_concatenation_of_both(self):
        self.assertEqual(jsonmerge.json_merge([1, 2, 3, 4], [5, 6]),
                         [1, 2, 3, 4, 5, 6])

    def test_merging_2_dicts_yields_dict_with_keys_from_both(self):
        a = dict(a=1, b=2, c=3)
        b = dict(c=-1, d=-2)
        self.assertEqual(set(jsonmerge.json_merge(a, b).keys()),
                         set(a.keys()) | set(b.keys()))

    def test_merging_2_dicts_yields_values_from_second_for_collisions(self):
        a = dict(a=1, b=2, c=3)
        b = dict(a="x", c="y")
        self.assertEqual(jsonmerge.json_merge(a, b),
                         dict(a="x", b=2, c="y"))


class TestJsonMergeAll(unittest.TestCase):
    def test_merging_nothing_results_in_exception(self):
        with self.assertRaises(ValueError):
            jsonmerge.json_merge_all([])

    def test_merging_doc_example(self):
        a = {
            "a": {
                "foo": 1,
                "bar": True
            },
            "b": {
                "foo": 3,
                "bar": False,
                "nested": {
                    "a": 1,
                    "b": 2
                }
            }
        }
        b = {
            "a": {
                "baz": "hi"
            },
            "b": {
                "foo": 10,
                "baz": "boz",
                "nested": {
                    "b": 10
                }
            },
            "c": ["alice"]
        }
        c = {
            "c": ["bill", "ben"]
        }

        expected = {
            "a": {
                "foo": 1,
                "bar": True,
                "baz": "hi"
            },
            "b": {
                "foo": 10,
                "bar": False,
                "baz": "boz",
                "nested": {
                    "a": 1,
                    "b": 10
                }
            },
            "c": ["alice", "bill", "ben"]
        }
        self.assertEqual(jsonmerge.json_merge_all([a, b, c]), expected)
