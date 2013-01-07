class DtfException(Exception):
    pass

class DtfNotImplemented(DtfException):
    pass

def validate_keys(keys, case, name):
    for key in keys:
        if case.has_key(key) is False:
            return False

    return True

class DtfCase(object):
    def __init__(self, case, name):
        self.case = case
        self.name = name

    def validate(self, keys):
        valid = validate_keys(keys, self.case, self.name)
        if valid is True:
            return (True, '[%s]: "%s" is a valid "%s" test case.'
                                  % (self.name, self.case['name'], self.case['type']))
        else:
            return (False, '[%s]: "%s" is not a valid "%s" test case.'
                            % (self.name, self.case['name'], self.case['type']))

    def run(self):
        raise DtfNotImplemented('test cases must implement run methods.')

    def run_and_validate(self):
        self.validate_case()
        self.run()

if __name__ == '__main__':
    case = DtfCase( { 'a': 1, 'b': 2, 'name': 'what', 'type': 'fox'}, 'bar')
    assert(case.validate([ 'a', 'b', 'name', 'type' ])[0] is True)
