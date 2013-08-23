import tokenize_fork as tokenize
import logging

logger = logging.getLogger(__name__)


class TokenTypes(dict):

    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.by_name = {}
        for tok_id, tok_name in tokenize.tok_name.iteritems():
            self.register(TokenType(tok_id, tok_name))

        self.register(DefaultTokenType())

    def register(self, token_type):
        if isinstance(token_type, TokenType):
            replacing = False
        else:
            token_class = token_type
            token_type = self[token_class.name]
            token_type = token_class(token_type.id, token_type.name)
            replacing = True

        for key in token_type.get_keys():
            assert replacing or key not in self
            self[key] = token_type

    def __repr__(self):
        is_int = lambda v: isinstance(v, int)
        return repr(dict((k, v) for k, v in self.iteritems() if is_int(k)))

    def __getattr__(self, key):
        if key in self:
            return self[key]


class TokenType(object):

    def __init__(self, id_, name):
        self.logger = logger.getChild(self.__class__.__name__)
        self.id, self.name = id_, name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s[%d] %s>' % (
            self.__class__.__name__,
            hash(self),
            self,
        )

    def __hash__(self):
        return self.id

    def get_keys(self):
        yield self.id
        yield self.name
        yield self

    def preprocess(self, token):
        '''Preprocess the token, this can do pretty much anything including
        changing the column'''
        return token


class StringTokenType(TokenType):
    name = 'STRING'

    def preprocess(self, token):
        '''Preprocess the token

        This automatically replaces strings with " to ' if possible
        '''
        string = token.token
        # Replace """ with ' or '''
        if string.startswith('"""') and string.endswith('"""'):
            new_string = string[3:-3]
            if "'" not in new_string:
                token.token = "'%s'" % new_string
            elif ("'" in new_string and "'''" not in new_string and
                    token.begin_row == token.end_row):
                token.token = "'''%s'''" % new_string
        # Replace " with ' or '''
        elif string.startswith('"') and string.endswith('"'):
            new_string = string[1:-1]
            if "'" not in new_string:
                token.token = "'%s'" % new_string
            elif "'" in new_string and "'''" not in new_string:
                token.token = "'''%s'''" % new_string
        # Replace ''' with '
        elif (string.startswith("'''") and string.endswith("'''")
                and token.begin_row == token.end_row):
            new_string = string[3:-3]
            if "'" not in new_string:
                token.token = "'%s'" % new_string

        return token


class DefaultTokenType(TokenType):

    def __init__(self):
        TokenType.__init__(self, -1, 'DEFAULT')


def get_token_types():
    token_types = TokenTypes()
    token_types.register(StringTokenType)
    return token_types

TOKEN_TYPES = get_token_types()
