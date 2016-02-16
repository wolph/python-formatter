import pytest

from formatter2 import Formatter


def test_syntax_error():
    with pytest.raises(SyntaxError):
        Formatter.format_string('a = '),

if __name__ == '__main__':
    from .base_test import main
    main('-vv')

