from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

web = webdriver.Chrome()
web.get('http://127.0.0.1:7860/output')


open_btn = web.find_element(By.CLASS_NAME, 'add-event')
open_btn.click()

time.sleep(2)

#replace the sample answer with actual answer here
name = web.find_element(By.CLASS_NAME, 'event-name')
name.send_keys('Go with Friend')

eventTimef = web.find_element(By.CLASS_NAME, 'event-time-from')
eventTimef.send_keys('1500')

eventTimet = web.find_element(By.CLASS_NAME, 'event-time-to')
eventTimet.send_keys('1630')


close_btn = web.find_element(By.CLASS_NAME, 'add-event-btn')
close_btn.click()


while(True):
    pass