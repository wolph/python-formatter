import pytest

from formatter2 import Formatter


@pytest.mark.parametrize('input_,expected', [
    # Test lists
    ('[]', '[]\n\n'),
    ('[0]', '[0]\n\n'),

    # Test list comprehension
    ('[x for x in range(5) if x]', '[x for x in range(5) if x]\n\n'),
    ('[(x, y) for x, y in enumerate(range(5))]',
     '[(x, y) for x, y in enumerate(range(5))]\n\n'),

    # Test slicing
    ('x[:]', 'x[:]\n\n'),
    ('x[1:]', 'x[1:]\n\n'),
    ('x[:1]', 'x[:1]\n\n'),
    ('x[1:1]', 'x[1:1]\n\n'),
    ('x[-1:1]', 'x[-1:1]\n\n'),
    ('x[1:-1]', 'x[1:-1]\n\n'),
    ('x[-1:-1]', 'x[-1:-1]\n\n'),
    ('x[-1:]', 'x[-1:]\n\n'),
    ('x[:-1]', 'x[:-1]\n\n'),
])
def test_lists(input_, expected):
    actual = Formatter.format_string(input_)
    assert actual == expected


if __name__ == '__main__':
    from .base_test import main
    main('-vv')
