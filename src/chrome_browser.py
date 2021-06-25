from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import fake_useragent
import random
import os
from selenium.webdriver.support.wait import WebDriverWait
import locale
locale.setlocale(locale.LC_ALL, '')
_project_path = os.getcwd()
_data_path = os.getcwd() + '\\data.txt'


# 设置随机分辨率
def set_resolution(driver):
    resolution_list = [
        {"width": 1280, "height": 800},
        {"width": 1366, "height": 768},
        {"width": 1440, "height": 900},
        {"width": 1600, "height": 900},
        {"width": 1024, "height": 768},
        {"width": 1280, "height": 1024},
        {"width": 1440, "height": 900},
        {"width": 1680, "height": 1050},
        {"width": 1280, "height": 800}
    ]
    _res_item = resolution_list[random.randint(0, len(resolution_list) - 1)]
    driver.set_window_size(_res_item['width'], _res_item['height'])
    return _res_item


# 设置随机手机
def set_mobile_name():
    name_list = ["Galaxy S5", "Pixel 2", "Pixel 2 XL", "iPhone 5/SE", "iPhone 6/7/8", "iPhone 6/7/8 Plus",
                 "iPhone X"]
    mobile = name_list[random.randint(0, len(name_list) - 1)]
    mobile_emulation = {"deviceName": mobile}
    capabilities = DesiredCapabilities.CHROME
    capabilities['loggingPrefs'] = {'browser': 'ALL'}
    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.binary_location = _project_path + r"\browser\Chrome\Application\chrome.exe"
    user_agent = get_header()  # 随机ua
    options.add_argument('user-agent=' + str(user_agent))
    # 无窗口模式
    options.add_argument('--headless')
    # 解决反爬识别selenium
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(executable_path="chromedriver68.exe", desired_capabilities=capabilities,
                              chrome_options=options)
    return driver


# 设置随机浏览器
def set_browser():
    options = webdriver.ChromeOptions()
    # 禁止图片加载
    # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # 解决反爬识别selenium
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 处理 gpu bug
    options.add_argument('--disable-gpu')
    options.add_argument("disable-extensions")  # 禁用扩展
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 隐藏模式
    # 无窗口模式
    options.add_argument('--headless')
    user_agent = get_header()  # 随机ua
    options.add_argument('user-agent=' + str(user_agent))
    options.binary_location = _project_path + r"\browser\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome(executable_path="chromedriver68.exe", chrome_options=options)
    return driver


# 退出浏览器
# is_pub 是否释放名额
def driver_quit(driver):
    try:
        driver.delete_all_cookies()
        driver.quit()
    except Exception as e:
        driver.quit()
        print(e)


# 根据class判断元素是否存在
# class_name class名称
def is_class_exist(driver_name, class_name):
    try:
        WebDriverWait(driver_name, 10, 0.2).until(lambda driver: driver_name.find_element_by_class_name(class_name))
        return True
    except:
        return False


# 判断元素是否存在
# text 需要查找的文字
def is_element_exist(_driver, text):
    try:
        _driver.find_element_by_xpath("//*[contains(text(),'" + text + "')]")
        # self.driver.find_element(By.LINK_TEXT, text)
        return True
    except:
        return False


# 更新数据
def update_txt(index, results='ok', page=0):
    f = open(_data_path, 'r+', encoding='utf-8')
    _lines = f.readlines()
    _row = _lines[index].replace('\n', '')
    _line = _row.split('&')

    # 0代表还未达到目标值，
    # 1001 已完成，
    # 1002 已经在运行
    # 1003 错误次数已达到设定值
    # 1004 没找到排名
    if results == 'ok':
        # 如果当天没找到排名或者当天已完成，
        if _line[6] != '1004' and _line[6] != '1001':
            _line[5] = str(int(_line[5]) + 1)
            # 是否已经达到，
            if int(_line[5]) >= int(_line[4]):
                _line[6] = '1001'
            else:
                _line[6] = '0'
            _line[8] = str(page)

    elif results == 'look':
        _line[6] = '1002'
    elif results == 'err':
        if int(_line[7]) > 2:
            _line[6] = '1003'
        else:
            _line[7] = str(int(_line[7]) + 1)
            _line[6] = '0'
    elif results == 'query':
        if page == 999:
            _line[6] = '1004'
        else:
            _line[6] = '0'
        _line[8] = str(page)
    else:
        _line[6] = '1004'
        _line[8] = '999'
    _lines[index] = '&'.join(_line) + '\n'
    f = open(_data_path, 'w+', encoding='utf-8')
    f.writelines(_lines)
    f.close()


# 获取user_agent函数
def get_header():
    location = os.getcwd() + '\\fake_useragent.json'
    ua = fake_useragent.UserAgent(path=location)
    return ua.random


