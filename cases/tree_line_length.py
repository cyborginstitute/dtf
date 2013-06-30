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

from dtf.cases import DtfCase
from dtf.utils import expand_tree

from line_length import DtfLineLength

class DtfTreeLineLength(DtfLineLength):
    def render_source_tree(self):
        self.msg('crawling "%s" for files.' % self.test_spec['directory'])

        output = [ item for item
                        in expand_tree(self.test_spec['directory'], self.test_spec['extension'])
                        if item not in self.test_spec['exceptions'] ]

        return output

    def check_directory(self):
        p = True
        failing = None

        for source_file in self.render_source_tree():
            result = self.check_file(source_file)

            if result is not None:
                p = False
                failing = source_file
                break
            else:
                self.msg('checked line lengths in %s, which passed.' % source_file)
                continue

        # boolean, int-or-None
        return failing, result 

    def test(self):
        result = self.check_directory()

        if result[0] is None:
            r = True
            msg = 'all files in {0} have no lines longer than {1} characters.'.format(self.test_spec['directory'], self.test_spec['max_length'])
        else:
            r = False
            msg = 'line {0} in "{1}" is longer than {2} characters.'.format(result[1], result[0], self.test_spec['max_length'])

        return r, msg

def main(name, test_spec):
    c = DtfTreeLineLength(name, test_spec)
    c.required_keys(['type', 'directory', 'extension', 'max_length', 'exceptions', 'name'])
    c.run()
