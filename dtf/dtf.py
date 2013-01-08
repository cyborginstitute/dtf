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
from utils import expand_tree, get_test_name
from core import TestDefinitions, TestRunner

def main():
    case_paths = ['cases/']

    dfn = TestDefinitions(case_paths)
    dfn.load_all()

    test_paths = [ 'tests/' ]

    t = TestRunner( test_paths )
    t.load_all()
    t.definitions(dfn.tests)
    t.run_all()

if __name__ == '__main__':
    main()
