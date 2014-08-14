import wx
import os
import ComicInfoXmlHandler

class ComicInfoGetter(wx.App):

    def OnInit(self):
        frm = GuiWindow("ComicInfo Getter from D&M Lexicon")
        frm.Show()
        return 1


class GuiWindow(wx.Frame):

    def __init__(self, title):

        self.fromxml = ['Series', 'Number', 'Title', 'Writer', 'Penciller', 'Genre', 'Year', 'Month', 'Day']
        self.cix = ComicInfoXmlHandler.ComicInfoXmlHandler(self.fromxml)

        wx.Frame.__init__(self, None, -1, title, size=(480, 600), pos=(400, 448))
        panel = wx.Panel(self, wx.ID_ANY)

        self.lexicon_url_input = wx.TextCtrl(panel, wx.ID_ANY, 'Info URL')
        self.filepath = wx.TextCtrl(panel, wx.ID_ANY , 'Archive Path', style=wx.TE_READONLY)
        self.openfilebutton = wx.Button(panel, wx.ID_ANY, '...')

        self.editorfield_series = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.editorfield_number = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.editorfield_title = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.editorfield_circle = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.editorfield_penciller = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.editorfield_genre = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.editorfield_year = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.editorfield_month = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.editorfield_day = wx.TextCtrl(panel, wx.ID_ANY, '')

        self.edirotfield_list = [
            self.editorfield_series,
            self.editorfield_number,
            self.editorfield_title,
            self.editorfield_circle,
            self.editorfield_penciller,
            self.editorfield_genre,
            self.editorfield_year,
            self.editorfield_month,
            self.editorfield_day
        ]

        self.openfilebutton.Bind(wx.EVT_BUTTON, self.open)
        self.filepath.Bind(wx.EVT_TEXT, self.loadcomicinfo)

        dt = Droptarget(self)
        self.SetDropTarget(dt)

        line_filepath = wx.BoxSizer(wx.HORIZONTAL)
        line_lexiconurl = wx.BoxSizer(wx.HORIZONTAL)
        line_series = wx.BoxSizer(wx.HORIZONTAL)
        line_artist = wx.BoxSizer(wx.HORIZONTAL)
        line_others = wx.BoxSizer(wx.HORIZONTAL)

        layout = wx.BoxSizer(wx.VERTICAL)

        line_filepath.Add(self.filepath, proportion=1, flag=wx.GROW)
        line_filepath.Add(self.openfilebutton, proportion=0, flag=wx.GROW)

        line_lexiconurl.Add(self.lexicon_url_input, proportion=1, flag=wx.GROW)

        line_series.Add(self.editorfield_series, proportion=1, flag=wx.GROW)
        line_series.Add(self.editorfield_number, proportion=0, flag=wx.GROW)
        line_series.Add(self.editorfield_title, proportion=1, flag=wx.GROW)

        line_artist.Add(self.editorfield_circle, proportion=1, flag=wx.GROW)
        line_artist.Add(self.editorfield_penciller, proportion=1, flag=wx.GROW)

        line_others.Add(self.editorfield_genre, proportion=1, flag=wx.GROW)
        line_others.Add(self.editorfield_year, proportion=0, flag=wx.GROW)
        line_others.Add(self.editorfield_month, proportion=0, flag=wx.GROW)
        line_others.Add(self.editorfield_day, proportion=0, flag=wx.GROW)

        layout.Add(line_filepath, proportion=0, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=5)
        layout.Add(line_lexiconurl, proportion=0, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=5)
        layout.Add(line_series, proportion=0, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=5)
        layout.Add(line_artist, proportion=0, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=5)
        layout.Add(line_others, proportion=0, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(layout)

    def open(self, e):
        path = ''
        dialog = wx.FileDialog(self, "Choose a File", path, "*.*")
        if dialog.ShowModal() == wx.ID_OK:
            path = os.path.join(dialog.GetDirectory(), dialog.GetFilename())
            self.filepath.SetValue(path)
        dialog.Destroy()

    def loadcomicinfo(self, e):
        for i in range(len(self.edirotfield_list)):
            self.edirotfield_list[i].SetValue('')
        self.cix.get_info(self.filepath.GetValue())
        for i in range(len(self.edirotfield_list)):
            if self.cix.todisplay[self.fromxml[i]] != None:
                self.edirotfield_list[i].SetValue(self.cix.todisplay[self.fromxml[i]])


class Droptarget(wx.FileDropTarget):

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, files):
        if len(files) == 1:
            self.window.filepath.SetValue(files[0])
        else:
            wx.MessageBox("I can't do with multiple files!", 'Error')

if __name__ == '__main__':
    app = ComicInfoGetter()
    app.MainLoop()