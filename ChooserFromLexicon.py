import wx


class ListOfCandidates(wx.ListCtrl):

    def __init__(self, parent, metadatas, callback):
        self.parent = parent
        self.metadatas = metadatas
        self.callback = callback

        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.LC_VIRTUAL)
        self.InsertColumn(0, 'Series')
        self.SetColumnWidth(0, 250)
        self.InsertColumn(1, 'Writer')
        self.SetColumnWidth(0, 2000)
        self.InsertColumn(2, 'Penciller')
        self.SetColumnWidth(0, 150)
        self.InsertColumn(3, 'Genre')
        self.SetColumnWidth(3, 100)
        self.InsertColumn(4, 'Date')
        self.SetColumnWidth(4, 100)

        self.SetItemCount(len(self.metadatas))

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDoubleClick)

    def OnGetItemText(self, row, col):
        candidate = self.metadatas[row]

        if col == 0:
            result = candidate['Series']
        elif col == 1:
            result = ', '.join(candidate['Writer'])
        elif col == 2:
            result = ', '.join(candidate['Penciller'])
        elif col == 3:
            result = ', '.join(candidate['Genre'])
        elif col == 4:
            result = '-'.join([
                candidate['Year'],
                candidate['Month'],
                candidate['Day']
            ])
        return result

    def OnDoubleClick(self, e):
        row = e.GetIndex()
        metadata = self.metadatas[row]
        self.callback(metadata)
        self.parent.Destroy()


class CandidateChooser(wx.Frame):

    def __init__(self, metadatas, callback):
        wx.Frame.__init__(self, None, -1, 'Choose correct one', size=(600, 200), pos=(400, 448))
        self.table = ListOfCandidates(self, metadatas, callback)




if __name__ == '__main__':
    app = wx.App()
    frame = CandidateChooser(metadatas)
    frame.Show()
    app.MainLoop()