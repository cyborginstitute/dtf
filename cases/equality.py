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
# 
# Part of the example distribution of DTF: https://pypi.python.org/pypi/dtf/

try:
    from cases import DtfCase
except ImportError:
    from dtf.cases import DtfCase

class DtfEquality(DtfCase):
    def test(self):
        if self.test_spec['value0'] == self.test_spec['value1']:
            r = True
            msg = ('[%s]: "%s" %s successful! %s equals %s'
                   % (self.name, self.test_spec['name'], 'equality test', self.test_spec['value0'], self.test_spec['value1']))
        else:
            r = False
            msg = ('[%s]: "%s" %s failed! %s does not equal %s'
                   % (self.name, self.test_spec['name'], 'equality test', self.test_spec['value0'], self.test_spec['value1']))

        return r, msg

def main(name, test_spec):
    c = DtfEquality(name, test_spec)
    c.required_keys(['name', 'type', 'value0', 'value1'])
    c.run()
