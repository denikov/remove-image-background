'''
TESTING APP MODULE
'''

# set the path to the project directory
import sys
import os
testdir = os.path.dirname(__file__)
srcdir = '../remove-image-background'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))


import app
from mock import patch
import pytest



@patch('app.App.__init__')
@pytest.mark.parametrize("arg1, arg2, boolean",
    [('python', 'tests/sample.json', True),
     ('python', 'tests/example.csv', False),
     ('python', '../tests/sample.json', False)])
def test_validateFile(mock_init, arg1, arg2, boolean):
# mock sys.argv parameters
    with patch.object(sys, 'argv', [arg1, arg2]):
        mock_init.return_value = None
        _app = app.App()
        _validated = _app.validateFile()
        assert (_validated is None) == boolean



@patch('app.App.validateFile')
@patch('app.App.startSearch')
@patch('app.App.__init__')
def test_run(mock_init, mock_startSearch, mock_validateFile):
    mock_init.return_value = None
    mock_validateFile.return_value = None
    _app = app.App()
    _app.run()
    assert _app.validateFile.called
    assert _app.startSearch.called
    assert os.path.isdir('./remove-image-background/downloads')
    assert os.path.isdir('./remove-image-background/temp')
