def spam():
    yield 'eggs'


spam = ('egg %d' % egg for egg in range(5))


def spam(eggs=123, a={'a': 'b', 'c': 3, 4: 'd', 'e': dict(a=1, b=3)}):
    for a in range(5) + range(5):
        yield (a, )
        b = (yield)
        assert b
        return

