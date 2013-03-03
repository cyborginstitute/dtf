from change import DtfChange
import yaml

# TODO make stand alone operation work with installed dtf
try:
    from dtf import PASSING
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "dtf")))
    from dtf.dtf import PASSING


class DtfPaired(DtfChange):
    def test(self, a=False, b=False):
        if self.hash(self.test_spec['file0']['path']) == self.test_spec['file0']['hash']:
            a = True

        if self.hash(self.test_spec['file1']['path']) == self.test_spec['file1']['hash']:
            b = True

        if a is True and b is True:
            msg = "[%s]: no changes" % self.name
        else:
            if a is False and b is False:
                msg = ('[%s]: both "%s" and "%s" files changed.'
                       % (self.name, self.test_spec['file1']['path'], self.test_spec['file0']['path']))
            elif a is False:
                msg = ('[%s]: "%s" changed without "%s".'
                       % (self.name, self.test_spec['file1']['path'], self.test_spec['file0']['path']))
            elif b is False:
                msg = ('[%s]: only "%s" changed without "%s".'
                       % (self.name, self.test_spec['file0']['path'], self.test_spec['file1']['path']))

        r = a and b

        return r, msg

    def passing(self):
        self.test_spec['file0']['hash'] = self.hash(self.test_spec['file0']['path'])
        self.test_spec['file1']['hash'] = self.hash(self.test_spec['file1']['path'])

        return yaml.dump(self.test_spec, default_flow_style=False)


def main(name, test_spec):
    c = DtfPaired(name, test_spec)
    c.required_keys(['file1', 'file0', 'type', 'name'])
    c.run()

    if PASSING is True:
        c.print_passing_spec()
