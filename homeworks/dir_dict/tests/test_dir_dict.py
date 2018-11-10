from unittest import TestCase
import os

from dir_dict import DirDict

TEST_PATH = os.path.join("tests", "test_dir")


class TextHistoryTestCase(TestCase):

    def test_dir_dict_base(self):
        d_dir = DirDict(TEST_PATH)
        self.assertEqual(0, len(d_dir))

        d_dir['el1'] = 'data1'
        d_dir['el2'] = 'data2'
        d_dir['el3'] = 'data3'

        self.assertEqual(3, len(d_dir))

        with self.assertRaises(KeyError):
            print(d_dir['el4'])

        self.assertEqual(d_dir['el1'], 'data1')
        self.assertEqual(d_dir['el2'], 'data2')
        self.assertEqual(d_dir['el3'], 'data3')

        del d_dir['el1']

        with self.assertRaises(KeyError):
            print(d_dir['el'])

        d = {'el2': 'data2', 'el3': 'data3'}
        self.assertEqual(str(d), str(d_dir))

    def tearDown(self):
        for item in os.listdir(TEST_PATH):
            os.remove(os.path.join(TEST_PATH, item))
        os.rmdir(TEST_PATH)
