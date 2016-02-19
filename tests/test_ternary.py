import pytest

from formatter2 import Formatter


@pytest.mark.parametrize('input_,expected', [
    ('1 if 2 else 3', '1 if 2 else 3\n\n'),
    ('1    if    2     else    3', '1 if 2 else 3\n\n'),
])
def test_comments(input_, expected):
    actual = Formatter.format_string(input_)
    assert actual == expected


if __name__ == '__main__':
    from .base_test import main
    main('-vv')

