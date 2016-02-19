import pytest

from formatter2 import Formatter


@pytest.mark.parametrize('input_,expected', [
    # Test simple parenthesis
    ('(1,)', '(1, )\n\n'),
    ('()', '()\n\n'),
    ('(())', '(())\n\n'),

    # Test generators
    ('(x for x in range(5) if x)', '(x for x in range(5) if x)\n\n'),
    ('((x, y) for x, y in enumerate(range(5)))',
     '((x, y) for x, y in enumerate(range(5)))\n\n'),

    # Test complex parenthesis
    ('((1,2,3,(4,5),6,(7,(8,))),)',
     '((1, 2, 3, (4, 5), 6, (7, (8, ))), )\n\n'),

])
def test_paren(input_, expected):
    actual = Formatter.format_string(input_)
    assert actual == expected


if __name__ == '__main__':
    from .base_test import main
    main('-vv')
