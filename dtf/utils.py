import os

def get_test_name(test):
    return test.rsplit('/', 1)[-1].rsplit('.', 1)[0]

def expand_tree(path, input_extension='yaml'):
    file_list = []
    for root, subFolders, files in os.walk(path):
        for file in files:
            f = os.path.join(root,file)
            if f.rsplit('.', 1)[1] == input_extension:
                file_list.append(f)

    return file_list

def get_tests(case_paths):
    from importlib import import_module
    import sys

    test_types = {}

    tests = []
    for path in case_paths:
        module_path = os.getcwd() + '/' + path
        sys.path.append( module_path )

        for f in expand_tree(path, 'py'):
            tests.append((get_test_name(f), module_path))

    for test in tests:
        if test[0] == '__init__':
            pass
        else:
            test_types.update( { test[0]: import_module(test[0], test[1]).main } )

    return test_types
