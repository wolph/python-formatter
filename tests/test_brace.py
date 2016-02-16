from formatter2 import Formatter


def test_brace_simple():
    assert Formatter.format_string('{1:2,}') == '{1: 2, }\n\n'
    assert Formatter.format_string('{}') == '{}\n\n'
    assert Formatter.format_string('{"a": {}}') == '''{'a': {}}\n\n'''


def test_brace_complex():
    assert (Formatter.format_string('''{1: {'a': 123, 'b': 'c'}}''')
            == '''{1: {'a': 123, 'b': 'c'}}\n\n''')

if __name__ == '__main__':
    from .base_test import main
    main('-vv')

