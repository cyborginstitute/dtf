# Copyright 2012-2013 Sam Kleinman
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

try:
     from dtf import VERBOSE, FATAL, PASSING
     from err import DtfException, DtfTestException, DtfNotImplemented
except ImportError:
     from dtf.dtf import VERBOSE, FATAL, PASSING
     from dtf.err import DtfException, DtfTestException, DtfNotImplemented

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
        All arguments to the :meth:`~cases.DtfCase.validate()` method are
        optional, and if any arguments have the value of ``None``
        :meth:`validate()` will substitute values from the object instance or
        user input values.

        :param list keys:

            A list of required keys that the :attr:`test_spec.keys
            <cases.dtf.test_spec>` must contain to be valid.

        :param list test_keys:

            A list of keys from the ``test_spec`` that the must be
            identical to or a superset of the keys in the ``keys``
            list. Defaults to the value of :attr:`test_spec.keys
            <cases.dtf.test_spec>`. 

        :param bool verbose:

            If ``true``, :meth:`~cases.DtfCase.validate()` will return output
            that confirms valid tests in addition to reporting invalid
            tests. Defaults to the value of :data:`~dtf.VERBOSE`.

        :param bool fatal:

            If ``true``, :meth:`~cases.DtfCase.validate()` will raise an
            :exc:`~err.DtfException` rather than printing the failure message
            for invalid tests..

        Checks the keys in each test specification to ensure that the test has
        the required keys.
        """
        if keys is None:
            if self.keys == []:
                raise DtfException('must add required_keys to DtfCase subclasses.')
            else: 
                keys = self.keys

        if test_keys is None:
            test_keys = self.test_spec.keys()

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

        if verbose is None:
            verbose = VERBOSE

        if fatal is None:
            fatal = FATAL

        self.response(result=t, msg=msg, verbose=verbose, fatal=fatal)
        return (t, msg, verbose, fatal)

    def dump(self, test_spec, path, keys=None):
        """
        :param dict test_spec: A dictionary to export to a yaml test
                               specification.

        :param string path: The path of the output file.

        :param list keys: Optional. A list of keys to validate using
                          :meth:`~cases.DtfTest.validate()`.

        Writes a ``test_spec`` in YAML format to a file specified by ``path``. A
        thin wrapper around :meth:`yaml.dump()` method, with additional
        validation and formatting

        When ``keys`` is not ``None``, :meth:`~cases.DtfTest.dump()` will
        validate the keys in ``test_spec`` using
        :meth:`~cases.DtfTest.validate()`. Invalid ``test_specs`` always raise a
        :exc:`~err.DtfException`.
        """
        if keys is not None:
            valid = self.validate(keys, test_spec)
            if valid[0] is False:
                raise DtfException(valid[1])

        with open(path, 'w') as f:
            f.write(yaml.dump(test_spec, default_flow_style=False))

    def response(self, result, msg, verbose=False, fatal=False):
        """
        :param bool result: 

        :param msg string: 

        :param bool verbose: Causes :meth:`~cases.DtfCases.response()` a
                             to ``False``.

        :param bool fatal: Defaults to ``False``. 
        """

        if result is True and verbose is True:
            print(msg)
        elif result is True and verbose is False:
            pass
        elif result is False and fatal is False:
            print(msg)
        elif result is False and fatal is True:
            raise DtfTestException(msg)

    def msg(self, msg, verbose=None):
        """
        :param string message: A message to return.

        A helper function that returns a message, tagged with
        :attr:`~cases.DtfCase.name`, *if* :data:`~dtf.VERBOSE` is true.
        """

        o = '[%s]: %s' % (self.name, msg)
        if verbose is None:
            verbose = VERBOSE

        if verbose is True: 
            print(o)

        return o

    def passing(self):
        """
        A stub method, for the :meth:`~cases.DtfCase.passing()` method, that
        case definitions may implement. The intention of the
        :meth:`~cases.DtfCase.passing()` method is that, when called it will
        take the ``test_spec`` for the current test and return a passing variant
        that the developer/writer can use to update a fixed test.

        Raises :exc:`~err.DtfNotImplemented`. 
        """
        raise DtfNotImplemented("cases must implement the optional passing() method")

    def print_passing_spec(self):
        """
        A wrapper for :meth:`~cases.DtfCase.passing()` that:
        - adds comments to the output for increased clarity.

        - only prints the passing specification if the instance attribute
          :attr:`~cases.DtfCase.return_value` is ``False``.
        """
        if self.return_value is False:
            print("# passing document for: " + self.name + ".yaml")
            print(self.passing() + '...')

    def test(self):
        """
        A stub method for the :meth:`~cases.DtfCase.test()` method, that case
        definitions must implement.
    
        :meth:`~cases.DtfCase.test()` should return a two-tuple that contains:

        0. A boolean that is ``True`` if the test passes and ``False`` if the
           test fails.

        1. A string that contains a message that *may* be delivered to the users
           depending on the verbosity settings.
        """
        raise DtfNotImplemented('cases must implement the required test() method.')

    def run(self):
        """
        A helper method that orchestrates test operation. Takes no arguments and
        preforms the folloing operations:
        
        1. Calls :meth:`~cases.DtfCase.validate()` method, passing
           :data:`~dtf.VEBOSE` and :data:`~dtf.FATAL` as appropriate.

        2. Sets :attr:`~cases.DtfCase.return_value` to the value of the first
           element returned by :meth:`~cases.DtfCase.test()`.

        3. Calls :meth:`~cases.DtfCase.response()` passing the results from
           :meth:`~cases.DtfCase.test()` :data:`~dtf.VEBOSE` and
           :data:`~dtf.FATAL` as appropriate.
        """
        self.validate(verbose=VERBOSE, fatal=FATAL)

        t = self.test()

        self.return_value = t[0]

        self.response(result=t[0], msg=t[1], verbose=VERBOSE, fatal=FATAL)

