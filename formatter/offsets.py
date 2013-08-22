import sys
import logging
from cStringIO import StringIO

from .types import TOKEN_TYPES, TokenType

logger = logging.getLogger(__name__)


class TokenOffsets(dict):

    def __init__(self, parent, default_type=None):
        if default_type is not None:
            assert isinstance(default_type, TokenType), 'end must be ' \
                'a TokenType'

        if parent is None:
            parent = DefaultTokenOffset(self)

        assert isinstance(parent, TokenOffset), 'parent must be a ' \
            'TokenOffsets instance, was %r instead' % parent

        self.default_type = default_type
        self.parent = parent

    def __repr__(self):
        return '<%s\n  %s\n>' % (
            self.__class__.__name__,
            '\n  '.join(sorted(repr(v) for v in set(self.itervalues()))),
        )

    def get_key(self, key):
        if isinstance(key, basestring):
            # Only a token given, no string. Return the default token type
            assert self.default_type, 'Token type must be given'
            key = self.default_type, key
        elif hasattr(key, 'tok_type') and hasattr(key, 'token'):
            # Something that looks like a Token was given, extract the
            # parameters
            key = key.tok_type, key.token
        elif isinstance(key, TokenType):
            # A TokenType was given, this means we have no token so we have to
            # assume there isn't one
            key = TOKEN_TYPES[key], None

        # To make lookups work in any case, convert to actual token types
        if not isinstance(key[0], TokenType):
            key = TOKEN_TYPES[key[0]], key[1]

        return key

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key, recurse=False):
        # Unpack the type and the token
        type_, token = key = self.get_key(key)
        if key in self:
            # Return if it completely exists
            value = dict.__getitem__(self, key)
        elif recurse and not isinstance(self.parent, DefaultTokenOffset):
            value = self.parent.parent[key]
        else:
            # Create one, it doesn't exist apparently
            if (type_, None) in self:
                value = dict.__getitem__(self, (type_, None))
                value = value.copy(type_, token)
            else:
                value = TokenOffset(self, type_, token)

            self[key] = value

        return value

    def __setitem__(self, key, value):
        if isinstance(key, basestring):
            assert self.default_type, 'Token type must be given'
            key = self.default_type, key

        dict.__setitem__(self, key, value)


class TokenOffset(object):

    def __init__(self, parent, type_, token, pre=0, post=0, children=None,
                 end=None):
        self.token = token
        self.pre = pre
        self.post = post
        self.type = type_
        self.parent = parent
        self.end = end

        if children is None:
            children = TokenOffsets(
                self,
                default_type=TOKEN_TYPES[type_],
            )
        self.children = children

    def copy(self, type_=None, token=None):
        return TokenOffset(
            parent=self.parent,
            type_=type_ or self.type,
            token=token or self.token,
            pre=self.pre,
            post=self.post,
        )

    def get_parent(self):
        return self._parent

    def set_parent(self, parent):
        assert isinstance(parent, TokenOffsets), 'parent must be a ' \
            'TokenOffset instance, was %s instead' % type(parent)
        self._parent = parent

    parent = property(get_parent, set_parent)

    def get_type(self):
        return self._type

    def set_type(self, type_):
        assert type_ in TOKEN_TYPES, 'Expected %r to be in %r' % (
            type_,
            self,
        )
        self._type = TOKEN_TYPES[type_]

    type = property(get_type, set_type)

    def get_surround(self):
        return self.pre, self.post

    def set_surround(self, surround):
        if isinstance(surround, int):
            pre = post = surround
        else:
            pre, post = surround

        self.pre = pre
        self.post = post

    surround = property(get_surround, set_surround)

    def get_end(self):
        return self._end

    def set_end(self, end):
        if end is not None:
            if not isinstance(end, list):
                end = [end]
            end = map(self.parent.get_key, end)
        self._end = end

    end = property(get_end, set_end)

    def __str__(self):
        return str(getattr(self, 'type', None))

    def __repr__(self):
        return '<%s[%s:%s]%r (%d,%d) %r>' % (
            self.__class__.__name__,
            hex(id(self)),
            self,
            self.token,
            self.pre,
            self.post,
            self.end,
        )


class DefaultTokenOffset(TokenOffset):

    def __init__(self, parent=None):
        if parent is None:
            parent = TokenOffsets(self)

        TokenOffset.__init__(
            self,
            parent=parent,
            type_=TOKEN_TYPES.DEFAULT,
            token=None,
        )

    @classmethod
    def _pprint(cls, stream, offset, visited, depth=0):
        stream.write(' ' * depth)

        if offset.children and offset.end:
            stream.write('[ ')

        offset.end, end = None, offset.end
        print >>stream, repr(offset)
        offset.end = end

        if offset in visited and offset.end:
            stream.write(' ' * (depth + 4))
            print >>stream, 'RECURSION'
        else:
            visited[offset] = True
            for child in sorted(offset.children.values()):
                cls._pprint(stream, child, visited, depth=depth + 4)

        if offset.end:
            stream.write(' ' * depth)
            stream.write('] ')
            print >>stream, repr(offset.end)

    def pprint(self, stream=sys.stderr):
        return self._pprint(stream, self, visited={}, depth=1)


