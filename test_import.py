from simral import import_dpa_perubahan as idp
from simral import simral_login
from selenium import webdriver


USERNAME="gilang_2021"
PASSWORD="1234567a"
PERIODE="PARSIAL 3 (2021-07-13 s/d 2021-08-31)"
CFG="2021"
JENIS_PERUBAHAN="Perubahan Anggaran Sebelum APBD-P"

import logging
import time

logging.basicConfig(level=logging.INFO)
driver=webdriver.Chrome(r'./chromedriver.exe')
simral_login.connect_to_simral(driver)
simral_login.find_captcha(driver)
print("Masukkan kode CAPTCHA:")
captcha_code=input()

if(captcha_code.isdigit()==False):
    logging.error("Format CAPTCHA salah (0-9)!")
    driver.quit()
    exit(-1)
    
simral_login.login(driver,USERNAME,PASSWORD,CFG,captcha_code)
idp.modul_perubahan(driver)
idp.pilih_kegiatan(driver,PERIODE,'[1.05.0.00.0.00.01.0000] SATUAN POLISI PAMONG PRAJA','[1.05.0.00.0.00.01.0001] Sekretariat Sat Pol PP')
idp.import_kegiatan(driver,JENIS_PERUBAHAN)
time.sleep(2)