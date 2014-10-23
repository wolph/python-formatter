from __future__ import print_function

from formatter2 import Formatter
from nose import tools
import sys
from io import StringIO


def test_stdin():
    fh = StringIO()
    formatter = Formatter()
    sys.stdin, stdin = fh, sys.stdin

    print(u'test = 123', file=fh)

    fh.seek(0)
    formatter('-'),
    fh.seek(0)
    formatter.format_file('-'),
    fh.seek(0)
    formatter(sys.stdin),

    filename = 'tests/test_brace.py'
    test_brace_contents = open(filename, 'r').read()
    formatter(filename)
    tools.eq_(
        test_brace_contents,
        open(filename, 'r').read(),
    )

    sys.stdin = stdin


if __name__ == '__main__':
    from .base_test import main
    main('-vv')

