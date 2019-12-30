from selenium import webdriver
from time import sleep
import base64


def Login(browser, username, password):
    browser.get('https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fjw.ustc.edu.cn%2Fucas-sso%2Flogin')
    nameinput = browser.find_element_by_id('username')
    pdinput = browser.find_element_by_id('password')
    nameinput.send_keys(username)
    pdinput.send_keys(password)
    browser.find_element_by_id('login').click()


def JudgeTeacher(browser, exn):
    sleep(1)
    questions = browser.find_elements_by_class_name('item')
    radioxpath = 'div/div/div/label[{index:d}]'
    for question in questions[:-3] + [questions[-2]]:
        question.find_element_by_xpath(radioxpath.format(index=1)).click()
    
    exn2index = lambda n: (n - 1) // 3 + 2
    questions[-3].find_element_by_xpath(radioxpath.format(index=exn2index(exn))).click()
    questions[-1].find_element_by_tag_name('textarea').send_keys(' ')
    browser.find_element_by_id('btn-group').find_elements_by_xpath('button')[1].click()


def JudgeTA(browser):
    sleep(1)
    questions = browser.find_elements_by_class_name('item')
    radioxpath = 'div/div/div/label[{index:d}]'
    for question in questions[:-1]:
        question.find_element_by_xpath(radioxpath.format(index=1)).click()
    questions[-1].find_element_by_tag_name('textarea').send_keys(' ')
    browser.find_element_by_id('btn-group').find_elements_by_xpath('button')[1].click()


def Judge(username, password):
    browser = webdriver.Chrome()
    Login(browser, username, password)
    browser.get('https://jw.ustc.edu.cn/for-std/evaluation/summative')
    sleep(5)  # 手动关闭弹窗

    # 从评教界面回到选择界面时需要重新查找元素
    # 评教完成的课程会被自动排到末尾，只需选出第一个
    notfinish = True
    exn = {}
    while notfinish:
        notfinish = False

        sleep(5)
        row = browser.find_element_by_class_name('el-table__row')
        coursename = row.find_element_by_class_name('name').text
        teachers = row.find_elements_by_xpath('td[3]/div/div/a')
        TAs = row.find_elements_by_xpath('td[4]/div/div/a')
        for teacher in teachers:
            if coursename not in exn:
                exn[coursename] = int(input(coursename + '习题课次数：'))
            if 'disabled' not in teacher.get_attribute('class'):
                teacher.click()
                JudgeTeacher(browser, exn[coursename])
                notfinish = True
                break
        if notfinish:
            continue
        for TA in TAs:
            if 'disabled' not in TA.get_attribute('class'):
                TA.click()
                JudgeTA(browser)
                notfinish = True
                break


