from cases import validate_keys as validate_case

def main(case, name):
    required_keys = [ 'name', 'type', 'value0', 'value1']

    if validate_case(required_keys, case, name) is True:
        print('[%s]: "%s" is a valid "%s" test case.' % (name, case['name'], case['type']))
    else:
        Exception(name + ' does not have required key: ' + key)

    if case['value1'] == case['value0']:
        statement = '[%s]: "%s" %s successful! %s equals %s' % (name, case['name'], 'equality test', case['value1'], case['value0'])
    else:
        statement = '[%s]: "%s" %s failed! %s does not equal %s' % (name, case['name'], 'equality test', case['value1'], case['value0'])

    print(statement)
