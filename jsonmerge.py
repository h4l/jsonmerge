"""
Merge two or more JSON documents.

Usage:
    jsonmerge.py [-i, --indent=N] <file.json>...

Options:
    -i
        Indent with the default width of 4 spaces.

    --indent=N
        Indent with the specified number of spaces.

Examples:

     $ cat > a.json
     {
        "a": {
            "foo": 1,
            "bar": true
        },
        "b": {
            "foo": 3,
            "bar": false,
            "nested": {
                "a": 1,
                "b": 2
            }
        }
     }
     ^D
     $ cat > b.json
     {
        "a": {
            "baz": "hi"
        },
        "b": {
            "foo": 10,
            "baz": "boz",
            "nested": {
                "b": 10
            }
        }
     }
     ^D
     $ python jsonmerge.py a.json b.json
     {
        "a": {
            "foo": 1,
            "bar": true,
            "baz": "hi"
        },
        "b": {
            "foo": 10,
            "bar": false,
            "baz": "boz",
            "nested": {
                "a": 1,
                "b": 10
            }
        }
     }
"""
import json
import itertools
import sys

import docopt


MISSING = object()


def json_merge_all(json_objects):
    merged = reduce(json_merge, json_objects, MISSING)
    # If json_objects is empty then reduce will return MISSING. (json_merge()
    # never returns missing.)
    if merged == MISSING:
        raise ValueError("json_objects was empty")
    return merged


def json_merge(a, b):
    """
    Merge a and b, returning the result. a and b are unchanged.

    If a and b are dicts they're recursively merged by considering matching
    keys in pairs of dicts to be semantically equivilent.

    The value from b wins in a merge situation in which two values are
    present. The special value MISSING is used to denote a missing value
    (None is considered an actual value).
    """
    if isinstance(a, dict) and isinstance(b, dict):
        return dict(
            (k, json_merge(a_val, b_val))
            for k, a_val, b_val in dictzip_longest(a, b, fillvalue=MISSING)
        )
    elif isinstance(a, list) and isinstance(b, list):
        # Don't try to merge lists by index, just concat them one after
        # another.
        return list(itertools.chain(a, b))

    # At most one of a, b can be MISSING
    if b is MISSING:
        assert a is not MISSING
        return a
    return b


def dictzip_longest(*dicts, **kwargs):
    """
    Like itertools.izip_longest but for dictionaries.

    For each key occuring in any of the dicts a tuple is returned containing
    (key, dict1-val, dict2-val, ... dictn-val)

    The fillvalue kwarg is substituted as the value for any dict not containing
    the key. fillvalue defaults to None.

    The order of the dict keys in the returned list is not defined.

    For example:
    >>> dictzip_longest(dict(a=1, b=2), dict(a=11, b=12), dict(x=100),
                        fillvalue=-1)
        [('a', 1, 11, -1), ('x', -1, -1, 100), ('b', 2, 12, -1)]
    """
    fillvalue = kwargs.get("fillvalue", None)
    keys = reduce(set.union, [set(d.keys()) for d in dicts], set())
    return [tuple([k] + [d.get(k, fillvalue) for d in dicts]) for k in keys]


if __name__ == "__main__":
    args = docopt.docopt(__doc__)

    indent = None
    if args.get("-i") or args.get("--indent") is not None:
        try:
            indent = int(args.get("--indent"))
        except:
            indent = 4

    json_objects = [json.load(open(f)) for f in args["<file.json>"]]
    merged = json_merge_all(json_objects)

    json.dump(merged, sys.stdout, indent=indent)
