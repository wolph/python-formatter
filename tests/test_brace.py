import pytest

from formatter2 import Formatter


@pytest.mark.parametrize('input_,expected', [
    # Test brace simple
    ('{1:2,}', '{1: 2, }\n\n'),
    ('{}', '{}\n\n'),
    ('{"a": {}}', '''{'a': {}}\n\n'''),

    # Test brace complex
    ('''{1: {'a': 123, 'b': 'c'}}''', '''{1: {'a': 123, 'b': 'c'}}\n\n'''),

])
def test_brace(input_, expected):
    actual = Formatter.format_string(input_)
    assert actual == expected

if __name__ == '__main__':
    from .base_test import main
    main('-vv')
