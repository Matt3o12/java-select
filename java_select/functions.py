import os
from jvmwrapper import JVMWrapper, InvalidJavaException

def getCurrentJVM():
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


def setCurrentJVM(newJvm):
    if not isinstance(newJvm, JVMWrapper):
        raise KeyError("{0} needs to be an instance of JVMWrapper".format(newJvm))

    os.environ["JAVA_HOME"] = newJvm.path

