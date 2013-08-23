from formatter import Formatter
from nose import tools


def test_paren_simple():
    tools.eq_(
        Formatter.format_string('(1,)'),
        '(1, )\n',
    )
    tools.eq_(
        Formatter.format_string('()'),
        '()\n',
    )
    tools.eq_(
        Formatter.format_string('(())'),
        '(())\n',
    )


def test_generator():
    tools.eq_(
        Formatter.format_string('(x for x in range(5) if x)'),
        '(x for x in range(5) if x)\n',
    )
    tools.eq_(
        Formatter.format_string('((x, y) for x, y in enumerate(range(5)))'),
        '((x, y) for x, y in enumerate(range(5)))\n',
    )


def test_paren_complex():
    tools.eq_(
        Formatter.format_string('((1,2,3,(4,5),6,(7,(8,))),)'),
        '((1, 2, 3, (4, 5), 6, (7, (8, ))), )\n',
    )

if __name__ == '__main__':
    from base_test import main
    main('-vv')
