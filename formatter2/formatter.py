import os
import sys
import logging
from cStringIO import StringIO

from .tokens import Tokens


logger = logging.getLogger(__name__)


class Formatter(object):

    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)

    def __call__(self, input_file, seek=True):
        if seek and hasattr(input_file, 'seek'):
            input_file.seek(0)

        if hasattr(input_file, 'readline'):
            tokens = Tokens.from_fh(input_file)
        elif input_file == '-':
            tokens = Tokens.from_readline(sys.stdin.readline)
        else:
            with open(input_file) as fh:
                file_ = StringIO()
                print >>file_, fh.read()
                file_.seek(0)
                tokens = Tokens.from_readline(file_.readline)

        formatted = tokens()
        # Test if we didn't break anything
        try:
            compile(formatted, '', 'exec')
        except SyntaxError:
            logging.debug('Formatted code:\n%s', formatted)
            logging.error('Unable to format %r', input_file)
            raise

        return formatted

    def format_path(self, path, recursive=False):
        if os.path.isfile(path) or path == '-':
            self.format_file(path)
        elif recursive:
            self.format_directory(path)

    def format_directory(self, directory):
        for path, dirs, files in os.walk(directory):
            for file_ in files:
                fullpath = os.path.join(path, file_)
                if os.path.splitext(fullpath)[-1] == '.py':
                    self.format_file(fullpath)

    def format_file(self, name):
        code = self(name)
        if name == '-':
            sys.stdout.write(code)
        else:
            with open(name, 'w') as fh:
                fh.write(code)

            # Ugly but effective
            old_argv = sys.argv[:]
            sys.argv = ['pep8', '--ignore', 'W391', name]
            import pep8
            pep8style = pep8.StyleGuide(parse_argv=True, config_file=False)
            pep8style.check_files()
            sys.argv = old_argv

    @classmethod
    def format_string(cls, string):
        formatter = Formatter()
        fh = StringIO()
        print >>fh, string
        return formatter(fh)
