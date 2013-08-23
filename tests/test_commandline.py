from formatter import Formatter


def test_format_path():
    formatter = Formatter()
    formatter.format_path('tests', recursive=True)
    formatter.format_path('tests/test_brace.py')


def test_main():
    from formatter.main import main
    try:
        main('formatter/main.py', 'non_existing_directory')
    except SystemExit:
        pass

    try:
        main('formatter/main.py', '-v', 'non_existing_directory')
    except SystemExit:
        pass

    try:
        main('formatter/main.py', '-vv', 'non_existing_directory')
    except SystemExit:
        pass

    try:
        main('formatter/main.py', '-vvv', 'non_existing_directory')
    except SystemExit:
        pass

if __name__ == '__main__':
    from base_test import main
    main('-vv')

