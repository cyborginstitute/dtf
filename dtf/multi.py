# Copyright 2013 Sam Kleinman
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
Provides additional :class:`~core.TestRunner()` classes that implement various
parallel operation modes to run tests.

For most moderate deployments, running tests in serial will out perform any of
the methods provided here. However, because the workloads of tests are not
uniform, and good test performance is crucial for usability, :mod:`dtf` provides
these options, largely for testing and research.
"""

from __future__ import absolute_import

from dtf.core import MultiTestRunner 
    
class PoolTestRunner(MultiTestRunner):
    """
    A :class:`~core.MultiTestRunner()` sub-class that initializes a single
    additional attribute for configuring thread or worker pools.

    Used as a base class for the test runners with parallel test
    execution. Lacks a :meth:`~core.TestRunner.run()`` method.
    """
    def __init__(self, test_paths=[], pool_size=2):
        """
        :param list test_paths: Defaults to an empty list. Passes through to
                                :attr:`~core.TestRunner.test_paths`.

        :param int pool_size: Defaults to ``2``. The size of the thread pool to
                              use to process tests.
        """
        super(PoolTestRunner, self).__init__(test_paths)
        self.pool_size = pool_size
        "The size of the worker thread pool used to run tests."

class ThreadedTestRunner(PoolTestRunner):
    """
    Uses the :mod:`threadpool` module to run a suite of tests with a pool of
    threads. This is the ideal modality for suites with workloads that spend the
    most of the time reading files and computing hashes, which may be common for
    some suites. See :class:`~multi.ProcessTestRunner()` for an alternate
    parallelism strategy.
    """
    def run(self):
        """
        Runs all tests in the :attr:`~core.TestRunner.queue` list using a thread
        pool to run all tests concurrently.
        """
        import threadpool

        pool = threadpool.ThreadPool(self.pool_size)

        for j in self.queue:
            job = threadpool.WorkRequest(self.case_definition.get(j[0]), args=(j[1], j[2]))
            pool.putRequest(job)

        pool.wait()

class ProcessTestRunner(PoolTestRunner):
    """
    Uses the :class:`~multiprocessing.Pool()` class within the standard
    :mod:`multiprocessing` module to run tests in parallel. Functionally
    equivelent to :class:`~multi.ThreadedTestRunner()`, without the fallback
    possibility. 

    Theoretically the :mod:`multiprocessing` approach has more overhead than
    :mod:`threading`; however, in cases where the performance bottlenecks are
    due to the interpreter lock, this approach may afford better performance.
    """
    def run(self):
        """
        Runs all tests in :attr:`~core.TestRunner.queue` using a pool of
        independent Python processes to run all tests concurrently.
        """

        from multiprocessing import Pool

        p = Pool(self.pool_size)

        for j in self.queue:
            p.apply_async(self.case_definition.get(j[0]), (j[1], j[2]))

        p.close()
        p.join()

class EventTestRunner(PoolTestRunner):
    """
    Uses the :class:`~gevent.pool.Pool()` class to run tests in parallel using
    gevent and greenlets. Typically this modality has only minor additional
    overhead in addition to running tests in serial, but may provide the same
    benefits as :class:`~multi.ThreadedTestRuner()` with lower overhead.
    """
    def run(self):
        """
        Runs all tests in :attr:`~core.TestRunner.queue` using a pool of
        greenlets to run tests concurrently.
        """
        import gevent
        from gevent.pool import Pool

        p = Pool(self.pool_size)

        for j in self.queue:
            p.spawn(self.case_definition.get(j[0]), j[1], j[2])
