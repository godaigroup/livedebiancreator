import logging, os, shutil
from optparse import OptionParser

from buildercore import *
from prefs import *

class ldc_cli:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        console = logging.StreamHandler()
        self.log.addHandler(console)

    def checkOptions(self):
        usage = "usage: %prog -i [name]"
        version = ldc_cli_version + " by Garrett Gee"
        parser = OptionParser(usage=usage,version=version)
        parser.add_option("-p", dest="projectfile", help="project file")

        parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="")
        parser.add_option("-d", "--debug", action="store_true", dest="debug", help="")

        (options, args) = parser.parse_args()

        if not options.projectfile:
            parser.print_help()
            sys.exit()

        self.builder.projectfile = options.projectfile

        if options.debug:
            self.log.setLevel(logging.DEBUG)
        elif options.verbose:
            self.log.setLevel(logging.INFO)
        else:
            self.log.setLevel(logging.WARNING)

    def test(self):
        self.builder = buildercore(self.log)

        self.checkOptions()

        self.builder.readProject()
        print self.builder.projectinstall
        print type(self.builder.projectinstall)
        self.builder.installfiles = []
        for item in self.builder.projectinstall.split(','):
            self.builder.installfiles.append(item)
        print self.builder.installfiles
        print type(self.builder.installfiles)


    def run(self):
        self.builder = buildercore(self.log)

        self.checkOptions()

        self.builder.readProject()
        self.builder.distfullname = self.builder.projectdistfullname
        self.builder.distshortname = self.builder.projectdistshortname
        self.builder.distver = self.builder.projectdistver
        self.builder.distbranch = self.builder.projectbranch
        self.builder.distplatform = self.builder.projectplatform
        self.builder.distrepo = self.builder.projectrepo
        self.builder.distrepofile = self.builder.projectrepofile

        # stage 0 create basic dir setup
        self.builder.stage0setpaths()
        if os.path.exists(self.builder.livefspath):
            self.builder.stage0deletelivefspath()
            self.builder.stage0createlivefspath()
        else:
            self.builder.stage0createlivefspath()
        if os.path.exists(self.builder.liveisopath):
            self.builder.stage0deleteliveisopath()
            self.builder.stage0createliveisopath()
        else:
            self.builder.stage0createliveisopath()

        # stage 1 debootstrap
        self.builder.stage1createbasefrombootstrap()

        # stage 2 chroot
        self.builder.chrootcmdinitialsetup()
        self.builder.installfiles = []
        for item in self.builder.projectinstall.split(','):
            if os.path.isfile(self.builder.custominstalldir + item):
                self.builder.installfiles.append(item)
        self.builder.stage2packages()
        self.builder.scriptsinchrootfiles = []
        for item in self.builder.projectscriptsinchroot.split(','):
            if os.path.isfile(self.builder.customscriptsinsidedir + item):
                self.builder.scriptsinchrootfiles.append(item)
        self.builder.stage2scripts()
        self.builder.chrootcmdclose()
        self.builder.chrootcmdwrite()
        self.builder.chrootactionbuild()

        # stage 3 iso prep and other
        self.builder.stage3isofolders()
        if os.path.exists(self.builder.liveisopathlive):
            self.builder.stage3deleteisopathlive()
            self.builder.stage3createisopathlive()
        else:
            self.builder.stage3createisopathlive()

        if os.path.exists(self.builder.liveisopathisolinux):
            self.builder.stage3deleteisopathisolinux()
            self.builder.stage3createisopathisolinux()
        else:
            self.builder.stage3createisopathisolinux()
        self.builder.stage3files()
        self.builder.stage3cmdoutsideinit()
        self.builder.scriptsoutchrootfiles = []
        for item in self.builder.projectscriptsoutchroot.split(','):
            if os.path.isfile(self.builder.customscriptsoutsidedir + item):
                self.builder.scriptsoutchrootfiles.append(item)
        self.builder.stage3cmdoutsidescripts()
        self.builder.stage3cmdoutsidewrite()
        self.builder.stage3cmdoutsiderun()
        if os.path.isfile(self.builder.squashfsfile):
            os.remove(self.builder.squashfsfile)
            self.builder.squashfilesystem()
        else:
            self.builder.squashfilesystem()

        # stage 4 make iso
        self.builder.stage4createiso()

        self.log.warning('[ ] done')


if __name__ == '__main__':
    app = ldc_cli()
    app.run()
    #app.test()