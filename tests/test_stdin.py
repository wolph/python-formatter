from formatter import Formatter
from nose import tools
import sys
from StringIO import StringIO


def test_stdin():
    fh = StringIO()
    formatter = Formatter()
    sys.stdin, stdin = fh, sys.stdin

    print >>fh, 'test = 123'

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

if __name__ == '__main__':
    from base_test import main
    main('-vv')

