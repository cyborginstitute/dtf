#!/usr/bin/python

# third party modules
import yaml

# internal imports
from utils import expand_tree, get_test_name, get_tests

def read_files(test_paths):
    tests = {}
    for path in test_paths:
        for test in expand_tree(path):
            with open(test) as f:
                tests.update( { get_test_name(test): yaml.load(f) } )

    return tests

def run_tests(tests, case_types):
    for test in tests:
        case = tests[test]

        if case['type'] in case_types:
            case_types[case['type']](case, test)

def main():
    case_paths = ['cases/']
    case_types = get_tests(case_paths)

    test_paths = [ 'tests/' ]
    tests = read_files(test_paths)

    run_tests(tests, case_types)

if __name__ == '__main__':
    main()
