import hashlib
import yaml

from cases import DtfCase

class DtfPaired(DtfCase): 
    @staticmethod
    def hash(file, block_size=2**20):
        md5 = hashlib.md5()
        with open(file, 'rb') as f:
            for chunk in iter(lambda: f.read(128*md5.block_size), b''):
                md5.update(chunk)
        return md5.hexdigest()

    def test(self, a=False, b=False):
        if self.hash(self.case['file0']['path']) == self.case['file0']['hash']: 
            a = True

        if self.hash(self.case['file1']['path']) == self.case['file1']['hash']: 
            b = True

        if a is True and b is True:
            msg = "[%s]: no changes" % self.name
        else: 
            if a is False and b is False:
                msg = '[%s]: both %s and %s files changed.' % (self.name, self.case['file1']['path'], self.case['file0']['path'])
            elif a is False:
                msg = '[%s]: only %s changed.' % (self.name, self.case['file1']['path'])
            elif b is False: 
                msg = '[%s]: only %s changed.' % (self.name, self.case['file0']['path'])

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
    if c.return_value is False:
        print(">>>> passing document for: " + c.name + ".yaml")
        print(c.passing())
