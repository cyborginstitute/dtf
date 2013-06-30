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

from __future__ import absolute_import

import os.path
import sys
import logging

logger = logging.getLogger(__name__)

from dtf.multi import ProcessTestRunner, ThreadedTestRunner, EventTestRunner
from dtf.core import SingleCaseDefinition, MultiCaseDefinition, SingleTestRunner, SuiteTestRunner
from dtf.utils import expand_tree, get_name
from dtf.err import DtfMissingOptionalDependency

import argparse

def interface():
    """
    :returns: Parsed :class:`~python:argparse.ArgumentParser` object
              that contains user input.

    See :doc:`/man/dtf` for full documentation of all user options.
    """

    parser = argparse.ArgumentParser("Document Testing Framework")

    # general operations
    parser.add_argument('--logfile', '-l', action='store', default=False,
                        help='Specify a file to log output. By default, dtf only logs critical errors and warnings. Use --debug and --info for more verbose logging.')
    parser.add_argument('--info', action='store_true', default=False,
                        help='Increases internal operational logging verbosity')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Enables the most verbose logging of internal operations.')

    # options for running larger test suites.
    parser.add_argument('--casedir', '-c', action='append',
                        help='directory containing python test implementations. you may specify multiple times.')
    parser.add_argument('--testdir', '-t', action='append',
                        help='directory containing yaml test implementaitons. you may specify multiple times.')


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
    logger.debug('creating case definition object. loading cases from "{0}"'.format(case_paths))
    dfn = MultiCaseDefinition(case_paths)

    logger.debug('loading cases.')
    dfn.load()
    logger.debug('successfully loaded cases.')

    if multi is None:
        logger.info('configuring test runner to execute tests serially.')
        t = SuiteTestRunner(test_paths)
    elif multi == 'thread':
        logger.info('configuring test runner to execute tests using a threadpool. {0} workers'.format(str(jobs)))
        t = ThreadedTestRunner(test_paths, jobs)
    elif multi == 'process':
        logger.info('configuring test runner to execute tests using a multiprocess pool {0} workers.'.format(str(jobs)))
        t = ProcessTestRunner(test_paths, jobs)
    elif multi == 'event':
        logger.info('configuring test runner to execute tests using a gevent-based thread pool. {0} workers.'.format(str(jobs)))
        t = EventTestRunner(test_paths, jobs)
    logger.debug('test runner configured.')


    logger.debug('loading tests.')
    t.load()
    logger.debug('loaded tests.')

    logger.debug('passing case definitions to test runner...')
    t.definitions(dfn.cases)
    logger.debug('cases loaded in test runner.')

    try:
        logger.debug('starting test run.')
        t.run()
        logger.debug('test run complete.')
    except DtfMissingOptionalDependency as err:
        logger.error('encountered a missing optional dependency attempting to run tests. Install {0} or use a different builder'.format(err.msg))
        exit(1)


def run_one(case, test):
    """
    :param path case:

       The path to a specific :term:`case` (i.e. Python module,)
       relative to the current working directory.

    :param path test:

       The path to a single :term:`test` (i.e. a test definition in
       YAML format,) relative to the current working directory.

    Use :meth:`run_one()` to run a single, specific ``dtf`` test.
    """
    logger.debug('creating case definition object.')
    dfn = SingleCaseDefinition()

    logger.debug('loading case {0}.'.format(case))
    dfn.load(case)
    logger.debug('loaded {0} case.'.format(case))

    logger.info('configuring test runner object.')
    t = SingleTestRunner()
    logger.debug('loading test {0}.'.format(test))
    t.load(test)
    logger.debug('test {0} successfully loaded.'.format(test))
    logger.info('test runner object configured.')

    logger.debug('passing case definitions to test runner.')
    t.definitions(dfn.cases)
    logger.debug('test runner ready to .')

    logger.debug('starting test run.')
    t.run(get_name(case))
    logger.debug('test run complete.')

######################################################################
#
# The following allows sphinx.ext.autodoc to parse this module.

if sys.argv[0] == 'test.py' or sys.argv[0].rsplit('/', 1)[1] == 'sphinx-build':
    VERBOSE,  FATAL, PASSING, MULTI, JOBS, \
      SINGLE, YAMLTEST, CASEDEF, CASEDIR, TESTDIR = [ None ] * 10

    logging.basicConfig(level=logging.CRITICAL)
    logging.info('running in non-interactive mode. only possible for tests and doc parsing')
else:
    logger.debug('calling user interface to collect input on command line.')
    user_input = interface()

    VERBOSE = user_input.verbose
    FATAL = user_input.fatal
    PASSING = user_input.passing
    MULTI = user_input.multi
    JOBS = user_input.jobs
    SINGLE = user_input.single
    YAMLTEST = user_input.yamltest
    CASEDEF = user_input.casedef

    if user_input.casedir is None:
        CASEDIR = ['cases/']
    else:
        CASEDIR = user_input.casedir

    if user_input.testdir is None:
        TESTDIR = ['tests/']
    else:
        TESTDIR = user_input.testdir

    logger.info('set default test and case dirs')

    if user_input.debug == True:
        log_level = logging.DEBUG
    elif user_input.info == True:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    logger.debug('configuring log level based on user input.')

    if user_input.logfile is not False:
       logging.basicConfig(filename=user_input.logfile, level=log_level)
    else:
       logging.basicConfig(level=log_level)

    logger.info('configuring logger. level {0}'.format(log_level))

from dtf.results import DtfResults
results = DtfResults()

if MULTI == 'process':
    results.sync = True

def main():
    """
    :meth:`main()` is the main entry point for the :doc:`dtf
    </man/dtf>` script. Based on the user input collected by
    :meth:`interface()`, :meth:`main()` will call either
    :meth:`run_one()` or :meth:`run_many()` with the appropriate
    arguments, as collected by :meth:`interface()`.
    """

    if SINGLE is False:
        logger.info('running a test suite.')
        run_many(CASEDIR, TESTDIR, MULTI, JOBS)
        results.render()
    else:
        logger.info('running {0} test with case {1}'.format(YAMLTEST, CASEDEF))
        run_one(CASEDEF, YAMLTEST)
        results.render()

if __name__ == '__main__':
    main()
