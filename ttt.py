# coding=utf8
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
class Alipay:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        #self.driver = webdriver.Chrome(options=chrome_options,executable_path="C:\\Users\\tiankun\\AppData\\Local\\Programs\\Python\\Python38\\chromedriver.exe")
        self.driver = webdriver.Chrome(executable_path="C:\\Users\\tiankun\\AppData\\Local\\Programs\\Python\\Python38\\chromedriver.exe")

    def login(self):
        driver = self.driver
        driver.get("http://59.216.1.26:8070/soa/")
        for usname in self.username:
            driver.find_element_by_name("userName").send_keys(usname)
            time.sleep(0.1)
        for pwd in self.password:
            driver.find_element_by_name("password").send_keys(pwd)
            time.sleep(0.1)

        driver.find_element_by_xpath("//a[@onclick='serviceURL();']").click()
        time.sleep(3)
        # 新开一个窗口
        #ActionChains(driver).key_down(Keys.CONTROL).send_keys('t').perform()
        #time.sleep(3)
        driver.get('http://59.216.1.26:8070/soa/menuMake.do?method=goToPage&thisId=28a8080196f0fd6610170d1dac0492ca8')
        self.getEle()

    def webshot(self,saveImgName):
        driver=self.driver
        driver.maximize_window()
        js_height = "return document.body.clientHeight"
        picname = saveImgName
        try:
            k = 1
            height = driver.execute_script(js_height)
            print(height)
            while True:
                if k * 500 < height:
                    js_move = "window.scrollTo(0,{})".format(k * 500)
                    print(js_move)
                    driver.execute_script(js_move)
                    time.sleep(0.2)
                    height = driver.execute_script(js_height)
                    k += 1
                else:
                    break
            scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            driver.set_window_size(800, scroll_height)
            driver.get_screenshot_as_file(picname + ".png")
            print("Process {} get one pic !!!".format(os.getpid()))
        except Exception as e:
            print(picname, e)

    def getEle(self):
        driver = self.driver
        table_list = driver.find_element_by_id("mainTable").text
        table_tr_list = table_list.split("\n")
        urllist = [0]
        listE = driver.find_elements_by_xpath("//a[@title='查看详细内容']")
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        for i in range(len(listE)):
            driver.maximize_window()
            listE[i].click()
            time.sleep(0.5)
            windows = driver.window_handles
            if len(windows) > 1:
                driver.switch_to.window(windows[-1])
                if driver.current_url != urllist[i]:
                    urllist.append(driver.current_url)
                    name = urllist[i+1][-32:]
                    self.webshot('C:\\Users\\tiankun\\floa1\\' + name)
                    time.sleep(0.5)
                    driver.close()
                    driver.switch_to.window(windows[0])
                    time.sleep(0.5)
            else:
                    print("down")
                    listE[i].click()
                    time.sleep(0.5)
                    windows = driver.window_handles
                    driver.switch_to.window(windows[-1])
                    urllist.append(driver.current_url)
                    name = urllist[i+1][-32:]
                    self.webshot('C:\\Users\\tiankun\\floa1\\' + name)
                    time.sleep(0.5)
                    driver.close()
                    driver.switch_to.window(windows[0])
                    time.sleep(0.5)
        #点击下一页
        driver.find_element_by_xpath("(//td[@class='page']//img)[3]").click()
        time.sleep(1)
        self.getEle()
if __name__ == '__main__':
    alipay = Alipay("admin","123457")
    logins = alipay.login()





