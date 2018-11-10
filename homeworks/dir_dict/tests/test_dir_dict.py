from unittest import TestCase
import os

from dir_dict import DirDict

TEST_PATH = os.path.join("tests", "test_dir")


class TextHistoryTestCase(TestCase):

    def test_dir_dict_base(self):
        d = DirDict(TEST_PATH)
        self.assertEqual(0, len(d))
        d['el1'] = 'data1'
        d['el2'] = 'data2'
        self.assertEqual(2, len(d))
        with self.assertRaises(KeyError):
            print(d['el3'])
        self.assertEqual(d['el1'], 'data1')
        self.assertEqual(d['el2'], 'data2')
        del d['el1']
        with self.assertRaises(KeyError):
            print(d['el'])

    def tearDown(self):
        for item in os.listdir(TEST_PATH):
            os.remove(os.path.join(TEST_PATH, item))
        os.rmdir(TEST_PATH)
