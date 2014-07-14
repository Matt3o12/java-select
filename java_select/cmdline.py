import sys
import optparse
import pdb

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
        else:
            raise optparse.OptionValueError("Invalid argument: {0}".format(args[0]))

    def showVersion(self):
        # TODO: Display correct version
        # TODO: also display current Java version.
        print "Version: 0.0 (dev)"


def main(args = None):
    if args is None:
        args = sys.argv[1:]

    JavaSelectScript(args).run()

if __name__ == "__main__":
    main()