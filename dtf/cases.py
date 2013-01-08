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
    def __init__(self, case, name):
        self.case = case
        self.name = name

    def validate(self, keys):
        valid = validate_keys(keys, self.case, self.name)
        if valid is True:
            return (True, '[%s]: "%s" is a valid "%s" test case.'
                                  % (self.name, self.case['name'], self.case['type']))
        else:
            return (False, '[%s]: "%s" is not a valid "%s" test case.'
                            % (self.name, self.case['name'], self.case['type']))

    def run(self):
        raise DtfNotImplemented('test cases must implement run methods.')

if __name__ == '__main__':
    case = DtfCase( { 'a': 1, 'b': 2, 'name': 'what', 'type': 'fox', 'extra': None}, 'bar')
    assert(case.validate([ 'a', 'b', 'name', 'type' ])[0] is True)
