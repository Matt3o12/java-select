import unittest
from java_select.cmdline import *
from nose_parameterized import parameterized

from mock import *
from StringIO import StringIO

class TestJavaSelectOptionParser(unittest.TestCase):
    def setUp(self):
        self.parser = JavaSelectOptionParser()

    def testInit(self):
        self.assertEquals("%prog command [options]", self.parser.usage)

class TestJavaSelectScript(unittest.TestCase):
    def setUp(self):
        self.script = JavaSelectScript([])

    @patch("sys.stdout", new_callable=StringIO)
    def testShowVersion(self, stdout):
        # TODO: make this more dynamic
        self.script.showVersion()
        self.assertEquals("Version: 0.0 (dev)\n", stdout.getvalue())

    def testRun_version(self):
        self.script.showVersion = MagicMock(name="showVersion")
        self.script.args = ['-v']
        self.script.run()
        self.script.showVersion.assert_called_once_with

    @parameterized.expand([
        [],
        ["arg1", "arg2"],
        ["arg1", "arg2", "arg3"]

    ])
    def testRun_help(self, *args):
        error = MagicMock("error")
        self.script.optParser.error = error
        self.script.args = list(args)
        self.script.run()
        self.assertEquals(1, error.call_count)
        self.assertEquals(1, len(error.call_args[0]))
        self.assertTrue(isinstance(error.call_args[0][0], basestring))

    def testRun_invalidArgument(self):
        self.script.args = ["Invalid_arg"]
        self.assertRaises(optparse.OptionValueError, self.script.run)

class TestLocalFunction(unittest.TestCase):
    @patch("java_select.cmdline.JavaSelectScript")
    @patch("sys.argv", ["script", "test", "args"])
    def testMain_noArgs(self, JavaSelectScriptMock):
        main()
        JavaSelectScriptMock.assert_called_once_with(["test", "args"])

    @patch("java_select.cmdline.JavaSelectScript")
    def testMain(self, JavaSelectScriptMock):
        args = ["hello", "world"]
        main(args)
        JavaSelectScriptMock.assert_called_once_with(["hello", "world"])
