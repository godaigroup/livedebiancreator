import logging, os, shutil

import wx
from wx.lib.wordwrap import wordwrap

from buildercore import *
from prefs import *

class WxTextCtrlHandler(logging.Handler):
    def __init__(self, ctrl):
        logging.Handler.__init__(self)
        self.ctrl = ctrl

    def emit(self, record):
        s = self.format(record) + '\n'
        wx.CallAfter(self.ctrl.WriteText, s)

class debug_console(wx.Frame):
    def __init__(self, log):
        self.log = log
        TITLE = "Debug Console"
        wx.Frame.__init__(self, None, wx.ID_ANY, TITLE, pos = wx.DefaultPosition, size = wx.Size( 1000,300 ))
        self.SetSizeHintsSz( wx.Size( 500,300 ), wx.Size( -1,-1 ) )

        panel = wx.Panel(self, wx.ID_ANY)
        log = wx.TextCtrl(panel, wx.ID_ANY, size=(-1,-1),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(log, 1, wx.ALL|wx.EXPAND, 5)

        self.Bind( wx.EVT_CLOSE, self.debugOnClose )

        panel.SetSizer(sizer)
        self.handler = WxTextCtrlHandler(log)
        self.log.addHandler(self.handler)
        FORMAT = "%(asctime)s %(levelname)s %(message)s"
        self.handler.setFormatter(logging.Formatter(FORMAT))
        self.log.setLevel(logging.DEBUG)

    def debugOnClose( self, event ):
        self.log.setLevel(logging.WARNING)
        self.log.removeHandler(self.handler)
        self.Destroy()

class ldcFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Live Debian Creator", pos=wx.DefaultPosition,
                          size=wx.Size(980, 575), style=wx.DEFAULT_FRAME_STYLE)

        self.SetSizeHintsSz(wx.Size(980, 575), wx.DefaultSize)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.st_distfullname = wx.StaticText(self, wx.ID_ANY, u"Dist Name: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_distfullname.Wrap(-1)
        bSizer2.Add(self.st_distfullname, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.tc_distfullname = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.tc_distfullname.SetMinSize(wx.Size(150, -1))

        bSizer2.Add(self.tc_distfullname, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.st_distshortname = wx.StaticText(self, wx.ID_ANY, u"Dist Short Name: ", wx.DefaultPosition, wx.DefaultSize,
                                              0)
        self.st_distshortname.Wrap(-1)
        bSizer2.Add(self.st_distshortname, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.tc_distshortname = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.tc_distshortname.SetMinSize(wx.Size(80, -1))

        bSizer2.Add(self.tc_distshortname, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.st_distver = wx.StaticText(self, wx.ID_ANY, u"Dist Version: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_distver.Wrap(-1)
        bSizer2.Add(self.st_distver, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.tc_distver = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.tc_distver.SetMinSize(wx.Size(50, -1))

        bSizer2.Add(self.tc_distver, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        bSizer1.Add(bSizer2, 0, wx.ALL | wx.EXPAND, 5)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.st_branch = wx.StaticText(self, wx.ID_ANY, u"Branch: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_branch.Wrap(-1)
        bSizer6.Add(self.st_branch, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        bSizer6.AddSpacer(( 15, 0), 0, wx.EXPAND, 5)

        self.tc_branch = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(80, -1), 0)
        self.tc_branch.SetMinSize(wx.Size(80, -1))

        bSizer6.Add(self.tc_branch, 0, wx.ALL, 5)

        self.st_platform = wx.StaticText(self, wx.ID_ANY, u"Platform: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_platform.Wrap(-1)
        bSizer6.Add(self.st_platform, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        c_platformChoices = [u"i386", u"amd64"]
        self.c_platform = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(80, -1), c_platformChoices, 0)
        self.c_platform.SetSelection(0)
        self.c_platform.SetMinSize(wx.Size(80, -1))

        bSizer6.Add(self.c_platform, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.st_repo = wx.StaticText(self, wx.ID_ANY, u"Initial Repo URL: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_repo.Wrap(-1)
        bSizer6.Add(self.st_repo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.tc_repo = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(190, -1), 0)
        self.tc_repo.SetMinSize(wx.Size(190, -1))

        bSizer6.Add(self.tc_repo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        bSizer1.Add(bSizer6, 0, wx.ALL | wx.EXPAND, 5)

        bSizer12 = wx.BoxSizer(wx.HORIZONTAL)

        self.st_repofile = wx.StaticText(self, wx.ID_ANY, u"Repo File: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_repofile.Wrap(-1)
        bSizer12.Add(self.st_repofile, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        bSizer12.AddSpacer(( 4, 0), 0, wx.EXPAND, 5)

        self.tc_repofile = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(400, -1), 0)
        self.tc_repofile.SetMinSize(wx.Size(400, -1))

        bSizer12.Add(self.tc_repofile, 0, wx.ALL, 5)

        bSizer1.Add(bSizer12, 0, wx.ALL | wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer71 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"Install: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        bSizer71.Add(self.m_staticText6, 0, wx.ALL, 5)

        cl_installChoices = []
        self.cl_install = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(280, 300), cl_installChoices, 0)
        self.cl_install.SetMinSize(wx.Size(280, 300))

        bSizer71.Add(self.cl_install, 0, wx.ALL, 5)

        bSizer3.Add(bSizer71, 0, wx.EXPAND, 5)

        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"Run Scripts in Chroot: ", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        bSizer9.Add(self.m_staticText8, 0, wx.ALL, 5)

        cl_scriptsinchrootChoices = []
        self.cl_scriptsinchroot = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(300, 300),
                                                  cl_scriptsinchrootChoices, 0)
        self.cl_scriptsinchroot.SetMinSize(wx.Size(300, 300))

        bSizer9.Add(self.cl_scriptsinchroot, 0, wx.ALL, 5)

        bSizer3.Add(bSizer9, 0, wx.EXPAND, 5)

        bSizer11 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"Run Scripts outside Chroot: ", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)
        bSizer11.Add(self.m_staticText9, 0, wx.ALL, 5)

        cl_scriptsoutchrootChoices = []
        self.cl_scriptsoutchroot = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(300, 300),
                                                   cl_scriptsoutchrootChoices, 0)
        self.cl_scriptsoutchroot.SetMinSize(wx.Size(300, 300))

        bSizer11.Add(self.cl_scriptsoutchroot, 0, wx.ALL, 5)

        bSizer3.Add(bSizer11, 0, wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 0, wx.ALL | wx.EXPAND, 5)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.b_buildit = wx.Button(self, wx.ID_ANY, u"Build It!", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer7.Add(self.b_buildit, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        bSizer1.Add(bSizer7, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.m_menubar1 = wx.MenuBar(0)
        self.m_file = wx.Menu()
        self.m_load = wx.MenuItem(self.m_file, wx.ID_ANY, u"Load Project" + u"\t" + u"Ctrl+L", wx.EmptyString,
                                  wx.ITEM_NORMAL)
        self.m_file.AppendItem(self.m_load)

        self.m_save = wx.MenuItem(self.m_file, wx.ID_ANY, u"Save Project" + u"\t" + u"Ctrl+S", wx.EmptyString,
                                  wx.ITEM_NORMAL)
        self.m_file.AppendItem(self.m_save)

        self.m_exit = wx.MenuItem(self.m_file, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_file.AppendItem(self.m_exit)

        self.m_menubar1.Append(self.m_file, u"File")

        self.m_tools = wx.Menu()
        self.m_install = wx.MenuItem(self.m_tools, wx.ID_ANY, u"2 - Install Apps in Chroot", wx.EmptyString,
                                     wx.ITEM_NORMAL)
        self.m_tools.AppendItem(self.m_install)

        self.m_scriptsinside = wx.MenuItem(self.m_tools, wx.ID_ANY, u"2 - Run Scripts in Chroot", wx.EmptyString,
                                           wx.ITEM_NORMAL)
        self.m_tools.AppendItem(self.m_scriptsinside)

        self.m_squashfs = wx.MenuItem(self.m_tools, wx.ID_ANY, u"3 - Build SquashFS", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_tools.AppendItem(self.m_squashfs)

        self.m_buildiso = wx.MenuItem(self.m_tools, wx.ID_ANY, u"4 - Build ISO", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_tools.AppendItem(self.m_buildiso)

        self.m_qemu = wx.MenuItem(self.m_tools, wx.ID_ANY, u"5 - Qemu", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_tools.AppendItem(self.m_qemu)

        self.m_menubar1.Append(self.m_tools, u"Tools")

        self.m_help = wx.Menu()
        self.m_documentation = wx.MenuItem(self.m_help, wx.ID_ANY, u"Documentation", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_help.AppendItem(self.m_documentation)

        self.m_about = wx.MenuItem(self.m_help, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_help.AppendItem(self.m_about)

        self.m_help.AppendSeparator()

        self.m_LogWindow = wx.MenuItem(self.m_help, wx.ID_ANY, u"Debug Window", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_help.AppendItem(self.m_LogWindow)

        self.m_menubar1.Append(self.m_help, u"Help")

        self.SetMenuBar(self.m_menubar1)

        self.Centre(wx.BOTH)

        # Connect Events
        self.b_buildit.Bind(wx.EVT_BUTTON, self.onBuildIt)
        self.Bind(wx.EVT_MENU, self.onLoad, id=self.m_load.GetId())
        self.Bind(wx.EVT_MENU, self.onSave, id=self.m_save.GetId())
        self.Bind(wx.EVT_MENU, self.onExit, id=self.m_exit.GetId())
        self.Bind(wx.EVT_MENU, self.onInstall, id=self.m_install.GetId())
        self.Bind(wx.EVT_MENU, self.onScriptInside, id=self.m_scriptsinside.GetId())
        self.Bind(wx.EVT_MENU, self.onSquashFS, id=self.m_squashfs.GetId())
        self.Bind(wx.EVT_MENU, self.onBuildISO, id=self.m_buildiso.GetId())
        self.Bind(wx.EVT_MENU, self.onQemu, id=self.m_qemu.GetId())
        self.Bind(wx.EVT_MENU, self.onHelp, id=self.m_documentation.GetId())
        self.Bind(wx.EVT_MENU, self.onAbout, id=self.m_about.GetId())
        self.Bind(wx.EVT_MENU, self.onLogWindow, id=self.m_LogWindow.GetId())


        self.onInit()

    def onLoad(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a project file",defaultDir=self.builder.customprojectsdir,defaultFile="",wildcard="Project settings (*.ini)|*.ini",
            style=wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.builder.projectfile = dlg.GetPath()
            self.resetUI()
            self.builder.readProject()
            self.configUI()
        dlg.Destroy()

    def resetUI(self):
        self.tc_distfullname.SetValue("")
        self.tc_distshortname.SetValue("")
        self.tc_distver.SetValue("")
        self.tc_branch.SetValue("")
        self.c_platform.SetStringSelection("amd64")
        self.tc_repo.SetValue("")
        self.tc_repofile.SetValue("")
        for i, j in enumerate(self.installfiles):
            self.cl_install.Check(i,0)
        for i, j in enumerate(self.scriptsinchrootfiles):
            self.cl_scriptsinchroot.Check(i,0)
        for i, j in enumerate(self.scriptsoutchrootfiles):
            self.cl_scriptsoutchroot.Check(i,0)

    def configUI(self):
        self.tc_distfullname.SetValue(self.builder.projectdistfullname)
        self.tc_distshortname.SetValue(self.builder.projectdistshortname)
        self.tc_distver.SetValue(self.builder.projectdistver)
        self.tc_branch.SetValue(self.builder.projectbranch)
        self.c_platform.SetStringSelection(self.builder.projectplatform)
        self.tc_repo.SetValue(self.builder.projectrepo)
        self.tc_repofile.SetValue(self.builder.projectrepofile)

        for item in self.builder.projectinstall.split(','):
            for i, j in enumerate(self.installfiles):
                if j == item:
                    self.cl_install.Check(i)

        for item in self.builder.projectscriptsinchroot.split(','):
            for i, j in enumerate(self.scriptsinchrootfiles):
                if j == item:
                    self.cl_scriptsinchroot.Check(i)

        for item in self.builder.projectscriptsoutchroot.split(','):
            for i, j in enumerate(self.scriptsoutchrootfiles):
                if j == item:
                    self.cl_scriptsoutchroot.Check(i)

    def onSave(self, event):
        event.Skip()

    def onExit(self, event):
        #save project settings?
        self.Destroy()

    def onInstall(self, event):
        dlg = wx.MessageDialog(self, "Run package install inside chroot?", 'Run package install inside chroot?', wx.YES_NO | wx.YES_DEFAULT )
        val = dlg.ShowModal()
        if val == wx.ID_YES:
            self.getGUIstate()
            self.builder.stage0setpaths()
            self.builder.chrootcmdinitialsetup()
            self.builder.installfiles = self.cl_install.GetCheckedStrings()
            self.builder.stage2packages()
            self.builder.chrootcmdclose()
            self.builder.chrootcmdwrite()
            self.builder.chrootactionbuild()
        elif val == wx.ID_NO:
            pass
        dlg.Destroy()

    def onScriptInside(self, event):
        dlg = wx.MessageDialog(self, "Run scripts inside chroot?", 'Run scripts inside chroot?', wx.YES_NO | wx.YES_DEFAULT )
        val = dlg.ShowModal()
        if val == wx.ID_YES:
            self.getGUIstate()
            self.builder.stage0setpaths()
            self.builder.chrootcmdinitialsetup()
            self.builder.scriptsinchrootfiles = self.cl_scriptsinchroot.GetCheckedStrings()
            self.builder.stage2scripts()
            self.builder.chrootcmdclose()
            self.builder.chrootcmdwrite()
            self.builder.chrootactionbuild()
        elif val == wx.ID_NO:
            pass
        dlg.Destroy()

    def onSquashFS(self, event):
        dlg = wx.MessageDialog(self, "Build Squashfs?", 'Build Squashfs?', wx.YES_NO | wx.YES_DEFAULT )
        val = dlg.ShowModal()
        if val == wx.ID_YES:
            self.getGUIstate()
            self.builder.stage0setpaths()
            self.stage3squashfs()
        elif val == wx.ID_NO:
            pass
        dlg.Destroy()

    def onBuildISO(self, event):
        dlg = wx.MessageDialog(self, "Build ISO?", 'Build ISO?', wx.YES_NO | wx.YES_DEFAULT )
        val = dlg.ShowModal()
        if val == wx.ID_YES:
            self.getGUIstate()
            self.builder.stage0setpaths()
            self.builder.stage4createiso()
        elif val == wx.ID_NO:
            pass
        dlg.Destroy()

    def onQemu(self, event):
        self.getGUIstate()
        self.builder.stage0setpaths()

    def onHelp(self, event):
        event.Skip()

    def onAbout(self, event):
        info = wx.AboutDialogInfo()
        #info.Name = "Live Debian Creator"
        info.Version = ldc_gui_version
        info.Description = wordwrap(
            "prerequisites: debootstrap syslinux squashfs-tools xorriso \n python-wxgtk2.8 python-wxtools \n run as root"
            ,350, wx.ClientDC(self))
        #info.WebSite = ("http://en.wikipedia.org/wiki/Hello_world", "Hello World home page")
        info.Developers = [ "Garrett Gee" ]
        #info.License = wordwrap(licenseText, 500, wx.ClientDC(self))

        wx.AboutBox(info)

    def onLogWindow(self, event):
        win = debug_console(self.log).Show()

    def onInit(self):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.WARNING)
        self.log.addHandler(logging.NullHandler())

        self.builder = buildercore(self.log)

        self.installfiles = os.listdir(self.builder.custominstalldir)
        self.installfiles.sort()
        self.cl_install.Set(self.installfiles)
        self.scriptsinchrootfiles = os.listdir(self.builder.customscriptsinsidedir)
        self.scriptsinchrootfiles.sort()
        self.cl_scriptsinchroot.Set(self.scriptsinchrootfiles)
        self.scriptsoutchrootfiles = os.listdir(self.builder.customscriptsoutsidedir)
        self.scriptsoutchrootfiles.sort()
        self.cl_scriptsoutchroot.Set(self.scriptsoutchrootfiles)

##this to auto setup for testing - remove later
        self.onTest()

    def onTest(self):
        #self.onLogWindow(1)

        #self.builder.projectfile = self.builder.customprojectsdir + "plac.ini"
        #self.builder.projectfile = self.builder.customprojectsdir + "wg.ini"
        self.builder.projectfile = self.builder.customprojectsdir + "webster-amd64.ini"
        self.builder.readProject()
        self.configUI()

    def getGUIstate(self):
        self.log.debug('[DEBUG] Function: getGUIstate')
        self.builder.distfullname = self.tc_distfullname.GetValue()
        self.builder.distshortname = self.tc_distshortname.GetValue()
        self.builder.distver = self.tc_distver.GetValue()
        self.builder.distbranch = self.tc_branch.GetValue()
        self.builder.distplatform = self.c_platform.GetStringSelection()
        self.builder.distrepo = self.tc_repo.GetValue()
        self.builder.distrepofile = self.tc_repofile.GetValue()
        ## if empty any vars need to prompt

    def stage0livefspath(self):
        if os.path.exists(self.builder.livefspath):
            dlg = wx.MessageDialog(self,
                                "delete " + self.builder.livefspath + " ?",
                                'Live FS path already exists',
                                wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL
                               )
            val = dlg.ShowModal()
            if val == wx.ID_YES:
                self.builder.stage0deletelivefspath()
                self.builder.stage0createlivefspath()
            elif val == wx.ID_NO:
                pass
            else:
                self.continuerun = 0
            dlg.Destroy()
        else:
            self.builder.stage0createlivefspath()

    def stage0liveisopath(self):
        if os.path.exists(self.builder.liveisopath):
            dlg = wx.MessageDialog(self,
                                "delete " + self.builder.liveisopath + " ?",
                                'Live ISO path already exists',
                                wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL
                               )
            val = dlg.ShowModal()
            if val == wx.ID_YES:
                self.builder.stage0deleteliveisopath()
                self.builder.stage0createliveisopath()
            elif val == wx.ID_NO:
                pass
            else:
                self.continuerun = 0
            dlg.Destroy()
        else:
            self.builder.stage0createliveisopath()

        if os.path.exists(self.builder.isopath):
            pass
        else:
            self.builder.stage0createisodir()

    def stage3init(self):
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

    def stage3squashfs(self):
        if os.path.isfile(self.builder.squashfsfile):
            os.remove(self.builder.squashfsfile)
            self.builder.squashfilesystem()
        else:
            self.builder.squashfilesystem()

    def onBuildIt(self, event):
        self.log.debug('[DEBUG] Function: onBuildIt')
        self.getGUIstate()

        self.continuerun = 1

        # stage 0 create basic dir setup
        self.builder.stage0setpaths()
        if self.continuerun:
            self.stage0livefspath()
        if self.continuerun:
            self.stage0liveisopath()

        # stage 1 debootstrap
        if self.continuerun:
            self.builder.stage1createbasefrombootstrap()

        # stage 2 chroot
        if self.continuerun:
            self.builder.chrootcmdinitialsetup()
            self.builder.installfiles = self.cl_install.GetCheckedStrings()
            self.builder.stage2packages()
            self.builder.scriptsinchrootfiles = self.cl_scriptsinchroot.GetCheckedStrings()
            self.builder.stage2scripts()
            self.builder.chrootcmdclose()
            self.builder.chrootcmdwrite()
            self.builder.chrootactionbuild()

        # stage 3 iso prep and other
        if self.continuerun:
            self.stage3init()
            self.builder.stage3files()

            self.builder.stage3cmdoutsideinit()
            self.builder.scriptsoutchrootfiles = self.cl_scriptsoutchroot.GetCheckedStrings()
            self.builder.stage3cmdoutsidescripts()
            self.builder.stage3cmdoutsidewrite()
            self.builder.stage3cmdoutsiderun()

            self.stage3squashfs()

        # stage 4 make iso
        if self.continuerun:
            self.builder.stage4createiso()

        self.log.warning('[ ] done')
        print "done"

        # get self.cl_scriptsinchroot
        # get self.cl_overlays
        # get self.cl_scriptsoutchroot

app = wx.App(0)
ldcFrame(None).Show()
app.MainLoop()