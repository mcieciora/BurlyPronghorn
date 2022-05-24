from os.path import exists
from sys import argv


def main(version):
    readme_location = '../../README.md'
    for expected_files in ['changelog.txt', 'results.html']:
        location = f'../../doc/{version}/{expected_files}'
        if not exists(location):
            print(f'[ERR] {location} does not exist!')
    if exists(readme_location):
        with open(readme_location, 'r') as f:
            file_content = f.read()
            if f'mcieciora/burly_pronghorn:{version}' not in file_content:
                print(f'[ERR] README.md was not updated with latest image version!')
    else:
        print(f'[ERR] README.md does not exist!')


if __name__ == '__main__':
    main(argv[1])
