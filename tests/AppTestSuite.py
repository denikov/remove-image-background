import unittest
import xmlrunner

from app_test import AppTest
from opencv_test import OpencvTest
from services_test import ServicesTest


app_tests = unittest.TestLoader().loadTestsFromTestCase(AppTest)
opencv_tests = unittest.TestLoader().loadTestsFromTestCase(OpencvTest)
services_tests = unittest.TestLoader().loadTestsFromTestCase(ServicesTest)

test_suite = unittest.TestSuite([app_tests, opencv_tests, services_tests])

#unittest.TextTestRunner(verbosity=2).run(test_suite)
xmlrunner.XMLTestRunner(output='/Users/denikov/.jenkins/workspace/Remove-Image-Background-local/test-reports').run(test_suite)