def get_token_offsets():
    token_offset = DefaultTokenOffset()
    token_offsets = token_offset.children

    token_offsets.default_type = TOKEN_TYPES.NAME
    token_offsets['with'].post = 1
    token_offsets['assert'].post = 1
    token_offsets['except'].post = 1
    token_offsets['import'].post = 1
    token_offsets['for'].post = 1
    token_offsets['if'].post = 1
    token_offsets['elif'].post = 1
    token_offsets['return'].post = 1
    token_offsets['as'].surround = 1
    token_offsets['in'].surround = 1
    token_offsets['or'].surround = 1
    token_offsets['and'].surround = 1
    token_offsets['not'].post = 1

    token_offsets.default_type = TOKEN_TYPES.OP
    token_offsets[':'].post = 1
    token_offsets[','].post = 1
    token_offsets['='].post = 1

    # Within parameters we don't want extra space around the =
    paren = token_offsets[TOKEN_TYPES.OP, '(']
    paren.end = TOKEN_TYPES.OP, ')'
    paren.children['='].surround = 0
    paren.children[','].post = 1
    paren.children[TOKEN_TYPES.NAME, 'or'].surround = 1
    paren.children[TOKEN_TYPES.NAME, 'and'].surround = 1
    paren.children[TOKEN_TYPES.NAME].surround = 0

    # Within parameters we don't want extra space around the =
    brace = token_offsets[TOKEN_TYPES.OP, '{']
    brace.end = TOKEN_TYPES.OP, '}'
    brace.children[':'].post = 1
    brace.children[','].post = 1
    brace.children[TOKEN_TYPES.NAME].surround = 0

    # Within slices we don't want extra space around the :
    bracket = token_offsets[TOKEN_TYPES.OP, '[']
    bracket.end = TOKEN_TYPES.OP, ']'
    #bracket.children[':'].surround = 0

    # A little recursion to handle cases with braces in parenthesis and vice
    # versa
    brace.children[TOKEN_TYPES.OP, '{'] = brace
    brace.children[TOKEN_TYPES.OP, '('] = paren
    brace.children[TOKEN_TYPES.OP, '['] = bracket
    paren.children[TOKEN_TYPES.OP, '{'] = brace
    paren.children[TOKEN_TYPES.OP, '('] = paren
    paren.children[TOKEN_TYPES.OP, '['] = bracket
    bracket.children[TOKEN_TYPES.OP, '{'] = brace
    bracket.children[TOKEN_TYPES.OP, '('] = paren
    bracket.children[TOKEN_TYPES.OP, '['] = bracket

    # Classes need a space after class and no space before (
    class_ = token_offsets[TOKEN_TYPES.NAME, 'class']
    class_.post = 1
    class_.end = TOKEN_TYPES.OP, ':'
    class_.children[TOKEN_TYPES.NAME].post = 0
    class_.children[TOKEN_TYPES.OP, '{'] = brace
    class_.children[TOKEN_TYPES.OP, '('] = paren
    class_.children[TOKEN_TYPES.OP, '['] = bracket

    # Def need a space after def and no space before (
    def_ = token_offsets[TOKEN_TYPES.NAME, 'def']
    def_.post = 1
    def_.end = TOKEN_TYPES.OP, ':'
    def_.children[TOKEN_TYPES.NAME].post = 0
    def_.children[TOKEN_TYPES.OP, '{'] = brace
    def_.children[TOKEN_TYPES.OP, '('] = paren
    def_.children[TOKEN_TYPES.OP, '['] = bracket

    # Make sure a from ... import ... style import has the space it needs
    from_ = token_offsets[TOKEN_TYPES.NAME, 'from']
    from_.post = 1
    from_.end = TOKEN_TYPES.NAME, 'import'
    from_.children[TOKEN_TYPES.NAME, 'import'].surround = 1

    # Make sure print statements are formatted, also when they have a >>
    print_ = token_offsets[TOKEN_TYPES.NAME, 'print']
    print_.post = 1
    print_.end = [
        (TOKEN_TYPES.OP, ','),
        (TOKEN_TYPES.NEWLINE, None), 
    ]
    print_.children[TOKEN_TYPES.OP, '>>'].surround = 0
    print_.children[TOKEN_TYPES.OP, '%'].surround = 1
    print_.children[TOKEN_TYPES.OP, ','].post = 1

    # Within dicts we don't want extra space around the :
    paren = token_offsets[TOKEN_TYPES.OP, '{']
    paren.end = TOKEN_TYPES.OP, '}'
    paren.children[':'].post = 1
    paren.children[','].post = 1
    paren.children[TOKEN_TYPES.NAME].surround = 0

    # Operators
    token_offsets['!='].surround = 1
    token_offsets['%'].surround = 1
    token_offsets['%='].surround = 1
    token_offsets['&'].surround = 1
    token_offsets['&='].surround = 1
    token_offsets['*'].surround = 1
    token_offsets['**'].surround = 1
    token_offsets['**='].surround = 1
    token_offsets['*='].surround = 1
    token_offsets['+'].surround = 1
    token_offsets['+='].surround = 1
    token_offsets['-'].surround = 1
    token_offsets['-='].surround = 1
    token_offsets['/'].surround = 1
    token_offsets['//'].surround = 1
    token_offsets['//='].surround = 1
    token_offsets['/='].surround = 1
    token_offsets['<'].surround = 1
    token_offsets['<<'].surround = 1
    token_offsets['<<='].surround = 1
    token_offsets['<='].surround = 1
    token_offsets['=='].surround = 1
    token_offsets['>'].surround = 1
    token_offsets['>='].surround = 1
    token_offsets['>>'].surround = 1
    token_offsets['>>='].surround = 1
    token_offsets['^'].surround = 1
    token_offsets['^='].surround = 1
    token_offsets[TOKEN_TYPES.NAME, 'is'].surround = 1
    token_offsets['|'].surround = 1
    token_offsets['|='].surround = 1
    token_offsets['='].surround = 1

    stream = StringIO()
    token_offset.pprint(stream)
    logger.debug('Token offsets:\n%s', stream.getvalue())

    return token_offsets

TOKEN_OFFSETS = get_token_offsets()
