'''
TESTING APP MODULE
'''

# set the path to the project directory
import sys
import os
testdir = os.path.dirname(__file__)
srcdir = '../remove-image-background'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))


import unittest
from unittest.mock import patch
import app


class AppTest(unittest.TestCase):

    @classmethod
    @patch('app.App.__init__')
    def setUpClass(inst, mock_init):
        mock_init.return_value = None
        inst.app = app.App()



    def test_validateFile(self):
        data = (('python', 'tests/sample.json', True),
                ('python', 'tests/example.csv', False),
                ('python', '../tests/sample.json', False))

        for arg1, arg2, boolean in data:
            with self.subTest(arg2):
# mock sys.argv parameters
                with patch.object(sys, 'argv', [arg1, arg2]):
                    validated = self.app.validateFile()
                    self.assertEqual((validated is None), boolean)



    @patch('app.App.validateFile')
    @patch('app.App.startSearch')
    def test_run(self, mock_startSearch, mock_validateFile):
        mock_validateFile.return_value = None
        self.app.run()
        self.assertTrue(mock_validateFile.called)
        self.assertTrue(mock_startSearch.called)
        self.assertTrue(os.path.isdir('./remove-image-background/downloads'))
        self.assertTrue(os.path.isdir('./remove-image-background/temp'))



if __name__ == '__main__':
    unittest.main(verbosity=2)
