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

# third-party modules
import yaml

# standard library
import sys
import os
from importlib import import_module

# internal modules
from utils import get_test_name, expand_tree

def get_module_path(path):
    r = os.getcwd() + '/' + path
    sys.path.append(r)
    return r

class TestDefinitions(object):
    def __init__(self, case_paths=[]):
        self.case_paths = case_paths
        self.tests = {}
        self.modules =  {}

    def _load_test(self, name, path):
        if name == '__init__':
            pass
        else:
            self.tests.update( { name: import_module(name, path).main } )

    def add_all(self):
        for path in self.case_paths:
            module_path = get_module_path(path)

            for f in expand_tree(path, 'py'):
                self.add(f, module_path)

    def add(self, f, path=None):
        if path is None:
            path = os.path.dirname(f)

        self.modules.update({get_test_name(f): path})

    def load_all(self):
        if not self.modules:
            self.add_all()

        for test in self.modules:
            self._load_test(test, self.modules[test])

    def load(self, filename):
        name = get_test_name(filename)

        if name in self.tests:
            pass
        elif name is False:
            raise Exception('ERROR: test named - ' + name + ' does not exist.')

        path = os.path.dirname(f)

        if path is False:
            raise Exception('ERROR: test named - ' + name + ' does not exist.')

        sys.path.append(path)
        self.add(name, path)
        self._load_test(name, path)


class TestRunner(object):
    def __init__(self, test_paths=[]):
        self.test_paths = test_paths
        self.test_specs = {}
        self.cases = None

    def definitions(self, definitions):
        self.cases = definitions

    def _load(self, spec):
        with open(spec) as f:
            self.test_specs.update( { get_test_name(spec): yaml.load(f) } )

    def _load_tree(self, path):
        for test in expand_tree(path):
            self._load(test)

    def _run(self, name, func):
        func(name, self.test_specs[name])

    def load_all(self, path=None):
        if path is None:
            for p in self.test_paths:
                self._load_tree(p)
        else:
            self._load_tree(path)

    def load(self, test):
        if test in self.test_specs:
            pass
        else:
            self._load(test)

    def run_all(self, definitions=None):
        if definitions is None and self.cases is None:
            raise Exception('Definitions not added to TestRunner Object.')
        else:
            definitions = self.cases

        for test in self.test_specs:
            case = self.test_specs[test]
            self._run(test, self.cases.get(case['type']))

    def run(self, test):
        if self.cases is None:
            raise Exception('Definitions not added to TestRunner Object.')
        else:
            if test in self.test_specs:
                case = self.test_specs[test]
                self._run(test, self.cases.get(case['type']))
            else:
                raise Exception('Test Not Defined or Loaded')
