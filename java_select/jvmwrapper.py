import re

class InvalidVersionFormatException(Exception):
    def __init__(self, msg = None, version = None, *args, **kwargs):
        if msg is None and version is None:
            raise ValueError("Either msg or version needs to be given.")

        if msg is None:
            msg = "Java version '{}' is not a valid Java Version".format(version)

        super(InvalidVersionFormatException, self).__init__(msg, *args, **kwargs)

    def __repr__(self):
        return "{self.__class__.__name__}(msg='{self.message}')".format(self=self)

class JVMWrapper(object):
    """
    Contains information about a JVM (the path, version, etc).
    """

    _version_regex = r"^1\.([0-9]{1,2})\.([0-9]{1,2})_([0-9]{1,3})(-[0-9a-zA-Z]+)?$"

    def __init__(self, path = None, version = None):
        self._version = None

        self.path = path
        self.version = version

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        if isinstance(version, basestring):
            version = self.getVersionByString(version)

        if not len(version) == 4:
            raise InvalidVersionFormatException(version=version)

        if version[0] != 1:
            raise InvalidVersionFormatException(version=version)

        self._version = version

    @property
    def version_verbose(self):
        return "{v[0]}.{v[1]}.{v[2]}_{v[3]:02}".format(v=self.version)

    @property
    def name(self):
        return "Java {self.version_verbose} at {self.path}".format(self=self)

    def __str__(self):
        return self.name

    def __repr__(self):
        str = "{self.__class__.__name__}(version='{self.version_verbose}', path='{self.path}')"
        return str.format(self=self)

    @classmethod
    def getVersionByString(cls, version):
        match = re.match(cls._version_regex, version)
        if match:
            # Names according to:
            # http://www.oracle.com/technetwork/java/javase/versioning-naming-139433.html

            feature = int(match.group(1))
            maintenance = int(match.group(2))
            update = int(match.group(3))

            return (1, feature, maintenance, update)
        else:
            raise InvalidVersionFormatException(version = version)


    # @classmethod
    # def getJVMByPath(cls, path):
    #     pass