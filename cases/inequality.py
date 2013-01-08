from cases import DtfCase

class DtfInequality(DtfCase):
    def test(self, a, b):
        if a != b:
            result = ('[%s]: "%s" %s successful! %s does not equal %s'
                      % (self.name, self.case['name'], 'inequality test', a, b))
        else:
            result = ('[%s]: "%s" %s failed! %s equals %s'
                      % (self.name, self.case['name'], 'inequality test', a, b))
        return result

    def run(self):
        print(self.validate()[1])
        print(self.test(self.case['value0'], self.case['value1']))

def main(name, case):
    c = DtfInequality(name, case)
    c.required_keys(['name', 'type', 'value0', 'value1'])
    c.run()
