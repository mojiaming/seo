import wx
import wx.grid
import wx.html2


# 关键字表格
class GridData(wx.grid.PyGridTableBase):
    _cols = "关键字 域名/名称 搜索引擎 点击区间 当日 已处理 排名".split()
    _data = []
    _highlighted = set()

    def __init__(self, data):
        wx.grid.GridTableBase.__init__(self)
        self._data = data

    def GetColLabelValue(self, col):
        return self._cols[col]

    def GetNumberRows(self):
        return len(self._data)

    def GetNumberCols(self):
        return len(self._cols)

    def GetValue(self, row, col):
        return self._data[row][col]

    def SetCellValue(self, row, value):
        _values = value.split('&')
        for index in range(len(_values)):
            self._data[row][index] = _values[index]

    def GetAttr(self, row, col, kind):
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(wx.GREEN if row in self._highlighted else wx.WHITE)
        return attr

    def AppendRows(self, newData=None):
        if newData is None:
            return
        self._data.append(newData)
        return self.Refresh(self._data, 1)

    def Refresh(self, data, length):
        try:
            self._data = data
            grid_view = self.GetView()
            grid_view.BeginBatch()
            append_msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, length)
            grid_view.ProcessTableMessage(append_msg)
            grid_view.EndBatch()
            get_value_msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
            grid_view.ProcessTableMessage(get_value_msg)
            return True
        except Exception as e:
            return False

    def ClearData(self):
        self._data.clear()
        grid_view = self.GetView()
        grid_view.BeginBatch()
        append_msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, 0, len(self._data))
        grid_view.ProcessTableMessage(append_msg)
        grid_view.EndBatch()
        get_value_msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        grid_view.ProcessTableMessage(get_value_msg)
        return True

