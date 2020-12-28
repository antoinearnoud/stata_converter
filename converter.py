# Note: run with pythonw cameleon.py


import wx
import glob
import pandas as pd
import os

#app = wx.App()
#frame = wx.Frame(parent=None, title='Hello World')
#frame.Show()
#app.MainLoop()

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent) #, title='Hello World')
        #panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.row_obj_dict = {}

        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 200),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.list_ctrl.InsertColumn(0, 'File', width=200)
        self.list_ctrl.InsertColumn(1, 'Path', width=200)
        self.list_ctrl.InsertColumn(2, 'Number Of Observations', width=200)
        self.list_ctrl.InsertColumn(3, 'Number Of Variables', width=200)

        open_button = wx.Button(self, label='Choose File')
        open_button.Bind(wx.EVT_BUTTON, self.on_open)
        main_sizer.Add(open_button, 0, wx.ALL | wx.CENTER, 5)

        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        convert_button = wx.Button(self, label='Convert to Stata 13')
        convert_button.Bind(wx.EVT_BUTTON, self.on_convert)
        main_sizer.Add(convert_button, 0, wx.ALL | wx.CENTER, 5)

        #self.text_ctrl = wx.TextCtrl(panel)
        #main_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        #my_btn = wx.Button(panel, label='Press Me')
        #my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        #main_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(main_sizer)

    def on_convert(self, event):
        selection = self.list_ctrl.GetFocusedItem()
        nb_files = self.list_ctrl.GetItemCount()
        for selection in range(0,nb_files):
            if selection >= 0:
                pathname = self.row_obj_dict[selection]
                newpath = os.path.join(os.path.splitext(pathname)[0] + "_v13.dta")
                #df.to_stata(os.path.join(os.path.dirname(pathname), "test.dta"))
                if os.path.isfile(newpath):
                    dlg = wx.MessageDialog(None, "The file already exists on disk. Do you want to replace it?",'Updater',wx.YES_NO | wx.ICON_QUESTION)
                    result = dlg.ShowModal()
                    if result == wx.ID_YES:
                        df = pd.read_stata(pathname)
                        df.to_stata(newpath, version = 117, write_index = False)
                        print("saving file to ", newpath)
                        #print(len(df))
                        #dlg = EditDialog(mp3)
                        #dlg.ShowModal()
                        wx.MessageBox('Conversion of files done.', 'All good!', wx.OK | wx.ICON_INFORMATION)
                        #self.update_mp3_listing(self.current_folder_path)
                        #dlg.Destroy()
                    else:
                        print("File already exist. Cancel.")
                else:
                    df = pd.read_stata(pathname)
                    df.to_stata(newpath, version = 117, write_index = False)
                    print("saving file to ", newpath)
                    wx.MessageBox('Conversion of files done.', 'All good!', wx.OK | wx.ICON_INFORMATION)


    # def on_convert(self, event):
    #     selection = self.list_ctrl.GetFocusedItem()
    #     if selection >= 0:
    #         mp3 = self.row_obj_dict[selection]
    #         dlg = EditDialog(mp3)
    #         dlg.ShowModal()
    #         self.update_mp3_listing(self.current_folder_path)
    #         dlg.Destroy()

    # open one file
    def on_open(self, event):

        # if self.contentNotSaved:
        #     if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
        #                      wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
        #         return

        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open Stata file", wildcard="Stata files (*.dta)|*.dta", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            #if fileDialog.ShowModal() == wx.ID_CANCEL:
            #    return     # the user changed their mind

            if fileDialog.ShowModal() == wx.ID_OK:


                #self.current_folder_path = folder_path
                self.list_ctrl.ClearAll() # added this

                self.list_ctrl.InsertColumn(0, 'File', width=200)
                self.list_ctrl.InsertColumn(1, 'Path', width=200)
                self.list_ctrl.InsertColumn(2, 'Number Of Observations', width=200)
                self.list_ctrl.InsertColumn(3, 'Number Of Variables', width=200)
                # Proceed loading the file chosen by the user
                pathname = fileDialog.GetPath()
                filename = fileDialog.GetFilename()
                statafile_object = pd.read_stata(pathname)
                try:
                    with open(pathname, 'r') as file:
                        index = 0
                        self.list_ctrl.InsertItem(index, filename)
                        self.list_ctrl.SetItem(index, 1, pathname)
                        self.list_ctrl.SetItem(index, 2, str(len(statafile_object)))
                        self.list_ctrl.SetItem(index, 3, str(len(statafile_object.columns)))
                        self.row_obj_dict[index] = pathname
                        #self.doLoadDataOrWhatever(file)
                except IOError:
                    wx.LogError("Cannot open file '%s'." % newfile)



    def update_sata_files_listing(self, folder_path):
        self.current_folder_path = folder_path
        self.list_ctrl.ClearAll()

        self.list_ctrl.InsertColumn(0, 'File', width=200)
        self.list_ctrl.InsertColumn(1, 'Path', width=200)
        self.list_ctrl.InsertColumn(2, 'Number Of Observations', width=200)
        self.list_ctrl.InsertColumn(3, 'Number Of Variables', width=200)

        statafiles = glob.glob(folder_path + '/*.dta')
        statafile_objects = []
        index = 0
        for statafile in statafiles:
            statafile_object = pd.read_stata(statafile)
            self.list_ctrl.InsertItem(index,
                os.path.basename(statafile))
            self.list_ctrl.SetItem(index, 1,
                statafile)
            self.list_ctrl.SetItem(index, 2,
                str(len(statafile_object)))
            self.list_ctrl.SetItem(index, 3,
                str(len(statafile_object.columns)))
            statafile_objects.append(statafile_object)
            self.row_obj_dict[index] = statafile #statafile_object
            index += 1

            # mp3_object = eyed3.load(mp3)
            # self.list_ctrl.InsertItem(index,
            #     mp3_object.tag.artist)
            # self.list_ctrl.SetItem(index, 1,
            #     mp3_object.tag.album)
            # self.list_ctrl.SetItem(index, 2,
            #     mp3_object.tag.title)
            # mp3_objects.append(mp3_object)
            # self.row_obj_dict[index] = mp3_object
            # index += 1

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None,
                         title='Stata Converter', size=(1000, 300))
        self.panel = MyPanel(self)
        self.create_menu()
        self.Show()

    # create menu
    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_folder_menu_item = file_menu.Append(
            wx.ID_ANY, 'Choose Folder',
            'Open a folder with Stata files'
        )
        menu_bar.Append(file_menu, '&File')
        self.Bind(
            event=wx.EVT_MENU,
            handler=self.on_open_folder,
            source=open_folder_menu_item,
        )
        self.SetMenuBar(menu_bar)

    # define action after clicking inside the menu
    def on_open_folder(self, event):
        title = "Choose a directory with Stata files:"
        dlg = wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.update_sata_files_listing(dlg.GetPath())
        dlg.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
