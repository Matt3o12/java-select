import unittest
from java_select.functions import _getCurrentJVM, _setCurrentJVM
from java_select.jvmwrapper import InvalidJavaException, JVMWrapper

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

    # just path the dict in case this test fails and changes the
    # environment.
    @patch.dict(os.environ)
    def testSetCurrentJVM_raises(self):
        self.assertRaises(KeyError, _setCurrentJVM, "Some string")
        self.assertRaises(KeyError, _setCurrentJVM, None)

    @patch.dict(os.environ, {"JAVA_HOME": ""})
    def testSetCurrentJVM_noJavaHome(self):
        del os.environ["JAVA_HOME"]
        wrapper = Mock(JVMWrapper)
        wrapper.configure_mock(path="/test/java/home")

        _setCurrentJVM(wrapper)
        self.assertEquals("/test/java/home", os.environ["JAVA_HOME"])

    @patch.dict(os.environ, {"JAVA_HOME": "/old/java/home"})
    def testSetCurrentJVM(self):
        wrapper = Mock(JVMWrapper)
        wrapper.configure_mock(path="/new/java/home")

        self.assertEquals("/old/java/home", os.environ["JAVA_HOME"])
        _setCurrentJVM(wrapper)
        self.assertEquals("/new/java/home", os.environ["JAVA_HOME"])