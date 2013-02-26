import hashlib
import os

# TODO make stand alone operation work with installed dtf
try:
    from cases import DtfCase, PASSING
    import dtf
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "dtf")))
    from cases import DtfCase, PASSING
    import dtf

class DtfChange(DtfCase):
    @staticmethod
    def hash(file, block_size=2**20):
        md5 = hashlib.md5()
        with open(file, 'rb') as f:
            for chunk in iter(lambda: f.read(128*md5.block_size), b''):
                md5.update(chunk)
        return md5.hexdigest()

    def test(self, r=False):
        if self.hash(self.test_spec['file']) == self.test_spec['hash']:
            r = True

        if r is False: 
            msg = ('[%s]: file named "%s" changed. Update other files as needed.' 
                   % ( self.test_spec['name'], self.test_spec['file']))
        else:
            msg = ('[%s]: file named "%s" is **not** changed. No further action required.' 
                   % ( self.test_spec['name'], self.test_spec['file']))

        return r, msg

    def passing(self):
        self.test_spec['hash'] = self.hash(self.test_spec['file'])
        
        return yaml.dump(self.test_spec, default_flow_style=False)

def main(name, test_spec):
    c = DtfChange(name, test_spec)
    c.required_keys(['file', 'hash', 'type', 'name'])
    c.run()

    if PASSING is True:
        c.print_passing_spec()
