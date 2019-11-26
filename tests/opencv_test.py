'''
TESTING OPENCV MODULE
'''

# set the path to the project directory
import sys
import os
testdir = os.path.dirname(__file__)
srcdir = '../remove-image-background'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from unittest.mock import patch
import opencv


class OpencvTest(unittest.TestCase):

    @classmethod
    def setUpClass(inst):
        inst.ocv = opencv.OpenCV()



    def test_createHash(self):
        hashed = self.ocv.createHash('hello world')
        self.assertIsNotNone(hashed)
        self.assertEqual(len(hashed), 36)



    def test_checkForFaces(self):
        hrefs = (('https://images.complex.com/complex/images/c_limit,dpr_auto,q_90,w_720/fl_lossy,pg_1/yko62ikk9rkjsjzzjwdc/keanu-reeves', True),
         ('https://www.phillymag.com/wp-content/uploads/sites/3/2018/11/gritty-time-magazine-person-of-the-year.jpg', False),
         ('https://images.news18.com/optimize/6sHKLG-piQvj9JL5vJ8w25YhGV0=/342x227/images.news18.com/ibnlive/uploads/342x227/jpg/2018/12/Mark-Zuckerberg.jpg', True))
        for href, boolean in hrefs:
            with self.subTest(href):
                self.assertEqual((self.ocv.checkForFaces(href) is not None), boolean)



    @patch('services.getLastImage')
    @patch.object(opencv.OpenCV, 'createHash')
    @patch.object(opencv.OpenCV, 'saveCropped')

    def test_processDownloadedImage(self, mock_save, mock_hash, mock_lastimage):
        data = (('./tests/test_images/test_image_1.png', 'kwel29394ignn2o290923rinkwlvn.png'),
                ('./tests/test_images/test_image_2.png', '233f29394ignn2o290923rinkwlvn.png'))
        for img_path, hashed in data:
            with self.subTest(hashed):
                mock_lastimage.return_value = img_path
                mock_hash.return_value = hashed
                mock_save.return_value = None
                fileName = self.ocv.processDownloadedImage(None)
                self.assertIsNotNone(fileName)



if __name__ == '__main__':
    unittest.main(verbosity=2)
