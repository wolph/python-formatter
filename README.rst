Introduction
============

`formatter` is a Python formatter based on the `tokenize` library in Python.
Due to a bug with line continuations we are currently running a fork of the
`tokenize` library however.

Install
=======

To install simply execute `python setup.py install` or `pip install
formatter`.
If you want to run the tests first, run `python setup.py nosetests`

Usage
=====

To format all of your code recursively (MAKE BACKUPS!):

    formatter -r DIRECTORY

