import sys
import argparse
import logging
from .formatter import Formatter


def main(*argv):
    parser = argparse.ArgumentParser('Format Python files')
    parser.add_argument('files', nargs='+')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Process directories recursively')
    parser.add_argument('-v', '--verbosity', action='count',
                        help='Increase verbosity', default=0)
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enter the debugger on exception')

    argv = argv or sys.argv
    args = parser.parse_args(argv[1:])

    if args.verbosity > 1:
        level = logging.DEBUG
    elif args.verbosity:
        level = logging.INFO
    else:
        level = logging.WARN

    handler = logging.StreamHandler()
    logger = logging.getLogger('')
    logger.setLevel(level)
    logger.addHandler(handler)

    try:
        formatter = Formatter()
        for file_ in args.files:
            formatter.format_path(file_, args.recursive)
    except Exception:
        if args.debug:
            type_, value, tb = sys.exc_info()
            import pdb
            pdb.post_mortem(tb)

        else:
            raise

    logger.removeHandler(handler)

