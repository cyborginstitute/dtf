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
        # results are a Tuple of a Boolean (pass/fail) and a message. 

        with self.lock:
            self.results[name] = { 'status': result, 'msg': msg }

        if self.sync: 
            self.response(name, result, msg)

    def extend(self, name, key, value):
        self.results[name][key] = value

    def response(self, name, result, msg):
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
        if self.passing:
            print("# passing document for: {0}.yaml".format(name))
            print('{0}...'.format(data))

    def render(self):
        for k, v in self.results.iteritems():
            self.response(k, v['status'], v['msg'])
        
            if 'passing' in v:
                self.response_spec(k, v['passing'])
