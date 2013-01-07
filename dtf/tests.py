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

from utils import get_test_name, expand_tree
from importlib import import_module
import sys
import os

class TestDefinitions(object):
    def __init__(self, case_paths):
        self.case_paths = case_paths
        self.tests = {}
        self.test_modules =  {}

    def get_test_modules(self):
        for path in self.case_paths:
            module_path = os.getcwd() + '/' + path
            sys.path.append( module_path )

            for f in expand_tree(path, 'py'):
                self.test_modules.update({get_test_name(f): module_path})

    def get_all_tests(self):
        if not self.test_modules:
            self.get_test_modules()

        for test in self.test_modules:
            if test == '__init__':
                pass
            else:
                self.tests.update( { test: import_module(test, self.test_modules[test]).main } )

    def get_test(self, name):
        if not self.test_modules:
            self.get_test_modules()

        path = self.test_modules.get(name)

        if path is None:
            raise Exception('ERROR: test named - ' + name + ' does not exist.')
        else:
            self.tests.update( { name: import_module(name, path).main } )
