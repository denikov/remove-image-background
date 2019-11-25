'''
TESTING SERVICES MODULE
'''

# set the path to the project directory
import sys
import os
testdir = os.path.dirname(__file__)
srcdir = '../remove-image-background'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import services
import json
from mock import patch


def test_loadList():
# pass test file to services module
    services._file_path = 'tests/sample.json'

# testing the initial values
    assert services._name_list == []
    assert services._current_index == 0

# returning the first value from the file
    firstName = services.loadList()
    assert firstName == 'alecia keys'



def test_addToJSON():
    with patch('services.removeFromTemp', return_value = None):
        returnedName = services.addToJSON('test.png')
        assert services._name_list[0]['file'] == 'test.png'
        assert services._current_index == 1
        assert returnedName == 'Kobe byrant'



def test_checkAllFound():
    services._current_index = 3
    assert services.checkAllFound() == 'mark walburg'
    services._current_index = 4
    assert services.checkAllFound() == None



# remove any modifications to the sample.json file
def teardown_module(module):
    with open(services._file_path) as p:
        names_list = json.load(p)
        del names_list[0]['file']
        with open(services._file_path, 'w') as outfile:
            json.dump(names_list, outfile, ensure_ascii=False, indent=2)
