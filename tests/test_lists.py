from formatter2 import Formatter


def test_list():
    assert Formatter.format_string('[]') == '[]\n\n'
    assert Formatter.format_string('[0]') == '[0]\n\n'


def test_list_comprehension():
    assert (Formatter.format_string('[x for x in range(5) if x]')
            == '[x for x in range(5) if x]\n\n')
    assert (
        Formatter.format_string('[(x, y) for x, y in enumerate(range(5))]')
        == '[(x, y) for x, y in enumerate(range(5))]\n\n')


def test_slice():
    assert Formatter.format_string('x[:]') == 'x[:]\n\n'
    assert Formatter.format_string('x[1:]') == 'x[1:]\n\n'
    assert Formatter.format_string('x[:1]') == 'x[:1]\n\n'
    assert Formatter.format_string('x[1:1]') == 'x[1:1]\n\n'
    assert Formatter.format_string('x[-1:1]') == 'x[-1:1]\n\n'
    assert Formatter.format_string('x[1:-1]') == 'x[1:-1]\n\n'
    assert Formatter.format_string('x[-1:-1]') == 'x[-1:-1]\n\n'
    assert Formatter.format_string('x[-1:]') == 'x[-1:]\n\n'
    assert Formatter.format_string('x[:-1]') == 'x[:-1]\n\n'

if __name__ == '__main__':
    from .base_test import main
    main('-vv')

