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

class DtfException(Exception):
    pass

class DtfNotImplemented(DtfException):
    pass

def validate_keys(keys, case, name):
    for key in keys:
        if case.has_key(key) is False:
            return False
    return True

class DtfCase(object):
    def __init__(self,name, case):
        self.case = case
        self.name = name
        self.keys = []

    def required_keys(self, keys):
        for key in keys:
            self.keys.append(key)

    def validate(self, keys=None, case=None, verbose=False, fatal=False):
        if case is None:
            case = self.case

        if keys is None and self.keys is False:
            raise DtfException('must add required_keys to DtfCase subclasses.')
        else: 
            keys = self.keys

        t = validate_keys(keys, case,self.name)

        if t is True:
            msg = ('[%s]: "%s" is a valid "%s" test case.'
                   % (self.name, self.case['name'], self.case['type']))
        elif t is False:
            msg = ('[%s]: "%s" is not a valid "%s" test case.'
                   % (self.name, self.case['name'], self.case['type']))

        return self.response(result=t, msg=msg, verbose=verbose, fatal=fatal)

    def dump(self, case, path, keys=None):
        if keys is not None:
            valid = self.validate(keys, case)
            if valid[0] is False:
                raise DtfException(valid[1])

        with open(path, 'w') as f:
            f.write(yaml.dump(case, default_flow_style=False))

    def response(self, result, msg, verbose=False, fatal=False):
        if result is True and verbose is True:
            print(msg)
        elif result is True and verbose is False:
            pass
        elif result is False and fatal is False:
            print(msg)
        elif result is False and fatal is True:
            raise Exception(msg)

    def test(self):
        raise DtfNotImplemented('test cases must implement run methods.')

    def run(self):
        self.validate()
        t = self.test()
        self.return_value = t[0]
        self.response(t[0], t[1])
