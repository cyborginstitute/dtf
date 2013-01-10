from cases import DtfCase

class DtfInequality(DtfCase):
    def test(self):
        a=self.case['value0']
        b=self.case['value1']

        if a != b:
            r = True
            result = ('[%s]: "%s" %s successful! %s does not equal %s'
                      % (self.name, self.case['name'], 'inequality test', a, b))
        else:
            r = False
            result = ('[%s]: "%s" %s failed! %s equals %s'
                      % (self.name, self.case['name'], 'inequality test', a, b))

        return r, result

def main(name, case):
    c = DtfInequality(name, case)
    c.required_keys(['name', 'type', 'value0', 'value1'])
    c.run()
