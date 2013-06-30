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

from __future__ import absolute_import

from threading import Lock
from dtf.dtf import VERBOSE, FATAL, PASSING
from dtf.utils import set_or_default

class DtfResults(object):
    def __init__(self, verbose=None, fatal=None, passing=None):
        """An interface to capture and report results from DtfCases."""
        self.verbose = set_or_default(verbose, VERBOSE)
        "If ``True`` return verbose results."

        self.fatal = set_or_default(fatal, FATAL)
        "If ``True``, die on test failure"

        self.passing = set_or_default(passing, PASSING)
        "If ``True`` attempt to return passing test cases."

        self.results = {}
        "Dict that represents the results of all tests."

        self.lock = Lock()
        "A :class:`python:Lock()` object for to support threading."

        self.sync = False
        "When true, call :meth:`~DtfResults.response() immediately.`"
        
    def add(self, name, result, msg):
        """
        :param string name: The name of the test.

        :param bool result: ``True`` if the test passed, and ``False`` if the test failed.

        :param string msg: A string with a human readable note about the outcome of the test.

        Adds current test results to the internal results structure.
        """

        # results are a Tuple of a Boolean (pass/fail) and a message. 

        with self.lock:
            self.results[name] = { 'status': result, 'msg': msg }

        if self.sync: 
            self.response(name, result, msg)

    update = extend
    "An alias for :meth:`~results.DtfResults.extend()`."
    
    def extend(self, name, key, value):
        """
        :param string name: The name of the test. Must exist

        :param string key: The key of the value to add to the results dict.

        :param obj value: The value of the key in the results dict.

        Adds an item with key ``key`` and the value ``value`` to dictionary in
        the ``name`` key of :attr:`~results.Dtf.Results.results`.  

        If ``name`` is not already in :attr:`~results.DtfResults.results`,
        raises :exc:`err.DtfException`.

        If ``key`` exists, :meth:`~results.DtfResults.extend()` will overwrite
        the existing value.
        """

        if name not in self.results:
            raise DtfException('{0} must already exist in results array to extend.')

        self.results[name][key] = value

        if key is 'passing' and self.sync:
            self.response_spec(name, value)

    def response(self, name, result, msg):
        """
        :param string name: The name of the test.
        
        :param boolean result: ``True`` if the test passed. ``False`` otherwise.

        :param string msg: A human readable message for the test.

        Processes the ``msg`` string, and then, depending on the values of
        :attr:`~results.DtfResults.fatal` add :attr:`~results.DtfResults.verbose` may: 

        - raise :exc:`err.DtfException`, 

        - do nothing, or

        - print a message.
        """

        text = '[{0}] {1}'.format(name, msg)
        if result is True and self.verbose is True:
            print(text)
        elif result is True and self.verbose is False:
            pass
        elif result is False and self.fatal is False:
            print(text)
        elif result is False and self.fatal is True:
            raise DtfException(text)

    def response_spec(self, name, data):
        """
        :param string name: The name of the test.

        :param string data: A string with the passing yaml document.

        If :attr:`~results.DtfResults.passing` is ``True``, prints the passing
        document (i.e. ``data``) for ``name`` .
        """

        if self.passing:
            print("# passing document for: {0}.yaml".format(name))
            print('{0}...'.format(data))

    def render(self):
        """
        Calls :meth:`~results.DtfResults.response()` and
        :meth:`~results.DtfResults.response_spec()` (as needed) for every result
        in :attr:`~results.DtfResults.results`.
        """

        

        for k, v in self.results.iteritems():
            self.response(k, v['status'], v['msg'])
        
            if 'passing' in v:
                self.response_spec(k, v['passing'])
