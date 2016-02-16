from formatter2 import Formatter


def test_comments():
    formatter = Formatter()
    formatter.format_path('tests/samples/comments.py')


if __name__ == '__main__':
    from .base_test import main
    main('-vv')


