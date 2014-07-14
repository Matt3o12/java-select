import os
from jvmwrapper import JVMWrapper, InvalidJavaException

def _getCurrentJVM():
    # TODO: Add logging
    if not "JAVA_HOME" in os.environ:
        return None

    javaHome = os.environ["JAVA_HOME"]
    jvm = None
    try:
        jvm = JVMWrapper.getJVMByPath(javaHome)
    except InvalidJavaException:
        return None

    return jvm


currentJVM = property(_getCurrentJVM())
