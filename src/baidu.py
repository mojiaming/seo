from selenium.webdriver.common.keys import Keys  # 键盘对象
import time
import random
from selenium.webdriver.common.by import By
from . import log
import locale
from selenium.webdriver.support.wait import WebDriverWait
from . import chrome_browser
import os
import threading
from pubsub import pub
_data_path = os.getcwd() + '\\data.txt'


class Baidu:
    _key = ''  # 关键字
    _value = ''  # 对应的值
    _index = 0  # 数据索引
    _res_item = None  # 屏幕分辨率
    _page = 0  # 关键字所在页数

    def __init__(self, line, index):
        self._key = line[0]
        self._value = line[1]
        self._index = index
        self.driver = None
        self._page = int(line[8])
        locale.setlocale(locale.LC_ALL, '')
        self.start_time = int(time.time())

    # 执行PC端点击事件
    def pc_bai_du(self):
        try:

            log.info("百度PC " + self._key + " " + self._value)
            self.driver = chrome_browser.set_browser()
            self._res_item = chrome_browser.set_resolution(self.driver)
            # 设置页面加载超时
            self.driver.implicitly_wait(10)
            self.driver.get('https://www.baidu.com/s?wd=' + self._key)
            # 核心代码已删除
            time.sleep(10)
            chrome_browser.update_txt(self._index, 'ok')
            chrome_browser.driver_quit(self.driver)
        except Exception as e:
            log.error(e)
            chrome_browser.update_txt(self._index, 'err')
            chrome_browser.driver_quit(self.driver)

    # 百度手机模式
    def mobile_bai_du(self):
        try:
            log.info("百度手机 " + self._key + " " + self._value)
            self.driver = chrome_browser.set_mobile_name()
            # 设置页面加载超时
            self.driver.implicitly_wait(10)
            self.driver.get("http://m.baidu.com")
            # 查找id为 'index-kw'的标签，即输入框
            WebDriverWait(self.driver, 10, 0.2).until(
                lambda driver: self.driver.find_element_by_id("index-kw"))
            inputs = self.driver.find_element_by_id("index-kw")
            # 在输入框中填入关键字
            inputs.send_keys(self._key)
            # '按下'回车键（第一种）
            inputs.send_keys(Keys.ENTER)
            # 核心代码已删除
            time.sleep(10)
            chrome_browser.update_txt(self._index, 'ok')
            chrome_browser.driver_quit(self.driver)
        except Exception as e:
            log.error(e)
            chrome_browser.update_txt(self._index, 'err')
            chrome_browser.driver_quit(self.driver)
