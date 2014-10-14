import os
import logging
from formatter2 import Formatter
import difflib


def get_file_contents(path):
    with open(path) as fh:
        return path, fh.read()


def get_contents(search_path):
    for path, dirs, files in os.walk(search_path):
        for file_ in files:
            if os.path.splitext(file_)[-1] == '.py':
                full_path = os.path.join(path, file_)
                yield get_file_contents(full_path)


def check_or_revert(old_contents, full_path, new_content):
    old_content = old_contents[full_path]
    if old_content != new_content:
        logging.error('File %r in the sample set changed, reverting '
                      'change', full_path)

        diff = '\n'.join(difflib.unified_diff(
            old_content.split('\n'),
            new_content.split('\n'),
            full_path + '.original',
            full_path + '.formatted',
        ))
        logging.info('Diff:\n%s', diff)
        with open(full_path, 'w') as fh:
            fh.write(old_contents[full_path])

        raise RuntimeError(
            'Contents of sample files should not change: %r ' % full_path)


def test_format_path():
    formatter = Formatter()
    file_contents = dict(get_contents('tests/samples/'))
    formatter.format_path('tests/samples/', recursive=True)
    for k, v in get_contents('tests/samples/'):
        check_or_revert(file_contents, k, v)

    formatter.format_path('tests/samples/generators.py')


def test_main():
    from formatter2.main import main
    try:
        main('formatter2/main.py', 'non_existing_directory')
    except SystemExit:
        pass

    try:
        main('formatter2/main.py', '-v', 'non_existing_directory')
    except SystemExit:
        pass

    try:
        main('formatter2/main.py', '-vv', 'non_existing_directory')
    except SystemExit:
        pass

    try:
        main('formatter2/main.py', '-vvv', 'non_existing_directory')
    except SystemExit:
        pass

if __name__ == '__main__':
    from base_test import main
    main()

