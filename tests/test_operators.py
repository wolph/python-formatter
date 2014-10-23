from formatter2 import Formatter
from nose import tools


def test_assignment():
    tools.eq_(Formatter.format_string('a = 1'), 'a = 1\n\n')
    tools.eq_(Formatter.format_string('a != b'), 'a != b\n\n')
    tools.eq_(Formatter.format_string('a % b'), 'a % b\n\n')
    tools.eq_(Formatter.format_string('a %= b'), 'a %= b\n\n')
    tools.eq_(Formatter.format_string('a & b'), 'a & b\n\n')
    tools.eq_(Formatter.format_string('a &= b'), 'a &= b\n\n')
    tools.eq_(Formatter.format_string('a * b'), 'a * b\n\n')
    tools.eq_(Formatter.format_string('a ** b'), 'a ** b\n\n')
    tools.eq_(Formatter.format_string('a **= b'), 'a **= b\n\n')
    tools.eq_(Formatter.format_string('a *= b'), 'a *= b\n\n')
    tools.eq_(Formatter.format_string('a + b'), 'a + b\n\n')
    tools.eq_(Formatter.format_string('a += b'), 'a += b\n\n')
    tools.eq_(Formatter.format_string('a - b'), 'a - b\n\n')
    tools.eq_(Formatter.format_string('a -= b'), 'a -= b\n\n')
    tools.eq_(Formatter.format_string('a / b'), 'a / b\n\n')
    tools.eq_(Formatter.format_string('a // b'), 'a // b\n\n')
    tools.eq_(Formatter.format_string('a //= b'), 'a //= b\n\n')
    tools.eq_(Formatter.format_string('a /= b'), 'a /= b\n\n')
    tools.eq_(Formatter.format_string('a < b'), 'a < b\n\n')
    tools.eq_(Formatter.format_string('a << b'), 'a << b\n\n')
    tools.eq_(Formatter.format_string('a <<= b'), 'a <<= b\n\n')
    tools.eq_(Formatter.format_string('a <= b'), 'a <= b\n\n')
    tools.eq_(Formatter.format_string('a == b'), 'a == b\n\n')
    tools.eq_(Formatter.format_string('a > b'), 'a > b\n\n')
    tools.eq_(Formatter.format_string('a >= b'), 'a >= b\n\n')
    tools.eq_(Formatter.format_string('a >> b'), 'a >> b\n\n')
    tools.eq_(Formatter.format_string('a >>= b'), 'a >>= b\n\n')
    tools.eq_(Formatter.format_string('a ^ b'), 'a ^ b\n\n')
    tools.eq_(Formatter.format_string('a ^= b'), 'a ^= b\n\n')
    tools.eq_(Formatter.format_string('a is b'), 'a is b\n\n')
    tools.eq_(Formatter.format_string('a is not b'), 'a is not b\n\n')
    tools.eq_(Formatter.format_string('a | b'), 'a | b\n\n')
    tools.eq_(Formatter.format_string('a |= b'), 'a |= b\n\n')
    tools.eq_(Formatter.format_string('a = b'), 'a = b\n\n')

if __name__ == '__main__':
    for k, v in list(globals().items()):
        if k.startswith('test_') and hasattr(v, '__call__'):
            print(('Running %r' % k))
            v()

