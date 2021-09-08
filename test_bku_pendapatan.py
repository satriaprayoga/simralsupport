from simral import simral_login
from simral import bku_pendapatan as bp
from simral import settings
from simral.sipd.Backup import *

from selenium import webdriver


import logging
import csv


USERNAME="lalapati"
PASSWORD="lalapati123"
CFG="2021"


logging.basicConfig(level=logging.INFO)

driver = webdriver.Chrome(r'./chromedriver.exe')
#driver.maximize_window()
driver.set_window_size(1250,700)
simral_login.connect_to_simral(driver)
simral_login.find_captcha(driver)

print("Masukkan kode captcha")
captcha=input()

if not captcha.isdigit():
    logging.error("Format CAPTCHA salah!")
    driver.quit()
    exit(-1)

simral_login.login(driver, USERNAME, PASSWORD, CFG, captcha)



pendapatan=[]
with open("test.csv","r") as f:
    pendapatanCsv=csv.DictReader(f)
    for d in pendapatanCsv:
       bp.modul_pendapatan(driver)
       bp.choose_skpd(driver)
       bp.input_bku_pendapatan(driver, d)
    
f.close()
driver.quit()