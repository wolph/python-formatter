from formatter2 import (TokenOffsets, TokenOffset, TOKEN_OFFSETS, tokens,
                        _stringio)
import pytest
import logging


def test_default_type():
    TOKEN_OFFSETS['something_not_existing'] = None


def test_token_offsets():
    t = TokenOffsets(None)
    assert repr(t)
    assert TOKEN_OFFSETS['='].surround
    TOKEN_OFFSETS['='].surround = 0, 0
    TOKEN_OFFSETS[':'] = TokenOffset(
        t,
        t.parent.type,
        t.parent.token,
        children=t,
    )

    x = tokens.SmartList(1, 2)
    assert str(x)
    x.copy()
    x + x

    x.set(5)

    y = tokens.Tokens(_stringio.StringIO('a=1\nb=1').readline)
    y = list(y)
    y[-1] -= y[-1]
    y[0].line = ' ' + y[0].line + ' '
    str(y[0])
    repr(y[0])
    logging.error('token: %r :: %s', y[0], y[0])


def test_add():
    with pytest.raises(TypeError):
        x = tokens.SmartList(1, 2)
        x + 'a'


def test_sub():
    with pytest.raises(TypeError):
        x = tokens.SmartList(1, 2)
        x - 1
        x - (1, 1)
        x - 'a'
