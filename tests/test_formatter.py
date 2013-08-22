from formatter import Formatter
from nose import tools


@tools.raises(SyntaxError)
def test_syntax_error():
    Formatter.format_string('a = '),

if __name__ == '__main__':
    from base_test import main
    main('-vv')
