import os
import wx
import InfoEditor
import lexicon_parser
import  ChooserFromLexicon


class ComicInfoGetter(wx.App):

    def OnInit(self):
        frm = GuiWindow("ComicInfoEditor")
        frm.Show()
        return 1


class GuiWindow(wx.Frame):

    def __init__(self, title):

        wx.Frame.__init__(self, None, -1, title, size=(480, 600), pos=(400, 448))
        panel = wx.Panel(self, wx.ID_ANY)

        self.lexicon_url_input = wx.TextCtrl(panel, wx.ID_ANY, 'Info URL')
        self.query_lexicon_button = wx.Button(panel, wx.ID_ANY, 'Query Lexicon')

        self.filepath = wx.TextCtrl(panel, wx.ID_ANY , 'Archive Path', style=wx.TE_READONLY)
        self.openfilebutton = wx.Button(panel, wx.ID_ANY, '...')

        self.savebutton = wx.Button(panel, wx.ID_ANY, 'Save XML to Archive')
        self.resetbutton = wx.Button(panel, wx.ID_ANY, 'Reset Editing')

        self.editorfield_series = wx.TextCtrl(panel, wx.ID_ANY, 'Series')
        self.search_by_title_button = wx.Button(panel, wx.ID_ANY, 'Search')

        self.editorfield_writer = wx.TextCtrl(panel, wx.ID_ANY, '')


        self.editorfield_penciller = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.editorfield_genre = wx.TextCtrl(panel, wx.ID_ANY, '')


        self.editorfield_year = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.editorfield_month = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.editorfield_day = wx.TextCtrl(panel, wx.ID_ANY, '')

        self.fields_metadatas = [
            self.editorfield_series,
            self.editorfield_writer,
            self.editorfield_penciller,
            self.editorfield_genre,
            self.editorfield_year,
            self.editorfield_month,
            self.editorfield_day
        ]


        self.query_lexicon_button.Bind(wx.EVT_BUTTON, self.query_lexicon)
        self.openfilebutton.Bind(wx.EVT_BUTTON, self.show_fileopen_dialog)
        self.search_by_title_button.Bind(wx.EVT_BUTTON, self.search_by_title)

        self.savebutton.Bind(wx.EVT_BUTTON, self.save_comicinfo)
        self.resetbutton.Bind(wx.EVT_BUTTON, self.open_archive)

        dt = Droptarget(self)
        self.SetDropTarget(dt)

        line_filepath = wx.BoxSizer(wx.HORIZONTAL)
        line_lexiconurl = wx.BoxSizer(wx.HORIZONTAL)
        line_series = wx.BoxSizer(wx.HORIZONTAL)
        line_artist = wx.BoxSizer(wx.HORIZONTAL)
        line_others = wx.BoxSizer(wx.HORIZONTAL)
        line_saveloadbuttons = wx.BoxSizer(wx.HORIZONTAL)

        layout = wx.BoxSizer(wx.VERTICAL)

        line_filepath.Add(self.filepath, proportion=1, flag=wx.GROW)
        line_filepath.Add(self.openfilebutton, proportion=0)

        line_lexiconurl.Add(self.lexicon_url_input, proportion=1, flag=wx.GROW)
        line_lexiconurl.Add(self.query_lexicon_button, proportion=0, flag=wx.GROW)

        line_series.Add(self.editorfield_series, proportion=1, flag=wx.GROW)
        line_series.Add(self.search_by_title_button, proportion=0, flag=wx.GROW)


        line_artist.Add(self.editorfield_writer, proportion=1, flag=wx.GROW)
        line_artist.Add(self.editorfield_penciller, proportion=1, flag=wx.GROW)

        line_others.Add(self.editorfield_genre, proportion=1, flag=wx.GROW)
        line_others.Add(self.editorfield_year, proportion=0, flag=wx.GROW)
        line_others.Add(self.editorfield_month, proportion=0, flag=wx.GROW)
        line_others.Add(self.editorfield_day, proportion=0, flag=wx.GROW)

        line_saveloadbuttons.Add(self.savebutton, proportion=0)
        line_saveloadbuttons.Add(self.resetbutton, proportion=0)

        layout.Add(line_filepath, proportion=0, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=5)
        layout.Add(line_lexiconurl, proportion=0, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=5)
        layout.Add(line_series, proportion=0, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=5)
        layout.Add(line_artist, proportion=0, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=5)
        layout.Add(line_others, proportion=0, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=5)
        layout.Add(line_saveloadbuttons, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

        panel.SetSizer(layout)

    def open_archive(self, path):
        self.reset_url_field()
        try:
            self.set_text_fields(self.load_comicinfo(path))
        except:
             wx.MessageBox("I can't find Comicrack.xml", 'Error')
             self.filepath.SetValue('')

    def show_fileopen_dialog(self, e):
        path = ''
        dialog = wx.FileDialog(self, "Choose a File", path, "*.*")
        if dialog.ShowModal() == wx.ID_OK:
            path = os.path.join(dialog.GetDirectory(), dialog.GetFilename())
            self.filepath.SetValue(path)
        dialog.Destroy()

    def reset_url_field(self):
        self.lexicon_url_input.SetValue('')

    def set_text_fields(self, metadata):
        self.editorfield_series.SetValue('')
        if metadata['Series']:
            self.editorfield_series.SetValue(metadata['Series'])

        self.editorfield_writer.SetValue('')
        if metadata['Writer']:
            self.editorfield_writer.SetValue(', '.join(metadata['Writer']))

        self.editorfield_penciller.SetValue('')
        if metadata['Penciller']:
            self.editorfield_penciller.SetValue(', '.join(metadata['Penciller']))

        self.editorfield_genre.SetValue('')
        if metadata['Genre']:
            self.editorfield_genre.SetValue(', '.join(metadata['Genre']))

        self.editorfield_year.SetValue('')
        if metadata['Year']:
            self.editorfield_year.SetValue(metadata['Year'])

        self.editorfield_month.SetValue('')
        if metadata['Month']:
            self.editorfield_month.SetValue(metadata['Month'])

        self.editorfield_day.SetValue('')
        if metadata['Day']:
            self.editorfield_day.SetValue(metadata['Day'])

    def load_comicinfo(self, path):
        try:
            metadata = InfoEditor.get_metadata(path)
            return metadata
        except:
            raise

    def query_lexicon(self, e):
        url = self.lexicon_url_input.GetValue()
        metadata = lexicon_parser.search_by_url(url)
        self.set_text_fields(metadata)

    def search_by_title(self, e):
        search_keyword = self.editorfield_series.GetValue()
        metadatas = lexicon_parser.search_from_keyword(search_keyword)
        chooser = ChooserFromLexicon.CandidateChooser(metadatas, self.set_text_fields)
        chooser.Show()

    def save_comicinfo(self, e):
        filepath = self.filepath.GetValue()
        metadata = self.get_metadata_from_fields()
        InfoEditor.write_metadata(filepath, metadata)

    def get_metadata_from_fields(self):

        metadata = {}

        metadata['Series'] = self.editorfield_series.GetValue()
        metadata['Writer'] = self.editorfield_writer.GetValue()
        metadata['Penciller'] = self.editorfield_penciller.GetValue()
        metadata['Genre'] = self.editorfield_genre.GetValue()
        metadata['Year'] = self.editorfield_year.GetValue()
        metadata['Month'] = self.editorfield_month.GetValue()
        metadata['Day'] = self.editorfield_day.GetValue()

        return metadata


class Droptarget(wx.FileDropTarget):

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, files):
        if len(files) == 1:
            self.window.filepath.SetValue(files[0])
            self.window.open_archive(files[0])
            return True
        else:
            wx.MessageBox("I can't do with multiple files!", 'Error')
            return False


if __name__ == '__main__':
    app = ComicInfoGetter()
    app.MainLoop()