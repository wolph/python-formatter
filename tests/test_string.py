from formatter import types, tokens, Formatter
from nose import tools


def test_string():
    tools.eq_(
        Formatter.format_string('''a = 'b' '''),
        '''a = 'b'\n\n''',
    )

    formatter = Formatter()
    formatter.format_path('tests/samples/continuations.py')


def test_string_type():
    x = types.StringTokenType(-255, 'TEST')
    t = tokens.Token({(0, ''): None}, 0, '', (0, 0), (0, 0), '')
    x.preprocess(t)

    tools.eq_(
        Formatter.format_string("a = '''b'''"),
        '''a = 'b'\n\n''',
    )

    tools.eq_(
        Formatter.format_string('''a = """b'c"""'''),
        "a = '''b'c'''\n\n",
    )

    tools.eq_(
        Formatter.format_string('''a = "b'c"'''),
        "a = '''b'c'''\n\n",
    )

    tools.eq_(
        Formatter.format_string('a = """b"""'),
        '''a = 'b'\n\n''',
    )

    tools.eq_(
        Formatter.format_string('''a = """b'c"""'''),
        "a = '''b'c'''\n\n",
    )

    tools.eq_(
        Formatter.format_string('''a = """b\'\'\'c"""'''),
        'a = """b\'\'\'c"""\n\n',
    )

if __name__ == '__main__':
    from base_test import main
    main('-vv')

