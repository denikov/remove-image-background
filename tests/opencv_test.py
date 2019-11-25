'''
TESTING OPENCV MODULE
'''

# set the path to the project directory
import sys
import os
testdir = os.path.dirname(__file__)
srcdir = '../remove-image-background'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import opencv
from mock import patch
import pytest

ocv = opencv.OpenCV()

def test_createHash():
    hashed = ocv.createHash('hello world')
    assert hashed is not None
    assert len(hashed) == 36


@pytest.mark.parametrize("href, boolean",
    [('https://images.complex.com/complex/images/c_limit,dpr_auto,q_90,w_720/fl_lossy,pg_1/yko62ikk9rkjsjzzjwdc/keanu-reeves', True),
     ('https://www.phillymag.com/wp-content/uploads/sites/3/2018/11/gritty-time-magazine-person-of-the-year.jpg', False),
     ('https://images.news18.com/optimize/6sHKLG-piQvj9JL5vJ8w25YhGV0=/342x227/images.news18.com/ibnlive/uploads/342x227/jpg/2018/12/Mark-Zuckerberg.jpg', True)])
def test_checkForFaces(href, boolean):
    assert (ocv.checkForFaces(href) is not None) == boolean


@patch('services.getLastImage')
@patch.object(opencv.OpenCV, 'createHash')
@patch.object(opencv.OpenCV, 'saveCropped')
@pytest.mark.parametrize("img_path, hashed",
                         [('./tests/test_images/test_image_1.png', 'kwel29394ignn2o290923rinkwlvn.png'),
                          ('./tests/test_images/test_image_2.png', '233f29394ignn2o290923rinkwlvn.png')])

def test_processDownloadedImage(mock_save, mock_hash, mock_lastimage, img_path, hashed):
    mock_lastimage.return_value = img_path
    mock_hash.return_value = hashed
    mock_save.return_value = None
    fileName = ocv.processDownloadedImage(None)
    assert fileName is not None
