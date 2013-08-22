import tokenize
from .offsets import TOKEN_OFFSETS
from .types import TOKEN_TYPES
import logging

logger = logging.getLogger(__name__)


class SmartList(list):

    def __init__(self, *items, **kwargs):
        self.logger = logger.getChild(self.__class__.__name__)
        size = len(items) or kwargs.get('size', 0)
        self.size = size
        assert size == 0 or size > 1
        if items:
            for item in items:
                self.append(item)
        else:
            for i in range(size):
                self.append(0)

    def copy(self):
        return SmartList(size=self.size, *self)

    def __iadd__(self, other, new=None):
        return self.__add__(other, self)

    def __add__(self, other, new=None):
        if new is None:
            new = self.copy()

        if isinstance(other, (list, tuple)):
            for i, v in enumerate(other):
                new[i] += v

        elif isinstance(other, (int, long)):
            for i, v in enumerate(self):
                new[i] += other

        else:
            raise TypeError('Unable to add type %r to %r' % (type(other),
                                                             self))

        return new

    def __isub__(self, other):
        return self.__sub__(other, self)

    def __sub__(self, other, new=None):
        if new is None:
            new = self.copy()

        if isinstance(other, (list, tuple)):
            for i, v in enumerate(self):
                new[i] -= v

        elif isinstance(other, (int, long)):
            for i, v in enumerate(self):
                new[i] -= other

        else:
            raise TypeError('Unable to subtract type %r to %r' % (type(other),
                                                                  self))
        return new

    def set(self, value):
        if isinstance(value, int):
            for i in range(len(self)):
                self[i] = value

        else:
            for i, v in enumerate(value):
                self[i] = v

    def __repr__(self):
        return '<%s%s>' % (
            self.__class__.__name__,
            list.__repr__(self),
        )

    def __str__(self):
        return '(%s)' % ','.join(map(str, self))


class Tokens(object):

    @classmethod
    def from_fh(self, fh):
        return self.from_readline(fh.readline)

    @classmethod
    def from_readline(self, readline):
        return Tokens(readline)

    def generate_tokens(self, readline):
        offsets = TOKEN_OFFSETS
        stack = []
        logger = self.logger.getChild('generate_tokens')
        for token_data in tokenize.generate_tokens(readline):
            token = Token(offsets, *token_data)
            token.preprocess()
            offset = offsets.get(token, recurse=True)
            logger.debug('offset: %r', offset)
            if stack:
                logger.debug('stack: %r', [[y.token for y in x] for x in stack])
            if offset.children:
                stack.append([offsets.get(end, recurse=True)
                              for end in offset.end])
                logger.debug('added %r to stack', token.token)
                offsets = offset.children
            elif stack and any(end == token for end in stack[-1]):
                logger.debug(
                    'removing %s from stack',
                    ', '.join(repr(x.token) for x in stack[-1]),
                )
                offsets = stack.pop()[0].parent

            yield token

    def __init__(self, readline):
        self.logger = logger.getChild(self.__class__.__name__)
        self.iterator = self.generate_tokens(readline)

    def __iter__(self):
        for item in self.iterator:
            yield item

    def to_str(self):
        '''Convert the tokens back to a string'''
        data = tokenize.untokenize(self.iterator)
        # Strip all trailing newlines at the end but make sure we end with a
        # newline
        data = data.rstrip() + '\n'
        # Strip the trailing whitespace for all lines
        lines = data.split('\n')
        lines = [l.rstrip() for l in lines]

        return '\n'.join(lines)

    def strip(self):
        '''Strip all whitespace so we can begin formatting'''
        self.iterator = self._strip(self.iterator)
        return self

    def _strip(self, iterator):
        current = iterator.next()
        for next in iterator:
            if current.end_row == next.begin_row:
                next.col -= next.begin_col - current.end_col

            yield current
            current = next

        yield current

    def format(self):
        '''
        Format the string, expects the extra whitespace to be removed already
        '''
        self.iterator = self._format(self.iterator)
        return self

    def _format(self, iterator):
        previous_offset = 0
        previous_line = None
        for token in iterator:
            if previous_line == token.begin_row:
                token.col += previous_offset
            else:
                previous_offset = 0
                previous_line = token.begin_row

            token.col += token.offset.pre
            previous_offset += token.offset.pre + token.offset.post
            yield token

    def __call__(self):
        return self.strip().format().to_str()


