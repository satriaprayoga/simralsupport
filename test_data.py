from simral_data import *
from selenium import webdriver
from simral_login import  *

USERNAME="gilang_2021"
PASSWORD="1234567a"
PERIODE="PARSIAL 3 (2021-07-13 s/d 2021-08-31)"
CFG="2021"
JENIS_PERUBAHAN="Perubahan Anggaran Sebelum APBD-P"

import logging
import time

logging.basicConfig(level=logging.INFO)
driver=webdriver.Chrome(r'./chromedriver.exe')
connect_to_simral(driver)
find_captcha(driver)
print("Masukkan kode CAPTCHA:")
captcha_code=input()

if(captcha_code.isdigit()==False):
    logging.error("Format CAPTCHA salah (0-9)!")
    driver.quit()
    exit(-1)
    
login(driver,USERNAME,PASSWORD,CFG,captcha_code)
modul_setup_sikd(driver)
save_data_skpd(driver)