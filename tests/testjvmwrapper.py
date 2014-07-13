import unittest
import json
import mock

from java_select.jvmwrapper import *

from nose_parameterized import parameterized, param

class JVMWrapperTest(unittest.TestCase):
    jvm_homes_path = os.path.join("tests", "jvm_homes_test.json")

    def assertRaisesInvalidVersionException(self, version):
        e = InvalidVersionFormatException
        self.assertRaises(e, JVMWrapper.getVersionByString, version)

    def setUp(self):
        self.jvm1 = JVMWrapper(
            version=(1, 6, 0, 34),
            path="/sdf"
        )

        self.jvm2 = JVMWrapper(
            version=(1, 8, 0, 1),
            path="/home/matt3o12/jvm1.8.0_01/Contents/Home"
        )

    def testGetName(self):
        self.assertEquals("Java 1.6.0_34 at /sdf", self.jvm1.name)

        name = "Java 1.8.0_01 at /home/matt3o12/jvm1.8.0_01/Contents/Home"
        self.assertEquals(name, self.jvm2.name)

    def testGetVersion(self):
        self.assertEquals((1,6,0,34), self.jvm1.version)
        self.assertEquals("1.6.0_34", self.jvm1.version_verbose)

        self.assertEquals((1,8,0,1), self.jvm2.version)
        self.assertEquals("1.8.0_01", self.jvm2.version_verbose)

    def testGetVersionByString(self):
        self.assertEquals((1,5,0,1), JVMWrapper.getVersionByString("1.5.0_01"))
        self.assertEquals((1,8,0,20), JVMWrapper.getVersionByString("1.8.0_20"))
        self.assertEquals((1,7,2,5), JVMWrapper.getVersionByString("1.7.2_5-b13"))
        self.assertEquals((1,11,2,5), JVMWrapper.getVersionByString("1.11.2_5-b13"))

    def testGetVersionByString_invalid(self):
        args = (InvalidVersionFormatException, JVMWrapper.getVersionByString)
        self.assertRaisesInvalidVersionException("2.5.0_01")
        self.assertRaisesInvalidVersionException("1.7.2")
        self.assertRaisesInvalidVersionException("blah")
        self.assertRaisesInvalidVersionException("1.b.3")
        self.assertRaisesInvalidVersionException("test 1.5.0_01")
        self.assertRaisesInvalidVersionException("1.5.0_01 test")

    def testGetVersionByString_nonstrict(self):
        version = lambda v: JVMWrapper.getVersionByString(v, strict=False)
        self.assertEquals((1,5,0,1), version("1.5.0_01"))
        self.assertEquals((1,11,2,5), version("1.11.2_5-b13"))
        self.assertEquals((1,5,0,1), version("test 1.5.0_01"))
        self.assertEquals((1,5,0,1), version("1.5.0_01 test"))

    def testSetVersion(self):
        self.jvm2.version = (1,3,0,3)
        self.assertEquals((1,3,0,3), self.jvm2.version)
        self.assertEquals("1.3.0_03", self.jvm2.version_verbose)

        e = InvalidVersionFormatException
        self.assertRaises(e, setattr, self.jvm2, "version", (1,))
        self.assertRaises(e, setattr, self.jvm2, "version", (1,3))
        self.assertRaises(e, setattr, self.jvm2, "version", (1,3,3))
        self.assertRaises(e, setattr, self.jvm2, "version", (2,0,0,1))

    def testSetVersionStr(self):
        self.jvm2.version = "1.5.0_04"
        self.assertEquals((1,5,0,4), self.jvm2.version)
        self.assertEquals("1.5.0_04", self.jvm2.version_verbose)

        e = InvalidVersionFormatException
        self.assertRaises(e, setattr, self.jvm2, "version", "1")
        self.assertRaises(e, setattr, self.jvm2, "version", "1.3")
        self.assertRaises(e, setattr, self.jvm2, "version", "1.3.3")
        self.assertRaises(e, setattr, self.jvm2, "version", "2.0.0_01")

    def testRepl(self):
        self.assertEquals("JVMWrapper(version='1.6.0_34', path='/sdf')", repr(self.jvm1))
        s = "JVMWrapper(version='1.8.0_01', path='/home/matt3o12/" \
                "jvm1.8.0_01/Contents/Home')"
        self.assertEquals(s, repr(self.jvm2))

    def testStr(self):
        self.assertEquals("Java 1.6.0_34 at /sdf", str(self.jvm1))
        s = "Java 1.8.0_01 at /home/matt3o12/jvm1.8.0_01/Contents/Home"
        self.assertEquals(s, str(self.jvm2))

    def test(self):
        json.load(open(self.jvm_homes_path, "r"))

    @parameterized.expand(json.load(open(jvm_homes_path, "r")))
    def testGetJVMByPath(self, path, version, cmdOut):
        version = tuple(version)

        with mock.patch("subprocess.Popen") as PopenMock:
            PopenMock().configure_mock(returncode = 0)
            PopenMock().communicate.return_value = (cmdOut, None)

            jvm = JVMWrapper.getJVMByPath(path)
            self.assertEquals(path, jvm.path)
            self.assertEquals(version, jvm.version)

    @parameterized.expand((c, ) for c in [1,-1,20,12])
    def testGetJVMByPath_nonZeroReturnCode(self, code):
        with mock.patch("subprocess.Popen") as PopenMock:
            PopenMock().configure_mock(returncode=code)
            PopenMock().communicate.return_value = (None, None)

            e = InvalidJavaCommandException
            self.assertRaises(e, JVMWrapper.getJVMByPath, "/test")


class InvalidVersionFormatExceptionTest(unittest.TestCase):
    def testInit(self):
        e = InvalidVersionFormatException
        self.assertEquals("Test Message", str(e(msg = "Test Message")))

        s = "Java version '1.6.3_02' is not a valid Java Version"
        self.assertEquals(s, str(e(version="1.6.3_02")))

    def testInitKeyError(self):
        self.assertRaises(ValueError, InvalidVersionFormatException)

    def testRepr(self):
        e = InvalidVersionFormatException(version="1.6.3_02")
        s = "InvalidVersionFormatException(msg='"\
                "Java version '1.6.3_02' is not a valid Java Version')"

        self.assertEquals(s, repr(e))

class InvalidJavaCommandExceptionTest(unittest.TestCase):
    def testInit(self):
        e = InvalidJavaCommandException
        self.assertEquals("Test Message", str(e(msg = "Test Message")))

        s = "'/test/java' is not a valid Java command."
        self.assertEquals(s, str(e(command="/test/java")))

    def testInitKeyError(self):
        self.assertRaises(ValueError, InvalidJavaCommandException)

    def testRepr(self):
        e = InvalidVersionFormatException(version="1.6.3_02")
        s = "InvalidVersionFormatException(msg='"\
                "Java version '1.6.3_02' is not a valid Java Version')"

        self.assertEquals(s, repr(e))