class Token(object):

    def __init__(self, offsets, tok_type, token, begin, end, line):
        assert tok_type != TOKEN_TYPES.ERRORTOKEN, ('Cannot format erroneous '
            'code')
        self.offset = offsets[tok_type, token]
        self.tok_type = tok_type
        self.token = token
        self._row = SmartList(size=2)
        self._col = SmartList(size=2)
        self.begin = begin
        self.end = end
        self.line = line

    def get_line(self):
        return self._line

    def set_line(self, line):
        if hasattr(self, '_line'):
            self.end_col += len(line) - len(self._line)
        self._line = line

    line = property(get_line, set_line)

    def preprocess(self):
        self.type.preprocess(self)

    @property
    def type(self):
        return TOKEN_TYPES[self.tok_type]

    def get_begin_row(self):
        return self._row[0]

    def set_begin_row(self, line):
        self._row[0] = line

    def get_end_row(self):
        return self._row[1]

    def set_end_row(self, line):
        self._row[1] = line

    def get_begin_col(self):
        return self._col[0]

    def set_begin_col(self, col):
        self._col[0] = col

    def get_end_col(self):
        return self._col[1]

    def set_end_col(self, col):
        self._col[1] = col

    def get_col(self):
        return self._col

    def set_col(self, col):
        self._col.set(col)

    def get_row(self):
        return self._row

    def set_row(self, row):
        self._row.set(row)

    def get_begin(self):
        return SmartList(self.begin_row, self.begin_col)

    def set_begin(self, begin):
        self.begin_row, self.begin_col = begin

    def get_end(self):
        return SmartList(self.end_row, self.end_col)

    def set_end(self, end):
        self.end_row, self.end_col = end

    col = property(get_col, set_col)
    row = property(get_row, set_row)
    begin = property(get_begin, set_begin)
    end = property(get_end, set_end)
    end_col = property(get_end_col, set_end_col)
    end_row = property(get_end_row, set_end_row)
    begin_col = property(get_begin_col, set_begin_col)
    begin_row = property(get_begin_row, set_begin_row)

    def __len__(self):
        # Got to love magic numbers :)
        # We're trying to emulate a token that is valid for the tokenize lib
        # so we need some magic
        return 5

    def __iter__(self):
        # Return something the tokenize library accepts
        yield self.tok_type
        yield self.token
        yield self.begin
        yield self.end
        yield self.line

    def __eq__(self, other):
        if isinstance(other, Token):
            return any(end == other.begin for end in self.end)
        elif isinstance(other, int):
            return self.tok_type == other
        elif hasattr(other, 'token') and hasattr(other, 'type'):
            return self.token == other.token and self.type == other.type
        elif not other:
            return False
        elif isinstance(other, tuple) and len(other) == 2:
            return self.tok_type, self.token == other
        else:
            raise TypeError('Dont know how to compare %r to %r' % (
                self, other))

    def __cmp__(self, other):
        if other:
            return cmp(self.end, other.begin)
        else:
            return 0

    def __sub__(self, other):
        assert self.end_row == other.begin_row
        return other.begin_col - self.end_col

    def __str__(self):
        return repr((self.token, self.type.name, self.begin, self.end))

    def __repr__(self):
        line = self.line
        if line.rstrip() != line:
            line = line.rstrip() + r'#'
        if line.lstrip() != line:
            line = r'#' + line.lstrip()

        if self.offset:
            pre = self.offset.pre
            post = self.offset.post
        else:
            pre = post = '?'

        return '<%s[%s]: %r (%d,%d)-(%d,%d):(%s,%s) %s>' % (
            self.__class__.__name__,
            self.type,
            self.token,
            self.begin[0],
            self.begin[1],
            self.end[0],
            self.end[1],
            pre,
            post,
            line,
        )
