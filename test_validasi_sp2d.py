from simral import simral_login
from simral import validasi_sp2d as val
from simral import settings

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
with open("validasi.csv","r") as f:
    pendapatanCsv=csv.DictReader(f)
    for d in pendapatanCsv:
       val.modul_kasda(driver)
       data=val.find_spd2d(driver, d['no_sp2d'], d['jumlah'])
       if data:
            if data['status']=='Proses Bank':
                if(data['jumlah']==int(d['jumlah'])):
                    val.validasi_sp2d(driver,data,d['tgl_cair'])
       else:
            pass
driver.implicitly_wait(2)
driver.quit()


