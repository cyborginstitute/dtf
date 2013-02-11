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

import yaml

from dtf import VERBOSE, FATAL, PASSING
from err import DtfException, DtfTestException, DtfNotImplemented

class DtfCase(object):
    """
    Pass the following two parameters when instantiating
    :class:`DtfCase` objects:
    
    :param string name:

        The name of the test, typically derived from the file name of
        the test specification itself.
    
    :param object test_spec: 

        The test_spec object, imported from the term:`test`
        specification provided in YAML by the user.

    :class:`DtfCase` is a base class useful for implementing most
    ``dtf`` cases while requiring only limited familiarity with
    ``dtf`` internals.

    """

    def __init__(self,name, test_spec):
        self.test_spec = test_spec
        """A dictionary, passed to the class during object creation,
        that holds the test specification imported from the
        user-supplied YAML specification."""

        self.name = name 
        """The name of the test, typically derived from the file name
        of the test itself."""
        
        self.keys = []
        """A list of top-level keys in the :attr:`test_spec`
        dictionary. Cases will pass a list of keys to the
        :meth:`required_keys()` method after creating the object, but
        before calling. :meth:`validate()`."""

    def required_keys(self, keys):
        """
        :param list keys: 

           A list of top level keys that :attr:`test_spec` must have
           to be considered valid by :meth:`validate()`.

        Currently does not implement recursive key checking.
        """

        for key in keys:
            self.keys.append(key)

    def validate(self, keys=None, test_keys=None, verbose=None, fatal=None):
        """
        All arguments to the :meth:`validate()` method are optional,
        and if any arguments have the value of ``None``
        :meth:`validate()` will substitute values from the object
        instance or user input values.

        :param list keys: 

            A list of required keys that `test_spec`` must contain to
            be valid.

        :param list test_keys:

            A list of keys from the ``test_spec`` that the must be
            identical to or a superset of the keys in the ``keys``
            list.

        :param bool verbose:

        :param bool fatal:

        """

        if test_keys is None:
            test_keys = self.test_spec.keys()

        if verbose is None:
            verbose = VERBOSE
            
        if fatal is None: 
            fatal = FATAL

        if keys is None and self.keys is False:
            raise DtfException('must add required_keys to DtfCase subclasses.')
        else:
            keys = self.keys

        t = True
        for key in keys:
            if key in test_keys:
                pass
            else:
                t = False
                break

        if t is True:
            msg = ('[%s]: "%s" is a valid "%s" test spec.'
                   % (self.name, self.test_spec['name'], self.test_spec['type']))
        elif t is False:
            msg = ('[%s]: "%s" is not a valid "%s" test spec.'
                   % (self.name, self.test_spec['name'], self.test_spec['type']))

        return self.response(result=t, msg=msg, verbose=verbose, fatal=fatal)

    def dump(self, test_spec, path, keys=None):
        if keys is not None:
            valid = self.validate(keys, test_spec)
            if valid[0] is False:
                raise DtfException(valid[1])

        with open(path, 'w') as f:
            f.write(yaml.dump(test_spec, default_flow_style=False))

    def response(self, result, msg, verbose=False, fatal=False):
        if result is True and verbose is True:
            print(msg)
        elif result is True and verbose is False:
            pass
        elif result is False and fatal is False:
            print(msg)
        elif result is False and fatal is True:
            raise DtfTestException(msg)

    def msg(self, msg):
        if VERBOSE:
            print('[%s]: %s' % (self.name, msg))

    def passing(self):
        raise DtfNotImplemented("cases must implement the optional passing() method")

    def print_passing_spec(self):
        if self.return_value is False:
            print("# passing document for: " + self.name + ".yaml")
            print(self.passing() + '...')

    def test(self):
        raise DtfNotImplemented('cases must implement the required run() method.')

    def run(self):
        self.validate(verbose=VERBOSE, fatal=FATAL)

        t = self.test()

        self.return_value = t[0]

        self.response(result=t[0], msg=t[1], verbose=VERBOSE, fatal=FATAL)
