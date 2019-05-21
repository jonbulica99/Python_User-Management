import unittest
from utils.constants import os, ROOT_DIR

loader = unittest.TestLoader()
# run all tests in the unittests directory
suite = loader.discover(os.path.join(ROOT_DIR, 'unittests'))
runner = unittest.TextTestRunner()
runner.run(suite)
