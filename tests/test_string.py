from formatter2 import types, tokens, Formatter


def test_string():
    assert Formatter.format_string('''a = 'b' ''') == '''a = 'b'\n\n'''

    formatter = Formatter()
    formatter.format_path('tests/samples/continuations.py')


def test_string_type():
    x = types.StringTokenType(-255, 'TEST')
    t = tokens.Token({(0, ''): None}, 0, '', (0, 0), (0, 0), '')
    x.preprocess(t)

    assert Formatter.format_string("a = '''b'''") == '''a = 'b'\n\n'''
    assert Formatter.format_string('''a = """b'c"""''') == "a = '''b'c'''\n\n"
    assert Formatter.format_string('''a = "b'c"''') == "a = '''b'c'''\n\n"
    assert Formatter.format_string('a = """b"""') == '''a = 'b'\n\n'''
    assert Formatter.format_string('''a = """b'c"""''') == "a = '''b'c'''\n\n"
    assert (Formatter.format_string("""a = '''b\'\'\'c'''""")
            == 'a = """b\'\'\'c"""\n\n')
    assert (Formatter.format_string('''a = "b\'\'\'c"''')
            == 'a = "b\'\'\'c"\n\n')
    assert (Formatter.format_string("a = '''b\n\nc'''")
            == "a = '''b\n\nc'''\n\n")

if __name__ == '__main__':
    from .base_test import main
    main('-vv')

