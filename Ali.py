# coding=utf-8
import time
from selenium import webdriver
from bs4 import BeautifulSoup

class Alipay:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def login(self):
        driver = self.driver
        driver.get("http://59.216.1.26:8070/soa/")
        for usname in self.username:
            driver.find_element_by_name("userName").send_keys(usname)
            time.sleep(0.2)
        for pwd in self.password:
            driver.find_element_by_name("password").send_keys(pwd)
            time.sleep(0.2)
        time.sleep(10)
        driver.find_element_by_xpath("//a[@onclick='serviceURL();']").click()
        records = self.getRecord(driver)
        return records

    def getRecord(self,driver):
        html = driver.page_source
        soup = BeautifulSoup(html,"lxml")
        table = soup.find("table",id="tradeRecordsIndex")
        records = []
        if table:
            trs = table.find_all("tr")
            for tr in trs:
                tds = tr.find_all("td")
                created_at = tds[1].text
                order = tds[2].text
                money = tds[3].text
                records.append({"time":created_at.replace("\n",""),"order":order.replace("\n",""),"money":money.replace("\n","")})
        return records

if __name__ == '__main__':
    alipay = Alipay("admin","123457")
    logins = alipay.login()
    print(logins)