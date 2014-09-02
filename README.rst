``jsonmerge``
=============

A small command line tool/Python library for deep-merging 2 or more JSON documents.

Example::

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

To Do
-----
Add packaging, upload to PyPi etc.

Similar Projects
----------------

I probably wouldn't have written this if `avian2/jsonmerge <https://github.com/avian2/jsonmerge>`_ existed when I wrote this.
