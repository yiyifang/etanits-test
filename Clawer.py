# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 19:28:52 2022

@author: nick
"""

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pathlib
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def getChrome():
    try:
        op = webdriver.ChromeOptions()
        #op.add_argument("--headless") #背景執行
        out_path = pathlib.Path(__file__).parent.absolute()  # 取得當前資料夾路徑
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': str(out_path)} #調整預設下載路徑
        op.add_experimental_option('prefs', prefs)
        browser = webdriver.Chrome(options=op)
        return browser
    except:
        print("chromedriver設定錯誤")
        
        
def download():
    url = "https://plvr.land.moi.gov.tw/DownloadOpenData"
    driver = getChrome()
    driver.get(url)
    
    parent = driver.current_window_handle
    uselessWindows = driver.window_handles
    for winId in uselessWindows:
        if winId != parent: 
            driver.switch_to.window(winId)
            driver.close()                   #關閉彈出分頁
    driver.switch_to.window(parent)          #切換到主頁
    
    WebDriverWait(driver,10).until(EC.visibility_of_any_elements_located((By.ID,"ui-id-2")))
    driver.find_element(By.ID, "ui-id-2").click()
    WebDriverWait(driver,10).until(EC.visibility_of_any_elements_located((By.ID,"historySeason_id")))
    select1 = Select(driver.find_element(By.ID, 'historySeason_id'))
    select1.select_by_value("108S2")
    select = Select(driver.find_element(By.ID, 'fileFormatId'))
    select.select_by_value("csv")
    driver.find_element(By.ID, "downloadBtnId").click()
    time.sleep(10)
    
if __name__ == '__main__':
    download()    
    



        