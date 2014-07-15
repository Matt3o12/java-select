import unittest
from java_select.functions import _getCurrentJVM
from java_select.jvmwrapper import InvalidJavaException

from mock import *
import os

class TestFunctionTestCase(unittest.TestCase):
    @patch.dict(os.environ, {"JAVA_HOME": ""})
    def testGetCurrentJVM_noJavaHome(self):
        del os.environ["JAVA_HOME"]
        self.assertTrue(_getCurrentJVM() is None)

    @patch.dict(os.environ, {"JAVA_HOME": "/invalid/java/home"})
    @patch("java_select.jvmwrapper.JVMWrapper.getJVMByPath")
    def testGetCurrentJVM_invalidHome(self, getJVMByPathMock):
        getJVMByPathMock.side_effect = InvalidJavaException()
        self.assertTrue(_getCurrentJVM() is None)
        getJVMByPathMock.assert_called_once_with("/invalid/java/home")

    @patch.dict(os.environ, {"JAVA_HOME": "/path/to/java/home"})
    @patch("java_select.jvmwrapper.JVMWrapper.getJVMByPath")
    def testGetCurrentJVM(self, getJVMByPathMock):
        JVMWrapperMock = Mock("JVMWrapper")
        getJVMByPathMock.return_value = JVMWrapperMock

        currentJVM = _getCurrentJVM()
        getJVMByPathMock.assert_called_once_with("/path/to/java/home")
        self.assertEquals(JVMWrapperMock, currentJVM)

