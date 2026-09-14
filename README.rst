Readme
======

Introduction
------------

.. image:: https://img.shields.io/github/actions/workflow/status/wolph/python-formatter/ci.yml?branch=master&label=CI&style=flat-square&labelColor=555
    :alt: Test Status
    :target: https://github.com/wolph/python-formatter/actions/workflows/ci.yml?query=branch%3Amaster

.. image:: https://img.shields.io/coverallsCoverage/github/wolph/python-formatter?branch=master&style=flat-square&labelColor=555
    :alt: Coverage Status
    :target: https://coveralls.io/github/wolph/python-formatter?branch=master

`formatter2` is a Python formatter based on the `tokenize` library in Python.
Due to a bug with line continuations we are currently running a fork of the
`tokenize` library however.

During every format sequence the `compile` method is used to check if no code
has been broken, but backing up is still a good idea.

The library is made to be very extendable and configurable but it's still in 
the beginning phase. Eventually this will become a fully featured formatting 
tool for Python.

Install
-------

To install simply execute `python setup.py install` or `pip install
formatter2`.
If you want to run the tests first, run `nosetests`

Usage
-----

To format all of your code recursively (MAKE BACKUPS!):

    python-formatter -r DIRECTORY

Or:

    format-python -r DIRECTORY

Formatting stdin is also possible:

    cat some_python_file.py | format-python - > some_formatted_file.py
