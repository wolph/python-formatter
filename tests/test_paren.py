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


def test_paren_complex():
    tools.eq_(
        Formatter.format_string('((1,2,3,(4,5),6,(7,(8,))),)'),
        '((1, 2, 3, (4, 5), 6, (7, (8, ))), )\n',
    )

if __name__ == '__main__':
    from base_test import main
    main('-vv')
