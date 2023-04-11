from ast import If
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import sys
from selenium.webdriver.chrome.options import Options
import json
import platform
import os
import re
CONFIG_FILE = "./config.json"  # 配置文件的路径，一般不需要修改
URL_LIST = "url_list.txt"
# from @Keuin: 如果不好使了，可能是因为网页布局有所改变，
# 请自行打开播放页面，用F12逐个定位下面列出的元素，并更新将他们的XPATH常量
XPATH_HOME_PAGE_LOGIN_BUTTON = '/html/body/div[4]/div[2]/div[2]/div[3]/div/div[1]/div/div/div/div[2]/button'
XPATH_SCORE_SHEET_VIDEO_HYPERLINK = "//div[@class='unit-name-td hoverblue']"
XPATH_SCORE_SHEET_VIDEO_LIST = '/html/body/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[6]/div/div[2]/section[2]/div[2]'
XPATH_LABEL_VIDEO_DURATION = '/html/body/div[4]/div[2]/div/div[2]/div/div/div/section[2]/div/div/div[2]/div/xt-wrap/xt-controls/xt-inner/xt-time/span[2]'
XPATH_LABEL_TIME_PLAYED = '/html/body/div[4]/div[2]/div/div[2]/div/div/div/section[2]/div/div/div[2]/div/xt-wrap/xt-controls/xt-inner/xt-time/span[1]'
XPATH_BUTTON_2X_SPEED = '/html/body/div[4]/div[2]/div/div[2]/div/div/div/section[2]/div/div/div[2]/div/xt-wrap/xt-controls/xt-inner/xt-speedbutton/xt-speedlist/ul/li[1]'
XPATH_BUTTON_SELECT_PLAY_SPEED = '/html/body/div[4]/div[2]/div/div[2]/div/div/div/section[2]/div/div/div[2]/div/xt-wrap/xt-controls/xt-inner/xt-speedbutton/xt-speedvalue'
XPATH_BUTTON_PLAY = '/html/body/div[4]/div[2]/div/div[2]/div/div/div/section[2]/div/div/div[2]/div/xt-wrap/xt-controls/xt-inner/xt-playbutton'
XPATH_BUTTON_PLAY_STATUS = '/html/body/div[4]/div[2]/div/div[2]/div/div/div/section[2]/div/div/div[2]/div/xt-wrap/xt-controls/xt-inner/xt-playbutton/xt-tip'
XPATH_VIDEO_PLAYER = "/html/body/div[4]/div[2]/div/div[2]/div/div/div/section[2]/div/div/div[2]/div/xt-wrap/xt-bigbutton"
XPATH_WATCH_PROGRESS = '/html/body/div[4]/div[2]/div/div[2]/div/div/div/section[1]/div[2]/div/div/span'
XPATH_VIDEO_TITLE = "/html/body/div[4]/div[2]/div/div[2]/div/div/div/section[1]/div[1]/span"
XPATH_SCORE_PAGE_TAG='/html/body/div[4]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div[6]'
class AutoYuketang:
    course_url = ""
    home_url = ""
    course_id = ""
    def set_chrome_driver(self):
        """
        根据系统环境配置chormedriver
        :return:
        """
        chrome_options = Options()

        if platform.system() == "Linux":  # for Linux
            # 16年之后，chrome给出的解决办法，抢了PhantomJS饭碗
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')  # root用户不加这条会无法运行
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--mute-audio")  # 静音播放
        else:  # for other OS
            chrome_options.add_argument("--mute-audio")  # 静音播放

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        print("成功配置chrome驱动")
    def read_config_file(self):
        """
        从JSON中读取数据，并写入URL
        :return:
        """
        if os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.course_url = data[0]["URL"]
                self.home_url = data[0]["HOME_URL"]
                print(f"成功读取配置文件：{CONFIG_FILE}")
        else:
            print(f"配置文件`{CONFIG_FILE}`不存在，请检查！")
    def load_url(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)
    def login(self, with_login_cookie):
        """
          雨课堂登录
          :param with_login_cookie:  如果使用cookie，则不需要登录
          :return:
          """

        if with_login_cookie:
            return

        print("未指定cookie，需要手动登录雨课堂")
        # self.load_url(self.home_url)
        while True:
            # time.sleep(5)
            if self.wait_element_path_loaded(XPATH_SCORE_PAGE_TAG):
                print('登录成功！')
                return
            # else:
            #     # 未登录。打开登录二维码
            #     self.wait_element_path_loaded(XPATH_HOME_PAGE_LOGIN_BUTTON)
            #     self.driver.find_element("xpath", XPATH_HOME_PAGE_LOGIN_BUTTON).click()
    def prepare_video_list(self, location):
        """
        为播放准备连接
        :param location: 保存网课连接的文件地址
        :return:
        """

        # self.course_id = "$" + \
        #                  re.match("https://[a-zA-Z0-9.]*/[a-zA-Z]*/[a-zA-Z]*/[a-zA-Z0-9]*/([0-9]+)",
        #                           self.driver.current_url).group(1) + "$"
        self.course_id = "$16568870$"
        print("当前课程ID：" + self.course_id)
        """如果文件不存在的话"""
        if not os.path.exists(location):
            print("URL文件不存在！创建文件")
            fp = open(location, 'w+', encoding='utf-8')
            fp.close()
        fp = open(location, 'r+', encoding='utf-8')
        lines = fp.readlines()  # 读取所有行
        last_line = ""
        if len(lines) != 0:
            last_line = lines[-1]  # 取最后一行
        if self.course_id not in last_line:
            print("URL未构建或构建不完全")
            fp.close()
            self.get_video_list(location)
        else:
            fp.close()
            print("检测到校验位，已从历史记录中获取链接")

        print("全部链接已就绪")

        return
    def get_video_list(self, location):
        """
        爬取全部网课连接
        :param location: 保存网课连接的文件地址
        :return:
        """
        with open(location, 'w+', encoding='utf-8') as fp:
            self.driver.get(self.course_url)
            self.wait_and_click(XPATH_SCORE_PAGE_TAG)
            self.wait_element_path_loaded(XPATH_SCORE_SHEET_VIDEO_LIST)
            video_button_list = self.driver.find_elements(By.XPATH, XPATH_SCORE_SHEET_VIDEO_HYPERLINK)
            print("正在爬取全部视频网页连接")
            for i in video_button_list:
                i.click()
                main_window_handle = self.driver.current_window_handle  # 当前主窗口
                window_handles = self.driver.window_handles  # 全部窗口句柄
                # 对窗口进行遍历
                for handle in window_handles:
                    # 筛选新打开的窗口B
                    if handle != main_window_handle:
                        # 不是主窗口。切换到新打开的窗口B
                        # browser.switch_to_window(handle) 旧版本
                        self.driver.switch_to.window(handle)
                        current_url = (self.driver.current_url + '\r')
                        if "video" in self.driver.current_url:
                            print(self.driver.current_url)
                            fp.writelines(current_url)
                            fp.flush()
                        self.driver.close()
                        self.driver.switch_to.window(main_window_handle)
                        time.sleep(0.5)
            fp.writelines(self.course_id)
            fp.flush()
            fp.close()
        return
    def wait_url_update(self, target_url, timeout=10.0):
        """
        等待直到url更新为目标url
        :param target_url: 预计更新后的目标url
        :param timeout: 超时时间
        :return:
        """
        self.load_url(target_url)
        while target_url != self.driver.current_url and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        if timeout <= 0:
            raise TimeoutException()

    def wait_element_path_loaded(self, element_xpath):
        """
        等待相应xpath的元素加载完成
        :param element_xpath: 元素xpath
        :return: 对对应的元素
        """
        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )
        return element

    def wait_and_click(self, element_xpath):
        """
        等待相应id的元素加载完成后点击元素
        :param element_xpath: 元素path
        :return:
        """
        element = self.wait_element_path_loaded(element_xpath)
        element.click()

    def wait_and_get_element_text(self, element_xpath):
        """
        等待相应id的元素加载完成后点获取其中的文字信息
        :param element_xpath: 元素path
        :return:
        """
        element = self.wait_element_path_loaded(element_xpath)
        return element.text
    def play_video_list(self, location):
        """
        播放全部的视频
        :param location: 文件的位置
        :return:
        """

        url_list = self.read_url_list(location)

        for url in url_list:
            self.play_video(url)

        print("已播放列表中的所有视频")

    def play_video(self, url):
        """
        播放视频
        :param url: 网课的URL
        :return:
        """
        print(url)
        self.wait_url_update(url)  # 切换到新的窗口
        self.wait_and_get_element_text(XPATH_VIDEO_PLAYER)
        try:
            work_persent = self.wait_and_get_element_text(XPATH_WATCH_PROGRESS)
        except TimeoutException:
            work_persent = "任务进度元素加载失败"  # 元素加载失败

        print("任务进度：" + work_persent)
        time.sleep(0.5)
        """该小节播放完成/不需要播放"""
        if "100%" in work_persent:
            print('该视频不需要播放，跳过')
            with open(URL_LIST, 'r') as r:
                lines = r.readlines()
            with open(URL_LIST, 'w') as w:
                for l in lines:
                    if str(url) not in l:
                        w.write(l)
            return

        """"需要播放视频的情况"""
        print('该视频需要播放，尝试加速播放')
        print('等待播放器加载完毕')
        self.wait_and_get_element_text(XPATH_VIDEO_PLAYER)
        """开始播放"""
        print('播放器已加载，尝试点击开始播放按钮')
        button = WebDriverWait(self.driver, 10, poll_frequency=2).until(ec.element_to_be_clickable(
            (By.XPATH, XPATH_BUTTON_PLAY)))

        """设置2倍速度"""
        if button:
            print('已开始播放，尝试设置二倍速')
            speed_button = WebDriverWait(self.driver, 10, poll_frequency=1).until(
                ec.presence_of_element_located((By.XPATH, XPATH_BUTTON_SELECT_PLAY_SPEED)))
            ac(self.driver).move_to_element(speed_button).perform()
            time.sleep(1)
            speed_2 = self.driver.find_element("xpath", XPATH_BUTTON_2X_SPEED)
            # speed_2.click()
            ac(self.driver).move_to_element(speed_2).move_by_offset(5, 5).click().perform()
            button.click()
            print('已设置为二倍速，等待视频播放完毕……')

            to_seconds = lambda x: int(x[0]) * 3600 + int(x[1]) * 60 + int(x[2])
            while True:
                time_total = to_seconds(self.driver.find_element("xpath", XPATH_LABEL_VIDEO_DURATION).text.split(':'))
                if time_total!=0:
                    break;
            time_elapsed = to_seconds(self.driver.find_element("xpath", XPATH_LABEL_TIME_PLAYED).text.split(':'))

            self.wait_video_play_finish(time_elapsed, time_total)
            print('视频放完啦，等几秒再看下一个')
            with open(URL_LIST, 'r') as r:
                lines = r.readlines()
            with open(URL_LIST, 'w') as w:
                for l in lines:
                    if str(url) not in l:
                        w.write(l)
            time.sleep(5)
    def isPreseted(self,element_xpath):
        element = self.driver.find_element(By.XPATH,element_xpath)
        if element is not None:
            return True
        else:
            return False
    def read_url_list(self, location):
        url_list = []
        with open(location, 'r', encoding='utf-8') as fp:
            url_content = fp.readlines()
            for url in url_content:
                if self.course_id not in url:
                    url = url[:-1]
                    url_list.append(url)
            fp.close()
        return url_list
    def wait_video_play_finish(self, current_time, target_time):
        """
        等待视频播放完成
        :param current_time: 当前时间
        :param target_time: 总时间
        :return:
        """

        to_seconds = lambda x: int(x[0]) * 3600 + int(x[1]) * 60 + int(x[2])
        lastcurrent_time = 0
        while current_time < target_time:
            try:
                play_button = WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(("xpath", XPATH_BUTTON_PLAY_STATUS), '重播'))
            except TimeoutException:
                pass
            current_time = to_seconds(self.driver.find_element("xpath", XPATH_LABEL_TIME_PLAYED).get_attribute('textContent').split(':'))
            if lastcurrent_time > current_time:
                break
            lastcurrent_time = current_time
            print(f"播放进度：{current_time}s/{target_time}s "
                f"(剩余{target_time - current_time}s, "
                f"进度：{round(current_time / target_time * 100, 2)}%)")

    def __init__(self, mode):

        with_cookie = False
        # if "CookieMode" in mode:
        #     with_cookie = True
        self.set_chrome_driver()
        self.read_config_file()  # 从JSON读入URL
        # """使用CookieMode登录"""
        # self.load_cookie(with_cookie)
        self.load_url(self.course_url)
        self.login(with_cookie)
        self.prepare_video_list(URL_LIST)
        self.play_video_list(URL_LIST)
        self.driver.quit()
if __name__ == '__main__':
    mode = ""
    if len(sys.argv) == 2:
        mode = sys.argv[1]
    AutoYuketang(mode)