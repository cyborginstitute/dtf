from cases import DtfCase

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
