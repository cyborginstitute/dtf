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
from utils import get_name, expand_tree
from err import DtfDiscoveryException

def get_module_path(path):
    r = os.getcwd() + '/' + path
    sys.path.append(r)
    return r

class CaseDefinition(object):
    def __init__(self, case_paths=[]):
        self.case_paths = case_paths
        self.cases = {}
        self.modules =  {}

    def _load_case(self, name, path):
        name = get_name(name)

        if name == '__init__':
            pass
        else:
            self.cases.update( { name: import_module(name, path).main } )

    def _add(self, f, path=None):
        if path is None:
            path = os.path.dirname(f)

        self.modules.update({get_case_name(f): path})

    def load(self):
        raise NotImplemented('CaseDefinition is a base class. Instantiate one of its sub-classes or implement a load().')

    def add(self):
        raise NotImplemented('CaseDefinition is a base class. Instantiate one of its sub-classes or implement a load().')

class SingleCaseDefinition(CaseDefinition):
    def add(self, f, path=None):
        self._add(f, path)

    def load(self, filename):
        name = get_case_name(filename)

        if name in self.cases:
            pass
        elif name is False:
            raise DtfDiscoveryException('case named - ' + name + ' does not exist.')

        path = os.path.dirname(filename)

        if path is False:
            raise DtfDiscoveryException('case named - ' + name + ' does not exist.')

        sys.path.append(path)
        self.add(name, path)
        self._load_case(name, path)

class MultiCaseDefinition(CaseDefinition):
    def add(self):
        for path in self.case_paths:
            module_path = get_module_path(path)

            for f in expand_tree(path, 'py'):
                self._load_case(f, module_path)

    def load(self):
        if not self.modules:
            self.add()

        for case in self.modules:
            self._load_case(case, self.modules[case])

class TestRunner(object):
    def __init__(self, test_paths=[]):
        self.test_paths = test_paths
        self.test_specs = {}
        self.cases = None
        self.queue = []

    def definitions(self, definitions):
        self.cases = definitions

    def _load(self, spec):
        with open(spec) as f:
            test = get_name(spec)
            case = yaml.load(f)

            self.test_specs.update( { test: case } )
            self._add_to_queue(test, case['type'])

    def _load_tree(self, path):
        for test in expand_tree(path):
            self._load(test)

    def _run(self, name, func):
        func(name, self.test_specs[name])

    def _add_to_queue(self, name, func):
        self.queue.append((func, name, self.test_specs[name]))

    def load(self):
        raise NotImplemented('TestRunner is a base class. Instantiate one of its sub-classes or implement a load().')

    def run(self, test):
        if self.cases is None:
            raise DtfDiscoveryException('Definitions not added to TestRunner Object.')
        else:
            if test in self.test_specs:
                case = self.test_specs[test]
                self._run(test, self.cases.get(case['type']))
            else:
                raise DtfDiscoveryException('Test Not Defined or Loaded')

class SingleTestRunner(TestRunner):
    def load(self, test):
        if test in self.test_specs:
            pass
        else:
            self._load(test)

class MultiTestRunner(TestRunner):
    def load(self, path=None):
        if path is None:
            for p in self.test_paths:
                self._load_tree(p)
        else:
            self._load_tree(path)

class SuiteTestRunner(MultiTestRunner):
    def run(self, definitions=None):
        if definitions is None and self.cases is None:
            raise DtfDiscoveryException('Definitions not added to TestRunner Object.')
        elif definitions is None:
            definitions = self.cases

        for test in self.test_specs:
            self._run(test, self.cases.get(self.test_specs[test]['type']))

class ThreadedTestRunner(MultiTestRunner):
    def __init__(self, test_paths=[], pool_size=2):
        super(ThreadedTestRunner, self).__init__(test_paths)
        self.pool_size = pool_size

    def run(self):
        try:
            import threadpool
        except ImportError:
            print('[dtf]: "threadpool" module not installed, falling back to serial mode.')
            return None

        pool = threadpool.ThreadPool(self.pool_size)

        for j in self.queue:
            pool.putRequest(threadpool.WorkRequest(self.cases.get(j[0]), (j[1], j[2])))

        import time
        time.sleep(0.01)
        pool.wait()

class ProcessTestRunner(MultiTestRunner):
    def __init__(self, test_paths=[], pool_size=2):
        super(ProcessTestRunner, self).__init__(test_paths)
        self.pool_size = pool_size

    def run(self):
        from multiprocessing import Pool

        p = Pool(processes=self.pool_size)

        for j in self.queue:
            p.apply_async(self.cases.get(j[0]), (j[1], j[2]))

        p.close()
        p.join()
