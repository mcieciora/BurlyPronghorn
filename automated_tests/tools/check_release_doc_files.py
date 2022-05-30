from os.path import exists
from sys import argv


def main(version):
    readme_location = '../../README.md'
    for expected_files in ['changelog.txt', 'results.html']:
        location = f'../../doc/{version}/{expected_files}'
        if not exists(location):
            print(f'[ERR] {location} does not exist!')
    if not exists(readme_location):
        print(f'[ERR] README.md does not exist!')


if __name__ == '__main__':
    main(argv[1])
