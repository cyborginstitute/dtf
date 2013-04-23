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

"""
:mod:`core` contains the primary interfaces for loading test
specifications and case definitions. The operations and interface used
in :mod:`dtf` build upon this infrastructure. If you want to implement
a different base behavior test selection and running, use these
classes as a starting point.
"""

# third-party modules
import yaml

# standard library
import sys
import os
from importlib import import_module

# internal modules
try: 
    from utils import get_name, expand_tree, get_module_path
    from err import DtfDiscoveryException
except:
    from dtf.utils import get_name, expand_tree, get_module_path
    from dtf.err import DtfDiscoveryException
    
class CaseDefinition(object):
    """
    :param list case_paths: A list of paths that hold case
                            definitions. May be empty upon object
                            creation.

    :class:`CaseDefinition` is a base class for loading and importing
    cases into the :mod:`dtf` process. Sub-classes must implement
    ``load()`` and ``add()`` methods, depending on the desired
    behavior.
    """

    def __init__(self, case_paths=[]):
        self.case_paths = case_paths
        "The list of paths that contain cases."
        self.cases = {}
        "A dictionary of loaded cases."
        self.modules =  {}


    def _load_case(self, name, path):
        """
        :param name: The name of the case definition, as you would use
                     to import the module in a Python ``import``
                     statement.

        :param path: The filesystem path of the Python module.


        Internal function to be called by ``import()`` which loads
        case donations into the current :mod:`dtf` instance. Will not
        not load a case named ``__init__``.
        """

        if name == '__init__':
            pass
        else:
            self.cases.update( { name: import_module(name, path).main } )

    def _add(self, f, path=None):
        """
        :param f: A file name that contains the path name to
                  :meth:`_add()` provides no validation of this
                  module.

        :param path: Defaults to ``None``. If specified, this becomes
                     the path that :mod:`dtf` uses as the base path to
                     import the module.

        An internal method used to add a single case definition to a
        :class:`~core.CaseDefinition` object's
        :attr:`~core.CaseDefinition.modules` attribute. Typically
        :class:`~core.CaseDefinition` sub-classes'
        :meth:`~core.CaseDefinition.add()` methods will wrap
        :meth:`~core.CaseDefinition._add()`.
        """

        if path is None:
            path = os.path.dirname(f)

        self.modules.update({get_name(f): path})

    def load(self):
        "Not implemented in the base class. Raises a :exc:`NotImplemented` exception"
        raise NotImplemented('CaseDefinition is a base class. Instantiate one of its sub-classes or implement a load().')

    def add(self):
        "Not implemented in the base class. Raises a :exc:`NotImplemented` exception"
        raise NotImplemented('CaseDefinition is a base class. Instantiate one of its sub-classes or implement a self().')

class SingleCaseDefinition(CaseDefinition):
    """
    Provides an interface to add and load a single case
    definition. used by :mod:`dtf` for invocations that run a single
    test. May also be more efficent when running a suite of tests that
    depend on a single case module (this operational mode is not
    currently implemented.)

    You do not need to instantiate :class:`SingleCaseDefinition` with
    the :attr:`~core.CaseDefinition.case_paths`` argument as in
    :class:`CaseDefinition`, as it has no impact given the current
    implementation.
    """

    def add(self, f, path=None):
        """
        A passthrough wrapper of :meth:`~core.CaseDefinition._add()`.
        """
        self._add(f, path)

    def load(self, filename):
        """
        :param filename: The full path to the case definition module
                         definition.

        Given the full path of the case module, ``filename``,
        :meth:`~core.SingleCaseDefinition.load()` will load the case
        definition into the current :mod:`dtf` instance.

        Will produce a :exc:`err.DtfDiscoveryException` if:

        1. You have not added this case using
           :meth:`~core.SingleCaseDefinition.add()`, or

        2. The path of the ``filename`` does not exist.

        The fundamental operation uses :meth:`~core.CaseDefinition._load_case()`
        """

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
    """
    Provides an interface to add a group of case definition modules to
    the current :mod:`dtf` process. Use in conjunction with
    :attr:`~core.CaseDefinition.case_paths` to load a directory of
    case modules.
    """

    def add(self):
        """
        Adds all modules, recursively, in
        :attr:`~core.CaseDefinition.case_paths` and calls
        :meth:`~core.CaseDefinition._add()` for each module. No
        arguments required when
        :attr:`~core.CaseDefinition.case_paths` is set.
        """

        for path in self.case_paths:
            module_path = get_module_path(path)

            for f in expand_tree(path, 'py'):
                self._add(f, module_path)

    def load(self):
        """
        If :attr:`~core.CaseDefinition.modules` is empty, calls
        :meth:`~core.MultiCaseDefinition.add()` before iterating
        through :attr:`~core.CaseDefinition.modules` and loading all
        relevant modules.
        """

        if not self.modules:
            self.add()

        for case in self.modules:
            self._load_case(case, self.modules[case])

