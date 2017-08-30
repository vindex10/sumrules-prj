from getopt import getopt, GetoptError
from sys import argv

from ConfigManager import ConfigManager

class BasicTest(object):
    def __init__(self, title="unnamed"):
        self.title = title
        self.configPath = title+".conf"
        self.config = ConfigManager()
        self.config.register(self, "TEST")
        self.interactive = False
        self.outputPath = "output/%s" % title
        self._keylist = ["title"
                        ,"interactive"
                        ,"outputPath"
                        ,"configPath"]
        self.parseCmd()

    def parseCmd(self):
        try:
            opts, args = getopt(argv[1:], "c:", ["config="])
        except GetoptError:
            return False
        for opt, arg in opts:
            if opt in ("-c", "--config"):
                self.params({"configPath": arg})
        return True

    def params(self, paramdict=None):
        if paramdict is None:
            return {k: getattr(self, k) for k in self._keylist}

        for key, val in paramdict.items():
            if key in self._keylist:
                setattr(self, key, val)
        return True

    def iwrite(self, f, data):
        if self.interactive:
            print(data)
        f.write(data+"\n")

    def __repr__(self):
        res = "Test title: %s\n" % self.title
        res += "Test params:\n"
        for k,v in self.params():
            res += k+": "+v+"\n"
        return res

    def run(self):
        with open(self.outputPath+"/params", "a") as f:
            for entry, val in self.config:
                    self.iwrite(f, "%s=%s" % (entry, str(val)))
        
