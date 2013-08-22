from formatter import types, tokens

def test_types():
    assert repr(types.TOKEN_TYPES)
    t = tokens.Token({(0, ''): None}, 0, '', (0, 0), (0, 0), '')
    t.line = 'abc'
    t.row = t.row
    assert t == 0
    assert not t == None
    assert t == (t.tok_type, t.token)
    # Yes, sounds weird but to make things easier (matching the end)
    # this is a more convenient working of the equals
    assert not t == t
    assert t > t
    assert not t < t
    assert not t < 0
    try:
        t == test_types
    except TypeError:
        pass

if __name__ == '__main__':
    from base_test import main
    main('-vv')
