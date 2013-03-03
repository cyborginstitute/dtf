from collections import OrderedDict
from unittest import TestCase

from dtf.cases import DtfCase
from dtf.err import DtfException, DtfNotImplemented

class TestDtfCase(TestCase):
    @classmethod
    def setUp(self):
        self.name = 'casename'
        self.key_list = ['path', 'type', 'name' ]
        self.test_spec = dict(name='test1', path='/path/to/newark', type='test')
        self.c = DtfCase(self.name, self.test_spec)

    def test_dtf_name(self):
        self.assertEqual(self.name, self.c.name)

    def test_dtf_test_spec0(self):
        self.assertEqual(self.c.test_spec, self.test_spec)
        
    def test_dtf_test_spec1(self):
        for key in self.key_list:
            self.assertTrue(key in self.c.test_spec.keys())

    def test_empty_keys(self):
        c = DtfCase(self.name, {})
        self.assertEqual(self.c.keys, [])

    def test_required_keys(self):
        self.c.required_keys(self.key_list)
        for key in self.key_list:
            self.assertTrue(key in self.c.keys)
        
    def test_validate_keys_pass(self):
        self.c.required_keys(self.key_list)
        self.assertTrue(self.c.validate()[0])

    def test_validate_keys_fail(self):
        self.c.required_keys(['foo', 'md5', 'hash'])
        self.assertFalse(self.c.validate()[0])

    def test_validate_keys_arg_overrid_fail(self):
        self.c.required_keys(self.key_list)
        self.assertFalse(self.c.validate(keys=['hash', 'type2'])[0])

    def test_validate_keys_arg_pass(self):
        self.assertTrue(self.c.validate(keys=self.key_list)[0])

    def test_validate_keys_arg_fail(self):
        self.assertFalse(self.c.validate(keys=['foo', 'md5', 'hash'])[0])

    def test_validate_keys_empty(self):
        self.c.keys = []
        with self.assertRaises(DtfException):
            self.c.validate()

    def test_dump_invalid_set(self):
        self.c.required_keys(self.key_list)
        with self.assertRaises(DtfException):
            self.c.dump(test_spec=self.test_spec, path='/dev/null', keys=['hash', 'type2'])

    def test_message(self):
        msg_str = 'test message'
        self.assertEqual('[%s]: %s' %(self.name, msg_str), self.c.msg(msg_str))

    def test_passing_not_implemented(self):
        with self.assertRaises(DtfNotImplemented):
            self.c.passing()

    def test_test_not_implemented(self):
        with self.assertRaises(DtfNotImplemented):
            self.c.test()
