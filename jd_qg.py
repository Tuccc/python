import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
# -*- coding: utf-8 -*-

firefox_options = Options()
firefox_options.add_argument('--headless')
browser = webdriver.Firefox(firefox_options=firefox_options)
# browser = webdriver.PhantomJS()
wait = WebDriverWait(browser, 2)


def login():
    with open('user.txt', 'r') as f:
        lines = f.readlines()
        f.close()
    user = lines[0]
    pwd = lines[1]
    browser.get('https://passport.jd.com/new/login.aspx')
    submit_tag = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.login-tab:nth-child(3)'))
            )
    sleep(1)
    submit_tag.click()
    user_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#loginname'))
    )
    pwd_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#nloginpwd'))
    )
    login_submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#loginsubmit'))
    )
    user_input.send_keys(user)
    pwd_input.send_keys(pwd)
    sleep(5)
    login_submit.click()


def qianggou_loop():
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn-reservation'))
    )
    submit.click()
    sleep(1)
    title = browser.title
    title_true = '商品已成功加入购物车'
    title_true.encode(encoding='utf-8')
    print(title)
    if title == title_true:
        js = 'window.open("https://cart.jd.com/cart.action");'
        browser.execute_script(js)
    else:
        return qianggou_loop()
        print('False')
    handles = browser.window_handles
    browser.switch_to_window(handles[1])
    print(browser.title)
    dingdan()


def dingdan():
    submit_buy = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.submit-btn'))
    )
    submit_buy.click()
    title_buy = '订单结算页 -京东商城'
    title_buy.encode(encoding='utf-8')
    if browser.title == title_buy:
        jiesuan()
    else:
        browser.get("https://cart.jd.com/cart.action")
        return dingdan()


def jiesuan():
    submit_tj = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#order-submit'))
    )
    submit_tj.click()
    sleep(2)
    title_js = '收银台'
    title_js.encode(encoding='utf-8')
    if browser.title == title_js:
        print('抢购成功')
        browser.close()
        handles = browser.window_handles
        browser.switch_to_window(handles[0])
        browser.get('https://item.jd.com/7299762.html')
        qianggou_loop()
    else:
        browser.get('https://trade.jd.com/shopping/order/getOrderInfo.action')
        return jiesuan()


def gouwuche():
    js = 'window.open("https://cart.jd.com/cart.action");'
    browser.execute_script(js)
    handles = browser.window_handles
    browser.switch_to_window(handles[1])
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.operation .remove-batch'))
    )
    print(browser.title)
    submit.click()


def main():
    print('start')
    login()
    sleep(1)
    browser.get('https://item.jd.com/7299762.html')
    set_time = datetime.datetime.strptime('2018-07-10 10:51:00', '%Y-%m-%d %H:%M:%S')
    while True:
        now_time = datetime.datetime.now()
        if ((set_time - now_time).seconds) == 0:
            print('True')
            browser.refresh()
            while True:
                qianggou_loop()


if __name__ == '__main__':
    main()
	# test GitHubDesktop
