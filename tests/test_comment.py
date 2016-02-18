import pytest

from formatter2 import Formatter


@pytest.mark.parametrize('input_,expected', [
    ("''", "''\n\n"),
    ("#test", "# test\n\n"),
    ("'ab'", "'ab'\n\n"),
    ('"ab"', "'ab'\n\n"),
    (r"'a\'b'", "'''a\\'b'''\n\n"),
    ('"""a\n\nb"""', "'''a\n\nb'''\n\n"),
    ("'''a\n\nb'''", "'''a\n\nb'''\n\n"),
])
def test_comments(input_, expected):
    actual = Formatter.format_string(input_)
    print('input: #%s#' % input_)
    print('input: #%r#' % input_)
    print('expected: #%s#' % expected)
    print('expected: #%r#' % expected)
    print('actual: #%s#' % actual)
    print('actual: #%r#' % actual)
    assert actual == expected


if __name__ == '__main__':
    from .base_test import main
    main('-vv')


