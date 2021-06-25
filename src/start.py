import os
from .baidu import Baidu
from . import log
_data_path = os.getcwd() + '\\data.txt'


class StartThread:

    def __init__(self):
        self._list = []

    # 启动运行
    def start(self):
        try:
            with open(_data_path, "r", encoding='utf-8') as f:
                self._list = f.readlines()
                f.close()
            for i in range(len(self._list)):
                _item = self._list[i].replace('\n', '').split('&')
                self.run(_item, i)
        except Exception as e:
            log.error(e)

    # 需要执行的耗时异步任务
    @staticmethod
    def run(_line, index):
        if _line[2] == "百度PC":
            Baidu(_line, index).pc_bai_du()
        else:
            Baidu(_line, index).mobile_bai_du()

