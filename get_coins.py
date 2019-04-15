from selenium import webdriver
import time
import smtp


driver = webdriver.Chrome()
url = 'http://www.hubbang.com/index.php?m=bbs'
driver.get(url)
driver.maximize_window()

login_botton = driver.find_element_by_id('J_sidebar_login')
login_botton.click()
user_box = driver.find_element_by_id('J_u_login_username')
user_box.send_keys('忘忧草')
passwd_box = driver.find_element_by_id('J_u_login_password')
passwd_box.send_keys('a1314520.lei')
login = driver.find_element_by_css_selector('button.btn.btn_big.btn_submit.mr20')
login.click()

time.sleep(3)
status_code = 0
try:
    daka = driver.find_element_by_xpath('//a[@id="J_punch_mine"]')
    daka.click()
    status_code = 1
    smtp.send_email(status_code)
except Exception as e:
    smtp.send_email(status_code)
finally:
    driver.close()