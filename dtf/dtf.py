#!/usr/bin/python

# Copyright 2012 Sam Kleinman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
