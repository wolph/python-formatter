try:
    from cStringIO import StringIO
except ImportError:  # pragma: no cover
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

