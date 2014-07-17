import sys
import optparse
import functions

class JavaSelectOptionParser(optparse.OptionParser, object):
    def __init__(self):
        super(JavaSelectOptionParser, self).__init__("%prog command [options]")
        self.add_option("-v", "--version", action="store_true")

class JavaSelectScript(object):
    def __init__(self, args):
        self.args = args
        self.optParser = JavaSelectOptionParser()

    def run(self):
        options, args = self.optParser.parse_args(self.args)

        if options.version:
            self.showVersion()
        elif len(args) != 1:
            self.optParser.error("Changes the Java Home. Use 'java-select help' for help")
        elif "show" in args:
            self.showCurrentJVM()
        else:
            raise optparse.OptionValueError("Invalid argument: {0}".format(args[0]))

    def showVersion(self):
        # TODO: Display correct version
        # TODO: also display current Java version.
        print "Version: 0.0 (dev)"

    def showCurrentJVM(self):
        jvm = functions.getCurrentJVM()
        if not jvm:
            print "No Java version could be found."
            print "Use 'java-select change' to change Java."
        else:
            print "Java {version} at {path}".format(version=jvm.version_verbose, path=jvm.path)



def main(args = None):
    if args is None:
        args = sys.argv[1:]

    JavaSelectScript(args).run()

if __name__ == "__main__":
    main()