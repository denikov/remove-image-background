'''
TESTING SERVICES MODULE
'''

# set the path to the project directory
import sys
import os
testdir = os.path.dirname(__file__)
srcdir = '../remove-image-background'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
import services
import json
from unittest.mock import patch


class ServicesTest(unittest.TestCase):

    @classmethod
    def setUpClass(inst):
# testing the initial values
        inst.initial_list = services._name_list
        inst.initial_index = services._current_index

# pass test file to services module
        services._file_path = 'tests/sample.json'
        inst.firstName = services.loadList()



    def test_loadList(self):
# returning the first value from the file
        self.assertEqual(self.initial_list, [])
        self.assertEqual(self.initial_index, 0)
        self.assertEqual(self.firstName, 'alecia keys')



    @patch('services.removeFromTemp')
    def test_addToJSON(self, mock_removeFromTemp):
        mock_removeFromTemp.return_value = None
        returnedName = services.addToJSON('test.png')
        self.assertEqual(services._name_list[0]['file'], 'test.png')
        self.assertEqual(services._current_index, 1)
        self.assertEqual(returnedName, 'Kobe byrant')



    def test_checkAllFound(self):
        services._current_index = 3
        self.assertEqual(services.checkAllFound(), 'mark walburg')
        services._current_index = 4
        self.assertIsNone(services.checkAllFound())



# remove any modifications to the sample.json file
    @classmethod
    def tearDownClass(inst):
        with open(services._file_path) as p:
            names_list = json.load(p)
            try:
                del names_list[0]['file']
            except:
                pass
            with open(services._file_path, 'w') as outfile:
                json.dump(names_list, outfile, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
