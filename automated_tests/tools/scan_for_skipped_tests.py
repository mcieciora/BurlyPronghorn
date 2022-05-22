from glob import glob


def main():
    for file in glob('../*_tests/test_*.py'):
        with open(file, 'r') as f:
            file_content = f.read()
            pattern = '@mark.skip'
            if pattern in file_content:
                print(f'[ERR] {file_content.count(pattern)} skip mark(s) found in: {file}')


if __name__ == '__main__':
    main()
