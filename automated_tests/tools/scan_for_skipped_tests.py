from glob import glob


def main():
    files_with_skip = []
    for file in glob('../*_tests/test_*.py'):
        with open(file, 'r') as f:
            if '@mark.skip' in f.read():
                files_with_skip.append(file)
    return 'OK' if files_with_skip else f'[WARNING] Skip mark found in: {files_with_skip}'


if __name__ == '__main__':
    print(main())
