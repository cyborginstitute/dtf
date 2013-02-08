#!/usr/bin/python

from cases import DtfCase
from utils import expand_tree
import dtf

class DtfLineLength(DtfCase):
    @staticmethod
    def check_line(line, max_length):
        if len(line) > max_length: 
            return True
        else: 
            return False

    def render_source_tree(self): 
        self.msg('crawling "%s" for files.' % self.case['directory'])

        output = [ item for item 
                        in expand_tree(self.case['directory'], self.case['extension'])
                        if item not in self.case['exceptions']
                ]

        return output

    def check_directory(self, p=None):
        for source_file in self.render_source_tree():
            ln = 1
            with open(source_file, 'r') as f: 
                ln += 1
                for line in f.readlines():
                    ln = ln + 1
                    if self.check_line(line, self.case['max_length']):
                        p = False
                        failing = source_file
                        break
                
            if p is False: 
                break
            else:
                self.msg('checked line lengths in %s, which passed.' % source_file)

        if p is False: 
            return p, failing, ln
        else:
            return True, p, p


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
    c = DtfLineLength(name, case)
    c.required_keys(['type', 'directory', 'extension', 'max_length', 'exceptions'])
    c.run()
