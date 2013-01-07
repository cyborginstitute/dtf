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
from utils import expand_tree, get_test_name
from tests import TestDefinitions

class TestRunner(object):
    def __init__(self, test_paths):
        self.test_paths = test_paths
        self.test_specs = {}

    def load_all_tests(self):
        for path in self.test_paths:
            for test in expand_tree(path):
                with open(test) as f:
                    self.test_specs.update( { get_test_name(test): yaml.load(f) } )

    def load_test(self, test):
        if test in self.test_specs:
            pass
        else:
            with open(test) as f:
                self.test_specs.update( { get_test_name(test): yaml.load(f) } )

    def run_all(self, definitions):
        for test in self.test_specs:
            case = self.test_specs[test]

            self.run(test, case, definitions.get(case['type']))

    @staticmethod
    def run(test, case, func=None):
        if func is None:
            tdfns = TestDefinitions(['./'])
            tdfns.get_all_tests()

            test_type = case['type']
            if test_type in tdfns.tests:
                func = tdfns.tests.get(test_type)
                func(case, test)
            else:
                Exception('ERROR: case named "%s" with non-extant type "%s"' % (test, test_type))
        else:
            func(case, test)

def main():
    case_paths = ['cases/']

    testdefs = TestDefinitions(case_paths)
    testdefs.get_all_tests()

    test_paths = [ 'tests/' ]

    t = TestRunner( test_paths )
    t.load_all_tests()
    t.run_all(testdefs.tests)

if __name__ == '__main__':
    main()
