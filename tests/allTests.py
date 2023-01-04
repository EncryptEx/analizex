import unittest
from click.testing import CliRunner
import sys
import os
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","src")
sys.path.append(path)
import coreAnalizer
import analizer

# run this file in root of repo

class Tests(unittest.TestCase):

	# check if Debug variable is false
	def test_checkDebug(self):
		self.assertTrue(not analizer.debug)

	# check for modes
	def test_checkTop(self):
		# -1 As top shouldn't be allowed
		runner = CliRunner()
		result = runner.invoke(analizer.analize, "test.txt --top -1".split())
		self.assertEqual(2, result.exit_code, "Didn't throw an error with -1 as top")
		runner2 = CliRunner()
		result2 = runner2.invoke(analizer.analize, "test.txt --top 2".split())
		self.assertEqual(0, result2.exit_code, "Did throw an error with 2 as top")

	def test_checkModes(self):
		# hello world are modes that shouldn't be allowed
		runner = CliRunner()
		result = runner.invoke(analizer.analize, "test.txt --modes hello,world".split())
		self.assertEqual(2, result.exit_code, "Didn't throw an error 2 with unknown modes")
		# all is a mode that should be allowed
		runner2 = CliRunner()
		result2 = runner2.invoke(analizer.analize, "test.txt --categories all".split())
		self.assertEqual(0, result2.exit_code, "Did throw an error where it shouldn't with known modes")

	def test_checkOutput(self):
		# check for an output not valid
		runner = CliRunner()
		result = runner.invoke(analizer.analize, "test.txt --output hello".split())
		self.assertEqual(2, result.exit_code, "Didn't throw an error 2 with unknown output type")
		# check for an output valid
		runner2 = CliRunner()
		result2 = runner2.invoke(analizer.analize, "test.txt --output html".split())
		self.assertEqual(0, result2.exit_code, "Did throw an error with known output type")
	
	def test_checkGeoLoc(self):
		# check for an geoloc invalid
		runner = CliRunner()
		result = runner.invoke(analizer.analize, "test.txt --ipgeoloc html".split())
		self.assertEqual(2, result.exit_code, "Didn't throw an error 2 with invalid ipgeoloc value")
		# check for an geoloc valid
		runner2 = CliRunner()
		result2 = runner2.invoke(analizer.analize, "test.txt --ipgeoloc false".split())
		self.assertEqual(0, result2.exit_code, "Did throw an error with valid ipgeoloc value")
	
	def test_checkReqTreshold(self):
		# check for an ReqTreshold invalid
		runner = CliRunner()
		result = runner.invoke(analizer.analize, "test.txt --reqtreshold false".split())
		self.assertEqual(2, result.exit_code, "Didn't throw an error 2 with invalid ReqTreshold value")
		# check for an ReqTreshold valid
		runner2 = CliRunner()
		result2 = runner2.invoke(analizer.analize, "test.txt --reqtreshold 1".split())
		self.assertEqual(0, result2.exit_code, "Did throw an error with valid ReqTreshold value")

if __name__ == '__main__':
	unittest.main()