class TestRunner(object):
    """
    :param list test_paths: A list of paths that contain test
                            definitions. Empty by default.

    :class:`~core.TestRunner` is a base class used as the basis for
    implementing interfaces for running :mod:`dtf` cases. Makes it
    possible for sub-classes to implement different operational modes
    with a common interface. :class:`~core.TestRunner` sub-classes
    implement running a single test, or running multiple tests at once with
    different parallelism options.
    """

    def __init__(self, test_paths=[]):
        self.test_paths = test_paths
        """A list of paths that contain tests.  Passed as an argument
        when instantiating :class:`~core.TestRunner`."""

        self.test_specs = {}
        """A dictionary of test specifications in the form of ``{
        <test_name>: <test_definitions> }``"""

        self.case_definition = None
        """A :class:`~core.CaseDefinition()` object."""

        self.queue = []
        """A list of the :attr:`~core.TestRunner.test_specs` used to
        support parallel test running."""

    def definitions(self, definitions):
        """
        :param definitions: A :class:`~core.CaseDefinition()` object.

        Use :meth:`~core.TestRunner.definitions()` to add
        :class:`~core.CaseDefinition()` after run-time. Provides fo a
        more gentle interface around the following operation in
        addition to the possibility for additional validation in the
        future:

        .. code-block:: python

           t = TestRunner()
           t.case_definitions = CaseDefinition(['cases/'])
        """
        self.case_definition = definitions

    def _load(self, spec):
        """
        :param spec: The filename of a test spec.

        An internal function to load a test function into the
        :attr:`~core.TestRunner.test_specs` and
        :attr:`:attr:`~core.TestRunner.queue` attributes of the
        :class:`~core.TestRunner` object.
        """

        with open(spec) as f:
            test = get_name(spec)
            specs = yaml.load_all(f)

            for spec in specs:
                self.test_specs.update( { test: spec } )
                self._add_to_queue(test, spec['type'])

    def _load_tree(self, path):
        """
        :param path: A file system path containing tests.

        An internal method that recursively loads all ``.yaml`` files,
        selected using :meth:`~utils.expand_tree()`, in ``path`` using
        :meth:`~core.TestRunner._load()`.
        """

        for test in expand_tree(path):
            self._load(test)

    def _run(self, name, func):
        """
        :param string name:

           Specifies the name of the test, by the same name used in
           :attr:`~core.TestRunner.test_specs`.

        :param callable func:

           A callable that takes two arguments:

           - name of the test.
           - the test spec.

        Runs the test, passing the ``callable`` the ``name`` value,
        and the value of ``name`` in the dict
        :attr:`~core.TestRunner.test_specs`, which is itself a dict
        representation of the test spec.
        """
        func(name, self.test_specs[name])

    def _add_to_queue(self, name, func):
        """
        :param string name: The identifier of a the test.

        :param callable func: A callable that ipmplements the test.

        Appends a three-tuple to the :attr:`~core.TestRunner.queue`
        list, that :mod:`dtf`.
        """
        self.queue.append((func, name, self.test_specs[name]))

    def load(self):
        """
        :raises: :exc:`NotImplementedError`.

        *Not Implemented in the base class.* All sub-classes must
        implement :meth:`~core.TestRunner.load()`.
        """
        raise NotImplementedError('TestRunner is a base class. Instantiate one of its sub-classes or implement a load().')

    def run(self):
        """
        :raises: :exc:`NotImplementedError`.

        *Not Implemented in the base class.* All sub-classes must
        implement :meth:`~core.TestRunner.run()`.
        """
        raise NotImplementedError('TestRunner is a base class. Instantiate one of its sub-classes or implement a run().')

