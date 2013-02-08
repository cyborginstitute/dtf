#!/usr/bin/python

from cases import DtfCase
from utils import expand_tree
from line_length import DtfLineLength
import dtf

class DtfTreeLineLength(DtfLineLength):
    def render_source_tree(self): 
        self.msg('crawling "%s" for files.' % self.case['directory'])

        output = [ item for item
                        in expand_tree(self.case['directory'], self.case['extension'])
                        if item not in self.case['exceptions'] ]

        return output

    def check_directory(self, p=None):
        for source_file in self.render_source_tree():
            result = self.check_file(source_file)

            if result[0] is False: 
                failing = source_file
                break
            else:
                self.msg('checked line lengths in %s, which passed.' % source_file)
                continue

        if p is False: 
            return False, failing, result[1]
        else:
            return True, None, None


    def test(self):
        result = self.check_directory()

        if result[0] is True: 
            msg = ('[%s]: all files in %s have no lines longer than %s characters.' 
                   % (self.name, self.case['directory'], self.case['max_length']))
        else:
            msg = ('[%s]: line %s in "%s" is longer than %s characters.' 
                   % (self.name, result[2], result[1], self.case['max_length']))
            
        return result[0], msg

def main(name, case):
    c = DtfTreeLineLength(name, case)
    c.required_keys(['type', 'directory', 'extension', 'max_length', 'exceptions', 'name'])
    c.run()
