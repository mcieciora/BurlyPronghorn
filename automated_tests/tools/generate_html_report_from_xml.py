from jinja2 import Environment, FileSystemLoader
import xml.etree.ElementTree as ET
from glob import glob
from datetime import datetime


def generate_html(date, number_of_tests, tests):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('html_report_template.html')

    with open('results.html', 'w') as f:
        f.write(template.render(
            date=date,
            number_of_tests=number_of_tests,
            tests=tests
        ))


def get_xml_data(filename):
    xml_root = ET.parse(filename).getroot()
    all_tests = []
    tests_number = int(xml_root[0].attrib['tests'])
    for attribute in ['errors', 'failures', 'skipped']:
        if int(xml_root[0].attrib[attribute]) != 0:
            raise ValueError
    for testcase in xml_root.iter('testcase'):
        all_tests.append(testcase.attrib['name'])
    return tests_number, all_tests


def main():
    all_tests_number = 0
    all_tests_list = []
    for file in glob('../*.xml'):
        try:
            number, table = get_xml_data(file)
            all_tests_number += number
            all_tests_list = all_tests_list + table
        except ValueError:
            print(f'[ERR] There are failed testcases in {file}')

    current_date = datetime.now().strftime("%d-%m-%Y")
    generate_html(current_date, all_tests_number, all_tests_list)

    if len(all_tests_list) != all_tests_number:
        print('[ERR] Amount of all tests is not equal to sum of the numbers defined in xml files')


if __name__ == '__main__':
    main()
