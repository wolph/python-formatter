import sys
import logging
from cStringIO import StringIO

from .types import TOKEN_TYPES, TokenType

logger = logging.getLogger(__name__)


class TokenOffsets(dict):

    def __init__(self, parent, default_type=None):
        self.logger = logger.getChild(self.__class__.__name__)
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

    def update(self, other):
        for k, v in other.iteritems():
            if k not in self:
                self[k].update(v)

    def __setitem__(self, key, value):
        if isinstance(key, basestring):
            assert self.default_type, 'Token type must be given'
            key = self.default_type, key

        dict.__setitem__(self, key, value)


class TokenOffset(object):

    def __init__(self, parent, type_, token, pre=0, post=0, children=None,
                 end=None):
        self.logger = logger.getChild(self.__class__.__name__)
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

    def update(self, other):
        self.pre = other.pre
        self.post = other.post
        self.end = other.end
        self.children.update(other.children)

    def copy(self, type_=None, token=None):
        return TokenOffset(
            parent=self.parent,
            type_=type_ or self.type,
            token=token or self.token,
            pre=self.pre,
            post=self.post,
        )

    def _get_parent(self):
        return self._parent

    def _set_parent(self, parent):
        assert isinstance(parent, TokenOffsets), 'parent must be a ' \
            'TokenOffsets instance, was %s instead' % type(parent)
        self._parent = parent

    def _get_type(self):
        return self._type

    def _set_type(self, type_):
        assert type_ in TOKEN_TYPES, 'Expected %r to be in %r' % (
            type_,
            self,
        )
        self._type = TOKEN_TYPES[type_]

    def _get_surround(self):
        return self.pre, self.post

    def _set_surround(self, surround):
        if isinstance(surround, int):
            pre = post = surround
        else:
            pre, post = surround

        self.pre = pre
        self.post = post

    def _get_end(self):
        return self._end

    def _set_end(self, end):
        if end is not None:
            if not isinstance(end, list):
                end = [end]
            end = map(self.parent.get_key, end)
        self._end = end

    parent = property(_get_parent, _set_parent, doc='''The parent.
    :class:`~formatter.offsets.TokenOffsets`''')
    type = property(_get_type, _set_type, doc='''The type.
    :class:`~formatter.types.TokenType`''')
    surround = property(_get_surround, _set_surround, doc='''Surround the token
    with this amount of space.
    Setting will set the `pre` and `post` when given a tuple or :func:`int`.
    ''')
    end = property(_get_end, _set_end, doc='''Set the end token in case of
    children.

    Should either be a token or a tuple with
    :class:`~formatter.types.TokenType` and `token` which will be a string.''')

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

    keywords = DefaultTokenOffset().children
    keywords.default_type = TOKEN_TYPES.NAME
    keywords['with'].post = 1
    keywords['assert'].post = 1
    keywords['except'].post = 1
    keywords['import'].post = 1
    keywords['for'].post = 1
    keywords['if'].post = 1
    keywords['elif'].post = 1
    keywords['return'].post = 1
    keywords['yield'].post = 1
    keywords['raise'].post = 1
    keywords['lambda'].post = 1
    
    keywords['as'].surround = 1
    keywords['in'].surround = 1
    keywords['or'].surround = 1
    keywords['and'].surround = 1
    keywords['not'].post = 1
    token_offsets.update(keywords)

    # Operators
    operators = DefaultTokenOffset().children
    operators.default_type = TOKEN_TYPES.OP
    operators['!='].surround = 1
    operators['%'].surround = 1
    operators['%='].surround = 1
    operators['&'].surround = 1
    operators['&='].surround = 1
    operators['*'].surround = 1
    operators['**'].surround = 1
    operators['**='].surround = 1
    operators['*='].surround = 1
    operators['+'].surround = 1
    operators['+='].surround = 1
    operators['-'].surround = 1
    operators['-='].surround = 1
    operators['/'].surround = 1
    operators['//'].surround = 1
    operators['//='].surround = 1
    operators['/='].surround = 1
    operators['<'].surround = 1
    operators['<<'].surround = 1
    operators['<<='].surround = 1
    operators['<='].surround = 1
    operators['=='].surround = 1
    operators['>'].surround = 1
    operators['>='].surround = 1
    operators['>>'].surround = 1
    operators['>>='].surround = 1
    operators['^'].surround = 1
    operators['^='].surround = 1
    operators['|'].surround = 1
    operators['|='].surround = 1
    operators['='].surround = 1
    operators[TOKEN_TYPES.NAME, 'is'].surround = 1
    token_offsets.update(operators)

    token_offsets.default_type = TOKEN_TYPES.OP
    token_offsets[':'].post = 1
    token_offsets[','].post = 1
    token_offsets['='].post = 1

    # Within parameters we don't want extra space around the =
    paren = token_offsets[TOKEN_TYPES.OP, '(']
    paren.end = TOKEN_TYPES.OP, ')'
    paren.children.default_type = TOKEN_TYPES.OP
    paren.children['='].surround = 0
    paren.children['*'].surround = 0
    paren.children['**'].surround = 0
    paren.children[','].post = 1
    paren.children.default_type = TOKEN_TYPES.NAME
    paren.children[TOKEN_TYPES.NAME].surround = 0
    paren.children['or'].surround = 1
    paren.children['and'].surround = 1
    paren.children['for'].surround = 1
    paren.children['if'].surround = 1
    paren.children.update(keywords)
    paren.children.update(operators)

    # Within dicts we don't want extra space around the :
    brace = token_offsets[TOKEN_TYPES.OP, '{']
    brace.end = TOKEN_TYPES.OP, '}'
    brace.children.default_type = TOKEN_TYPES.OP
    brace.children[':'].post = 1
    brace.children[','].post = 1
    brace.children[TOKEN_TYPES.NAME].surround = 0

    # Within slices we don't want extra space around the :
    bracket = token_offsets[TOKEN_TYPES.OP, '[']
    bracket.end = TOKEN_TYPES.OP, ']'
    bracket.children.default_type = TOKEN_TYPES.OP
    bracket.children[':'].surround = 0
    bracket.children[','].post = 1
    bracket.children.default_type = TOKEN_TYPES.NAME
    bracket.children['for'].surround = 1
    bracket.children['if'].surround = 1
    bracket.children.update(keywords)

    # A little recursion to handle cases with braces in parenthesis and vice
    # versa
    brace.children.default_type = TOKEN_TYPES.OP
    paren.children.default_type = TOKEN_TYPES.OP
    bracket.children.default_type = TOKEN_TYPES.OP
    brace.children['{'] = brace
    brace.children['('] = paren
    brace.children['['] = bracket
    paren.children['{'] = brace
    paren.children['('] = paren
    paren.children['['] = bracket
    bracket.children['{'] = brace
    bracket.children['('] = paren
    bracket.children['['] = bracket

    # Classes need a space after class and no space before (
    class_ = token_offsets[TOKEN_TYPES.NAME, 'class']
    class_.post = 1
    class_.end = TOKEN_TYPES.OP, ':'
    class_.children.default_type = TOKEN_TYPES.OP
    class_.children['{'] = brace
    class_.children['('] = paren
    class_.children['['] = bracket
    class_.children[TOKEN_TYPES.NAME].post = 0

    # Def need a space after def and no space before (
    def_ = token_offsets[TOKEN_TYPES.NAME, 'def']
    def_.post = 1
    def_.end = TOKEN_TYPES.OP, ':'
    def_.children.default_type = TOKEN_TYPES.OP
    def_.children['{'] = brace
    def_.children['('] = paren
    def_.children['['] = bracket
    def_.children[TOKEN_TYPES.NAME].post = 0

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
    print_.children.default_type = TOKEN_TYPES.OP
    print_.children['>>'].surround = 0
    print_.children['%'].surround = 1
    print_.children[','].post = 1

    stream = StringIO()
    token_offset.pprint(stream)
    logger.debug('Token offsets:\n%s', stream.getvalue())

    return token_offsets

TOKEN_OFFSETS = get_token_offsets()