class SingleTestRunner(TestRunner):
    """
    :class:`~core.SingleTestRunner` is a sub-class of :class:`~core.TestRunner`
    implements :meth:`~core.SingleTestRunner.load()` and
    :meth:`~core.SingleTestRunner.run()` to run a single test at a
    time. :option:`dtf --single` uses this interface.

    From a script, use :class:`~core.SingleTestRunner` to run a single test as
    follows:

    .. code-block:: python

       dfn = SingleCaseDefinition()
       dfn.load(<test>)

       t = SingleTestRunner()
       t.load(<case>)
       t.definitions(dfn.cases)
       t.run(<test-name>)
    """
    def load(self, test):
        """
        :param string test: The name of the test to load into :mod:`dtf`.

        You must call :meth:`~core.SingleTestRunner.load()` after
        calling :meth:`~core.TestRunner.definitions()`.
        """

        if test in self.test_specs:
            pass
        else:
            self._load(test)

    def run(self, test):
        """
        :param string test: The name of the test to run.

        Runs the single named test. If :attr:`~core.TestRunner.case_definition`
        is ``None`` or if :attr:`~core.TestRunner.test_specs` does not contain
        the specified test, :meth:`~core.SingleTestRunner.run()` raises
        :exc:`~err.DtfDiscoveryException`.

        To prevent make sure to call :meth:`~core.TestRunner.definitions()` and
        :meth:`~core.SingleTestRunner.load()`.
        """

        if self.case_definition is None:
            raise DtfDiscoveryException('Definitions not added to TestRunner Object.')
        else:
            if test in self.test_specs:
                case = self.test_specs[test]
                self._run(test, self.case_definition.get(case['type']))
            else:
                raise DtfDiscoveryException('Test Not Defined or Loaded')

class MultiTestRunner(TestRunner):
    """
    :class:`~core.MultiTestRunner` is a sub-class of :class:`~core.TestRunner`,
    intended as a base class for test runner implementations that run more than
    one test at a time.
    """
    def load(self, path=None):
        """
        :param string path: A relative or absolute path that contains test
                            specifications.

        This :meth:`~core.MultiTestRunner.load()` loads, (by way of
        :meth:`~core.TestRunner._load_tree()`, all ``.yaml`` test files within
        the specified ``path``.
        """
        if path is None:
            for p in self.test_paths:
                self._load_tree(p)
        else:
            self._load_tree(path)

class SuiteTestRunner(MultiTestRunner):
    """
    :class:`~core.SuiteTestRunner()` is a sub-class of
    :class:`~core.MultiTestRunner()` that runs all test represented in the
    :attr:`~core.TestRunner.test_specs` dict.
    """

    def run(self, definitions=None):
        """
        :param dict definitions: Optional. A dictionary in the format of
                                 :attr:`~core.TestRunner.case_definition`, and
                                 if specified will override
                                 :attr:`~core.TestRunner.case_definition` if
                                 specified.
                                 
        Raises :exc:`~err.DtfDiscoveryException` when ``definitions`` is not
        defined and :attr:`~core.TestRunner.case_definition` is empty.

        Runs all tests in :attr:`~core.TestRunner.test_specs` sequentially.
        """
        if definitions is None and not self.case_definition:
            raise DtfDiscoveryException('Definitions not added to TestRunner Object.')
        elif definitions is None:
            definitions = self.case_definition

        for test in self.test_specs:
            self._run(test, self.case_definition.get(self.test_specs[test]['type']))
