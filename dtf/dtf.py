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

"""
:mod:`dtf` provides the main user interface for `dtf`, coordinating
input from users with the actual behavior of ``dtf`` as implemented in
:mod:`core`.

See :doc:`/man/dtf` for complete documentation of the command-line
interface of ``dtf``.
"""

# internal imports
from utils import expand_tree, get_name
from core import SingleCaseDefinition, MultiCaseDefinition
from core import SingleTestRunner, SuiteTestRunner, ProcessTestRunner, ThreadedTestRunner

import argparse
import sys

def interface():
    """
    :returns: Parsed :class:`~python:argparse.ArgumentParser` object
              that contains user input.

    See :doc:`/man/dtf` for full documentation of all user options.
    """

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

def run_many(case_paths=['cases/'], test_paths=['tests/'], multi=None, jobs=2):
    """
    :param list case_paths:

        A list of paths that contain :term:`cases <case>`, or Python
        definitions of a consistency test. By default, :mod:`dtf` uses
        the :file:`cases/` in the current directory as the path for
        cases.

    :param list test_paths:

        A list of path that contain :term:`test` definitions, or
        :term:`YAML` specifications of conditions to verify.

    :param string multi:

        ``multi`` contrails the parallelism model for :mod:`dtf`. The
        default mode is ``None``, which runs all tests
        sequentially. You may also specify ``thread`` to run tests in
        parallel using a thread pool, or ``process`` to run tests in
        parallel using a pool of separate processes.

    :param int jobs:

        When running in ``thread`` or ``process`` ``multi`` mode, the
        value of the ``jobs`` value controls the size of the thread or
        process worker pool. The default value is ``2``.

    You must specify values to the ``case_paths`` value that contain
    the cases to support the test in the ``test_paths``.  You may
    achieve additional control over test operation by breaking tests,
    into folders and running those tests separately.

    :meth:`run_many()` performs all testing for ``dtf`` when running
    a suite of tests. By default :meth:`run_many()` runs test
    sequentially; however, you can optionally run tests using a simple
    parallel model using the ``multi`` and ``jobs`` options.

    The options to :meth:`run_many()` are controllable using the
    :doc:`command line options </man/dtf>`.
    """
    dfn = MultiCaseDefinition(case_paths)
    dfn.load()

    if multi is None:
        t = SuiteTestRunner(test_paths)
    elif multi == 'thread':
        t = ThreadedTestRunner(test_paths, jobs)
    elif multi == 'process':
        t = ProcessTestRunner(test_paths, jobs)

    t.load()
    t.definitions(dfn.cases)
    t.run()

def run_one(case, test):
    """
    :param path case_paths:

       The path to a specific :term:`case` (i.e. Python module,)
       relative to the current working directory.

    :param path test_paths:

       The path to a single :term:`test` (i.e. a test definition in
       YAML format,) relative to the current working directory.

    Use :meth:`run_one()` to run a single, specific ``dtf`` test.
    """

    dfn = SingleCaseDefinition()
    dfn.load(test)

    t = SingleTestRunner()
    t.load(case)
    t.definitions(dfn.cases)
    t.run(get_name(case))

######################################################################

# The following allows sphinx.ext.autodoc to parse this module.

if sys.argv[0].rsplit('/', 1)[1] == 'sphinx-build':
    VERBOSE,  FATAL, PASSING, MULTI, JOBS, \
    SINGLE, YAMLTEST, CASEDEF, CASEDIR, TESTDIR = [ None ] * 10
else:
    user_input = interface()
    VERBOSE = user_input.verbose
    FATAL = user_input.fatal
    PASSING = user_input.passing
    MULTI = user_input.multi
    JOBS = user_input.jobs
    SINGLE = user_input.single
    YAMLTEST = user_input.yamltest
    CASEDEF = user_input.casedef
    CASEDIR = user_input.casedir
    TESTDIR = user_input.testdir

def main():
    """
    :meth:`main()` is the main entry point for the :doc:`dtf
    </man/dtf>` script. Based on the user input collected by
    :meth:`interface()`, :meth:`main()` will call either
    :meth:`run_one()` or :meth:`run_many()` with the appropriate
    arguments, as collected by :meth:`interface()`.
    """

    if SINGLE is False:
        run_many(CASEDIR, TESTDIR, MULTI, JOBS)
    else:
        run_one(YAMLTEST, CASEDEF)

if __name__ == '__main__':
    main()
