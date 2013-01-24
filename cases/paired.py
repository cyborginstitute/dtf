from change import DtfChange
import yaml

# TODO make stand alone operation work with installed dtf
try:
    from cases import PASSING
    import dtf
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "dtf")))
    from cases import PASSING
    import dtf


class DtfPaired(DtfChange):
    def test(self, a=False, b=False):
        if self.hash(self.case['file0']['path']) == self.case['file0']['hash']:
            a = True

        if self.hash(self.case['file1']['path']) == self.case['file1']['hash']:
            b = True

        if a is True and b is True:
            msg = "[%s]: no changes" % self.name
        else:
            if a is False and b is False:
                msg = ('[%s]: both "%s" and "%s" files changed.'
                       % (self.name, self.case['file1']['path'], self.case['file0']['path']))
            elif a is False:
                msg = ('[%s]: "%s" changed without "%s".'
                       % (self.name, self.case['file1']['path'], self.case['file0']['path']))
            elif b is False:
                msg = ('[%s]: only "%s" changed without "%s".'
                       % (self.name, self.case['file0']['path'], self.case['file1']['path']))

        r = a and b

        return r, msg

    def passing(self):
        self.case['file0']['hash'] = self.hash(self.case['file0']['path'])
        self.case['file1']['hash'] = self.hash(self.case['file1']['path'])

        return yaml.dump(self.case, default_flow_style=False)


def main(name, case):
    c = DtfPaired(name, case)
    c.required_keys(['file1', 'file0', 'type', 'name'])
    c.run()

    if PASSING is True:
        c.print_passing_spec()

if __name__ == '__main__':
    dtf.run_one(dtf.user_input.yamlcase, __file__)
