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

# internal imports
from utils import expand_tree, get_name
from core import SingleCaseDefinition, MultiCaseDefinition
from core import SuiteTestRunner, ProcessTestRunner, ThreadedTestRunner

import sys
import argparse

def interface():
    parser = argparse.ArgumentParser("Document Testing Framework")

    # options for running larger test suites.
    parser.add_argument('--casedir', '-c', action='append',
                        default=['cases/'], help='directory containing python test implementations. you may specify multiple times.')
    parser.add_argument('--testdir', '-t', action='append',
                        default=['tests/'], help='directory containing yaml test implementaitons. you may specify multiple times.')

    # options for single test running operation.
    parser.add_argument('--single', '-s', action='store_true',
                        default=False, help='specify to toggle "single" mode to only run one test.')
    parser.add_argument('--yamltest', '-y', action='store',
                        default=None, help='in "single" mode, specify the path to the YAML case spec.')
    parser.add_argument('--casedef', '-d', action='store',
                        default=None, help='in "single" mode, specify the path of the corresponding test implementation.')

    # behavioral operations. some passed to tests.
    parser.add_argument('--multi', '-m', action='store',
                        default=None, help='Run tests in a threaded or multi-rocessing environment. Specify "thread" or "process" to determine parallelism model. Disabled by default.')
    parser.add_argument('--jobs', '-j', action='store', type=int,
                        default=2, help='Number of parallel tests to run. Must run with "--multi". Default value is 2.')
    parser.add_argument('--verbose', '-v', action='store_true',
                        default=False, help='report all test activity. False by default.')
    parser.add_argument('--fatal', '-f', action='store_true',
                        default=False, help='terminate following first unsucessful test. False by default.')
    parser.add_argument('--passing', '-p', action='store_true',
                        default=False, help='return a passing document for failed tests.')

    return parser.parse_args()

def run_all(case_paths=['cases/'], test_paths=['tests/']):
    dfn = MultiCaseDefinition(case_paths)
    dfn.load()

    if user_input.multi is None:
        t = SuiteTestRunner(test_paths)
    elif user_input.multi == 'thread': 
        t = ThreadedTestRunner(test_paths, user_input.jobs)
    elif user_input.multi == 'process': 
        t = ProcessTestRunner(test_paths, user_input.jobs)

    t.load()
    t.definitions(dfn.cases)
    t.run()

def run_one(case, test):
    dfn = SingleCaseDefinition()
    dfn.load(test)

    t = SingleTestRunner()
    t.load(case)
    t.definitions(dfn.cases)
    t.run(get_name(case))

def main():
    if user_input.single is False:
        run_all(user_input.casedir, user_input.testdir)
    else:
        run_one(user_input.yamltest, user_input.casedef)

######################################################################

user_input = interface()
VERBOSE = user_input.verbose
FATAL = user_input.fatal
PASSING = user_input.passing

if __name__ == '__main__':
    main()
