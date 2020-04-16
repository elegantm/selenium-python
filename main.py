#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2020/04/14 14:21:04
@Author  :   elegantm
@Version :   1.0
@Contact :   elegantm88@gmail.com
@Desc    :   None
'''

# here put the import lib
import requests
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
import  time  #调入time函数
import  re
import  logging as log



partenExam='2019.*下半年'
serverKey=''
serverchanurl='https://sc.ftqq.com/'

def init_conf():
    logger = log.getLogger()
    logger.setLevel(log.INFO)  # Log等级总开关
    logfile = './log.txt'
    fh = log.FileHandler(logfile, mode='a')  # open的打开模式这里可以进行参考
    formatter = log.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setLevel(log.INFO)  # 输出到file的log等级的开关
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def crow_website() -> str:

    # fireOptions = webdriver.FirefoxOptions()
    # fireOptions.headless = True

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')

    browser = webdriver.Chrome(options=options)

    # browser = webdriver.Firefox(options=fireOptions,executable_path=r'D:\Program Files\selenium_explore\geckodriver.exe')


    browser.get("http://rsj.sh.gov.cn/xxzsp/ksy/wangz/wendchaxun_701.jsp")
    time.sleep(0.5)  # 休眠0.3秒
    browser.find_element_by_id("wend_wendmc").send_keys("计算机")
    # browser.find_element_by_id("wend_niand_dmfy").send_keys("2019年度")
    browser.find_element_by_tag_name('img').click()

    normal_window = browser.current_window_handle

    #####获取所有页面句柄
    all_Handles = browser.window_handles
    #####如果新的pay_window句柄不是当前句柄，用switch_to_window方法切换
    content = ''
    for pay_window in all_Handles:
        if pay_window != normal_window:
            browser.switch_to.window(pay_window)
            content = browser.page_source

    browser.quit()

    return content



def deal_page_info(content:str):
    soup = BeautifulSoup(content, 'html5lib')
    log.info('{0}:{1}'.format("总长度", len(soup.find_all('wend'))))
    # log.info("总长度", len(soup.find_all('wend')))

    for link in soup.find_all('wend'):
        log.info(link.wendmc.string)
        log.info(link.wenddz.string)
        #     print(link.fabsj.stripped_strings[0])
        if len(link.wendmc.string) > 3 and re.search(partenExam, link.wendmc.string):
            # 输出信息
            print(link.wendmc.string)
            log.info("--find partern- start--")
            log.info(link.wendmc.string)
            log.info(link.wenddz.string)
            sendMessageToWechat("2019下半年领取 ",str(link.wendmc.string +" -----\n\n: "+ link.wenddz.string))
            log.info("--find partern- end--")



def sendMessageToWechat(topic:str,message:str):
    payload ={'text':topic,'desp':message}
    r = requests.get(serverchanurl+serverKey,payload)
    log.info("send wechat topic: %s,%s %s",topic," message:  ",message)




def get_time(datestr):
    if len(datestr)<3:
        return None
    t = datetime.datetime.strptime(datestr, '%Y.%m.%d')
    return t





if __name__ == '__main__':
    init_conf()
    page =crow_website()
    deal_page_info(page)


