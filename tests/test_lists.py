from formatter import Formatter
from nose import tools


def test_list():
    tools.eq_(
        Formatter.format_string('[]'),
        '[]\n',
    )
    tools.eq_(
        Formatter.format_string('[0]'),
        '[0]\n',
    )

def test_list_comprehension():
    tools.eq_(
        Formatter.format_string('[x for x in range(5) if x]'),
        '[x for x in range(5) if x]\n',
    )
    tools.eq_(
        Formatter.format_string('[(x, y) for x, y in enumerate(range(5))]'),
        '[(x, y) for x, y in enumerate(range(5))]\n',
    )

def test_slice():
    tools.eq_(
        Formatter.format_string('x[:]'),
        'x[:]\n',
    )
    tools.eq_(
        Formatter.format_string('x[1:]'),
        'x[1:]\n',
    )
    tools.eq_(
        Formatter.format_string('x[:1]'),
        'x[:1]\n',
    )
    tools.eq_(
        Formatter.format_string('x[1:1]'),
        'x[1:1]\n',
    )
    tools.eq_(
        Formatter.format_string('x[-1:1]'),
        'x[-1:1]\n',
    )
    tools.eq_(
        Formatter.format_string('x[1:-1]'),
        'x[1:-1]\n',
    )
    tools.eq_(
        Formatter.format_string('x[-1:-1]'),
        'x[-1:-1]\n',
    )
    tools.eq_(
        Formatter.format_string('x[-1:]'),
        'x[-1:]\n',
    )
    tools.eq_(
        Formatter.format_string('x[:-1]'),
        'x[:-1]\n',
    )

if __name__ == '__main__':
    from base_test import main
    main('-vv')
