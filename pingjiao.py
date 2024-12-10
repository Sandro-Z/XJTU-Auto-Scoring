import random
import re
import time

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
#options = webdriver.EdgeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
print("说明：\n不喜欢的老师全部4星中好评~\n等待时间较长属于正常现象,一个页面最长可加载1分钟，请不要点击页面元素~\n如果出现意外，如报错退出，请重新运行~~")
name = input("学号:\n>>")
password = input("密码:\n>>")
unfavoredTeacher = set()
s = input("在此输入你不喜欢的老师的名字，输入#结束\n>>")
while s != '#':
    unfavoredTeacher.add(s)
    s = input('>>')
driver = webdriver.Chrome(options=options)
#driver=webdriver.Firefox(options=options)
#driver = webdriver.Edge(options=options)
driver.implicitly_wait(20)
driver.maximize_window()
driver.get("http://ehall.xjtu.edu.cn/")
driver.find_element(By.XPATH, '//*[@id=\"ampHasNoLogin\"]').click()
driver.find_element(By.XPATH, '//*[@id="form1"]/input[1]').send_keys(name)
driver.find_element(By.XPATH, '//*[@id="form1"]/input[2]').send_keys(password)
driver.find_element(By.XPATH, '//*[@id="account_login"]').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="ampPersonalAsideLeftMini"]/div/div[2]').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="ampPersonalAsideLeftTabHead"]/div[2]/i').click()  # 添加 点击可用应用
driver.find_element(By.XPATH, '//*[@id="ampPersonalAsideLeftAllCanUseAppsSearchInput"]').send_keys('网上评教',
                                                                                                   Keys.ENTER)  # 添加 点击可用应用
time.sleep(2)
driver.find_element(By.XPATH,
                    '/html/body/article[5]/aside[1]/div[2]/div[2]/div[2]/div[2]/ul/li[1]/span[1]').click()  # dianjiquanbu
time.sleep(2)

driver.find_element(By.XPATH, '//*[@id="ampPersonalAsideLeftAllCanUseAppsTabContent"]/div[1]/div/h5').click()  # 报错位置
time.sleep(2)

if (len(driver.find_elements(By.XPATH, '//*[@id="ampDetailEnter"]')) != 0):
    driver.find_element(By.XPATH, '//*[@id="ampDetailEnter"]').click()
    time.sleep(2)

handles = driver.window_handles
driver.switch_to.window(handles[-1])
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="12aa5b5d-3791-4a69-8fda-6e1768da4d97"]').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="pjglTopCard"]').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="tabName-content-1"]/div/div[1]').click()
time.sleep(2)

# /html/body/div[7]/div/div[1]/section/div/div[2]/div[2]/div[2]/div/    div[2]  /div[4]/div/span[1]
# /html/body/div[7]/div/div[1]/section/div/div[2]/div[2]/div[2]/div/    div[1]  /div[4]/div/span[1]
div_list = driver.find_elements(By.XPATH, '/html/body/div[7]/div/div[1]/section/div/div[2]/div[2]/div[2]/div/div')
overtime = 0
for num in range(0, len(div_list)):
    div = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[1]/section/div/div[2]/div[2]/div[2]/div/div[' + str(1 + overtime) + ']')  # 永远都是点击第一个
    if len(div.find_elements(by=By.XPATH, value='./div[4]/div/span[1]')) == 0:
        overtime += 1
        continue
    # 有些人评教逾期，没有立即评教按钮，要判断一下
    div.find_element(by=By.XPATH, value='./div[4]/div/span[1]').click()  # 进入评价页面
    time.sleep(2)
    # //*[@id="buttons"]/button
    if len(driver.find_elements(By.XPATH, '//*[@id="buttons"]/button')) != 0:
        driver.find_element(By.XPATH, '//*[@id="buttons"]/button').click()

    div_answer_list = driver.find_elements(By.XPATH, '/html/body/div[' + str(8 + num - overtime) + ']/div/div[1]/section/div[2]/div')
    # /html/body/div[9]/div/div[1]/section/div[2]/div[1] 第二次的xpath和第一次不一样？？？？？？？
    time.sleep(2)
    name = re.findall('<div class="sc-panel-thingNoImg-1-title">(.*?)</div>', driver.page_source, re.S)
    if name[0] in unfavoredTeacher:
        for div_answer, index in zip(div_answer_list, range(0, len(div_answer_list))):
            if index == len(div_answer_list) - 1:
                div_answer.find_element(by=By.XPATH,value='./div/div[2]/div[2]/div/div/div/div[1]/div/div/div/textarea').send_keys(
                    random.choice(
                        ["可以更好"]))
            else:
                div_answer.find_element(by=By.XPATH, value='./div/div[2]/div[2]/div/label[2]').click()
    else:
        for div_answer, index in zip(div_answer_list, range(0, len(div_answer_list))):
            if index == len(div_answer_list) - 1:
                div_answer.find_element(by=By.XPATH,
                                        value='./div/div[2]/div[2]/div/div/div/div[1]/div/div/div/textarea').send_keys(
                    random.choice(
                        ["真棒", "老师教的很好", "很好", "Excellent!", "很棒", "Good"]))
            else:
                div_answer.find_element(by=By.XPATH, value='./div/div[2]/div[2]/div/label[1]').click()

    div.find_element(by=By.XPATH, value='//a[contains(text(),"提交")]').click()  # 提交
    div.find_element(by=By.XPATH, value='//a[contains(text(),"确认")]').click()  # 确认
    time.sleep(10)
    print("end")
print("finished.")
