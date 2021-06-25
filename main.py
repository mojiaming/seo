# First things, first. Import the wxPython package.

import win32api
import sys
import os
from src.start import StartThread
import wx
import wx.grid
from src import log
from src.ui import GridData
from apscheduler.schedulers.blocking import BlockingScheduler
import threading
import random
import webbrowser as web
from pubsub import pub
scheduler = BlockingScheduler()


APP_TITLE = u'企建排名'
APP_ICON = 'res/favicon.ico'  # 请更换成你的icon


class MainFrame(wx.Frame):
    # '''程序主窗口类，继承自wx.Frame'''

    def __init__(self):
        try:
            '''构造函数'''
            wx.Frame.__init__(self, None, -1, APP_TITLE, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
            self.SetBackgroundColour(wx.Colour(224, 224, 224))
            self.SetSize((900, 600))
            self.Center()
            # 以下代码处理图标
            if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
                exe_name = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
                icon = wx.Icon(exe_name, wx.BITMAP_TYPE_ICO)
            else:
                icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon)

            self.thread_p = ''
            self.start_class = StartThread()

            wx.StaticText(self, -1, u'关键字：', pos=(20, 50), size=(50, -1), style=wx.ALIGN_LEFT)
            self.tc1 = wx.TextCtrl(self, -1, '', pos=(70, 50), size=(100, -1), name='input1', style=wx.ALIGN_LEFT)

            wx.StaticText(self, -1, u'域名：', pos=(170, 50), size=(50, -1), style=wx.ALIGN_LEFT)
            self.tc2 = wx.TextCtrl(self, -1, '', pos=(220, 50), size=(100, -1), name='input2', style=wx.ALIGN_LEFT)

            wx.StaticText(self, -1, u'点击数：', pos=(330, 50), size=(50, -1), style=wx.ALIGN_LEFT)
            self.tc3 = wx.TextCtrl(self, -1, '', pos=(380, 50), size=(50, -1), name='input3', style=wx.ALIGN_LEFT)
            self.tc3.SetValue("1~5")
            h_box = wx.BoxSizer(wx.HORIZONTAL)
            type_list = ['百度PC', '百度手机']
            self.type_choice = wx.Choice(self, -1, choices=type_list, pos=(500, 50))
            h_box.Add(wx.StaticText(self, label='搜索引擎：', pos=(440, 50)), 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE,
                      border=5)
            h_box.Add(self.type_choice, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
            self.Bind(wx.EVT_CHOICE, self.on_choice, self.type_choice)
            self.type = ''

            pc_bt = wx.Button(self, label='开始', pos=(20, 10), style=wx.FRAME_SHAPED)
            pc_bt.SetBackgroundColour("#32db64")
            self.Bind(wx.EVT_BUTTON, self.on_start, pc_bt)

            mobile_bt = wx.Button(self, label='结束', pos=(320, 10))
            mobile_bt.SetBackgroundColour("#f53d3d")
            self.Bind(wx.EVT_BUTTON, self.on_end, mobile_bt)

            re_bt = wx.Button(self, label='重置', pos=(120, 10), style=wx.FRAME_SHAPED)
            re_bt.SetBackgroundColour("#488aff")
            self.Bind(wx.EVT_BUTTON, self.on_reset, re_bt)

            pc_bt = wx.Button(self, label='添加', pos=(600, 50), style=wx.FRAME_SHAPED)
            pc_bt.SetBackgroundColour("#488aff")
            self.Bind(wx.EVT_BUTTON, self.on_add_keyword, pc_bt)

            pc_bt = wx.Button(self, label='清空所有', pos=(420, 10), style=wx.FRAME_SHAPED)
            pc_bt.SetBackgroundColour("#f53d3d")
            self.Bind(wx.EVT_BUTTON, self.on_clear, pc_bt)

            load_bt = wx.Button(self, label='初始化开始', pos=(220, 10), style=wx.FRAME_SHAPED)
            load_bt.SetBackgroundColour("#ffc409")
            self.Bind(wx.EVT_BUTTON, self.on_load, load_bt)

            self.keyword_bt = wx.Button(self, label='关键字', pos=(10, 100), style=wx.FRAME_SHAPED)
            self.keyword_bt.SetBackgroundColour("#409eff")
            self.Bind(wx.EVT_BUTTON, self.on_switch_key, self.keyword_bt)

            self.log_bt = wx.Button(self, label='运行日记', pos=(85, 100), style=wx.FRAME_SHAPED)
            self.Bind(wx.EVT_BUTTON, self.on_switch_log, self.log_bt)

            self.open_file_bt = wx.Button(self, label='导入关键字', pos=(160, 100), style=wx.FRAME_SHAPED)
            self.Bind(wx.EVT_BUTTON, self.on_open_file, self.open_file_bt)

            self.export_file_bt = wx.Button(self, label='导出', pos=(240, 100), style=wx.FRAME_SHAPED)
            self.Bind(wx.EVT_BUTTON, self.on_export_file, self.export_file_bt)

            self.home_bt = wx.Button(self, label='官网', pos=(800, 100), style=wx.FRAME_SHAPED)
            self.Bind(wx.EVT_BUTTON, self.on_home, self.home_bt)

            self._data_list = []
            self._list = self.read_file("data.txt")
            for line in self._list:
                line = line.strip('\n')
                _list = line.split('&')
                if _list[8] == '999':
                    _list[6] = '未找到'
                else:
                    _list[6] = _list[8]
                self._data_list.append(_list)

                if len(line.split('&')) < 6:
                    self._data_list = []
                    break

            self.grid_data = GridData(self._data_list)
            self.grid = wx.grid.Grid(self, pos=(10, 130), size=(870, 400))
            self.grid.SetTable(self.grid_data)
            # 设置表格宽度
            self.grid.SetColSize(0, 220)
            self.grid.SetColSize(1, 220)
            self.grid.SetColSize(4, 50)
            self.grid.SetColSize(5, 50)
            self.grid.SetColSize(6, 50)
            self.log_grid = wx.grid.Grid(self, pos=(10, 130), size=(870, 400))

            self._logs = []
            for line in reversed(self.read_file("run.log")):
                line = line.strip('\n')
                self._logs.append(line)

            self.log_grid.CreateGrid(200, 1)

            for index in range(len(self._logs)):
                if index == 200:
                    break
                else:
                    self.log_grid.SetCellValue(index, 0, self._logs[index])

            # 设置表格宽度
            self.log_grid.SetColSize(0, 700)
            self.log_grid.Hide()
            pub.subscribe(self.up_data, 'update_log')

        except Exception as e:
            log.error(e)

    # 启动按钮事件
    def on_start(self, event=''):
        if event != '':
            event.Skip()
        try:
            threading.Thread(target=self.start_timing).start()
            self.thread_p = threading.Thread(target=self.start_class.start)
            self.thread_p.daemon = True
            self.thread_p.start()
        except Exception as e:
            log.error(e)
            print(e)

    # 手动启动后每天凌晨12继续启动
    def start(self):
        try:
            self.update_txt()
        except Exception as e:
            log.error(e)
            print(e)

    # 重置事件
    def on_reset(self, event):
        event.Skip()
        # 重新配置文件
        self.update_txt()
        self.up_data()

    # 结束按钮事件
    def on_end(self, event):
        event.Skip()
        try:
            log.close()
            os.system("taskkill /F /IM 企建快排.exe")
            wx.Exit()
            # sys.exit()
        except Exception as e:
            print(e)

    # 更新日记记录和关键字表格数据
    def up_data(self):
        try:
            # 更新日记列表最新200条
            _new_logs = []
            i = 0
            for line in reversed(self.read_file("run.log")):
                line = line.strip('\n')
                _new_logs.append(line)
                i = i + 1
                if i >= 200:
                    break

            for index in range(len(_new_logs)):
                self.log_grid.SetCellValue(index, 0, _new_logs[index])
                attr = wx.grid.GridCellAttr()
                attr.IncRef()
            self._logs = _new_logs

            # 关键字表格数据更新
            self._list = self.read_file("data.txt")

            self._data_list = []
            for index in range(len(self._list)):
                _list = self._list[index].strip('\n').split('&')
                if _list[8] == '999':
                    _list[6] = '未找到'
                else:
                    _list[6] = _list[8]
                self._data_list.append(_list)

            self.grid_data.Refresh(self._data_list, 0)

        except Exception as e:
            log.error(e)

    # 导入关键字事件
    def on_open_file(self, event):
        try:
            event.Skip()
            wildcard = 'All files(*.txt)|*.txt'
            dialog = wx.FileDialog(None, 'select', os.getcwd(), '', wildcard)
            if dialog.ShowModal() == wx.ID_OK:
                with open('data.txt', "a", encoding='utf-8') as fp:
                    with open(dialog.GetPath(), "r", encoding='utf-8') as f:
                        self._list = f.readlines()
                        for line in self._list:
                            fp.write(line)
                            line = line.strip('\n')
                            self._data_list.append(line.split('&'))
                        f.close()
                        self.grid_data.Refresh(self._data_list, len(self._list))
                    fp.close()
                    self.update_txt()
            dialog.Destroy()

        except Exception as e:
            log.error(e)

    # 导出关键字事件
    def on_export_file(self, event):
        event.Skip()
        try:
            dlg = wx.FileDialog(self, message=u"保存文件",
                                defaultDir=os.getcwd(),
                                defaultFile='data.txt',
                                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if dlg.ShowModal() == wx.ID_OK:
                file = dlg.GetPath()
                with open("data.txt", "r", encoding='utf-8') as df:
                    with open(file, 'w', encoding='utf-8') as f:
                        data = df.read()
                        f.write(data)
                        f.close()
                    df.close()
                dlg.Destroy()
        except Exception as e:
            log.error(e)

    # 视图切换
    def on_switch_key(self, event):
        event.Skip()
        self.grid.Show()
        self.log_grid.Hide()
        self.log_bt.SetBackgroundColour("#ffffff")
        self.keyword_bt.SetBackgroundColour("#409eff")

    # 视图切换
    def on_switch_log(self, event):
        event.Skip()
        self.grid.Hide()
        self.log_grid.Show()
        self.keyword_bt.SetBackgroundColour("#ffffff")
        self.log_bt.SetBackgroundColour("#409eff")

    # 打开官网
    def on_home(self, event):
        event.Skip()
        web.open('www.qijianwang.net')


    # 启动定时任务
    def start_timing(self):
        # 在每天12点，运行一次
        scheduler.add_job(self.start, 'cron', day='1-31', hour='0')
        # 每多少分钟触发
        # scheduler.add_job(self.up_data, 'interval', minutes=1)
        self.up_data()
        scheduler.start()

    # 手动添加关键字事件
    def on_add_keyword(self, event):
        event.Skip()
        if self.tc1.GetValue() == '' or self.tc2.GetValue() == '' or self.tc3.GetValue() == '' or self.type == '':
            return
        row = self.tc1.GetValue() + "&" + self.tc2.GetValue() + "&" + self.type + "&" + self.tc3.GetValue() + "&0&0&0&0&0"
        with open("data.txt", "a", encoding='utf-8') as f:
            self._list.append(row+"\n")
            f.write(row+"\n")
            self._data_list.append(row.split('&'))
            self.grid_data.AppendRows(row.split('&'))

    # 选择搜索引擎类型事件
    def on_choice(self, event):
        event.Skip()
        self.type = event.GetString()

    # 清空所有数据
    def on_clear(self, event):
        event.Skip()
        self._data_list.clear()
        self.grid_data.ClearData()
        with open("data.txt", "w", encoding='utf-8') as f:
            f.write("")
            f.close()

    # 初始化数据
    def on_load(self, event):
        event.Skip()
        self.on_start()

    # 读取文件
    @staticmethod
    def read_file(path):
        with open(path, "r", encoding='utf-8') as f:
            _list = f.readlines()
            f.close()
            return _list

    # 更新关键字数据
    def update_txt(self):
        _lines = self.read_file('data.txt')
        for index in range(len(_lines)):
            _row = _lines[index].replace('\n', '')
            _line = _row.split('&')

            # 自动补全
            if len(_line) < 9:
                for i in range(9 - len(_line)):
                    _line.append("0")

            # 点击区间
            _interval = _line[3].split('~')
            if len(_interval) > 1:
                _ran = random.randint(int(_interval[0]), int(_interval[1]))
                # 当日需点击次数
                _line[4] = str(_ran)
            else:
                # 当日需点击次数
                _line[4] = _line[3]

            # 已点击次数
            _line[5] = str(0)
            # 状态
            _line[6] = str(0)
            # 错误次数
            _line[7] = str(0)
            # 关键字在第几页
            # _line[8] = str(0)
            _lines[index] = '&'.join(_line) + '\n'
        f = open('data.txt', 'w+', encoding='utf-8')
        f.writelines(_lines)
        f.close()


class MainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = MainFrame()
        self.Frame.Show()
        return True


if __name__ == "__main__":
    app = MainApp(redirect=True, filename="debug.txt")
    app.MainLoop()
