from cases import DtfCase

class DtfEquality(DtfCase):
    def run(self):
        print(self.validate()[1])

        if self.case['value0'] == self.case['value1']:
            result = ('[%s]: "%s" %s successful! %s equals %s'
                      % (self.name, self.case['name'], 'equality test', self.case['value0'], self.case['value1']))
        else:
            result = ('[%s]: "%s" %s failed! %s does not equal %s'
                      % (self.name, self.case['name'], 'equality test', self.case['value0'], self.case['value1']))

        print result

def main(name, case):
    c = DtfEquality(name, case)
    c.required_keys(['name', 'type', 'value0', 'value1'])
    c.run()



