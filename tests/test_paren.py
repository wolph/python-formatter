from formatter2 import Formatter


def test_paren_simple():
    assert Formatter.format_string('(1,)') == '(1, )\n\n'
    assert Formatter.format_string('()') == '()\n\n'
    assert Formatter.format_string('(())') == '(())\n\n'


def test_generator():
    assert (Formatter.format_string('(x for x in range(5) if x)')
            == '(x for x in range(5) if x)\n\n')
    assert (Formatter.format_string('((x, y) for x, y in enumerate(range(5)))')
            == '((x, y) for x, y in enumerate(range(5)))\n\n')


def test_paren_complex():
    assert (Formatter.format_string('((1,2,3,(4,5),6,(7,(8,))),)')
            == '((1, 2, 3, (4, 5), 6, (7, (8, ))), )\n\n')

if __name__ == '__main__':
    from .base_test import main
    main('-vv')

