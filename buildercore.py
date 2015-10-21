#import datetime, random, re, string, sys, time
import ConfigParser, shutil, subprocess

import logging, os
from optparse import OptionParser

from prefs import *

class buildercore:
    def __init__(self, log):
        self.log = log

        self.curpath = os.path.dirname(os.path.abspath(__file__))
        customdir = "customization"
        self.custominstalldir = self.curpath + slash + customdir + slash + "install" + slash
        self.customscriptsinsidedir = self.curpath + slash + customdir + slash + "livefs-scripts-inside" + slash
        self.customscriptsoutsidedir = self.curpath + slash + customdir + slash + "scripts-outside" + slash
        self.customprojectsdir = self.curpath + slash + customdir + slash + "projects" + slash
        self.customextrasdir = self.curpath + slash + customdir + slash + "extras" + slash

        self.builderpath = self.curpath + slash
        self.livefs = self.curpath + slash + "livefs" + slash
        self.liveiso = self.curpath + slash + "liveiso" + slash
        self.isopath = self.curpath + slash + "iso" + slash

    def readProject(self):
        config = ConfigParser.ConfigParser()
        config.read(self.projectfile)

        def ReadOption(section, option, default, i, include):
            if config.has_section(section):
                if config.has_option(section, option):
                    if (i):
                        var = int(config.get(section, option))
                    else:
                        var = config.get(section, option)
                else:
                    var = default
                    if (include):
                        config.set(section, option, var)
            else:
                var = default
                config.add_section(section)
                if (include):
                    config.set(section, option, var)
            return var

        self.projectdistfullname = ReadOption("settings", "distfullname", "DIST FULL NAME", 0, 1)
        self.projectdistshortname = ReadOption("settings", "distshortname", "SHORTNAME", 0, 1)
        self.projectdistver = ReadOption("settings", "distver", "1", 0, 1)
        self.projectbranch = ReadOption("settings", "branch", "wheezy", 0, 1)
        self.projectplatform = ReadOption("settings", "platform", "amd64", 0, 1)
        self.projectrepo = ReadOption("settings", "repo", "http://ftp.us.debian.org/debian/", 0, 1)
        self.projectrepofile = ReadOption("settings", "repofile", "/etc/apt/sources.list", 0, 1)
        self.projectinstall = ReadOption("settings", "install", "", 0, 1)
        self.projectscriptsinchroot = ReadOption("settings", "scriptsinchroot", "", 0, 1)
        self.projectscriptsoutchroot = ReadOption("settings", "scriptsoutchroot", "", 0, 1)

        # if (write):
        #     file = open(self.configfile, 'w')
        #     config.write(file)
        #     file.close()

    def stage0setpaths(self):
        self.log.debug('[DEBUG] Function: stage0setpaths')

        self.buildname = self.distshortname + "-" + self.distver + "-" + self.distplatform
        self.log.debug('self.buildname: ' + self.buildname)
        self.livefspath = self.livefs + self.buildname + slash
        self.liveisopath = self.liveiso + self.buildname + slash
        self.log.debug('self.livefspath: ' + self.livefspath)
        self.log.debug('self.liveisopath: ' + self.liveisopath)

        self.chrootscript = ""
        self.outsidescript = ""

        self.squashfsfile = self.liveisopath + "live" + slash + "filesystem.squashfs"

    def stage0deletelivefspath(self):
        self.log.debug('[DEBUG] Function: stage0deletelivefspath')
        shutil.rmtree(self.livefspath)

    def stage0createlivefspath(self):
        self.log.debug('[DEBUG] Function: stage0createlivefspath')
        os.makedirs(self.livefspath)

    def stage0deleteliveisopath(self):
        self.log.debug('[DEBUG] Function: stage0deleteliveisopath')
        shutil.rmtree(self.liveisopath)

    def stage0createliveisopath(self):
        self.log.debug('[DEBUG] Function: stage0createliveisopath')
        os.makedirs(self.liveisopath)

    def stage0createisodir(self):
        self.log.debug('[DEBUG] Function: stage0createisodir')
        os.makedirs(self.isopath)

    def stage1createbasefrombootstrap(self):
        self.log.debug('[DEBUG] Function: stage1createbasefrombootstrap')
        #debootstrap
        os.chdir(self.livefs)
        #cmd = "sudo debootstrap --arch=" + self.distplatform + " " + self.distbranch + " " + self.buildname
        cmd = "debootstrap --arch=" + self.distplatform + " " + self.distbranch + " " + self.buildname + " " + self.distrepo
        self.log.debug('[DEBUG] cmd: ' + cmd)
        os.system(cmd)

        #copy apt config file
        cmd = "cp -f " + self.distrepofile + " " + self.livefspath + "etc/apt/sources.list"
        self.log.debug('[DEBUG] cmd: ' + cmd)
        os.system(cmd)

        #copy resolv.conf  file
        cmd = "cp -f /etc/resolv.conf " + self.livefspath + "etc/"
        self.log.debug('[DEBUG] cmd: ' + cmd)
        os.system(cmd)

    def chrootcmdinitialsetup(self):
        self.log.debug('[DEBUG] Function: chrootcmdinitialsetup')
        self.chrootscript += "##### chrootcmdinitialsetup #####\n"
        self.chrootscript += "mount none -t proc /proc\n"
        self.chrootscript += "mount none -t sysfs /sys\n"
        self.chrootscript += "mount none -t devpts /dev/pts\n"
        self.chrootscript += "export HOME=/root\n"
        self.chrootscript += "export LC_ALL=C\n"
        #self.chrootscript += "apt-get update\n"
        #self.chrootscript += "apt-get install --yes dbus\n"
        #self.chrootscript += "dbus-uuidgen > /var/lib/dbus/machine-id\n"
        self.chrootscript += "dpkg-divert --add --rename --local /sbin/initctl\n"
        self.chrootscript += "dpkg-divert --add --rename --local /sbin/start-stop-daemon\n"
        self.chrootscript += "echo -e '#!/bin/sh\necho 'fake start-stop-daemon - doing nothing''  | install -m 755 /dev/stdin /sbin/start-stop-daemon\n"
        self.chrootscript += "echo -e '#!/bin/sh\nexit 101' | install -m 755 /dev/stdin /usr/sbin/policy-rc.d\n"
        self.chrootscript += "apt-get update\n"
        self.chrootscript += "apt-get install --yes dbus\n"
        self.chrootscript += "dbus-uuidgen > /var/lib/dbus/machine-id\n"

        self.chrootscript += "export DEBIAN_FRONTEND=noninteractive\n"

        self.chrootscript += "echo " + self.distshortname + " > /etc/hostname\n"
        self.chrootscript += "echo -n > /etc/motd\n"

    def stage2packages(self):
        self.log.debug('[DEBUG] Function: stage2packages')
        self.chrootscript += "##### stage2packages #####\n"

        # required packages
        self.chrootscript += "apt-get install -q -y live-boot\n"
        if self.distplatform == "amd64":
            self.chrootscript += "apt-get install -q -y linux-image-" + self.distplatform + '\n'
        elif self.distplatform == "i386":
            self.chrootscript += "apt-get install -q -y linux-image-486\n"
        else:
            pass
        self.chrootscript += "apt-get install -q -y expect\n"

        # user selected package lists
        for i in self.installfiles:
            f = open(self.custominstalldir + i, 'r')
            for line in f:
                if line == "\n":
                    continue
                elif line == "\r\n":
                    continue
                else:
                    line = line.rstrip('\n')
                    line = line.rstrip('\r')
                    self.chrootscript += "apt-get install -q -y " + line + '\n'
            f.close()

    def stage2scripts(self):
        self.log.debug('[DEBUG] Function: stage2scripts')
        self.chrootscript += "##### stage2scripts #####\n"
        for i in self.scriptsinchrootfiles:
            #copy file to tmp dir
            cmd = "cp -f " + self.customscriptsinsidedir + i + " " + self.livefspath + "tmp"
            self.log.debug('[DEBUG] cmd: ' + cmd)
            os.system(cmd)
            cmd = "chmod +x " + self.livefspath + "tmp" + slash + i
            self.log.debug('[DEBUG] cmd: ' + cmd)
            os.system(cmd)
            #queue to run
            self.chrootscript += "/bin/bash /tmp/" + i + '\n'

    def chrootcmdclose(self):
        self.log.debug('[DEBUG] Function: chrootcmdclose')
        self.chrootscript += "##### chrootcmdclose #####\n"
        self.chrootscript += "rm -f /var/lib/dbus/machine-id\n"
        self.chrootscript += "rm -f /sbin/initctl /sbin/start-stop-daemon\n"
        self.chrootscript += "rm -f /usr/sbin/policy-rc.d\n"
        self.chrootscript += "dpkg-divert --remove --rename /sbin/initctl\n"
        self.chrootscript += "dpkg-divert --remove --rename /sbin/start-stop-daemon\n"
        self.chrootscript += "apt-get clean \n"
        self.chrootscript += "rm -rf /tmp/* \n"
        #self.chrootscript += "rm -f /etc/resolv.conf\n"
        self.chrootscript += "umount -lf /proc \n"
        self.chrootscript += "umount -lf /sys \n"
        self.chrootscript += "umount -lf /dev/pts\n"
        self.chrootscript += "exit\n"
        self.log.debug('[DEBUG] self.chrootscript: ' + self.chrootscript)

    def chrootcmdwrite(self):
        self.log.debug('[DEBUG] Function: chrootcmdwrite')
        f = open(self.livefspath + "tmp/build.sh", 'w')
        f.write(self.chrootscript)
        f.close()

    def chrootactionbuild(self):
        self.log.debug('[DEBUG] Function: chrootactionbuild')
        os.chdir(self.livefs)
        cmd = "chroot " + self.livefspath + " /bin/sh tmp/build.sh"
        self.log.debug('[DEBUG] cmd: ' + cmd)
        os.system(cmd)

    def stage3isofolders(self):
        self.log.debug('[DEBUG] Function: stage3isofolders')
        self.liveisopathlive = self.liveisopath + "live" + slash
        self.liveisopathisolinux = self.liveisopath + "isolinux" + slash

        self.squashfsfile = self.liveisopathlive + "filesystem.squashfs"

    def stage3createisopathlive(self):
        os.makedirs(self.liveisopathlive)

    def stage3deleteisopathlive(self):
        self.log.debug('[DEBUG] Function: stage3deleteisopathlive')
        shutil.rmtree(self.liveisopathlive)

    def stage3createisopathisolinux(self):
        os.makedirs(self.liveisopathisolinux)

    def stage3deleteisopathisolinux(self):
        self.log.debug('[DEBUG] Function: stage3deleteisopathisolinux')
        shutil.rmtree(self.liveisopathisolinux)

    def stage3cmdoutsideinit(self):
        self.log.debug('[DEBUG] Function: stage3cmdoutsideinit')
        self.outsidescript += "export BUILDERPATH=" + self.builderpath + "\n"
        self.outsidescript += "export SCRIPTSPATH=" + self.customscriptsinsidedir + "\n"
        self.outsidescript += "export LIVEFSPATH=" + self.livefspath + "\n"
        self.outsidescript += "export LIVEISOPATH=" + self.liveisopath + "\n"
        self.outsidescript += "export EXTRAPATH=" + self.customextrasdir + "\n"

    def stage3cmdoutsidescripts(self):
        self.log.debug('[DEBUG] Function: stage3cmdoutsidescripts')
        #os.chdir(self.customscriptsoutsidedir)
        for i in self.scriptsoutchrootfiles:
            self.outsidescript += "/bin/bash " + self.customscriptsoutsidedir + i + '\n'
        self.log.debug('[DEBUG] self.outsidescript: ' + self.outsidescript)

    def stage3cmdoutsidewrite(self):
        self.log.debug('[DEBUG] Function: stage3cmdoutsidewrite')
        f = open(self.customscriptsoutsidedir + "zz.sh", 'w')
        f.write(self.outsidescript)
        f.close()

    def stage3cmdoutsiderun(self):
        self.log.debug('[DEBUG] Function: stage3cmdoutsiderun')
        os.chdir(self.customscriptsoutsidedir)
        cmd = "/bin/bash zz.sh"
        self.log.debug('[DEBUG] cmd: ' + cmd)
        os.system(cmd)
        os.remove('zz.sh')

    def stage3files(self):
        self.stage3kernelinitrd()
        self.stage3isolinuxcfg()
        self.stage3isolinuxfiles()
        self.stage3preseedfile()

    def stage3kernelinitrd(self):
        self.log.debug('[DEBUG] Function: stage3kernelinitrd')
        cmd = "cp -f " + self.livefspath + "boot/initrd.img-* " + self.liveisopathlive + "initrd"
        self.log.debug('[DEBUG] cmd: ' + cmd)
        os.system(cmd)

        cmd = "cp -f " + self.livefspath + "boot/vmlinuz-* " + self.liveisopathlive + "vmlinuz"
        self.log.debug('[DEBUG] cmd: ' + cmd)
        os.system(cmd)

    def stage3isolinuxcfg(self):
        self.log.debug('[DEBUG] Function: stage3kernelinitrd')
        data = """
UI menu.c32

prompt 0
menu title Boot Menu

timeout 10

label """ + self.distshortname + " " + self.distver + """
    menu label ^""" + self.distfullname + " " + self.distver + """
    menu default
    kernel /live/vmlinuz
    append initrd=/live/initrd boot=live ip=frommedia preseed/file=/cdrom/live/preseed.cfg

label """ + self.distshortname + " " + self.distver + """ Persistent
    menu label """ + self.distfullname + " " + self.distver + """ ^Persistent
    kernel /live/vmlinuz
    append initrd=/live/initrd boot=live ip=frommedia persistence preseed/file=/cdrom/live/preseed.cfg
"""
        #append initrd=/live/initrd boot=live ip=frommedia netcfg/enable=false apt-setup/use_mirror=false passwd/make-user=false passwd/root-password=roooot passwd/root-password-again=roooot
        #append initrd=/live/initrd boot=live ip=frommedia locale=en_US keymap=us netcfg/enable=false apt-setup/use_mirror=false passwd/make-user=false passwd/root-password=roooot passwd/root-password-again=roooot

        f = open(self.liveisopathisolinux + "isolinux.cfg", 'w')
        self.log.debug('[DEBUG] isolinux.cfg: ' + data)
        f.write(data)
        f.close()

    def stage3isolinuxfiles(self):
        self.log.debug('[DEBUG] Function: stage3isolinuxfiles')
        cmd = "cp -f /usr/lib/syslinux/isolinux.bin " + self.liveisopathisolinux
        self.log.debug('[DEBUG] cmd: ' + cmd)
        os.system(cmd)
        cmd = "cp -f /usr/lib/syslinux/menu.c32 " + self.liveisopathisolinux
        self.log.debug('[DEBUG] cmd: ' + cmd)
        os.system(cmd)
        cmd = "cp -f /usr/lib/syslinux/hdt.c32 " + self.liveisopathisolinux
        self.log.debug('[DEBUG] cmd: ' + cmd)
        os.system(cmd)

    def stage3preseedfile(self):
        self.log.debug('[DEBUG] Function: stage3preseedfile')
        data = """
#this stuff doesn't work for preseed.cfg - works in boot option
#Preseeding only locale sets language, country and locale.
#d-i debian-installer/locale string en_US
# Keyboard selection.
#d-i console-keymaps-at/keymap select us

# Disable network configuration entirely - livecd has all
d-i netcfg/enable boolean false
# Apt setup - livecd has apt preconfigured and will overwrite
d-i apt-setup/use_mirror boolean false
# Root password - livecd will overwrite
d-i passwd/root-password password roooot
d-i passwd/root-password-again password roooot
# Skip creation of a normal user account - livecd will overwrite
d-i passwd/make-user boolean false
"""

        f = open(self.liveisopathlive + "preseed.cfg", 'w')
        self.log.debug('[DEBUG] preseed.cfg: ' + data)
        f.write(data)
        f.close()

    def squashfilesystem(self):
        self.log.debug('[DEBUG] Function: squashfilesystem')
        #os.chdir(self.livefs)
        cmd = "mksquashfs " + self.livefspath + " " + self.squashfsfile
        self.log.debug('[DEBUG] cmd: ' + cmd)
        os.system(cmd)

    def stage4createiso(self):
        os.chdir(self.liveisopath)
        self.iso = self.isopath + self.buildname + ".iso"
        cmd = "xorriso -as mkisofs -r -J -joliet-long -l -cache-inodes -isohybrid-mbr /usr/lib/syslinux/isohdpfx.bin -partition_offset 16 -A \"" + self.distfullname + "\" -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -o " + self.iso + " . "
        #cmd = "genisoimage -rational-rock -volid \"" + self.distfullname + "\" -cache-inodes -joliet -full-iso9660-filenames -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -output " + self.iso + " . "
        self.log.debug('[DEBUG] cmd: ' + cmd)
        os.system(cmd)

    def doAll(self):
        self.stage0setpaths()
        self.chrootcmdinitialsetup()
        # self.distfullname
        # self.distshortname
        # self.distver
        # self.distbranch
        # self.distplatform
        # self.distrepo