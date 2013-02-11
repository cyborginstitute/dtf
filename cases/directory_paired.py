from change import DtfChange
import os

# TODO make stand alone operation work with installed dtf
try:
    from cases import PASSING
    import dtf
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "dtf")))
    from cases import PASSING
    import dtf

class DtfDirectoryPaired(DtfChange):
    def test(self, a=False, b=False):
        if self.hash(self.test_spec['file']['path']) == self.test_spec['file']['hash']:
            a = True 

        self.new_directory_count = len(os.listdir(self.test_spec['directory']))

        if self.test_spec['count'] == self.new_directory_count: 
            b = True

        if a is True and b is True: 
            msg = ('[%s]: number of files in "%s" and the content of "%s" has not changed.' 
                   % (self.name, self.test_spec['directory'], self.test_spec['file']['path']))
        else: 
            if a is False and b is False: 
                msg = ('[%s]: number of files in "%s" and the content of "%s" have changed.' 
                       % (self.name, self.test_spec['directory'], self.test_spec['file']['path']))
            elif a is False: 
                msg = ('[%s]: content of "%s" has changed. Likely false positive.' 
                       % (self.name, self.test_spec['file']['path']))
            elif b is False:
                msg = ('[%s]: number of files in "%s" changed. Update "%s" now.' 
                       % (self.name, self.test_spec['directory'], self.test_spec['file']['path']))
                
        r = a and b
        return r, msg        

    def passing(self):
        self.test_spec['file']['hash'] = self.hash(self.test_spec['file']['path'])
        self.test_spec['count'] = self.new_directory_count

        return yaml.dump(self.test_spec, default_flow_style=False)

def main(name, test_spec):
    c = DtfDirectoryPaired(name, test_spec)
    c.required_keys(['directory', 'file', 'count', 'type', 'name'])
    c.run()

    if PASSING is True:
        c.print_passing_spec()
