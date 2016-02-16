from formatter2 import Formatter


def test_assignment():
    assert Formatter.format_string('a = 1') == 'a = 1\n\n'
    assert Formatter.format_string('a != b') == 'a != b\n\n'
    assert Formatter.format_string('a % b') == 'a % b\n\n'
    assert Formatter.format_string('a %= b') == 'a %= b\n\n'
    assert Formatter.format_string('a & b') == 'a & b\n\n'
    assert Formatter.format_string('a &= b') == 'a &= b\n\n'
    assert Formatter.format_string('a * b') == 'a * b\n\n'
    assert Formatter.format_string('a ** b') == 'a ** b\n\n'
    assert Formatter.format_string('a **= b') == 'a **= b\n\n'
    assert Formatter.format_string('a *= b') == 'a *= b\n\n'
    assert Formatter.format_string('a + b') == 'a + b\n\n'
    assert Formatter.format_string('a += b') == 'a += b\n\n'
    assert Formatter.format_string('a - b') == 'a - b\n\n'
    assert Formatter.format_string('a -= b') == 'a -= b\n\n'
    assert Formatter.format_string('a / b') == 'a / b\n\n'
    assert Formatter.format_string('a // b') == 'a // b\n\n'
    assert Formatter.format_string('a //= b') == 'a //= b\n\n'
    assert Formatter.format_string('a /= b') == 'a /= b\n\n'
    assert Formatter.format_string('a < b') == 'a < b\n\n'
    assert Formatter.format_string('a << b') == 'a << b\n\n'
    assert Formatter.format_string('a <<= b') == 'a <<= b\n\n'
    assert Formatter.format_string('a <= b') == 'a <= b\n\n'
    assert Formatter.format_string('a == b') == 'a == b\n\n'
    assert Formatter.format_string('a > b') == 'a > b\n\n'
    assert Formatter.format_string('a >= b') == 'a >= b\n\n'
    assert Formatter.format_string('a >> b') == 'a >> b\n\n'
    assert Formatter.format_string('a >>= b') == 'a >>= b\n\n'
    assert Formatter.format_string('a ^ b') == 'a ^ b\n\n'
    assert Formatter.format_string('a ^= b') == 'a ^= b\n\n'
    assert Formatter.format_string('a is b') == 'a is b\n\n'
    assert Formatter.format_string('a is not b') == 'a is not b\n\n'
    assert Formatter.format_string('a | b') == 'a | b\n\n'
    assert Formatter.format_string('a |= b') == 'a |= b\n\n'
    assert Formatter.format_string('a = b') == 'a = b\n\n'

if __name__ == '__main__':
    for k, v in list(globals().items()):
        if k.startswith('test_') and hasattr(v, '__call__'):
            print(('Running %r' % k))
            v()

