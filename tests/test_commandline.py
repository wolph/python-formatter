from formatter import Formatter


def test_format_path():
    formatter = Formatter()
    formatter.format_path('tests', recursive=True)
    formatter.format_path('tests/test_brace.py')


def test_main():
    from formatter.main import main
    main('formatter', '-r')

if __name__ == '__main__':
    from base_test import main
    main('-vv')
