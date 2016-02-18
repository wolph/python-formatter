from __future__ import print_function
import pytest

from formatter2 import types, tokens, Formatter


@pytest.mark.parametrize('input_,expected', [
    ('''a = 'b' ''', '''a = 'b'\n\n'''),
    ("a = '''b'''", '''a = 'b'\n\n'''),
    ('''a = """b'c"""''', "a = '''b'c'''\n\n"),
    ('''a = "b'c"''', "a = '''b'c'''\n\n"),
    ('a = """b"""', '''a = 'b'\n\n'''),
    ('''a = """b'c"""''', "a = '''b'c'''\n\n"),
    (r"""a = '''b\'\'\'c'''""", "a = '''b\\'\\'\\'c'''\n\n"),
    ('''a = "b\'\'\'c"''', "a = '''b\\'\\'\\'c'''\n\n"),
    ("a = '''b\n\nc'''", "a = '''b\n\nc'''\n\n"),
])
def test_string_formatting(input_, expected):
    actual = Formatter.format_string(input_)
    assert actual == expected


def test_string_type():
    x = types.StringTokenType(-255, 'TEST')
    t = tokens.Token({(0, ''): None}, 0, '', (0, 0), (0, 0), '')
    x.preprocess(t)


if __name__ == '__main__':
    from .base_test import main
    main('-vv')

